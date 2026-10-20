#!/usr/bin/env python3
"""Second Brain MCP bridge.

Exposes a self-hosted LightRAG-style "second brain" to Claude Code as MCP
tools, speaking JSON-RPC over stdio.

Standard library only -- there is no pip install step, so the same file runs
unchanged on a laptop, inside CI, and in a Claude Code cloud container whose
egress to PyPI may be closed.

Every endpoint, path and auth header is read from the environment so that this
file does not have to be edited to match a particular server. See README.md.
"""

from __future__ import annotations

import json
import os
import socket
import ssl
import sys
import urllib.error
import urllib.request

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "second-brain"
SERVER_VERSION = "0.1.0"

# Environment variable -> (default, description). Also used by the `describe`
# tool so the documentation cannot drift away from the code.
SETTINGS = {
    "SECOND_BRAIN_URL": ("", "Base URL of the second brain, e.g. https://brain.example.com"),
    "SECOND_BRAIN_TOKEN": ("", "Bearer token. Store as an environment secret, never in this repo."),
    "SECOND_BRAIN_AUTH_HEADER": ("Authorization", "Header carrying the credential."),
    "SECOND_BRAIN_AUTH_PREFIX": ("Bearer ", "Prefix placed before the token."),
    "SECOND_BRAIN_QUERY_PATH": ("/query", "Retrieval endpoint."),
    "SECOND_BRAIN_INSERT_PATH": ("/documents/text", "Write endpoint."),
    "SECOND_BRAIN_HEALTH_PATH": ("/health", "Liveness endpoint."),
    "SECOND_BRAIN_MODE": ("hybrid", "Default retrieval mode (naive|local|global|hybrid|mix)."),
    "SECOND_BRAIN_TIMEOUT": ("30", "Per-request timeout in seconds."),
    "SECOND_BRAIN_CA_BUNDLE": ("", "PEM bundle, if the server uses a private CA."),
}

SECRET_SETTINGS = {"SECOND_BRAIN_TOKEN"}


def setting(name: str) -> str:
    value = os.environ.get(name)
    if value is None or value == "":
        return SETTINGS[name][0]
    return value


def build_ssl_context() -> ssl.SSLContext:
    ca_bundle = setting("SECOND_BRAIN_CA_BUNDLE")
    if ca_bundle:
        return ssl.create_default_context(cafile=ca_bundle)
    return ssl.create_default_context()


class BrainError(Exception):
    """A failure to reach the second brain, with an actionable cause."""

    def __init__(self, summary: str, cause: str, remedy: str):
        super().__init__(summary)
        self.summary = summary
        self.cause = cause
        self.remedy = remedy

    def render(self) -> str:
        return (
            f"{self.summary}\n\n"
            f"Likely cause: {self.cause}\n"
            f"What fixes it: {self.remedy}"
        )


