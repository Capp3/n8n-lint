# Release Notes - n8n-lint v1.1.0

**Release Date:** 2025-09-13  
**Version:** 1.1.0  
**Type:** Major Release - Mono Package Architecture & PyPI Deployment

---

## 🚀 **Major Features**

### Mono Package Architecture

- **Complete Restructuring**: Converted from single package to organized mono package structure
- **Modular Design**: Organized into logical sub-packages (`cli/`, `core/`, `formatters/`, `schemas/`, `utils/`)
- **Clean API**: Well-defined public API with proper imports and exports
- **Backward Compatibility**: Maintains existing CLI interface and functionality

### PyPI Deployment Pipeline

- **Automated Build**: UV-powered build system with wheel and source distributions
- **CI/CD Integration**: GitHub Actions workflow for automated PyPI deployment
- **Semantic Versioning**: Proper version management with automated releases
- **Security**: Secure credential management with PyPI API tokens

### Documentation Overhaul

- **Modern Structure**: Comprehensive documentation with user/developer separation
- **Read the Docs Theme**: Clean, professional documentation appearance
- **Quick Start Focus**: Optimized main page for immediate value
- **GitHub Pages**: Automated documentation deployment and hosting

---

## ✨ **New Features**

### Enhanced CLI Interface

- **4 Core Commands**: `validate`, `import-schema`, `list-schemas`, `export-report`
- **Multiple Output Formats**: Console, JSON, HTML, and Markdown
- **Rich Formatting**: Beautiful console output with progress bars and colors
- **Flexible Options**: Quiet, verbose, debug modes with comprehensive help

### Comprehensive Validation Engine

- **Node Validation**: Validates n8n workflow nodes against schemas
- **Error Reporting**: Detailed error messages with context and suggestions
- **Schema Management**: Support for custom node schemas
- **Performance**: Validates 1000+ nodes in under a second

### Professional Documentation

- **User Guides**: Complete installation, usage, and troubleshooting guides
- **API Reference**: Full Python API documentation with examples
- **CLI Reference**: Comprehensive command-line interface documentation
- **Developer Guide**: Development setup and contribution guidelines

---

## 🔧 **Technical Improvements**

### Package Structure

```
src/n8n_lint/
├── __init__.py (clean public API)
├── cli/ (command-line interface)
├── core/ (validation engine, logging, errors)
├── formatters/ (output formatters)
├── schemas/ (schema management)
└── utils/ (utility functions)
```

### Build System

- **UV Integration**: Fast, reliable build system with dependency management
- **Dual Distribution**: Both wheel and source distributions
- **Modern Metadata**: SPDX license format, proper classifiers
- **Quality Checks**: Automated linting, formatting, and type checking

### Testing & Quality

- **87 Tests**: Comprehensive test suite with 100% pass rate
- **Code Quality**: Zero linting issues, proper formatting
- **Security**: No vulnerabilities (Safety + Bandit scans)
- **Type Safety**: Full MyPy type checking compliance

---

## 📦 **Installation**

### Using pip

```bash
pip install n8n-lint
```

### Using uv (Recommended)

```bash
uvx n8n-lint validate workflow.json
```

### From Source

```bash
git clone https://github.com/capp3/n8n_lint.git
cd n8n_lint
uv sync
uv run n8n_lint validate workflow.json
```

---

## 🎯 **Usage Examples**

### Basic Validation

```bash
n8n_lint validate workflow.json
```

### JSON Output for Automation

```bash
n8n_lint validate workflow.json --output json
```

### Import Custom Schema

```bash
n8n_lint import-schema custom-schema.json --node-type my.custom.node
```

### Export HTML Report

```bash
n8n_lint export-report workflow.json --output report.html --format html
```

---

## 🔗 **Resources**

- **GitHub Repository**: [https://github.com/capp3/n8n_lint](https://github.com/capp3/n8n_lint)
- **PyPI Package**: [https://pypi.org/project/n8n-lint/](https://pypi.org/project/n8n-lint/)
- **Documentation**: [https://capp3.github.io/n8n_lint/](https://capp3.github.io/n8n_lint/)
- **Issues & Support**: [https://github.com/capp3/n8n_lint/issues](https://github.com/capp3/n8n_lint/issues)

---

## 🏆 **Achievements**

- ✅ **Production Ready**: Full PyPI deployment pipeline
- ✅ **Professional Quality**: Comprehensive documentation and testing
- ✅ **Developer Friendly**: Clean architecture and contribution guidelines
- ✅ **User Focused**: Simple CLI with powerful validation capabilities
- ✅ **Future Proof**: Modern tooling and sustainable architecture

---

## 🚀 **What's Next**

- **Community Feedback**: Gather user feedback and feature requests
- **Schema Expansion**: Add support for more n8n node types
- **Performance Optimization**: Further improvements to validation speed
- **IDE Integration**: Potential VS Code extension development

---

**Full Changelog**: [View complete changelog](https://github.com/capp3/n8n_lint/compare/v1.0.0...v1.1.0)
