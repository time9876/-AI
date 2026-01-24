"""Evidence bundle generator for starx runtime."""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional


def generate_evidence_bundle(
    out_dir: str,
    run_id: Optional[str] = None,
    include_env: bool = True,
    include_git: bool = True,
    include_tests: bool = False,
    notes: Optional[str] = None,
) -> str:
    """
    Generate an evidence bundle capturing runtime context and metadata.

    Args:
        out_dir: Base output directory for the evidence bundle
        run_id: Optional run identifier (auto-generated if not provided)
        include_env: Whether to include environment variables
        include_git: Whether to include git repository information
        include_tests: Whether to include test execution results
        notes: Optional free-form notes to include in the bundle

    Returns:
        Path to the generated evidence bundle directory
    """
    # Generate run_id if not provided
    if run_id is None:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create output directory
    bundle_dir = Path(out_dir) / f"evidence_{run_id}"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Initialize evidence data
    evidence = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "notes": notes,
    }

    # Collect environment information
    if include_env:
        evidence["environment"] = {
            "platform": _get_platform_info(),
            "python_version": _get_python_version(),
            "env_vars": dict(os.environ) if include_env else {},
        }

    # Collect git information
    if include_git:
        evidence["git"] = _collect_git_info()

    # Collect test information (placeholder for future implementation)
    if include_tests:
        evidence["tests"] = {"status": "not_implemented"}

    # Write evidence bundle
    manifest_path = bundle_dir / "evidence_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(evidence, f, indent=2)

    return str(bundle_dir)


def _get_platform_info() -> dict:
    """Get platform information."""
    import platform

    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
    }


def _get_python_version() -> str:
    """Get Python version."""
    import sys

    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def _collect_git_info() -> dict:
    """Collect git repository information."""
    git_info = {}

    try:
        # Get current branch
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        git_info["branch"] = result.stdout.strip()

        # Get current commit
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        git_info["commit"] = result.stdout.strip()

        # Get commit message
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"],
            capture_output=True,
            text=True,
            check=True,
        )
        git_info["commit_message"] = result.stdout.strip()

        # Get status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        git_info["dirty"] = bool(result.stdout.strip())

    except (subprocess.CalledProcessError, FileNotFoundError):
        git_info["error"] = "Git information not available"

    return git_info
