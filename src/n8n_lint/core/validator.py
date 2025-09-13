"""Core validation logic for n8n workflows."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..schemas import schema_manager
from .errors import ValidationError
from .logger import LogLevel, N8nLogger, OutputFormat


class ValidationRule(ABC):
    """Abstract base class for validation rules."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def validate(self, data: Any, context: dict[str, Any]) -> list[ValidationError]:
        """Validate data and return list of errors."""
        pass


class RequiredPropertyRule(ValidationRule):
    """Validates that required properties are present."""

    def __init__(self):
        super().__init__("required_property", "Validates required properties are present")

    def validate(self, data: Any, context: dict[str, Any]) -> list[ValidationError]:
        errors: list[ValidationError] = []

        if not isinstance(data, dict):
            return errors

        schema = context.get("schema")
        if not schema or "required" not in schema:
            return errors

        required_props = schema["required"]
        for prop in required_props:
            if prop not in data:
                errors.append(
                    ValidationError(
                        message=f"Required property '{prop}' is missing",
                        severity="error",
                        node_type=context.get("node_type"),
                        property_path=prop,
                        expected="present",
                        actual="missing",
                    )
                )

        return errors


class TypeValidationRule(ValidationRule):
    """Validates property types match schema."""

    def __init__(self):
        super().__init__("type_validation", "Validates property types match schema")

    def validate(self, data: Any, context: dict[str, Any]) -> list[ValidationError]:
        errors: list[ValidationError] = []

        if not isinstance(data, dict):
            return errors

        schema = context.get("schema")
        if not schema or "properties" not in schema:
            return errors

        properties = schema["properties"]
        for prop, value in data.items():
            if prop in properties:
                prop_schema = properties[prop]
                if "type" in prop_schema:
                    expected_type = prop_schema["type"]
                    actual_type = self._get_type_name(value)

                    if not self._type_matches(value, expected_type):
                        errors.append(
                            ValidationError(
                                message=f"Property '{prop}' has wrong type",
                                severity="error",
                                node_type=context.get("node_type"),
                                property_path=prop,
                                expected=expected_type,
                                actual=actual_type,
                            )
                        )

        return errors

    def _get_type_name(self, value: Any) -> str:
        """Get type name for a value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return type(value).__name__

    def _type_matches(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected type."""
        if expected_type == "null":
            return value is None
        elif expected_type == "boolean":
            return isinstance(value, bool)
        elif expected_type == "integer":
            return isinstance(value, int)
        elif expected_type == "number":
            return isinstance(value, int | float)
        elif expected_type == "string":
            return isinstance(value, str)
        elif expected_type == "array":
            return isinstance(value, list)
        elif expected_type == "object":
            return isinstance(value, dict)
        else:
            return True  # Unknown type, don't validate


class UnknownPropertyRule(ValidationRule):
    """Warns about unknown properties."""

    def __init__(self):
        super().__init__("unknown_property", "Warns about unknown properties")

    def validate(self, data: Any, context: dict[str, Any]) -> list[ValidationError]:
        errors: list[ValidationError] = []

        if not isinstance(data, dict):
            return errors

        schema = context.get("schema")
        if not schema or "properties" not in schema:
            return errors

        known_props = set(schema["properties"].keys())
        for prop in data:
            if prop not in known_props:
                errors.append(
                    ValidationError(
                        message=f"Unknown property '{prop}'",
                        severity="warning",
                        node_type=context.get("node_type"),
                        property_path=prop,
                        expected="known property",
                        actual="unknown property",
                    )
                )

        return errors


