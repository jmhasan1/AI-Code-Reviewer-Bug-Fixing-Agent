# Evaluation Strategy

## Purpose

The evaluation strategy measures the reliability of the **AI Code Reviewer & Bug-Fixing Agent** as the system evolves.

Evaluation is introduced before the LLM/agent layer so that later improvements can be measured against deterministic baselines.

The project follows an incremental evaluation model: first establish deterministic repository-intelligence correctness, then evaluate retrieval quality, review quality, fix correctness, and finally end-to-end validation.

---

## Current Baseline

Milestone 2 establishes the repository-intelligence baseline.

### Current Automated Test Suite

```text
11 tests passing
```

The current tests cover:

- API health endpoint
- Repository inspection
- File scanning
- Language detection
- Python AST parsing
- Unified repository parsing
- Parser registry
- Unsupported-language handling
- Symbol indexing
- Python relationship extraction

### Static Analysis

```text
Ruff: passing
```

The current implementation has no external LLM dependency and does not yet evaluate model-generated review quality.

Therefore, the current evaluation focuses on deterministic repository understanding and structural code intelligence.

---

# Milestone 2 Evaluation

## Repository Scanning

The scanner should:

- Discover supported source files.
- Ignore configured irrelevant directories.
- Correctly identify supported languages.
- Ignore unsupported file types.

### Evaluation Evidence

Scanning should be evaluated using representative repositories containing:

- Supported Python files
- JavaScript and TypeScript files
- Unsupported file types
- Virtual environments
- Build output
- Cache directories
- Generated or irrelevant repository content

The expected result is that only relevant source files are included in the repository analysis.

---

## Source Parsing

The Python parser should correctly identify:

- Modules
- Classes
- Functions
- Methods
- Async functions
- Imports
- Source line ranges
- Qualified names

Parsing should remain deterministic and should preserve source-location information that can later be used as evidence in review findings.

### Evaluation Evidence

For a known Python source file, the evaluation should compare the produced `CodeArtifact` objects against expected:

- Artifact types
- Symbol names
- Qualified names
- Parent symbols
- Line ranges
- Imports
- Source content

---

## Symbol Indexing

The symbol index should support deterministic lookup by:

- Symbol name
- Qualified name
- File path

### Evaluation Evidence

Given a known repository artifact, an index query should return the expected artifact without depending on semantic similarity or an LLM.

Example:

```text
Query:
find authenticate_user

Expected:
authenticate_user
```

---

## Relationship Extraction

The relationship layer should correctly identify:

- Module imports
- Symbol definitions
- Function and method calls
- Class inheritance

Supported relationship types:

```text
IMPORTS
DEFINES
CALLS
INHERITS_FROM
```

### Evaluation Evidence

For a known Python repository, expected relationships should be compared against extracted `CodeRelationship` objects.

Example:

```text
Query:
what functions call authenticate_user?

Expected:
callers connected through CALLS relationships
```

---

# Planned Retrieval Evaluation

Milestone 3 will introduce repository retrieval.

Evaluation will compare retrieval strategies using representative code queries and known expected results.

The planned retrieval layer consists of:

1. Exact symbol retrieval
2. Relationship-aware retrieval
3. Semantic vector retrieval
4. Hybrid retrieval

---

## Exact Retrieval

Measure whether known symbols and files can be retrieved correctly.

Example:

```text
Query:
find authenticate_user

Expected:
authenticate_user
```

Primary evaluation concerns:

- Exact match correctness
- Symbol lookup accuracy
- File-path lookup accuracy
- Qualified-name lookup accuracy

---

## Structural Retrieval

Measure whether related code can be retrieved through repository relationships.

Example:

```text
Query:
what functions call authenticate_user?
```

Expected results should include callers connected through `CALLS` relationships.

Primary evaluation concerns:

- Relationship traversal correctness
- Relevant caller/callee retrieval
- Dependency-context coverage
- Avoidance of unrelated artifacts

---

## Semantic Retrieval

Measure whether natural-language queries retrieve relevant code artifacts.

Example:

```text
Query:
find code responsible for validating authentication tokens
```

Expected results should contain the relevant authentication and token-validation artifacts.

Primary evaluation concerns:

- Relevance of retrieved artifacts
- Natural-language query understanding
- Retrieval of semantically related code
- Noise introduced by irrelevant results

---

## Hybrid Retrieval

The final retrieval layer will combine:

- Exact matching
- Symbol metadata
- Structural relationships
- Semantic similarity

Evaluation should measure whether hybrid retrieval improves relevant-context recall without introducing excessive irrelevant context.

A useful comparison will be:

