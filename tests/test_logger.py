"""Unit tests for the logger module."""

import json
from unittest.mock import Mock, patch

from n8n_lint.core.errors import ValidationError
from n8n_lint.core.logger import LogLevel, N8nLogger, OutputFormat
from n8n_lint.formatters.base import ValidationSummary


class TestLogLevel:
    """Test LogLevel enum functionality."""

    def test_log_level_comparison(self):
        """Test LogLevel comparison operators."""
        assert LogLevel.QUIET < LogLevel.NORMAL
        assert LogLevel.NORMAL < LogLevel.VERBOSE
        assert LogLevel.VERBOSE < LogLevel.DEBUG

        assert LogLevel.DEBUG > LogLevel.VERBOSE
        assert LogLevel.VERBOSE > LogLevel.NORMAL
        assert LogLevel.NORMAL > LogLevel.QUIET

        assert LogLevel.NORMAL >= LogLevel.NORMAL
        assert LogLevel.NORMAL <= LogLevel.NORMAL


class TestValidationError:
    """Test ValidationError class."""

    def test_validation_error_creation(self):
        """Test ValidationError creation with all parameters."""
        error = ValidationError(
            message="Test error",
            severity="error",
            node_type="test-node",
            property_path="test.property",
            expected="string",
            actual="number",
            line_number=42,
            file_path="test.json",
        )

        assert error.message == "Test error"
        assert error.severity == "error"
        assert error.node_type == "test-node"
        assert error.property_path == "test.property"
        assert error.expected == "string"
        assert error.actual == "number"
        assert error.line_number == 42
        assert error.file_path == "test.json"

    def test_validation_error_minimal(self):
        """Test ValidationError creation with minimal parameters."""
        error = ValidationError("Test error")

        assert error.message == "Test error"
        assert error.severity == "error"
        assert error.node_type is None
        assert error.property_path is None
        assert error.expected is None
        assert error.actual is None
        assert error.line_number is None
        assert error.file_path is None

    def test_validation_error_to_dict(self):
        """Test ValidationError to_dict method."""
        error = ValidationError(
            message="Test error",
            severity="warning",
            node_type="test-node",
            property_path="test.property",
            expected="string",
            actual="number",
            line_number=42,
            file_path="test.json",
        )

        result = error.to_dict()
        expected = {
            "message": "Test error",
            "severity": "warning",
            "node_type": "test-node",
            "property_path": "test.property",
            "expected": "string",
            "actual": "number",
            "line_number": 42,
            "file_path": "test.json",
        }

        assert result == expected

    def test_validation_error_to_console_text(self):
        """Test ValidationError to_console_text method."""
        error = ValidationError(
            message="Test error", severity="error", node_type="test-node", property_path="test.property", line_number=42
        )

        text = error.to_console_text()
        assert "ERROR: Test error" in str(text)
        assert "Node: test-node" in str(text)
        assert "Property: test.property" in str(text)
        assert "Line: 42" in str(text)


