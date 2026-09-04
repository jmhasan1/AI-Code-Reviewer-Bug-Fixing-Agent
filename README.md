# AI Code Reviewer & Bug-Fixing Agent

An agentic AI system for reviewing software repositories, identifying bugs and code-quality issues, proposing fixes, and validating changes through automated testing.

## Project Status

🚧 **Active development**

This project is being developed as a practical Generative AI engineering project and Build Sprint MVP.

## Planned Capabilities

- Repository ingestion and codebase understanding
- Code-aware retrieval (RAG)
- AI-powered code review
- Bug and root-cause analysis
- Fix generation
- Automated validation and testing
- Iterative agentic debugging
- Structured review reports
- Support for multiple programming languages over time

## Architecture

The planned workflow is:

```text
Repository
    ↓
Repository Scanner
    ↓
Code Index / Retrieval
    ↓
Review Agent
    ↓
Fix Agent
    ↓
Validation
    ↓
Review / Retry
    ↓
Final Report
```

## Technology

- Python
- FastAPI
- LangGraph
- LLM APIs
- ChromaDB
- Streamlit
- pytest
- Ruff

## Development

This project uses `uv` for Python environment and dependency management.

### Create the environment

```bash
uv venv
```

### Install dependencies

```bash
uv sync
```

### Run tests

```bash
uv run pytest
```

### Run linting

```bash
uv run ruff check .
```

### Run the API

```bash
uv run uvicorn app.main:app --reload
```

The health endpoint is available at:

```text
GET /health
```

## System Architecture

The AI Code Reviewer & Bug-Fixing Agent is designed as a modular agentic system that can ingest a software repository, understand its structure, retrieve relevant code, analyze issues, propose changes, and validate those changes.

### High-Level Flow

```text
User
 │
 ▼
Repository Input
 │
 ▼
Repository Ingestion
 │
 ├── File Discovery
 ├── Language Detection
 └── Code Parsing
 │
 ▼
Code Index
 │
 ├── Semantic Retrieval
 ├── Metadata Retrieval
 └── Code Context
 │
 ▼
Review Agent
 │
 ▼
Fix Agent
 │
 ▼
Validation
 │
 ├── Static Analysis
 └── Automated Tests
 │
 ▼
Validation Decision
 │
 ├── Passed ──► Final Report
 │
 └── Failed ──► Limited Agent Retry
```

## Design Principles

### 1. Modular architecture

Repository ingestion, retrieval, agents, tools, and validation are separated so that each component can evolve independently.

### 2. Structured agent state

Agent nodes communicate through structured state rather than relying exclusively on free-form text.

### 3. Evidence-based review

Review findings should reference concrete repository artifacts such as files, functions, classes, and line ranges whenever possible.

### 4. Validation before claiming success

A generated fix should not automatically be considered correct. The system should attempt to validate proposed changes.

### 5. Controlled execution

Repository code is considered untrusted input. Test execution must be isolated and restricted rather than granting arbitrary host-level access.

### 6. Extensibility

Python is the initial target language because it provides a strong MVP path through its AST and pytest ecosystem. The ingestion layer is designed so additional languages can be introduced later.

## CI Foundation

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install 3.13

      - name: Install dependencies
        run: uv sync --dev

      - name: Run Ruff
        run: uv run ruff check .

      - name: Run tests
        run: uv run pytest
```

This gives the repository a basic automated quality gate from the beginning.

## License

MIT