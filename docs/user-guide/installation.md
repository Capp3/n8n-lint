# Installation Guide

This guide covers all the different ways to install and set up n8n-lint.

## Prerequisites

- Python 3.12 or higher
- pip or uv package manager

## Installation Methods

### Method 1: Using pip (Recommended for most users)

```bash
pip install n8n-lint
```

### Method 2: Using uv (Recommended for development)

```bash
# Install uv if you haven't already
pip install uv

# Install n8n-lint
uv add n8n-lint

# Or use uvx for one-time usage
uvx n8n-lint validate workflow.json
```

### Method 3: From Source

```bash
# Clone the repository
git clone https://github.com/capp3/n8n_lint.git
cd n8n_lint

# Install in development mode
pip install -e .

# Or using uv
uv sync
uv run n8n_lint validate workflow.json
```

## Verification

After installation, verify that n8n-lint is working correctly:

```bash
# Check version
n8n_lint --version

# Should output: n8n-lint version 1.1.0

# Check help
n8n_lint --help
```

## Virtual Environments

It's recommended to use a virtual environment:

### Using venv

```bash
# Create virtual environment
python -m venv n8n-lint-env

# Activate (Linux/macOS)
source n8n-lint-env/bin/activate

# Activate (Windows)
n8n-lint-env\Scripts\activate

# Install n8n-lint
pip install n8n-lint
```

### Using uv

```bash
# Create project with uv
uv init my-project
cd my-project

# Add n8n-lint as dependency
uv add n8n-lint

# Run n8n-lint
uv run n8n_lint validate workflow.json
```

## Global vs Local Installation

### Global Installation

```bash
pip install n8n-lint
# Available system-wide
n8n_lint --help
```

### Local Installation (Project-specific)

```bash
# In your project directory
pip install --user n8n-lint
# Or
uv add n8n-lint
```

## Docker Installation

If you prefer to use Docker:

```bash
# Build Docker image
docker build -t n8n-lint .

# Run validation
docker run --rm -v $(pwd):/workspace n8n-lint validate /workspace/workflow.json
```

## Troubleshooting Installation

### Common Issues

**Issue**: `command not found: n8n_lint`

```bash
# Solution: Add Python user bin to PATH
export PATH="$HOME/.local/bin:$PATH"
```

**Issue**: Permission denied

```bash
# Solution: Use --user flag
pip install --user n8n-lint
```

**Issue**: Python version too old

```bash
# Solution: Upgrade Python or use pyenv
pyenv install 3.12.0
pyenv local 3.12.0
```

### Platform-Specific Notes

#### Windows

- Make sure Python is in your PATH
- Use PowerShell or Command Prompt
- Consider using Windows Subsystem for Linux (WSL)

#### macOS

- Use Homebrew to install Python: `brew install python`
- May need to update PATH in your shell profile

#### Linux

- Use your package manager to install Python 3.12+
- Ubuntu/Debian: `sudo apt install python3.12 python3.12-pip`
- CentOS/RHEL: `sudo yum install python312 python312-pip`

## Next Steps

After successful installation:

1. [Basic Usage Guide](basic-usage.md) - Learn how to validate workflows
2. [Examples](../examples/sample_workflow.json) - See common usage patterns
3. [CLI Reference](../cli-reference/index.md) - Complete command documentation

## Support

If you encounter installation issues:

- Check the [CLI Reference](../cli-reference/index.md)
- [Open an issue](https://github.com/capp3/n8n_lint/issues)
