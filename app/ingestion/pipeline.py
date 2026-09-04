from pathlib import Path

from app.ingestion.models import CodeArtifact
from app.ingestion.registry import create_default_registry
from app.ingestion.repository import inspect_repository
from app.ingestion.scanner import detect_language, scan_repository


def parse_repository(
    repository_path: Path,
) -> list[CodeArtifact]:
    """Scan and parse all supported source files in a repository."""
    repository_path = repository_path.resolve()

    repository_info = inspect_repository(repository_path)
    files = scan_repository(repository_path)

    registry = create_default_registry()

    artifacts: list[CodeArtifact] = []

    for file_path in files:
        language = _detect_file_language(file_path)

        if language is None:
            continue

        parser = registry.get(language)

        if parser is None:
            continue

        artifacts.extend(
            parser.parse_file(
                file_path=file_path,
                repository_id=repository_info.repository_id,
                repository_root=repository_path,
            )
        )

    return artifacts


def _detect_file_language(file_path: Path) -> str | None:
    """Detect a source file's programming language."""
    return detect_language(file_path)