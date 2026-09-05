# AI Code Reviewer & Bug-Fixing Agent

An agentic AI system for understanding software repositories, identifying bugs and code-quality issues, proposing targeted fixes, and validating those changes through automated testing.

The project is being developed incrementally, beginning with deterministic **repository intelligence** before introducing semantic retrieval and agentic LLM workflows.

## Project Status

🚧 **Active development**

### Current Milestone

**Milestone 2 — Repository Intelligence: Complete**

Implemented:

- Repository inspection
- Recursive source-file scanning
- Language detection
- Python AST parsing
- Structured code artifacts
- Language parser abstraction
- Parser registry
- Unified repository parsing pipeline
- Symbol indexing
- Code relationship extraction

Current test status:

```text
11 tests passing
Ruff checks passing
```

The current implementation is intentionally deterministic and does not yet require an LLM or vector database.

---

## Current Capabilities

The repository-ingestion and code-intelligence layer can currently:

1. Inspect a repository
2. Discover supported source files
3. Ignore irrelevant directories
4. Detect source languages
5. Parse Python source using the built-in AST
6. Extract modules, classes, functions, and methods
7. Preserve source locations and metadata
8. Build an exact symbol index
9. Extract structural code relationships

### Current Python Relationship Types

```text
IMPORTS
DEFINES
CALLS
INHERITS_FROM
```

JavaScript and TypeScript are currently detected by the scanner but do not yet have language-specific parsers.

---

## Planned Capabilities

As development progresses, the system is intended to support:

- Repository ingestion and codebase understanding
- Code-aware retrieval (RAG)
- Exact and structural code retrieval
- Semantic vector retrieval
- Hybrid retrieval
- AI-powered code review
- Bug and root-cause analysis
- Fix generation
- Automated validation and testing
- Iterative agentic debugging
- Structured review reports
- Support for multiple programming languages over time

---

# Architecture

## Current Architecture

The current implementation focuses on deterministic repository intelligence:

```text
Repository
    |
    v
Repository Inspection
    |
    v
Repository Scanner
    |
    v
Language Detection
    |
    v
Parser Registry
    |
    v
Python AST Parser
    |
    v
CodeArtifact[]
    |
    +-- SymbolIndex
    |
    +-- Relationship Analysis
              |
              v
       CodeRelationship[]
```

The current architecture deliberately establishes reliable repository understanding before introducing LLM-based reasoning.

## Target Architecture

The completed system will extend repository intelligence with retrieval, agentic review, fix generation, and validation:

```text
Repository + Issue
        |
        v
Repository Ingestion
        |
        v
Repository Analysis
        |
        v
Hybrid Retrieval
   +---------+---------+
   |         |         |
   v         v         v
 Exact   Structural  Semantic
 Search    Search     Search
   |         |         |
   +---------+---------+
             |
             v
        Review Agent
             |
             v
          Fix Agent
             |
             v
         Validation
          /       \
       PASS       FAIL
        |           |
        v           v
 Final Report   Re-analysis
                    |
                    v
                Fix Agent
```

The target workflow is designed around evidence-based review and validation before a fix is considered successful.

---

# Technology

## Currently Implemented

- Python 3.13+
- FastAPI
- Pydantic
- Pydantic Settings
- Uvicorn
- pytest
- Ruff
- uv
- Python `ast`

## Planned

The following technologies will be introduced only when their corresponding milestones are implemented:

- LLM APIs
- Embeddings
- ChromaDB
- LangGraph
- Streamlit

This keeps the current repository lightweight and ensures dependencies are added only when functionality actually requires them.

---

# Project Structure

