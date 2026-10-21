#!/usr/bin/env bash
# One-time host setup, run ON the OVH instance as root:
#   sudo bash ~/ovhcloud/bootstrap.sh
#
# - firewall, fail2ban, automatic security updates
# - persistent data volume mounted at /srv/agent
# - Docker Engine + compose plugin
# - ANTHROPIC_API_KEY stored as a root-owned secret file (never in env files, git or shell history)
# - systemd unit that keeps the agent stack running across SSH disconnects and reboots
set -euo pipefail

[[ $EUID -eq 0 ]] || { echo "run with sudo"; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA_DEV="${DATA_DEV:-/dev/sdb}"
DATA_DIR=/srv/agent
SECRETS_DIR=/etc/agent/secrets
AGENT_UID=10001   # matches the non-root user baked into docker/Dockerfile

echo ">> Firewall"
ufw default deny incoming
ufw default allow outgoing
ufw limit 22/tcp
ufw --force enable
systemctl enable --now fail2ban
dpkg-reconfigure -f noninteractive unattended-upgrades

echo ">> Persistent volume"
if [[ -b "$DATA_DEV" ]]; then
  blkid "$DATA_DEV" >/dev/null || mkfs.ext4 -L agent-data "$DATA_DEV"
  mkdir -p "$DATA_DIR"
  grep -q 'LABEL=agent-data' /etc/fstab \
    || echo 'LABEL=agent-data /srv/agent ext4 defaults,noatime,nofail 0 2' >> /etc/fstab
  mount -a
else
  echo "   $DATA_DEV not found; using root disk (data will NOT survive instance deletion)"
  mkdir -p "$DATA_DIR"
fi
mkdir -p "$DATA_DIR"/{workspace,state,logs,index}
chown -R "$AGENT_UID:$AGENT_UID" "$DATA_DIR"/{workspace,state,logs,index}
chown agent:agent "$DATA_DIR"
# Let the 'agent' login user edit files the container writes.
setfacl -R -m u:agent:rwX -m d:u:agent:rwX "$DATA_DIR" 2>/dev/null || {
  apt-get install -y acl && setfacl -R -m u:agent:rwX -m d:u:agent:rwX "$DATA_DIR"; }

echo ">> Docker Engine"
if ! command -v docker >/dev/null; then
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    > /etc/apt/sources.list.d/docker.list
  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi
# Global log rotation so a chatty agent can't fill the disk.
cat > /etc/docker/daemon.json <<'JSON'
{ "log-driver": "json-file", "log-opts": { "max-size": "50m", "max-file": "5" },
  "live-restore": true }
JSON
systemctl restart docker
# NOTE: the docker group is root-equivalent. Only the 'agent' admin user gets it.
usermod -aG docker agent

echo ">> Secrets"
install -d -m 0700 -o root -g root "$SECRETS_DIR"
if [[ ! -s "$SECRETS_DIR/anthropic_api_key" ]]; then
  # read -s: no echo, nothing written to shell history or the process list.
  read -rsp "Paste ANTHROPIC_API_KEY (input hidden): " KEY; echo
  [[ "$KEY" == sk-ant-* ]] || { echo "doesn't look like an Anthropic key"; exit 1; }
  umask 077
  printf '%s' "$KEY" > "$SECRETS_DIR/anthropic_api_key"
  unset KEY
fi
# Container runs as AGENT_UID and must be able to read only this one file.
chown "$AGENT_UID:root" "$SECRETS_DIR/anthropic_api_key"
chmod 0400 "$SECRETS_DIR/anthropic_api_key"
chmod 0711 "$SECRETS_DIR"

echo ">> Agent stack"
install -d -o agent -g agent /opt/agent
cp -r "$HERE/docker/." /opt/agent/
cp "$HERE/agent_metrics.py" /opt/agent/
chown -R agent:agent /opt/agent
install -m 0644 "$HERE/systemd/agent.service" /etc/systemd/system/agent.service
systemctl daemon-reload
systemctl enable --now agent.service

echo ">> Done. Check with: systemctl status agent; docker compose -f /opt/agent/compose.yaml ps"
