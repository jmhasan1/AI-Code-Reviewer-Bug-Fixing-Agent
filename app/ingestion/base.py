from abc import ABC, abstractmethod
from pathlib import Path

from app.ingestion.models import CodeArtifact


class LanguageParser(ABC):
    """Base interface for language-specific source-code parsers."""

    language: str

    @abstractmethod
    def parse_file(
        self,
        file_path: Path,
        repository_id: str,
        repository_root: Path,
    ) -> list[CodeArtifact]:
        """Parse a source file into code artifacts."""
        raise NotImplementedError