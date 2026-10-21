#!/usr/bin/env bash
# Provision a headless agent host on OVHcloud Public Cloud with the OpenStack CLI.
# Run from your Mac after sourcing the OpenRC file downloaded from the OVH
# Control Panel (Public Cloud > Project > Users & Roles > Download OpenRC):
#
#   brew install python-openstackclient
#   source ~/Downloads/openrc.sh          # prompts for the OpenStack user password
#   ./provision.sh
#
# Everything is idempotent-ish: re-running skips resources that already exist.
set -euo pipefail

NAME="${NAME:-agent-01}"
REGION="${OS_REGION_NAME:?source your OVH openrc.sh first}"
FLAVOR="${FLAVOR:-b3-8}"            # 2 vCPU / 8 GB. Use b3-16 if you index large repos or run local models.
IMAGE="${IMAGE:-Ubuntu 24.04}"
VOLUME_SIZE_GB="${VOLUME_SIZE_GB:-100}"
VOLUME_TYPE="${VOLUME_TYPE:-high-speed}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/ovh_agent_ed25519}"
MY_IP="${MY_IP:-$(curl -fsS https://api.ipify.org)}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo ">> Region $REGION, flavor $FLAVOR, SSH allowed from $MY_IP/32"

# 1. Dedicated SSH key (ed25519, passphrase-protected, stored in macOS Keychain).
if [[ ! -f "$SSH_KEY" ]]; then
  ssh-keygen -t ed25519 -a 100 -f "$SSH_KEY" -C "ovh-agent-$(whoami)"
  ssh-add --apple-use-keychain "$SSH_KEY" 2>/dev/null || ssh-add "$SSH_KEY"
fi
openstack keypair show agent-key >/dev/null 2>&1 \
  || openstack keypair create --public-key "$SSH_KEY.pub" agent-key

# 2. Security group: SSH from your IP only. Nothing else is exposed;
#    metrics/dashboards are reached through SSH tunnels.
if ! openstack security group show agent-sg >/dev/null 2>&1; then
  openstack security group create agent-sg --description "Agent host: SSH from admin IP only"
  openstack security group rule create --ingress --protocol tcp --dst-port 22 \
    --remote-ip "$MY_IP/32" agent-sg
fi

# 3. Persistent block volume for workspaces, indexes, logs (survives instance rebuilds).
openstack volume show agent-data >/dev/null 2>&1 \
  || openstack volume create --size "$VOLUME_SIZE_GB" --type "$VOLUME_TYPE" agent-data

# 4. Instance, bootstrapped by cloud-init (creates the 'agent' user, hardens SSH).
if ! openstack server show "$NAME" >/dev/null 2>&1; then
  openstack server create \
    --flavor "$FLAVOR" \
    --image "$IMAGE" \
    --key-name agent-key \
    --network Ext-Net \
    --security-group agent-sg \
    --user-data "$HERE/cloud-init.yaml" \
    --wait \
    "$NAME"
fi

# 5. Attach the volume (appears as /dev/sdb on OVH b3 instances).
if ! openstack server show "$NAME" -f json -c volumes_attached | grep -q "$(openstack volume show agent-data -f value -c id)"; then
  openstack server add volume "$NAME" agent-data
fi

IP="$(openstack server show "$NAME" -f json -c addresses \
  | python3 -c 'import json,sys; a=json.load(sys.stdin)["addresses"]; print([x for x in a["Ext-Net"] if ":" not in x][0])')"

cat <<EOF

>> Instance ready at $IP

Add this to ~/.ssh/config on your Mac (see mac/ssh_config for the full block):

  Host ovh-agent
    HostName $IP
    User agent
    IdentityFile $SSH_KEY

Then copy and run the bootstrap:

  scp -r "$HERE" ovh-agent:~/ovhcloud
  ssh -t ovh-agent 'sudo bash ~/ovhcloud/bootstrap.sh'
EOF
