# Starx Workbench

Evidence Bundle Generation Framework

## Overview

Starx is a framework for generating evidence bundles that capture runtime artifacts, system information, execution context, and metadata. Evidence bundles are useful for compliance, auditing, debugging, and forensic analysis.

## Features

- **System Information Capture**: Automatically collects hostname, platform, and Python version
- **Execution Context**: Records command invocation, working directory, and relevant environment variables
- **Artifact Collection**: Catalogs files and artifacts in the workspace
- **Runtime Logs**: Captures execution timeline and events
- **Metrics Collection**: Records timing and process information
- **Custom Metadata**: Supports adding custom key-value metadata to bundles

## Installation

```bash
pip install -e .
```

## Usage

### Generate an Evidence Bundle

```bash
python -m starx --generate-evidence
```

### Specify Output Directory

```bash
python -m starx --generate-evidence --output-dir /path/to/output
```

### Add Custom Metadata

```bash
python -m starx --generate-evidence --metadata "task=TASK-0001,purpose=demo"
```

## Evidence Bundle Structure

Evidence bundles are saved as JSON files with the following structure:

```json
{
  "bundle_id": "unique-uuid",
  "version": "1.0.0",
  "created_at": "ISO-8601 timestamp",
  "system_info": {
    "hostname": "...",
    "platform": "...",
    "python_version": "..."
  },
  "execution_context": {
    "command": "...",
    "working_directory": "...",
    "environment_vars": {...},
    "arguments": [...]
  },
  "artifacts": [...],
  "logs": [...],
  "metrics": {...},
  "metadata": {...}
}
```

## Project Structure

```
starx/
├── __init__.py
├── __main__.py              # CLI entry point (minimal glue code)
└── tools/
    └── evidence/            # Evidence bundle implementation
        ├── __init__.py
        ├── models.py        # Data models for evidence bundles
        ├── collector.py     # Utilities for collecting evidence
        └── generator.py     # Main generator logic
```

## Development

The project follows a minimal implementation approach:
- Core evidence generation logic is isolated in `starx/tools/evidence/`
- CLI glue code is minimal and contained in `starx/__main__.py`
- No external dependencies required (uses only Python standard library)

## License

See repository license.