"""
Evidence Bundle Generator

Main component for generating evidence bundles.
"""

import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from .models import EvidenceBundle, ArtifactMetadata
from .collector import EvidenceCollector


class EvidenceBundleGenerator:
    """
    Generator for creating evidence bundles.
    
    Evidence bundles capture comprehensive information about system state,
    execution context, and runtime artifacts.
    """
    
    VERSION = "1.0.0"
    
    def __init__(self, output_dir: str = None):
        """
        Initialize the evidence bundle generator.
        
        Args:
            output_dir: Directory where evidence bundles will be saved.
                       Defaults to './evidence_bundles'
        """
        self.output_dir = output_dir or "./evidence_bundles"
        self.collector = EvidenceCollector()
    
    def generate(self, 
                 command: str = None,
                 metadata: Dict[str, Any] = None,
                 collect_artifacts: bool = True) -> EvidenceBundle:
        """
        Generate a new evidence bundle.
        
        Args:
            command: Command string to record in execution context
            metadata: Additional metadata to include in the bundle
            collect_artifacts: Whether to collect artifact information
            
        Returns:
            EvidenceBundle: The generated evidence bundle
        """
        # Generate unique bundle ID
        bundle_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat() + "Z"
        
        # Collect system information
        system_info = self.collector.collect_system_info()
        
        # Collect execution context
        execution_context = self.collector.collect_execution_context(command=command)
        
        # Collect runtime logs
        logs = self.collector.collect_runtime_logs()
        
        # Collect metrics
        metrics = self.collector.collect_metrics()
        
        # Collect artifacts if requested
        artifacts = []
        if collect_artifacts:
            artifacts = self._collect_artifacts()
        
        # Build evidence bundle
        bundle = EvidenceBundle(
            bundle_id=bundle_id,
            version=self.VERSION,
            created_at=created_at,
            system_info=system_info,
            execution_context=execution_context,
            artifacts=artifacts,
            logs=logs,
            metrics=metrics,
            metadata=metadata or {}
        )
        
        return bundle
    
    def generate_and_save(self,
                         command: str = None,
                         metadata: Dict[str, Any] = None,
                         filename: str = None) -> tuple[EvidenceBundle, str]:
        """
        Generate an evidence bundle and save it to disk.
        
        Args:
            command: Command string to record
            metadata: Additional metadata
            filename: Optional filename (defaults to bundle_id.json)
            
        Returns:
            Tuple of (EvidenceBundle, filepath)
        """
        # Generate bundle
        bundle = self.generate(command=command, metadata=metadata)
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Determine filename
        if filename is None:
            filename = f"{bundle.bundle_id}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Save bundle
        bundle.save(filepath)
        
        return bundle, filepath
    
    def _collect_artifacts(self) -> list[ArtifactMetadata]:
        """Collect information about artifacts in the current directory."""
        artifacts = []
        
        # Collect basic file information from current directory
        try:
            cwd = os.getcwd()
            for item in os.listdir(cwd)[:10]:  # Limit to first 10 items
                item_path = os.path.join(cwd, item)
                if os.path.isfile(item_path):
                    stat = os.stat(item_path)
                    artifacts.append(ArtifactMetadata(
                        artifact_type="file",
                        name=item,
                        size_bytes=stat.st_size,
                        created_at=datetime.fromtimestamp(stat.st_ctime).isoformat() + "Z"
                    ))
        except Exception:
            # Silently skip if we can't read directory
            pass
        
        return artifacts
