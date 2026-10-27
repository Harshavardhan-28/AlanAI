# MCP Audit — Architecture

## What this is

A security audit + risk-scoring marketplace for MCP (Model Context Protocol) servers. Anyone can
publish an MCP (GitHub repo, npm/PyPI package, Docker image, or remote endpoint URL). Every
version is pinned (commit SHA / digest), audited by a fan-out of independent audit agents, and
assigned a deterministic, explainable risk score (0–100, higher = riskier) with a verdict tier.
Users consume MCPs through a CLI + gateway that enforces verdicts, pins versions, and scans tool
descriptions/results for prompt injection at runtime.

## Components

```
                          ┌──────────────┐
                          │   apps/web   │  Next.js marketplace UI
                          └──────┬───────┘
                                 │ HTTPS (OpenAPI contract)
        ┌────────────────────────┼─────────────────────────┐
        │                        │                         │
┌───────▼───────┐      ┌─────────▼────────┐      ┌─────────▼─────────┐
│ packages/cli  │      │     apps/api     │      │ packages/gateway  │
│  mcpaudit CLI │─────▶│  FastAPI + PG    │◀─────│  MCP proxy +      │
└───────────────┘      │  (REST, RBAC)    │      │  verdict enforce  │
                       └───┬────┬────┬───┘      └─────────┬─────────┘
                           │    │    │                    │ polls verdicts/revocations
              Postgres ◀───┘    │    └──▶ Redis (arq queue, cache, revocations)
                                │
                       ┌────────▼─────────┐      ┌───────────────────┐
                       │   apps/worker    │─────▶│  infra/sandbox    │
                       │ ingestion +      │      │  hardened Docker, │
                       │ audit DAG,       │      │  egress proxy,    │
                       │ agents, scoring, │      │  honeytokens      │
                       │ scheduler, docs  │      └───────────────────┘
                       └────────┬─────────┘
                                │ snapshots + evidence
                          MinIO (S3)
```

## Data flow (submit → verdict)

1. **Submit**: `POST /v1/mcps` with a source (github URL / npm / pypi / docker / remote URL).
2. **Ingestion** (WS-B, `apps/worker/ingest`): fetches the source **without executing it**, pins to
   an immutable reference (commit SHA, package tarball digest, image digest), extracts a manifest
   + tool list, stores a source snapshot in S3, creates `McpVersion`, enqueues an `Audit`.
3. **Orchestration** (WS-C, `apps/worker/orchestrator`): fans out the audit across all registered
   agents in parallel with per-agent timeouts/budgets; collects `AgentResult`s; persists
   `Finding`s and `AuditAgentRun`s; emits live status events on Redis.
4. **Agents** (WS-D*, WS-E): each implements `AuditAgent.run(AuditContext) -> AgentResult`.
   Deterministic checks first; LLM judgment second (schema-validated, mockable offline).
5. **Scoring** (WS-F, `apps/worker/scoring`): aggregates findings using a **versioned config**
   (`packages/shared/scoring/scoring.v1.yaml`). Hard-fail rules (confirmed exfil, download-exec,
   injection payload, known-malicious dependency, N credible community reports) force `DANGEROUS`.
   Every score stores config version + agent versions + inputs for reproducibility.
6. **Serve**: API exposes score, findings, version timeline, diffs, docs. Web renders it.
7. **Enforce**: `mcpaudit check/install` and the gateway query the verdict endpoint, pin versions,
   block `DANGEROUS`/unverified servers, and scan tool descriptions + results for injection at
   runtime. Revocations propagate via the revocations endpoint (poll) — and are written instantly
   by the community fast-path quarantine.
8. **Re-audit** (WS-G): cron scheduler re-audits on tier/popularity cadence, on rule/agent
   version bumps, and on remote-endpoint tool-list drift. Score history powers trend charts.

## Trust boundaries

- **Untrusted MCP code runs only in the sandbox** (`infra/sandbox`). Host, API, and worker never
  execute fetched code. Ingestion is pure fetch + static extraction.
- **All MCP content is untrusted data**: tool descriptions, outputs, READMEs. The LLM judge gets
  structured prompts with data/instruction separation, schema-validated output, no tool access,
  and can never lower a deterministic hard-fail.
- **Sandbox** (WS-E): hardened Docker (gVisor `runsc` when available), read-only root FS, no host
  mounts, dropped caps, seccomp, CPU/mem/time limits, all egress through a logging proxy.
  Honeytoken files + fake env secrets are planted; canary access or exfil = hard fail.
- **Platform secrets** come from env only; never logged, never in evidence artifacts.

## Storage layout

- **Postgres**: canonical records (see `apps/api/alembic/versions/0001_init.py`).
- **Redis**: arq job queue, audit live-status pub/sub, revocation feed, cache, rate limits.
- **S3 (MinIO dev)**:
  - `mcpaudit-snapshots/<mcp_id>/<version_id>/src.tar.zst` — immutable source snapshots
  - `mcpaudit-evidence/<audit_id>/<agent_id>/...` — raw evidence (network logs, captures)
  - `mcpaudit-docs/<mcp_id>/<version_id>/...` — generated docs

## Module → owner map

See `docs/TASKS.md` for the live board. Contracts every module obeys:

- API surface: `packages/shared/openapi.yaml`
- Agent interface + shared types: `packages/shared/python/mcpaudit_shared/`
- Scoring schema/config: `packages/shared/scoring/`
- DB schema: `apps/api/alembic/versions/`
