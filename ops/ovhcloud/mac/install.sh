#!/usr/bin/env bash
# One-command setup from a Mac, after you've ordered the OVH VPS.
#
#   First Mac (sets up the server):   ./install.sh <SERVER_IP> [--user ubuntu]
#   Each additional Mac:              ./install.sh <SERVER_IP> --client-only
#   Shared host you already admin:    ./install.sh <SERVER_IP> --colocate <admin-ssh-alias>
#     (no bootstrap/hardening; runs colocate.sh: locked-down agent user, no sudo/docker)
#
# --user is the login OVH created (Ubuntu images: "ubuntu"; Debian: "debian").
# If you didn't add an SSH key when ordering, you'll be asked once for the
# password from OVH's delivery email; after that, password login is disabled.
set -euo pipefail

IP="${1:?usage: install.sh <SERVER_IP> [--user ubuntu] [--client-only] [--colocate <admin-alias>]}"; shift
INIT_USER=ubuntu
CLIENT_ONLY=0
ADMIN=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --user) INIT_USER="$2"; shift 2 ;;
    --client-only) CLIENT_ONLY=1; shift ;;
    --colocate) ADMIN="${2:?--colocate needs your admin ssh alias}"; shift 2 ;;
    *) echo "unknown option $1"; exit 1 ;;
  esac
done

HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(cd "$HERE/.." && pwd)"
ALIAS=ovh-agent
KEY="$HOME/.ssh/ovh_agent_ed25519"
SSH_CONFIG="$HOME/.ssh/config"
SSH_OPTS=(-i "$KEY" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15)
say() { printf '\n\033[1;34m>> %s\033[0m\n' "$*"; }

say "Local tools"
if command -v brew >/dev/null; then
  for pkg in jq rsync; do brew list --formula "$pkg" >/dev/null 2>&1 || brew install -q "$pkg"; done
else
  echo "Homebrew not found; skipping jq/rsync install (agent-ctl tokens/spend need jq)."
fi

say "SSH key for this Mac ($KEY)"
mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"
if [[ ! -f "$KEY" ]]; then
  echo "Choose a passphrase; macOS Keychain will remember it."
  ssh-keygen -t ed25519 -a 100 -f "$KEY" -C "ovh-agent@$(scutil --get LocalHostName 2>/dev/null || hostname -s)"
fi
ssh-add --apple-use-keychain "$KEY" 2>/dev/null || ssh-add "$KEY" 2>/dev/null || true

say "SSH alias '$ALIAS' in $SSH_CONFIG"
touch "$SSH_CONFIG" && chmod 600 "$SSH_CONFIG"
awk '/^# >>> ovh-agent >>>/{skip=1} !skip{print} /^# <<< ovh-agent <<</{skip=0}' "$SSH_CONFIG" > "$SSH_CONFIG.tmp"
cat >> "$SSH_CONFIG.tmp" <<EOF
# >>> ovh-agent >>>
Host $ALIAS
  HostName $IP
  User agent
  IdentityFile $KEY
  IdentitiesOnly yes
  IgnoreUnknown UseKeychain
  UseKeychain yes
  AddKeysToAgent yes
  ControlMaster auto
  ControlPath ~/.ssh/cm-%r@%h:%p
  ControlPersist 4h
  ServerAliveInterval 30
  ServerAliveCountMax 4
  Compression yes
  ForwardAgent no
# <<< ovh-agent <<<
EOF
mv "$SSH_CONFIG.tmp" "$SSH_CONFIG"

