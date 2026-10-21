#!/usr/bin/env bash
# Control and observe the remote agent from the Mac terminal.
#
#   agent-ctl logs            live container logs (Ctrl-C detaches; agent keeps running)
#   agent-ctl tokens          live per-call token/cost feed from usage.jsonl
#   agent-ctl spend [hours]   token + cost totals over the last N hours (default 24)
#   agent-ctl metrics         open an SSH tunnel to Prometheus metrics on localhost:9464
#   agent-ctl top             live CPU/mem/IO of the agent container
#   agent-ctl attach          tmux session on the server for interactive work
#   agent-ctl restart|stop|start|status
set -euo pipefail

HOST="${HOST:-ovh-agent}"
COMPOSE="docker compose -f /opt/agent/compose.yaml"
USAGE=/srv/agent/logs/usage.jsonl

case "${1:-status}" in
  logs)    ssh -t "$HOST" "$COMPOSE logs -f --tail=200 agent" ;;
  tokens)
    ssh "$HOST" "tail -n 20 -F $USAGE" | jq -r --unbuffered \
      '"\(.ts|localtime|strftime("%H:%M:%S")) \(.model) in=\(.input) out=\(.output) cache_r=\(.cache_read) cache_w=\(.cache_write) $\(.cost_usd) \(.seconds)s \(.stop_reason)"'
    ;;
  spend)
    HOURS="${2:-24}"
    ssh "$HOST" "cat $USAGE" | jq -s --argjson h "$HOURS" '
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
  attach)  ssh -t "$HOST" "tmux new -A -s agent" ;;
  restart) ssh "$HOST" "sudo systemctl restart agent" ;;
  stop)    ssh "$HOST" "sudo systemctl stop agent" ;;
  start)   ssh "$HOST" "sudo systemctl start agent" ;;
  status)  ssh "$HOST" "systemctl --no-pager status agent | head -5; $COMPOSE ps; df -h /srv/agent | tail -1" ;;
  *) sed -n '2,12p' "$0"; exit 1 ;;
esac
