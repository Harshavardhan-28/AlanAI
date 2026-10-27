FROM python:3.12-slim

# docker CLI for sandbox orchestration
RUN apt-get update && apt-get install -y --no-install-recommends docker.io git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /repo

COPY packages/shared/python /repo/packages/shared/python
COPY apps/worker /repo/apps/worker
COPY packages/shared/scoring /repo/packages/shared/scoring
COPY pyproject.toml /repo/

RUN pip install --no-cache-dir -e packages/shared/python -e "apps/worker[dev]"

CMD ["python", "-m", "worker.main"]
