#!/usr/bin/env bash
# Mac -> OVH code sync. Pick one mode:
#
#   ./sync.sh mutagen  ~/code/myproj   # continuous two-way sync (recommended if files must live on the Mac)
#   ./sync.sh watch    ~/code/myproj   # one-way rsync on every save (fswatch); remote edits are NOT pulled back
#   ./sync.sh push     ~/code/myproj   # one-shot rsync
#   ./sync.sh pull     ~/code/myproj   # one-shot rsync of the agent's changes back to the Mac
#
# Requires: brew install mutagen-io/mutagen/mutagen fswatch rsync
set -euo pipefail

MODE="${1:?mode: mutagen|watch|push|pull}"
SRC="$(cd "${2:?local project dir}" && pwd)"
PROJECT="$(basename "$SRC")"
HOST="${HOST:-ovh-agent}"
DEST="/srv/agent/workspace/$PROJECT"

EXCLUDES=(.git/ node_modules/ .venv/ venv/ __pycache__/ .DS_Store dist/ build/ .next/ .pytest_cache/ .env .env.*)
RSYNC_EXCLUDES=(); for e in "${EXCLUDES[@]}"; do RSYNC_EXCLUDES+=(--exclude "$e"); done

push() {
  rsync -azh --delete "${RSYNC_EXCLUDES[@]}" "$SRC/" "$HOST:$DEST/"
}

case "$MODE" in
  push) push ;;
  pull) rsync -azh "${RSYNC_EXCLUDES[@]}" "$HOST:$DEST/" "$SRC/" ;;
  watch)
    push
    echo ">> watching $SRC (Ctrl-C to stop)"
    fswatch -o -l 0.5 --exclude '/\.git/' --exclude 'node_modules' "$SRC" \
      | while read -r _; do push; done
    ;;
  mutagen)
    IGNORES=(); for e in "${EXCLUDES[@]}"; do IGNORES+=(--ignore "${e%/}"); done
    mutagen sync terminate "$PROJECT" 2>/dev/null || true
    # two-way-resolved: both sides may edit; on a true conflict the Mac (alpha) wins.
    mutagen sync create --name "$PROJECT" --sync-mode two-way-resolved \
      --ignore-vcs "${IGNORES[@]}" \
      --default-file-mode-beta 0664 --default-directory-mode-beta 0775 \
      "$SRC" "$HOST:$DEST"
    mutagen sync monitor "$PROJECT"
    ;;
  *) echo "unknown mode $MODE"; exit 1 ;;
esac
