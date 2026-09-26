# Family agents: Codex + OpenRouter + an intercom from Claude Code

```
 Dad's Claude Code ──opens issue "for-codex"──▶ private repo (mailbox) ◀──polls── her machine
        ▲                                                                          │
        └───────────── reads the reply comment ◀── intercom.py posts result ◀── codex exec
```

- **Main work** goes to Codex with OpenAI models.
- **Small tasks** go to OpenRouter free models, through `codex --profile free` or
  `openrouter_free.py ask`.
- **The intercom** is GitHub Issues in a private repo. Each task is an issue. Her
  machine runs `intercom.py watch`, sends each new task to `codex exec`, and
  posts the result back as a comment. Every message is logged, you can read it
  from your phone, and there's no server to run.

## Files
| File | Where it goes |
|---|---|
| `CODEX_BOOTSTRAP_PROMPT.md` | Paste into her Codex on first run |
| `intercom/intercom.py` | Her machine (watcher) and optionally yours (`send`) |
| `intercom/openrouter_free.py` | Her machine, for quick free-model calls |
| `intercom/codex-config.toml` | Merged into her `~/.codex/config.toml` |
| `intercom/AGENTS.md` | Her Codex house rules, read automatically |
| `intercom/.env.example` | Template for her keys. The real `.env` stays on her machine only |

## Setup (about 20 minutes)
1. **Keys, one set just for her, each with a spending cap:**
   - OpenAI: create a separate Project at platform.openai.com, set a monthly
     budget, and create a key. If she signs into Codex with a ChatGPT plan
     instead, skip the key.
   - OpenRouter: create a key at openrouter.ai/settings/keys with a credit
     limit. A $0 limit works if she only uses `:free` models.
   - GitHub: create a fine-grained token with access to **only** the intercom
     repo and Issues set to read/write.
2. **Mailbox repo:** create a **private** repo such as `yourname/family-intercom`
   and add her as a collaborator. Optionally put `AGENTS.md` in it too.
3. **Her machine:** install Codex CLI (`npm i -g @openai/codex`) and Python 3,
   copy `intercom/` over, fill in `.env`, and paste the bootstrap prompt into Codex.

## Sending her Codex a task from your Claude Code
Claude Code (web or CLI) already has GitHub tools, so you can just say:

> Open an issue in `yourname/family-intercom` titled "Tweak: use the free model
> for summaries", label it `for-codex`, and put this in the body: …

- Add the `free-model` label to run the task on the OpenRouter free profile.
- Later, say "check the reply on family-intercom #12".
- From a terminal: `python intercom.py send "Title" "Body" [--free]`, and
  `python intercom.py status` to see where tasks stand.

Only issues opened by usernames in `ALLOWED_SENDERS` get run. Anyone else's are
skipped, which matters because the watcher runs code on her computer.

## Safety defaults built in
- The keys never go in any prompt or repo. `.env` is gitignored.
- Codex runs in `workspace-write` sandbox mode inside `CODEX_WORKDIR`.
- Every task and every result is stored as an issue you can review.
- `AGENTS.md` rules cover not sharing personal info, making purchases, or posting publicly.
- OpenAI requires users under 18 to have parental permission, and OpenRouter
  free models may log prompts. Keep private info out of free-model tasks.
