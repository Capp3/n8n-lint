# Development Setup

This guide covers setting up a development environment for n8n-lint.

## Prerequisites

- Python 3.12 or higher
- Git
- uv (recommended) or pip

## Quick Setup

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/capp3/n8n_lint.git
cd n8n_lint

# Install uv if you haven't already
pip install uv

# Install dependencies
uv sync --all-groups

# Activate the environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Run tests to verify setup
uv run pytest tests/
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/capp3/n8n_lint.git
cd n8n_lint

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev,test,security]"

# Run tests to verify setup
pytest tests/
```

## Development Dependencies

The project includes several dependency groups:

- **dev** - Development tools (pytest, pre-commit, ruff, mypy)
- **test** - Testing framework and tools
- **security** - Security scanning tools (safety, bandit)

## Project Structure

```
n8n_lint/
├── src/n8n_lint/          # Main package
│   ├── cli/               # CLI interface
│   ├── core/              # Core functionality
│   ├── formatters/        # Output formatters
│   ├── schemas/           # Schema management
│   └── utils/             # Utility functions
├── tests/                 # Test suite
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD workflows
└── pyproject.toml         # Project configuration
```

## Development Commands

### Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run with coverage
uv run pytest tests/ --cov=src/n8n_lint

# Run specific test file
uv run pytest tests/test_validator.py

# Run with verbose output
uv run pytest tests/ -v
```

### Code Quality

```bash
# Run linting
uv run ruff check .

# Run formatting
uv run ruff format .

# Run type checking
uv run mypy src/

# Run security checks
uv run safety check
uv run bandit -r src/
```

### Building

```bash
# Build package
uv build

# Check build artifacts
ls -la dist/
```

## IDE Setup

### VS Code

Install recommended extensions:

- Python
- Pylance
- Ruff
- MyPy Type Checker

### PyCharm

Configure the Python interpreter to use the virtual environment:

- File → Settings → Project → Python Interpreter
- Add interpreter → Existing environment
- Select `.venv/bin/python`

## Pre-commit Hooks

Set up pre-commit hooks for automatic code quality checks:

```bash
# Install pre-commit
uv run pre-commit install

# Run on all files
uv run pre-commit run --all-files
```

## Testing Workflow

### Running CLI

```bash
# Test CLI commands
uv run n8n_lint --help
uv run n8n_lint validate tests/test.json
uv run n8n_lint list-schemas
```

### Manual Testing

```bash
# Create test workflow
echo '{"nodes": [{"id": "test", "type": "n8n-nodes-base.function"}], "connections": {}}' > test.json

# Validate
uv run n8n_lint validate test.json

# Clean up
rm test.json
```

## Debugging

### Using ipdb

```python
# Add breakpoint in code
import ipdb; ipdb.set_trace()

# Run with debugger
uv run pytest tests/test_validator.py -s
```

### Verbose Logging

```bash
# Enable debug logging
uv run n8n_lint validate workflow.json --debug
```

## Documentation Development

### Building Documentation

```bash
# Install documentation dependencies
uv sync --group dev

# Build documentation
uv run mkdocs build

# Serve documentation locally
uv run mkdocs serve
```

### Documentation Structure

- `docs/index.md` - Main documentation page
- `docs/user-guide/` - User documentation
- `docs/cli-reference/` - CLI documentation
- `docs/api-reference/` - API documentation
- `docs/developer/` - Developer documentation

## Contributing Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Make changes**
4. **Run tests and quality checks**
   ```bash
   uv run pytest tests/
   uv run ruff check .
   uv run mypy src/
   ```
5. **Commit changes**
   ```bash
   git commit -m "Add my feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/my-feature
   ```
7. **Create a pull request**

## Troubleshooting

### Common Issues

**Issue**: Import errors

```bash
# Solution: Ensure you're in the virtual environment
source .venv/bin/activate
```

**Issue**: Test failures

```bash
# Solution: Check Python version
python --version  # Should be 3.12+

# Solution: Reinstall dependencies
uv sync --all-groups --reinstall
```

**Issue**: Build failures

```bash
# Solution: Clean build artifacts
rm -rf dist/ build/ *.egg-info/
uv build
```

### Getting Help

- [GitHub Issues](https://github.com/capp3/n8n_lint/issues)
- [Discussions](https://github.com/capp3/n8n_lint/discussions)
- [Documentation](https://capp3.github.io/n8n_lint/)

## Next Steps

- [GitHub Repository](https://github.com/capp3/n8n_lint) - Source code and issues
- [API Reference](../api-reference/index.md) - Complete API documentation
