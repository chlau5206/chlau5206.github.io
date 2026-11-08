"""  lib/file_utils.py 
Common file helper functions used by AI Librarian tools.

Upstream:
    Metadata_Classifier.py
    AI_Tag_Generator.py
    Duplicate_Detector.py
    AI_Curator_Report.py
    Note_Health_Report.py
"""

from pathlib import Path
import yaml
#print (yaml.__version__)

def normalize_filename(filename: str) -> str:
    """
    Normalize filenames.

    Examples:
        abc def.md
        abc-def.md

    become:

        abc_def.md
    """

    p = Path(filename)

    name = p.stem
    name = name.replace(" ", "_")
    name = name.replace("-", "_")

    while "__" in name:
        name = name.replace("__", "_")

    return name + p.suffix


def should_skip_file(
    md_file: Path,
    docs_root: Path,
    skip_folders: set[str],
    skip_files: set[str]
) -> bool:

    rel_path = md_file.relative_to(docs_root)

    if md_file.name.lower() in {
        x.lower()
        for x in skip_files
    }:
        return True

    for part in rel_path.parts[:-1]:

        if part.lower() in {
            x.lower()
            for x in skip_folders
        }:
            return True

    return False


def load_skip_config(
    config_file: Path
) -> tuple[set[str], set[str]]:
    """
    Load skip configuration.

    Returns:
        skip_folders
        skip_files
    """

    if not config_file.exists():
        return set(), set()

    data = yaml.safe_load(
        config_file.read_text(
            encoding="utf-8"
        )
    ) or {}

    skip_folders = set(
        data.get(
            "skip_folders",
            []
        )
    )

    skip_files = set(
        data.get(
            "skip_files",
            []
        )
    )

    return (
        skip_folders,
        skip_files
    )