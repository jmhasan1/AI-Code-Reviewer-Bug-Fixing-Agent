from pathlib import Path

from app.ingestion.models import ArtifactType, CodeArtifact
from app.ingestion.relationships import RelationshipType
from app.ingestion.relationships_parser import extract_python_relationships


def test_python_relationship_extraction(tmp_path: Path) -> None:
    source = """
from helpers import format_name
from models import BaseUser


class User(BaseUser):
    def display_name(self):
        return format_name(self.name)


def create_user(name):
    return User(name)
"""

    file_path = tmp_path / "users.py"
    file_path.write_text(source, encoding="utf-8")

    artifacts = [
        CodeArtifact(
            repository_id="repo-1",
            file_path="users.py",
            language="python",
            artifact_type=ArtifactType.MODULE,
            symbol_name="users",
            qualified_name="users",
            start_line=1,
            end_line=12,
            content=source,
        ),
        CodeArtifact(
            repository_id="repo-1",
            file_path="users.py",
            language="python",
            artifact_type=ArtifactType.CLASS,
            symbol_name="User",
            qualified_name="User",
            start_line=6,
            end_line=9,
            content="class User(BaseUser):\n...",
        ),
        CodeArtifact(
            repository_id="repo-1",
            file_path="users.py",
            language="python",
            artifact_type=ArtifactType.METHOD,
            symbol_name="display_name",
            qualified_name="User.display_name",
            parent_symbol="User",
            start_line=7,
            end_line=8,
            content="def display_name(self):\n...",
        ),
        CodeArtifact(
            repository_id="repo-1",
            file_path="users.py",
            language="python",
            artifact_type=ArtifactType.FUNCTION,
            symbol_name="create_user",
            qualified_name="create_user",
            start_line=11,
            end_line=12,
            content="def create_user(name):\n...",
        ),
    ]

    relationships = extract_python_relationships(
        file_path=file_path,
        repository_id="repo-1",
        repository_root=tmp_path,
        artifacts=artifacts,
    )

    relationship_pairs = {
        (
            relationship.source,
            relationship.target,
            relationship.relationship_type,
        )
        for relationship in relationships
    }

    assert (
        "users",
        "helpers",
        RelationshipType.IMPORTS,
    ) in relationship_pairs

    assert (
        "users",
        "models",
        RelationshipType.IMPORTS,
    ) in relationship_pairs

    assert (
        "users",
        "User",
        RelationshipType.DEFINES,
    ) in relationship_pairs

    assert (
        "User",
        "User.display_name",
        RelationshipType.DEFINES,
    ) in relationship_pairs

    assert (
        "User.display_name",
        "format_name",
        RelationshipType.CALLS,
    ) in relationship_pairs

    assert (
        "User",
        "BaseUser",
        RelationshipType.INHERITS_FROM,
    ) in relationship_pairs

    assert (
        "create_user",
        "User",
        RelationshipType.CALLS,
    ) in relationship_pairs