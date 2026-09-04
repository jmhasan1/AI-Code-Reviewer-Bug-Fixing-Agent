from pathlib import Path

SUPPORTED_EXTENSIONS: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".tox",
}


def detect_language(path: Path) -> str | None:
    """Return the supported language for a source file."""
    return SUPPORTED_EXTENSIONS.get(path.suffix.lower())


def scan_repository(repository_path: Path) -> list[Path]:
    """Discover supported source files in a repository."""
    repository_path = repository_path.resolve()

    if not repository_path.exists():
        raise FileNotFoundError(
            f"Repository path does not exist: {repository_path}"
        )

    if not repository_path.is_dir():
        raise NotADirectoryError(
            f"Repository path is not a directory: {repository_path}"
        )

    source_files: list[Path] = []

    for path in repository_path.rglob("*"):
        if not path.is_file():
            continue

        relative_parts = path.relative_to(repository_path).parts

        if any(part in IGNORED_DIRECTORIES for part in relative_parts):
            continue

        if detect_language(path) is None:
            continue

        source_files.append(path)

    return sorted(source_files)