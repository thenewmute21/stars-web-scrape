#!/usr/bin/env python3
"""
Tiny helper for quick, cheap tasks on OpenRouter's free models.

    python openrouter_free.py models                 # list currently-free models
    python openrouter_free.py ask "Summarize this: ..."
    python openrouter_free.py ask "..." --model meta-llama/llama-3.3-70b-instruct:free

The free list changes often, so `models` reads it live instead of hardcoding.
Free models are rate-limited and may log prompts: never send personal info or keys.

Env: OPENROUTER_API_KEY (in .env next to this file), optional OPENROUTER_FREE_MODEL.
"""
import argparse
import json
import os
import sys
import urllib.request

from intercom import load_dotenv

API = "https://openrouter.ai/api/v1"


def free_models():
    with urllib.request.urlopen(f"{API}/models", timeout=30) as resp:
        data = json.load(resp)["data"]
    free = [m for m in data
            if str(m.get("pricing", {}).get("prompt")) == "0"
            and str(m.get("pricing", {}).get("completion")) == "0"]
    return sorted(free, key=lambda m: -int(m.get("context_length") or 0))


def ask(prompt, model):
    key = os.environ.get("OPENROUTER_API_KEY") or sys.exit("Missing OPENROUTER_API_KEY")
    req = urllib.request.Request(
        f"{API}/chat/completions",
        data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "X-Title": "family-agents"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)["choices"][0]["message"]["content"]


def main():
    load_dotenv()
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("models")
    a = sub.add_parser("ask")
    a.add_argument("prompt")
    a.add_argument("--model", default=os.environ.get("OPENROUTER_FREE_MODEL"))
    args = p.parse_args()

    if args.cmd == "models":
        for m in free_models():
            print(f"{m['id']:<60} ctx={m.get('context_length')}")
        return
    model = args.model or free_models()[0]["id"]
    print(ask(args.prompt, model))


if __name__ == "__main__":
    main()
