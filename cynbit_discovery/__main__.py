"""Run with python -m cynbit_discovery --text 'Your project brief'."""

import argparse
import json
from pathlib import Path

from .engine import DiscoveryEngine, render_markdown


def main():
    parser = argparse.ArgumentParser(description="Prepare a source-backed discovery brief.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Inquiry text; prefer --file for private input.")
    source.add_argument("--file", type=Path, help="UTF-8 text file containing an inquiry.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    try:
        text = args.file.read_text(encoding="utf-8") if args.file else args.text
        result = DiscoveryEngine().analyze(text)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2) if args.format == "json" else render_markdown(result))


if __name__ == "__main__":
    main()
