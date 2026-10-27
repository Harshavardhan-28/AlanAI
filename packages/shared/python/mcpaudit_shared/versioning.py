"""Version-diff contract produced by the drift agent / versioning module."""

from pydantic import BaseModel, Field


class VersionDiff(BaseModel):
    tools_added: list[str] = Field(default_factory=list)
    tools_removed: list[str] = Field(default_factory=list)
    descriptions_changed: list[str] = Field(default_factory=list)
    permissions_added: list[str] = Field(default_factory=list)
    dependencies_added: list[str] = Field(default_factory=list)
    dependencies_removed: list[str] = Field(default_factory=list)
    network_hosts_added: list[str] = Field(default_factory=list)
    rug_pull_signals: list[str] = Field(default_factory=list)
