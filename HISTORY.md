# History

## 1.1.1 (2025-09-13)

### Major Release - Mono Package Architecture & PyPI Deployment

#### 🚀 Major Features

- **Mono Package Architecture**: Complete restructuring into organized sub-packages
- **PyPI Deployment Pipeline**: Automated build and deployment with GitHub Actions
- **Documentation Overhaul**: Modern documentation with Read the Docs theme
- **Professional Quality**: 87 tests passing, zero linting issues, comprehensive security

#### ✨ New Features

- **Enhanced CLI Interface**: 4 core commands with multiple output formats
- **Comprehensive Validation Engine**: Node validation with detailed error reporting
- **Schema Management**: Support for custom node schemas
- **Rich Formatting**: Beautiful console output with progress bars

#### 🔧 Technical Improvements

- **Package Structure**: Organized into `cli/`, `core/`, `formatters/`, `schemas/`, `utils/`
- **Build System**: UV-powered with wheel and source distributions
- **Quality Assurance**: Automated testing, linting, formatting, and security scanning
- **Documentation**: Complete user guides, API reference, and developer documentation

#### 📦 Installation

```bash
pip install n8n-lint
# or
uvx n8n-lint validate workflow.json
```

#### 🎯 Usage

```bash
n8n-lint validate workflow.json
n8n-lint import-schema schema.json --node-type custom.node
n8n-lint export-report workflow.json --output report.html
```

#### 🔗 Resources

- **Repository**: https://github.com/capp3/n8n_lint
- **PyPI**: https://pypi.org/project/n8n-lint/
- **Documentation**: https://capp3.github.io/n8n_lint/

---

## 1.0.0 (2025-09-10)

### Initial Release

- Core validation engine for n8n workflows
- Basic CLI interface with validate command
- JSON output support for automation
- Comprehensive test suite (87 tests)
- Production-ready quality and documentation
