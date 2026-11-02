import argparse
from pathlib import Path
from datetime import datetime

# ---------------------------
# Helpers
# ---------------------------

def title_from_filename(filename: str) -> str:
    name = Path(filename).stem

    name = name.replace("_", " ")
    name = name.replace("-", " ")

    return name.title()


def has_front_matter(content: str) -> bool:
    lines = content.splitlines()

    if len(lines) < 3:
        return False

    return lines[0].strip() == "---"


def build_metadata(md_file: Path, docs_root: Path) -> str:
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

    tag_lines = "\n".join(f"  - {tag}" for tag in tags)

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


# ---------------------------
# Processing
# ---------------------------

def process_file(md_file: Path,
                 docs_root: Path,
                 dry_run: bool):

    if md_file.suffix.lower() != ".md":
        return

    if md_file.name.lower() == "index.md":
        print(f"SKIP (index): {md_file}")
        return

    content = md_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    if has_front_matter(content):
        print(f"SKIP (metadata exists): {md_file}")
        return

    metadata = build_metadata(md_file, docs_root)

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


# ---------------------------
# Main
# ---------------------------

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

    if args.file:
        process_file(
            Path(args.file).resolve(),
            docs_root,
            args.dry_run
        )
        return

    for md_file in docs_root.rglob("*.md"):
        process_file(
            md_file,
            docs_root,
            args.dry_run
        )


if __name__ == "__main__":
    main()