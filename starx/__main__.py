"""
Minimal entrypoint for starx to support acceptance evidence generation.

This file provides only a tiny glue layer to invoke the evidence generator when
called as: python -m starx acceptance --evidence-out <path> [--evidence-run-id <id>] [--notes "..."]

It intentionally does not implement the full project's CLI and keeps changes minimal.
"""
from __future__ import annotations

import sys

def _print_usage_and_exit() -> None:
    print("Usage: python -m starx <run|stats|acceptance> [options]", file=sys.stderr)
    sys.exit(2)

def _handle_acceptance(argv: list[str]) -> None:
    # minimal ad-hoc parsing; only supports a few flags as required
    evidence_out = None
    run_id = None
    include_env = True
    include_git = True
    include_tests = False
    notes = None

    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--evidence-out", "--evidence-outdir"):
            if i + 1 < len(argv):
                evidence_out = argv[i + 1]
                i += 2
                continue
            else:
                print("error: --evidence-out requires a path", file=sys.stderr)
                sys.exit(2)
        elif a == "--evidence-run-id":
            if i + 1 < len(argv):
                run_id = argv[i + 1]
                i += 2
                continue
            else:
                print("error: --evidence-run-id requires a value", file=sys.stderr)
                sys.exit(2)
        elif a == "--no-env":
            include_env = False
            i += 1
            continue
        elif a == "--no-git":
            include_git = False
            i += 1
            continue
        elif a == "--include-tests":
            include_tests = True
            i += 1
            continue
        elif a == "--notes":
            if i + 1 < len(argv):
                notes = argv[i + 1]
                i += 2
                continue
            else:
                print("error: --notes requires a value", file=sys.stderr)
                sys.exit(2)
        else:
            # unknown flag: skip it (allow existing acceptance flow to accept other flags)
            i += 1
            continue

    if not evidence_out:
        print("error: acceptance requires --evidence-out <path>", file=sys.stderr)
        sys.exit(2)

    try:
        from starx.tools.evidence import generate_evidence_bundle

        out_path = generate_evidence_bundle(
            out_dir=evidence_out,
            run_id=run_id,
            include_env=include_env,
            include_git=include_git,
            include_tests=include_tests,
            notes=notes,
        )
        print(f"evidence bundle created: {out_path}")
        sys.exit(0)
    except Exception as e:
        print(f"Acceptance evidence generation failed: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    if len(sys.argv) < 2:
        _print_usage_and_exit()

    cmd = sys.argv[1]
    if cmd == "acceptance":
        _handle_acceptance(sys.argv[2:])
    elif cmd in ("run", "stats"):
        # minimal placeholder to preserve single entrypoint semantics.
        print(f"Command '{cmd}' is not implemented in this minimal runtime.")
        sys.exit(0)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        _print_usage_and_exit()

if __name__ == "__main__":
    main()
