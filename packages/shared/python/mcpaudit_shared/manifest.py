"""Manifest + tool list produced by ingestion, consumed by all agents."""

from typing import Any

from pydantic import BaseModel, Field

from mcpaudit_shared.enums import SourceType


class ToolSpec(BaseModel):
    name: str
    description: str | None = None
    input_schema: dict[str, Any] = Field(default_factory=dict)


class McpManifest(BaseModel):
    """Everything ingestion could determine *without executing* the source."""

    source_type: SourceType
    locator: str
    pinned_ref: str = Field(description="commit SHA | exact package version | image digest ref")
    digest: str = Field(description="sha256 of the snapshot tarball / package / image manifest")
    name: str | None = None
    declared_purpose: str | None = None
    languages: list[str] = Field(default_factory=list)
    dependencies: dict[str, str] = Field(
        default_factory=dict, description="name -> pinned-or-declared version spec"
    )
    install_hooks: list[str] = Field(
        default_factory=list,
        description="postinstall scripts, setup.py cmdclass, Dockerfile RUN, etc.",
    )
    tools: list[ToolSpec] = Field(default_factory=list)
    entrypoint: str | None = Field(default=None, description="How the sandbox should start the MCP")
    readme_key: str | None = Field(default=None, description="S3 key of extracted README")
    metadata: dict[str, Any] = Field(default_factory=dict)
