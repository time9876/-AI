"""Core dataclass models for Starx MVS-1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .hashing import stable_hash
from .serialization import to_json, to_json_data


@dataclass(frozen=True)
class EvidenceItem:
    """A small immutable record for subject-related evidence."""

    source: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_json_data(self) -> dict[str, Any]:
        """Return a JSON-compatible representation of the evidence item."""
        return to_json_data(self)

    def to_json(self) -> str:
        """Serialize the evidence item to canonical JSON."""
        return to_json(self)

    def stable_hash(self) -> str:
        """Return the stable hash of the evidence item."""
        return stable_hash(self)


@dataclass(frozen=True)
class SubjectState:
    """Initial subject state container for Starx MVS-1."""

    subject_id: str
    label: str = ""
    evidence: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    attributes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def initial(cls, subject_id: str, label: str = "") -> "SubjectState":
        """Create an empty initial state for a subject."""
        return cls(subject_id=subject_id, label=label)

    def to_json_data(self) -> dict[str, Any]:
        """Return a JSON-compatible representation of the subject state."""
        return to_json_data(self)

    def to_json(self) -> str:
        """Serialize the subject state to canonical JSON."""
        return to_json(self)

    def stable_hash(self) -> str:
        """Return the stable hash of the subject state."""
        return stable_hash(self)