```text
ai-code-reviewer-bug-fixing-agent/
│
├── app/
│   ├── agents/                 # Future agent orchestration
│   ├── api/                    # API layer
│   ├── config/                 # Application configuration
│   ├── ingestion/              # Repository intelligence
│   ├── rag/                    # Future retrieval layer
│   ├── tools/                  # Future agent tools
│   └── validation/             # Future validation layer
│
├── tests/
│   ├── test_health.py
│   ├── test_repository.py
│   ├── test_scanner.py
│   ├── test_parser.py
│   ├── test_pipeline.py
│   ├── test_index.py
│   └── test_relationships.py
│
├── examples/
│   └── sample_project/
│
├── docs/
│   ├── architecture.md
│   └── evaluation.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

Some directories contain intentionally empty architectural placeholders for future milestones. Their presence does not mean that the corresponding functionality is currently implemented.

---

# Development

This project uses [`uv`](https://docs.astral.sh/uv/) for Python environment and dependency management.

## Create the Environment

```bash
uv venv
```

## Install Dependencies

```bash
uv sync
```

## Run Tests

```bash
uv run pytest
```

## Run Linting

```bash
uv run ruff check .
```

## Run the API

```bash
uv run uvicorn app.main:app --reload
```

Health endpoint:

```text
GET /health
```

---

# Configuration

Copy the example environment file:

### macOS / Linux

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

The current configuration model includes settings for future LLM, embedding, vector-store, and agent functionality.

Actual provider integrations will be introduced in later milestones.

> **Important:** Never commit real API keys or other secrets to the repository.

---

# Development Roadmap

## Milestone 1 — Foundation

- Repository setup
- Python environment
- Configuration
- FastAPI foundation
- Testing
- Ruff
- CI
- Initial architecture

**Status: Complete**

---

## Milestone 2 — Repository Intelligence

- Repository scanner
- Language detection
- Python AST parser
- Code artifact model
- Parser abstraction
- Parser registry
- Unified parsing pipeline
- Symbol index
- Code relationships

**Status: Complete**

---

## Milestone 3 — Repository Knowledge & Retrieval

### 3.1 Repository Analysis Model

- Combine repository metadata
- `CodeArtifact[]`
- `CodeRelationship[]`
- `SymbolIndex`
- Unified `RepositoryAnalysis`

### 3.2 Retrieval Interfaces

- Common retriever abstraction
- Exact symbol retrieval
- Relationship retrieval
- Retrieval result model

### 3.3 Semantic Retrieval

- Embedding integration
- ChromaDB
- Artifact indexing
- Similarity search

### 3.4 Hybrid Retrieval

- Exact retrieval
- Structural retrieval
- Semantic retrieval
- Ranking
- Deduplication
- Context-size controls

### 3.5 Retrieval Evaluation

- Representative repository queries
- Retrieval precision/recall
- Baseline evaluation

**Status: Planned**

---

## Milestone 4 — Review Agent

- LangGraph
- Structured review state
- Code analysis
- Root-cause analysis
- Severity
- Confidence
- Evidence and citations

**Status: Planned**

---

## Milestone 5 — Bug-Fixing Agent

- Patch generation
- Safe file modification
- Diff generation
- Fix explanations

**Status: Planned**

---

## Milestone 6 — Validation Loop

- Test generation
- Test execution
- Result parsing
- Fix → test → retry
- Iteration limits

**Status: Planned**

---

## Milestone 7 — UI, Deployment & Submission

- Repository upload
- Issue input
- Review progress
- Findings
- Proposed diff
- Test results
- Final report
- Deployment
- Demo repository
- Demo video
- Submission materials

**Status: Planned**

---

# Design Principles

## Evidence-Based Review

Future findings should reference concrete repository artifacts, files, symbols, and line ranges.

## Deterministic Repository Intelligence

Repository structure should be extracted deterministically wherever possible before involving an LLM.

## Hybrid Retrieval

Code retrieval should combine:

- Exact symbol matching
- Structural relationships
- Semantic similarity

No single retrieval strategy is expected to be sufficient for repository-level code understanding.

## Validation Before Success

A generated fix should not be considered successful until validation provides supporting evidence.

## Controlled Execution

Repository code is untrusted input. Future test execution will use controlled and restricted execution environments.

## Human Oversight

The system assists developers and should not silently modify production code.

## Extensibility

Python is the initial fully supported language. The parser abstraction is designed to accommodate additional languages without requiring a redesign of the overall workflow.

---

# CI

The repository uses GitHub Actions to run:

- Dependency installation
- Ruff
- pytest

Every push to `main` and pull request targeting `main` is subject to the configured quality checks.

The CI workflow provides a basic automated quality gate as the project evolves.

---

# Evaluation

The project maintains an evaluation strategy alongside the architecture so that future retrieval, review, fixing, and validation capabilities can be measured against the deterministic repository-intelligence baseline.

See [`docs/evaluation.md`](docs/evaluation.md) for:

- Current baseline evaluation
- Repository scanning and parsing evaluation
- Symbol and relationship evaluation
- Planned retrieval evaluation
- Planned agent evaluation
- Validation metrics
- Initial evaluation dataset
- MVP success criteria

---

# Documentation

Additional project documentation:

- [`docs/architecture.md`](docs/architecture.md) — Current and target system architecture
- [`docs/evaluation.md`](docs/evaluation.md) — Evaluation strategy and success criteria

---

# License

MIT
