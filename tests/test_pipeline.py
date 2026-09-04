from pathlib import Path

from app.ingestion import ArtifactType, parse_repository
from app.ingestion.parser import PythonParser
from app.ingestion.registry import create_default_registry


def test_default_parser_registry() -> None:
    registry = create_default_registry()

    assert registry.supported_languages() == ["python"]

    parser = registry.get("python")

    assert isinstance(parser, PythonParser)
    assert registry.get("javascript") is None


def test_parse_repository(tmp_path: Path) -> None:
    app_directory = tmp_path / "app"
    app_directory.mkdir()

    (app_directory / "users.py").write_text(
        '''"""User management."""

class User:
    """Represent a user."""

    def __init__(self, name):
        self.name = name

    def display_name(self):
        return self.name


def validate_name(name):
    return bool(name)
''',
        encoding="utf-8",
    )

    (app_directory / "utils.py").write_text(
        """def add(a, b):
    return a + b
""",
        encoding="utf-8",
    )

    (tmp_path / "README.md").write_text(
        "# Example",
        encoding="utf-8",
    )

    artifacts = parse_repository(tmp_path)

    assert len(artifacts) == 7

    assert [artifact.artifact_type for artifact in artifacts] == [
        ArtifactType.MODULE,
        ArtifactType.CLASS,
        ArtifactType.METHOD,
        ArtifactType.METHOD,
        ArtifactType.FUNCTION,
        ArtifactType.MODULE,
        ArtifactType.FUNCTION,
    ]

    assert artifacts[0].file_path == "app/users.py"
    assert artifacts[0].symbol_name == "users"

    assert artifacts[1].symbol_name == "User"
    assert artifacts[2].qualified_name == "User.__init__"
    assert artifacts[3].qualified_name == "User.display_name"

    assert artifacts[4].symbol_name == "validate_name"

    assert artifacts[5].file_path == "app/utils.py"
    assert artifacts[6].symbol_name == "add"

    repository_ids = {
        artifact.repository_id
        for artifact in artifacts
    }

    assert len(repository_ids) == 1


def test_parse_repository_ignores_unsupported_languages(
    tmp_path: Path,
) -> None:
    (tmp_path / "app.py").write_text(
        "def hello():\n    return 'hello'\n",
        encoding="utf-8",
    )

    (tmp_path / "app.js").write_text(
        "function hello() { return 'hello'; }\n",
        encoding="utf-8",
    )

    artifacts = parse_repository(tmp_path)

    assert all(artifact.language == "python" for artifact in artifacts)