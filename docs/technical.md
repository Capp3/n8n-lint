# Technical Documentation

## Project Overview

**N8n JSON Linter** - A Python CLI tool for validating n8n workflow JSON structures with node-by-node schema validation.

## Architecture Decisions

### Technology Stack

- **Language**: Python 3.12+
- **CLI Framework**: Typer (for modern CLI with type hints)
- **Output Formatting**: Rich (for colored console output)
- **Testing**: pytest with pytest-cov
- **Linting**: ruff (replaces black, isort, flake8)
- **Type Checking**: mypy (replaces "ty" dependency)
- **Build System**: uv (modern Python package manager)
- **Documentation**: mkdocs with material theme

### Project Structure

```
src/n8n_lint/
├── __init__.py          # Package metadata
├── __main__.py          # Entry point for python -m
├── cli.py              # CLI interface with Typer
├── validator.py        # Core validation logic
├── logger.py           # Logging and output formatting
├── utils.py            # Utility functions
└── schemas/            # Node schema definitions
    ├── __init__.py
    ├── registry.json   # Schema metadata and validation
    ├── function.json
    ├── http_request.json
    ├── set.json
    ├── if.json
    └── switch.json
```

## Design Decisions

### Schema Management Strategy

**Decision**: Hybrid Schema System with directory storage and CLI-managed registry
**Rationale**:

- Combines flexibility of directory-based storage with robustness of registry management
- CLI import capability addresses extensibility requirement
- JSON Schema format for maximum compatibility
- Automatic discovery with metadata validation
- Supports both manual creation and user-defined schemas

**Implementation**:

- `schemas/` directory for individual JSON schema files
- `schemas/registry.json` for metadata and validation
- CLI command `n8n_lint import-schema <file>` for adding new schemas
- Schema validation on import with conflict resolution

### Validation Engine Architecture

**Decision**: Rule-based validation engine with configurable strictness
**Rationale**:

- Highly modular and extensible design
- Easy to add new validation rules
- Clear separation of concerns
- Testable individual rules
- Supports configurable strictness levels (strict, balanced, lenient)
- Comprehensive validation with detailed error reporting

**Implementation**:

- Base `ValidationRule` abstract class
- Specific rules (RequiredProperty, TypeValidation, etc.)
- `ValidationEngine` to coordinate rules
- Configuration system for strictness levels
- Error aggregation system

### Error Aggregation Strategy

**Decision**: Hybrid error system with flat storage and hierarchical grouping
**Rationale**:

- Best performance benefits of flat storage with rich presentation capabilities
- Supports both simple levels (Error, Warning, Info) and detailed categories
- Full context reporting including node type, property path, expected vs actual
- Node-based grouping with summary + details
- Severity-based prioritization and sorting

**Implementation**:

- `ValidationError` class with full context
- `ErrorAggregator` for collection and grouping
- Severity-based sorting and filtering
- Reporting formatters for console and JSON output
- Node-based grouping with summaries

### JSON Parsing Strategy

**Decision**: Hybrid parser with standard JSON parsing and intelligent error recovery
**Rationale**:

- Reliability of standard JSON parsing with added error recovery
- Provides helpful error messages and suggestions
- Meets requirement for small file handling (< 1MB)
- Node-by-node processing for validation
- Intelligent error recovery for common issues

**Implementation**:

- Standard JSON parser for reliability
- Error recovery for common issues (missing commas, quotes)
- Error suggestion system
- Node-by-node processing for validation
- Helpful error messages with context

### CLI Integration Strategy

**Decision**: Hybrid command structure with direct validation and subcommands
**Rationale**:

- Simplicity of direct validation for common use cases
- Extensibility for advanced features like schema import
- Rich formatting with plain text fallback
- Detailed exit codes for different scenarios

**Implementation**:

- Direct validation as default command (`n8n_lint <file>`)
- `--plain-text` flag for Rich formatting fallback
- `--output json` for machine-readable output
- Detailed exit codes (0=success, 1=errors, 2=warnings, 3=info only)
- Subcommands for advanced features (import-schema)

## Dependencies

### Runtime Dependencies

- `typer`: CLI framework with type hints
- `rich`: Console output formatting and colors

### Development Dependencies

- `pytest>=8.3.5`: Testing framework
- `pytest-cov>=6.1.1`: Coverage reporting
- `ruff>=0.11.11`: Linting and formatting
- `mypy`: Type checking
- `mkdocs>=1.6.1`: Documentation generation
- `mkdocs-material>=9.6.14`: Documentation theme

### Build Dependencies

- `uv`: Package management and building
- `pyinstaller>=6.13.0`: Standalone executable creation

## Implementation Phases

### Phase 1: Foundation

- Fix packaging inconsistencies
- Create schema directory structure
- Implement basic logger with verbosity controls

### Phase 2: Core Validation

- Implement JSON validation engine
- Create initial node schemas
- Build node-by-node validation logic

### Phase 3: CLI Integration

- Implement validate command
- Add verbosity controls and JSON output
- Implement proper exit codes

### Phase 4: Testing

- Unit tests for all functionality
- Integration tests
- Achieve ≥60% test coverage

### Phase 5: Documentation

- Update all documentation
- Create examples and test data
- Add Tasks and Status pages

## Risk Mitigation

### Schema Complexity

- Start with core nodes only
- Design extensible schema system
- Document schema assumptions
- Add "unknown node" warnings

### Performance

- Monitor memory usage with large files
- Add file size warnings
- Consider streaming for very large workflows
- Benchmark performance

### Schema Accuracy

- Test against real n8n workflows
- Document schema assumptions
- Add validation for schema completeness
- Regular updates from n8n documentation

## Future Enhancements

### Stage 2 (Post-MVP)

- Expand to all built-in n8n nodes
- Add configuration file support
- Automatic schema updates
- Richer logging and reporting

### Stage 3 (Long-term)

- VS Code extension
- CI/CD plugins
- Web-based GUI
- Performance optimizations

## Development Guidelines

### Code Style

- Follow PEP 8 with ruff formatting
- Use type hints throughout
- Maximum line length: 120 characters
- Use absolute imports

### Testing

- Unit tests for all public functions
- Integration tests for CLI commands
- Test coverage ≥60% baseline
- Mock external dependencies

### Documentation

- Google-style docstrings
- Type hints for all functions
- Keep README.md updated
- Document all CLI options

## Environment Setup

### Development

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run ruff format .

# Run type checking
uv run mypy src/
```

### Production

```bash
# Install via uvx
uvx n8n_lint validate workflow.json

# Or install package
uv add n8n_lint
n8n_lint validate workflow.json
```

## Version History

- **v0.0.1**: Initial project setup with basic structure
- **v0.1.0**: MVP with core validation functionality (planned)
- **v0.2.0**: Expanded node support and configuration (planned)
- **v1.0.0**: Full feature set with all n8n nodes (planned)
