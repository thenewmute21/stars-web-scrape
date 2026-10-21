"""Placeholder agent: keeps the stack healthy until you point AGENT_CMD at your framework.

Serves the metrics endpoint and verifies the API key loads, then idles.
Set the real command with:  agent-ctl set-cmd "python -m myagent"
"""

import logging
import os
import time

from agent_metrics import setup_logging, start_metrics_server

setup_logging()
start_metrics_server()
log = logging.getLogger("agent_idle")
key = os.environ.get("ANTHROPIC_API_KEY", "")
log.info("idle placeholder running; API key loaded=%s; workspace=%s",
         key.startswith("sk-ant-"), os.environ.get("AGENT_WORKSPACE"))
log.info("set AGENT_CMD in /opt/agent/.env (or run: agent-ctl set-cmd \"...\") to start your agent")
while True:
    time.sleep(3600)
