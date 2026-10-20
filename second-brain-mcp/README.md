# Second Brain MCP bridge

Gives Claude Code — including sessions started from the mobile and web apps —
authenticated access to the self-hosted second brain, the same way the Codex
mobile app reaches it.

`second_brain_mcp.py` is a stdio MCP server written against the Python standard
library only. There is no `pip install` step, so the same file runs unchanged on
a laptop, in CI, and inside a Claude Code cloud container whose egress to PyPI
may be closed.

## Why mobile fails while the desktop works

A desktop client runs **on your own machine**, so it inherits that machine's
network: LAN DNS, an already-established VPN, and any private CA you have
installed. A phone app and a cloud agent have none of that. They reach the brain
from the public internet or not at all.

So a brain that answers on the desktop and fails on mobile is almost never down.
It is one of:

| Symptom at the client | Actual cause |
| --- | --- |
| Hostname does not resolve | The name is LAN-only / split-horizon DNS |
| Connection times out | VPN-only route, or a firewall dropping the packets |
| TLS verification fails | Self-signed cert, trusted only on the desktop |
| Proxy returns `403 Tunnel connection failed` | Host not on the cloud environment's allow-list |
| `401` / `403` from the brain itself | Token expired, or an ingress proxy stripping the auth header |

`second_brain_health` and `second_brain_describe` report which of these it is,
with the fix, rather than a generic failure.

The durable answer is to give the brain one publicly resolvable hostname with
authenticated ingress — a Cloudflare Tunnel keeps the host itself unexposed —
and point every client at that.

## Setup

**1. Point the bridge at the brain.** Set `SECOND_BRAIN_URL` to the public
origin, e.g. `https://brain.example.com`.

**2. Store the token as a secret, not in this repo.** Add `SECOND_BRAIN_TOKEN`
under the cloud environment's settings (environment menu in the session title
bar → Edit → Network secrets, or as an environment variable). A new session
picks it up. `.mcp.json` only references `${SECOND_BRAIN_TOKEN}`, so the value
is never committed.

**3. Allow the host.** In the same settings, under Network access, add the
brain's hostname to Allowed domains (leave the package-managers box ticked).
Without this the proxy refuses the tunnel and the bridge reports exactly that.

**4. Confirm.** Start a session and run the `second_brain_health` tool.

## Tools

| Tool | Purpose |
| --- | --- |
| `second_brain_query` | Ask a question; returns the retrieved answer. Accepts `mode` and `top_k`. |
| `second_brain_insert` | Store a note for later sessions to retrieve. |
| `second_brain_health` | Reachability check that names the cause and the fix when it fails. |
| `second_brain_describe` | Resolved config with the token redacted, plus a read-only endpoint probe. |

## Matching your server's API

Defaults follow the LightRAG server shape (`POST /query` with
`{"query", "mode"}`, `POST /documents/text`, `GET /health`), chosen because the
host runs a `lightrag-queue-guard` job. **Confirm this against the real server
before trusting it.** If the paths differ, run `second_brain_describe` to see
which respond, then override — no code change needed:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SECOND_BRAIN_URL` | — | Base origin (required) |
| `SECOND_BRAIN_TOKEN` | — | Bearer token |
| `SECOND_BRAIN_AUTH_HEADER` | `Authorization` | Header carrying the credential |
| `SECOND_BRAIN_AUTH_PREFIX` | `Bearer ` | Prefix before the token |
| `SECOND_BRAIN_QUERY_PATH` | `/query` | Retrieval endpoint |
| `SECOND_BRAIN_INSERT_PATH` | `/documents/text` | Write endpoint |
| `SECOND_BRAIN_HEALTH_PATH` | `/health` | Liveness endpoint |
| `SECOND_BRAIN_MODE` | `hybrid` | Default retrieval mode |
| `SECOND_BRAIN_TIMEOUT` | `30` | Per-request timeout, seconds |
| `SECOND_BRAIN_CA_BUNDLE` | — | PEM bundle, if the brain uses a private CA |

Responses are read loosely: the answer is taken from whichever of `response`,
`answer`, `result`, `text`, `content` or `data` is present, so a differing
schema degrades to showing the raw JSON instead of breaking.

## Testing without the real brain

```bash
python3 second-brain-mcp/second_brain_mcp.py <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
EOF
```

With `SECOND_BRAIN_URL` unset, any tool call returns the configuration error
rather than hanging — useful for checking the wiring before credentials exist.

## Scope

This bridge serves Claude Code. The ChatGPT mobile app needs the same public
ingress from step 3 but is configured on the OpenAI side (custom GPT action or
connector); it does not consume this file.

This directory is self-contained and shares nothing with the Ylopo scraper in
the repository root. It is here because it was the available repository — it
would sit more naturally in its own.
