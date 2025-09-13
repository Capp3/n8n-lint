"""Unit tests for the schemas module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from n8n_lint.schemas import SchemaManager


class TestSchemaManager:
    """Test SchemaManager functionality."""

    def test_schema_manager_initialization(self):
        """Test SchemaManager initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with (
                patch("n8n_lint.schemas.SCHEMAS_DIR", temp_path),
                patch("n8n_lint.schemas.REGISTRY_FILE", temp_path / "registry.json"),
                patch.object(Path, "exists", return_value=False),
            ):
                # Mock registry file not existing
                manager = SchemaManager()

                assert manager.registry == {}
                assert manager.schemas == {}

    def test_load_registry_success(self):
        """Test successful registry loading."""
        registry_data = {
            "version": "1.0.0",
            "schemas": {"test-node": {"file": "test.json", "description": "Test node"}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(registry_data, f)
            temp_path = Path(f.name)

        try:
            with patch("n8n_lint.schemas.REGISTRY_FILE", temp_path):
                manager = SchemaManager()
                assert manager.registry == registry_data
        finally:
            temp_path.unlink()

    def test_load_registry_invalid_json(self):
        """Test registry loading with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"invalid": json}')  # Invalid JSON
            temp_path = Path(f.name)

        try:
            with patch("n8n_lint.schemas.REGISTRY_FILE", temp_path):
                manager = SchemaManager()
                assert manager.registry == {}
        finally:
            temp_path.unlink()

    def test_load_schemas_from_registry(self):
        """Test loading schemas from registry entries."""
        registry_data = {
            "version": "1.0.0",
            "schemas": {"test-node": {"file": "test.json", "description": "Test node"}},
        }

        schema_data = {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}}}

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as registry_file:
            json.dump(registry_data, registry_file)
            registry_path = Path(registry_file.name)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as schema_file:
            json.dump(schema_data, schema_file)
            schema_path = Path(schema_file.name)

        try:
            # Mock the schemas directory to contain our test files
            with (
                patch("n8n_lint.schemas.SCHEMAS_DIR", schema_path.parent),
                patch("n8n_lint.schemas.REGISTRY_FILE", registry_path),
            ):
                # Rename schema file to match registry
                test_schema_path = schema_path.parent / "test.json"
                schema_path.rename(test_schema_path)

                manager = SchemaManager()

                assert "test-node" in manager.schemas
                assert manager.schemas["test-node"] == schema_data
        finally:
            # Cleanup
            if registry_path.exists():
                registry_path.unlink()
            test_schema_path = schema_path.parent / "test.json"
            if test_schema_path.exists():
                test_schema_path.unlink()

    def test_get_schema_existing(self):
        """Test getting existing schema."""
        manager = SchemaManager()
        manager.schemas["test-node"] = {"type": "object"}

        schema = manager.get_schema("test-node")
        assert schema == {"type": "object"}

    def test_get_schema_nonexistent(self):
        """Test getting non-existent schema."""
        manager = SchemaManager()

        schema = manager.get_schema("nonexistent-node")
        assert schema is None

    def test_get_registry_entry_existing(self):
        """Test getting existing registry entry."""
        manager = SchemaManager()
        manager.registry = {"schemas": {"test-node": {"file": "test.json", "description": "Test node"}}}

        entry = manager.get_registry_entry("test-node")
        assert entry == {"file": "test.json", "description": "Test node"}

    def test_get_registry_entry_nonexistent(self):
        """Test getting non-existent registry entry."""
        manager = SchemaManager()

        entry = manager.get_registry_entry("nonexistent-node")
        assert entry is None

    def test_list_node_types(self):
        """Test listing node types."""
        manager = SchemaManager()
        manager.schemas = {"node1": {}, "node2": {}, "node3": {}}

        node_types = manager.list_node_types()
        assert set(node_types) == {"node1", "node2", "node3"}

    def test_validate_schema_valid(self):
        """Test schema validation with valid schema."""
        manager = SchemaManager()
        schema = {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}}}

        result = manager.validate_schema(schema)
        assert result is True

    def test_validate_schema_missing_type(self):
        """Test schema validation with missing type."""
        manager = SchemaManager()
        schema = {"properties": {"id": {"type": "string"}}}

        result = manager.validate_schema(schema)
        assert result is False

    def test_validate_schema_missing_properties(self):
        """Test schema validation with missing properties."""
        manager = SchemaManager()
        schema = {"type": "object"}

        result = manager.validate_schema(schema)
        assert result is False

    def test_import_schema_success(self):
        """Test successful schema import."""
        schema_data = {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}}}

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with patch("n8n_lint.schemas.SCHEMAS_DIR", temp_path):
                manager = SchemaManager()

                result = manager.import_schema("test-node", schema_data)

                assert result is True
                assert "test-node" in manager.schemas
                assert manager.schemas["test-node"] == schema_data

                # Check that file was created
                schema_file = temp_path / "test-node.json"
                assert schema_file.exists()

                with open(schema_file) as f:
                    saved_data = json.load(f)
                assert saved_data == schema_data

    def test_import_schema_invalid(self):
        """Test schema import with invalid schema."""
        manager = SchemaManager()
        invalid_schema = {
            "properties": {"id": {"type": "string"}}
            # Missing "type" field
        }

        result = manager.import_schema("test-node", invalid_schema)
        assert result is False

    def test_import_schema_io_error(self):
        """Test schema import with IO error."""
        schema_data = {"type": "object", "properties": {"id": {"type": "string"}}}

        # Mock SCHEMAS_DIR to a non-writable location
        with patch("n8n_lint.schemas.SCHEMAS_DIR", Path("/nonexistent/directory")):
            manager = SchemaManager()

            result = manager.import_schema("test-node", schema_data)
            assert result is False
