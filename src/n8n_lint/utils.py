"""Utility functions for n8n-lint."""

import json
from pathlib import Path
from typing import Any


def load_json_file(file_path: Path) -> dict[str, Any] | None:
    """Load and parse a JSON file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def save_json_file(data: dict[str, Any], file_path: Path) -> bool:
    """Save data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        return False
    else:
        return True


def format_error_message(
    message: str, node_type: str | None = None, property_path: str | None = None, line_number: int | None = None
) -> str:
    """Format an error message with context."""
    parts = [message]

    if node_type:
        parts.append(f"Node: {node_type}")

    if property_path:
        parts.append(f"Property: {property_path}")

    if line_number:
        parts.append(f"Line: {line_number}")

    return " | ".join(parts)
