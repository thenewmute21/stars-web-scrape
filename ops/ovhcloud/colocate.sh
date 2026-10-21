#!/usr/bin/env bash
# Install the agent stack on a server that ALREADY runs other production services
# (e.g. Hermes), instead of a dedicated VPS. Run ON the server as root:
#   sudo bash ~/ovhcloud/colocate.sh
#
# Unlike bootstrap.sh this changes nothing host-wide: no apt upgrade, no ufw,
# no sshd edits, no swap/sysctl, no system Node. It adds:
# - an 'agent' login user with NO sudo and NO docker group (docker = root on the host).
#   It may only run a few root-owned helpers via sudo: agent-compose (ps/logs/stats),
#   agent-set-cmd, agent-set-key, and systemctl start|stop|restart|reload agent.
# - /opt/agent root-owned, so the agent user can't edit compose.yaml to grant itself
#   privileges; only requirements.txt and Dockerfile are agent-writable (dependencies).
# - data on DATA_ROOT (default /mnt/data/agent), linked as /srv/agent.
# - Node 22 + Claude Code inside /home/agent only.
# - container capped at AGENT_CPUS / AGENT_MEM_LIMIT so production keeps priority.
# Safe to re-run. The API key is set separately (agent-set-key, via install.sh --colocate).
set -euo pipefail

