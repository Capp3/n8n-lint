# API Reference

Complete API reference for n8n-lint Python package.

## Installation

```python
pip install n8n-lint
```

## Quick Start

```python
from n8n_lint import validate_workflow_file

# Validate a workflow file
exit_code = validate_workflow_file("workflow.json")
if exit_code == 0:
    print("Validation successful")
else:
    print("Validation failed")
```

## Core API

### validate_workflow_file

Validate an n8n workflow file.

```python
def validate_workflow_file(
    file_path: str | Path,
    log_level: LogLevel = LogLevel.NORMAL,
    output_format: OutputFormat = OutputFormat.CONSOLE,
    plain_text: bool = False,
    logger: N8nLogger | None = None
) -> int
```

**Parameters:**

- `file_path` - Path to the workflow JSON file
- `log_level` - Logging level (QUIET, NORMAL, VERBOSE, DEBUG)
- `output_format` - Output format (CONSOLE, JSON)
- `plain_text` - Use plain text instead of Rich formatting
- `logger` - Custom logger instance

**Returns:**

- `int` - Exit code (0 for success, 1 for errors)

**Example:**

```python
from n8n_lint import validate_workflow_file, LogLevel, OutputFormat

# Basic validation
exit_code = validate_workflow_file("workflow.json")

# With custom options
exit_code = validate_workflow_file(
    "workflow.json",
    log_level=LogLevel.VERBOSE,
    output_format=OutputFormat.JSON
)
```

## Core Classes

### LogLevel

Logging level enumeration.

```python
class LogLevel(Enum):
    QUIET = 0      # Only errors
    NORMAL = 1     # Errors and warnings
    VERBOSE = 2    # Detailed information
    DEBUG = 3      # All information
```

### OutputFormat

Output format enumeration.

```python
class OutputFormat(Enum):
    CONSOLE = "console"  # Rich console output
    JSON = "json"        # JSON output
```

### N8nLogger

Main logging and output class.

```python
class N8nLogger:
    def __init__(
        self,
        log_level: LogLevel = LogLevel.NORMAL,
        output_format: OutputFormat = OutputFormat.CONSOLE,
        plain_text: bool = False,
        show_progress: bool = True
    )

    def log_error(self, message: str, **kwargs) -> None
    def log_warning(self, message: str, **kwargs) -> None
    def log_info(self, message: str, **kwargs) -> None
    def log_debug(self, message: str, **kwargs) -> None

    def get_exit_code(self) -> int
    def get_all_messages(self) -> list[ValidationError]
    def export_report(self, format_type: str, file_path: str) -> str
```

**Example:**

```python
from n8n_lint import N8nLogger, LogLevel, OutputFormat

# Create logger
logger = N8nLogger(
    log_level=LogLevel.VERBOSE,
    output_format=OutputFormat.JSON
)

# Log messages
logger.log_error("Required property missing")
logger.log_warning("Deprecated property used")

# Get results
exit_code = logger.get_exit_code()
messages = logger.get_all_messages()
```

### ValidationError

Represents a validation error.

```python
class ValidationError:
    def __init__(
        self,
        message: str,
        severity: str = "error",
        node_type: str | None = None,
        property_path: str | None = None,
        line_number: int | None = None,
        file_path: str | None = None
    )

    def to_dict(self) -> dict[str, Any]
    def to_console_text(self) -> str
```

**Example:**

```python
from n8n_lint import ValidationError

# Create validation error
error = ValidationError(
    message="Required property 'typeVersion' is missing",
    severity="error",
    node_type="n8n-nodes-base.function",
    property_path="typeVersion"
)

# Convert to dictionary
error_dict = error.to_dict()
```

## Schema Management

### schema_manager

Global schema manager instance.

```python
from n8n_lint import schema_manager

# Get schema for node type
schema = schema_manager.get_schema("n8n-nodes-base.function")

# List all node types
node_types = schema_manager.list_node_types()

# Import custom schema
success = schema_manager.import_schema(
    "my.custom.node",
    schema_data
)
```

## Formatters

### OutputFormatter

Base class for output formatters.

```python
class OutputFormatter(ABC):
    @abstractmethod
    def format_errors(self, errors: list[ValidationError]) -> str
    @abstractmethod
    def format_summary(self, summary: ValidationSummary) -> str
```

### Available Formatters

- `ConsoleFormatter` - Rich console output
- `JSONFormatter` - JSON output
- `HTMLFormatter` - HTML output
- `MarkdownFormatter` - Markdown output

**Example:**

```python
from n8n_lint import ConsoleFormatter, ValidationError

formatter = ConsoleFormatter()
errors = [ValidationError("Test error")]

# Format errors
formatted_output = formatter.format_errors(errors)
```

## Advanced Usage

### Custom Validation

```python
from n8n_lint import N8nLogger, ValidationError, LogLevel

# Create custom logger
logger = N8nLogger(log_level=LogLevel.DEBUG)

# Add custom validation logic
def custom_validate(workflow_data):
    errors = []

    # Custom validation rules
    if "customProperty" not in workflow_data:
        errors.append(ValidationError(
            "Custom property required",
            node_type="custom"
        ))

    return errors

# Use custom validation
workflow_errors = custom_validate(workflow_data)
for error in workflow_errors:
    logger.log_error(error.message)
```

### Integration with Other Tools

```python
import json
from n8n_lint import validate_workflow_file, N8nLogger

# Validate and process results
def validate_and_process(file_path):
    logger = N8nLogger(output_format=OutputFormat.JSON)

    # Validate workflow
    exit_code = validate_workflow_file(file_path, logger=logger)

    # Process results
    if exit_code == 0:
        return {"status": "valid", "errors": []}
    else:
        errors = logger.get_all_messages()
        return {
            "status": "invalid",
            "errors": [error.to_dict() for error in errors]
        }
```

## Error Handling

```python
from n8n_lint import validate_workflow_file
from pathlib import Path

try:
    exit_code = validate_workflow_file("workflow.json")
except FileNotFoundError:
    print("Workflow file not found")
except json.JSONDecodeError:
    print("Invalid JSON format")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Considerations

- Use `LogLevel.QUIET` for better performance
- Use `OutputFormat.JSON` for programmatic processing
- Consider using `plain_text=True` for faster output

## Related Documentation

- [User Guide](../user-guide/index.md) - User documentation
- [CLI Reference](../cli-reference/index.md) - Command-line interface
- [Developer Guide](../developer/index.md) - Development documentation
