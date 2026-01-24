"""
Log Contract Module

This module defines the logging contract for the Starx system.
All components must adhere to this contract for consistent logging.
"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime


class LogContract:
    """Defines the logging contract for Starx components."""
    
    def __init__(self, component_name: str):
        """
        Initialize the log contract.
        
        Args:
            component_name: Name of the component using this contract
        """
        self.component_name = component_name
        self.logger = logging.getLogger(f"starx.{component_name}")
    
    def log_event(self, level: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Log an event with metadata.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Log message
            metadata: Optional metadata dictionary
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "component": self.component_name,
            "message": message,
            "metadata": metadata or {}
        }
        
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(f"{log_data}")
    
    def info(self, message: str, **kwargs):
        """Log info level message."""
        self.log_event("INFO", message, kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning level message."""
        self.log_event("WARNING", message, kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error level message."""
        self.log_event("ERROR", message, kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug level message."""
        self.log_event("DEBUG", message, kwargs)
