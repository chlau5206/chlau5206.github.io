"""  lib/metadata_utils.py
Metadata helper functions.

Upstream:
    Metadata_Classifier.py
    AI_Tag_Generator.py
    AI_Curator_Report.py
"""

import re
import yaml 

from pathlib import Path


def title_from_filename(
    filename: str
) -> str:

    name = Path(filename).stem

    name = name.replace("_", " ")
    name = name.replace("-", " ")

    return name.title()


def has_front_matter(
    content: str
) -> bool:

    lines = content.splitlines()

    if len(lines) < 3:
        return False

    return lines[0].strip() == "---"


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

    yaml_block = match.group(1)

    body = content[match.end():]

    return (
        yaml_block,
        body
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
        return ""

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


def extract_excluded_tags(
    yaml_block: str
) -> list[str]:

    tags = []

    lines = yaml_block.splitlines()

    in_tags = False

    for line in lines:

        if line.strip() == "excluded_tags:":
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


def replace_tags(
    yaml_block: str,
    tags: list[str]
) -> str:

    lines = yaml_block.splitlines()

    output = []

    in_tags = False

    for line in lines:

        if line.strip() == "tags:":

            in_tags = True

            output.append(
                "tags:"
            )

            for tag in tags:

                output.append(
                    f"  - {tag}"
                )

            continue

        if in_tags:

            if line.startswith("  - "):
                continue

            in_tags = False

        output.append(line)

    return "\n".join(output)


def rebuild_document(
    yaml_block: str,
    body: str
) -> str:

    return (
        "---\n"
        + yaml_block
        + "\n---\n"
        + body
    )
