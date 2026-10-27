"""The AuditAgent interface + AuditContext. EVERY audit agent implements AuditAgent."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from mcpaudit_shared.findings import AgentResult
from mcpaudit_shared.manifest import McpManifest


class AuditBudgets(BaseModel):
    """Per-audit resource budget enforced by the orchestrator."""

    wall_clock_seconds: int = 300
    max_output_tokens: int = 20_000
    network_allowed: bool = False  # agents must not call the network unless granted
    llm_calls_allowed: int = 0  # >0 only for LLM-backed agents


class SandboxHandle(BaseModel):
    """Handle to a prepared sandbox, provided only to the dynamic agent."""

    container_id: str
    egress_log_path: str | None = None
    honeytoken_paths: list[str] = Field(default_factory=list)
    mcp_endpoint: str | None = Field(default=None, description="In-sandbox MCP protocol endpoint")


class AuditContext(BaseModel):
    """Everything an agent is allowed to know. Agents must be pure functions of this."""

    model_config = {"arbitrary_types_allowed": True}

    mcp_id: str
    version_id: str
    audit_id: str
    source_snapshot_path: Path = Field(
        description="Read-only extracted source snapshot. Agents must not execute it."
    )
    manifest: McpManifest
    sandbox: SandboxHandle | None = None
    prior_results: list[AgentResult] = Field(
        default_factory=list,
        description="Results of earlier agents in the DAG (e.g. judge sees all)",
    )
    budgets: AuditBudgets = Field(default_factory=AuditBudgets)
    extras: dict[str, Any] = Field(
        default_factory=dict,
        description="Agent-specific extras, e.g. previous-version manifest for the drift agent",
    )


class AuditAgent(ABC):
    """One pluggable audit. Deterministic first, LLM second; output schema-validated."""

    agent_id: str  # unique, stable, kebab-case, e.g. "static-sast"
    agent_version: str = "0.1.0"

    @abstractmethod
    async def run(self, context: AuditContext) -> AgentResult:
        """Execute the audit. Must respect context.budgets. Must never raise — return
        status=FAILED with errors populated instead."""
        ...

    def supports(self, context: AuditContext) -> bool:
        """Override to opt out (e.g. remote agent only supports remote_url sources)."""
        return True