[[ $EUID -eq 0 ]] || { echo "run with sudo"; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA_ROOT="${DATA_ROOT:-/mnt/data/agent}"
SECRETS_DIR=/etc/agent/secrets
AGENT_UID=10001          # container user baked into docker/Dockerfile
CPUS="${AGENT_CPUS:-2}"
MEM="${AGENT_MEM_LIMIT:-6g}"
NODE_VERSION="${NODE_VERSION:-22}"

echo ">> 'agent' login user (no sudo group, no docker group)"
id agent >/dev/null 2>&1 || useradd -m -s /bin/bash agent
gpasswd -d agent docker >/dev/null 2>&1 || true
gpasswd -d agent sudo >/dev/null 2>&1 || true
install -d -m 700 -o agent -g agent /home/agent/.ssh
touch /home/agent/.ssh/authorized_keys
chown agent:agent /home/agent/.ssh/authorized_keys && chmod 600 /home/agent/.ssh/authorized_keys

echo ">> Data on $DATA_ROOT -> /srv/agent"
# setfacl is the one package we may add (tiny, no services); everything else is host-neutral.
command -v setfacl >/dev/null \
  || DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=600 install -y -q acl >/dev/null
mkdir -p "$DATA_ROOT"/{workspace,state,logs,index}
[[ -L /srv/agent || ! -e /srv/agent ]] || { echo "/srv/agent exists and is not a symlink; refusing"; exit 1; }
ln -sfn "$DATA_ROOT" /srv/agent
chown agent:agent "$DATA_ROOT"
chown "$AGENT_UID:$AGENT_UID" "$DATA_ROOT"/{workspace,state,logs,index}
setfacl -R -m u:agent:rwX -m d:u:agent:rwX -m u:$AGENT_UID:rwX -m d:u:$AGENT_UID:rwX \
  "$DATA_ROOT"/{workspace,state,logs,index}
ln -sfn /srv/agent/workspace /home/agent/workspace

echo ">> Agent stack in /opt/agent (root-owned)"
install -d -m 0755 -o root -g root /opt/agent
for f in compose.yaml entrypoint.sh agent_idle.py cc_agent.py; do install -m 0644 "$HERE/docker/$f" /opt/agent/; done
install -m 0644 "$HERE/agent_metrics.py" /opt/agent/
# Dependencies stay editable by the agent user; keep their edits on re-run.
for f in Dockerfile requirements.txt; do
  [[ -f /opt/agent/$f ]] || install -m 0644 "$HERE/docker/$f" /opt/agent/
  chown agent:agent /opt/agent/$f
done
if [[ ! -f /opt/agent/.env ]]; then
  printf 'AGENT_CMD=python /app/agent_idle.py\nAGENT_MEM_LIMIT=%s\nAGENT_CPUS=%s\n' "$MEM" "$CPUS" > /opt/agent/.env
fi
chown root:agent /opt/agent/.env && chmod 0640 /opt/agent/.env   # readable, only agent-set-cmd writes it

echo ">> Root-owned helpers the agent user may sudo"
install -m 0755 -o root -g root "$HERE"/bin/agent-compose "$HERE"/bin/agent-set-cmd "$HERE"/bin/agent-set-key /usr/local/bin/
cat > /etc/sudoers.d/91-agent-limited <<'EOF'
agent ALL=(root) NOPASSWD: /usr/local/bin/agent-compose, /usr/local/bin/agent-set-cmd, /usr/local/bin/agent-set-key, /usr/bin/systemctl start agent, /usr/bin/systemctl stop agent, /usr/bin/systemctl restart agent, /usr/bin/systemctl reload agent
EOF
chmod 0440 /etc/sudoers.d/91-agent-limited
visudo -cf /etc/sudoers.d/91-agent-limited >/dev/null

echo ">> Node $NODE_VERSION + Claude Code for the agent user only"
if ! sudo -iu agent bash -c 'command -v node >/dev/null && [[ "$(node -v)" == v'"$NODE_VERSION"'* ]]'; then
  base="https://nodejs.org/dist/latest-v${NODE_VERSION}.x"
  tarball="$(curl -fsSL "$base/SHASUMS256.txt" | awk '/linux-x64\.tar\.xz$/{print $2}')"
  sum="$(curl -fsSL "$base/SHASUMS256.txt" | awk '/linux-x64\.tar\.xz$/{print $1}')"
  curl -fsSL "$base/$tarball" -o "/tmp/$tarball"
  echo "$sum  /tmp/$tarball" | sha256sum -c --quiet
  rm -rf /home/agent/.local/node && install -d -o agent -g agent /home/agent/.local/node
  tar -xJf "/tmp/$tarball" -C /home/agent/.local/node --strip-components=1 && rm -f "/tmp/$tarball"
  chown -R agent:agent /home/agent/.local
fi
grep -q '.local/node/bin' /home/agent/.profile 2>/dev/null \
  || echo 'export PATH="$HOME/.local/node/bin:$HOME/.local/npm/bin:$PATH"' >> /home/agent/.profile
# Top of .bashrc: Ubuntu's .bashrc returns early for non-interactive shells, and
# `ssh ovh-agent 'claude --version'` must still find node/claude.
grep -q '.local/node/bin' /home/agent/.bashrc 2>/dev/null \
  || sed -i '1i export PATH="$HOME/.local/node/bin:$HOME/.local/npm/bin:$PATH"' /home/agent/.bashrc
chown agent:agent /home/agent/.profile /home/agent/.bashrc
sudo -iu agent bash -c 'npm config set prefix "$HOME/.local/npm" && npm install -g @anthropic-ai/claude-code >/dev/null 2>&1' \
  || echo "   (Claude Code install failed; retry as agent: npm i -g @anthropic-ai/claude-code)"

echo ">> systemd unit (starts once the API key is set)"
cat > /etc/systemd/system/agent.service <<'EOF'
[Unit]
Description=Autonomous agent stack (docker compose, colocated)
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target
ConditionPathExists=/etc/agent/secrets/anthropic_api_key

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/agent
# Explicit -f: a COMPOSE_FILE line in .env must never redirect us to another compose file.
ExecStart=/usr/bin/docker compose -f /opt/agent/compose.yaml up -d --build --remove-orphans
ExecStop=/usr/bin/docker compose -f /opt/agent/compose.yaml down
ExecReload=/usr/bin/docker compose -f /opt/agent/compose.yaml up -d --build --remove-orphans
TimeoutStartSec=900

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable agent.service >/dev/null 2>&1
if [[ -s $SECRETS_DIR/anthropic_api_key ]]; then systemctl restart agent.service; fi

echo ">> Done."
systemctl --no-pager --lines=0 status agent.service || true
