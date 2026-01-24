# Acceptance Evidence Documentation

This document provides evidence that the acceptance testing functionality works as intended.

## Test Execution Summary

### Success Scenario

**Command:** `python -m starx acceptance`

**Output:**
```
============================================================
Starx Acceptance Testing
============================================================

Running acceptance tests...

[TEST] required_files_exist
  ✓ PASSED
[TEST] cli_entrypoint_pattern
  ✓ PASSED
[TEST] config_schema_valid
  ✓ PASSED

All acceptance tests passed!

============================================================
ACCEPTANCE PASSED
============================================================
Total tests: 3
Passed: 3
Failed: 0
Evidence bundle saved to: .starx/evidence
```

**Exit Code:** 0 (Success)

### Failure Scenario

**Command:** `python -m starx acceptance` (with a required file temporarily removed)

**Output:**
```
============================================================
Starx Acceptance Testing
============================================================

Running acceptance tests...

[TEST] required_files_exist
  ✗ FAILED: Missing required files

============================================================
ACCEPTANCE FAILED
============================================================
Test: required_files_exist
Reason: Missing required files: docs/STARX_RUNTIME_SPEC.md
Evidence saved to: .starx/evidence_failure
```

**Exit Code:** 1 (Failure)

## Evidence Files

### Success Case
- `acceptance_report_latest.json` - Complete test results with all tests passing
- `test_logs_latest.log` - Detailed execution logs

### Failure Case (Example)
- `example_failure/` - Complete evidence bundle for a failed test run including:
  - `acceptance_report_*.json` - Test summary showing failure
  - `failure_*.json` - Detailed failure information
  - `diff_*.txt` - Minimal diff showing what failed
  - `test_logs_*.log` - Execution logs

## Verification of Requirements

### ✅ Single Entrypoint Pattern
All commands are accessible via `python -m starx`:
- `python -m starx run` - Execute workflow
- `python -m starx stats` - Display statistics
- `python -m starx acceptance` - Run acceptance tests

### ✅ Required Files Protected
The following files exist and are verified by acceptance tests:
- `docs/STARX_RUNTIME_SPEC.md`
- `starx/config/schema.yaml`
- `starx/core/logging/log_contract.py`

### ✅ Failure Detection and Reporting
When acceptance fails:
1. System immediately stops execution
2. Minimal diff is generated
3. Detailed failure reason is provided
4. Evidence bundle is saved
5. Non-zero exit code is returned

### ✅ Evidence Bundle Generation
Complete evidence bundles are automatically generated containing:
- JSON report with test results
- Detailed logs with timestamps
- Failure details and diffs (when applicable)
- Metadata about execution

## How to Reproduce

1. **Test Success Scenario:**
   ```bash
   python -m starx acceptance
   # Check .starx/evidence/ for evidence files
   ```

2. **Test Failure Scenario:**
   ```bash
   # Temporarily rename a required file
   mv docs/STARX_RUNTIME_SPEC.md docs/STARX_RUNTIME_SPEC.md.bak
   
   # Run acceptance tests
   python -m starx acceptance
   
   # Restore the file
   mv docs/STARX_RUNTIME_SPEC.md.bak docs/STARX_RUNTIME_SPEC.md
   ```

3. **View All Commands:**
   ```bash
   python -m starx --help
   python -m starx run
   python -m starx stats
   ```