def request(path: str, payload: dict | None = None, method: str = "POST") -> dict:
    """Call the second brain, translating transport failures into causes.

    The classification is the useful part: "cannot reach the second brain" is
    not actionable, whereas "DNS does not resolve, so the host is not publicly
    reachable" names the fix.
    """
    base_url = setting("SECOND_BRAIN_URL").rstrip("/")
    if not base_url:
        raise BrainError(
            "SECOND_BRAIN_URL is not set, so there is no second brain to call.",
            "The bridge has not been pointed at a server yet.",
            "Set SECOND_BRAIN_URL in the environment (see README.md).",
        )

    url = f"{base_url}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"

    token = setting("SECOND_BRAIN_TOKEN")
    if token:
        headers[setting("SECOND_BRAIN_AUTH_HEADER")] = f"{setting('SECOND_BRAIN_AUTH_PREFIX')}{token}"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    timeout = float(setting("SECOND_BRAIN_TIMEOUT"))

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=build_ssl_context()) as resp:
            body = resp.read().decode("utf-8", "replace")
        try:
            return json.loads(body) if body else {}
        except json.JSONDecodeError:
            return {"raw": body}

    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:800]
        if exc.code in (401, 403):
            raise BrainError(
                f"The second brain refused the credential (HTTP {exc.code}) at {url}.",
                "SECOND_BRAIN_TOKEN is missing, expired, or sent in the wrong header.",
                "Refresh the token and confirm SECOND_BRAIN_AUTH_HEADER matches what the "
                "server expects. A proxy in front of the brain may also be stripping the header.",
            ) from exc
        if exc.code == 404:
            raise BrainError(
                f"No endpoint at {url} (HTTP 404).",
                "The server is reachable and authenticated, but this path is wrong.",
                "Run the `second_brain_describe` tool to probe which paths respond, then set "
                "SECOND_BRAIN_QUERY_PATH / _INSERT_PATH / _HEALTH_PATH accordingly.",
            ) from exc
        raise BrainError(
            f"The second brain returned HTTP {exc.code} at {url}.",
            f"Server-side error. Response: {detail or '(empty)'}",
            "Check the service logs on the host. Note that a full disk makes a RAG store "
            "fail writes and return 5xx while still answering /health.",
        ) from exc

    except ssl.SSLCertVerificationError as exc:
        raise BrainError(
            f"TLS certificate verification failed for {url}.",
            "The certificate is self-signed or issued by a private CA that this client "
            "does not trust. A desktop machine that has the CA installed would succeed here, "
            "which is exactly how a failure looks when it only affects mobile and cloud clients.",
            "Point SECOND_BRAIN_CA_BUNDLE at the CA PEM, or put the brain behind a "
            "publicly trusted certificate.",
        ) from exc

    except urllib.error.URLError as exc:
        reason = exc.reason
        reason_text = str(reason).lower()
        if "tunnel connection failed" in reason_text or "407" in reason_text:
            raise BrainError(
                f"This environment's network policy blocked {url}.",
                "The container reaches the internet through a filtering proxy, and that proxy "
                "refused to open a tunnel to this host. In a cloud session a host that is not "
                "on the allow-list surfaces this way rather than as a DNS error, so this does "
                "not by itself mean the second brain is down.",
                "Add the host under Allowed domains in the cloud environment's Network access "
                "settings (the environment menu in the session title bar, then Edit), leaving "
                "the package managers box ticked. A new session picks it up.",
            ) from exc
        if isinstance(reason, socket.gaierror):
            raise BrainError(
                f"The hostname in {url} does not resolve.",
                "The name is private -- it resolves on your own network but not from the "
                "public internet. This is the single most common reason a phone or a cloud "
                "agent fails while the desktop on the same LAN works.",
                "Give the brain a public DNS name with authenticated ingress (a Cloudflare "
                "Tunnel is the least-exposed option), then set SECOND_BRAIN_URL to it.",
            ) from exc
        if isinstance(reason, (socket.timeout, TimeoutError)):
            raise BrainError(
                f"Connecting to {url} timed out after {timeout:g}s.",
                "Packets are being dropped rather than refused, which means a firewall, a "
                "VPN-only route, or this environment's own network policy is filtering the host.",
                "Confirm the host is reachable from outside your network, and add it under "
                "Allowed domains in the cloud environment's Network access settings.",
            ) from exc
        if isinstance(reason, ConnectionRefusedError):
            raise BrainError(
                f"The host for {url} is reachable but refused the connection.",
                "Nothing is listening on that port -- the service is probably stopped.",
                "Start the second brain service on the host and confirm the port in SECOND_BRAIN_URL.",
            ) from exc
        raise BrainError(
            f"Could not reach {url}.",
            f"Transport failure: {reason}",
            "Verify the URL, then check this environment's Network access settings allow the host.",
        ) from exc

    except socket.timeout as exc:
        raise BrainError(
            f"Request to {url} timed out after {timeout:g}s.",
            "The server accepted the connection but did not answer in time. A heavily loaded "
            "or disk-starved host does this.",
            "Check load and free disk on the host, or raise SECOND_BRAIN_TIMEOUT.",
        ) from exc


def extract_answer(result: dict) -> str:
    """Pull the answer out of a response without assuming one exact schema."""
    for key in ("response", "answer", "result", "text", "content", "data"):
        value = result.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return json.dumps(result, indent=2)[:4000]


# --- tools -----------------------------------------------------------------

