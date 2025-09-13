# CLI Reference

Complete reference for all n8n-lint command-line interface commands and options.

## Global Options

These options are available for all commands:

| Option      | Short | Description                |
| ----------- | ----- | -------------------------- |
| `--version` | `-v`  | Show version and exit      |
| `--help`    | `-h`  | Show help message and exit |

## Commands

### validate

Validate an n8n workflow JSON file.

```bash
n8n-lint validate [OPTIONS] FILE_PATH
```

**Arguments:**

- `FILE_PATH` - Path to the n8n workflow JSON file

**Options:**
| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--quiet` | `-q` | `False` | Quiet mode - only show errors |
| `--verbose` | `-v` | `False` | Verbose mode - show detailed information |
| `--debug` | `-vv` | `False` | Debug mode - show all information |
| `--output` | `-o` | `console` | Output format: console, json, html, or markdown |
| `--plain-text` | | `False` | Use plain text output instead of Rich formatting |

**Examples:**

```bash
# Basic validation
n8n-lint validate workflow.json

# JSON output for automation
n8n-lint validate workflow.json --output json

# Quiet mode
n8n-lint validate workflow.json --quiet

# Verbose mode
n8n-lint validate workflow.json --verbose
```

### import-schema

Import a new node schema for validation.

```bash
n8n-lint import-schema [OPTIONS] SCHEMA_FILE
```

**Arguments:**

- `SCHEMA_FILE` - Path to the schema JSON file

**Options:**
| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--node-type` | `-t` | `Yes` | Node type identifier (e.g., 'n8n-nodes-base.function') |

**Examples:**

```bash
# Import custom schema
n8n-lint import-schema custom-schema.json --node-type my.custom.node

# Import official node schema
n8n-lint import-schema http-request-schema.json --node-type n8n-nodes-base.httpRequest
```

### list-schemas

List all available node schemas.

```bash
n8n-lint list-schemas
```

**Examples:**

```bash
# List all schemas
n8n-lint list-schemas

# Output example:
# Available node schemas:
#   • n8n-nodes-base.function: Execute JavaScript code
#   • n8n-nodes-base.httpRequest: Make HTTP requests
#   • n8n-nodes-base.set: Set data values
```

### export-report

Export validation report in HTML or Markdown format.

```bash
n8n-lint export-report [OPTIONS] FILE_PATH OUTPUT_FILE
```

**Arguments:**

- `FILE_PATH` - Path to the n8n workflow JSON file
- `OUTPUT_FILE` - Output file path for the report

**Options:**
| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--format` | `-f` | `html` | Report format: html or markdown |
| `--quiet` | `-q` | `False` | Quiet mode - only show errors |
| `--verbose` | `-v` | `False` | Verbose mode - show detailed information |
| `--debug` | `-vv` | `False` | Debug mode - show all information |

**Examples:**

```bash
# Export HTML report
n8n-lint export-report workflow.json report.html --format html

# Export Markdown report
n8n-lint export-report workflow.json report.md --format markdown

# Export with verbose output
n8n-lint export-report workflow.json report.html --verbose
```

## Exit Codes

n8n-lint uses the following exit codes:

| Code | Meaning                             |
| ---- | ----------------------------------- |
| `0`  | Success - no validation errors      |
| `1`  | Validation errors found             |
| `2`  | Invalid arguments or file not found |

## Environment Variables

| Variable                 | Description               | Default   |
| ------------------------ | ------------------------- | --------- |
| `N8N_LINT_LOG_LEVEL`     | Set default log level     | `normal`  |
| `N8N_LINT_OUTPUT_FORMAT` | Set default output format | `console` |

## Configuration Files

n8n-lint supports configuration files for default settings:

### .n8nlintrc

Create a `.n8nlintrc` file in your project root:

```json
{
  "default_output_format": "json",
  "default_log_level": "quiet",
  "custom_schemas": {
    "my.custom.node": "./schemas/my-custom-schema.json"
  }
}
```

## Shell Completion

n8n-lint supports shell completion for Bash, Zsh, and Fish:

```bash
# Install completion for current shell
n8n-lint --install-completion

# Show completion script
n8n-lint --show-completion
```

## Examples

### Basic Validation

```bash
n8n-lint validate workflow.json
```

### CI/CD Pipeline

```bash
n8n-lint validate workflow.json --output json --quiet
```

### Development Workflow

```bash
n8n-lint validate workflow.json --verbose
n8n-lint export-report workflow.json report.html --format html
```

### Custom Schema Workflow

```bash
n8n-lint import-schema my-schema.json --node-type my.custom.node
n8n-lint validate workflow-with-custom-nodes.json
```

## Related Documentation

- [Basic Usage Guide](../user-guide/basic-usage.md) - Getting started
- [Examples](../examples/sample_workflow.json) - Real-world examples
