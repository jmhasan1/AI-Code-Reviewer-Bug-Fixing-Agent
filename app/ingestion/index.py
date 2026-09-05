from collections import defaultdict

from app.ingestion.models import CodeArtifact


class SymbolIndex:
    """Index code artifacts for exact and qualified-name lookup."""

    def __init__(self, artifacts: list[CodeArtifact]) -> None:
        self._by_name: dict[str, list[CodeArtifact]] = defaultdict(list)
        self._by_qualified_name: dict[str, list[CodeArtifact]] = defaultdict(list)
        self._by_file: dict[str, list[CodeArtifact]] = defaultdict(list)

        for artifact in artifacts:
            self._by_name[artifact.symbol_name].append(artifact)

            if artifact.qualified_name:
                self._by_qualified_name[artifact.qualified_name].append(artifact)

            self._by_file[artifact.file_path].append(artifact)

    def find_by_name(self, symbol_name: str) -> list[CodeArtifact]:
        """Find artifacts by symbol name."""
        return list(self._by_name.get(symbol_name, []))

    def find_by_qualified_name(self, qualified_name: str) -> list[CodeArtifact]:
        """Find artifacts by qualified name."""
        return list(self._by_qualified_name.get(qualified_name, []))

    def find_by_file(self, file_path: str) -> list[CodeArtifact]:
        """Find artifacts defined in a file."""
        return list(self._by_file.get(file_path, []))