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
```

### Core Components

#### 1. CLI Module (`cli.py`)

**Purpose**: Command-line interface using Typer framework

**Key Features**:

- Modern CLI with type hints and auto-completion
- Subcommands for different operations
- Help system and error handling
- Output format options (console, JSON)

**Commands**:

- `validate` - Validate n8n workflow JSON files
- `import-schema` - Import custom node schemas
- `list-schemas` - List available node schemas

#### 2. Validator Module (`validator.py`)

**Purpose**: Core validation logic for n8n workflows

**Key Features**:

- JSON structure validation
- Node-by-node schema validation
- Property type checking
- Required field validation
- Error aggregation and reporting

**Validation Rules**:

- Workflow structure validation
- Node property validation
- Type validation
- Required field checking

#### 3. Logger Module (`logger.py`)

**Purpose**: Logging and output formatting

**Key Features**:

- Configurable log levels (QUIET, NORMAL, VERBOSE, DEBUG)
- Rich console output with colors
- JSON output for automation
- Error aggregation and summary

**Output Formats**:

- Console output with Rich formatting
- JSON output for machine processing
- Structured error reporting

#### 4. Schema Module (`schemas/`)

**Purpose**: Node schema management

**Key Features**:

- JSON schema definitions for n8n nodes
- Schema registry management
- Custom schema import
- Validation rule application

**Schema Structure**:

- Individual JSON schema files
- Registry for schema management
- Type definitions and validation rules

### Design Patterns

#### 1. Hybrid Error System

**Pattern**: Flat storage with hierarchical grouping

**Implementation**:

- Flat list storage for performance
- Hierarchical grouping for display
- Severity-based categorization
- Context-rich error information

**Benefits**:

- Fast error processing
- Clear error organization
- Rich error context
- Easy error filtering

#### 2. Hybrid JSON Parsing

**Pattern**: Standard parsing with intelligent error recovery

**Implementation**:

- Standard JSON parsing for valid files
- Intelligent error recovery for malformed JSON
- Detailed error reporting with suggestions
- Graceful degradation

**Benefits**:

- Fast parsing for valid files
- Helpful error messages for invalid files
- Better user experience
- Reduced frustration

#### 3. Hybrid CLI Structure

**Pattern**: Direct validation with subcommands

**Implementation**:

- Direct validation command
- Subcommands for advanced features
- Consistent interface design
- Help system integration

**Benefits**:

- Simple primary use case
- Advanced features available
- Consistent user experience
- Easy to learn and use

#### 4. Hybrid Schema Management

**Pattern**: Directory storage with CLI-managed registry

**Implementation**:

- Directory-based schema storage
- CLI-managed registry
- Automatic schema discovery
- Custom schema import

**Benefits**:

- Easy schema management
- Automatic discovery
- Custom schema support
- Maintainable structure

### Error Handling Strategy

#### Error Types

1. **Validation Errors**: Node property validation failures
2. **JSON Errors**: Malformed JSON structure
3. **Schema Errors**: Missing or invalid schemas
4. **System Errors**: File I/O and system issues

#### Error Reporting

- **Console Output**: Rich formatted errors with context
- **JSON Output**: Structured error data for automation
- **Error Aggregation**: Summary of all errors found
- **Context Information**: Node type, property, line number

#### Error Recovery

- **Graceful Degradation**: Continue validation despite errors
- **Partial Results**: Return what can be validated
- **Clear Messages**: Actionable error descriptions
- **Suggestions**: Helpful hints for fixing errors

### Testing Strategy

#### Unit Testing

- **Coverage Target**: 60% minimum, 80% preferred
- **Test Categories**: CLI, validation, logging, schemas
- **Mocking**: External dependencies and file I/O
- **Fixtures**: Reusable test data and configurations

#### Integration Testing

- **End-to-End**: Complete workflow validation
- **Error Scenarios**: Various error conditions
- **Output Formats**: Console and JSON output
- **Performance**: Large file handling

#### Test Data

- **Valid Workflows**: Various n8n workflow examples
- **Invalid Workflows**: Common error scenarios
- **Edge Cases**: Boundary conditions and special cases
- **Custom Schemas**: User-defined node types

### Performance Considerations

#### Validation Performance

- **Streaming**: Large file handling
- **Caching**: Schema loading and validation
- **Optimization**: Efficient validation algorithms
- **Memory**: Minimal memory footprint

#### CLI Performance

- **Startup Time**: Fast command execution
- **Response Time**: Quick validation results
- **Memory Usage**: Efficient resource utilization
- **Error Handling**: Fast error detection and reporting

### Security Considerations

#### Input Validation

- **JSON Validation**: Secure JSON parsing
- **File Validation**: Safe file handling
- **Schema Validation**: Secure schema processing
- **Error Handling**: Safe error reporting

#### Output Security

- **Error Messages**: No sensitive information leakage
- **Logging**: Secure logging practices
- **File I/O**: Safe file operations
- **User Input**: Input sanitization

### Maintenance Strategy

#### Code Quality

- **Linting**: Automated code quality checks
- **Type Checking**: Static type analysis
- **Testing**: Comprehensive test coverage
- **Documentation**: Clear, up-to-date documentation

#### Dependency Management

- **Version Pinning**: Specific version requirements
- **Security Updates**: Regular dependency updates
- **Compatibility**: Python version compatibility
- **Build System**: Modern build and package management

#### Documentation

- **User Guide**: Clear usage instructions
- **API Documentation**: Code documentation
- **Examples**: Practical usage examples
- **Troubleshooting**: Common issues and solutions

### Future Considerations

#### Extensibility

- **Plugin System**: Custom validation rules
- **Schema Extensions**: Additional node types
- **Output Formats**: New output options
- **Integration**: IDE and CI/CD integration

#### Scalability

- **Large Files**: Streaming validation
- **Batch Processing**: Multiple file validation
- **Performance**: Optimization for large workflows
- **Memory**: Efficient memory usage

#### Community

- **Contributions**: Community-driven development
- **Feedback**: User feedback integration
- **Documentation**: Community documentation
- **Support**: Community support channels

### Conclusion

The n8n-lint project implements a clean, maintainable architecture focused on core validation functionality. The hybrid design patterns provide flexibility while maintaining simplicity, and the comprehensive testing strategy ensures reliability and quality.

The project demonstrates that a well-designed CLI tool can provide powerful functionality while remaining simple to use and maintain. The focus on core validation functionality ensures that the tool serves its primary purpose effectively while remaining extensible for future enhancements.
