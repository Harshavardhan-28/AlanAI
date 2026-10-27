"""Canonical enums. These mirror packages/shared/openapi.yaml exactly — keep in sync."""

from enum import StrEnum


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Verdict(StrEnum):
    VERIFIED_SAFE = "VERIFIED_SAFE"
    LOW_RISK = "LOW_RISK"
    MODERATE_RISK = "MODERATE_RISK"
    HIGH_RISK = "HIGH_RISK"
    DANGEROUS = "DANGEROUS"
    PENDING = "PENDING"


class SourceType(StrEnum):
    GITHUB = "github"
    NPM = "npm"
    PYPI = "pypi"
    DOCKER = "docker"
    REMOTE_URL = "remote_url"


class CategoryKey(StrEnum):
    SECRETS_EXFIL = "secrets_exfil"
    MALWARE_EXEC = "malware_exec"
    SUPPLY_CHAIN = "supply_chain"
    PROMPT_INJECTION = "prompt_injection"
    CAPABILITY_EXCESS = "capability_excess"
    PROTOCOL_RELIABILITY = "protocol_reliability"
    COMPLIANCE = "compliance"
    COMMUNITY = "community"


class AuditStatus(StrEnum):
    QUEUED = "queued"
    INGESTING = "ingesting"
    RUNNING = "running"
    SCORING = "scoring"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class AgentRunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    SKIPPED = "skipped"
