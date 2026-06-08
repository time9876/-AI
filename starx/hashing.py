"""Stable hashing utilities."""

from __future__ import annotations

import hashlib
from typing import Any

from .serialization import to_json


def stable_hash(value: Any) -> str:
    """Return a deterministic SHA-256 hash for a JSON-serializable value."""
    payload = to_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
