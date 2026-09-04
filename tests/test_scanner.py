from pathlib import Path

from app.ingestion.scanner import detect_language, scan_repository


def test_detect_language() -> None:
    assert detect_language(Path("example.py")) == "python"
    assert detect_language(Path("example.js")) == "javascript"
    assert detect_language(Path("example.ts")) == "typescript"
    assert detect_language(Path("example.txt")) is None


def test_scan_repository(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()

    ignored = tmp_path / ".venv"
    ignored.mkdir()

    (source / "main.py").write_text("print('hello')", encoding="utf-8")
    (source / "app.js").write_text("console.log('hello')", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Example", encoding="utf-8")
    (ignored / "ignored.py").write_text("print('ignored')", encoding="utf-8")

    files = scan_repository(tmp_path)

    assert [path.name for path in files] == ["app.js", "main.py"]