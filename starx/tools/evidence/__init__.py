"""
Evidence Bundle Generation Module

This module provides functionality for generating evidence bundles
that capture runtime artifacts, configuration, and execution context.
"""

from .generator import EvidenceBundleGenerator
from .models import EvidenceBundle

__all__ = ["EvidenceBundleGenerator", "EvidenceBundle"]
