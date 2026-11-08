### metadata_classifier.py  11/2/2026
#!/usr/bin/env python3

"""
metadata_classifier.py

Author: Charles H Lau

MkDocs Metadata Auto Classifier

Automatically adds YAML front matter metadata to Markdown files
within a MkDocs documentation repository.

Features:
- Processes Markdown (*.md) files only
- Skips index.md files
- Skips files that already contain YAML front matter
- Generates titles from filenames
- Derives category from the first-level folder
- Generates tags from the folder hierarchy
- Populates created and updated dates from file timestamps
- Supports single-file or recursive processing
- Provides a dry-run mode for safe previewing

Generated Metadata:
    title      Human-readable title from filename
    category   First folder under docs root
    tags       Folder hierarchy as tag list
    status     Default value: completed
    created    File creation date
    updated    File last modified date

Typical Workflow:
    1. Import or reorganize notes.
    2. Run with --dry-run to review changes.
    3. Run without --dry-run to apply metadata.
    4. Commit changes to Git.

Use Case:
    Part of the Personal AI Librarian / Knowledge Management
    workflow for MkDocs, Obsidian, and AI-assisted note
    organization.
"""

import argparse
from pathlib import Path
from datetime import datetime

from lib.file_utils import * 
from lib.metadata_utils import *

# ---------------------------------------------------------
# Skip Rules
# ---------------------------------------------------------

DEFAULT_SKIP_FOLDERS = frozenset({
    "Reports",
    "Archive"
})

DEFAULT_SKIP_FILES = frozenset({
    "index.md",
    "README.md"
})


# ---------------------------------------------------------
# Metadata Builder
# ---------------------------------------------------------

def build_metadata(
    md_file: Path,
    docs_root: Path
) -> str:

    rel_path = md_file.relative_to(docs_root)

    folders = list(rel_path.parts[:-1])

    category = folders[0] if folders else "general"

    tags = folders

    title = title_from_filename(md_file.name)

    stat = md_file.stat()

    try:
        created = datetime.fromtimestamp(stat.st_ctime)
    except Exception:
        created = datetime.today()

    updated = datetime.fromtimestamp(stat.st_mtime)

    created_str = created.strftime("%Y-%m-%d")
    updated_str = updated.strftime("%Y-%m-%d")

    tag_lines = "\n".join(
        f"  - {tag}"
        for tag in tags
    )

    metadata = f"""---
title: {title}
category: {category}
tags:
{tag_lines}
status: completed
created: {created_str}
updated: {updated_str}
---
"""

    return metadata


# ---------------------------------------------------------
# File Processing
# ---------------------------------------------------------

def process_file(
    md_file: Path,
    docs_root: Path,
    dry_run: bool,
):

    if md_file.suffix.lower() != ".md":
        return

    if should_skip_file(  md_file, 
                          docs_root,
                          skip_files=DEFAULT_SKIP_FILES,
                          skip_folders=DEFAULT_SKIP_FOLDERS):
        return

    # if md_file.name.lower() == "index.md":
    #     print(f"SKIP (index): {md_file}")
    #     return

    content = md_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    if has_front_matter(content):
        print(f"SKIP (metadata exists): {md_file}")
        return

    metadata = build_metadata(
        md_file,
        docs_root
    )

    if dry_run:

        print("=" * 60)
        print(md_file)
        print(metadata)

        return

    md_file.write_text(
        metadata + content,
        encoding="utf-8"
    )

    print(f"UPDATED: {md_file}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="MkDocs Metadata Auto Classifier"
    )

    parser.add_argument(
        "--docs",
        required=True,
        help="Path to docs root"
    )

    parser.add_argument(
        "--file",
        help="Process a single file"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes only"
    )

    args = parser.parse_args()

    docs_root = Path(args.docs).resolve()

    # Single file mode

    if args.file:

        process_file(
            Path(args.file).resolve(),
            docs_root,
            args.dry_run
        )

        return

    # Recursive mode

    for md_file in docs_root.rglob("*.md"):

        new_name = normalize_filename(
            md_file.name
        )

        if new_name != md_file.name:

            new_path = md_file.with_name(
                new_name
            )

            print(
                f"RENAME: "
                f"{md_file.name} -> {new_name}"
            )

            if not args.dry_run:
                md_file.rename(new_path)

            md_file = new_path

        process_file(
            md_file,
            docs_root,
            args.dry_run
        )


if __name__ == "__main__":
    main()