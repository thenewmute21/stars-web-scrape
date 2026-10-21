#!/usr/bin/env bash
# Load the API key from the mounted Docker secret into this process only.
# It never appears in compose.yaml, `docker inspect`, or the image layers.
set -euo pipefail

SECRET_FILE=/run/secrets/anthropic_api_key
if [[ -z "${ANTHROPIC_API_KEY:-}" && -r "$SECRET_FILE" ]]; then
  ANTHROPIC_API_KEY="$(<"$SECRET_FILE")"
  export ANTHROPIC_API_KEY
fi
[[ -n "${ANTHROPIC_API_KEY:-}" ]] || { echo "ANTHROPIC_API_KEY secret missing" >&2; exit 78; }

mkdir -p "$AGENT_LOG_DIR"
echo "agent starting: key=sk-ant-***${ANTHROPIC_API_KEY: -4} workspace=$AGENT_WORKSPACE"
exec "$@"
