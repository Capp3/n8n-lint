"""Markdown formatter for n8n-lint output."""

from datetime import datetime

from ..core.errors import ValidationError
from .base import OutputFormatter, ValidationSummary


class MarkdownFormatter(OutputFormatter):
    """Markdown formatter for documentation-friendly output."""

    def __init__(self, plain_text: bool = False):
        super().__init__(plain_text)

    def format_error(self, error: ValidationError) -> str:
        """Format a single validation error as Markdown."""
        # Severity indicator
        severity_icon = {
            "error": "❌",
            "warning": "⚠️",
            "info": "i",
        }.get(error.severity, "🔍")

        markdown = f"### {severity_icon} {error.severity.upper()}: {error.message}\n"

        # Add context information
        context_parts = []
        if error.node_type:
            context_parts.append(f"**Node:** `{error.node_type}`")
        if error.property_path:
            context_parts.append(f"**Property:** `{error.property_path}`")
        if error.line_number:
            context_parts.append(f"**Line:** {error.line_number}")
        if error.file_path:
            context_parts.append(f"**File:** `{error.file_path}`")

        if context_parts:
            markdown += f"\n**Context:** {', '.join(context_parts)}\n"

        # Add expected/actual values
        if error.expected and error.actual:
            markdown += "\n**Details:**\n"
            markdown += f"- **Expected:** `{error.expected}`\n"
            markdown += f"- **Actual:** `{error.actual}`\n"
        elif error.expected:
            markdown += f"\n**Expected:** `{error.expected}`\n"
        elif error.actual:
            markdown += f"\n**Actual:** `{error.actual}`\n"

        return markdown

    def format_errors(self, errors: list[ValidationError]) -> str:
        """Format a list of validation errors as Markdown."""
        if not errors:
            return ""

        markdown = "# Validation Errors\n\n"
        error_groups = self._group_errors_by_severity(errors)

        for severity, group_errors in error_groups.items():
            if not group_errors:
                continue
            markdown += self._format_error_group(severity, group_errors)

        return markdown

    def _group_errors_by_severity(self, errors: list[ValidationError]) -> dict[str, list[ValidationError]]:
        """Group errors by severity."""
        error_groups: dict[str, list[ValidationError]] = {"error": [], "warning": [], "info": []}
        for error in errors:
            if error.severity in error_groups:
                error_groups[error.severity].append(error)
        return error_groups

    def _format_error_group(self, severity: str, group_errors: list[ValidationError]) -> str:
        """Format a group of errors with the same severity."""
        severity_title = {"error": "Errors", "warning": "Warnings", "info": "Info Messages"}[severity]
        markdown = f"## {severity_title} ({len(group_errors)})\n\n"

        for i, error in enumerate(group_errors, 1):
            markdown += f"### {i}. {error.message}\n"
            markdown += self._format_error_context(error)
            markdown += self._format_error_details(error)
            markdown += "\n---\n\n"

        return markdown

    def _format_error_context(self, error: ValidationError) -> str:
        """Format error context information."""
        context_parts = []
        if error.node_type:
            context_parts.append(f"**Node:** `{error.node_type}`")
        if error.property_path:
            context_parts.append(f"**Property:** `{error.property_path}`")
        if error.line_number:
            context_parts.append(f"**Line:** {error.line_number}")
        if error.file_path:
            context_parts.append(f"**File:** `{error.file_path}`")

        if context_parts:
            return f"\n**Context:** {', '.join(context_parts)}\n"
        return ""

    def _format_error_details(self, error: ValidationError) -> str:
        """Format error expected/actual details."""
        if error.expected and error.actual:
            return "\n**Details:**\n" + f"- **Expected:** `{error.expected}`\n" + f"- **Actual:** `{error.actual}`\n"
        elif error.expected:
            return f"\n**Expected:** `{error.expected}`\n"
        elif error.actual:
            return f"\n**Actual:** `{error.actual}`\n"
        return ""

    def format_summary(self, summary: ValidationSummary) -> str:
        """Format a validation summary as Markdown."""
        # Determine status
        if summary.has_errors:
            status_icon = "❌"
            status_text = "Failed"
        elif summary.has_warnings:
            status_icon = "⚠️"
            status_text = "Warning"
        elif summary.has_info:
            status_icon = "i"
            status_text = "Info"
        else:
            status_icon = "✅"
            status_text = "Success"

        markdown = f"# {status_icon} Validation Summary: {status_text}\n\n"

        # Create summary table
        markdown += "| Metric | Count |\n"
        markdown += "|--------|-------|\n"
        markdown += f"| Errors | {summary.total_errors} |\n"
        markdown += f"| Warnings | {summary.total_warnings} |\n"
        markdown += f"| Info Messages | {summary.total_info} |\n"
        markdown += f"| Total Messages | {summary.total_messages} |\n"
        markdown += f"| Nodes Validated | {summary.total_nodes} |\n"

        if summary.validation_time > 0:
            markdown += f"| Validation Time | {summary.validation_time:.2f}s |\n"

        markdown += "\n"

        # Add file information
        if summary.file_path:
            markdown += f"**File:** `{summary.file_path}`\n\n"

        # Add status message
        if summary.is_success:
            markdown += "🎉 **Validation completed successfully with no issues!**\n"
        elif summary.has_errors:
            markdown += f"❌ **Validation failed with {summary.total_errors} error{'s' if summary.total_errors != 1 else ''}.**\n"
        elif summary.has_warnings:
            markdown += f"⚠️ **Validation completed with {summary.total_warnings} warning{'s' if summary.total_warnings != 1 else ''}.**\n"
        else:
            markdown += f"i **Validation completed with {summary.total_info} info message{'s' if summary.total_info != 1 else ''}.**\n"

        return markdown

    def format_validation_result(self, errors: list[ValidationError], summary: ValidationSummary) -> str:
        """Format complete validation result as Markdown."""
        markdown = "# n8n-lint Validation Report\n\n"
        markdown += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        if summary.file_path:
            markdown += f"**File:** `{summary.file_path}`\n\n"

        # Add errors if any
        if errors:
            markdown += self.format_errors(errors)
            markdown += "\n"

        # Add summary
        markdown += self.format_summary(summary)

        return markdown
