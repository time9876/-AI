# Starx Runtime Specification

## Overview

Starx is a project workflow management system that provides automated acceptance testing and evidence generation capabilities.

## Architecture

### Core Components

1. **CLI Interface** - Single entrypoint pattern via `python -m starx`
2. **Runtime Engine** - Executes workflow commands
3. **Acceptance Framework** - Validates project acceptance criteria
4. **Evidence Generator** - Creates evidence bundles for acceptance validation

### Command Interface

Starx provides three main commands:

```bash
python -m starx run       # Execute main workflow
python -m starx stats     # Display project statistics  
python -m starx acceptance # Run acceptance tests and generate evidence
```

## Acceptance Testing

### Purpose

The acceptance testing framework validates that all project requirements are met and generates evidence bundles to demonstrate compliance.

### Evidence Bundle

When acceptance tests run, the system generates a comprehensive evidence bundle containing:

- Test execution logs
- Pass/fail status for each criterion
- Detailed failure reasons and minimal diffs
- Metadata about the test execution
- Timestamps and environment information

### Failure Handling

When acceptance tests fail:

1. The system immediately stops execution
2. A minimal diff is generated showing the discrepancy
3. A detailed failure reason is provided
4. No workarounds are attempted
5. The evidence bundle is saved with failure details

### Evidence Output

Evidence bundles are saved to `.starx/evidence/` directory with the following structure:

```
.starx/evidence/
  ├── acceptance_report_<timestamp>.json
  ├── test_logs_<timestamp>.log
  └── diffs/
      └── <test_name>_<timestamp>.diff
```

## Configuration

All runtime configuration is defined in `starx/config/schema.yaml`. See that file for available options.

## Logging

Logging follows the contract defined in `starx/core/logging/log_contract.py`. All components must use the LogContract class for consistent logging behavior.

## Required Files

The following files are critical to the system and must not be deleted or renamed:

- `docs/STARX_RUNTIME_SPEC.md` - This specification document
- `starx/config/schema.yaml` - Configuration schema
- `starx/core/logging/log_contract.py` - Logging contract definition
