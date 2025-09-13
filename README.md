# n8n-lint

A simple Python CLI tool for validating n8n workflow JSON files.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-87%20passing-green.svg)](https://github.com/your-username/n8n-lint)
[![Coverage](https://img.shields.io/badge/coverage-88%25-green.svg)](https://github.com/your-username/n8n-lint)

## Quick Start

```bash
# Use with uvx (recommended)
uvx n8n-lint validate workflow.json

# Or install with pip
pip install n8n-lint
n8n-lint validate workflow.json
```

## Features

- ✅ **Validate n8n workflows** - Check JSON structure and node properties
- ✅ **Complete CLI interface** - validate, import-schema, list-schemas, export-report
- ✅ **Multiple output formats** - Console, JSON, HTML, and Markdown
- ✅ **Custom schemas** - Import your own node schemas
- ✅ **Rich formatting** - Beautiful console output with progress bars
- ✅ **Report generation** - Export validation reports in HTML/Markdown
- ✅ **High performance** - Validates 1000+ nodes in under a second
- ✅ **Production ready** - 87 tests passing, 0 linting issues

## Installation

### Using uvx (Recommended)

```bash
uvx n8n-lint validate workflow.json
```

### Using pip

```bash
pip install n8n-lint
n8n-lint validate workflow.json
```

### From Source

```bash
git clone https://github.com/your-username/n8n-lint.git
cd n8n-lint
uv sync
uv run n8n-lint validate workflow.json
```

## Usage

### Basic Validation

```bash
# Validate a workflow file
n8n-lint validate workflow.json

# Validate with JSON output
n8n-lint validate workflow.json --output json

# Quiet mode (errors only)
n8n-lint validate workflow.json --quiet
```

### Schema Management

```bash
# List available schemas
n8n-lint list-schemas

# Import a custom schema
n8n-lint import-schema custom-schema.json --node-type my-custom-node
```

### Report Generation

```bash
# Export HTML report
n8n-lint export-report workflow.json --output report.html --format html

# Export Markdown report
n8n-lint export-report workflow.json --output report.md --format markdown
```

### Command Reference

```bash
# Show help
n8n-lint --help

# Show version
n8n-lint --version

# Validate command help
n8n-lint validate --help
```

## Exit Codes

- `0` - Success (no errors)
- `1` - Validation errors found
- `2` - Warnings found
- `3` - Info messages only

## Performance

n8n-lint is optimized for speed and efficiency:

- ⚡ **Fast validation** - Validates 1000+ nodes in under a second
- 🚀 **Schema caching** - Intelligent caching for repeated node types
- 💾 **Memory efficient** - Minimal memory footprint for large workflows
- 🔄 **Progress tracking** - Real-time progress updates for long validations

### Performance Benchmarks

| Workflow Size | Validation Time | Memory Usage |
| ------------- | --------------- | ------------ |
| 100 nodes     | ~0.1s           | ~5MB         |
| 500 nodes     | ~0.3s           | ~15MB        |
| 1000 nodes    | ~0.7s           | ~25MB        |

## Supported Node Types

- `n8n-nodes-base.function` - JavaScript execution
- `n8n-nodes-base.httpRequest` - HTTP API calls
- `n8n-nodes-base.set` - Data manipulation
- `n8n-nodes-base.if` - Conditional logic
- `n8n-nodes-base.switch` - Multi-condition logic

## Examples

### Valid Workflow

```json
{
  "name": "My Workflow",
  "nodes": [
    {
      "id": "1",
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "typeVersion": 1,
      "position": [100, 100]
    },
    {
      "id": "2",
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [300, 100],
      "parameters": {
        "url": "https://api.example.com",
        "method": "GET"
      }
    }
  ],
  "connections": {
    "Start": {
      "main": [
        [
          {
            "node": "HTTP Request",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

### Validation Output

```bash
$ n8n-lint validate workflow.json
✅ Validation complete: No issues found
```

### Error Output

```bash
$ n8n-lint validate invalid-workflow.json
❌ ERROR: Required property 'typeVersion' is missing (Node: n8n-nodes-base.function, Property: typeVersion, Line: 2, File: invalid-workflow.json)
  Expected: present
  Actual: missing
```

## JSON Output

For automation and CI/CD integration:

```bash
n8n-lint validate workflow.json --output json
```

```json
{
  "timestamp": "2025-09-08T10:30:00.000Z",
  "validation_result": {
    "errors": [
      {
        "message": "Required property 'typeVersion' is missing",
        "severity": "error",
        "node_type": "n8n-nodes-base.function",
        "property_path": "typeVersion",
        "expected": "present",
        "actual": "missing",
        "line_number": 2,
        "file_path": "workflow.json"
      }
    ],
    "summary": {
      "errors": 1,
      "warnings": 0,
      "info": 0,
      "total_messages": 1,
      "total_nodes": 2,
      "validation_time": 0.001,
      "file_path": "workflow.json",
      "has_errors": true,
      "has_warnings": false,
      "has_info": false,
      "is_success": false
    }
  }
}
```

## Development

### Setup

```bash
git clone https://github.com/your-username/n8n-lint.git
cd n8n-lint
uv sync
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/n8n_lint

# Run specific test file
uv run pytest tests/test_validator.py
```

### Code Quality

```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check

# Type checking
uv run mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation:** [Github Pages](https://capp3.github.io/n8n-lint/)
- **Issues:** [GitHub Issues](https://github.com/capp3/n8n-lint/issues)
- **Discussions:** [GitHub Discussions](https://github.com/capp3/n8n-lint/discussions)

## Roadmap

- [ ] VS Code extension for real-time validation
- [ ] Additional node type support as needed
- [ ] Configuration file support
- [ ] Performance optimizations for large workflows

---

**n8n-lint** - Simple, fast, and reliable n8n workflow validation.