```text
Exact Retrieval
       |
       v
Structural Retrieval
       |
       v
Semantic Retrieval
       |
       v
Hybrid Retrieval
```

The objective is not simply to maximize the number of retrieved files, but to provide the review agent with the smallest useful set of high-quality repository context.

---

# Planned Agent Evaluation

Once review and fixing agents are implemented, evaluation will include the following dimensions.

## Review Accuracy

Measure:

- True positive findings
- False positive findings
- Missed defects
- Severity classification

The evaluation dataset should contain intentionally buggy repositories with known expected defects so findings can be compared against a ground-truth result.

---

## Root-Cause Quality

Measure whether the agent identifies the actual source of a reported defect rather than only describing its symptoms.

A strong result should connect:

```text
Observed Behavior
        |
        v
Relevant Code
        |
        v
Root Cause
```

The evaluation should distinguish a correct root-cause explanation from a response that merely restates the reported problem.

---

## Evidence Quality

Findings should reference concrete repository evidence whenever possible:

- File paths
- Symbols
- Line ranges
- Relevant repository relationships

The goal is to make findings independently reviewable by a developer.

---

## Fix Quality

Generated patches should be evaluated for:

- Correctness
- Scope
- Regression risk
- Test compatibility

Generated changes should be represented as explicit diffs so that the proposed change can be evaluated independently of the agent's explanation.

A high-quality fix should address the root cause while avoiding unnecessary modifications.

---

# Planned Validation Metrics

The validation loop will track:

- Tests passed
- Tests failed
- Validation attempts
- Successful fixes
- Failed fixes
- Retry count
- Final validation status

Agent retry loops will have explicit iteration limits.

A generated fix should not be considered successful solely because the agent produced a plausible patch. Validation must provide supporting evidence.

---

## Validation Evaluation

The future validation subsystem should evaluate whether:

1. The proposed change can be applied successfully.
2. Relevant tests execute successfully.
3. Existing tests continue to pass.
4. Regression tests pass where applicable.
5. Failed fixes are correctly detected.
6. Retry behavior remains bounded.
7. The final status accurately reflects the validation result.

Conceptually:

```text
Generated Fix
     |
     v
Apply in Controlled Environment
     |
     v
Run Validation
     |
 +---+---+
 |       |
PASS    FAIL
 |       |
 v       v
Success  Re-analysis
         |
         v
      Limited Retry
```

Repository code should be treated as untrusted input, so future execution-based evaluation should use controlled and isolated environments.

---

# Initial Evaluation Dataset

The project will use small intentionally buggy Python repositories as the initial evaluation dataset.

Representative defects should include:

1. Incorrect conditional logic
2. Missing error handling
3. Incorrect function arguments
4. Off-by-one errors
5. Failing API behavior
6. Regression-prone fixes

Each example should contain tests that allow a generated fix to be validated objectively.

The dataset should provide enough ground truth to evaluate:

- Whether the defect is detected
- Whether the root cause is correctly identified
- Whether the relevant code is retrieved
- Whether the generated patch addresses the defect
- Whether validation confirms the fix

---

# Evaluation by Development Stage

| Stage | Primary Evaluation |
|---|---|
| Milestones 1–2 | Repository scanning, parsing, indexing, relationships |
| Milestone 3 | Exact, structural, semantic, and hybrid retrieval |
| Review Agent | Defect detection, root cause, severity, evidence |
| Fix Agent | Patch correctness, scope, regression risk |
| Validation | Tests, validation evidence, failure detection |
| Agentic Workflow | Retry behavior, bounded iterations, final status |

This staged approach prevents higher-level agent behavior from being evaluated without first establishing the correctness of the repository-intelligence and retrieval foundations.

---

# Success Criteria

A successful MVP should:

- Correctly analyze the target repository.
- Reliably identify the relevant source artifacts.
- Provide a plausible and evidence-based root-cause explanation.
- Generate a targeted fix when the agent layer is implemented.
- Execute available validation checks.
- Clearly report whether the fix was validated.
- Detect unsuccessful fixes.
- Keep retry iterations bounded.
- Provide enough evidence for a developer to review the result.

For the current milestone, success is narrower: the deterministic repository-intelligence foundation should remain correct and reproducible, with the automated test suite passing and static analysis clean.

---

# Evaluation Philosophy

The project follows a progression:

```text
Deterministic correctness
          |
          v
Repository retrieval quality
          |
          v
Review quality
          |
          v
Fix correctness
          |
          v
Validation success
```

Each stage should have measurable evidence before the next layer is treated as production-ready.

This evaluation strategy is intentionally aligned with the architecture: deterministic repository understanding provides the baseline, retrieval provides relevant context, agents perform reasoning and change generation, and validation provides evidence that the resulting changes actually work.