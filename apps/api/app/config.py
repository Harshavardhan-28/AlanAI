"""API settings from environment (never hard-code secrets)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://mcpaudit:mcpaudit@localhost:5432/mcpaudit"
    redis_url: str = "redis://localhost:6379/0"
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "mcpaudit"
    s3_secret_key: str = "mcpaudit-dev-only"
    s3_bucket_snapshots: str = "mcpaudit-snapshots"
    s3_bucket_evidence: str = "mcpaudit-evidence"
    s3_bucket_docs: str = "mcpaudit-docs"
    jwt_secret: str = "dev-only-insecure-secret-change-me"
    jwt_issuer: str = "mcpaudit"
    scoring_config_path: str = "packages/shared/scoring/scoring.v1.yaml"


settings = Settings()
