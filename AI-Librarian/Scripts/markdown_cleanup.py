#!/usr/bin/env python3
""" Markdown_Cleanup.py

Fix imported markdown files that render differently in MkDocs.

Converts recipe-style sections so MkDocs preserves line breaks.

Example:
    材料:
    牛奶 100克
    雞蛋 2個

becomes
    材料:
    牛奶 100克··
    雞蛋 2個··

(where ·· = two spaces)

Usage:
    python Markdown_Cleanup.py
    python Markdown_Cleanup.py --dry-run
    python Markdown_Cleanup.py --docs docs
"""

from pathlib import Path
import argparse

from lib.file_utils import (
    load_skip_config,
    get_markdown_files,
    load_yaml_config,
)
from lib.markdown_utils import (
    read_markdown,
    write_markdown,
)

def fix_content(text: str) -> str:

    lines = text.splitlines()

    output = []

    inside_section = False

    for line in lines:

        stripped = line.strip()
        cleanup_rule_file = (
            Path(__file__).parent
            / "Supporting"
            / "cleanup_rule.yml"
        )
        SECTION_HEADERS = load_yaml_config(cleanup_rule_file)
        if  stripped in  SECTION_HEADERS:
            inside_section = True
            output.append(line)

            continue

        if stripped == "":

            inside_section = False
            output.append(line)

            continue

        if inside_section:

            if line.endswith("  "):
                output.append(line)
            else:
                output.append(
                    line.rstrip() + "  "
                )

        else:

            output.append(line)

    return "\n".join(output)


def process_file(
    md_file: Path,
    dry_run: bool
) -> bool:

    original = md_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    original = read_markdown(
        md_file
    )

    updated = fix_content(
        original
    )

    if original == updated:
        return False

    print(
        f"FIXED: {md_file}"
    )

    if not dry_run:

        write_markdown(
            md_file,
            updated
        )

    return True

def main():

    parser = argparse.ArgumentParser(
        description="Markdown cleanup utility"
    )

    parser.add_argument(
        "--docs", "-s",
        default="docs",
        # required=True,
        help="Docs root directory"
    )

    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Preview changes only"
    )

    args = parser.parse_args()

    docs_root = Path(
        args.docs
    )

    config_file = (
        Path(__file__).parent
        / "Supporting"
        / "skip_config.yml"
    )

    (
        skip_folders,
        skip_files
    ) = load_skip_config(
        config_file
    )

    md_files = get_markdown_files(
        docs_root,
        skip_folders,
        skip_files
    )

    modified = 0

    for md_file in md_files:

        if process_file(
            md_file,
            args.dry_run
        ):
            modified += 1

    print()
    print("=" * 60)
    print(
        f"Modified Files: {modified}"
    )
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
