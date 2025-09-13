"""Console script for n8n_lint."""

from pathlib import Path

import typer
from rich.console import Console

from ..core.logger import LogLevel, OutputFormat
from ..core.validator import validate_workflow_file
from ..schemas import schema_manager

app = typer.Typer(name="n8n_lint", help="Validate n8n workflow JSON files", no_args_is_help=True)
console = Console()

# Typer argument/option constants to avoid B008 linting issues
FILE_PATH_ARG = typer.Argument(..., help="Path to the n8n workflow JSON file")
SCHEMA_FILE_ARG = typer.Argument(..., help="Path to the schema JSON file")
OUTPUT_FILE_OPT = typer.Option(..., "--output", "-o", help="Output file path for the report")


def _exit_success() -> None:
    """Exit with success code."""
    raise typer.Exit(0)


def _exit_error() -> None:
    """Exit with error code."""
    raise typer.Exit(1)


def _exit_with_code(code: int) -> None:
    """Exit with specified code."""
    raise typer.Exit(code)


def version_callback(value: bool):
    """Show version information."""
    if value:
        console.print("n8n-lint version 1.1.1")
        raise typer.Exit()


@app.callback()
def main(
    version: bool | None = typer.Option(
        None, "--version", "-v", callback=version_callback, help="Show version and exit"
    ),
):
    """N8n JSON Linter - Validate n8n workflow files."""
    pass


@app.command()
def validate(
    file_path: Path = FILE_PATH_ARG,
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Quiet mode - only show errors"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose mode - show detailed information"),
    debug: bool = typer.Option(False, "--debug", "-vv", help="Debug mode - show all information"),
    output: str = typer.Option("console", "--output", "-o", help="Output format: console, json, html, or markdown"),
    plain_text: bool = typer.Option(False, "--plain-text", help="Use plain text output instead of Rich formatting"),
):
    """Validate an n8n workflow JSON file."""

    # Determine log level
    if debug:
        log_level = LogLevel.DEBUG
    elif verbose:
        log_level = LogLevel.VERBOSE
    elif quiet:
        log_level = LogLevel.QUIET
    else:
        log_level = LogLevel.NORMAL

    # Determine output format
    output_lower = output.lower()
    if output_lower == "json":
        output_format = OutputFormat.JSON
    elif output_lower in ["html", "markdown"]:
        output_format = OutputFormat.CONSOLE  # Use console formatter for now
    else:
        output_format = OutputFormat.CONSOLE

    # Validate the workflow file
    exit_code = validate_workflow_file(
        file_path=file_path, log_level=log_level, output_format=output_format, plain_text=plain_text
    )

    # Exit with appropriate code
    raise typer.Exit(exit_code)


@app.command()
def import_schema(
    schema_file: Path = SCHEMA_FILE_ARG,
    node_type: str = typer.Option(
        ..., "--node-type", "-t", help="Node type identifier (e.g., 'n8n-nodes-base.function')"
    ),
):
    """Import a new node schema for validation."""

    try:
        import json

        # Load the schema file
        with open(schema_file) as f:
            schema_data = json.load(f)

        # Import the schema
        success = schema_manager.import_schema(node_type, schema_data)

        if success:
            console.print(f"✅ Successfully imported schema for node type: {node_type}")
            _exit_success()
        else:
            console.print(f"❌ Failed to import schema for node type: {node_type}")
            _exit_error()

    except json.JSONDecodeError as e:
        console.print(f"❌ Invalid JSON in schema file: {e}")
        raise typer.Exit(1) from e
    except typer.Exit:
        # Re-raise typer.Exit to allow proper exit handling
        raise
    except Exception as e:
        console.print(f"❌ Error importing schema: {e}")
        raise typer.Exit(1) from e


@app.command()
def list_schemas():
    """List all available node schemas."""

    node_types = schema_manager.list_node_types()

    if not node_types:
        console.print("No schemas available.")
        return

    console.print("Available node schemas:")
    for node_type in sorted(node_types):
        registry_entry = schema_manager.get_registry_entry(node_type)
        if registry_entry:
            description = registry_entry.get("description", "No description")
            console.print(f"  • {node_type}: {description}")
        else:
            console.print(f"  • {node_type}")


@app.command()
def export_report(
    file_path: Path = FILE_PATH_ARG,
    output_file: Path = OUTPUT_FILE_OPT,
    format_type: str = typer.Option("html", "--format", "-f", help="Report format: html or markdown"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Quiet mode - only show errors"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose mode - show detailed information"),
    debug: bool = typer.Option(False, "--debug", "-vv", help="Debug mode - show all information"),
):
    """Export validation report in HTML or Markdown format."""

    # Determine log level
    if debug:
        log_level = LogLevel.DEBUG
    elif verbose:
        log_level = LogLevel.VERBOSE
    elif quiet:
        log_level = LogLevel.QUIET
    else:
        log_level = LogLevel.NORMAL

    # Validate the workflow file and get results
    from ..core.logger import N8nLogger
    from ..core.validator import validate_workflow_file

    # Create logger for validation
    logger = N8nLogger(log_level=log_level, output_format=OutputFormat.CONSOLE, plain_text=False, show_progress=True)

    # Validate workflow
    exit_code = validate_workflow_file(
        file_path=file_path, log_level=log_level, output_format=OutputFormat.CONSOLE, plain_text=False, logger=logger
    )

    # Export report
    try:
        report_content = logger.export_report(format_type, str(file_path))

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_content)

        console.print(f"✅ Report exported to: {output_file}")

        # Exit with validation result code
        if exit_code == 0:
            _exit_success()
        else:
            _exit_with_code(exit_code)

    except typer.Exit:
        # Re-raise typer.Exit to allow proper exit handling
        raise
    except Exception as e:
        console.print(f"❌ Error exporting report: {e}")
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
