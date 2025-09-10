# Usage Guide

This guide provides comprehensive examples and usage patterns for the n8n JSON Linter.

## Basic Usage

### Validating a Workflow

The most common use case is validating an n8n workflow file:

```bash
# Basic validation
n8n-lint validate my-workflow.json

# With verbose output
n8n-lint validate my-workflow.json --verbose

# Quiet mode (errors only)
n8n-lint validate my-workflow.json --quiet
```

### Output Formats

#### Console Output (Default)

```bash
n8n-lint validate workflow.json
```

Produces human-readable output with color-coded messages:

```
ERROR: Required property 'parameters' is missing (Node: n8n-nodes-base.function)
(Property: parameters) (Line: 1)

WARNING: Unknown property 'unknownField' (Node: n8n-nodes-base.function)
(Property: unknownField) (Line: 1)

╭───────────────────────────── Validation Summary ─────────────────────────────╮
│ Validation complete: 1 errors, 1 warnings, 0 info messages                 │
╰──────────────────────────────────────────────────────────────────────────────╯
```

#### JSON Output

```bash
n8n-lint validate workflow.json --output json
```

Produces machine-readable JSON output:

```json
{"level": "ERROR", "message": "Required property 'parameters' is missing", "context": {"node_type": "n8n-nodes-base.function", "property_path": "parameters", "line_number": 1}}
{"level": "WARNING", "message": "Unknown property 'unknownField'", "context": {"node_type": "n8n-nodes-base.function", "property_path": "unknownField", "line_number": 1}}
{"summary": {"errors": 1, "warnings": 1, "info": 0, "total": 2}}
```

## Verbosity Levels

### Quiet Mode (`--quiet`)

Only shows errors:

```bash
n8n-lint validate workflow.json --quiet
```

### Normal Mode (Default)

Shows errors and warnings:

```bash
n8n-lint validate workflow.json
```

### Verbose Mode (`--verbose`)

Shows errors, warnings, and additional information:

```bash
n8n-lint validate workflow.json --verbose
```

### Debug Mode (`--debug`)

Shows all information including debug details:

```bash
n8n-lint validate workflow.json --debug
```

## Schema Management

### Listing Available Schemas

```bash
n8n-lint list-schemas
```

Output:

```
Available node schemas:
  • n8n-nodes-base.function: Function Node Schema
  • n8n-nodes-base.httpRequest: HTTP Request Node Schema
  • n8n-nodes-base.set: Set Node Schema
  • n8n-nodes-base.if: IF Node Schema
  • n8n-nodes-base.switch: Switch Node Schema
```

### Importing Custom Schemas

```bash
n8n-lint import-schema custom-node.json --node-type my-custom-node
```

Example custom schema file (`custom-node.json`):

```json
{
  "type": "object",
  "title": "Custom Node Schema",
  "description": "Schema for custom node validation",
  "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
  "properties": {
    "id": { "type": "string", "description": "Unique identifier for the node" },
    "name": { "type": "string", "description": "Display name of the node" },
    "type": {
      "type": "string",
      "enum": ["my-custom-node"],
      "description": "Node type identifier"
    },
    "typeVersion": {
      "type": "number",
      "description": "Version of the node type"
    },
    "position": {
      "type": "array",
      "items": { "type": "number" },
      "minItems": 2,
      "maxItems": 2,
      "description": "Position coordinates [x, y]"
    },
    "parameters": {
      "type": "object",
      "required": ["customParam"],
      "properties": {
        "customParam": { "type": "string", "description": "Custom parameter" }
      }
    }
  }
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Validate n8n Workflows

on:
  push:
    paths:
      - "workflows/**/*.json"
  pull_request:
    paths:
      - "workflows/**/*.json"

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - name: Install uv
        uses: astral-sh/setup-uv@v1
      - name: Validate workflows
        run: |
          uvx n8n-lint validate workflows/ --output json
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: n8n-lint
        name: n8n-lint
        entry: uvx n8n-lint validate
        language: system
        files: \.json$
        args: [--quiet]
```

### Shell Script

```bash
#!/bin/bash
# validate-workflows.sh

set -e

echo "Validating n8n workflows..."

# Find all JSON files in workflows directory
find workflows/ -name "*.json" -type f | while read -r file; do
    echo "Validating: $file"
    uvx n8n-lint validate "$file" --quiet
done

echo "All workflows validated successfully!"
```

## Exit Codes

The tool uses standard exit codes for automation:

- `0` - Success (no issues found)
- `1` - Errors found
- `2` - Warnings found (no errors)
- `3` - Info messages only (no errors or warnings)

Example usage in scripts:

```bash
#!/bin/bash

if n8n-lint validate workflow.json --quiet; then
    echo "Workflow is valid"
else
    echo "Workflow has issues"
    exit 1
fi
```

## Error Types

### Errors (Exit Code 1)

Critical issues that prevent the workflow from functioning:

- Missing required properties
- Invalid property types
- Malformed JSON structure

### Warnings (Exit Code 2)

Non-critical issues that may cause problems:

- Unknown properties
- Deprecated properties
- Potential configuration issues

### Info (Exit Code 3)

Informational messages:

- Best practice suggestions
- Performance recommendations
- Additional context

## Examples

### Valid Workflow

```bash
n8n-lint validate examples/sample_workflow.json
```

Output:

```
╭───────────────────────────── Validation Summary ─────────────────────────────╮
│ Validation complete: No issues found                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### Workflow with Issues

```bash
n8n-lint validate examples/workflow_with_errors.json
```

Output:

```
ERROR: Required property 'parameters' is missing (Node: n8n-nodes-base.function)
(Property: parameters) (Line: 1)

ERROR: Property 'method' has wrong type (Node: n8n-nodes-base.httpRequest)
(Property: method) (Expected: string, Actual: INVALID_METHOD) (Line: 2)

WARNING: Unknown property 'unknownProperty' (Node: n8n-nodes-base.httpRequest)
(Property: unknownProperty) (Line: 2)

╭───────────────────────────── Validation Summary ─────────────────────────────╮
│ Validation complete: 2 errors, 1 warnings, 0 info messages                 │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Troubleshooting

### Common Issues

1. **File Not Found**: Ensure the workflow file exists and the path is correct
2. **Invalid JSON**: Check that the file contains valid JSON syntax
3. **Schema Not Found**: Import custom schemas or check node type names
4. **Permission Errors**: Ensure read access to workflow files

### Getting Help

```bash
# Show help
n8n-lint --help

# Show command-specific help
n8n-lint validate --help
n8n-lint import-schema --help
n8n-lint list-schemas --help
```
