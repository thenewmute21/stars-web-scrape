"""Minimal 24/7 agent: runs Claude Code headless on each task file dropped in the inbox.

  /srv/agent/state/inbox/<name>.md     task prompt (plain text); first line may be
                                       `cwd: <dir under the workspace>`
  /srv/agent/state/outbox/<name>.json  Claude Code's JSON result
  /srv/agent/state/done/<name>.md      the processed task

Runs only when a task arrives, so it never spends tokens on its own. Every run's
usage goes to usage.jsonl (agent-ctl tokens / spend) and the Prometheus metrics.
Set with: agent-ctl set-cmd "python /app/cc_agent.py"
"""

import json
import logging
import os
import subprocess
import time
from pathlib import Path

from agent_metrics import record_claude_code, setup_logging, start_metrics_server

STATE = Path(os.environ.get("AGENT_STATE_DIR", "/srv/agent/state"))
WS = Path(os.environ.get("AGENT_WORKSPACE", "/srv/agent/workspace"))
INBOX, OUTBOX, DONE = STATE / "inbox", STATE / "outbox", STATE / "done"
TIMEOUT_S = int(os.environ.get("AGENT_TASK_TIMEOUT_S", "3600"))

setup_logging()
start_metrics_server()
log = logging.getLogger("cc_agent")
for d in (INBOX, OUTBOX, DONE):
    d.mkdir(parents=True, exist_ok=True)
log.info("cc_agent ready; drop tasks in %s", INBOX)


def run(task: Path) -> None:
    prompt = task.read_text()
    cwd = WS
    first, _, rest = prompt.partition("\n")
    if first.startswith("cwd:"):
        cand = (WS / first[4:].strip()).resolve()
        if cand.is_dir() and (cand == WS.resolve() or WS.resolve() in cand.parents):
            cwd, prompt = cand, rest
    t0 = time.monotonic()
    # bypassPermissions is acceptable only because the container is the sandbox:
    # non-root, read-only root fs, cap_drop ALL, and only /srv/agent/* is writable.
    p = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "json", "--permission-mode", "bypassPermissions"],
        cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT_S,
    )
    elapsed = time.monotonic() - t0
    try:
        result = json.loads(p.stdout)
    except json.JSONDecodeError:
        result = {"is_error": True, "result": (p.stdout or p.stderr)[-4000:], "exit_code": p.returncode}
    (OUTBOX / f"{task.stem}.json").write_text(json.dumps(result, indent=1))
    try:
        record_claude_code(result, elapsed, tag=task.stem)
    except Exception:  # metering must never break the loop
        log.exception("usage metering failed")
    task.rename(DONE / task.name)
    log.info("task %s done in %.1fs error=%s", task.name, elapsed, bool(result.get("is_error")))


while True:
    for task in sorted(INBOX.glob("*.md")):
        try:
            run(task)
        except Exception:
            log.exception("task %s failed", task.name)
            task.rename(DONE / f"{task.name}.failed")
    time.sleep(5)