class TestN8nLogger:
    """Test N8nLogger class."""

    def test_logger_initialization_default(self):
        """Test logger initialization with default parameters."""
        logger = N8nLogger()

        assert logger.log_level == LogLevel.NORMAL
        assert logger.output_format == OutputFormat.CONSOLE
        assert logger.plain_text is False
        assert len(logger.errors) == 0
        assert len(logger.warnings) == 0
        assert len(logger.info_messages) == 0

    def test_logger_initialization_custom(self):
        """Test logger initialization with custom parameters."""
        logger = N8nLogger(log_level=LogLevel.DEBUG, output_format=OutputFormat.JSON, plain_text=True)

        assert logger.log_level == LogLevel.DEBUG
        assert logger.output_format == OutputFormat.JSON
        assert logger.plain_text is True

    def test_log_error(self):
        """Test logging error messages."""
        logger = N8nLogger(LogLevel.NORMAL, OutputFormat.CONSOLE, False)

        logger.log_error("Test error", node_type="test-node")

        assert len(logger.errors) == 1
        assert logger.errors[0].message == "Test error"
        assert logger.errors[0].node_type == "test-node"
        assert logger.errors[0].severity == "error"

    def test_log_warning(self):
        """Test logging warning messages."""
        logger = N8nLogger(LogLevel.NORMAL, OutputFormat.CONSOLE, False)

        logger.log_warning("Test warning", node_type="test-node")

        assert len(logger.warnings) == 1
        assert logger.warnings[0].message == "Test warning"
        assert logger.warnings[0].node_type == "test-node"
        assert logger.warnings[0].severity == "warning"

    def test_log_info(self):
        """Test logging info messages."""
        logger = N8nLogger(LogLevel.VERBOSE, OutputFormat.CONSOLE, False)

        logger.log_info("Test info", node_type="test-node")

        assert len(logger.info_messages) == 1
        assert logger.info_messages[0].message == "Test info"
        assert logger.info_messages[0].node_type == "test-node"
        assert logger.info_messages[0].severity == "info"

    def test_log_debug(self):
        """Test logging debug messages."""
        logger = N8nLogger(LogLevel.DEBUG, OutputFormat.CONSOLE, False)

        # Mock the internal logger
        logger.logger = Mock()

        logger.log_debug("Test debug")

        logger.logger.debug.assert_called_once_with("Test debug")

    def test_log_level_filtering_quiet(self):
        """Test log level filtering in quiet mode."""
        logger = N8nLogger(LogLevel.QUIET, OutputFormat.CONSOLE, False)

        # Mock console to capture output
        with patch.object(logger.console, "print") as mock_print:
            logger.log_error("Test error")
            logger.log_warning("Test warning")
            logger.log_info("Test info")

            # In quiet mode, only errors should be printed
            assert mock_print.call_count == 1

    def test_log_level_filtering_normal(self):
        """Test log level filtering in normal mode."""
        logger = N8nLogger(LogLevel.NORMAL, OutputFormat.CONSOLE, False)

        # Mock console to capture output
        with patch.object(logger.console, "print") as mock_print:
            logger.log_error("Test error")
            logger.log_warning("Test warning")
            logger.log_info("Test info")

            # In normal mode, errors and warnings should be printed
            assert mock_print.call_count == 2

    def test_log_level_filtering_verbose(self):
        """Test log level filtering in verbose mode."""
        logger = N8nLogger(LogLevel.VERBOSE, OutputFormat.CONSOLE, False)

        # Mock console to capture output
        with patch.object(logger.console, "print") as mock_print:
            logger.log_error("Test error")
            logger.log_warning("Test warning")
            logger.log_info("Test info")

            # In verbose mode, errors, warnings, and info should be printed
            assert mock_print.call_count == 3

    def test_json_output_format(self):
        """Test JSON output format."""
        logger = N8nLogger(LogLevel.NORMAL, OutputFormat.JSON, False)

        # Mock console to capture output
        with patch.object(logger.console, "print") as mock_print:
            logger.log_error("Test error", node_type="test-node")

            # Verify JSON output
            call_args = mock_print.call_args[0][0]
            json_output = json.loads(call_args)

            assert json_output["level"] == "ERROR"
            assert json_output["message"] == "Test error"
            assert json_output["context"]["node_type"] == "test-node"

    def test_get_exit_code_errors(self):
        """Test exit code calculation with errors."""
        logger = N8nLogger()
        logger.log_error("Test error")
        logger.log_warning("Test warning")
        logger.log_info("Test info")

        exit_code = logger.get_exit_code()
        assert exit_code == 1  # Errors present

    def test_get_exit_code_warnings_only(self):
        """Test exit code calculation with warnings only."""
        logger = N8nLogger()
        logger.log_warning("Test warning")
        logger.log_info("Test info")

        exit_code = logger.get_exit_code()
        assert exit_code == 2  # Warnings only

    def test_get_exit_code_info_only(self):
        """Test exit code calculation with info only."""
        logger = N8nLogger()
        logger.log_info("Test info")

        exit_code = logger.get_exit_code()
        assert exit_code == 3  # Info only

    def test_get_exit_code_success(self):
        """Test exit code calculation with no messages."""
        logger = N8nLogger()

        exit_code = logger.get_exit_code()
        assert exit_code == 0  # Success

    def test_get_all_messages(self):
        """Test getting all validation messages."""
        logger = N8nLogger()
        logger.log_error("Test error")
        logger.log_warning("Test warning")
        logger.log_info("Test info")

        all_messages = logger.get_all_messages()
        assert len(all_messages) == 3
        assert all_messages[0].severity == "error"
        assert all_messages[1].severity == "warning"
        assert all_messages[2].severity == "info"

    def test_print_summary_with_errors(self):
        """Test summary printing with errors."""
        logger = N8nLogger(LogLevel.NORMAL, OutputFormat.CONSOLE, False)
        logger.log_error("Test error")
        logger.log_warning("Test warning")

        # Get the formatter to check what would be printed
        formatter = logger.formatters["console"]
        summary = ValidationSummary(
            total_errors=1,
            total_warnings=1,
            total_info=0,
            total_nodes=0,
            validation_time=0,
            file_path="",
        )

        # Get the summary text directly - bypassing the Panel
        summary_text = formatter._format_summary_plain(summary)

        # Verify summary text contains expected elements
        assert summary_text == "Validation complete: 1 error, 1 warning"

    def test_print_summary_json_format(self):
        """Test summary printing in JSON format."""
        logger = N8nLogger(LogLevel.NORMAL, OutputFormat.JSON, False)
        logger.log_error("Test error")
        logger.log_warning("Test warning")

        # For JSON output, we need to test the formatter directly
        formatter = logger.formatters["json"]
        all_messages = logger.get_all_messages()

        from n8n_lint.formatters.base import ValidationSummary

        summary = ValidationSummary(
            total_errors=1,
            total_warnings=1,
            total_info=0,
            total_nodes=0,
            validation_time=0,
            file_path="",
        )

        # Get the formatted output
        output = formatter.format_validation_result(all_messages, summary)

        # Should be valid JSON
        json_output = json.loads(output)

        assert "validation_result" in json_output
        assert "summary" in json_output["validation_result"]
        assert json_output["validation_result"]["summary"]["errors"] == 1
        assert json_output["validation_result"]["summary"]["warnings"] == 1

    def test_print_summary_no_issues(self):
        """Test summary printing with no issues."""
        logger = N8nLogger(LogLevel.NORMAL, OutputFormat.CONSOLE, False)

        # Get the formatter to check what would be printed
        formatter = logger.formatters["console"]
        summary = ValidationSummary(
            total_errors=0,
            total_warnings=0,
            total_info=0,
            total_nodes=0,
            validation_time=0,
            file_path="",
        )

        # Get the summary text directly - bypassing the Panel
        summary_text = formatter._format_summary_plain(summary)

        # Verify summary text contains expected elements
        assert summary_text == "Validation complete: No issues found"