TOOLS = [
    {
        "name": "second_brain_query",
        "description": (
            "Ask the second brain a question and get the retrieved answer. Use this for "
            "anything about the owner's own notes, projects, decisions or history."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The question, in natural language."},
                "mode": {
                    "type": "string",
                    "enum": ["naive", "local", "global", "hybrid", "mix"],
                    "description": "Retrieval strategy. Defaults to SECOND_BRAIN_MODE.",
                },
                "top_k": {"type": "integer", "description": "How many items to retrieve."},
            },
            "required": ["query"],
        },
    },
    {
        "name": "second_brain_insert",
        "description": "Store a note in the second brain so later sessions can retrieve it.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The note to store."},
                "description": {"type": "string", "description": "Optional label for the note."},
            },
            "required": ["text"],
        },
    },
    {
        "name": "second_brain_health",
        "description": (
            "Check whether the second brain is reachable from here, and if not, report the "
            "precise cause and its fix. Run this first when retrieval is failing."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "second_brain_describe",
        "description": (
            "Show the resolved configuration with secrets redacted, and probe the candidate "
            "endpoints to discover which paths the server actually serves."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def tool_query(args: dict) -> str:
    query = (args.get("query") or "").strip()
    if not query:
        raise BrainError("No question given.", "The `query` argument was empty.", "Pass a question.")
    payload = {"query": query, "mode": args.get("mode") or setting("SECOND_BRAIN_MODE")}
    if args.get("top_k") is not None:
        payload["top_k"] = args["top_k"]
    return extract_answer(request(setting("SECOND_BRAIN_QUERY_PATH"), payload))


def tool_insert(args: dict) -> str:
    text = (args.get("text") or "").strip()
    if not text:
        raise BrainError("No text given.", "The `text` argument was empty.", "Pass the note text.")
    payload = {"text": text}
    if args.get("description"):
        payload["description"] = args["description"]
    result = request(setting("SECOND_BRAIN_INSERT_PATH"), payload)
    return f"Stored in the second brain.\n\n{json.dumps(result, indent=2)[:1500]}"


def tool_health(_args: dict) -> str:
    result = request(setting("SECOND_BRAIN_HEALTH_PATH"), None, method="GET")
    return (
        "The second brain is reachable from this environment.\n\n"
        f"{json.dumps(result, indent=2)[:2000]}"
    )


def tool_describe(_args: dict) -> str:
    lines = ["Resolved configuration:", ""]
    for name in SETTINGS:
        if name in SECRET_SETTINGS:
            shown = "(set)" if os.environ.get(name) else "(not set)"
        else:
            value = setting(name)
            shown = value if value else "(empty)"
            if not os.environ.get(name) and value:
                shown += "  [default]"
        lines.append(f"  {name} = {shown}")

    lines += ["", "Endpoint probe:", ""]
    # Read-only probes only. The write endpoint is deliberately not exercised:
    # probing it would insert junk into the knowledge base being audited.
    probes = [
        (setting("SECOND_BRAIN_HEALTH_PATH"), "GET", None),
        (setting("SECOND_BRAIN_QUERY_PATH"), "POST", {"query": "ping", "mode": "naive"}),
    ]
    for path, method, payload in probes:
        try:
            request(path, payload, method=method)
            lines.append(f"  {method} {path} -> responded")
        except BrainError as exc:
            lines.append(f"  {method} {path} -> {exc.summary}")
    lines.append(f"  POST {setting('SECOND_BRAIN_INSERT_PATH')} -> not probed (would write)")
    return "\n".join(lines)


HANDLERS = {
    "second_brain_query": tool_query,
    "second_brain_insert": tool_insert,
    "second_brain_health": tool_health,
    "second_brain_describe": tool_describe,
}


# --- JSON-RPC over stdio ---------------------------------------------------

def handle(message: dict) -> dict | None:
    method = message.get("method")
    request_id = message.get("id")

    if method == "initialize":
        requested = (message.get("params") or {}).get("protocolVersion")
        return {
            "protocolVersion": requested or PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        }

    if method in ("notifications/initialized", "initialized"):
        return None  # notification; no reply

    if method == "ping":
        return {}

    if method == "tools/list":
        return {"tools": TOOLS}

    if method == "tools/call":
        params = message.get("params") or {}
        name = params.get("name")
        handler = HANDLERS.get(name)
        if handler is None:
            return {
                "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                "isError": True,
            }
        try:
            return {"content": [{"type": "text", "text": handler(params.get("arguments") or {})}]}
        except BrainError as exc:
            return {"content": [{"type": "text", "text": exc.render()}], "isError": True}
        except Exception as exc:  # noqa: BLE001 - surface as tool error, never crash the server
            return {
                "content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}],
                "isError": True,
            }

    if request_id is None:
        return None
    raise LookupError(method or "(no method)")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue

        request_id = message.get("id")
        try:
            result = handle(message)
        except LookupError as exc:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {exc}"},
            }
        else:
            if result is None:
                continue  # notification
            response = {"jsonrpc": "2.0", "id": request_id, "result": result}

        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
