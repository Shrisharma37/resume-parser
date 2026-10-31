"""Catalog-based skill recognition."""

import json
import re
from pathlib import Path
from typing import Mapping, Sequence

from resume_parser.config import SKILLS_FILE

SkillCatalog = Mapping[str, Sequence[str]]


def load_skills_catalog(path: Path | str = SKILLS_FILE) -> dict[str, list[str]]:
    """Load canonical skill names and matching aliases from a JSON file."""
    skills_path = Path(path)
    with skills_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict) or not all(
        isinstance(name, str)
        and isinstance(aliases, list)
        and all(isinstance(alias, str) for alias in aliases)
        for name, aliases in data.items()
    ):
        raise ValueError(f"Invalid skills catalog format: {skills_path}")
    return data


def extract_skills(text: str, catalog: SkillCatalog | None = None) -> list[str]:
    """Find catalogued skills in text, returning canonical names in catalog order."""
    skills_catalog = catalog if catalog is not None else load_skills_catalog()
    found = []
    for skill, aliases in skills_catalog.items():
        terms = [skill, *aliases]
        if any(
            re.search(
                rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])",
                text,
                flags=re.IGNORECASE,
            )
            for term in terms
            if term
        ):
            found.append(skill)
    return found