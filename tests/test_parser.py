from pathlib import Path

from app.ingestion.models import ArtifactType
from app.ingestion.parser import parse_python_file


def test_parse_python_file(tmp_path: Path) -> None:
    source = '''"""Example module."""

from database import get_connection
import logging


class UserService:
    """Manage users."""

    def __init__(self, repository):
        self.repository = repository

    def get_user(self, user_id):
        return self.repository.find(user_id)


def validate_user_id(user_id):
    """Validate a user ID."""
    return user_id > 0
'''

    source_file = tmp_path / "users.py"
    source_file.write_text(source, encoding="utf-8")

    artifacts = parse_python_file(
        file_path=source_file,
        repository_id="test-repository",
        repository_root=tmp_path,
    )

    assert len(artifacts) == 5

    module = artifacts[0]
    class_artifact = artifacts[1]
    init_method = artifacts[2]
    get_user_method = artifacts[3]
    validate_function = artifacts[4]

    assert module.artifact_type == ArtifactType.MODULE
    assert module.symbol_name == "users"
    assert module.language == "python"
    assert module.file_path == "users.py"

    assert class_artifact.artifact_type == ArtifactType.CLASS
    assert class_artifact.symbol_name == "UserService"
    assert class_artifact.qualified_name == "UserService"

    assert init_method.artifact_type == ArtifactType.METHOD
    assert init_method.qualified_name == "UserService.__init__"
    assert init_method.parent_symbol == "UserService"

    assert get_user_method.artifact_type == ArtifactType.METHOD
    assert get_user_method.qualified_name == "UserService.get_user"
    assert get_user_method.parent_symbol == "UserService"

    assert validate_function.artifact_type == ArtifactType.FUNCTION
    assert validate_function.symbol_name == "validate_user_id"
    assert validate_function.qualified_name == "validate_user_id"

    assert module.imports == [
        "database",
        "logging",
    ]

def test_parse_async_function(tmp_path: Path) -> None:
    source = """\
async def fetch_user(user_id):
    return await get_user(user_id)
"""

    source_file = tmp_path / "service.py"
    source_file.write_text(source, encoding="utf-8")

    artifacts = parse_python_file(
        file_path=source_file,
        repository_id="test-repository",
        repository_root=tmp_path,
    )

    assert len(artifacts) == 2

    function = artifacts[1]

    assert function.artifact_type == ArtifactType.FUNCTION
    assert function.symbol_name == "fetch_user"
    assert function.qualified_name == "fetch_user"
    assert function.start_line == 1
    assert function.end_line == 2