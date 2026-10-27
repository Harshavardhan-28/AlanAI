# MCP Audit

Security audit + risk-scoring marketplace for MCP (Model Context Protocol) servers.

- **Publish** an MCP (GitHub, npm, PyPI, Docker, or remote URL) — every version is pinned and
  automatically audited by a fan-out of security agents.
- **Discover** MCPs in the marketplace with transparent, evidence-linked risk scores (0–100,
  higher = riskier) and verdict tiers from `VERIFIED_SAFE` to `DANGEROUS`.
- **Consume** safely via the `mcpaudit` CLI and gateway: verdict checks, version pinning,
  runtime prompt-injection scanning, instant quarantine propagation.

## Quick start

```bash
cp .env.example .env
make dev        # db, redis, minio, api, worker, web
make migrate    # DB schema
make seed       # demo data + fixture corpus audits
make test       # all tests
```

- Web: http://localhost:3000 · API: http://localhost:8000 · MinIO console: http://localhost:9001

## Docs

- `docs/ARCHITECTURE.md` — components, data flow, trust boundaries
- `docs/DECISIONS.md` — recorded technical decisions
- `docs/TASKS.md` — workstream board
- `packages/shared/openapi.yaml` — API contract of record
- `packages/shared/scoring/` — scoring config + schema
- `fixtures/README.md` — inert malicious-fixture corpus

## Contributing

See `CONTRIBUTING.md` (branch naming, conventional commits, file ownership, safety rules).
