# System Architecture

## Overview

The **AI Code Reviewer & Bug-Fixing Agent** is being developed as a modular agentic system for repository analysis, code review, bug fixing, and automated validation.

Development is incremental. The current implementation focuses on building a deterministic **repository-intelligence foundation** before introducing LLM-powered review, semantic retrieval, and full agent orchestration.

The architecture therefore distinguishes between:

- **Implemented repository-intelligence capabilities**
- **Planned retrieval, agent, fixing, and validation capabilities**

This keeps the architecture aligned with the current implementation while documenting the intended evolution of the system.

---

## Current Implementation

The current implementation establishes the repository ingestion and code-intelligence foundation.

### Current Pipeline

```text
Repository
    |
    v
Repository Inspection
    |
    v
Repository Scanner
    |
    +-- File Discovery
    +-- Ignore Irrelevant Directories
    +-- Language Detection
    |
    v
Language Parser Registry
    |
    +-- PythonParser
    |
    v
CodeArtifact[]
    |
    +-------------------+
    |                   |
    v                   v
SymbolIndex       Relationship Analysis
                        |
                        +-- IMPORTS
                        +-- DEFINES
                        +-- CALLS
                        +-- INHERITS_FROM
```

The current pipeline is deterministic and does not require an LLM.

---

## Repository Inspection

The repository inspection layer provides basic metadata about the repository before parsing begins.

It currently:

- Resolves the repository path.
- Scans supported source files.
- Counts discovered source files.
- Detects the languages represented in the repository.
- Assigns a repository identifier for the analysis run.

Repository metadata is represented by `RepositoryInfo`.

---

## Repository Scanner

The repository scanner recursively discovers supported source files while ignoring generated files, virtual environments, caches, build directories, and other irrelevant repository content.

### Currently Recognized Languages

| Language | Detection | Language-specific Parser |
|---|---|---|
| Python | Supported | Implemented |
| JavaScript | Supported | Not yet implemented |
| TypeScript | Supported | Not yet implemented |

The scanner currently recognizes:

- `.py`
- `.js`
- `.jsx`
- `.ts`
- `.tsx`

Ignored directories include common repository and generated-content directories such as:

- `.git`
- `.venv`
- `venv`
- `env`
- `__pycache__`
- `.pytest_cache`
- `.ruff_cache`
- `.mypy_cache`
- `node_modules`
- `dist`
- `build`
- `.next`
- `.tox`

JavaScript and TypeScript are currently detected by the scanner but are not yet parsed into language-specific code artifacts.

---

## Language Parser Registry

Language-specific parsers implement a common `LanguageParser` interface.

The parser registry maps a detected programming language to its corresponding parser implementation.

This abstraction allows additional language parsers to be introduced without changing the repository scanning and processing pipeline.

### Current Registered Parser

```text
ParserRegistry
    |
    +-- PythonParser
```

The current default registry registers only `PythonParser`.

---

## Python AST Parser

Python source files are parsed using Python's built-in `ast` module.

The parser extracts structural information without requiring an LLM.

This provides deterministic source-code understanding while preserving useful source-location information for future review findings and evidence.

The parser currently extracts:

- Modules
- Classes
- Functions
- Methods
- Imports
- Docstrings
- Parent symbols
- Qualified names
- Source content
- Start and end line numbers

---

## Code Artifact Model

Parsed source code is represented using structured `CodeArtifact` objects.

Each artifact contains information such as:

| Field | Purpose |
|---|---|
| `repository_id` | Identifies the analyzed repository |
| `file_path` | Repository-relative source path |
| `language` | Programming language |
| `artifact_type` | Module, class, function, or method |
| `symbol_name` | Symbol name |
| `qualified_name` | Qualified symbol name where available |
| `start_line` | Beginning source line |
| `end_line` | Ending source line |
| `content` | Source code represented by the artifact |
| `parent_symbol` | Parent class/symbol when applicable |
| `docstring` | Extracted documentation when available |
| `imports` | Imports associated with the source module |

The current artifact types are:

```text
MODULE
CLASS
FUNCTION
METHOD
```

This structured representation forms the foundation for later code retrieval, review findings, and evidence-based reporting.

---

## Symbol Index

`SymbolIndex` provides deterministic lookup of parsed artifacts.

Artifacts can currently be retrieved by:

- Symbol name
- Qualified name
- File path

Conceptually:

```text
CodeArtifact[]
      |
      v
  SymbolIndex
      |
      +-- find_by_name()
      +-- find_by_qualified_name()
      +-- find_by_file()
```

