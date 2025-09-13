"""Console formatter with enhanced Rich formatting."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..core.errors import ValidationError
from .base import OutputFormatter, ValidationSummary


class ConsoleFormatter(OutputFormatter):
    """Enhanced console formatter with Rich formatting and Gruvbox colors."""

    def __init__(self, plain_text: bool = False):
        super().__init__(plain_text)
        self.console = Console(force_terminal=False, no_color=plain_text)

        # Gruvbox color scheme
        self.colors = {
            "error": "#fb4934",  # Red
            "warning": "#fabd2f",  # Yellow
            "info": "#83a598",  # Blue
            "success": "#b8bb26",  # Green
            "header": "#d3869b",  # Purple
            "context": "#928374",  # Gray
            "dim": "#665c54",  # Dark gray
        }

    def format_error(self, error: ValidationError) -> str:
        """Format a single validation error with enhanced styling."""
        if self.plain_text:
            return self._format_error_plain(error)

        text = Text()
        self._add_severity_indicator(text, error)
        self._add_error_message(text, error)
        self._add_error_context(text, error)
        self._add_error_details(text, error)

        return str(text)

    def _add_severity_indicator(self, text: Text, error: ValidationError) -> None:
        """Add severity indicator to text."""
        if error.severity == "error":
            text.append("❌ ERROR: ", style=f"bold {self.colors['error']}")
        elif error.severity == "warning":
            text.append("⚠️  WARNING: ", style=f"bold {self.colors['warning']}")
        elif error.severity == "info":
            text.append("i  INFO: ", style=f"bold {self.colors['info']}")
        else:
            text.append(f"🔍 {error.severity.upper()}: ", style="bold")

    def _add_error_message(self, text: Text, error: ValidationError) -> None:
        """Add error message to text."""
        text.append(error.message, style="bold")

    def _add_error_context(self, text: Text, error: ValidationError) -> None:
        """Add error context to text."""
        context_parts = []
        if error.node_type:
            context_parts.append(f"Node: {error.node_type}")
        if error.property_path:
            context_parts.append(f"Property: {error.property_path}")
        if error.line_number:
            context_parts.append(f"Line: {error.line_number}")
        if error.file_path:
            context_parts.append(f"File: {error.file_path}")

        if context_parts:
            text.append(f" ({', '.join(context_parts)})", style=f"dim {self.colors['context']}")

    def _add_error_details(self, text: Text, error: ValidationError) -> None:
        """Add expected/actual details to text."""
        if error.expected and error.actual:
            text.append(f"\n  Expected: {error.expected}", style=f"dim {self.colors['context']}")
            text.append(f"\n  Actual: {error.actual}", style=f"dim {self.colors['context']}")
        elif error.expected:
            text.append(f"\n  Expected: {error.expected}", style=f"dim {self.colors['context']}")
        elif error.actual:
            text.append(f"\n  Actual: {error.actual}", style=f"dim {self.colors['context']}")

    def _format_error_plain(self, error: ValidationError) -> str:
        """Format error in plain text mode."""
        severity_symbol = {
            "error": "ERROR:",
            "warning": "WARNING:",
            "info": "INFO:",
        }.get(error.severity, f"{error.severity.upper()}:")

        message = f"{severity_symbol} {error.message}"

        context_parts = []
        if error.node_type:
            context_parts.append(f"Node: {error.node_type}")
        if error.property_path:
            context_parts.append(f"Property: {error.property_path}")
        if error.line_number:
            context_parts.append(f"Line: {error.line_number}")
        if error.file_path:
            context_parts.append(f"File: {error.file_path}")

        if context_parts:
            message += f" ({', '.join(context_parts)})"

        if error.expected and error.actual:
            message += f"\n  Expected: {error.expected}\n  Actual: {error.actual}"
        elif error.expected:
            message += f"\n  Expected: {error.expected}"
        elif error.actual:
            message += f"\n  Actual: {error.actual}"

        return message

    def format_errors(self, errors: list[ValidationError]) -> str:
        """Format a list of validation errors with grouping."""
        if not errors:
            return ""

        if self.plain_text:
            return "\n".join(self._format_error_plain(error) for error in errors)

        # Group errors by severity
        error_groups: dict[str, list[ValidationError]] = {"error": [], "warning": [], "info": []}
        for error in errors:
            if error.severity in error_groups:
                error_groups[error.severity].append(error)

        formatted_errors = []

        for _severity, group_errors in error_groups.items():
            if not group_errors:
                continue

            # Add each error individually
            for error in group_errors:
                formatted_errors.append(self.format_error(error))

        return "\n\n".join(formatted_errors)

    def format_summary(self, summary: ValidationSummary) -> str:
        """Format a validation summary with enhanced styling."""
        if self.plain_text:
            return self._format_summary_plain(summary)

        border_style, status_icon = self._get_summary_style(summary)
        summary_text = self._build_summary_text(summary)

        panel = Panel(
            summary_text, title=f"{status_icon} Validation Summary", border_style=border_style, padding=(1, 2)
        )

        # Use console to render the panel to string
        from io import StringIO

        from rich.console import Console

        string_io = StringIO()
        temp_console = Console(file=string_io, force_terminal=False, width=80)
        temp_console.print(panel)
        return string_io.getvalue().strip()

    def _get_summary_style(self, summary: ValidationSummary) -> tuple[str, str]:
        """Get border style and status icon based on summary results."""
        if summary.has_errors:
            return self.colors["error"], "❌"
        elif summary.has_warnings:
            return self.colors["warning"], "⚠️"
        elif summary.has_info:
            return self.colors["info"], "i"
        else:
            return self.colors["success"], "✅"

    def _build_summary_text(self, summary: ValidationSummary) -> str:
        """Build the summary text with counts and timing."""
        summary_parts = []
        if summary.total_errors > 0:
            summary_parts.append(f"{summary.total_errors} error{'s' if summary.total_errors != 1 else ''}")
        if summary.total_warnings > 0:
            summary_parts.append(f"{summary.total_warnings} warning{'s' if summary.total_warnings != 1 else ''}")
        if summary.total_info > 0:
            summary_parts.append(f"{summary.total_info} info message{'s' if summary.total_info != 1 else ''}")

        if summary_parts:
            summary_text = f"Validation complete: {', '.join(summary_parts)}"
        else:
            summary_text = "Validation complete: No issues found"

        # Add timing information
        if summary.validation_time > 0:
            summary_text += f" (took {summary.validation_time:.2f}s)"

        # Add node count
        if summary.total_nodes > 0:
            summary_text += f" - {summary.total_nodes} node{'s' if summary.total_nodes != 1 else ''} validated"

        return summary_text

    def _format_summary_plain(self, summary: ValidationSummary) -> str:
        """Format summary in plain text mode."""
        summary_parts = []
        if summary.total_errors > 0:
            summary_parts.append(f"{summary.total_errors} error{'s' if summary.total_errors != 1 else ''}")
        if summary.total_warnings > 0:
            summary_parts.append(f"{summary.total_warnings} warning{'s' if summary.total_warnings != 1 else ''}")
        if summary.total_info > 0:
            summary_parts.append(f"{summary.total_info} info message{'s' if summary.total_info != 1 else ''}")

        if summary_parts:
            summary_text = f"Validation complete: {', '.join(summary_parts)}"
        else:
            summary_text = "Validation complete: No issues found"

        if summary.validation_time > 0:
            summary_text += f" (took {summary.validation_time:.2f}s)"

        if summary.total_nodes > 0:
            summary_text += f" - {summary.total_nodes} node{'s' if summary.total_nodes != 1 else ''} validated"

        return summary_text

    def format_validation_result(self, errors: list[ValidationError], summary: ValidationSummary) -> str:
        """Format complete validation result."""
        result_parts = []

        # Add errors if any
        if errors:
            result_parts.append(self.format_errors(errors))

        # Add summary - convert Panel to string for text output
        summary_panel = self.format_summary(summary)
        if hasattr(summary_panel, "__rich__"):
            # It's a Rich object, convert to string
            from io import StringIO

            from rich.console import Console

            string_io = StringIO()
            console = Console(file=string_io, force_terminal=False)
            console.print(summary_panel)
            summary_text = string_io.getvalue()
        else:
            summary_text = str(summary_panel)

        result_parts.append(summary_text)

        return "\n\n".join(result_parts)

    def render_validation_result(self, errors: list[ValidationError], summary: ValidationSummary) -> None:
        """Render complete validation result directly to console."""
        # Add errors if any
        if errors:
            self.console.print(self.format_errors(errors))

        # Add summary - format_summary returns a Rich Panel object
        summary_panel = self.format_summary(summary)
        self.console.print(summary_panel)

    def format_progress(self, current: int, total: int, message: str = "") -> str:
        """Format progress information with Rich progress bar."""
        if total == 0:
            return ""

        if self.plain_text:
            return super().format_progress(current, total, message)

        # Create a simple progress display
        percentage = (current / total) * 100
        bar_length = 20
        filled_length = int(bar_length * current // total)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)

        progress_text = f"[{bar}] {percentage:.1f}% ({current}/{total})"
        if message:
            progress_text = f"{message} {progress_text}"

        return progress_text