say "agent-ctl command"
BIN="$HOME/.local/bin"; mkdir -p "$BIN"
ln -sfn "$HERE/agent-ctl.sh" "$BIN/agent-ctl"
chmod +x "$HERE"/*.sh
case ":$PATH:" in *":$BIN:"*) ;; *)
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
  echo "Added ~/.local/bin to PATH in ~/.zshrc (open a new terminal)." ;;
esac

if command -v code >/dev/null; then
  say "VS Code Remote-SSH extension"
  code --install-extension ms-vscode-remote.remote-ssh >/dev/null && echo "installed"
fi

if [[ $CLIENT_ONLY -eq 1 ]]; then
  say "Checking access"
  if ssh -o BatchMode=yes "$ALIAS" true 2>/dev/null; then
    echo "This Mac can reach the server. Try: agent-ctl status"
  else
    echo "This Mac's key isn't authorized yet. On the Mac that's already set up, run:"
    echo
    echo "  agent-ctl authorize '$(cat "$KEY.pub")'"
    echo
    echo "then re-run: $0 $IP --client-only"
  fi
  exit 0
fi

if [[ -n "$ADMIN" ]]; then
  say "Installing the locked-down agent stack via your admin login '$ADMIN'"
  rsync -az --delete --exclude mac/ "$KIT/" "$ADMIN:ovhcloud/"
  ssh "$ADMIN" 'sudo bash ~/ovhcloud/colocate.sh'
  say "Authorizing this Mac's key for agent@$IP"
  ssh "$ADMIN" "sudo sh -c 'cat >> /home/agent/.ssh/authorized_keys && sort -u -o /home/agent/.ssh/authorized_keys /home/agent/.ssh/authorized_keys'" < "$KEY.pub"
  ssh -O exit "$ALIAS" 2>/dev/null || true
  if ! ssh "$ADMIN" 'sudo test -s /etc/agent/secrets/anthropic_api_key'; then
    say "Anthropic API key"
    echo "Use a dedicated key for this agent (Console → API keys), ideally in a workspace with a spend limit."
    read -rsp "Paste ANTHROPIC_API_KEY (input hidden): " AK; echo
    [[ "$AK" == sk-ant-* ]] || { echo "That doesn't look like an Anthropic key."; exit 1; }
    printf '%s' "$AK" | ssh "$ALIAS" 'sudo -n /usr/local/bin/agent-set-key'
    unset AK
  fi
  say "Verifying"
  ssh "$ALIAS" 'echo "logged in as $(whoami) on $(hostname)"; sudo -n /usr/local/bin/agent-compose ps'
  echo; echo "Done. Try: agent-ctl status | agent-ctl logs | agent-ctl code"
  exit 0
fi

say "Authorizing this Mac's key for $INIT_USER@$IP"
if ! ssh "${SSH_OPTS[@]}" -o BatchMode=yes "$INIT_USER@$IP" true 2>/dev/null; then
  # OVH emails a temporary password and forces a change at the first login, then
  # closes the session. ssh-copy-id can't do that change, so do it interactively first.
  echo "First login: enter the temporary password from OVH's delivery email."
  echo "If asked, type it again as the current password, then choose a new one (twice)."
  echo "The connection then closes by itself; that's expected."
  ssh -t -o StrictHostKeyChecking=accept-new -o PubkeyAuthentication=no "$INIT_USER@$IP" true || true
  echo "Now enter your NEW password once more so this Mac's key can be installed."
  ssh-copy-id -i "$KEY.pub" -o StrictHostKeyChecking=accept-new -o PubkeyAuthentication=no "$INIT_USER@$IP"
  ssh "${SSH_OPTS[@]}" -o BatchMode=yes "$INIT_USER@$IP" true \
    || { echo "Key login still fails. Re-run this script; the password step is safe to repeat."; exit 1; }
fi

say "Uploading setup kit"
rsync -az --delete -e "ssh ${SSH_OPTS[*]}" --exclude mac/ "$KIT/" "$INIT_USER@$IP:ovhcloud/"

KEY_ARG=""
if ! ssh "${SSH_OPTS[@]}" "$INIT_USER@$IP" 'sudo test -s /etc/agent/secrets/anthropic_api_key' 2>/dev/null; then
  say "Anthropic API key"
  echo "Use a dedicated key for this server (Console → API keys), ideally in a workspace with a spend limit."
  read -rsp "Paste ANTHROPIC_API_KEY (input hidden): " AK; echo
  [[ "$AK" == sk-ant-* ]] || { echo "That doesn't look like an Anthropic key."; exit 1; }
  # Sent over SSH stdin into a 0600 temp file; bootstrap moves it into place and shreds the temp.
  printf '%s' "$AK" | ssh "${SSH_OPTS[@]}" "$INIT_USER@$IP" 'umask 077; cat > ~/.ak_tmp'
  unset AK
  KEY_ARG="ANTHROPIC_API_KEY_FILE=\$HOME/.ak_tmp"
fi

say "Running server bootstrap (takes 3–6 minutes)"
ssh -t "${SSH_OPTS[@]}" "$INIT_USER@$IP" "sudo $KEY_ARG bash ~/ovhcloud/bootstrap.sh"

say "Verifying login as 'agent' through the alias"
ssh -O exit "$ALIAS" 2>/dev/null || true
ssh "$ALIAS" 'echo "logged in as $(whoami) on $(hostname)"; docker compose -f /opt/agent/compose.yaml ps --format "{{.Name}}: {{.Status}}"'

cat <<EOF

Done. Next:
  agent-ctl status                  health, disk, container
  agent-ctl code <project>          open /srv/agent/workspace/<project> in VS Code over SSH
  agent-ctl claude                  Claude Code in a persistent tmux session on the server
  agent-ctl set-cmd "python -m x"   run your agent framework as the background service
  agent-ctl tokens | logs | spend   watch it work

On your other Mac:  git clone this repo, then  ops/ovhcloud/mac/install.sh $IP --client-only
EOF
