"""Unit tests for the CLI module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from n8n_lint.cli.main import app


class TestCLI:
    """Test CLI functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_help(self):
        """Test CLI help command."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Validate n8n workflow JSON files" in result.output

    def test_cli_version(self):
        """Test CLI version command."""
        result = self.runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "n8n-lint version 1.1.2" in result.output

    def test_validate_command_help(self):
        """Test validate command help."""
        result = self.runner.invoke(app, ["validate", "--help"])
        assert result.exit_code == 0
        assert "Validate an n8n workflow JSON file" in result.output

    def test_validate_command_file_not_found(self):
        """Test validate command with non-existent file."""
        result = self.runner.invoke(app, ["validate", "nonexistent.json"])
        assert result.exit_code == 1  # Error code for file not found

    def test_validate_command_invalid_json(self):
        """Test validate command with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"invalid": json}')  # Invalid JSON
            temp_path = Path(f.name)

        try:
            result = self.runner.invoke(app, ["validate", str(temp_path)])
            assert result.exit_code == 1  # Error exit code
        finally:
            temp_path.unlink()

    def test_validate_command_success(self):
        """Test validate command with valid workflow."""
        workflow_data = {
            "nodes": [
                {
                    "id": "1",
                    "name": "Test Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                }
            ],
            "connections": {"1": {"main": []}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager to return a schema
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.get_schema.return_value = {
                    "type": "object",
                    "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "typeVersion": {"type": "number"},
                        "position": {"type": "array"},
                        "parameters": {"type": "object"},
                    },
                }

                result = self.runner.invoke(app, ["validate", str(temp_path)])
                assert result.exit_code == 0  # Success
        finally:
            temp_path.unlink()

    def test_validate_command_with_errors(self):
        """Test validate command with validation errors."""
        workflow_data = {
            "nodes": [
                {
                    "id": "1",
                    "name": "Test Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    # Missing required "parameters" field
                }
            ],
            "connections": {"1": {"main": []}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager to return a schema
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.get_schema.return_value = {
                    "type": "object",
                    "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "typeVersion": {"type": "number"},
                        "position": {"type": "array"},
                        "parameters": {"type": "object"},
                    },
                }

                result = self.runner.invoke(app, ["validate", str(temp_path), "--deep"])
                assert result.exit_code == 1  # Error exit code
                assert "ERROR:" in result.output
        finally:
            temp_path.unlink()

    def test_validate_command_quiet_mode(self):
        """Test validate command with quiet mode."""
        workflow_data = {
            "nodes": [
                {
                    "id": "1",
                    "name": "Test Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                }
            ],
            "connections": {"1": {"main": []}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.get_schema.return_value = {
                    "type": "object",
                    "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "typeVersion": {"type": "number"},
                        "position": {"type": "array"},
                        "parameters": {"type": "object"},
                    },
                }

                result = self.runner.invoke(app, ["validate", str(temp_path), "--quiet"])
                assert result.exit_code == 0
        finally:
            temp_path.unlink()

    def test_validate_command_verbose_mode(self):
        """Test validate command with verbose mode."""
        workflow_data = {
            "nodes": [
                {
                    "id": "1",
                    "name": "Test Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                }
            ],
            "connections": {"1": {"main": []}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.get_schema.return_value = {
                    "type": "object",
                    "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "typeVersion": {"type": "number"},
                        "position": {"type": "array"},
                        "parameters": {"type": "object"},
                    },
                }

                result = self.runner.invoke(app, ["validate", str(temp_path), "--verbose"])
                assert result.exit_code == 0
        finally:
            temp_path.unlink()

    def test_validate_command_debug_mode(self):
        """Test validate command with debug mode."""
        workflow_data = {
            "nodes": [
                {
                    "id": "1",
                    "name": "Test Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                }
            ],
            "connections": {"1": {"main": []}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.get_schema.return_value = {
                    "type": "object",
                    "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "typeVersion": {"type": "number"},
                        "position": {"type": "array"},
                        "parameters": {"type": "object"},
                    },
                }

                result = self.runner.invoke(app, ["validate", str(temp_path), "--debug"])
                assert result.exit_code == 0
        finally:
            temp_path.unlink()

    def test_validate_command_json_output(self):
        """Test validate command with JSON output."""
        workflow_data = {
            "nodes": [
                {
                    "id": "1",
                    "name": "Test Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                }
            ],
            "connections": {"1": {"main": []}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.get_schema.return_value = {
                    "type": "object",
                    "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "typeVersion": {"type": "number"},
                        "position": {"type": "array"},
                        "parameters": {"type": "object"},
                    },
                }

                result = self.runner.invoke(app, ["validate", str(temp_path), "--output", "json"])
                assert result.exit_code == 0

                # Check that output contains valid JSON
                output = result.output.strip()
                # Should be valid JSON
                json.loads(output)
        finally:
            temp_path.unlink()

    def test_validate_command_plain_text(self):
        """Test validate command with plain text output."""
        workflow_data = {
            "nodes": [
                {
                    "id": "1",
                    "name": "Test Node",
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [100, 100],
                    "parameters": {"functionCode": "return $input.all();"},
                }
            ],
            "connections": {"1": {"main": []}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(workflow_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.get_schema.return_value = {
                    "type": "object",
                    "required": ["id", "name", "type", "typeVersion", "position", "parameters"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "typeVersion": {"type": "number"},
                        "position": {"type": "array"},
                        "parameters": {"type": "object"},
                    },
                }

                result = self.runner.invoke(app, ["validate", str(temp_path), "--plain-text"])
                assert result.exit_code == 0
        finally:
            temp_path.unlink()

    def test_import_schema_command_help(self):
        """Test import-schema command help."""
        result = self.runner.invoke(app, ["import-schema", "--help"])
        assert result.exit_code == 0
        assert "Import a new node schema for validation" in result.output

    def test_import_schema_command_success(self):
        """Test import-schema command success."""
        schema_data = {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(schema_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager at the module level
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.import_schema.return_value = True

                result = self.runner.invoke(app, ["import-schema", str(temp_path), "--node-type", "test-node"])

                # The mock should make this succeed
                assert result.exit_code == 0
                assert "Successfully imported schema" in result.output
        finally:
            temp_path.unlink()

    def test_import_schema_command_failure(self):
        """Test import-schema command failure."""
        schema_data = {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(schema_data, f)
            temp_path = Path(f.name)

        try:
            # Mock schema manager
            with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
                mock_schema_manager.import_schema.return_value = False

                result = self.runner.invoke(app, ["import-schema", str(temp_path), "--node-type", "test-node"])

                assert result.exit_code == 1
                assert "Failed to import schema" in result.output
        finally:
            temp_path.unlink()

    def test_import_schema_command_invalid_json(self):
        """Test import-schema command with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"invalid": json}')  # Invalid JSON
            temp_path = Path(f.name)

        try:
            result = self.runner.invoke(app, ["import-schema", str(temp_path), "--node-type", "test-node"])

            assert result.exit_code == 1
            assert "Invalid JSON" in result.output
        finally:
            temp_path.unlink()

    def test_list_schemas_command(self):
        """Test list-schemas command."""
        # Mock schema manager
        with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
            mock_schema_manager.list_node_types.return_value = ["node1", "node2"]
            mock_schema_manager.get_registry_entry.side_effect = [
                {"description": "Test node 1"},
                {"description": "Test node 2"},
            ]

            result = self.runner.invoke(app, ["list-schemas"])

            assert result.exit_code == 0
            assert "Available node schemas:" in result.output
            assert "node1: Test node 1" in result.output
            assert "node2: Test node 2" in result.output

    def test_list_schemas_command_no_schemas(self):
        """Test list-schemas command with no schemas."""
        # Mock schema manager
        with patch("n8n_lint.cli.main.schema_manager") as mock_schema_manager:
            mock_schema_manager.list_node_types.return_value = []

            result = self.runner.invoke(app, ["list-schemas"])

            assert result.exit_code == 0
            assert "No schemas available." in result.output
