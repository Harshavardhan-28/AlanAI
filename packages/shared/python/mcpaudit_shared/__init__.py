"""Shared contracts for the MCP Audit platform.

Every audit agent, the orchestrator, the scoring engine, and (via OpenAPI parity) the API
uses these types. Changing anything here is a contract change — orchestrator approval only.
"""

from mcpaudit_shared.agent import AuditAgent, AuditBudgets, AuditContext
from mcpaudit_shared.enums import (
    AgentRunStatus,
    AuditStatus,
    CategoryKey,
    Severity,
    SourceType,
    Verdict,
)
from mcpaudit_shared.findings import AgentResult, Evidence, Finding
from mcpaudit_shared.manifest import McpManifest, ToolSpec
from mcpaudit_shared.scoring import CategoryScore, ScoreInput, ScoreOutput
from mcpaudit_shared.versioning import VersionDiff

__all__ = [
    "AgentResult",
    "AgentRunStatus",
    "AuditAgent",
    "AuditBudgets",
    "AuditContext",
    "AuditStatus",
    "CategoryKey",
    "CategoryScore",
    "Evidence",
    "Finding",
    "McpManifest",
    "ScoreInput",
    "ScoreOutput",
    "Severity",
    "SourceType",
    "ToolSpec",
    "Verdict",
    "VersionDiff",
]