The symbol index is intended to support exact structural retrieval alongside future semantic retrieval.

---

## Code Relationships

The current implementation extracts structural relationships from Python source code.

Supported relationship types are:

- `IMPORTS`
- `DEFINES`
- `CALLS`
- `INHERITS_FROM`

These relationships provide the foundation for repository-level dependency and context analysis.

Relationships are represented using `CodeRelationship` objects containing:

- Repository identifier
- Source
- Target
- Relationship type
- File path

### Relationship Flow

```text
Parsed Python Source
        |
        v
Relationship Analysis
        |
        +-- IMPORTS
        +-- DEFINES
        +-- CALLS
        +-- INHERITS_FROM
        |
        v
CodeRelationship[]
```

---

## Current Repository Architecture

The currently implemented repository-intelligence layer can be summarized as:

```text
                    Repository
                        |
                        v
              +---------------------+
              | Repository Inspection|
              +----------+----------+
                         |
                         v
              +---------------------+
              | Repository Scanner  |
              +----------+----------+
                         |
                  Language Detection
                         |
                         v
              +---------------------+
              |   Parser Registry   |
              +----------+----------+
                         |
                         v
                  +------------+
                  | PythonParser|
                  +------+-----+
                         |
                         v
                  +--------------+
                  | CodeArtifact[]|
                  +------+-------+
                         |
             +-----------+-----------+
             |                       |
             v                       v
      +-------------+       +------------------+
      | Symbol Index|       | Relationship     |
      |             |       | Analysis         |
      +-------------+       +--------+---------+
                                     |
                                     v
                              CodeRelationship[]
```

---

# Target Architecture

The completed system will extend the deterministic repository-intelligence layer with:

- Repository analysis
- Hybrid code retrieval
- AI-powered review
- Fix generation
- Controlled validation
- Bounded agentic retry
- Structured final reporting

## Target Workflow

```text
User
  |
  v
Repository + Issue
  |
  v
Repository Ingestion
  |
  +-------------+-------------+
  |             |             |
  v             v             v
Scanner      Parsers     Relationships
  |             |             |
  +-------------+-------------+
                |
                v
       Repository Analysis
                |
                v
         Hybrid Retrieval
        +------+------+------+
        |             |      |
        v             v      v
      Exact      Structural Semantic
      Search       Search    Search
        |             |      |
        +-------------+------+
                |
                v
          Review Agent
                |
                v
           Fix Agent
                |
                v
            Validation
                |
          +-----+-----+
          |           |
        PASS         FAIL
          |           |
          v           v
    Final Report   Re-analysis
                       |
                       v
                    Fix Agent
```

The target workflow is intentionally layered: deterministic repository understanding provides the evidence and context on which retrieval and agentic reasoning can operate.

---

## Planned Components

### Repository Analysis

A future repository-analysis layer will combine:

- Repository metadata
- Code artifacts
- Symbol indexes
- Code relationships

into a coherent repository representation that can be consumed by retrieval and review components.

### Hybrid Retrieval

The retrieval subsystem is planned to use multiple complementary strategies:

1. **Exact symbol retrieval**
2. **Relationship-aware retrieval**
3. **Semantic vector retrieval**

These strategies will eventually be combined into a hybrid retrieval system.

The goal is to retrieve both:

- Precisely matching structural code
- Semantically relevant code that may not share exact names or terms

This architecture avoids depending on a single retrieval strategy for repository-level code understanding.

### Review Agent

The review agent will analyze a reported issue together with relevant repository context.

Future review findings are expected to identify:

- Bugs
- Root causes
- Code-quality issues
- Severity
- Confidence
- Supporting evidence
- Source locations

Findings should be grounded in concrete repository artifacts whenever possible.

### Fix Agent

The fix agent will generate targeted code changes based on review findings and retrieved repository context.

Generated changes should be represented as **explicit diffs** rather than silently modifying the repository.

This keeps proposed changes inspectable and supports human oversight.

### Validation

The validation subsystem will eventually:

1. Apply proposed changes in a controlled environment.
2. Run relevant tests and validation checks.
3. Capture execution results.
4. Determine whether the proposed fix is supported by validation evidence.

A generated fix should not be considered successful solely because an LLM produced it.

### Agent Orchestration

LangGraph is planned to coordinate the review, fixing, and validation workflow using:

- Structured shared state
- Explicit workflow nodes
- Validation decisions
- Bounded retry loops

The orchestration layer is a future capability; the current repository contains architectural placeholders rather than a completed agent workflow.

