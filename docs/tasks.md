# Tasks

## LEVEL 3 COMPREHENSIVE IMPLEMENTATION PLAN

### Requirements Analysis

- **Core Requirements:**

  - [ ] CLI tool for n8n workflow validation with Typer
  - [ ] JSON structure validation (well-formedness)
  - [ ] Node-by-node schema validation for core n8n nodes
  - [ ] Configurable logging with verbosity levels
  - [ ] Machine-readable JSON output for CI/CD integration
  - [ ] Comprehensive test coverage (≥60% baseline)

- **Technical Constraints:**
  - [ ] Python 3.12+ compatibility
  - [ ] Single monolithic package distribution via `uv`
  - [ ] Zero external runtime dependencies
  - [ ] Support for `uvx n8n_lint` execution
  - [ ] MIT license compliance

### Components Affected

#### 1. CLI Module (`src/n8n_lint/cli.py`)

- **Changes needed:**
  - [ ] Replace placeholder with proper `validate` command
  - [ ] Add verbosity controls (`-q`, `-v`, `-vv`)
  - [ ] Add JSON output option (`--output json`)
  - [ ] Add file path argument handling
  - [ ] Implement proper exit codes
- **Dependencies:** `typer`, `rich`, `validator`, `logger`

#### 2. Validator Module (`src/n8n_lint/validator.py`)

- **Changes needed:**
  - [ ] JSON parsing and validation logic
  - [ ] Schema loading and management
  - [ ] Node-by-node validation engine
  - [ ] Error collection and reporting
  - [ ] Integration with logger
- **Dependencies:** `json`, `pathlib`, `schemas`, `logger`

#### 3. Logger Module (`src/n8n_lint/logger.py`)

- **Changes needed:**
  - [ ] Configurable verbosity levels
  - [ ] Structured logging with severity levels
  - [ ] JSON output formatting
  - [ ] Console output formatting
- **Dependencies:** `logging`, `json`, `rich`

#### 4. Schemas Module (`src/n8n_lint/schemas/`)

- **Changes needed:**
  - [ ] Create schema directory structure
  - [ ] Define core node schemas (Function, HTTP Request, Set, IF, Switch)
  - [ ] Schema loading utilities
  - [ ] Validation rule definitions
- **Dependencies:** `json`, `pathlib`

#### 5. Utils Module (`src/n8n_lint/utils.py`)

- **Changes needed:**
  - [ ] File I/O utilities
  - [ ] JSON handling helpers
  - [ ] Error formatting utilities
- **Dependencies:** `pathlib`, `json`

#### 6. Test Suite (`tests/`)

- **Changes needed:**
  - [ ] CLI command testing
  - [ ] Validator logic testing
  - [ ] Schema validation testing
  - [ ] Integration testing
  - [ ] Mock data and fixtures
- **Dependencies:** `pytest`, `pytest-cov`

### Design Decisions Required (Creative Phases)

#### 🎨 Architecture Design

- [ ] **Schema Management Strategy**

  - Decision: How to structure and load node schemas
  - Options: JSON files, Python modules, or hybrid approach
  - Impact: Extensibility and maintainability

- [ ] **Validation Engine Architecture**
  - Decision: How to organize validation rules and error reporting
  - Options: Plugin-based, rule-based, or monolithic approach
  - Impact: Performance and extensibility

#### ⚙️ Algorithm Design

- [ ] **Error Aggregation Strategy**

  - Decision: How to collect and prioritize validation errors
  - Options: Fail-fast, collect-all, or severity-based
  - Impact: User experience and performance

- [ ] **JSON Parsing Strategy**
  - Decision: How to handle large workflow files and memory usage
  - Options: Streaming, chunked, or full-load parsing
  - Impact: Performance and memory usage

### Implementation Strategy

#### Phase 1: Foundation (Setup & Core Structure)

1. [ ] **Fix packaging inconsistencies**
   - Align CLI command name between README and pyproject.toml
   - Fix description typo and add classifiers
   - Replace "ty" dependency with mypy
2. [ ] **Create schema directory structure**
   - Create `src/n8n_lint/schemas/` directory
   - Add `__init__.py` and `registry.json` for metadata
   - Implement schema loading utilities
3. [ ] **Implement basic logger**
   - Configurable verbosity levels
   - Console and JSON output formatting
   - Integration with Rich for colored output

#### Phase 2: Core Validation Engine

1. [ ] **Implement JSON validation**
   - Hybrid parser with standard JSON parsing and error recovery
   - File path validation and error reporting
   - Integration with logger
2. [ ] **Create initial node schemas**
   - Function node schema (JSON Schema format)
   - HTTP Request node schema (JSON Schema format)
   - Set node schema (JSON Schema format)
   - IF node schema (JSON Schema format)
   - Switch node schema (JSON Schema format)
   - Update registry.json with metadata
3. [ ] **Build validation engine**
   - Rule-based validation engine with configurable strictness
   - Base ValidationRule class and specific rule implementations
   - Error aggregation system with hierarchical grouping

#### Phase 3: CLI Integration

1. [ ] **Implement hybrid CLI structure**
   - Direct validation as default command (`n8n_lint <file>`)
   - Verbosity controls (`-q`, `-v`, `-vv`)
   - JSON output option (`--output json`)
   - Plain text flag (`--plain-text`)
   - Detailed exit codes (0=success, 1=errors, 2=warnings, 3=info only)
2. [ ] **Add advanced CLI features**
   - Schema import command (`n8n_lint import-schema <file>`)
   - Help and documentation
   - Usage examples
   - Error message formatting

#### Phase 4: Testing & Quality Assurance

1. [ ] **Unit tests for core functionality**
   - CLI command testing
   - Validator logic testing
   - Schema validation testing
   - Logger functionality testing
