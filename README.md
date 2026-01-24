# Starx Workbench

A project workflow management system with automated acceptance testing and evidence generation capabilities.

## Overview

Starx provides a unified CLI interface for managing project workflows, generating statistics, and running acceptance tests with automatic evidence bundle generation.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt  # or pip install PyYAML>=5.4
```

## Usage

Starx provides a single entrypoint pattern with three commands:

### Run Workflow
Execute the main project workflow:
```bash
python -m starx run
```

### Display Statistics
Show project statistics and verify required files:
```bash
python -m starx stats
```

### Run Acceptance Tests
Run acceptance tests and generate evidence bundle:
```bash
python -m starx acceptance
```

You can specify a custom output directory for evidence:
```bash
python -m starx acceptance --output-dir=/path/to/evidence
```

## Features

- **Single Entrypoint**: All commands accessible via `python -m starx`
- **Acceptance Testing**: Automated validation of project requirements
- **Evidence Generation**: Comprehensive evidence bundles with JSON reports and logs
- **Failure Detection**: Immediate stop and detailed reporting on test failures
- **Minimal Diffs**: Clear reporting of what failed and why

## Evidence Bundle

When acceptance tests run, the system generates:

- `acceptance_report_<timestamp>.json` - Complete test results
- `test_logs_<timestamp>.log` - Detailed test execution logs
- `failure_<test>_<timestamp>.json` - Individual failure details (on failure)
- `diff_<test>_<timestamp>.txt` - Minimal diff information (on failure)

## Required Files

The following files are critical and must not be deleted or renamed:

- `docs/STARX_RUNTIME_SPEC.md` - Runtime specification
- `starx/config/schema.yaml` - Configuration schema
- `starx/core/logging/log_contract.py` - Logging contract

## Architecture

See `docs/STARX_RUNTIME_SPEC.md` for detailed architecture and runtime specification.