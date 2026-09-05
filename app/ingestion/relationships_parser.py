import ast
from pathlib import Path

from app.ingestion.models import ArtifactType, CodeArtifact
from app.ingestion.relationships import CodeRelationship, RelationshipType


def extract_python_relationships(
    file_path: Path,
    repository_id: str,
    repository_root: Path,
    artifacts: list[CodeArtifact],
) -> list[CodeRelationship]:
    """Extract relationships from a Python source file."""

    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    relative_path = file_path.relative_to(repository_root).as_posix()
    relationships: list[CodeRelationship] = []

    relationships.extend(
        _extract_import_relationships(
            tree=tree,
            file_path=relative_path,
            repository_id=repository_id,
        )
    )

    relationships.extend(
        _extract_definition_relationships(
            artifacts=artifacts,
            file_path=relative_path,
            repository_id=repository_id,
        )
    )

    relationships.extend(
        _extract_call_relationships(
            tree=tree,
            artifacts=artifacts,
            file_path=relative_path,
            repository_id=repository_id,
        )
    )

    relationships.extend(
        _extract_inheritance_relationships(
            tree=tree,
            artifacts=artifacts,
            file_path=relative_path,
            repository_id=repository_id,
        )
    )

    return relationships


def _extract_import_relationships(
    tree: ast.AST,
    file_path: str,
    repository_id: str,
) -> list[CodeRelationship]:
    relationships: list[CodeRelationship] = []

    module_name = Path(file_path).with_suffix("").as_posix().replace("/", ".")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                relationships.append(
                    CodeRelationship(
                        repository_id=repository_id,
                        source=module_name,
                        target=alias.name,
                        relationship_type=RelationshipType.IMPORTS,
                        file_path=file_path,
                    )
                )

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                relationships.append(
                    CodeRelationship(
                        repository_id=repository_id,
                        source=module_name,
                        target=node.module,
                        relationship_type=RelationshipType.IMPORTS,
                        file_path=file_path,
                    )
                )

    return relationships


def _extract_definition_relationships(
    artifacts: list[CodeArtifact],
    file_path: str,
    repository_id: str,
) -> list[CodeRelationship]:
    relationships: list[CodeRelationship] = []

    module_artifact = next(
        (
            artifact
            for artifact in artifacts
            if artifact.artifact_type == ArtifactType.MODULE
        ),
        None,
    )

    if module_artifact is None:
        return relationships

    for artifact in artifacts:
        if artifact.artifact_type == ArtifactType.MODULE:
            continue

        parent = artifact.parent_symbol or module_artifact.qualified_name

        if parent is None:
            continue

        relationships.append(
            CodeRelationship(
                repository_id=repository_id,
                source=parent,
                target=artifact.qualified_name or artifact.symbol_name,
                relationship_type=RelationshipType.DEFINES,
                file_path=file_path,
            )
        )

    return relationships


def _extract_call_relationships(
    tree: ast.AST,
    artifacts: list[CodeArtifact],
    file_path: str,
    repository_id: str,
) -> list[CodeRelationship]:
    relationships: list[CodeRelationship] = []

    artifact_by_line = sorted(
        (
            artifact
            for artifact in artifacts
            if artifact.artifact_type
            in {
                ArtifactType.FUNCTION,
                ArtifactType.METHOD,
            }
        ),
        key=lambda artifact: artifact.start_line,
    )

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        target = _get_call_target(node)

        if target is None:
            continue

        caller = _find_containing_artifact(node, artifact_by_line)

        if caller is None:
            continue

        relationships.append(
            CodeRelationship(
                repository_id=repository_id,
                source=caller.qualified_name or caller.symbol_name,
                target=target,
                relationship_type=RelationshipType.CALLS,
                file_path=file_path,
            )
        )

    return relationships


def _extract_inheritance_relationships(
    tree: ast.AST,
    artifacts: list[CodeArtifact],
    file_path: str,
    repository_id: str,
) -> list[CodeRelationship]:
    relationships: list[CodeRelationship] = []

    classes = {
        artifact.symbol_name: artifact
        for artifact in artifacts
        if artifact.artifact_type == ArtifactType.CLASS
    }

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        source_artifact = classes.get(node.name)

        if source_artifact is None:
            continue

        for base in node.bases:
            target = _get_expression_name(base)

            if target is None:
                continue

            relationships.append(
                CodeRelationship(
                    repository_id=repository_id,
                    source=source_artifact.qualified_name or node.name,
                    target=target,
                    relationship_type=RelationshipType.INHERITS_FROM,
                    file_path=file_path,
                )
            )

    return relationships


def _get_call_target(node: ast.Call) -> str | None:
    return _get_expression_name(node.func)


def _get_expression_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parts: list[str] = []

        current: ast.AST | None = node

        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value

        if isinstance(current, ast.Name):
            parts.append(current.id)
            return ".".join(reversed(parts))

    return None


def _find_containing_artifact(
    node: ast.AST,
    artifacts: list[CodeArtifact],
) -> CodeArtifact | None:
    lineno = getattr(node, "lineno", None)

    if lineno is None:
        return None

    containing = [
        artifact
        for artifact in artifacts
        if artifact.start_line <= lineno <= artifact.end_line
    ]

    if not containing:
        return None

    return min(containing, key=lambda artifact: artifact.line_count)