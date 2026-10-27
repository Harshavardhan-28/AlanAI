# Workstream board

Status: ⬜ pending · 🔨 in progress · ✅ done · ⛔ blocked

Contract paths (orchestrator-owned; change requests only):
`packages/shared/openapi.yaml` · `packages/shared/python/mcpaudit_shared/` ·
`packages/shared/scoring/` · `apps/api/alembic/versions/` · root tooling

| WS | Name | Owned paths | Depends on | Status |
|----|------|-------------|-----------|--------|
| A | Core API + DB | `apps/api/` (routers, services; not alembic/versions) | Phase 0 | 🔨 spawned |
| B | Ingestion | `apps/worker/worker/ingest/` | Phase 0 | 🔨 spawned |
| C | Audit orchestrator | `apps/worker/worker/orchestrator/` | Phase 0 | 🔨 spawned |
| D1 | Static + Secrets/Exfil agents | `apps/worker/worker/agents/static/`, `.../agents/secrets/` | agent iface | 🔨 spawned |
| D2 | Supply-chain + Provenance + Compliance | `.../agents/supply_chain/`, `.../agents/provenance/`, `.../agents/compliance/` | agent iface | 🔨 spawned |
| D3 | Injection + Capability + Drift agents | `.../agents/injection/`, `.../agents/capability/`, `.../agents/drift/` | agent iface | 🔨 spawned |
| D4 | Protocol/Fuzz + Remote + Community agents | `.../agents/protocol/`, `.../agents/remote/`, `.../agents/community/` | agent iface | 🔨 spawned |
| E | Sandbox runner + Dynamic agent | `infra/sandbox/`, `.../agents/dynamic/` | agent iface | 🔨 spawned |
| F | Scoring engine + Judge agent | `apps/worker/worker/scoring/`, `.../agents/judge/` | schemas | 🔨 spawned |
| G | Versioning + scheduler | `apps/worker/worker/scheduler/` | schemas | 🔨 spawned |
| H | Community layer | `apps/api/app/community/` | OpenAPI | 🔨 spawned |
| I | Web app | `apps/web/` | OpenAPI (mock) | 🔨 spawned |
| J | CLI + Gateway | `packages/cli/`, `packages/gateway/` | OpenAPI | 🔨 spawned |
| K | Hosted access + Docs generator | `apps/api/app/hosting/`, `apps/worker/worker/docs/` | OpenAPI | 🔨 spawned |
| L | Fixtures + QA + CI | `fixtures/`, `tests/e2e/`, `infra/ci/` | Phase 0 | 🔨 spawned |

## Acceptance criteria (summary per WS; full briefs in spawn messages)

- **A**: full OpenAPI impl, auth+RBAC+API keys, CRUD+search+pagination, rate limits, contract tests.
- **B**: fetch GitHub/npm/PyPI/Docker/remote pinned to SHA/digest, snapshot→S3, manifest+tools, zero code execution, unit tests with mocked network.
- **C**: arq consumer, parallel DAG fan-out with timeouts/budgets/retries, agent registry, persistence of runs+findings, SSE status events, failure-mode tests (crash/timeout/partial).
- **D1-D4**: each agent implements `AuditAgent`, detects its threat-model rows against fixtures, unit tests green with offline mocks.
- **E**: hardened sandbox runner (no mounts, RO rootfs, dropped caps, limits, egress logging proxy), honeytokens, MCP protocol client, dynamic agent flags canary access/exfil.
- **F**: scoring engine implementing `scoring.v1.yaml` semantics, hard fails, explainability, golden-file regression tests; judge agent (LLM via `mcpaudit_shared.llm`, mock-tested).
- **G**: version diffs, cadence policies by tier/popularity, drift re-audit triggers, revocation events.
- **H**: reviews/reports/evidence upload, anti-abuse (rate limit, one-review-per-version, reputation weighting), auto-quarantine fast path, appeal flow.
- **I**: marketplace browse/search/filter, MCP detail (score, findings, timeline, tools, docs, reviews), submit flow, live audit status (SSE), publisher+admin dashboards — against mocked API.
- **J**: `mcpaudit check/install/status`; gateway proxy with verdict enforcement, version pinning, runtime injection scanning of tool descriptions/results, revocation sync.
- **K**: auto-docs from tool schemas/README, hosted endpoint through gateway for audited MCPs, usage metering.
- **L**: inert malicious-fixture corpus (one per threat-model row + benign + obfuscated variants) with expected verdicts; e2e suite; CI green.

## Blockers

- CI activation: automation token lacks `workflows` permission (D-12). CI definition lives in
  `infra/ci/ci.yml`; needs a human to copy it to `.github/workflows/` on GitHub.
