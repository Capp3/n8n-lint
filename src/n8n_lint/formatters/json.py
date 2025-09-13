"""JSON formatter for n8n-lint output."""

import json
from datetime import datetime

from ..core.errors import ValidationError
from .base import OutputFormatter, ValidationSummary


class JSONFormatter(OutputFormatter):
    """JSON formatter for structured output."""

    def __init__(self, plain_text: bool = False):
        super().__init__(plain_text)

    def format_error(self, error: ValidationError) -> str:
        """Format a single validation error as JSON."""
        return json.dumps(error.to_dict(), indent=2)

    def format_errors(self, errors: list[ValidationError]) -> str:
        """Format a list of validation errors as JSON."""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "errors": [error.to_dict() for error in errors],
            "count": len(errors),
        }
        return json.dumps(error_data, indent=2)

    def format_summary(self, summary: ValidationSummary) -> str:
        """Format a validation summary as JSON."""
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "errors": summary.total_errors,
                "warnings": summary.total_warnings,
                "info": summary.total_info,
                "total_messages": summary.total_messages,
                "total_nodes": summary.total_nodes,
                "validation_time": summary.validation_time,
                "file_path": summary.file_path,
                "has_errors": summary.has_errors,
                "has_warnings": summary.has_warnings,
                "has_info": summary.has_info,
                "is_success": summary.is_success,
            },
        }
        return json.dumps(summary_data, indent=2)

    def format_validation_result(self, errors: list[ValidationError], summary: ValidationSummary) -> str:
        """Format complete validation result as JSON."""
        result_data = {
            "timestamp": datetime.now().isoformat(),
            "validation_result": {
                "errors": [error.to_dict() for error in errors],
                "summary": {
                    "errors": summary.total_errors,
                    "warnings": summary.total_warnings,
                    "info": summary.total_info,
                    "total_messages": summary.total_messages,
                    "total_nodes": summary.total_nodes,
                    "validation_time": summary.validation_time,
                    "file_path": summary.file_path,
                    "has_errors": summary.has_errors,
                    "has_warnings": summary.has_warnings,
                    "has_info": summary.has_info,
                    "is_success": summary.is_success,
                },
            },
        }
        return json.dumps(result_data, indent=2)
