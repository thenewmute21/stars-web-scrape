"""Token/cost metering and secret-safe logging for an Anthropic-SDK agent.

Drop-in usage inside your agent:

    import anthropic
    from agent_metrics import metered, setup_logging, start_metrics_server

    setup_logging()
    start_metrics_server()                      # :9464/metrics, loopback only in compose
    client = metered(anthropic.Anthropic())     # same API as the plain client

    msg = client.messages.create(model="claude-opus-5-5", max_tokens=16000, messages=[...])
    with client.messages.stream(model="claude-opus-5-5", max_tokens=64000, messages=[...]) as s:
        final = s.get_final_message()

Every response's `usage` is appended to $AGENT_LOG_DIR/usage.jsonl and exported
as Prometheus counters, so the Mac can tail or scrape them over SSH.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path

from prometheus_client import Counter, Histogram, start_http_server

LOG_DIR = Path(os.environ.get("AGENT_LOG_DIR", "/srv/agent/logs"))
USAGE_FILE = LOG_DIR / "usage.jsonl"

# USD per 1M tokens: (input, output, cache_write_5m, cache_read). Estimates only —
# reconcile against the Console / Usage & Cost API for billing.
PRICES = {
    "claude-opus-5-5": (4.00, 20.00, 5.00, 0.20),
    "claude-sonnet-5-5": (2.00, 10.00, 2.50, 0.20),
    "claude-haiku-5-5": (0.10, 0.50, 0.125, 0.01),
}

TOKENS = Counter("agent_tokens_total", "Tokens consumed", ["model", "kind"])
COST = Counter("agent_cost_usd_total", "Estimated spend in USD", ["model"])
REQUESTS = Counter("agent_requests_total", "Messages API calls", ["model", "stop_reason"])
LATENCY = Histogram(
    "agent_request_seconds", "Messages API wall time", ["model"],
    buckets=(1, 2, 5, 10, 20, 40, 60, 120, 300, 600),
)

_SECRET_RE = re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}")


class RedactSecrets(logging.Filter):
    """Mask anything that looks like an Anthropic key before it reaches a log sink."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = _SECRET_RE.sub("sk-ant-***REDACTED***", record.getMessage())
        record.args = None
        return True


def setup_logging(level: int = logging.INFO) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler(), logging.FileHandler(LOG_DIR / "agent.log")]
    for h in handlers:
        h.addFilter(RedactSecrets())
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )


def start_metrics_server(port: int | None = None) -> None:
    start_http_server(port or int(os.environ.get("AGENT_METRICS_PORT", "9464")))


def record_usage(message, elapsed: float, tag: str | None = None) -> None:
    """Export one Messages API response's usage block."""
    model = message.model
    u = message.usage
    counts = {
        "input": u.input_tokens or 0,
        "output": u.output_tokens or 0,
        "cache_write": getattr(u, "cache_creation_input_tokens", 0) or 0,
        "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0,
    }
    p_in, p_out, p_cw, p_cr = PRICES.get(model, (0, 0, 0, 0))
    cost = (
        counts["input"] * p_in + counts["output"] * p_out
        + counts["cache_write"] * p_cw + counts["cache_read"] * p_cr
    ) / 1_000_000

    for kind, n in counts.items():
        TOKENS.labels(model, kind).inc(n)
    COST.labels(model).inc(cost)
    REQUESTS.labels(model, message.stop_reason or "none").inc()
    LATENCY.labels(model).observe(elapsed)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with USAGE_FILE.open("a") as f:
        f.write(json.dumps({
            "ts": time.time(), "model": model,
            # streamed final messages carry no _request_id (anthropic 2.x)
            "request_id": getattr(message, "_request_id", None),
            "stop_reason": message.stop_reason, "seconds": round(elapsed, 2),
            "cost_usd": round(cost, 6), "tag": tag, **counts,
        }) + "\n")


class _MeteredStream:
    def __init__(self, manager):
        self._manager = manager
        self._stream = None
        self._t0 = 0.0

    def __enter__(self):
        self._t0 = time.monotonic()
        self._stream = self._manager.__enter__()
        return self._stream

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            try:
                record_usage(self._stream.get_final_message(), time.monotonic() - self._t0)
            except Exception:  # metering must never break the agent loop
                logging.getLogger(__name__).exception("usage metering failed")
        return self._manager.__exit__(exc_type, exc, tb)


class _MeteredMessages:
    def __init__(self, messages):
        self._messages = messages

    def create(self, **kwargs):
        t0 = time.monotonic()
        message = self._messages.create(**kwargs)
        if not kwargs.get("stream"):
            try:
                record_usage(message, time.monotonic() - t0)
            except Exception:  # metering must never break the agent loop
                logging.getLogger(__name__).exception("usage metering failed")
        return message

    def stream(self, **kwargs):
        return _MeteredStream(self._messages.stream(**kwargs))

    def __getattr__(self, name):
        return getattr(self._messages, name)


class metered:
    """Wrap an `anthropic.Anthropic` client; `.messages` calls are metered, the rest pass through."""

    def __init__(self, client):
        self._client = client
        self.messages = _MeteredMessages(client.messages)

    def __getattr__(self, name):
        return getattr(self._client, name)


def record_claude_code(result: dict, elapsed: float, tag: str | None = None) -> None:
    """Export one `claude -p --output-format json` result (Claude Code, e.g. on a subscription token)."""
    u = result.get("usage") or {}
    counts = {
        "input": u.get("input_tokens", 0) or 0,
        "output": u.get("output_tokens", 0) or 0,
        "cache_write": u.get("cache_creation_input_tokens", 0) or 0,
        "cache_read": u.get("cache_read_input_tokens", 0) or 0,
    }
    model = next(iter(result.get("modelUsage") or {}), "claude-code")
    cost = float(result.get("total_cost_usd") or 0)   # Claude Code's own estimate; a subscription isn't billed per token
    stop = "error" if result.get("is_error") else (result.get("subtype") or "success")
    for kind, n in counts.items():
        TOKENS.labels(model, kind).inc(n)
    COST.labels(model).inc(cost)
    REQUESTS.labels(model, stop).inc()
    LATENCY.labels(model).observe(elapsed)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with USAGE_FILE.open("a") as f:
        f.write(json.dumps({
            "ts": time.time(), "model": model, "request_id": result.get("session_id"),
            "stop_reason": stop, "seconds": round(elapsed, 2), "cost_usd": round(cost, 6),
            "tag": tag, **counts,
        }) + "\n")
