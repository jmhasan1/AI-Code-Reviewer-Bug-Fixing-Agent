# System Architecture

## Overview

The AI Code Reviewer & Bug-Fixing Agent is an agentic AI system designed to analyze software repositories, identify bugs and code-quality issues, propose fixes, and validate those changes through automated testing.

## High-Level Workflow

```text
User
 |
 v
Repository Input
 |
 v
Repository Scanner
 |
 +-- File Discovery
 +-- Language Detection
 +-- Code Parsing
 |
 v
Code Index / Retrieval
 |
 +-- Semantic Retrieval
 +-- Metadata Retrieval
 +-- Relevant Code Context
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
 +-- Static Analysis
 +-- Automated Tests
 |
 v
Validation Decision
 |
 +-- Passed --> Final Report
 |
 +-- Failed --> Limited Retry
```

## Core Components

### Repository Ingestion

Discovers source files, identifies supported languages, filters irrelevant files, and extracts structured code artifacts.

### Code Retrieval

Provides relevant repository context to the AI reviewer using code-aware retrieval and metadata such as file paths, symbols, and line ranges.

### Review Agent

Analyzes the repository and user-reported issue, identifies potential bugs, determines root causes, and produces structured review findings.

### Fix Agent

Generates targeted code changes based on the review findings and retrieved repository context.

### Validation

Runs appropriate validation checks against proposed changes. Generated fixes are not considered successful until validation provides supporting evidence.

### Agent Orchestration

LangGraph will coordinate the review, fixing, and validation workflow using structured shared state and bounded retry loops.

## Design Principles

1. **Modularity** — Components are separated so they can evolve independently.
2. **Evidence-based analysis** — Findings should reference concrete repository artifacts.
3. **Structured outputs** — Agent results should use typed schemas rather than relying solely on free-form text.
4. **Validation before success** — A generated fix should be validated before being presented as successful.
5. **Controlled execution** — Repository code is treated as untrusted input.
6. **Extensibility** — Python is the initial supported language, with the architecture designed for additional languages.
7. **Human oversight** — The system assists developers rather than silently modifying production code.

## Initial Language Strategy

Python is the first supported language because it provides a strong MVP path through the built-in AST, pytest, and mature static-analysis tooling.

The repository ingestion layer will use language-specific parsers behind a common interface so additional languages can be introduced without redesigning the agent workflow.
