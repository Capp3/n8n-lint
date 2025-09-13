"""Base formatter interface for n8n-lint output."""

from abc import ABC, abstractmethod

from ..core.errors import ValidationError


class ValidationSummary:
    """Represents a validation summary with statistics."""

    def __init__(
        self,
        total_errors: int = 0,
        total_warnings: int = 0,
        total_info: int = 0,
        total_nodes: int = 0,
        validation_time: float = 0.0,
        file_path: str = "",
    ):
        self.total_errors = total_errors
        self.total_warnings = total_warnings
        self.total_info = total_info
        self.total_nodes = total_nodes
        self.validation_time = validation_time
        self.file_path = file_path

    @property
    def total_messages(self) -> int:
        """Total number of validation messages."""
        return self.total_errors + self.total_warnings + self.total_info

    @property
    def has_errors(self) -> bool:
        """Whether there are any errors."""
        return self.total_errors > 0

    @property
    def has_warnings(self) -> bool:
        """Whether there are any warnings."""
        return self.total_warnings > 0

    @property
    def has_info(self) -> bool:
        """Whether there are any info messages."""
        return self.total_info > 0

    @property
    def is_success(self) -> bool:
        """Whether validation was successful (no errors or warnings)."""
        return not self.has_errors and not self.has_warnings


class OutputFormatter(ABC):
    """Abstract base class for output formatters."""

    def __init__(self, plain_text: bool = False):
        self.plain_text = plain_text

    @abstractmethod
    def format_error(self, error: ValidationError) -> str:
        """Format a single validation error."""
        pass

    @abstractmethod
    def format_errors(self, errors: list[ValidationError]) -> str:
        """Format a list of validation errors."""
        pass

    @abstractmethod
    def format_summary(self, summary: ValidationSummary) -> str:
        """Format a validation summary."""
        pass

    @abstractmethod
    def format_validation_result(self, errors: list[ValidationError], summary: ValidationSummary) -> str:
        """Format complete validation result."""
        pass

    def format_progress(self, current: int, total: int, message: str = "") -> str:
        """Format progress information."""
        if total == 0:
            return ""

        percentage = (current / total) * 100
        bar_length = 20
        filled_length = int(bar_length * current // total)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)

        if message:
            return f"{message} [{bar}] {percentage:.1f}% ({current}/{total})"
        else:
            return f"[{bar}] {percentage:.1f}% ({current}/{total})"
