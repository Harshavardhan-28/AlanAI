"""MCP Audit worker package.

Layout (ownership enforced via CONTRIBUTING.md):
  worker/ingest/        WS-B  safe fetch + pin + manifest extraction
  worker/orchestrator/  WS-C  queue consumer, DAG fan-out, agent registry
  worker/agents/        WS-D*/WS-E/WS-F  the audit agents (one subpackage each)
  worker/scoring/       WS-F  deterministic scoring engine
  worker/scheduler/     WS-G  cron re-audit + drift polling
  worker/docs/          WS-K  auto-documentation generator
"""
