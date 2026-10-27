# tests/e2e

End-to-end suite (Playwright + API-driven), owned by **WS-L**.

Requires the dev stack (`make dev`). Covers:
- submit → live audit → score → findings visible
- benign fixture → LOW/VERIFIED_SAFE; malicious fixture → DANGEROUS with evidence
- rug-pull v2 → drift detected, score drops
- community report → instant quarantine → gateway blocks
- CLI: `mcpaudit check` on known/unknown/quarantined sources
