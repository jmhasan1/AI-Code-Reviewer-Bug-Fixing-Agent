from app.ingestion.base import LanguageParser
from app.ingestion.parser import PythonParser


class ParserRegistry:
    """Registry mapping programming languages to their parsers."""

    def __init__(self) -> None:
        self._parsers: dict[str, LanguageParser] = {}

    def register(self, parser: LanguageParser) -> None:
        """Register a language parser."""
        self._parsers[parser.language] = parser

    def get(self, language: str) -> LanguageParser | None:
        """Return the parser registered for a language."""
        return self._parsers.get(language)

    def supported_languages(self) -> list[str]:
        """Return registered language names."""
        return sorted(self._parsers)


def create_default_registry() -> ParserRegistry:
    """Create the default parser registry."""
    registry = ParserRegistry()

    registry.register(PythonParser())

    return registry