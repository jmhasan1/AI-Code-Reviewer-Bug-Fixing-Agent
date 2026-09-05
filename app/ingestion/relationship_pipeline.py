from pathlib import Path

from app.ingestion.models import CodeArtifact
from app.ingestion.relationships import CodeRelationship
from app.ingestion.relationships_parser import extract_python_relationships
from app.ingestion.scanner import detect_language, scan_repository


def analyze_relationships(
    repository_path: Path,
    repository_id: str,
    artifacts: list[CodeArtifact],
) -> list[CodeRelationship]:
    """Extract relationships across a parsed repository."""

    repository_path = repository_path.resolve()
    relationships: list[CodeRelationship] = []

    artifacts_by_file: dict[str, list[CodeArtifact]] = {}

    for artifact in artifacts:
        artifacts_by_file.setdefault(artifact.file_path, []).append(artifact)

    for file_path in scan_repository(repository_path):
        language = detect_language(file_path)

        if language != "python":
            continue

        relative_path = file_path.relative_to(repository_path).as_posix()

        relationships.extend(
            extract_python_relationships(
                file_path=file_path,
                repository_id=repository_id,
                repository_root=repository_path,
                artifacts=artifacts_by_file.get(relative_path, []),
            )
        )

    return relationships