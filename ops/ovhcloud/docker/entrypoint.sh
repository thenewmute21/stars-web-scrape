#!/usr/bin/env bash
# Load the API key from the mounted Docker secret into this process only.
# It never appears in compose.yaml, `docker inspect`, or the image layers.
set -euo pipefail

SECRET_FILE=/run/secrets/anthropic_api_key
if [[ -z "${ANTHROPIC_API_KEY:-}${CLAUDE_CODE_OAUTH_TOKEN:-}" && -r "$SECRET_FILE" ]]; then
  cred="$(<"$SECRET_FILE")"
  # A subscription token (claude setup-token) only works through Claude Code;
  # an API key works for the SDK and Claude Code alike.
  if [[ "$cred" == sk-ant-oat* ]]; then export CLAUDE_CODE_OAUTH_TOKEN="$cred"; else export ANTHROPIC_API_KEY="$cred"; fi
  unset cred
fi
tail4="${ANTHROPIC_API_KEY:-${CLAUDE_CODE_OAUTH_TOKEN:-}}"
[[ -n "$tail4" ]] || { echo "Claude credential secret missing" >&2; exit 78; }

mkdir -p "$AGENT_LOG_DIR"
echo "agent starting: auth=$([[ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]] && echo subscription || echo api_key) key=sk-ant-***${tail4: -4} workspace=$AGENT_WORKSPACE"
unset tail4
exec "$@"
