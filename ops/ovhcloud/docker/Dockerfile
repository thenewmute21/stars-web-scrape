# Runtime image for the agent: Python 3.12 + Node 22, non-root, no secrets baked in.
FROM python:3.12-slim-bookworm

ARG NODE_MAJOR=22
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git ripgrep tini jq gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Claude Code CLI: lets the agent run on a Claude subscription token (cc_agent.py).
RUN npm install -g @anthropic-ai/claude-code && npm cache clean --force

RUN groupadd -g 10001 agent && useradd -u 10001 -g agent -m -s /bin/bash agent

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agent_metrics.py agent_idle.py cc_agent.py entrypoint.sh ./
RUN chmod 0755 entrypoint.sh \
    && git config --system safe.directory '*'

USER agent
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    AGENT_WORKSPACE=/srv/agent/workspace \
    AGENT_LOG_DIR=/srv/agent/logs

# tini reaps zombie tool subprocesses (git, rg, node) spawned by the agent loop.
ENTRYPOINT ["/usr/bin/tini", "--", "/app/entrypoint.sh"]
CMD ["python", "/app/agent_idle.py"]
