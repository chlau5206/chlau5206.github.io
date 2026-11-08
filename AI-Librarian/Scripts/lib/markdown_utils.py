"""  lib/markdown_utils.py
Markdown helper functions.

Upstream:
    AI_Tag_Generator.py
    Duplicate_Detector.py
    AI_Curator_Report.py
    Note_Health_Report.py
"""

from pathlib import Path
import yaml


def read_markdown(
    path: Path
) -> str:

    try:

        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    except Exception:

        return ""


def get_markdown_files(
    docs_root: Path
) -> list[Path]:

    return sorted(
        docs_root.rglob("*.md")
    )


def load_categories(
    yaml_file: Path
) -> dict:
    """
    Load categories.yml
    """

    if not yaml_file.exists():
        return {}

    return yaml.safe_load(
        yaml_file.read_text(
            encoding="utf-8"
        )
    ) or {}

