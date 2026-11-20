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
from lib.file_utils import load_yaml_config
from lib.metadata_utils import (
    extract_front_matter
)

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

# This used in Markdown_cleanup.py, AI_Tag_Generater.py, Duplicate_Detector.py
def write_markdown(
    path: Path,
    content: str
):

    path.write_text(
        content,
        encoding="utf-8"
    )

def load_categories(
    yaml_file: Path
) -> dict:
    """
    Load categories.yml
    """
    # if not yaml_file.exists():
    #     return {}

    # return yaml.safe_load(
    #     yaml_file.read_text(
    #         encoding="utf-8"
    #     )
    # ) or {}

    return load_yaml_config(yaml_file) or {}

def strip_front_matter(
    content: str
) -> str:

    _, body = extract_front_matter(
        content
    )

    return body

def word_count(
    content: str
) -> int:

    return len(
        content.split()
    )

