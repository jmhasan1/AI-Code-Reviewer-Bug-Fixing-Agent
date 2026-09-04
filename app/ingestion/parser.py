import ast
from pathlib import Path

from app.ingestion.base import LanguageParser
from app.ingestion.models import ArtifactType, CodeArtifact


def _get_source_segment(
    source: str,
    node: ast.AST,
) -> str:
    """Return the source code corresponding to an AST node."""
    segment = ast.get_source_segment(source, node)

    if segment is not None:
        return segment

    lines = source.splitlines()
    start = getattr(node, "lineno", 1)
    end = getattr(node, "end_lineno", start)

    return "\n".join(lines[start - 1 : end])


def _get_docstring(node: ast.AST) -> str | None:
    """Return an AST node's docstring when available."""
    if isinstance(
        node,
        (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
    ):
        return ast.get_docstring(node)

    return None


def _get_imports(tree: ast.Module) -> list[str]:
    """Extract imported module names from a Python module."""
    imports: list[str] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)

        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                imports.append(node.module)

    return imports


def parse_python_file(
    file_path: Path,
    repository_id: str,
    repository_root: Path,
) -> list[CodeArtifact]:
    """Parse a Python file into structured code artifacts."""
    source = file_path.read_text(encoding="utf-8")

    tree = ast.parse(
        source,
        filename=str(file_path),
    )

    relative_path = file_path.resolve().relative_to(
        repository_root.resolve()
    )

    file_path_string = relative_path.as_posix()
    imports = _get_imports(tree)

    artifacts: list[CodeArtifact] = []

    artifacts.append(
        CodeArtifact(
            repository_id=repository_id,
            file_path=file_path_string,
            language="python",
            artifact_type=ArtifactType.MODULE,
            symbol_name=file_path.stem,
            qualified_name=file_path_string.removesuffix(".py").replace("/", "."),
            start_line=1,
            end_line=max(len(source.splitlines()), 1),
            content=source,
            docstring=_get_docstring(tree),
            imports=imports,
        )
    )

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            artifacts.append(
                _build_class_artifact(
                    node=node,
                    source=source,
                    file_path=file_path_string,
                    repository_id=repository_id,
                    imports=imports,
                )
            )

            artifacts.extend(
                _build_method_artifacts(
                    class_node=node,
                    source=source,
                    file_path=file_path_string,
                    repository_id=repository_id,
                    imports=imports,
                )
            )

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            artifacts.append(
                _build_function_artifact(
                    node=node,
                    source=source,
                    file_path=file_path_string,
                    repository_id=repository_id,
                    imports=imports,
                )
            )

    return artifacts


def _build_class_artifact(
    node: ast.ClassDef,
    source: str,
    file_path: str,
    repository_id: str,
    imports: list[str],
) -> CodeArtifact:
    """Build a CodeArtifact for a class."""
    return CodeArtifact(
        repository_id=repository_id,
        file_path=file_path,
        language="python",
        artifact_type=ArtifactType.CLASS,
        symbol_name=node.name,
        qualified_name=node.name,
        start_line=node.lineno,
        end_line=node.end_lineno or node.lineno,
        content=_get_source_segment(source, node),
        docstring=_get_docstring(node),
        imports=imports,
    )


def _build_function_artifact(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    source: str,
    file_path: str,
    repository_id: str,
    imports: list[str],
) -> CodeArtifact:
    """Build a CodeArtifact for a function."""
    return CodeArtifact(
        repository_id=repository_id,
        file_path=file_path,
        language="python",
        artifact_type=ArtifactType.FUNCTION,
        symbol_name=node.name,
        qualified_name=node.name,
        start_line=node.lineno,
        end_line=node.end_lineno or node.lineno,
        content=_get_source_segment(source, node),
        docstring=_get_docstring(node),
        imports=imports,
    )


def _build_method_artifacts(
    class_node: ast.ClassDef,
    source: str,
    file_path: str,
    repository_id: str,
    imports: list[str],
) -> list[CodeArtifact]:
    """Build CodeArtifacts for methods defined directly inside a class."""
    artifacts: list[CodeArtifact] = []

    for node in class_node.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        artifacts.append(
            CodeArtifact(
                repository_id=repository_id,
                file_path=file_path,
                language="python",
                artifact_type=ArtifactType.METHOD,
                symbol_name=node.name,
                qualified_name=f"{class_node.name}.{node.name}",
                start_line=node.lineno,
                end_line=node.end_lineno or node.lineno,
                content=_get_source_segment(source, node),
                parent_symbol=class_node.name,
                docstring=_get_docstring(node),
                imports=imports,
            )
        )

    return artifacts

class PythonParser(LanguageParser):
    """Parser for Python source files."""

    language = "python"

    def parse_file(
        self,
        file_path: Path,
        repository_id: str,
        repository_root: Path,
    ) -> list[CodeArtifact]:
        """Parse a Python source file."""
        return parse_python_file(
            file_path=file_path,
            repository_id=repository_id,
            repository_root=repository_root,
        )