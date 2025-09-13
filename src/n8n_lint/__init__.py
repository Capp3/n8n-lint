"""Top-level package for n8n-lint."""

__author__ = """Dom Capparelli"""
__email__ = "web@Capparelli.ie"
__version__ = "1.1.1"

# Clean public API imports
from .core import LogLevel, N8nLogger, OutputFormat, ValidationError, validate_workflow_file
from .formatters import ConsoleFormatter, HTMLFormatter, JSONFormatter, MarkdownFormatter, OutputFormatter
from .schemas import schema_manager

__all__ = [
    # Formatters
    "ConsoleFormatter",
    "HTMLFormatter",
    "JSONFormatter",
    # Core functionality
    "LogLevel",
    "MarkdownFormatter",
    "N8nLogger",
    "OutputFormat",
    "OutputFormatter",
    "ValidationError",
    # Schema management
    "schema_manager",
    "validate_workflow_file",
]
