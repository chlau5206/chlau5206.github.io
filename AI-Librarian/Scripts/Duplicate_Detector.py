# Duplicate_Detector.py
#!/usr/bin/env python3
"""
Duplicate_Detector.py

Purpose:
    Scan a MkDocs / Obsidian vault for potential duplicate notes.

Detects:
    - Similar filenames
    - Similar content
    - Exact duplicates

Output:
    docs/reports/Duplicate_Report.md

Usage:
    python Duplicate_Detector.py
    python Duplicate_Detector.py --docs docs
    python Duplicate_Detector.py --threshold 85

Author:
    Charles AI Librarian Project
"""

from pathlib import Path
from difflib import SequenceMatcher
import argparse
from datetime import datetime
import hashlib
from lib.markdown_utils import * 
from lib.metadata_utils import * 

# =====================================================================
# CONFIG
# =====================================================================

DEFAULT_SKIP_FOLDERS = frozenset({
    "Reports",
    "Archive"
})

DEFAULT_SKIP_FILES = frozenset({
    "index.md",
    "README.md"
})

DEFAULT_THRESHOLD = 85
NOW = datetime.now()

# =====================================================================
# HELPERS
# =====================================================================

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio() * 100

def md5_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


# =====================================================================
# DUPLICATE ANALYSIS
# =====================================================================

def analyze_files(files, threshold):

    filename_matches = []
    content_matches = []
    exact_duplicates = []

    content_hashes = {}

    for file in files:

        text = read_markdown(file)

        file_hash = md5_hash(text)

        if file_hash not in content_hashes:
            content_hashes[file_hash] = []

        content_hashes[file_hash].append(file)

    # Exact duplicates

    for hash_value, matching_files in content_hashes.items():

        if len(matching_files) > 1:

            exact_duplicates.append(matching_files)

    # Similarity check

    total = len(files)

    for i in range(total):

        file_a = files[i]
        name_a = file_a.stem.lower()
        text_a = read_markdown(file_a)

        for j in range(i + 1, total):

            file_b = files[j]
            name_b = file_b.stem.lower()
            text_b = read_markdown(file_b)

            # Filename similarity

            name_score = similarity(name_a, name_b)

            if name_score >= threshold:

                filename_matches.append(
                    (name_score, file_a, file_b)
                )

            # Content similarity

            content_score = similarity(text_a, text_b)

            if content_score >= threshold:

                content_matches.append(
                    (content_score, file_a, file_b)
                )

    filename_matches.sort(reverse=True, key=lambda x: x[0])
    content_matches.sort(reverse=True, key=lambda x: x[0])

    return (
        exact_duplicates,
        filename_matches,
        content_matches,
    )


# =====================================================================
# REPORT
# =====================================================================

def generate_report(
    output_file,
    exact_duplicates,
    filename_matches,
    content_matches,
    threshold,
):

    # now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []

    lines.append("# Duplicate Report")
    lines.append("")
    lines.append(f"Generated: {NOW}.strftime('%Y-%m-%d %H:%M')")  
    lines.append("")
    lines.append(f"Threshold: {threshold}%")
    lines.append("")

    # ---------------------------------------------------------
    # Exact duplicates
    # ---------------------------------------------------------

    lines.append("## Exact Duplicate Files")
    lines.append("")

    if exact_duplicates:

        for group in exact_duplicates:

            lines.append("### Duplicate Group")
            lines.append("")

            for file in group:
                lines.append(f"- {file}")

            lines.append("")

    else:

        lines.append("No exact duplicates found.")
        lines.append("")

    # ---------------------------------------------------------
    # Similar filenames
    # ---------------------------------------------------------

    lines.append("## Similar Filenames")
    lines.append("")

    if filename_matches:

        for score, file_a, file_b in filename_matches:

            lines.append(
                f"- **{score:.1f}%** : "
                f"`{file_a.name}` ↔ `{file_b.name}`"
            )

    else:

        lines.append("No similar filenames found.")

    lines.append("")

    # ---------------------------------------------------------
    # Similar content
    # ---------------------------------------------------------

    lines.append("## Similar Content")
    lines.append("")

    if content_matches:

        for score, file_a, file_b in content_matches:

            lines.append(
                f"- **{score:.1f}%** : "
                f"`{file_a.name}` ↔ `{file_b.name}`"
            )

    else:

        lines.append("No similar content found.")

    lines.append("")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# =====================================================================
# MAIN
# =====================================================================

def main():

    parser = argparse.ArgumentParser(
        description="Detect duplicate markdown notes."
    )

    parser.add_argument(
        "--docs",
        default="docs",
        help="Docs root folder"
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help="Similarity threshold"
    )

    args = parser.parse_args()

    docs_root = Path(args.docs)

    files = get_markdown_files(docs_root, DEFAULT_SKIP_FILES)

    (
        exact_duplicates,
        filename_matches,
        content_matches,
    ) = analyze_files(
        files,
        args.threshold
    )

    report_file = (
        docs_root
        / "reports"
        / f"Duplicate_Report_{NOW.strftime('%Y-%m-%d')}.md"
    )

    generate_report(
        report_file,
        exact_duplicates,
        filename_matches,
        content_matches,
        args.threshold,
    )

    print()
    print("Duplicate Report Generated")
    print(report_file)
    print()


if __name__ == "__main__":
    main()

