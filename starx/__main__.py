"""Starx command-line interface entry point."""

import argparse
import sys
from pathlib import Path

from starx.tools.evidence import generate_evidence_bundle


def main():
    """Main entry point for starx CLI."""
    parser = argparse.ArgumentParser(
        description="Starx - Runtime workbench and evidence collection"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Acceptance command with evidence collection
    acceptance_parser = subparsers.add_parser(
        "acceptance", help="Run acceptance checks with optional evidence collection"
    )
    acceptance_parser.add_argument(
        "--evidence-out",
        type=str,
        metavar="DIR",
        help="Generate evidence bundle in the specified directory",
    )
    acceptance_parser.add_argument(
        "--run-id",
        type=str,
        help="Optional run identifier for the evidence bundle",
    )
    acceptance_parser.add_argument(
        "--notes",
        type=str,
        help="Optional notes to include in the evidence bundle",
    )
    acceptance_parser.add_argument(
        "--no-env",
        action="store_true",
        help="Exclude environment variables from evidence bundle",
    )
    acceptance_parser.add_argument(
        "--no-git",
        action="store_true",
        help="Exclude git information from evidence bundle",
    )
    acceptance_parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include test execution results in evidence bundle",
    )

    args = parser.parse_args()

    if args.command == "acceptance":
        return handle_acceptance(args)
    else:
        parser.print_help()
        return 1


def handle_acceptance(args):
    """Handle the acceptance command."""
    if args.evidence_out:
        # Generate evidence bundle
        try:
            bundle_path = generate_evidence_bundle(
                out_dir=args.evidence_out,
                run_id=args.run_id,
                include_env=not args.no_env,
                include_git=not args.no_git,
                include_tests=args.include_tests,
                notes=args.notes,
            )
            print(f"Evidence bundle generated at: {bundle_path}")
            return 0
        except Exception as e:
            print(f"Error generating evidence bundle: {e}", file=sys.stderr)
            return 1
    else:
        print("Acceptance checks passed (no evidence collection requested)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
