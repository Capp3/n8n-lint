"""Logging and output formatting for n8n-lint."""

import json
import logging
import sys
from enum import Enum

from rich.console import Console
from rich.logging import RichHandler

from ..formatters import ConsoleFormatter, HTMLFormatter, JSONFormatter, MarkdownFormatter
from ..formatters.base import OutputFormatter, ValidationSummary
from ..utils.progress import ProgressTracker
from .errors import ValidationError


class LogLevel(Enum):
    """Log level enumeration."""

    QUIET = 0
    NORMAL = 1
    VERBOSE = 2
    DEBUG = 3

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value


class OutputFormat(Enum):
    """Output format enumeration."""

    CONSOLE = "console"
    JSON = "json"


class N8nLogger:
    """Main logger class for n8n-lint with Rich formatting and JSON output."""

    def __init__(
        self,
        log_level: LogLevel = LogLevel.NORMAL,
        output_format: OutputFormat = OutputFormat.CONSOLE,
        plain_text: bool = False,
        show_progress: bool = True,
    ):
        self.log_level = log_level
        self.output_format = output_format
        self.plain_text = plain_text
        self.show_progress = show_progress
        self.errors: list[ValidationError] = []
        self.warnings: list[ValidationError] = []
        self.info_messages: list[ValidationError] = []
        self.formatters: dict[str, OutputFormatter] = {}

        # Setup console
        if plain_text:
            self.console = Console(force_terminal=False, no_color=True)
        else:
            self.console = Console()

        # Setup formatters
        self._setup_formatters()

        # Setup progress tracking
        self.progress_tracker = ProgressTracker(plain_text=plain_text, show_progress=show_progress)

        # Setup logging
        self._setup_logging()

    def _setup_formatters(self) -> None:
        """Setup output formatters."""
        self.formatters = {
            "console": ConsoleFormatter(plain_text=self.plain_text),
            "json": JSONFormatter(plain_text=self.plain_text),
        }

        # Add additional formatters if not plain text
        if not self.plain_text:
            self.formatters["html"] = HTMLFormatter(plain_text=self.plain_text)
            self.formatters["markdown"] = MarkdownFormatter(plain_text=self.plain_text)

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        # Clear existing handlers
        logging.getLogger().handlers.clear()

        # Set log level
        if self.log_level == LogLevel.QUIET:
            level = logging.CRITICAL
        elif self.log_level == LogLevel.NORMAL:
            level = logging.INFO
        elif self.log_level == LogLevel.VERBOSE:
            level = logging.DEBUG
        else:  # DEBUG
            level = logging.DEBUG

        # Setup handler
        if self.plain_text:
            handler: logging.Handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        else:
            handler = RichHandler(console=self.console, show_time=False, show_path=False, markup=True)

        # Configure root logger
        logging.basicConfig(level=level, handlers=[handler], format="%(message)s")

        self.logger = logging.getLogger("n8n_lint")

    def log_error(self, message: str, **kwargs) -> None:
        """Log an error message."""
        error = ValidationError(message, severity="error", **kwargs)
        self.errors.append(error)

        # Always print errors, even in quiet mode
        if self.output_format == OutputFormat.JSON:
            self._log_json(error)
        else:
            self.console.print(error.to_console_text())

    def log_warning(self, message: str, **kwargs) -> None:
        """Log a warning message."""
        warning = ValidationError(message, severity="warning", **kwargs)
        self.warnings.append(warning)

        if self.log_level >= LogLevel.NORMAL:
            if self.output_format == OutputFormat.JSON:
                self._log_json(warning)
            else:
                self.console.print(warning.to_console_text())

    def log_info(self, message: str, **kwargs) -> None:
        """Log an info message."""
        info = ValidationError(message, severity="info", **kwargs)
        self.info_messages.append(info)

        if self.log_level >= LogLevel.VERBOSE:
            if self.output_format == OutputFormat.JSON:
                self._log_json(info)
            else:
                self.console.print(info.to_console_text())

    def log_debug(self, message: str) -> None:
        """Log a debug message."""
        if self.log_level >= LogLevel.DEBUG:
            self.logger.debug(message)

    def _log_json(self, error: ValidationError) -> None:
        """Log error in JSON format."""
        json_output = {
            "timestamp": self._get_timestamp(),
            "level": error.severity.upper(),
            "message": error.message,
            "context": {
                "node_type": error.node_type,
                "property_path": error.property_path,
                "expected": error.expected,
                "actual": error.actual,
                "line_number": error.line_number,
                "file_path": error.file_path,
            },
        }
        self.console.print(json.dumps(json_output))

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now().isoformat()

    def print_summary(self, file_path: str = "", total_nodes: int = 0) -> None:
        """Print validation summary using enhanced formatters."""
        total_errors = len(self.errors)
        total_warnings = len(self.warnings)
        total_info = len(self.info_messages)

        # In quiet mode, only print summary if there are errors
        if self.log_level == LogLevel.QUIET and total_errors == 0:
            return

        # Create validation summary
        summary = ValidationSummary(
            total_errors=total_errors,
            total_warnings=total_warnings,
            total_info=total_info,
            total_nodes=total_nodes,
            validation_time=self.progress_tracker.get_elapsed_time(),
            file_path=file_path,
        )

        # Get all messages
        all_messages = self.get_all_messages()

        # Use appropriate formatter
        if self.output_format == OutputFormat.JSON:
            formatter = self.formatters["json"]
            output = formatter.format_validation_result(all_messages, summary)
            # Use print() directly for JSON to avoid Rich formatting
            print(output)
        elif self.output_format == OutputFormat.CONSOLE:
            formatter = self.formatters["console"]
            # Use render method for proper Rich object display
            if hasattr(formatter, "render_validation_result"):
                formatter.render_validation_result(all_messages, summary)
            else:
                output = formatter.format_validation_result(all_messages, summary)
                self.console.print(output)
        else:
            # For other formats, use console formatter as fallback
            formatter = self.formatters["console"]
            if hasattr(formatter, "render_validation_result"):
                formatter.render_validation_result(all_messages, summary)
            else:
                output = formatter.format_validation_result(all_messages, summary)
                self.console.print(output)

    def get_exit_code(self) -> int:
        """Get appropriate exit code based on validation results."""
        if len(self.errors) > 0:
            return 1  # Errors
        elif len(self.warnings) > 0:
            return 2  # Warnings
        elif len(self.info_messages) > 0:
            return 3  # Info only
        else:
            return 0  # Success

    def get_all_messages(self) -> list[ValidationError]:
        """Get all validation messages."""
        return self.errors + self.warnings + self.info_messages

    def start_validation(self, total_nodes: int, file_path: str = "") -> None:
        """Start validation progress tracking."""
        self.progress_tracker.start_validation(total_nodes, file_path)

    def update_progress(self, node_name: str, node_type: str = "") -> None:
        """Update validation progress."""
        self.progress_tracker.update_progress(node_name, node_type)

    def complete_validation(self) -> None:
        """Complete validation progress tracking."""
        self.progress_tracker.complete_validation()

    def export_report(self, format_type: str, file_path: str = "") -> str:
        """Export validation report in specified format."""
        if format_type not in self.formatters:
            raise ValueError("Unsupported format: " + format_type)

        formatter = self.formatters[format_type]
        all_messages = self.get_all_messages()

        summary = ValidationSummary(
            total_errors=len(self.errors),
            total_warnings=len(self.warnings),
            total_info=len(self.info_messages),
            validation_time=self.progress_tracker.get_elapsed_time(),
            file_path=file_path,
        )

        return formatter.format_validation_result(all_messages, summary)


# Global logger instance
logger = N8nLogger()
