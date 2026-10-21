# Offloading a Claude-powered agent to OVHcloud

Blueprint for running a long-lived autonomous agent (multi-turn loops, codebase
indexing, tool execution) on OVHcloud, leaving the Mac Studio as a thin editor.

```
 Mac Studio (editor only)                   OVHcloud (GRA / SBG / BHS)                     Anthropic API
┌──────────────────────────┐   SSH :22    ┌──────────────────────────────────────┐  HTTPS  ┌──────────────┐
│ VS Code Remote-SSH       │─────────────▶│ b3-8 / VPS  Ubuntu 24.04             │────────▶│ /v1/messages │
│  or Mutagen two-way sync │  (multiplex) │  systemd ─▶ docker compose           │         └──────────────┘
│ agent-ctl.sh             │◀── tunnels ──│   └─ agent container (non-root, ro)  │  HTTPS  ┌──────────────┐
│  logs / tokens / metrics │   :9464      │        reads/writes /srv/agent/*     │────────▶│ OVH AI       │
└──────────────────────────┘              │  /srv/agent = Block Storage volume   │ (opt.)  │ Endpoints    │
                                          └──────────────────────────────────────┘         └──────────────┘
```

| File | Runs on | Purpose |
|---|---|---|
| `provision.sh` | Mac | OpenStack CLI: keypair, firewall group, volume, instance |
| `cloud-init.yaml` | OVH (first boot) | `agent` user, SSH hardening, base packages |
| `bootstrap.sh` | OVH (once, sudo) | ufw, fail2ban, volume mount, Docker, API-key secret, systemd unit |
| `docker/` | OVH | Python 3.12 + Node 22 non-root image, compose stack, secret-loading entrypoint |
| `systemd/agent.service` | OVH | Keeps the stack up across SSH disconnects and reboots |
| `agent_metrics.py` | OVH (in container) | Token/cost metering → `usage.jsonl` + Prometheus; key redaction in logs |
| `mac/ssh_config` | Mac | Multiplexed, keychain-backed SSH alias `ovh-agent` |
| `mac/sync.sh` | Mac | Mutagen / rsync / fswatch sync modes |
| `mac/agent-ctl.sh` | Mac | Logs, live token feed, spend report, metrics tunnel, restart |
| `git/post-receive` | OVH | `git push ovh main` → deploy + restart |

---

## 1. Architecture

### A) Fully headless on one OVH instance (recommended starting point)

The entire agent (loop, context store, file index, tool execution) runs in a Docker
container on one instance. The Mac only edits code and watches logs.

| | |
|---|---|
| **Pros** | One box, one bill, simple. File ops are local-disk fast (NVMe, µs latency). The workload is I/O- and wait-bound (most wall time is waiting on the API), so 2–4 vCPU is enough. |
| **Cons** | Single point of failure (mitigated by the volume + snapshots). Any local model (embeddings, parsers) competes with the agent for CPU/RAM. |
| **Size** | Public Cloud **b3-8** (2 vCPU / 8 GB, ~€40/mo) is the minimum for a loop + ripgrep/tree-sitter index of a few repos. **b3-16** (4 vCPU / 16 GB) if you index large monorepos or run CPU embeddings. A VPS (≥4 vCore / 8 GB tier) is cheaper but has no OpenStack API, so you provision it in the Control Panel and skip `provision.sh`. Check `openstack flavor list` for current names/prices in your region. |

Docker vs tmux: use **both, for different jobs**. Docker + systemd is the
production path (auto-restart, resource limits, no dependency on your shell).
`tmux` (`agent-ctl attach`) is for interactive sessions such as running an agent
CLI by hand, and it also survives disconnects.

### B) Hybrid: headless host + OVH AI Endpoints / AI Deploy for auxiliary models

Same host as A, but GPU- or RAM-heavy *non-reasoning* work is moved off it:

| Task | Where | Notes |
|---|---|---|
| Planning, coding, tool decisions | **Anthropic API** (`claude-opus-5-5`) | Unchanged. All reasoning stays on Claude. |
| Embeddings for semantic code search | **OVH AI Endpoints** (serverless, OpenAI-compatible, pay-per-token) | Pick an embedding model from the AI Endpoints catalog (e.g. a BGE-M3-class model). EU-hosted, no GPU to manage. |
| Custom/private parsers, OCR, rerankers | **OVH AI Deploy** (`ovhai app run <image> --gpu 1 ...`) | Container on a GPU billed per minute; scale to 0 when idle. Use only when no serverless model fits. |
| Vector store | On the host (pgvector / Qdrant / sqlite-vec on `/srv/agent/index`) | Keep it next to the agent; it's queried on every turn. |