2. [ ] **Integration testing**
   - End-to-end workflow validation
   - Error handling scenarios
   - Output format validation
3. [ ] **Coverage and quality checks**
   - Achieve ≥60% test coverage
   - Linting and code quality checks
   - Performance testing with large files

#### Phase 5: Documentation & Polish

1. [ ] **Update documentation**
   - Installation instructions
   - Usage examples
   - API documentation
   - Add Tasks and Status pages to mkdocs
2. [ ] **Create example files**
   - Sample n8n workflow
   - Test data for validation
   - CI/CD integration examples

### Dependencies & Integration Points

#### External Dependencies

- **typer**: CLI framework
- **rich**: Console output formatting
- **pytest**: Testing framework
- **mypy**: Type checking
- **ruff**: Linting and formatting

#### Internal Dependencies

- CLI → Validator → Schemas
- CLI → Logger
- Validator → Logger
- All modules → Utils

### Challenges & Mitigations

#### Challenge 1: Schema Complexity

- **Risk**: n8n node schemas are complex and may change
- **Mitigation**: Start with core nodes, design extensible schema system
- **Fallback**: Manual schema updates with clear documentation

#### Challenge 2: Performance with Large Workflows

- **Risk**: Large n8n workflows may cause memory issues
- **Mitigation**: Implement streaming JSON parsing, chunked processing
- **Fallback**: Add file size warnings and limits

#### Challenge 3: Schema Accuracy

- **Risk**: Manual schemas may not match actual n8n requirements
- **Mitigation**: Test against real n8n workflows, document assumptions
- **Fallback**: Add "unknown node" warnings instead of errors

### Testing Strategy

#### Unit Tests

- [ ] **CLI Tests**
  - Command parsing and argument handling
  - Exit code validation
  - Help text verification
- [ ] **Validator Tests**
  - JSON parsing edge cases
  - Schema validation logic
  - Error collection and reporting
- [ ] **Logger Tests**
  - Verbosity level handling
  - Output format validation
  - JSON vs console output

#### Integration Tests

- [ ] **End-to-End Tests**
  - Complete workflow validation
  - Error handling scenarios
  - Output format consistency
- [ ] **Performance Tests**
  - Large file handling
  - Memory usage validation
  - Response time benchmarks

### Documentation Plan

- [ ] **API Documentation**
  - Module docstrings
  - Function documentation
  - Type hints and examples
- [ ] **User Guide**
  - Installation instructions
  - Usage examples
  - Troubleshooting guide
- [ ] **Developer Documentation**
  - Architecture decisions
  - Schema extension guide
  - Contributing guidelines

## Active Tasks (MVP - Stage 1)

- [ ] **Phase 1: Foundation**
  - [ ] Fix packaging inconsistencies (CLI name, classifiers, dependencies)
  - [ ] Create schema directory structure
  - [ ] Implement basic logger with verbosity controls
- [ ] **Phase 2: Core Validation**
  - [ ] Implement JSON validation engine
  - [ ] Create initial node schemas (Function, HTTP Request, Set, IF, Switch)
  - [ ] Build node-by-node validation logic
- [ ] **Phase 3: CLI Integration**
  - [ ] Implement validate command with proper arguments
  - [ ] Add verbosity controls and JSON output option
  - [ ] Implement proper exit codes and error handling
- [ ] **Phase 4: Testing**
  - [ ] Unit tests for all core functionality
  - [ ] Integration tests for end-to-end validation
  - [ ] Achieve ≥60% test coverage
- [ ] **Phase 5: Documentation**
  - [ ] Update all documentation files
  - [ ] Create example workflows and test data
  - [ ] Add Tasks and Status pages to mkdocs

## Repo Hygiene / Packaging

- [ ] Align CLI command name between `README.md` and `pyproject.toml`
  - Acceptance: docs and `project.scripts` agree (`n8n_lint` vs `n8n-linter`).
- [ ] Fill `classifiers` and fix typos in `pyproject.toml`
  - Acceptance: meaningful classifiers added; description typo corrected.
- [ ] Replace `test` dependency "ty" with a real type checker or remove
  - Acceptance: use `mypy` (or document alternative) and ensure it runs locally/CI.
- [ ] Polish docs (`docs/index.md`, `docs/usage.md`, `docs/installation.md`) and add links to tasks/status
  - Acceptance: mkdocs renders nav with Tasks and Status pages.

## Memory Bank / Documentation

- [x] Create `docs/tasks.md` (this file)
- [x] Create and maintain `docs/status.md` with session updates
- [x] Create `docs/technical.md` to record decisions and dependencies
- [x] Create `docs/creative-decisions.md` with detailed design decisions
- [ ] (Optional) Establish `logs/` and `config/` directories per workspace rules

## Completed Tasks

- 2025-09-07: Created initial `docs/tasks.md` scaffolding.
- 2025-09-07: Created comprehensive Level 3 implementation plan.
- 2025-09-07: Completed all creative phase design decisions:
  - Schema Management Strategy: Hybrid system with directory storage and CLI-managed registry
  - Validation Engine Architecture: Rule-based validation with configurable strictness
  - Error Aggregation Strategy: Hybrid error system with flat storage and hierarchical grouping
  - JSON Parsing Strategy: Hybrid parser with standard JSON parsing and intelligent error recovery
  - CLI Integration Strategy: Hybrid command structure with direct validation and subcommands

## Notes / Context

- Python 3.12, `typer`, `ruff`, `pytest`, and `uv` are in use per `pyproject.toml`.
- Source of truth for work tracking is this `docs/tasks.md` file.
- **Complexity Level**: Level 3 (Intermediate Feature) - requires comprehensive planning and creative phases.
- **Next Mode**: CREATIVE mode for architecture and algorithm design decisions.
