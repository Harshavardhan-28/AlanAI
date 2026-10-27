"""Finding and AgentResult — the output contract of every audit agent."""

import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from mcpaudit_shared.enums import AgentRunStatus, CategoryKey, Severity


class Evidence(BaseModel):
    """Pointer to proof. At least one of file/snippet/artifact_key/network_log should be set."""

    file: str | None = None
    line: int | None = None
    snippet: str | None = Field(default=None, max_length=4000)
    artifact_key: str | None = Field(
        default=None, description="S3 key in the evidence bucket for large captures"
    )
    network_log: str | None = Field(
        default=None, description="Reference into the sandbox egress log"
    )


class Finding(BaseModel):
    """One security-relevant observation. Every score point traces back to a Finding."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    category: CategoryKey
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    title: str = Field(max_length=200)
    description: str = Field(max_length=8000)
    evidence: Evidence = Field(default_factory=Evidence)
    remediation: str | None = None
    cwe: str | None = None
    owasp: str | None = None
    # Hard-fail candidates set this; scoring config decides. Agents never set verdicts directly.
    hard_fail_rule: str | None = Field(
        default=None,
        description="ID of a hard-fail rule this finding confirms (e.g. 'canary_exfiltration')",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AgentResult(BaseModel):
    """What an agent returns to the orchestrator. Status reflects agent health, not risk."""

    agent_id: str
    agent_version: str = "0.1.0"
    status: AgentRunStatus
    findings: list[Finding] = Field(default_factory=list)
    category_scores: dict[str, float] = Field(
        default_factory=dict,
        description="Optional per-category raw subscores; the scoring engine owns final math",
    )
    raw_evidence_keys: list[str] = Field(
        default_factory=list, description="S3 keys of raw captures uploaded by the agent"
    )
    duration_ms: int = 0
    errors: list[str] = Field(default_factory=list)
