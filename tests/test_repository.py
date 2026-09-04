from pathlib import Path

from app.ingestion.repository import inspect_repository


def test_inspect_repository(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()

    (source / "main.py").write_text("print('hello')", encoding="utf-8")
    (source / "utils.py").write_text("def add(a, b): return a + b", encoding="utf-8")
    (source / "app.js").write_text("console.log('hello')", encoding="utf-8")

    repository = inspect_repository(tmp_path)

    assert repository.name == tmp_path.name
    assert repository.file_count == 3
    assert repository.languages == {
        "javascript": 1,
        "python": 2,
    }
    assert repository.repository_id