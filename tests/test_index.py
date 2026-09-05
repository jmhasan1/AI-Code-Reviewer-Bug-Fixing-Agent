from app.ingestion.index import SymbolIndex
from app.ingestion.models import ArtifactType, CodeArtifact


def test_symbol_index() -> None:
    artifacts = [
        CodeArtifact(
            repository_id="repo-1",
            file_path="app/users.py",
            language="python",
            artifact_type=ArtifactType.FUNCTION,
            symbol_name="create_user",
            qualified_name="create_user",
            start_line=1,
            end_line=3,
            content="def create_user():\n    pass",
        ),
        CodeArtifact(
            repository_id="repo-1",
            file_path="app/users.py",
            language="python",
            artifact_type=ArtifactType.CLASS,
            symbol_name="User",
            qualified_name="User",
            start_line=5,
            end_line=10,
            content="class User:\n    pass",
        ),
    ]

    index = SymbolIndex(artifacts)

    assert index.find_by_name("User")[0].symbol_name == "User"
    assert (
        index.find_by_qualified_name("create_user")[0].symbol_name
        == "create_user"
    )
    assert len(index.find_by_file("app/users.py")) == 2
    assert index.find_by_name("missing") == []