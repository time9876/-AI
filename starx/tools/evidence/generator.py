"""
Minimal evidence bundle generator.

API:
def generate_evidence_bundle(
    out_dir: str,
    run_id: str | None = None,
    include_env: bool = True,
    include_git: bool = True,
    include_tests: bool = False,
    notes: str | None = None
) -> str

Generates a directory under out_dir with minimal metadata files.
"""
from __future__ import annotations

import os
import sys
import json
import uuid
import socket
import platform
import subprocess
import datetime
from typing import Optional

def _safe_write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)

def _run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        return out.strip()
    except Exception:
        return None

def generate_evidence_bundle(
    out_dir: str,
    run_id: Optional[str] = None,
    include_env: bool = True,
    include_git: bool = True,
    include_tests: bool = False,
    notes: Optional[str] = None,
) -> str:
    """Create an evidence bundle directory under out_dir and populate minimal files.

    Returns the path to the created evidence bundle directory.

    Raises OSError if out_dir or the evidence dir cannot be created.
    """
    # Ensure out_dir exists or can be created
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        raise OSError(f"Cannot create or access out_dir '{out_dir}': {e}")

    # Create unique evidence directory
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    shortid = uuid.uuid4().hex[:8]
    base_name = f"evidence_{timestamp}_{shortid}"
    base_path = os.path.join(out_dir, base_name)
    try:
        os.makedirs(base_path, exist_ok=False)
    except Exception as e:
        raise OSError(f"Cannot create evidence bundle dir '{base_path}': {e}")

    # manifest.json
    manifest = {
        "timestamp_utc": timestamp,
        "run_id": run_id,
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
    }
    _safe_write_json(os.path.join(base_path, "manifest.json"), manifest)

    # env.json
    env_data = {"python_executable": sys.executable}
    if include_env:
        pip_freeze = _run_cmd([sys.executable, "-m", "pip", "freeze"])
        if pip_freeze is not None:
            env_data["pip_freeze"] = pip_freeze.splitlines()
        else:
            env_data["pip_freeze"] = None
    _safe_write_json(os.path.join(base_path, "env.json"), env_data)

    # git.json
    git_data = {}
    if include_git:
        commit = _run_cmd(["git", "rev-parse", "HEAD"]) or None
        branch = _run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or None
        status = _run_cmd(["git", "status", "--porcelain"]) or ""
        git_data["commit"] = commit
        git_data["branch"] = branch
        git_data["dirty"] = bool(status)
        git_data["status_lines"] = status.splitlines() if status else []
    else:
        git_data = {"included": False}
    _safe_write_json(os.path.join(base_path, "git.json"), git_data)

    # optional notes
    if notes:
        with open(os.path.join(base_path, "notes.txt"), "w", encoding="utf-8") as fh:
            fh.write(notes)

    # logs/ and reports/
    logs_dir = os.path.join(base_path, "logs")
    reports_dir = os.path.join(base_path, "reports")
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    return base_path
