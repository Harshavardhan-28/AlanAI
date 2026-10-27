"""Scoring engine I/O types. The engine is deterministic; config lives in scoring.v<N>.yaml."""

from pydantic import BaseModel, Field

from mcpaudit_shared.enums import CategoryKey, Verdict
from mcpaudit_shared.findings import Finding


class ScoreInput(BaseModel):
    """All findings from one audit, plus provenance needed for reproducibility."""

    audit_id: str
    version_id: str
    findings: list[Finding]
    agent_versions: dict[str, str] = Field(default_factory=dict)
    config_version: str


class CategoryScore(BaseModel):
    category: CategoryKey
    score: int = Field(ge=0, le=100)
    top_finding_ids: list[str] = Field(default_factory=list)


class ScoreOutput(BaseModel):
    """Deterministic result. Every point traces to a finding id in `explainability`."""

    risk_score: int = Field(ge=0, le=100)
    verdict: Verdict
    categories: list[CategoryScore]
    hard_fails_triggered: list[str] = Field(default_factory=list)
    config_version: str
    agent_versions: dict[str, str] = Field(default_factory=dict)
    explainability: dict[str, list[dict[str, object]]] = Field(
        default_factory=dict,
        description="category -> [{finding_id, points}] — the receipt for every score point",
    )
