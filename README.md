# N8n JSON Linter – Project Brief (Final)

## Overview

The **N8n JSON Linter** is a Python-based CLI tool designed to validate JSON structures within n8n workflows. The tool will:

1. Perform **basic JSON validation** (well-formedness, schema correctness where applicable).
2. Provide **node-by-node linting** by validating JSON against known property requirements for each n8n node type.
3. Offer **clear, informative logging** for identifying missing, malformed, or extra properties in workflows.
4. Support **machine-readable output** for CI/CD integration, with optional JSON output mode.

The project will be released as a **single monolithic package**, built and distributed using `uv` (with `uvx` for runtime execution). This ensures users avoid dependency issues during installation and use.

The goal is to make debugging n8n workflows more efficient by pinpointing exactly where and why validation errors occur.

---

## Project Goals

* **Stage 1 (MVP)**

  * CLI tool for validating JSON workflows.
  * Basic JSON linting (ensure valid JSON structure).
  * Node-by-node linting for a **core subset of nodes** (e.g., Function, HTTP Request, Set, IF, Switch) with design considerations for expanding to full coverage.
  * Logging with clear error reports (console + verbose output).
  * Manual schema acquisition: add node schemas by hand, with a placeholder system to expand coverage.
  * Error severity levels:

    * **Error** for missing required properties.
    * **Warning** for empty/unused properties.
    * **Info** for additional helpful checks.
  * CLI flag for JSON output to support CI/CD pipelines.

* **Stage 2 (Iteration & Enhancements)**

  * Expand support to include all built-in n8n nodes.
  * Add configuration file (`.n8nlintrc`) for user-defined rules.
  * Schema management improvements (option to add nodes manually with command flag).
  * Richer logging (structured JSON output with severity).
  * Unit tests for linting rules with baseline coverage goals.

* **Stage 3 (Future Enhancements)**

  * Automatic schema updates from n8n GitHub or other sources (e.g., [context7.com](https://context7.com/?q=n8n)).
  * VS Code extension with inline diagnostics.
  * CI/CD plugins (GitHub Action, pre-commit hook).
  * Exportable report formats (HTML, Markdown).
  * Web-based GUI for linting results.

---

## Key Features

* **CLI Tool**: Run with `uvx n8n-linter validate workflow.json`.
* **Logging**: Configurable verbosity (info, warning, error, debug).
* **Error Highlighting**: Identifies missing properties, invalid values, or extra keys.
* **Node Awareness**: Validates against known property requirements for each n8n node type.
* **Machine-Readable Output**: JSON output option for CI/CD workflows.
* **Standalone Distribution**: Zero external dependencies for runtime users.

---

## Folder Structure

```bash
n8n-linter/
├── pyproject.toml        # Project metadata & dependencies (for uv & PyPI)
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── src/
│   └── n8n_linter/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py        # Entry point for CLI
│       ├── validator.py  # Core JSON & schema validation logic
│       ├── logger.py     # Logging utilities
│       ├── schemas/      # Node schema definitions (manual + future scraping)
│       └── utils.py      # Helper functions
├── tests/
│   ├── test_validator.py
│   ├── test_cli.py
│   └── test_schemas.py
├── examples/
│   └── sample_workflow.json
└── .gitignore
```

---

## PyPI & Packaging

* **Distribution**: Package will be published to PyPI under the name `n8n-linter`.
* **Build System**: `uv` handles builds and dependency resolution.
* **Command**: Users run via `uvx n8n-linter` without needing to manage dependencies.
* **Entry Point**: Defined in `pyproject.toml` as `n8n-linter= n8n_linter.cli:main`.
* **License**: MIT, included in repo.

---

## Current Iteration Tasks (Weekend Goal)

* [ ] Implement CLI skeleton with `typer` (preferred) or `argparse`.
* [ ] Add basic JSON linting (ensure valid JSON, readable structure).
* [ ] Implement logging with verbosity options.
* [ ] Add initial node schema definitions for a core subset of nodes.
* [ ] Validate workflows against these schemas.
* [ ] Support JSON output mode for CI/CD integration.
* [ ] Add unit tests for core functionality (loose coverage targets).

---

## Future Enhancements

* Schema auto-update from n8n repository or [context7.com](https://context7.com/?q=n8n).
* Expand schema coverage to all official & custom nodes.
* VS Code extension support.
* CI/CD integration plugin.
* Exportable report formats (JSON, HTML, Markdown).
* Web-based visualiser for linting results.
* Performance improvements for very large workflows.

---

## Development Principles

* **Correctness First**: Prioritise accuracy over performance in MVP.
* **Extensible Design**: Build with future node support in mind.
* **Verbose by Default**: Output should be helpful and review-friendly, similar to `mkdocs validate`.
* **Loose Test Coverage Early**: Ensure testing is in place but avoid over-constraining while schemas stabilise.

---

## Summary

This brief defines the project scope, goals, folder structure, packaging, and development roadmap. It includes current iteration tasks and longer-term enhancements. With schemas manually defined at first and an extensible architecture, the project is well-scoped for weekend development and future expansion. This document is production-ready as a developer hand-off guide.
