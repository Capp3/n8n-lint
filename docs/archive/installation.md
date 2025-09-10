# Installation

This document provides installation instructions for the n8n JSON Linter.

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

## Installation Methods

### Method 1: Using uv (Recommended)

The easiest way to install and use n8n-lint is with `uvx`:

```bash
# Run directly without installation
uvx n8n-lint validate workflow.json

# Or install globally
uv tool install n8n-lint
```

### Method 2: From Source

```bash
# Clone the repository
git clone https://github.com/your-username/n8n-lint.git
cd n8n-lint

# Install dependencies
uv sync

# Install the package
uv pip install -e .
```

### Method 3: Using pip

```bash
# Install from PyPI (when available)
pip install n8n-lint
```

## Verification

After installation, verify that n8n-lint is working correctly:

```bash
# Check version
n8n-lint --version

# Run help
n8n-lint --help

# Test with sample workflow
n8n-lint validate examples/sample_workflow.json
```

## Troubleshooting

### Common Issues

1. **Python Version**: Ensure you're using Python 3.12 or higher
2. **uv Not Found**: Install uv from [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
3. **Permission Errors**: Use `--user` flag with pip or ensure proper permissions

### Getting Help

- Check the [Usage Guide](usage.md) for detailed examples
- Review [GitHub Issues](https://github.com/your-username/n8n-lint/issues) for known problems
- Join [GitHub Discussions](https://github.com/your-username/n8n-lint/discussions) for community support
