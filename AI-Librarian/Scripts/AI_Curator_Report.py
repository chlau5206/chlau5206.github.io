#!/usr/bin/env python3
"""  AI_Curator_Report.py

Author: Charles H Lau

Personal AI Librarian - Vault Intelligence Report

Analyzes a Markdown knowledge base and generates
curation recommendations.

Features
--------
- Counts notes by category
- Detects sparse categories
- Detects untagged notes
- Detects low-tag notes
- Detects stale notes
- Detects large notes
- Detects empty notes
- Summarizes vault statistics
- Generates Markdown report

Output
------
Reports/AI_Curator_Report.md

Typical Workflow
----------------
Metadata_Classifier.py
        ↓
AI_Tag_Generator.py
        ↓
Duplicate_Detector.py
        ↓
AI_Curator_Report.py
        ↓
Note_Health_Report.py
        ↓
Git Commit / Push
"""

import argparse
import re

from collections import Counter
from datetime import datetime
from pathlib import Path
from lib.file_utils import *

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DEFAULT_SKIP_FOLDERS = frozenset({
    "Reports",
    "Archive"
})

DEFAULT_SKIP_FILES = frozenset({
    "index.md",
    "README.md"
})

STALE_DAYS = 365
LOW_TAG_THRESHOLD = 3
LARGE_NOTE_LINES = 500


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

# def should_skip_file(
#     md_file: Path,
#     docs_root: Path,
#     skip_folders=DEFAULT_SKIP_FOLDERS,
#     skip_files=DEFAULT_SKIP_FILES
# ) -> bool:

#     rel_path = md_file.relative_to(docs_root)

#     if md_file.name.lower() in {
#         x.lower()
#         for x in skip_files
#     }:
#         return True

#     for folder in rel_path.parts[:-1]:

#         if folder in skip_folders:
#             return True

#     return False


def extract_front_matter(
    content: str
):

    if not content.startswith("---"):
        return None, content

    match = re.match(
        r"^---\n(.*?)\n---\n?",
        content,
        re.DOTALL
    )

    if not match:
        return None, content

    return (
        match.group(1),
        content[match.end():]
    )


def extract_category(
    yaml_block: str
) -> str:

    match = re.search(
        r"^category:\s*(.*)$",
        yaml_block,
        re.MULTILINE
    )

    if not match:
        return "unknown"

    return match.group(1).strip()


def extract_tags(
    yaml_block: str
) -> list[str]:

    tags = []

    lines = yaml_block.splitlines()

    in_tags = False

    for line in lines:

        if line.strip() == "tags:":
            in_tags = True
            continue

        if in_tags:

            if line.startswith("  - "):
                tags.append(
                    line[4:].strip()
                )
            else:
                break

    return tags


# ---------------------------------------------------------
# Analyzer
# ---------------------------------------------------------

def analyze_vault(
    docs_root: Path
):

    report = {
        "total_notes": 0,
        "categories": Counter(),
        "no_tags": [],
        "low_tags": [],
        "empty_notes": [],
        "large_notes": [],
        "stale_notes": [],
    }

    now = datetime.now()

    for md_file in docs_root.rglob("*.md"):

        if should_skip_file(
            md_file,
            docs_root
        ):
            continue

        report["total_notes"] += 1

        try:
            content = md_file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except Exception:
            continue

        yaml_block, body = extract_front_matter(
            content
        )

        if yaml_block:

            category = extract_category(
                yaml_block
            )

            report["categories"][category] += 1

            tags = extract_tags(
                yaml_block
            )

            if len(tags) == 0:
                report["no_tags"].append(
                    md_file
                )

            elif len(tags) < LOW_TAG_THRESHOLD:
                report["low_tags"].append(
                    (
                        md_file,
                        len(tags)
                    )
                )

        stripped_body = body.strip()

        if len(stripped_body) < 20:

            report["empty_notes"].append(
                md_file
            )

        lines = body.count("\n")

        if lines > LARGE_NOTE_LINES:

            report["large_notes"].append(
                (
                    md_file,
                    lines
                )
            )

        age_days = (
            now
            - datetime.fromtimestamp(
                md_file.stat().st_mtime
            )
        ).days

        if age_days > STALE_DAYS:

            report["stale_notes"].append(
                (
                    md_file,
                    age_days
                )
            )

    return report


# ---------------------------------------------------------
# Report Writer
# ---------------------------------------------------------

def write_report(
    report,
    report_file: Path
):

    sparse_categories = []

    for category, count in sorted(
        report["categories"].items()
    ):
        if count < 5:
            sparse_categories.append(
                (category, count)
            )

    output = []

    output.append(
        "# AI Curator Report\n"
    )

    output.append(
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
    )

    output.append(
        f"Total Notes: {report['total_notes']}\n"
    )

    output.append(
        "## Categories\n"
    )

    for category, count in sorted(
        report["categories"].items()
    ):

        output.append(
            f"- {category}: {count}"
        )

    output.append("")

    output.append(
        "## Sparse Categories\n"
    )

    if sparse_categories:

        for category, count in sparse_categories:

            output.append(
                f"- {category}: {count} notes"
            )

    else:

        output.append(
            "- None"
        )

    output.append("")

    output.append(
        "## Notes Without Tags\n"
    )

    if report["no_tags"]:

        for note in report["no_tags"]:

            output.append(
                f"- {note}"
            )

    else:

        output.append(
            "- None"
        )

    output.append("")

    output.append(
        "## Low Tag Coverage\n"
    )

    if report["low_tags"]:

        for note, count in report["low_tags"]:

            output.append(
                f"- {note} ({count} tags)"
            )

    else:

        output.append(
            "- None"
        )

    output.append("")

    output.append(
        "## Stale Notes\n"
    )

    if report["stale_notes"]:

        for note, days in sorted(
            report["stale_notes"],
            key=lambda x: x[1],
            reverse=True
        ):

            output.append(
                f"- {note} ({days} days old)"
            )

    else:

        output.append(
            "- None"
        )

    output.append("")

    output.append(
        "## Large Notes\n"
    )

    if report["large_notes"]:

        for note, lines in sorted(
            report["large_notes"],
            key=lambda x: x[1],
            reverse=True
        ):

            output.append(
                f"- {note} ({lines} lines)"
            )

    else:

        output.append(
            "- None"
        )

    output.append("")

    output.append(
        "## Empty Notes\n"
    )

    if report["empty_notes"]:

        for note in report["empty_notes"]:

            output.append(
                f"- {note}"
            )

    else:

        output.append(
            "- None"
        )

    report_file.write_text(
        "\n".join(output),
        encoding="utf-8"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="AI Curator Report"
    )

    parser.add_argument(
        "--docs",
        required=True,
        help="Docs folder"
    )

    today = datetime.now.strftime('%Y-%m-%d')
    parser.add_argument(
        "--output",
        default=f"Reports/AI_Curator_Report_{today}.md",
        help="Report file"
    )

    args = parser.parse_args()

    docs_root = Path(
        args.docs
    ).resolve()

    report_file = Path(
        args.output
    ).resolve()

    report_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report = analyze_vault(
        docs_root
    )

    write_report(
        report,
        report_file
    )

    print(
        f"Report written: {report_file}"
    )


if __name__ == "__main__":
    main()