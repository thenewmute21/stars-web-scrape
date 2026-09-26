# Prompt to paste into her Codex (first run)

Do these first, before pasting (keys must never go into the prompt itself):
1. Copy the `intercom/` folder to her machine, e.g. `~/family-agents/intercom/`.
2. Copy `intercom/.env.example` to `intercom/.env` and fill in the keys on her
   machine. Type them in directly; don't paste them through any chat.
3. Open a terminal in `~/family-agents/intercom/` and start `codex`.

Then paste everything below the line:

---

You're setting up my AI workspace. My dad built a starter kit in this folder.
Please do the following in order, and check with me before any step that
installs software or changes files outside this folder.

1. Read `AGENTS.md` and follow those rules for everything you do.
2. Check that `.env` exists and every key in `.env.example` has a value in it.
   Don't print the values. Just tell me which ones are missing.
3. Merge `codex-config.toml` into `~/.codex/config.toml`. Keep whatever settings
   are already there. Back up the old file to `~/.codex/config.toml.bak` first.
4. Make sure `OPENAI_API_KEY` and `OPENROUTER_API_KEY` get loaded into my shell
   from `.env` (for example, add a line to `~/.zshrc` or `~/.bashrc` that sources
   the file). Show me the line before you add it.
5. Test OpenRouter: run `python3 openrouter_free.py models` and pick a free model
   that supports tool calling. Put its id in the `[profiles.free]` model in
   `~/.codex/config.toml` and in `OPENROUTER_FREE_MODEL` in `.env`. Then run
   `python3 openrouter_free.py ask "Say hi in five words"`.
6. Test the intercom: run `python3 intercom.py status`. If the labels are missing,
   `python3 intercom.py once` will create them.
7. Set up `python3 intercom.py watch` to start at login (launchd on macOS, a
   systemd user service on Linux, Task Scheduler on Windows), and show me how to
   stop it. Log to `~/family-agents/intercom/watch.log`.
8. Send a test task to yourself:
   `python3 intercom.py send "Hello from setup" "Create hello.txt in the workspace containing today's date." --free`
   Then run `python3 intercom.py once` and confirm the issue got a reply.
9. Give me a short cheat sheet: how to use the default model, how to use the
   free profile, how Dad's tasks reach me, and how to pause the watcher.
