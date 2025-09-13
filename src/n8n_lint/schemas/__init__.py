"""Schema management for n8n node validation."""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Schema directory path
SCHEMAS_DIR = Path(__file__).parent
REGISTRY_FILE = SCHEMAS_DIR / "registry.json"


class SchemaManager:
    """Manages n8n node schemas with registry-based metadata."""

    def __init__(self) -> None:
        self.registry: dict[str, Any] = {}
        self.schemas: dict[str, dict[str, Any]] = {}
        self._load_registry()
        self._load_schemas()

    def _load_registry(self) -> None:
        """Load schema registry metadata."""
        if REGISTRY_FILE.exists():
            try:
                with open(REGISTRY_FILE) as f:
                    self.registry = json.load(f)
                logger.debug(f"Loaded registry with {len(self.registry)} entries")
            except (OSError, json.JSONDecodeError):
                logger.exception("Failed to load registry")
                self.registry = {}
        else:
            logger.warning("Registry file not found, creating empty registry")
            self.registry = {}

    def _load_schemas(self) -> None:
        """Load all schema files from the schemas directory."""
        # Load schemas based on registry entries
        if "schemas" in self.registry:
            for node_type, registry_entry in self.registry["schemas"].items():
                schema_file = SCHEMAS_DIR / registry_entry["file"]
                if schema_file.exists():
                    try:
                        with open(schema_file) as f:
                            schema = json.load(f)
                        self.schemas[node_type] = schema
                        logger.debug(f"Loaded schema for node type: {node_type}")
                    except (OSError, json.JSONDecodeError):
                        logger.exception("Failed to load schema")

        # Fallback: load all JSON files in directory
        for schema_file in SCHEMAS_DIR.glob("*.json"):
            if schema_file.name == "registry.json":
                continue

            node_type = schema_file.stem
            if node_type not in self.schemas:  # Only load if not already loaded
                try:
                    with open(schema_file) as f:
                        schema = json.load(f)
                    self.schemas[node_type] = schema
                    logger.debug(f"Loaded schema for node type: {node_type}")
                except (OSError, json.JSONDecodeError):
                    logger.exception("Failed to load schema")

    def get_schema(self, node_type: str) -> dict[str, Any] | None:
        """Get schema for a specific node type."""
        return self.schemas.get(node_type)

    def get_registry_entry(self, node_type: str) -> dict[str, Any] | None:
        """Get registry metadata for a specific node type."""
        if "schemas" in self.registry:
            return self.registry["schemas"].get(node_type)
        return None

    def list_node_types(self) -> list[str]:
        """List all available node types."""
        return list(self.schemas.keys())

    def validate_schema(self, schema: dict[str, Any]) -> bool:
        """Validate that a schema has required fields."""
        required_fields = ["type", "properties"]
        return all(field in schema for field in required_fields)

    def import_schema(self, node_type: str, schema: dict[str, Any]) -> bool:
        """Import a new schema and update registry."""
        if not self.validate_schema(schema):
            logger.error(f"Invalid schema for node type: {node_type}")
            return False

        # Save schema file
        schema_file = SCHEMAS_DIR / f"{node_type}.json"
        try:
            with open(schema_file, "w") as f:
                json.dump(schema, f, indent=2)
            self.schemas[node_type] = schema
            logger.info(f"Imported schema for node type: {node_type}")
        except OSError:
            logger.exception("Failed to save schema")
            return False
        else:
            return True


# Global schema manager instance
schema_manager = SchemaManager()
