from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, Field

from app.ingestion.scanner import detect_language, scan_repository


class RepositoryInfo(BaseModel):
    """Metadata describing an analyzed repository."""

    repository_id: str
    name: str
    root_path: str
    file_count: int = Field(ge=0)
    languages: dict[str, int] = Field(default_factory=dict)


def inspect_repository(repository_path: Path) -> RepositoryInfo:
    """Scan a repository and return basic metadata."""
    repository_path = repository_path.resolve()

    files = scan_repository(repository_path)

    languages: dict[str, int] = {}

    for file_path in files:
        language = detect_language(file_path)

        if language is not None:
            languages[language] = languages.get(language, 0) + 1

    return RepositoryInfo(
        repository_id=str(uuid4()),
        name=repository_path.name,
        root_path=str(repository_path),
        file_count=len(files),
        languages=languages,
    )