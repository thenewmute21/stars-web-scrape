#!/usr/bin/env bash
# Host setup, run ON the server as root (mac/install.sh does this for you):
#   sudo bash ~/ovhcloud/bootstrap.sh
#
# Works on an OVH VPS (single NVMe disk) or a Public Cloud instance with an
# attached Block Storage volume (set DATA_DEV, default /dev/sdb if present).
# Safe to re-run.
#
# - 'agent' admin user with your SSH keys; key-only SSH, no root login
# - firewall, fail2ban, unattended security upgrades, swap, inotify limits
# - Docker Engine + compose; Node 22 + Claude Code CLI on the host for tmux sessions
# - ANTHROPIC_API_KEY stored as a root-owned secret file (never in env files, git or shell history)
# - systemd unit that keeps the agent stack running across SSH disconnects and reboots
set -euo pipefail

[[ $EUID -eq 0 ]] || { echo "run with sudo"; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA_DEV="${DATA_DEV:-/dev/sdb}"
DATA_DIR=/srv/agent
SECRETS_DIR=/etc/agent/secrets
AGENT_UID=10001   # matches the non-root user baked into docker/Dockerfile
INVOKING_USER="${SUDO_USER:-root}"
export DEBIAN_FRONTEND=noninteractive

echo ">> Packages"
apt-get update -q
apt-get -y -q -o Dpkg::Options::=--force-confold upgrade
apt-get install -y -q ufw fail2ban unattended-upgrades tmux jq git rsync ripgrep acl curl ca-certificates

echo ">> Admin user 'agent'"
id agent >/dev/null 2>&1 || useradd -m -s /bin/bash -G sudo agent
echo 'agent ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/90-agent && chmod 0440 /etc/sudoers.d/90-agent
install -d -m 700 -o agent -g agent /home/agent/.ssh
# Merge keys from the user who ran us (ubuntu/debian/root) into agent's authorized_keys.
SRC_KEYS="$(getent passwd "$INVOKING_USER" | cut -d: -f6)/.ssh/authorized_keys"
touch /home/agent/.ssh/authorized_keys
if [[ -f "$SRC_KEYS" ]]; then
  sort -u "$SRC_KEYS" /home/agent/.ssh/authorized_keys -o /home/agent/.ssh/authorized_keys
fi
chown agent:agent /home/agent/.ssh/authorized_keys && chmod 600 /home/agent/.ssh/authorized_keys
[[ -s /home/agent/.ssh/authorized_keys ]] || { echo "no SSH keys found for agent; aborting before locking SSH"; exit 1; }

echo ">> SSH hardening"
cat > /etc/ssh/sshd_config.d/10-agent-hardening.conf <<'EOF'
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
AllowAgentForwarding no
X11Forwarding no
MaxAuthTries 4
ClientAliveInterval 60
ClientAliveCountMax 5
EOF
mkdir -p /run/sshd
sshd -t
systemctl reload ssh 2>/dev/null || systemctl reload sshd

echo ">> Firewall"
ufw default deny incoming
ufw default allow outgoing
ufw limit 22/tcp
ufw --force enable
systemctl enable --now fail2ban
dpkg-reconfigure -f noninteractive unattended-upgrades

echo ">> Kernel/memory tuning"
# VS Code Remote-SSH from two Macs + the agent's file watchers need many inotify watches.
cat > /etc/sysctl.d/90-agent.conf <<'EOF'
fs.inotify.max_user_watches=1048576
fs.inotify.max_user_instances=1024
vm.swappiness=10
EOF
sysctl --system >/dev/null
if ! swapon --show | grep -q /swapfile; then
  fallocate -l 4G /swapfile && chmod 600 /swapfile && mkswap /swapfile >/dev/null && swapon /swapfile
  grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

echo ">> Data directory"
mkdir -p "$DATA_DIR"
if [[ -b "$DATA_DEV" ]] && ! findmnt -S "$DATA_DEV" >/dev/null; then
  blkid "$DATA_DEV" >/dev/null || mkfs.ext4 -L agent-data "$DATA_DEV"
  grep -q 'LABEL=agent-data' /etc/fstab \
    || echo 'LABEL=agent-data /srv/agent ext4 defaults,noatime,nofail 0 2' >> /etc/fstab
  mount -a
fi
mkdir -p "$DATA_DIR"/{workspace,state,logs,index}
chown "$AGENT_UID:$AGENT_UID" "$DATA_DIR"/{workspace,state,logs,index}
chown agent:agent "$DATA_DIR"
# Both the container user and the 'agent' login user (VS Code, tmux) can read/write everything.
setfacl -R -m u:agent:rwX -m d:u:agent:rwX -m u:$AGENT_UID:rwX -m d:u:$AGENT_UID:rwX \
  "$DATA_DIR"/{workspace,state,logs,index}
ln -sfn "$DATA_DIR/workspace" /home/agent/workspace

echo ">> Docker Engine"
if ! command -v docker >/dev/null; then
  install -m 0755 -d /etc/apt/keyrings
  DISTRO="$(. /etc/os-release && echo "$ID")"   # ubuntu or debian
  curl -fsSL "https://download.docker.com/linux/$DISTRO/gpg" -o /etc/apt/keyrings/docker.asc
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/$DISTRO $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    > /etc/apt/sources.list.d/docker.list
  apt-get update -q
  apt-get install -y -q docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi
# Global log rotation so a chatty agent can't fill the disk.
cat > /etc/docker/daemon.json <<'JSON'
{ "log-driver": "json-file", "log-opts": { "max-size": "50m", "max-file": "5" },
  "live-restore": true }
JSON
systemctl restart docker
# NOTE: the docker group is root-equivalent. Only the 'agent' admin user gets it.
usermod -aG docker agent

echo ">> Node 22 + Claude Code CLI (for interactive sessions in tmux)"
if ! command -v node >/dev/null || [[ "$(node -v)" != v22* ]]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash - >/dev/null
  apt-get install -y -q nodejs
fi
npm install -g @anthropic-ai/claude-code >/dev/null 2>&1 \
  || echo "   (Claude Code CLI install skipped; install later with: sudo npm i -g @anthropic-ai/claude-code)"

echo ">> Secrets"
install -d -m 0711 -o root -g root "$SECRETS_DIR"
if [[ ! -s "$SECRETS_DIR/anthropic_api_key" ]]; then
  if [[ -n "${ANTHROPIC_API_KEY_FILE:-}" && -s "$ANTHROPIC_API_KEY_FILE" ]]; then
    KEY="$(<"$ANTHROPIC_API_KEY_FILE")"; shred -u "$ANTHROPIC_API_KEY_FILE"
  else
    # read -s: no echo, nothing written to shell history or the process list.
    read -rsp "Paste ANTHROPIC_API_KEY (input hidden): " KEY; echo
  fi
  [[ "$KEY" == sk-ant-* ]] || { echo "doesn't look like an Anthropic key"; exit 1; }
  (umask 077; printf '%s' "$KEY" > "$SECRETS_DIR/anthropic_api_key")
  unset KEY
fi
# Container runs as AGENT_UID and must be able to read only this one file.
chown "$AGENT_UID:root" "$SECRETS_DIR/anthropic_api_key"
chmod 0400 "$SECRETS_DIR/anthropic_api_key"

echo ">> Agent stack"
install -d -o agent -g agent /opt/agent
cp -r "$HERE/docker/." /opt/agent/
cp "$HERE/agent_metrics.py" /opt/agent/
# Size the container to the box: half of RAM, leaving the rest for VS Code servers and the OS.
MEM_MB=$(( $(awk '/MemTotal/{print $2}' /proc/meminfo) / 1024 / 2 ))
CPUS=$(nproc)
if [[ ! -f /opt/agent/.env ]]; then
  cat > /opt/agent/.env <<EOF
# Edit, then: sudo systemctl reload agent   (or: agent-ctl set-cmd "...")
AGENT_CMD=python /app/agent_idle.py
AGENT_MEM_LIMIT=${MEM_MB}m
AGENT_CPUS=$(( CPUS > 2 ? CPUS - 1 : CPUS ))
EOF
fi
chown -R agent:agent /opt/agent
install -m 0644 "$HERE/systemd/agent.service" /etc/systemd/system/agent.service
systemctl daemon-reload
systemctl enable agent.service
systemctl restart agent.service

echo ">> Done."
systemctl --no-pager --lines=0 status agent.service || true
docker compose -f /opt/agent/compose.yaml ps