---

## Planned Module Structure

The repository contains architectural placeholders for future components:

```text
app/
├── agents/
│   ├── graph.py
│   ├── state.py
│   ├── reviewer.py
│   └── fixer.py
│
├── ingestion/
│   ├── repository.py
│   ├── scanner.py
│   ├── parser.py
│   ├── base.py
│   ├── registry.py
│   ├── pipeline.py
│   ├── models.py
│   ├── index.py
│   ├── relationships.py
│   ├── relationships_parser.py
│   └── relationship_pipeline.py
│
├── rag/
│   ├── embeddings.py
│   ├── indexer.py
│   └── retriever.py
│
├── tools/
│   ├── code_search.py
│   ├── file_reader.py
│   └── test_runner.py
│
├── validation/
│   ├── evaluator.py
│   └── sandbox.py
│
├── api/
└── ui/
```

### Implementation Status of Planned Modules

The presence of files under `agents/`, `rag/`, `tools/`, and `validation/` does **not** mean those capabilities are currently implemented.

At the current stage, these modules serve primarily as architectural placeholders for later milestones.

The repository's implemented functionality is concentrated in the ingestion and repository-intelligence layer, together with the basic FastAPI application and health endpoint.

---

## Design Principles

### 1. Deterministic repository understanding first

Structural repository analysis should not depend on an LLM.

The current scanner, parser, artifact model, symbol index, and relationship analysis provide a deterministic foundation for later AI capabilities.

### 2. Evidence-based analysis

Future review findings should reference concrete repository artifacts, symbols, files, and line ranges.

The existing `CodeArtifact` model preserves source-location and structural information specifically to support this principle.

### 3. Hybrid retrieval

No single retrieval strategy is sufficient for code.

Exact, structural, and semantic retrieval should complement one another so that the review agent can obtain both precise and contextually relevant repository information.

### 4. Structured outputs

Repository artifacts, relationships, retrieval results, and future agent outputs should use structured or typed schemas rather than relying entirely on free-form text.

### 5. Validation before success

A generated fix should not be considered successful until validation provides supporting evidence.

The intended workflow therefore treats validation as a decision point rather than an optional final step.

### 6. Controlled execution

Repository code is untrusted input.

Future test execution and validation must therefore be isolated and restricted rather than granting arbitrary host-level access.

### 7. Extensibility

Python is the first fully supported language.

The parser abstraction is intentionally designed so additional language-specific parsers can be introduced without redesigning the overall repository-analysis workflow.

### 8. Human oversight

The system assists developers and should not silently modify production code.

Review findings and proposed fixes should remain inspectable, and generated changes should be represented explicitly before validation or application.

---

## Language Strategy

Python is the first fully supported language because:

- Python provides a built-in AST.
- Structural parsing can be deterministic.
- `pytest` provides a strong testing ecosystem.
- Python provides a practical MVP target.

JavaScript and TypeScript are currently recognized by the repository scanner but do not yet have language-specific parsers.

Future language support will be introduced through the common `LanguageParser` interface so that new parsers can be added without redesigning the agent workflow.

---

## Current Technology Boundary

The current project implementation establishes the deterministic foundation using Python, Pydantic, FastAPI, and Python's built-in AST tooling.

The repository also contains placeholders for the future RAG, agent, tools, and validation layers.

The architectural target includes LangGraph-based orchestration and hybrid retrieval, but these should be treated as **planned capabilities rather than current implementation** until the corresponding modules are implemented.

---

## Architecture Evolution

The project is intended to evolve through incremental milestones:

```text
Milestone 1–2
Deterministic Repository Intelligence
        |
        +-- Repository Inspection
        +-- File Scanning
        +-- Language Detection
        +-- Python AST Parsing
        +-- Code Artifacts
        +-- Symbol Index
        +-- Relationship Analysis
        |
        v
Milestone 3+
Repository Analysis + Retrieval
        |
        +-- Unified Repository Model
        +-- Exact Retrieval
        +-- Relationship-aware Retrieval
        +-- Semantic Retrieval
        +-- Hybrid Retrieval
        |
        v
Agentic Review
        |
        +-- Review Agent
        +-- Fix Agent
        +-- Structured State
        |
        v
Validation
        |
        +-- Controlled Execution
        +-- Tests
        +-- Validation Evidence
        +-- Bounded Retry
        |
        v
Final Review Report
```

This incremental architecture allows the system to establish reliable, testable repository understanding before adding probabilistic LLM behavior and agentic execution.
