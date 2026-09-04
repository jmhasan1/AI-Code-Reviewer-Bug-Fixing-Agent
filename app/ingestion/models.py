from enum import StrEnum

from pydantic import BaseModel, Field


class ArtifactType(StrEnum):
    """Types of code artifacts extracted from a repository."""

    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"


class CodeArtifact(BaseModel):
    """A structured unit of source code extracted from a repository."""

    repository_id: str
    file_path: str
    language: str
    artifact_type: ArtifactType
    symbol_name: str
    qualified_name: str | None = None

    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)

    content: str

    parent_symbol: str | None = None

    docstring: str | None = None

    imports: list[str] = Field(default_factory=list)

    @property
    def line_count(self) -> int:
        """Return the number of source lines covered by the artifact."""
        return self.end_line - self.start_line + 1