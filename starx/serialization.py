"""JSON serialization helpers for Starx dataclass models."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
import json
from typing import Any


def to_json_data(value: Any) -> Any:
    """Convert dataclass-backed values into JSON-compatible data."""
    if is_dataclass(value) and not isinstance(value, type):
        return to_json_data(asdict(value))
    if isinstance(value, dict):
        return {str(key): to_json_data(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_json_data(item) for item in value]
    return value


def to_json(value: Any) -> str:
    """Serialize a value to canonical JSON with deterministic key ordering."""
    return json.dumps(to_json_data(value), sort_keys=True, separators=(",", ":"))
