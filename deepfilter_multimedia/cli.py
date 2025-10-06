"""Command-line interface for deepfilter-multimedia."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from deepfilter_multimedia import __version__
from deepfilter_multimedia.core import process_file


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="dfm",
        description="DeepFilter Multimedia - Remove noise from audio and video files using DeepFilterNet",
        epilog="Based on DeepFilterNet: https://github.com/Rikorose/DeepFilterNet"
    )

    parser.add_argument(
        "input",
        type=str,
        nargs="+",
        help="Input audio or video file(s) to process"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file path (only valid for single input file). "
             "If not specified, saves to 'output/<filename>_enhanced.<ext>'"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output (default: enabled)"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Disable progress messages"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    return parser


def validate_args(args: argparse.Namespace) -> None:
    """
    Validate command-line arguments.

    Args:
        args: Parsed arguments

    Raises:
        ValueError: If arguments are invalid
    """
    if len(args.input) > 1 and args.output is not None:
        raise ValueError(
            "Cannot specify --output when processing multiple files. "
            "Files will be saved to 'output/' directory."
        )

    for input_file in args.input:
        if not Path(input_file).exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Determine verbosity
    verbose = not args.quiet if args.quiet else True

    try:
        # Validate arguments
        validate_args(args)

        # Process each input file
        for i, input_file in enumerate(args.input):
            if len(args.input) > 1 and verbose:
                print(f"\n[{i+1}/{len(args.input)}] Processing {input_file}")

            output_file = args.output if len(args.input) == 1 else None
            result = process_file(input_file, output_file, verbose=verbose)

            if verbose:
                print(f"✓ Saved to: {result}\n")

        if verbose and len(args.input) > 1:
            print(f"✓ Successfully processed {len(args.input)} file(s)")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        parser.print_help()
        return 1
    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
