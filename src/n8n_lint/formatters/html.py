"""HTML formatter for n8n-lint output."""

from datetime import datetime

from ..core.errors import ValidationError
from .base import OutputFormatter, ValidationSummary


class HTMLFormatter(OutputFormatter):
    """HTML formatter for web-based output."""

    def __init__(self, plain_text: bool = False):
        super().__init__(plain_text)

    def format_error(self, error: ValidationError) -> str:
        """Format a single validation error as HTML."""
        severity_class = f"error-{error.severity}"

        html = f'<div class="validation-error {severity_class}">'
        html += '<div class="error-header">'
        html += f'<span class="severity-icon">{self._get_severity_icon(error.severity)}</span>'
        html += f'<span class="severity-text">{error.severity.upper()}</span>'
        html += "</div>"
        html += f'<div class="error-message">{self._escape_html(error.message)}</div>'

        # Add context information
        context_parts = []
        if error.node_type:
            context_parts.append(f"Node: {self._escape_html(error.node_type)}")
        if error.property_path:
            context_parts.append(f"Property: {self._escape_html(error.property_path)}")
        if error.line_number:
            context_parts.append(f"Line: {error.line_number}")
        if error.file_path:
            context_parts.append(f"File: {self._escape_html(error.file_path)}")

        if context_parts:
            html += f'<div class="error-context">{", ".join(context_parts)}</div>'

        # Add expected/actual values
        if error.expected and error.actual:
            html += '<div class="error-details">'
            html += f'<div class="expected">Expected: {self._escape_html(error.expected)}</div>'
            html += f'<div class="actual">Actual: {self._escape_html(error.actual)}</div>'
            html += "</div>"
        elif error.expected:
            html += '<div class="error-details">'
            html += f'<div class="expected">Expected: {self._escape_html(error.expected)}</div>'
            html += "</div>"
        elif error.actual:
            html += '<div class="error-details">'
            html += f'<div class="actual">Actual: {self._escape_html(error.actual)}</div>'
            html += "</div>"

        html += "</div>"
        return html

    def format_errors(self, errors: list[ValidationError]) -> str:
        """Format a list of validation errors as HTML."""
        if not errors:
            return ""

        html = '<div class="validation-errors">'
        for error in errors:
            html += self.format_error(error)
        html += "</div>"
        return html

    def format_summary(self, summary: ValidationSummary) -> str:
        """Format a validation summary as HTML."""
        summary_class, status_icon = self._get_summary_style(summary)

        html = f'<div class="validation-summary {summary_class}">'
        html += self._build_summary_header(status_icon)
        html += self._build_summary_text(summary)
        html += self._build_summary_info(summary)
        html += "</div>"

        return html

    def _get_summary_style(self, summary: ValidationSummary) -> tuple[str, str]:
        """Get summary class and status icon based on results."""
        if summary.has_errors:
            return "summary-error", "❌"
        elif summary.has_warnings:
            return "summary-warning", "⚠️"
        elif summary.has_info:
            return "summary-info", "i"
        else:
            return "summary-success", "✅"

    def _build_summary_header(self, status_icon: str) -> str:
        """Build the summary header HTML."""
        return (
            '<div class="summary-header">'
            f'<span class="status-icon">{status_icon}</span>'
            '<span class="summary-title">Validation Summary</span>'
            "</div>"
        )

    def _build_summary_text(self, summary: ValidationSummary) -> str:
        """Build the summary text HTML."""
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

        return f'<div class="summary-text">{summary_text}</div>'

    def _build_summary_info(self, summary: ValidationSummary) -> str:
        """Build the summary info HTML."""
        info_parts = []
        if summary.validation_time > 0:
            info_parts.append(f"Took {summary.validation_time:.2f}s")
        if summary.total_nodes > 0:
            info_parts.append(f"{summary.total_nodes} node{'s' if summary.total_nodes != 1 else ''} validated")

        if info_parts:
            return f'<div class="summary-info">{", ".join(info_parts)}</div>'
        return ""

    def format_validation_result(self, errors: list[ValidationError], summary: ValidationSummary) -> str:
        """Format complete validation result as HTML."""
        html = "<!DOCTYPE html>"
        html += '<html lang="en">'
        html += "<head>"
        html += '<meta charset="UTF-8">'
        html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        html += "<title>n8n-lint Validation Report</title>"
        html += f"<style>{self._get_css()}</style>"
        html += "</head>"
        html += "<body>"
        html += '<div class="container">'
        html += "<h1>n8n-lint Validation Report</h1>"
        html += '<div class="report-meta">'
        html += f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        if summary.file_path:
            html += f"<p>File: {self._escape_html(summary.file_path)}</p>"
        html += "</div>"

        # Add errors if any
        if errors:
            html += self.format_errors(errors)

        # Add summary
        html += self.format_summary(summary)

        html += "</div>"
        html += "</body>"
        html += "</html>"
        return html

    def _get_severity_icon(self, severity: str) -> str:
        """Get icon for severity level."""
        icons = {
            "error": "❌",
            "warning": "⚠️",
            "info": "i",
        }
        return icons.get(severity, "🔍")

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
        )

    def _get_css(self) -> str:
        """Get CSS styles for HTML output."""
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }

        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }

        .report-meta {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            color: #6c757d;
        }

        .validation-error {
            border-left: 4px solid #dc3545;
            background: #f8d7da;
            padding: 15px;
            margin: 10px 0;
            border-radius: 0 5px 5px 0;
        }

        .validation-error.error-warning {
            border-left-color: #ffc107;
            background: #fff3cd;
        }

        .validation-error.error-info {
            border-left-color: #17a2b8;
            background: #d1ecf1;
        }

        .error-header {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }

        .severity-icon {
            font-size: 18px;
            margin-right: 8px;
        }

        .severity-text {
            font-weight: bold;
            font-size: 14px;
            text-transform: uppercase;
        }

        .error-message {
            font-weight: 500;
            margin-bottom: 8px;
        }

        .error-context {
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 8px;
        }

        .error-details {
            background: rgba(0,0,0,0.05);
            padding: 10px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 14px;
        }

        .expected {
            color: #28a745;
            margin-bottom: 5px;
        }

        .actual {
            color: #dc3545;
        }

        .validation-summary {
            border-radius: 8px;
            padding: 20px;
            margin-top: 30px;
        }

        .summary-error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
        }

        .summary-warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
        }

        .summary-info {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
        }

        .summary-success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
        }

        .summary-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }

        .status-icon {
            font-size: 24px;
            margin-right: 10px;
        }

        .summary-title {
            font-size: 18px;
            font-weight: bold;
        }

        .summary-text {
            font-size: 16px;
            margin-bottom: 8px;
        }

        .summary-info {
            font-size: 14px;
            color: #6c757d;
        }
        """