```python
# Embedding call from the agent host to OVH AI Endpoints (OpenAI-compatible REST).
import os, requests
r = requests.post(
    os.environ["OVH_EMBED_URL"],            # copy the model's endpoint URL from the AI Endpoints catalog
    headers={"Authorization": f"Bearer {os.environ['OVH_AI_ENDPOINTS_TOKEN']}"},
    json={"model": os.environ["OVH_EMBED_MODEL"], "input": chunks},
    timeout=60,
)
vectors = [d["embedding"] for d in r.json()["data"]]
```
Store `OVH_AI_ENDPOINTS_TOKEN` exactly like the Anthropic key (a second Docker secret).

**Recommendation:** start with **A**. Move to **B** only when `agent-ctl top`
shows local embedding/parsing pinning the CPU or pushing you to a bigger flavor.
A b3-8 plus pay-per-token embeddings is usually cheaper than a b3-32.

### Network, latency and persistence

- **Keep the codebase on the server's disk.** The agent does thousands of small
  reads per loop (grep, open, stat). Local NVMe makes them microseconds. Never point
  the agent at a Mac directory over `sshfs`/NFS: every file op would then cost a WAN
  round trip (20–150 ms), and an index build would take hours.
- **API latency doesn't matter much.** A round trip from Europe to the Anthropic
  API adds roughly 80–150 ms to a Messages call that already takes seconds to
  generate. Choose the region close to *you* (GRA/SBG for Europe, BHS for North
  America) so SSH and the editor feel responsive. Use streaming for long outputs
  so idle TCP timeouts can't kill a request.
- **Mac ↔ server traffic is small:** keystrokes, file diffs and log lines.
  `ControlMaster` in `mac/ssh_config` reuses one SSH connection, so `rsync`,
  `mutagen`, VS Code and `agent-ctl` don't pay a fresh handshake each time.
- **Persistence:**
  - `/srv/agent` is an **OVH Block Storage volume** (`high-speed`). It survives
    instance deletion and rebuilds. Layout: `workspace/` (code), `state/`
    (conversation checkpoints, so the agent can resume after a restart), `index/`,
    `logs/`.
  - The instance root disk is disposable. Rebuild it at will.
  - Back up with volume snapshots: `openstack volume snapshot create --volume agent-data --force agent-data-$(date +%F)`.
    Run that from a weekly cron on the Mac. Also push the `workspace/` repos to Git.
  - Have the agent write its context state to `/srv/agent/state` after every turn
    (append-only JSONL). With `restart: unless-stopped`, a crashed container
    then resumes where it left off, not from scratch.

---

## 2. Provisioning and deployment

### 2.1 Prerequisites (Mac)

```bash
brew install python-openstackclient jq mutagen-io/mutagen/mutagen fswatch rsync
# OVH Control Panel → Public Cloud → your project → Users & Roles → create user
# (role: Administrator or Compute Operator) → "Download OpenStack's RC file" for your region.
source ~/Downloads/openrc.sh
openstack flavor list | grep -E 'b3-(8|16)'      # confirm flavor names/prices in your region
openstack image list | grep -i ubuntu
```

### 2.2 Provision (Mac)

```bash
cd ops/ovhcloud
FLAVOR=b3-8 VOLUME_SIZE_GB=100 ./provision.sh
```
This creates a passphrase-protected ed25519 key, a security group allowing **only
your current IP** on port 22, a 100 GB high-speed volume, and the instance with
`cloud-init.yaml`. Paste the printed `HostName` into `mac/ssh_config` and append
that block to `~/.ssh/config`.

Equivalent manual commands:
```bash
openstack keypair create --public-key ~/.ssh/ovh_agent_ed25519.pub agent-key
openstack security group create agent-sg
openstack security group rule create --ingress --protocol tcp --dst-port 22 --remote-ip "$(curl -s https://api.ipify.org)/32" agent-sg
openstack volume create --size 100 --type high-speed agent-data
openstack server create --flavor b3-8 --image "Ubuntu 24.04" --key-name agent-key \
  --network Ext-Net --security-group agent-sg --user-data cloud-init.yaml --wait agent-01
openstack server add volume agent-01 agent-data
```

