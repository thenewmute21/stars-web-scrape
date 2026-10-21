#!/usr/bin/env bash
# Control and observe the remote agent from either Mac.
#
#   agent-ctl status            health, container, disk, memory
#   agent-ctl logs              live container logs (Ctrl-C detaches; agent keeps running)
#   agent-ctl tokens            live per-call token/cost feed from usage.jsonl
#   agent-ctl spend [hours]     token + cost totals over the last N hours (default 24)
#   agent-ctl metrics           SSH tunnel to Prometheus metrics on localhost:9464
#   agent-ctl top               live CPU/mem of the agent container
#   agent-ctl set-cmd "<cmd>"   set the background agent's command and restart it
#   agent-ctl code [project]    open /srv/agent/workspace/<project> in VS Code (Remote-SSH)
#   agent-ctl claude [project]  Claude Code CLI in a persistent tmux session on the server
#   agent-ctl attach            plain tmux shell on the server
#   agent-ctl clone <git-url>   clone a repo into the server workspace
#   agent-ctl authorize '<ssh-ed25519 ...>'   allow another Mac's SSH key
#   agent-ctl rotate-key        replace the Anthropic API key (input hidden)
#   agent-ctl restart|stop|start
set -euo pipefail

HOST="${HOST:-ovh-agent}"
COMPOSE="docker compose -f /opt/agent/compose.yaml"
USAGE=/srv/agent/logs/usage.jsonl
WS=/srv/agent/workspace

case "${1:-status}" in
  status)
    ssh "$HOST" "systemctl is-active agent >/dev/null && echo 'service: active' || echo 'service: INACTIVE';
      $COMPOSE ps --format '{{.Name}}: {{.Status}}'; grep ^AGENT_CMD /opt/agent/.env;
      df -h /srv/agent | tail -1 | awk '{print \"disk: \"\$3\" used / \"\$2\" (\"\$5\")\"}';
      free -h | awk '/Mem/{print \"mem: \"\$3\" used / \"\$2}'; uptime" ;;
  logs)    ssh -t "$HOST" "$COMPOSE logs -f --tail=200 agent" ;;
  tokens)
    ssh "$HOST" "touch $USAGE; tail -n 20 -F $USAGE" | jq -r --unbuffered \
      '"\(.ts|localtime|strftime("%H:%M:%S")) \(.model) in=\(.input) out=\(.output) cache_r=\(.cache_read) cache_w=\(.cache_write) $\(.cost_usd) \(.seconds)s \(.stop_reason)"'
    ;;
  spend)
    HOURS="${2:-24}"
    ssh "$HOST" "cat $USAGE 2>/dev/null" | jq -s --argjson h "$HOURS" '
      map(select(.ts > (now - $h*3600))) | group_by(.model) | map({
        model: .[0].model, calls: length,
        input: (map(.input)|add), output: (map(.output)|add),
        cache_read: (map(.cache_read)|add), cache_write: (map(.cache_write)|add),
        cost_usd: ((map(.cost_usd)|add)*100|round/100)
      })'
    ;;
  metrics)
    echo ">> http://localhost:9464/metrics  (Ctrl-C to close tunnel)"
    ssh -N -L 9464:127.0.0.1:9464 "$HOST"
    ;;
  top)     ssh -t "$HOST" "docker stats agent-agent-1" ;;
  set-cmd)
    CMD="${2:?usage: agent-ctl set-cmd \"python -m myagent\"}"
    printf '%s' "$CMD" | ssh "$HOST" 'c=$(cat); grep -v "^AGENT_CMD=" /opt/agent/.env > /opt/agent/.env.new
      printf "AGENT_CMD=%s\n" "$c" >> /opt/agent/.env.new && mv /opt/agent/.env.new /opt/agent/.env
      sudo systemctl reload agent && echo "AGENT_CMD=$c (restarted)"'
    ;;
  code)
    command -v code >/dev/null || { echo "VS Code 'code' CLI not on PATH (VS Code → Command Palette → Shell Command: Install)"; exit 1; }
    code --remote "ssh-remote+$HOST" "$WS/${2:-}"
    ;;
  claude)
    DIR="$WS/${2:-}"
    ssh -t "$HOST" "tmux new -A -s claude-${2:-main} -c '$DIR' claude"
    ;;
  attach)  ssh -t "$HOST" "tmux new -A -s main -c $WS" ;;
  clone)
    URL="${2:?usage: agent-ctl clone <git-url>}"
    ssh "$HOST" "cd $WS && git clone '$URL'"
    ;;
  authorize)
    PUB="${2:?usage: agent-ctl authorize 'ssh-ed25519 AAAA... name'}"
    [[ "$PUB" =~ ^ssh-(ed25519|rsa)\ [A-Za-z0-9+/=]+ ]] || { echo "not an SSH public key"; exit 1; }
    printf '%s\n' "$PUB" | ssh "$HOST" 'cat >> ~/.ssh/authorized_keys && sort -u -o ~/.ssh/authorized_keys ~/.ssh/authorized_keys && echo "authorized ($(wc -l < ~/.ssh/authorized_keys) keys)"'
    ;;
  rotate-key)
    read -rsp "New ANTHROPIC_API_KEY (input hidden): " AK; echo
    [[ "$AK" == sk-ant-* ]] || { echo "doesn't look like an Anthropic key"; exit 1; }
    printf '%s' "$AK" | ssh "$HOST" 'sudo sh -c "umask 077; cat > /etc/agent/secrets/anthropic_api_key.new &&
      chown 10001:root /etc/agent/secrets/anthropic_api_key.new && chmod 0400 /etc/agent/secrets/anthropic_api_key.new &&
      mv /etc/agent/secrets/anthropic_api_key.new /etc/agent/secrets/anthropic_api_key" && sudo systemctl restart agent && echo "rotated; revoke the old key in the Console"'
    unset AK
    ;;
  restart) ssh "$HOST" "sudo systemctl restart agent" ;;
  stop)    ssh "$HOST" "sudo systemctl stop agent" ;;
  start)   ssh "$HOST" "sudo systemctl start agent" ;;
  *) sed -n '2,19p' "$0"; exit 1 ;;
esac
