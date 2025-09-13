# Basic Usage

This guide covers the essential commands and usage patterns for n8n-lint.

## Quick Start

The most common use case is validating an n8n workflow file:

```bash
n8n_lint validate workflow.json
```

## Core Commands

### validate - Validate Workflows

The primary command for validating n8n workflow files:

```bash
# Basic validation
n8n_lint validate workflow.json

# Quiet mode (errors only)
n8n_lint validate workflow.json --quiet

# Verbose mode (detailed information)
n8n_lint validate workflow.json --verbose

# Debug mode (all information)
n8n_lint validate workflow.json --debug
```

#### Output Formats

```bash
# Console output (default)
n8n_lint validate workflow.json

# JSON output for automation
n8n_lint validate workflow.json --output json

# Plain text output
n8n_lint validate workflow.json --plain-text
```

### import-schema - Import Custom Schemas

Add custom node schemas for validation:

```bash
n8n_lint import-schema custom-schema.json --node-type my.custom.node
```

### list-schemas - List Available Schemas

See all available node schemas:

```bash
n8n_lint list-schemas
```

### export-report - Export Reports

Generate detailed validation reports:

```bash
# HTML report
n8n_lint export-report workflow.json --output report.html --format html

# Markdown report
n8n_lint export-report workflow.json --output report.md --format markdown
```

## Common Usage Patterns

### CI/CD Integration

```bash
# In your CI pipeline
n8n_lint validate workflow.json --output json > validation-results.json

# Check exit code
if [ $? -eq 0 ]; then
    echo "Validation passed"
else
    echo "Validation failed"
    exit 1
fi
```

### Batch Validation

```bash
# Validate multiple workflows
for workflow in workflows/*.json; do
    echo "Validating $workflow"
    n8n_lint validate "$workflow"
done
```

### Development Workflow

```bash
# Watch mode with file monitoring
n8n_lint validate workflow.json --verbose

# Generate reports for documentation
n8n_lint export-report workflow.json --output docs/validation-report.html --format html
```

## Understanding Output

### Success Output

```bash
$ n8n_lint validate valid-workflow.json
✅ Validation complete: No issues found (took 0.02s) - 3 nodes validated
```

### Error Output

```bash
$ n8n_lint validate invalid-workflow.json
❌ ERROR: Required property 'typeVersion' is missing (Node: n8n-nodes-base.function)
❌ ERROR: Required property 'position' is missing (Node: n8n-nodes-base.function)

╭─────────────────────────── ❌ Validation Summary ────────────────────────────╮
│                                                                              │
│  Validation complete: 2 errors (took 0.00s) - 1 node validated               │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### JSON Output

```bash
$ n8n_lint validate workflow.json --output json
{
  "summary": {
    "total_nodes": 1,
    "errors": 2,
    "warnings": 0,
    "duration": 0.001
  },
  "errors": [
    {
      "message": "Required property 'typeVersion' is missing",
      "node_type": "n8n-nodes-base.function",
      "property_path": "typeVersion",
      "severity": "error"
    }
  ]
}
```

## Exit Codes

n8n-lint uses standard exit codes:

- `0` - Validation successful (no errors)
- `1` - Validation failed (errors found)
- `2` - Invalid arguments or file not found

## Performance Tips

### Large Workflows

```bash
# Use quiet mode for large workflows
n8n_lint validate large-workflow.json --quiet

# JSON output is faster for automation
n8n_lint validate workflow.json --output json
```

### Multiple Files

```bash
# Process files in parallel (if supported by your shell)
find . -name "*.json" -exec n8n_lint validate {} \;
```

## Best Practices

1. **Always validate before deployment**
2. **Use JSON output in CI/CD pipelines**
3. **Generate reports for documentation**
4. **Import custom schemas for your specific nodes**
5. **Use appropriate verbosity levels**

## Next Steps

- [Examples](../examples/sample_workflow.json) - See real-world usage examples
- [CLI Reference](../cli-reference/index.md) - Complete command documentation
