"""Unit tests for the validator module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from n8n_lint.core.logger import LogLevel, OutputFormat
from n8n_lint.core.validator import (
    JSONParser,
    RequiredPropertyRule,
    TypeValidationRule,
    UnknownPropertyRule,
    ValidationEngine,
    validate_workflow_file,
)


class TestValidationRules:
    """Test individual validation rules."""

    def test_required_property_rule_success(self):
        """Test RequiredPropertyRule with valid data."""
        rule = RequiredPropertyRule()
        data = {"required_field": "value", "optional_field": "value"}
        schema = {"required": ["required_field"]}
        context = {"schema": schema, "node_type": "test"}

        errors = rule.validate(data, context)
        assert len(errors) == 0

    def test_required_property_rule_missing(self):
        """Test RequiredPropertyRule with missing required field."""
        rule = RequiredPropertyRule()
        data = {"optional_field": "value"}
        schema = {"required": ["required_field"]}
        context = {"schema": schema, "node_type": "test"}

        errors = rule.validate(data, context)
        assert len(errors) == 1
        assert errors[0].severity == "error"
        assert "Required property 'required_field' is missing" in errors[0].message

    def test_required_property_rule_no_required_list(self):
        """Test RequiredPropertyRule with no required list in schema."""
        rule = RequiredPropertyRule()
        data = {"field": "value"}
        schema = {"properties": {"field": {"type": "string"}}}
        context = {"schema": schema, "node_type": "test"}

        errors = rule.validate(data, context)
        assert len(errors) == 0

    def test_type_validation_rule_success(self):
        """Test TypeValidationRule with valid types."""
        rule = TypeValidationRule()
        data = {"string_field": "value", "number_field": 42, "boolean_field": True}
        schema = {
            "properties": {
                "string_field": {"type": "string"},
                "number_field": {"type": "number"},
                "boolean_field": {"type": "boolean"},
            }
        }
        context = {"schema": schema, "node_type": "test"}

        errors = rule.validate(data, context)
        assert len(errors) == 0

    def test_type_validation_rule_wrong_type(self):
        """Test TypeValidationRule with wrong types."""
        rule = TypeValidationRule()
        data = {"string_field": 42, "number_field": "not_a_number"}
        schema = {
            "properties": {
                "string_field": {"type": "string"},
                "number_field": {"type": "number"},
            }
        }
        context = {"schema": schema, "node_type": "test"}

        errors = rule.validate(data, context)
        assert len(errors) == 2
        assert all(error.severity == "error" for error in errors)
        assert "Property 'string_field' has wrong type" in errors[0].message
        assert "Property 'number_field' has wrong type" in errors[1].message

    def test_unknown_property_rule_success(self):
        """Test UnknownPropertyRule with known properties only."""
        rule = UnknownPropertyRule()
        data = {"known_field": "value"}
        schema = {"properties": {"known_field": {"type": "string"}}}
        context = {"schema": schema, "node_type": "test"}

        errors = rule.validate(data, context)
        assert len(errors) == 0

    def test_unknown_property_rule_unknown(self):
        """Test UnknownPropertyRule with unknown properties."""
        rule = UnknownPropertyRule()
        data = {"known_field": "value", "unknown_field": "value"}
        schema = {"properties": {"known_field": {"type": "string"}}}
        context = {"schema": schema, "node_type": "test"}

        errors = rule.validate(data, context)
        assert len(errors) == 1
        assert errors[0].severity == "warning"
        assert "Unknown property 'unknown_field'" in errors[0].message


class TestJSONParser:
    """Test JSON parsing functionality."""

    def test_parse_string_valid(self):
        """Test parsing valid JSON string."""
        parser = JSONParser(Mock())
        data = '{"key": "value", "number": 42}'

        result = parser.parse_string(data)
        assert result == {"key": "value", "number": 42}

    def test_parse_string_invalid(self):
        """Test parsing invalid JSON string."""
        parser = JSONParser(Mock())
        data = '{"key": "value", "number": 42'  # Missing closing brace

        result = parser.parse_string(data)
        assert result is None

    def test_parse_file_valid(self):
        """Test parsing valid JSON file."""
        parser = JSONParser(Mock())
        data = {"key": "value", "number": 42}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            temp_path = Path(f.name)

        try:
            result = parser.parse_file(temp_path)
            assert result == data
        finally:
            temp_path.unlink()

    def test_parse_file_invalid(self):
        """Test parsing invalid JSON file."""
        parser = JSONParser(Mock())

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"key": "value", "number": 42')  # Missing closing brace
            temp_path = Path(f.name)

        try:
            result = parser.parse_file(temp_path)
            assert result is None
        finally:
            temp_path.unlink()

    def test_parse_file_not_found(self):
        """Test parsing non-existent file."""
        parser = JSONParser(Mock())
        result = parser.parse_file(Path("nonexistent.json"))
        assert result is None

    def test_get_json_suggestions(self):
        """Test JSON error suggestions."""
        parser = JSONParser(Mock())

        # Test comma delimiter error
        content = '{"key": "value" "another": "value"}'
        error = Mock()
        error.msg = "Expecting ',' delimiter"

        suggestions = parser._get_json_suggestions(content, error)
        assert "Add missing comma" in suggestions

        # Test colon delimiter error
        error.msg = "Expecting ':' delimiter"
        suggestions = parser._get_json_suggestions(content, error)
        assert "Add missing colon" in suggestions


class TestValidationEngine:
    """Test the main validation engine."""

    def test_validate_workflow_structure_valid(self):
        """Test workflow structure validation with valid data."""
        engine = ValidationEngine(Mock())
        workflow_data = {"nodes": [{"id": "1", "type": "test"}], "connections": {"1": {"main": []}}}

        result = engine._validate_workflow_structure(workflow_data, "test.json")
        assert result is True

    def test_validate_workflow_structure_missing_nodes(self):
        """Test workflow structure validation with missing nodes."""
        engine = ValidationEngine(Mock())
        workflow_data = {"connections": {}}

        result = engine._validate_workflow_structure(workflow_data, "test.json")
        assert result is False

    def test_validate_workflow_structure_missing_connections(self):
        """Test workflow structure validation with missing connections."""
        engine = ValidationEngine(Mock())
        workflow_data = {"nodes": []}

        result = engine._validate_workflow_structure(workflow_data, "test.json")
        assert result is False

    def test_validate_node_valid(self):
        """Test node validation with valid node."""
        engine = ValidationEngine(Mock())
        node = {
            "id": "1",
            "name": "Test Node",
            "type": "n8n-nodes-base.function",
            "typeVersion": 1,
            "position": [100, 100],
            "parameters": {"functionCode": "return $input.all();"},
        }

        # Mock schema manager to return a schema
        with patch("n8n_lint.core.validator.schema_manager") as mock_schema_manager:
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

            result = engine._validate_node(node, 0, "test.json")
            assert result is True

    def test_validate_node_missing_type(self):
        """Test node validation with missing type."""
        engine = ValidationEngine(Mock())
        node = {"id": "1", "name": "Test Node"}

        result = engine._validate_node(node, 0, "test.json")
        assert result is False

    def test_validate_node_not_dict(self):
        """Test node validation with non-dict node."""
        engine = ValidationEngine(Mock())
        node = "not_a_dict"

        result = engine._validate_node(node, 0, "test.json")
        assert result is False

    def test_validate_workflow_integration(self):
        """Test full workflow validation integration."""
        engine = ValidationEngine(Mock())
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

        # Mock schema manager
        with patch("n8n_lint.core.validator.schema_manager") as mock_schema_manager:
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

            result = engine.validate_workflow(workflow_data, "test.json")
            assert result is True


class TestValidateWorkflowFile:
    """Test the main validate_workflow_file function."""

    def test_validate_workflow_file_success(self):
        """Test successful workflow file validation."""
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
            with patch("n8n_lint.core.validator.schema_manager") as mock_schema_manager:
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

                exit_code = validate_workflow_file(temp_path, LogLevel.NORMAL, OutputFormat.CONSOLE, False)
                assert exit_code == 0
        finally:
            temp_path.unlink()

    def test_validate_workflow_file_invalid_json(self):
        """Test validation with invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"invalid": json}')  # Invalid JSON
            temp_path = Path(f.name)

        try:
            exit_code = validate_workflow_file(temp_path, LogLevel.NORMAL, OutputFormat.CONSOLE, False)
            assert exit_code == 1  # Error exit code
        finally:
            temp_path.unlink()

    def test_validate_workflow_file_not_found(self):
        """Test validation with non-existent file."""
        exit_code = validate_workflow_file(Path("nonexistent.json"), LogLevel.NORMAL, OutputFormat.CONSOLE, False)
        assert exit_code == 1  # Error exit code
