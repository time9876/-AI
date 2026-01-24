"""
Evidence Bundle Data Models

Defines the structure and types for evidence bundles.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional


@dataclass
class SystemInfo:
    """System information captured at bundle generation time."""
    hostname: str
    platform: str
    python_version: str
    timestamp: str


@dataclass
class ExecutionContext:
    """Execution context information."""
    command: str
    working_directory: str
    environment_vars: Dict[str, str] = field(default_factory=dict)
    arguments: List[str] = field(default_factory=list)


@dataclass
class ArtifactMetadata:
    """Metadata for captured artifacts."""
    artifact_type: str
    name: str
    size_bytes: int
    checksum: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class EvidenceBundle:
    """
    Evidence Bundle structure containing all captured data.
    
    An evidence bundle captures:
    - System information
    - Execution context
    - Runtime artifacts
    - Configuration snapshots
    - Metadata
    """
    bundle_id: str
    version: str
    created_at: str
    system_info: SystemInfo
    execution_context: ExecutionContext
    artifacts: List[ArtifactMetadata] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert evidence bundle to dictionary."""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convert evidence bundle to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save(self, filepath: str) -> None:
        """Save evidence bundle to file."""
        with open(filepath, 'w') as f:
            f.write(self.to_json())
