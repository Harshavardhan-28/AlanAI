# Contributing (humans and agents)

## Branching

- `main` — always green. Only the Orchestrator merges.
- Workstreams: `ws/<id>-<name>` (e.g. `ws/a-core-api`), each in its own git worktree.

## Commits

Conventional Commits: `feat(api): ...`, `fix(worker): ...`, `test(agents): ...`, `docs: ...`,
`chore(ci): ...`. Commit small and often; never leave work uncommitted at the end of a session.

## File ownership

Your brief lists OWNED PATHS. **Never edit outside them.** If you need a change to a contract
(`packages/shared/openapi.yaml`, `packages/shared/python/mcpaudit_shared/`,
`packages/shared/scoring/`, `apps/api/alembic/versions/`, root tooling), request it from the
Orchestrator — they change it on `main`, you rebase.

## Before every commit

```
ruff check apps packages/shared/python   # python lint
ruff format apps packages/shared/python  # python format
pytest <your module tests> -q            # your tests, green
pnpm --filter <your pkg> lint && pnpm --filter <your pkg> typecheck   # TS modules
```

## Safety rules

- Never execute untrusted/fetched MCP code outside the sandbox. Ingestion is fetch + static
  extraction only.
- Use only inert fixtures from `fixtures/`. No real secrets. No real network calls in tests —
  mock them (LLM client defaults to deterministic mock mode).
- Never commit secrets, keys, or `.env` files.

## Definition of Done (per workstream)

1. Acceptance criteria in your brief met.
2. Unit + integration tests passing (you ran them, you saw them pass).
3. Lint + type-check clean.
4. Module docs written (`docs/<ws>.md`).
5. No TODO stubs on the main path; structured logging + basic metrics in place.
6. Everything committed; report lists commit hashes and test counts.
