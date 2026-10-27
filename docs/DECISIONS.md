# Decisions

Format: `D-<n>` — decision, context, status. Append-only; supersede, don't edit history.

## D-1 — One language for API + workers: Python 3.12
The brief allows FastAPI/Python or TS; we pick **Python (FastAPI)** for API and workers because the
security tooling ecosystem (semgrep, bandit, gitleaks, OSV clients, MCP SDK) is strongest there.
CLI/gateway stay TypeScript (published to npm as `mcpaudit`). Status: accepted.

## D-2 — Score convention: `risk_score` is canonical
0–100, **higher = riskier**. The API stores/returns `risk_score`; UI may display
`trust = 100 - risk` as a friendly label but never stores it. Verdict tiers:
`VERIFIED_SAFE`, `LOW_RISK`, `MODERATE_RISK`, `HIGH_RISK`, `DANGEROUS`, `PENDING`.
Status: accepted.

## D-3 — Queue: arq on Redis
arq is async-native, fits FastAPI workers, needs only Redis (already in stack). Job payloads carry
IDs only; state lives in Postgres. Status: accepted.

## D-4 — Monorepo layout without a build orchestrator
Plain directories + pnpm workspaces (TS) + pip-installable packages (Python). Root `Makefile` is the
single entry: `make dev`, `make test`, `make lint`, `make typecheck`. No turborepo/nx — not needed
at this scale. Status: accepted.

## D-5 — Migrations: Alembic
Single source of truth in `apps/api/alembic/versions/`. Only the Orchestrator (or WS-A via a
contract-change request) may add migrations. Status: accepted.

## D-6 — Scoring weights live in versioned config, not code
`packages/shared/scoring/scoring.v<N>.yaml`. Every `Score` row stores `config_version`,
`agent_versions`, and the full finding-ID list so any score is reproducible and explainable.
Status: accepted.

## D-7 — LLM access: thin provider abstraction, offline mock by default
`mcpaudit_shared.llm` exposes `LLMClient` with `mock` (deterministic, default in tests/CI) and
`anthropic` providers. Every LLM output is schema-validated; failures degrade gracefully and never
affect hard-fail rules. Status: accepted.

## D-8 — Sandbox: hardened Docker first, gVisor when available
Runtime `runsc` is used if the host provides it; otherwise plain Docker with: read-only rootfs,
`--cap-drop ALL`, seccomp profile, `--network` restricted to an egress-proxy net, mem/cpu/pids
limits, no host mounts. Dev/CI runs the fixture corpus against this. Status: accepted.

## D-9 — Auth model
Web: HttpOnly session cookie (JWT). CLI/gateway: `Authorization: Bearer mcpa_...` API keys,
scoped (`read`, `submit`, `gateway`). RBAC roles: `user`, `publisher`, `auditor`, `admin`.
Status: accepted.

## D-10 — OpenAPI is the contract of record
`packages/shared/openapi.yaml` is hand-maintained and CI-validated. API implementation must match
it; TS clients may be generated from it. Changes go through the Orchestrator. Status: accepted.

## D-11 — Fixture safety
All malicious fixtures are inert: exfil posts to a sink inside the sandbox network, downloads fetch
a local marker file, secret theft reads only planted canary files. No real secrets, no real
third-party calls in tests. Status: accepted.

## D-12 — CI definition lives in infra/ci/
The GitHub App token used by the automation sandbox lacks the `workflows` permission, so
`.github/workflows/*.yml` cannot be pushed. The canonical CI definition is `infra/ci/ci.yml`;
a human with workflow permission copies it to `.github/workflows/ci.yml` to activate. Locally,
`make test` / `make lint` / `make typecheck` run the same checks. Status: accepted (workaround).
