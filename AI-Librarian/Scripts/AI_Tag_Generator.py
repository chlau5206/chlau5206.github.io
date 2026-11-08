#!/usr/bin/env python3
"""  AI_Tag_Generator.py

Author: Charles H Lau

Summary
=======
Generate tags for Markdown notes using
category-aware keyword classification.

Features
========
- Processes Markdown (*.md) files only
- Reads YAML front matter
- Loads category rules from categories.yml
- Loads skip rules from ai_tag_skip.yml
- Preserves existing tags
- Respects excluded_tags
- Level-1 category classification
- Level-2 cross-category classification
- Whole-word matching
- Dry-run mode
- Single-file mode
- Recursive mode
- Summary statistics

Usage
=====
Process all notes:
    python AI_Tag_Generator.py --docs docs

Dry run:
    python AI_Tag_Generator.py \
        --docs docs \
        --dry-run

Single file:
    python AI_Tag_Generator.py \
        --docs docs \
        --file docs/Recipes/Beef_Bourguignon.md

Parameters
==========
Required
    --docs PATH

Optional
    --file FILE
    --dry-run
"""

import argparse
import re

from pathlib import Path

from lib.file_utils import (
    should_skip_file,
    load_skip_config,
)

from lib.markdown_utils import (
    read_markdown,
    load_categories,
)

from lib.metadata_utils import (
    parse_front_matter,
    rebuild_document,
    get_category,
    get_tags,
    get_excluded_tags,
    set_tags,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MAX_TAGS = 10
MAX_LEVEL1_TAGS = 7
MAX_LEVEL2_TAGS = 3

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def keyword_found(
    keyword: str,
    text: str
) -> bool:
    """
    Whole-word matching.
    """

    pattern = (
        rf"\b{re.escape(keyword.lower())}\b"
    )

    return (
        re.search(
            pattern,
            text.lower()
        )
        is not None
    )


def collect_text(
    md_file: Path,
    body: str
) -> str:
    """
    Build searchable text.
    """

    return " ".join(
        [
            md_file.stem,
            str(md_file.parent),
            body,
        ]
    )


def generate_tags(
    category: str,
    categories: dict,
    text: str,
):
    """
    Returns:

        level1_tags
        level2_tags
    """

    level1 = []
    level2 = []

    # ---------------------
    # Level 1
    # ---------------------

    own_rules = categories.get(
        category,
        {}
    )

    for keyword, tags in own_rules.items():

        if keyword_found(
            keyword,
            text
        ):

            for tag in tags:

                if tag not in level1:

                    level1.append(tag)

    # ---------------------
    # Level 2
    # ---------------------

    for cat_name, rules in categories.items():

        if cat_name == category:
            continue

        for keyword, tags in rules.items():

            if keyword_found(
                keyword,
                text
            ):

                for tag in tags:

                    if (
                        tag not in level1
                        and tag not in level2
                    ):
                        level2.append(tag)

    return (
        level1[:MAX_LEVEL1_TAGS],
        level2[:MAX_LEVEL2_TAGS]
    )


# ---------------------------------------------------------
# Process File
# ---------------------------------------------------------

def process_file(
    md_file: Path,
    docs_root: Path,
    categories: dict,
    skip_folders: set[str],
    skip_files: set[str],
    dry_run: bool,
):

    content = read_markdown(
        md_file
    )

    if not content:
        return None

    metadata, body = (
        parse_front_matter(content)
    )

    if not metadata:
        return "skipped"

    category = get_category(
        metadata
    )

    if not category:
        return "skipped"

    existing_tags = set(
        get_tags(metadata)
    )

    excluded_tags = set(
        get_excluded_tags(metadata)
    )

    searchable_text = collect_text(
        md_file,
        body
    )

    (
        level1_tags,
        level2_tags
    ) = generate_tags(
        category,
        categories,
        searchable_text
    )

    generated_tags = (
        level1_tags
        + level2_tags
    )

    final_tags = []

    # Existing tags first

    for tag in existing_tags:

        if tag not in excluded_tags:

            if tag not in final_tags:

                final_tags.append(tag)

    # Generated tags second

    for tag in generated_tags:

        if tag in excluded_tags:
            continue

        if tag not in final_tags:

            final_tags.append(tag)

    final_tags = (
        final_tags[:MAX_TAGS]
    )

    if set(final_tags) == existing_tags:

        return {
            "status": "skipped",
            "added": 0,
            "level1": 0,
            "level2": 0,
        }

    set_tags(
        metadata,
        final_tags
    )

    if dry_run:

        print("=" * 60)

        print(md_file)

        print(
            f"Category: {category}"
        )

        print(
            f"Existing : {sorted(existing_tags)}"
        )

        print(
            f"Excluded : {sorted(excluded_tags)}"
        )

        print(
            f"Level1   : {level1_tags}"
        )

        print(
            f"Level2   : {level2_tags}"
        )

        print(
            f"Final    : {final_tags}"
        )

    else:

        md_file.write_text(
            rebuild_document(
                metadata,
                body
            ),
            encoding="utf-8"
        )

    added_count = (
        len(set(final_tags))
        -
        len(existing_tags)
    )

    return {
        "status": "updated",
        "added": max(
            added_count,
            0
        ),
        "level1": len(level1_tags),
        "level2": len(level2_tags),
    }


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description=
        "AI Tag Generator"
    )

    parser.add_argument(
        "--docs",
        required=True,
        help="Docs root"
    )

    parser.add_argument(
        "--file",
        help=
        "Single file mode"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=
        "Preview only"
    )

    args = parser.parse_args()

    docs_root = Path(
        args.docs
    ).resolve()

    supporting_dir = (
        Path(__file__)
        .parent
        / "Supporting"
    )

    categories_file = (
        supporting_dir
        / "categories.yml"
    )

    skip_file = (
        supporting_dir
        / "ai_tag_skip.yml"
    )

    categories = (
        load_categories(
            categories_file
        )
    )

    (
        skip_folders,
        skip_files
    ) = load_skip_config(
        skip_file
    )

    scanned = 0
    updated = 0
    skipped = 0

    tags_added = 0

    level1_count = 0
    level2_count = 0

    if args.file:

        files = [
            Path(args.file)
        ]

    else:

        files = sorted(
            docs_root.rglob("*.md")
        )

    for md_file in files:

        if should_skip_file(
            md_file,
            docs_root,
            skip_folders,
            skip_files
        ):
            skipped += 1
            continue

        scanned += 1

        result = process_file(
            md_file,
            docs_root,
            categories,
            skip_folders,
            skip_files,
            args.dry_run
        )

        if not result:
            continue

        if result["status"] == "updated":

            updated += 1

            tags_added += (
                result["added"]
            )

            level1_count += (
                result["level1"]
            )

            level2_count += (
                result["level2"]
            )

        else:

            skipped += 1

    print()
    print("=" * 60)
    print("AI Tag Generator Summary")
    print("=" * 60)

    print(
        f"Scanned      : {scanned}"
    )

    print(
        f"Updated      : {updated}"
    )

    print(
        f"Skipped      : {skipped}"
    )

    print(
        f"Tags Added   : {tags_added}"
    )

    print(
        f"Level1 Tags  : {level1_count}"
    )

    print(
        f"Level2 Tags  : {level2_count}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()