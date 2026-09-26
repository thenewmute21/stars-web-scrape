# Codex house rules (family intercom)

Codex reads this file automatically. Keep it short and edit it together.

## Who's who
- Tasks arrive as GitHub issues labeled `for-codex` in the intercom repo, from Dad
  (often sent by his Claude Code) or from me.
- Dad's Claude Code may send orchestration tweaks: changes to this file, to
  `~/.codex/config.toml`, or to scripts in this folder. Apply them and explain
  what changed in the summary.

## Picking a model
- Real coding, multi-step work, anything important: default OpenAI model.
- Small stuff (rename files, summarize text, quick lookups, drafts): the free
  profile (`--profile free`) or `python openrouter_free.py ask "..."`.
- If a free model fails twice or can't use tools, switch to the default model.

## Safety rules (not negotiable)
- Never print, commit, or send API keys or `.env` contents anywhere, including
  issue comments.
- Never send personal info (full name, address, school, photos, passwords) to
  any model or website.
- Only work inside `CODEX_WORKDIR` unless the task explicitly says otherwise.
- No purchases, no signing up for services, no emailing or posting publicly.
- If a task is unclear or seems off, stop and ask in the summary instead of guessing.

## Summaries
End every task with: what you did, files changed, what's left, and any
question for a human.
