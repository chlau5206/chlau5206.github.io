#!/usr/bin/env python3

""" note_health_report.py
Author: Charles H Lau

Generate a health report for a MkDocs / Obsidian vault.

Checks:
- Missing metadata
- Empty notes
- Short notes
- Large notes
- Stale notes
- Duplicate titles
- Category statistics

Output:
    docs/reports/Vault_Health_Report_today_date.md

Usage:
    python note_health_report.py
    python note_health_report.py --docs docs
"""

from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta
import argparse

from lib.metadata_utils import * # has_front_matter
from lib.markdown_utils import * # read_markdown

NOW = datetime.now()

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

SHORT_NOTE = 100
LARGE_NOTE = 5000


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Generate vault health report"
    )

    parser.add_argument(
        "--docs",
        default="docs",
        help="Docs root directory"
    )

    args = parser.parse_args()

    docs_root = Path(args.docs)

    report_file = (
        docs_root
        / "Reports"
        / f"Vault_Health_Report_{NOW.strftime('%Y-%m-%d')}.md"
    )

    markdown_files = [
        f
        for f in docs_root.rglob("*.md")
        if f.name.lower() != "index.md"
        and "reports" not in f.parts
    ]

    total_notes = len(markdown_files)

    missing_metadata = []
    empty_notes = []
    short_notes = []
    large_notes = []
    stale_notes = []

    categories = Counter()
    titles = []

    cutoff = NOW - timedelta(
        days=STALE_DAYS
    )

    # -----------------------------------------------------
    # Scan Files
    # -----------------------------------------------------

    for file in markdown_files:

        text = read_markdown(file)

        rel = file.relative_to(docs_root)

        # Category Statistics

        if len(rel.parts) > 1:
            categories[rel.parts[0]] += 1

        # Metadata Check

        if not has_front_matter(text):
            missing_metadata.append(str(rel))

        # Size Check

        content_size = len(text.strip())

        if content_size == 0:

            empty_notes.append(str(rel))

        elif content_size < SHORT_NOTE:

            short_notes.append(str(rel))

        elif content_size > LARGE_NOTE:

            large_notes.append(str(rel))

        # Stale Note Check

        modified = datetime.fromtimestamp(
            file.stat().st_mtime
        )

        if modified < cutoff:
            stale_notes.append(str(rel))

        titles.append(
            file.stem.lower()
        )

    # -----------------------------------------------------
    # Duplicate Titles
    # -----------------------------------------------------

    duplicates = [
        title
        for title, count
        in Counter(titles).items()
        if count > 1
    ]

    # -----------------------------------------------------
    # Report
    # -----------------------------------------------------

    report_lines = []

    report_lines.append(
        "# Vault Health Report"
    )
    report_lines.append("")

    report_lines.append(
        f"Generated: {datetime.now():%Y-%m-%d %H:%M}"
    )

    report_lines.append("")

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    report_lines.extend([
        "## Summary",
        "",
        f"- Total Notes: {total_notes}",
        f"- Categories: {len(categories)}",
        f"- Missing Metadata: {len(missing_metadata)}",
        f"- Empty Notes: {len(empty_notes)}",
        f"- Short Notes: {len(short_notes)}",
        f"- Large Notes: {len(large_notes)}",
        f"- Stale Notes: {len(stale_notes)}",
        f"- Duplicate Titles: {len(duplicates)}",
        ""
    ])

    # -----------------------------------------------------
    # Categories
    # -----------------------------------------------------

    report_lines.extend([
        "## Categories",
        ""
    ])

    for category, count in categories.most_common():

        report_lines.append(
            f"- {category}: {count}"
        )

    report_lines.append("")

    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    report_lines.extend([
        "## Missing Metadata",
        ""
    ])

    if missing_metadata:

        for item in missing_metadata:
            report_lines.append(
                f"- {item}"
            )

    else:

        report_lines.append(
            "No issues found."
        )

    report_lines.append("")

    # -----------------------------------------------------
    # Empty Notes
    # -----------------------------------------------------

    report_lines.extend([
        "## Empty Notes",
        ""
    ])

    if empty_notes:

        for item in empty_notes:
            report_lines.append(
                f"- {item}"
            )

    else:

        report_lines.append(
            "No issues found."
        )

    report_lines.append("")

    # -----------------------------------------------------
    # Short Notes
    # -----------------------------------------------------

    report_lines.extend([
        "## Short Notes",
        ""
    ])

    if short_notes:

        for item in short_notes:
            report_lines.append(
                f"- {item}"
            )

    else:

        report_lines.append(
            "No issues found."
        )

    report_lines.append("")

    # -----------------------------------------------------
    # Large Notes
    # -----------------------------------------------------

    report_lines.extend([
        "## Large Notes",
        ""
    ])

    if large_notes:

        for item in large_notes:
            report_lines.append(
                f"- {item}"
            )

    else:

        report_lines.append(
            "No issues found."
        )

    report_lines.append("")

    # -----------------------------------------------------
    # Stale Notes
    # -----------------------------------------------------

    report_lines.extend([
        "## Stale Notes",
        ""
    ])

    if stale_notes:

        for item in stale_notes:
            report_lines.append(
                f"- {item}"
            )

    else:

        report_lines.append(
            "No issues found."
        )

    report_lines.append("")

    # -----------------------------------------------------
    # Duplicate Titles
    # -----------------------------------------------------

    report_lines.extend([
        "## Duplicate Titles",
        ""
    ])

    if duplicates:

        for item in duplicates:
            report_lines.append(
                f"- {item}"
            )

    else:

        report_lines.append(
            "No issues found."
        )

    report_lines.append("")

    # -----------------------------------------------------
    # Save Report
    # -----------------------------------------------------

    report_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )

    print()
    print("Vault Health Report Generated")
    print(report_file)
    print()


if __name__ == "__main__":
    main()

