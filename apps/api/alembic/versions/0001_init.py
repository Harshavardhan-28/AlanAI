"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-10-27

Schema for the MCP Audit platform. Only the Orchestrator / WS-A may add migrations.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
    CREATE EXTENSION IF NOT EXISTS pgcrypto;

    CREATE TABLE users (
        id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        email         citext UNIQUE NOT NULL,
        display_name  text NOT NULL,
        password_hash text NOT NULL,
        role          text NOT NULL DEFAULT 'user' CHECK (role IN ('user','publisher','auditor','admin')),
        reputation    double precision NOT NULL DEFAULT 1.0,
        created_at    timestamptz NOT NULL DEFAULT now()
    );

    CREATE TABLE api_keys (
        id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id      uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name         text NOT NULL,
        key_hash     text UNIQUE NOT NULL,
        key_prefix   text NOT NULL,
        scopes       text[] NOT NULL DEFAULT '{}',
        created_at   timestamptz NOT NULL DEFAULT now(),
        last_used_at timestamptz,
        revoked_at   timestamptz
    );

    CREATE TABLE mcps (
        id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        publisher_id     uuid NOT NULL REFERENCES users(id),
        name             text NOT NULL,
        display_name     text,
        description      text NOT NULL DEFAULT '',
        declared_purpose text NOT NULL DEFAULT '',
        tags             text[] NOT NULL DEFAULT '{}',
        source_type      text NOT NULL CHECK (source_type IN ('github','npm','pypi','docker','remote_url')),
        source_locator   text NOT NULL,
        current_verdict  text NOT NULL DEFAULT 'PENDING'
            CHECK (current_verdict IN ('VERIFIED_SAFE','LOW_RISK','MODERATE_RISK','HIGH_RISK','DANGEROUS','PENDING')),
        current_risk_score integer CHECK (current_risk_score BETWEEN 0 AND 100),
        quarantined      boolean NOT NULL DEFAULT false,
        quarantine_reason text,
        stars_avg        double precision NOT NULL DEFAULT 0,
        review_count     integer NOT NULL DEFAULT 0,
        created_at       timestamptz NOT NULL DEFAULT now(),
        UNIQUE (source_type, source_locator)
    );
    CREATE INDEX idx_mcps_verdict ON mcps (current_verdict);
    CREATE INDEX idx_mcps_search ON mcps USING gin (to_tsvector('english', name || ' ' || description));

    CREATE TABLE mcp_versions (
        id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        mcp_id        uuid NOT NULL REFERENCES mcps(id) ON DELETE CASCADE,
        version_label text NOT NULL,
        pinned_ref    text NOT NULL,
        digest        text NOT NULL,
        manifest      jsonb NOT NULL DEFAULT '{}',
        tools         jsonb NOT NULL DEFAULT '[]',
        snapshot_key  text,
        status        text NOT NULL DEFAULT 'queued'
            CHECK (status IN ('queued','ingesting','running','scoring','completed','failed','partial')),
        created_at    timestamptz NOT NULL DEFAULT now(),
        UNIQUE (mcp_id, pinned_ref, digest)
    );
    CREATE INDEX idx_versions_mcp ON mcp_versions (mcp_id, created_at DESC);

    CREATE TABLE audits (
        id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        version_id   uuid NOT NULL REFERENCES mcp_versions(id) ON DELETE CASCADE,
        status       text NOT NULL DEFAULT 'queued'
            CHECK (status IN ('queued','ingesting','running','scoring','completed','failed','partial')),
        trigger      text NOT NULL DEFAULT 'submit'
            CHECK (trigger IN ('submit','manual','scheduled','drift','quarantine','rules_update')),
        error        text,
        created_at   timestamptz NOT NULL DEFAULT now(),
        started_at   timestamptz,
        completed_at timestamptz
    );
    CREATE INDEX idx_audits_version ON audits (version_id, created_at DESC);
    CREATE INDEX idx_audits_status ON audits (status) WHERE status IN ('queued','ingesting','running','scoring');

    CREATE TABLE audit_agent_runs (
        id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        audit_id      uuid NOT NULL REFERENCES audits(id) ON DELETE CASCADE,
        agent_id      text NOT NULL,
        agent_version text NOT NULL DEFAULT '0.1.0',
        status        text NOT NULL DEFAULT 'pending'
            CHECK (status IN ('pending','running','succeeded','failed','timed_out','skipped')),
        duration_ms   integer,
        finding_count integer NOT NULL DEFAULT 0,
        result        jsonb,
        error         text,
        started_at    timestamptz,
        finished_at   timestamptz,
        UNIQUE (audit_id, agent_id)
    );

    CREATE TABLE findings (
        id          uuid PRIMARY KEY,
        audit_id    uuid NOT NULL REFERENCES audits(id) ON DELETE CASCADE,
        agent_id    text NOT NULL,
        category    text NOT NULL
            CHECK (category IN ('secrets_exfil','malware_exec','supply_chain','prompt_injection',
                                'capability_excess','protocol_reliability','compliance','community')),
        severity    text NOT NULL CHECK (severity IN ('info','low','medium','high','critical')),
        confidence  double precision NOT NULL CHECK (confidence BETWEEN 0 AND 1),
        title       text NOT NULL,
        description text NOT NULL,
        evidence    jsonb NOT NULL DEFAULT '{}',
        remediation text,
        cwe         text,
        owasp       text,
        hard_fail_rule text,
        created_at  timestamptz NOT NULL DEFAULT now()
    );
    CREATE INDEX idx_findings_audit ON findings (audit_id);
    CREATE INDEX idx_findings_severity ON findings (audit_id, severity);

    CREATE TABLE scores (
        id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        version_id     uuid NOT NULL REFERENCES mcp_versions(id) ON DELETE CASCADE,
        audit_id       uuid NOT NULL REFERENCES audits(id) ON DELETE CASCADE,
        risk_score     integer NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
        verdict        text NOT NULL
            CHECK (verdict IN ('VERIFIED_SAFE','LOW_RISK','MODERATE_RISK','HIGH_RISK','DANGEROUS','PENDING')),
        categories     jsonb NOT NULL DEFAULT '[]',
        hard_fails     text[] NOT NULL DEFAULT '{}',
        explainability jsonb NOT NULL DEFAULT '{}',
        llm_summary    text,
        config_version text NOT NULL,
        agent_versions jsonb NOT NULL DEFAULT '{}',
        scored_at      timestamptz NOT NULL DEFAULT now(),
        UNIQUE (audit_id)
    );
    CREATE INDEX idx_scores_version ON scores (version_id, scored_at DESC);

    CREATE TABLE score_configs (
        id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        version    text UNIQUE NOT NULL,
        config     jsonb NOT NULL,
        created_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE TABLE reviews (
        id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        mcp_id     uuid NOT NULL REFERENCES mcps(id) ON DELETE CASCADE,
        version_id uuid NOT NULL REFERENCES mcp_versions(id) ON DELETE CASCADE,
        author_id  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        stars      integer NOT NULL CHECK (stars BETWEEN 1 AND 5),
        body       text NOT NULL,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now(),
        UNIQUE (mcp_id, version_id, author_id)
    );

    CREATE TABLE reports (
        id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        mcp_id        uuid NOT NULL REFERENCES mcps(id) ON DELETE CASCADE,
        reporter_id   uuid NOT NULL REFERENCES users(id),
        kind          text NOT NULL CHECK (kind IN ('malware','data_exfil','prompt_injection','other')),
        severity      text NOT NULL CHECK (severity IN ('info','low','medium','high','critical')),
        description   text NOT NULL,
        evidence_keys text[] NOT NULL DEFAULT '{}',
        status        text NOT NULL DEFAULT 'open' CHECK (status IN ('open','resolved','dismissed')),
        resolved_by   uuid REFERENCES users(id),
        resolved_at   timestamptz,
        created_at    timestamptz NOT NULL DEFAULT now()
    );
    CREATE INDEX idx_reports_open ON reports (mcp_id, created_at) WHERE status = 'open';

    CREATE TABLE flags (
        id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        mcp_id     uuid NOT NULL REFERENCES mcps(id) ON DELETE CASCADE,
        kind       text NOT NULL CHECK (kind IN ('quarantine','release','appeal')),
        actor_id   uuid REFERENCES users(id),
        reason     text NOT NULL DEFAULT '',
        created_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE TABLE schedule_entries (
        id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        mcp_id       uuid NOT NULL REFERENCES mcps(id) ON DELETE CASCADE,
        next_run_at  timestamptz NOT NULL,
        cadence      text NOT NULL CHECK (cadence IN ('daily','weekly','monthly','never')),
        reason       text NOT NULL DEFAULT 'periodic',
        last_run_at  timestamptz,
        created_at   timestamptz NOT NULL DEFAULT now(),
        UNIQUE (mcp_id, reason)
    );
    CREATE INDEX idx_schedule_due ON schedule_entries (next_run_at);

    CREATE TABLE doc_pages (
        id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        mcp_id       uuid NOT NULL REFERENCES mcps(id) ON DELETE CASCADE,
        version_id   uuid NOT NULL REFERENCES mcp_versions(id) ON DELETE CASCADE,
        slug         text NOT NULL,
        title        text NOT NULL,
        markdown     text NOT NULL,
        generated_at timestamptz NOT NULL DEFAULT now(),
        UNIQUE (version_id, slug)
    );

    CREATE TABLE events (
        id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        kind       text NOT NULL,
        actor_id   uuid REFERENCES users(id),
        target_type text,
        target_id  uuid,
        detail     jsonb NOT NULL DEFAULT '{}',
        created_at timestamptz NOT NULL DEFAULT now()
    );
    CREATE INDEX idx_events_target ON events (target_type, target_id, created_at DESC);
    CREATE INDEX idx_events_kind ON events (kind, created_at DESC);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS events, doc_pages, schedule_entries, flags, reports, reviews,
        score_configs, scores, findings, audit_agent_runs, audits, mcp_versions, mcps,
        api_keys, users CASCADE;
    """)
