#!/usr/bin/env python3
"""
Family agent intercom: a GitHub-Issues mailbox between Dad's Claude Code and
the kid's Codex.

    Dad / Claude Code  --(open issue, label "for-codex")-->  private repo
    Kid's machine      --(intercom.py watch)--> picks it up -> `codex exec`
                       --(comment with result, label "codex-done")--> repo

Why GitHub Issues: no server to host, every message is logged and visible to
a parent, Claude Code already has GitHub tools, and you can reply from a phone.

Stdlib only. Commands:
    python intercom.py send "Title" "Body text"        # or: --body-file task.md
    python intercom.py send "Title" "Body" --free      # route to OpenRouter free model
    python intercom.py watch                           # run on the kid's machine
    python intercom.py once                            # process pending tasks once and exit
    python intercom.py status                          # list recent tasks

Env (put these in .env next to this file, never commit it):
    GITHUB_TOKEN           fine-grained PAT, access to INTERCOM_REPO only, Issues: read/write
    INTERCOM_REPO          owner/repo, e.g. dad/family-intercom (make it PRIVATE)
    ALLOWED_SENDERS        comma list of GitHub usernames allowed to send tasks
    CODEX_WORKDIR          folder Codex works in (default: ~/codex-workspace)
    CODEX_SANDBOX          read-only | workspace-write (default) | danger-full-access
    POLL_SECONDS           default 60
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

LABEL_TASK = "for-codex"
LABEL_WORKING = "codex-working"
LABEL_DONE = "codex-done"
LABEL_FAILED = "codex-failed"
LABEL_FREE = "free-model"
MAX_COMMENT = 60000


def load_dotenv():
    env_file = Path(__file__).resolve().parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def cfg(name, default=None, required=False):
    val = os.environ.get(name, default)
    if required and not val:
        sys.exit(f"Missing {name}. Set it in intercom/.env (see .env.example).")
    return val


def gh(method, path, payload=None):
    url = f"https://api.github.com/repos/{cfg('INTERCOM_REPO', required=True)}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {cfg('GITHUB_TOKEN', required=True)}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            return json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GitHub {method} {path} -> {e.code}: {e.read().decode()[:500]}")


def ensure_labels():
    colors = {LABEL_TASK: "1f6feb", LABEL_WORKING: "d29922", LABEL_DONE: "2da44e",
              LABEL_FAILED: "cf222e", LABEL_FREE: "8250df"}
    existing = {l["name"] for l in gh("GET", "/labels?per_page=100")}
    for name, color in colors.items():
        if name not in existing:
            gh("POST", "/labels", {"name": name, "color": color})


def cmd_send(args):
    body = Path(args.body_file).read_text() if args.body_file else (args.body or "")
    labels = [LABEL_TASK] + ([LABEL_FREE] if args.free else [])
    ensure_labels()
    issue = gh("POST", "/issues", {"title": args.title, "body": body, "labels": labels})
    print(f"Sent task #{issue['number']}: {issue['html_url']}")


def pending_tasks():
    issues = gh("GET", f"/issues?state=open&labels={LABEL_TASK}&per_page=20&sort=created&direction=asc")
    allowed = {u.strip().lower() for u in cfg("ALLOWED_SENDERS", "").split(",") if u.strip()}
    out = []
    for it in issues:
        if "pull_request" in it:
            continue
        names = {l["name"] for l in it["labels"]}
        if names & {LABEL_WORKING, LABEL_DONE, LABEL_FAILED}:
            continue
        if it["user"]["login"].lower() not in allowed:
            print(f"Skipping #{it['number']}: sender {it['user']['login']} not in ALLOWED_SENDERS")
            continue
        out.append(it)
    return out


def run_codex(issue):
    workdir = Path(os.path.expanduser(cfg("CODEX_WORKDIR", "~/codex-workspace")))
    workdir.mkdir(parents=True, exist_ok=True)
    prompt = (
        f"Task #{issue['number']} from the family intercom.\n"
        f"Title: {issue['title']}\n\n{issue.get('body') or ''}\n\n"
        "When finished, end with a short summary of what you did, what changed, "
        "and anything that needs a human decision."
    )
    with tempfile.NamedTemporaryFile("r", suffix=".md", delete=False) as tmp:
        last_msg = tmp.name
    cmd = ["codex", "exec", "--skip-git-repo-check",
           "--sandbox", cfg("CODEX_SANDBOX", "workspace-write"),
           "-C", str(workdir), "--output-last-message", last_msg]
    if any(l["name"] == LABEL_FREE for l in issue["labels"]):
        cmd += ["--profile", "free"]
    cmd.append(prompt)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60 * 60)
    summary = Path(last_msg).read_text().strip() if Path(last_msg).exists() else ""
    os.unlink(last_msg)
    if not summary:
        summary = (proc.stdout or "")[-8000:]
    if proc.returncode != 0:
        summary += f"\n\n<details><summary>stderr</summary>\n\n```\n{(proc.stderr or '')[-4000:]}\n```\n</details>"
    return proc.returncode == 0, summary


def process(issue):
    n = issue["number"]
    print(f"Working on #{n}: {issue['title']}")
    gh("POST", f"/issues/{n}/labels", {"labels": [LABEL_WORKING]})
    try:
        ok, summary = run_codex(issue)
    except Exception as e:  # noqa: BLE001 - report any failure back to the sender
        ok, summary = False, f"Intercom error: {e}"
    header = "Done" if ok else "Failed"
    gh("POST", f"/issues/{n}/comments", {"body": f"**Codex: {header}**\n\n{summary}"[:MAX_COMMENT]})
    gh("DELETE", f"/issues/{n}/labels/{LABEL_WORKING}")
    gh("POST", f"/issues/{n}/labels", {"labels": [LABEL_DONE if ok else LABEL_FAILED]})
    if ok:
        gh("PATCH", f"/issues/{n}", {"state": "closed", "state_reason": "completed"})
    print(f"#{n}: {header}")


def cmd_once(_args):
    for issue in pending_tasks():
        process(issue)


def cmd_watch(_args):
    ensure_labels()
    interval = int(cfg("POLL_SECONDS", "60"))
    print(f"Watching {cfg('INTERCOM_REPO')} every {interval}s. Ctrl+C to stop.")
    while True:
        try:
            cmd_once(None)
        except Exception as e:  # noqa: BLE001 - keep the watcher alive through network blips
            print(f"Poll error: {e}")
        time.sleep(interval)


def cmd_status(_args):
    for it in gh("GET", f"/issues?state=all&labels={LABEL_TASK}&per_page=15"):
        tags = ",".join(l["name"] for l in it["labels"] if l["name"] != LABEL_TASK) or "pending"
        print(f"#{it['number']:<4} [{tags}] {it['title']}")


def main():
    load_dotenv()
    p = argparse.ArgumentParser(description="Family agent intercom")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("send", help="send a task to Codex")
    s.add_argument("title")
    s.add_argument("body", nargs="?")
    s.add_argument("--body-file")
    s.add_argument("--free", action="store_true", help="use the OpenRouter free-model profile")
    s.set_defaults(func=cmd_send)
    sub.add_parser("watch", help="poll for tasks and run them").set_defaults(func=cmd_watch)
    sub.add_parser("once", help="run pending tasks once").set_defaults(func=cmd_once)
    sub.add_parser("status", help="list recent tasks").set_defaults(func=cmd_status)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
