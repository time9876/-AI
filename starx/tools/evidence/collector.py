"""
Evidence Collector Utilities

Utilities for collecting system information and runtime data.
"""

import os
import sys
import platform
import socket
from datetime import datetime
from typing import Dict, List, Any

from .models import SystemInfo, ExecutionContext


class EvidenceCollector:
    """Collects various types of evidence data."""
    
    @staticmethod
    def collect_system_info() -> SystemInfo:
        """Collect system information."""
        return SystemInfo(
            hostname=socket.gethostname(),
            platform=f"{platform.system()} {platform.release()}",
            python_version=sys.version.split()[0],
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    @staticmethod
    def collect_execution_context(command: str = None, args: List[str] = None) -> ExecutionContext:
        """Collect execution context information."""
        if command is None:
            command = " ".join(sys.argv)
        
        if args is None:
            args = sys.argv[1:]
        
        # Collect only relevant environment variables (filter sensitive data)
        safe_env_vars = {
            k: v for k, v in os.environ.items()
            if k in ['PATH', 'HOME', 'USER', 'SHELL', 'PWD', 'LANG']
        }
        
        return ExecutionContext(
            command=command,
            working_directory=os.getcwd(),
            environment_vars=safe_env_vars,
            arguments=args
        )
    
    @staticmethod
    def collect_runtime_logs() -> List[str]:
        """Collect runtime logs."""
        # Placeholder for log collection
        return [
            f"[{datetime.utcnow().isoformat()}Z] Evidence bundle generation started",
            f"[{datetime.utcnow().isoformat()}Z] Collecting system information",
            f"[{datetime.utcnow().isoformat()}Z] Collecting execution context",
        ]
    
    @staticmethod
    def collect_metrics() -> Dict[str, Any]:
        """Collect runtime metrics."""
        import time
        return {
            "collection_timestamp": datetime.utcnow().isoformat() + "Z",
            "process_id": os.getpid(),
            "execution_time_ms": int(time.time() * 1000)
        }