### 2.3 Bootstrap (server)

```bash
scp -r ops/ovhcloud ovh-agent:~/ovhcloud
ssh -t ovh-agent 'sudo bash ~/ovhcloud/bootstrap.sh'    # prompts for the API key with hidden input
```
What it does:
1. `ufw` default-deny inbound, SSH rate-limited; `fail2ban`; unattended security upgrades.
2. Formats (first run only) and mounts the volume at `/srv/agent` by label, with `nofail`.
3. Installs Docker Engine from Docker's apt repo, with global log rotation (50 MB × 5).
4. Saves the API key to `/etc/agent/secrets/anthropic_api_key`, mode `0400`, readable only by the container's UID.
5. Installs and starts `agent.service`, which runs `docker compose up -d --build`.

### 2.4 Plug in your agent

- Put your framework's code in `/srv/agent/workspace/` (clone it there, or sync it, see §3).
- Set `command:` in `/opt/agent/compose.yaml` to its entrypoint (e.g. `["python", "-m", "myagent.main"]` or `["node", "dist/index.js"]`).
- Add its dependencies to `/opt/agent/requirements.txt` (or add an `npm ci` step to the Dockerfile).
- Wire up metering, which takes three lines:

```python
import anthropic
from agent_metrics import metered, setup_logging, start_metrics_server

setup_logging()
start_metrics_server()
client = metered(anthropic.Anthropic())   # reads ANTHROPIC_API_KEY loaded by entrypoint.sh

with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    cache_control={"type": "ephemeral"},  # cache the growing prefix; long loops get much cheaper
    messages=history,
    tools=tools,
) as stream:
    response = stream.get_final_message()
```

Apply changes: `sudo systemctl reload agent`, which rebuilds the image and restarts the container.

### 2.5 Secret handling: rules

| Do | Don't |
|---|---|
| Keep the key in a root-owned `0400` file, mounted as a compose **secret** (`/run/secrets/...`) | Put it in `compose.yaml` `environment:`, a `.env` in the repo, the Dockerfile, or `ENV` |
| Enter it with `read -rs` (no echo, no history) | `export ANTHROPIC_API_KEY=...` in an interactive shell, which lands in `~/.bash_history` |
| Use a **dedicated API key** for this host in its own Console workspace, with a spend limit | Reuse your personal or other production keys |
| Redact `sk-ant-…` in every log sink (`RedactSecrets` filter) | Log request headers or `os.environ` |
| Rotate: write the new key to the file, then `sudo systemctl restart agent`, then revoke the old key | Leave old keys active |

`docker inspect` does not show the key: it is loaded from the secret file at
process start, so it never appears in the container config.

---

## 3. Mac → OVH workflow

Pick one source of truth. Most sync pain comes from the agent and you editing the
same file on different machines.

### Option 1 (recommended): VS Code / Cursor Remote-SSH, code lives only on the server

1. Install the **Remote - SSH** extension. Run `Remote-SSH: Connect to Host…` and choose `ovh-agent`.
2. `File → Open Folder → /srv/agent/workspace/<project>`.
3. The VS Code server, language servers, linters and file watcher all run **on OVH**.
   The Mac renders the UI only, so it stays responsive.
4. The integrated terminal is a shell on the server. `tmux new -A -s dev` keeps it alive.
5. Edits are written straight to the disk the agent uses. There is nothing to sync and no conflicts can occur.

Settings that help (`settings.json` on the Mac):
```json
{
  "remote.SSH.useLocalServer": true,
  "remote.SSH.connectTimeout": 30,
  "files.watcherExclude": { "**/node_modules/**": true, "**/.venv/**": true, "/srv/agent/index/**": true }
}
```

### Option 2: files stay on the Mac, with continuous two-way sync (Mutagen)

```bash
ops/ovhcloud/mac/sync.sh mutagen ~/code/myproj   # Mac ⇄ /srv/agent/workspace/myproj
```
Sync takes under a second per save and is bidirectional, so the agent's edits show up locally. On a real
conflict the Mac wins (`two-way-resolved`). `.git`, `node_modules`, venvs and
`.env*` are never synced, so secrets on the Mac stay on the Mac.

