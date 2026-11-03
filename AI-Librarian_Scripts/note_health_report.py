# Note health report
# Usage: python scripts\note_health_report.py

from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta

DOCS_ROOT = Path("docs")
REPORT_FILE = Path("reports/vault_health.md")

STALE_DAYS = 365
SHORT_NOTE = 100
LARGE_NOTE = 5000


def has_frontmatter(text):
    return text.startswith("---")


def main():

    markdown_files = [
        f for f in DOCS_ROOT.rglob("*.md")
        if f.name.lower() != "index.md"
    ]

    total_notes = len(markdown_files)

    missing_metadata = []
    short_notes = []
    empty_notes = []
    large_notes = []
    stale_notes = []

    categories = Counter()
    titles = []

    cutoff = datetime.now() - timedelta(days=STALE_DAYS)

    for file in markdown_files:

        text = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        rel = file.relative_to(DOCS_ROOT)

        if len(rel.parts) > 1:
            categories[rel.parts[0]] += 1

        if not has_frontmatter(text):
            missing_metadata.append(str(rel))

        content_size = len(text.strip())

        if content_size == 0:
            empty_notes.append(str(rel))

        elif content_size < SHORT_NOTE:
            short_notes.append(str(rel))

        elif content_size > LARGE_NOTE:
            large_notes.append(str(rel))

        modified = datetime.fromtimestamp(
            file.stat().st_mtime
        )

        if modified < cutoff:
            stale_notes.append(str(rel))

        titles.append(file.stem.lower())

    duplicates = [
        item
        for item, count in Counter(titles).items()
        if count > 1
    ]

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with REPORT_FILE.open(
        "w",
        encoding="utf-8"
    ) as rpt:

        rpt.write("# Vault Health Report\n\n")

        rpt.write("## Summary\n\n")
        rpt.write(f"- Total Notes: {total_notes}\n")
        rpt.write(f"- Categories: {len(categories)}\n\n")

        rpt.write("## Categories\n\n")

        for name, count in categories.most_common():
            rpt.write(f"- {name}: {count}\n")

        rpt.write("\n## Metadata\n\n")
        rpt.write(
            f"- Missing Metadata: {len(missing_metadata)}\n\n"
        )

        for item in missing_metadata:
            rpt.write(f"  - {item}\n")

        rpt.write("\n## Empty Notes\n\n")

        for item in empty_notes:
            rpt.write(f"- {item}\n")

        rpt.write("\n## Short Notes\n\n")

        for item in short_notes:
            rpt.write(f"- {item}\n")

        rpt.write("\n## Large Notes\n\n")

        for item in large_notes:
            rpt.write(f"- {item}\n")

        rpt.write("\n## Stale Notes\n\n")

        for item in stale_notes:
            rpt.write(f"- {item}\n")

        rpt.write("\n## Duplicate Titles\n\n")

        for item in duplicates:
            rpt.write(f"- {item}\n")

    print(f"Report written to: {REPORT_FILE}")


if __name__ == "__main__":
    main()