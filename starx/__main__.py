"""
Main entrypoint for Starx CLI.

Usage:
    python -m starx run        # Execute main workflow
    python -m starx stats      # Display project statistics
    python -m starx acceptance # Run acceptance tests and generate evidence
"""

import sys
import argparse
from starx.cli import run_command, stats_command, acceptance_command


def main():
    """Main entrypoint for Starx CLI."""
    parser = argparse.ArgumentParser(
        description="Starx Workbench - Project Workflow Management System",
        prog="python -m starx"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Execute the main workflow")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Display project statistics")
    
    # Acceptance command
    acceptance_parser = subparsers.add_parser(
        "acceptance",
        help="Run acceptance tests and generate evidence bundle"
    )
    acceptance_parser.add_argument(
        "--output-dir",
        default=".starx/evidence",
        help="Directory to save evidence bundle (default: .starx/evidence)"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute the requested command
    if args.command == "run":
        return run_command()
    elif args.command == "stats":
        return stats_command()
    elif args.command == "acceptance":
        return acceptance_command(args.output_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
