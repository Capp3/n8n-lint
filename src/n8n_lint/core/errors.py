"""Error classes for n8n-lint."""

from typing import Any


class ValidationError:
    """Represents a validation error with full context."""

    def __init__(
        self,
        message: str,
        severity: str = "error",
        node_type: str | None = None,
        property_path: str | None = None,
        expected: str | None = None,
        actual: str | None = None,
        line_number: int | None = None,
        file_path: str | None = None,
    ):
        self.message = message
        self.severity = severity
        self.node_type = node_type
        self.property_path = property_path
        self.expected = expected
        self.actual = actual
        self.line_number = line_number
        self.file_path = file_path

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for JSON output."""
        return {
            "message": self.message,
            "severity": self.severity,
            "node_type": self.node_type,
            "property_path": self.property_path,
            "expected": self.expected,
            "actual": self.actual,
            "line_number": self.line_number,
            "file_path": self.file_path,
        }

    def to_console_text(self) -> str:
        """Convert error to console text for display."""
        severity_symbol = {
            "error": "❌ ERROR:",
            "warning": "⚠️  WARNING:",
            "info": "i  INFO:",
        }.get(self.severity, f"🔍 {self.severity.upper()}:")

        message = f"{severity_symbol} {self.message}"

        context_parts = []
        if self.node_type:
            context_parts.append(f"Node: {self.node_type}")
        if self.property_path:
            context_parts.append(f"Property: {self.property_path}")
        if self.line_number:
            context_parts.append(f"Line: {self.line_number}")
        if self.file_path:
            context_parts.append(f"File: {self.file_path}")

        if context_parts:
            message += f" ({', '.join(context_parts)})"

        if self.expected and self.actual:
            message += f"\n  Expected: {self.expected}\n  Actual: {self.actual}"
        elif self.expected:
            message += f"\n  Expected: {self.expected}"
        elif self.actual:
            message += f"\n  Actual: {self.actual}"

        return message
