from mcpaudit_shared import AgentResult, AuditAgent, AuditContext, CategoryKey, Finding, Severity


def test_contracts_importable():
    assert AuditAgent is not None
    assert AuditContext is not None


def test_finding_defaults():
    f = Finding(
        category=CategoryKey.SECRETS_EXFIL,
        severity=Severity.HIGH,
        confidence=0.9,
        title="reads ~/.ssh",
        description="reads ssh keys and posts them",
    )
    assert f.id is not None
    assert f.evidence.file is None


def test_agent_result_shape():
    r = AgentResult(agent_id="x", status="succeeded")
    assert r.findings == []
    assert r.agent_version == "0.1.0"
