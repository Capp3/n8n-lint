def test_print_summary_json_format():
    """Test summary printing in JSON format."""
    import io
    import json
    import sys

    from n8n_lint.core.logger import LogLevel, N8nLogger, OutputFormat

    logger = N8nLogger(LogLevel.NORMAL, OutputFormat.JSON, False)
    logger.log_error("Test error")
    logger.log_warning("Test warning")

    # Use stdout capture instead of mock
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        logger.print_summary()
        output = captured_output.getvalue()

        # Should be valid JSON
        json_output = json.loads(output)

        assert "validation_result" in json_output
        assert "summary" in json_output["validation_result"]
        assert json_output["validation_result"]["summary"]["errors"] == 1
        assert json_output["validation_result"]["summary"]["warnings"] == 1
    finally:
        sys.stdout = sys.__stdout__  # Restore stdout