class ValidationEngine:
    """Main validation engine that coordinates rules."""

    def __init__(self, logger: N8nLogger):
        self.logger = logger
        self.rules: list[ValidationRule] = [RequiredPropertyRule(), TypeValidationRule(), UnknownPropertyRule()]
        self._schema_cache: dict[str, dict[str, Any] | None] = {}  # Cache for schema lookups

    def validate_workflow(self, workflow_data: dict[str, Any], file_path: str | None = None) -> bool:
        """Validate an n8n workflow."""
        self.logger.log_debug(f"Starting validation of workflow from {file_path}")

        # Validate workflow structure
        if not self._validate_workflow_structure(workflow_data, file_path):
            return False

        # Validate nodes
        nodes = workflow_data.get("nodes", [])
        if not isinstance(nodes, list):
            self.logger.log_error("Workflow 'nodes' must be an array", file_path=file_path)
            return False

        all_valid = True
        for i, node in enumerate(nodes):
            # Update progress for each node
            node_type = node.get("type", "unknown")
            node_name = node.get("name", f"Node {i}")
            self.logger.update_progress(node_name, node_type)

            if not self._validate_node(node, i, file_path):
                all_valid = False

        return all_valid

    def _validate_workflow_structure(self, workflow_data: dict[str, Any], file_path: str | None) -> bool:
        """Validate basic workflow structure."""
        required_fields = ["nodes", "connections"]

        for field in required_fields:
            if field not in workflow_data:
                self.logger.log_error(f"Workflow missing required field '{field}'", file_path=file_path)
                return False

        return True

    def _validate_node(self, node: dict[str, Any], node_index: int, file_path: str | None) -> bool:
        """Validate a single node."""
        if not isinstance(node, dict):
            self.logger.log_error(
                f"Node {node_index} must be an object", file_path=file_path, line_number=node_index + 1
            )
            return False

        # Get node type
        node_type = node.get("type")
        if not node_type:
            self.logger.log_error(
                f"Node {node_index} missing 'type' property", file_path=file_path, line_number=node_index + 1
            )
            return False

        # Get schema for node type (with caching)
        schema = self._get_cached_schema(node_type)
        if not schema:
            self.logger.log_warning(
                f"No schema found for node type '{node_type}'",
                node_type=node_type,
                file_path=file_path,
                line_number=node_index + 1,
            )
            return True  # Don't fail validation for unknown node types

        # Validate node against schema
        context = {"schema": schema, "node_type": node_type, "node_index": node_index, "file_path": file_path}

        all_valid = True
        for rule in self.rules:
            errors = rule.validate(node, context)
            for error in errors:
                if error.severity == "error":
                    all_valid = False

                # Log the error with appropriate method
                if error.severity == "error":
                    self.logger.log_error(
                        error.message,
                        node_type=error.node_type,
                        property_path=error.property_path,
                        expected=error.expected,
                        actual=error.actual,
                        line_number=node_index + 1,
                        file_path=file_path,
                    )
                else:
                    self.logger.log_warning(
                        error.message,
                        node_type=error.node_type,
                        property_path=error.property_path,
                        expected=error.expected,
                        actual=error.actual,
                        line_number=node_index + 1,
                        file_path=file_path,
                    )

        return all_valid

    def _get_cached_schema(self, node_type: str) -> dict[str, Any] | None:
        """Get schema with caching for better performance."""
        if node_type not in self._schema_cache:
            self._schema_cache[node_type] = schema_manager.get_schema(node_type)
        return self._schema_cache[node_type]


class JSONParser:
    """JSON parser with error recovery and suggestions."""

    def __init__(self, logger: N8nLogger):
        self.logger = logger

    def parse_file(self, file_path: str | Path) -> dict[str, Any] | None:
        """Parse JSON file with error recovery."""
        file_path = Path(file_path)

        if not file_path.exists():
            self.logger.log_error(f"File not found: {file_path}")
            return None

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            return self.parse_string(content, str(file_path))

        except OSError as e:
            self.logger.log_error(f"Failed to read file {file_path}: {e}")
            return None

    def parse_string(self, content: str, file_path: str | None = None) -> dict[str, Any] | None:
        """Parse JSON string with error recovery."""
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Invalid JSON: {e.msg}", file_path=file_path, line_number=e.lineno)

            # Try to provide suggestions
            suggestions = self._get_json_suggestions(content, e)
            if suggestions:
                self.logger.log_info(f"Suggestions: {suggestions}")

            return None

    def _get_json_suggestions(self, content: str, error: json.JSONDecodeError) -> str:
        """Get suggestions for fixing JSON errors."""
        suggestions = []

        if "Expecting ',' delimiter" in error.msg:
            suggestions.append("Add missing comma")
        elif "Expecting ':' delimiter" in error.msg:
            suggestions.append("Add missing colon")
        elif "Expecting property name" in error.msg:
            suggestions.append("Add property name or fix quotes")
        elif "Unterminated string" in error.msg:
            suggestions.append("Add missing closing quote")
        elif "Extra data" in error.msg:
            suggestions.append("Remove extra characters after JSON")

        return "; ".join(suggestions) if suggestions else "Check JSON syntax"


def validate_workflow_file(
    file_path: str | Path,
    log_level: LogLevel = LogLevel.NORMAL,
    output_format: OutputFormat = OutputFormat.CONSOLE,
    plain_text: bool = False,
    logger: N8nLogger | None = None,
) -> int:
    """Validate an n8n workflow file and return exit code."""

    # Setup logger if not provided
    if logger is None:
        # Disable progress for JSON output to avoid interfering with JSON parsing
        show_progress = output_format != OutputFormat.JSON
        logger = N8nLogger(log_level, output_format, plain_text, show_progress)

    # Parse JSON
    parser = JSONParser(logger)
    workflow_data = parser.parse_file(file_path)

    if workflow_data is None:
        logger.print_summary(str(file_path))
        return logger.get_exit_code()

    # Count nodes for progress tracking
    total_nodes = 0
    if isinstance(workflow_data, dict) and "nodes" in workflow_data:
        total_nodes = len(workflow_data["nodes"])

    # Start progress tracking
    logger.start_validation(total_nodes, str(file_path))

    # Validate workflow
    engine = ValidationEngine(logger)
    engine.validate_workflow(workflow_data, str(file_path))

    # Complete progress tracking
    logger.complete_validation()

    # Print summary
    logger.print_summary(str(file_path), total_nodes)

    return logger.get_exit_code()
