"""
Starx - Evidence Bundle Generation CLI

Main entry point for the Starx evidence bundle generation tool.
"""

import sys
import argparse
from pathlib import Path

from starx.tools.evidence import EvidenceBundleGenerator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="starx",
        description="Starx Evidence Bundle Generation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--generate-evidence",
        action="store_true",
        help="Generate an evidence bundle"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./evidence_bundles",
        help="Output directory for evidence bundles (default: ./evidence_bundles)"
    )
    
    parser.add_argument(
        "--metadata",
        type=str,
        help="Additional metadata as key=value pairs (comma-separated)"
    )
    
    args = parser.parse_args()
    
    if args.generate_evidence:
        # Parse metadata if provided
        metadata = {}
        if args.metadata:
            for pair in args.metadata.split(','):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    metadata[key.strip()] = value.strip()
        
        # Generate evidence bundle
        generator = EvidenceBundleGenerator(output_dir=args.output_dir)
        bundle, filepath = generator.generate_and_save(
            command=" ".join(sys.argv),
            metadata=metadata
        )
        
        print(f"✓ Evidence bundle generated successfully!")
        print(f"  Bundle ID: {bundle.bundle_id}")
        print(f"  Saved to: {filepath}")
        print(f"\nBundle Summary:")
        print(f"  - System: {bundle.system_info.platform}")
        print(f"  - Python: {bundle.system_info.python_version}")
        print(f"  - Artifacts: {len(bundle.artifacts)}")
        print(f"  - Logs: {len(bundle.logs)} entries")
        
        return 0
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