Use `sync.sh watch` (one-way rsync via fswatch) only when the agent must not write
back, e.g. a read-only analysis agent.

### Option 3: Git push to deploy

```bash
# server, once:
git init --bare ~/repos/myproj.git && cp ~/ovhcloud/git/post-receive ~/repos/myproj.git/hooks/
# Mac:
git remote add ovh ovh-agent:repos/myproj.git
git push ovh main     # checks out into /srv/agent/workspace/myproj and reloads the agent
```
Best for versioned releases of the **agent code itself**. Combine it with Option 1
or 2 for the codebases the agent works *on*.

---

## 4. Diagnostics and monitoring

Install the helper: `ln -s "$PWD/ops/ovhcloud/mac/agent-ctl.sh" /usr/local/bin/agent-ctl`

| Need | Command (on the Mac) | Mechanism |
|---|---|---|
| Live logs | `agent-ctl logs` | `docker compose logs -f` over SSH. Ctrl-C detaches and the agent keeps running |
| Live token / cost feed | `agent-ctl tokens` | `tail -F usage.jsonl` piped to local `jq`: one line per API call with in/out/cache tokens, $, latency, stop reason |
| Spend report | `agent-ctl spend 24` | Per-model totals over N hours |
| Metrics | `agent-ctl metrics`, then open `http://localhost:9464/metrics` | SSH tunnel to a Prometheus endpoint bound to `127.0.0.1` on the server |
| Resource usage | `agent-ctl top` | `docker stats` |
| Health | `agent-ctl status` | systemd + compose + disk usage |

Example `agent-ctl tokens` output:
```
14:02:11 claude-opus-5-5 in=1830 out=912 cache_r=48210 cache_w=0 $0.0352 9.4s tool_use
14:02:24 claude-opus-5-5 in=2410 out=1504 cache_r=49120 cache_w=2410 $0.0616 13.1s tool_use
```

Exported Prometheus series: `agent_tokens_total{model,kind}`,
`agent_cost_usd_total{model}`, `agent_requests_total{model,stop_reason}`,
`agent_request_seconds{model}`. For dashboards, run Grafana locally on the Mac and point a
Prometheus scrape job at `localhost:9464` through the tunnel. No dashboard
port is ever opened on the server.

What to watch:
- **`cache_r` near 0 on consecutive turns**: something in your prefix changes
  every turn (a timestamp in the system prompt, tool order), and you're paying
  full input price for the whole history.
- **`stop_reason=max_tokens`**: raise `max_tokens` (stream it).
- **`stop_reason=refusal`** spikes: inspect `stop_details` in your loop.
- **Costs**: the `$` figures are estimates from the price table in
  `agent_metrics.py`. The Anthropic Console (or the Usage & Cost Admin API) is
  the billing source of truth. Set a **workspace spend limit** in the Console as a
  hard stop for a runaway loop.

Alerts (optional): a cron on the server that checks
`jq -s 'map(select(.ts>now-3600).cost_usd)|add' usage.jsonl` against a threshold
and calls `systemctl stop agent` plus a webhook if the hourly spend is exceeded.

---

## Security checklist

- [ ] SSH: key-only, no root, no passwords (cloud-init); port 22 allowed only from your IP (security group **and** ufw)
- [ ] `ForwardAgent no`: autonomous code must never get access to your Mac's SSH keys
- [ ] The container runs as UID 10001 with a read-only root fs, `cap_drop: ALL`, `no-new-privileges`, and memory/pid limits
- [ ] Only `/srv/agent/*` is writable inside the container. The agent cannot touch the host or its secrets
- [ ] No inbound ports besides SSH. Metrics are on `127.0.0.1` and reached through a tunnel
- [ ] Dedicated Anthropic key with a workspace spend limit, stored `0400` and loaded as a compose secret
- [ ] `docker` group membership = root on the host. Give it only to the admin user (or use rootless Docker)
- [ ] The agent executes model-generated commands: keep personal credentials (cloud keys, GitHub tokens with broad scope) **off** this host. Use fine-grained, repo-scoped tokens
- [ ] Unattended upgrades on. Rebuild the image monthly (`docker compose build --pull`)
- [ ] Volume snapshots scheduled. Workspaces pushed to Git
- [ ] If your IP changes, update the rule: `openstack security group rule create ... --remote-ip NEW/32` (or put the box behind Tailscale/WireGuard and close 22 publicly)
