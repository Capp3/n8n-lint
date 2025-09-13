"""Integration tests for end-to-end validation."""

import json
import tempfile
from pathlib import Path

from typer.testing import CliRunner

from n8n_lint.cli.main import app


class TestIntegration:
    """Integration tests for the complete n8n-lint workflow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_complete_workflow_validation_success(self):
        """Test complete workflow validation with valid n8n workflow."""
        workflow_data = {
            "name": "Test Workflow",
            "nodes": [
                {"id": "1", "name": "Start", "type": "n8n-nodes-base.start", "typeVersion": 1, "position": [100, 100]},
                {
                    "id": "2",
                    "name": "Function Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [300, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                },
                {
                    "id": "3",
                    "name": "HTTP Request",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 1,
                    "position": [500, 100],
                    "parameters": {"url": "https://api.example.com/data", "method": "GET"},
                },
            ],
            "connections": {
                "Start": {"main": [[{"node": "Function Node", "type": "main", "index": 0}]]},
                "Function Node": {"main": [[{"node": "HTTP Request", "type": "main", "index": 0}]]},
            },
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            result = self.runner.invoke(app, ["validate", str(temp_path), "--deep"])

            # Should succeed with warnings for unknown node types
            assert result.exit_code == 2  # Warnings only
            assert "WARNING:" in result.output
            assert "No schema found for node type" in result.output
        finally:
            temp_path.unlink()

    def test_complete_workflow_validation_with_errors(self):
        """Test complete workflow validation with validation errors."""
        workflow_data = {
            "name": "Test Workflow with Errors",
            "nodes": [
                {
                    "id": "1",
                    "name": "Function Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    # Missing required "parameters" field
                },
                {
                    "id": "2",
                    "name": "HTTP Request",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 1,
                    "position": [300, 100],
                    "parameters": {
                        "url": "https://api.example.com/data"
                        # Missing required "method" field
                    },
                    "unknownProperty": "This should trigger a warning",
                },
            ],
            "connections": {},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            result = self.runner.invoke(app, ["validate", str(temp_path), "--deep"])

            # Should fail with errors
            assert result.exit_code == 1  # Errors present
            assert "ERROR:" in result.output
            assert "Required property" in result.output
            assert "WARNING:" in result.output
            assert "Unknown property" in result.output
        finally:
            temp_path.unlink()

    def test_json_output_format_integration(self):
        """Test JSON output format in integration scenario."""
        workflow_data = {
            "name": "Test Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Function Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                }
            ],
            "connections": {},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            result = self.runner.invoke(app, ["validate", str(temp_path), "--output", "json"])

            # Should succeed
            assert result.exit_code == 0

            # Parse JSON output - the entire output should be a single JSON object
            output = result.output.strip()
            json_obj = json.loads(output)

            # Verify JSON structure
            assert "timestamp" in json_obj
            assert "validation_result" in json_obj
            assert "summary" in json_obj["validation_result"]
            assert "errors" in json_obj["validation_result"]["summary"]
            assert "warnings" in json_obj["validation_result"]["summary"]
        finally:
            temp_path.unlink()

    def test_quiet_mode_integration(self):
        """Test quiet mode in integration scenario."""
        workflow_data = {
            "name": "Test Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Function Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    # Missing required "parameters" field
                }
            ],
            "connections": {},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            result = self.runner.invoke(app, ["validate", str(temp_path), "--quiet", "--deep"])

            # Should fail with errors
            assert result.exit_code == 1

            # In quiet mode, should only show errors, not warnings or info
            output = result.output
            assert "ERROR:" in output
            # Should have error message about missing parameters
            assert "parameters" in output and "missing" in output
        finally:
            temp_path.unlink()

    def test_verbose_mode_integration(self):
        """Test verbose mode in integration scenario."""
        workflow_data = {
            "name": "Test Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Function Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                }
            ],
            "connections": {},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            result = self.runner.invoke(app, ["validate", str(temp_path), "--verbose"])

            # Should succeed
            assert result.exit_code == 0

            # Should have validation complete message
            assert "Validation complete" in result.output
        finally:
            temp_path.unlink()

    def test_schema_import_and_validation_integration(self):
        """Test schema import followed by validation integration."""
        # First, create a custom schema
        custom_schema = {
            "type": "object",
            "title": "Custom Node Schema",
            "description": "Schema for custom node validation",
            "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
            "properties": {
                "id": {"type": "string", "description": "Unique identifier for the node"},
                "name": {"type": "string", "description": "Display name of the node"},
                "type": {"type": "string", "enum": ["custom-node"], "description": "Node type identifier"},
                "typeVersion": {"type": "number", "description": "Version of the node type"},
                "position": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 2,
                    "description": "Position coordinates [x, y]",
                },
                "parameters": {
                    "type": "object",
                    "required": ["customParam"],
                    "properties": {"customParam": {"type": "string", "description": "Custom parameter"}},
                },
            },
        }

        # Create temporary schema file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(custom_schema, f)
            schema_path = Path(f.name)

        # Create workflow with custom node
        workflow_data = {
            "name": "Test Workflow with Custom Node",
            "nodes": [
                {
                    "id": "1",
                    "name": "Custom Node",
                    "type": "custom-node",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"customParam": "test value"},
                }
            ],
            "connections": {},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            workflow_path = Path(f.name)

        try:
            # Import the custom schema
            import_result = self.runner.invoke(app, ["import-schema", str(schema_path), "--node-type", "custom-node"])

            assert import_result.exit_code == 0
            assert "Successfully imported schema" in import_result.output

            # Validate workflow with custom node
            validate_result = self.runner.invoke(app, ["validate", str(workflow_path)])

            # Should succeed since custom node now has schema
            assert validate_result.exit_code == 0
            assert "Validation complete: No issues found" in validate_result.output

        finally:
            schema_path.unlink()
            workflow_path.unlink()

    def test_multiple_validation_scenarios(self):
        """Test multiple validation scenarios in sequence."""
        test_cases = [
            {
                "name": "Valid workflow",
                "data": {
                    "name": "Valid Workflow",
                    "nodes": [
                        {
                            "id": "1",
                            "name": "Function Node",
                            "type": "n8n-nodes-base.function",
                            "typeVersion": 1,
                            "position": [100, 100],
                            "parameters": {"functionCode": "return $input.all();"},
                        }
                    ],
                    "connections": {},
                },
                "expected_exit_code": 0,
            },
            {
                "name": "Workflow with missing required field",
                "data": {
                    "name": "Invalid Workflow",
                    "nodes": [
                        {
                            "id": "1",
                            "name": "Function Node",
                            "type": "n8n-nodes-base.function",
                            "typeVersion": 1,
                            "position": [100, 100],
                            # Missing required "parameters" field
                        }
                    ],
                    "connections": {},
                },
                "expected_exit_code": 1,
            },
            {
                "name": "Workflow with unknown property",
                "data": {
                    "name": "Workflow with Unknown Property",
                    "nodes": [
                        {
                            "id": "1",
                            "name": "Function Node",
                            "type": "n8n-nodes-base.function",
                            "typeVersion": 1,
                            "position": [100, 100],
                            "parameters": {"functionCode": "return $input.all();"},
                            "unknownProperty": "This should trigger a warning",
                        }
                    ],
                    "connections": {},
                },
                "expected_exit_code": 2,  # Warnings only
            },
        ]

        for test_case in test_cases:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                json.dump(test_case["data"], f)
                temp_path = Path(f.name)

            try:
                # Use --deep flag for test cases that expect DEEP validation behavior
                if test_case["name"] in ["Workflow with missing required field", "Workflow with unknown property"]:
                    result = self.runner.invoke(app, ["validate", str(temp_path), "--deep"])
                else:
                    result = self.runner.invoke(app, ["validate", str(temp_path)])

                assert result.exit_code == test_case["expected_exit_code"], (
                    f"Test case '{test_case['name']}' failed: expected exit code {test_case['expected_exit_code']}, got {result.exit_code}"
                )
            finally:
                temp_path.unlink()
