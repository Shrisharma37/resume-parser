"""Split resume text into common named sections."""

import re


SECTION_ALIASES = {
    "summary": {
        "summary",
        "professional summary",
        "profile",
        "professional profile",
        "objective",
        "career objective",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
    },
    "education": {
        "education",
        "academic background",
        "academic qualification",
        "academic qualifications",
        "academics",
        "educational qualifications",
    },
    "skills": {"skills", "technical skills", "core competencies", "competencies"},
    "projects": {
        "projects",
        "personal projects",
        "project experience",
        "selected projects",
    },
    "certifications": {
        "certification",
        "certifications",
        "certificates",
        "licenses and certifications",
    },
    "awards": {"achievement", "achievements", "awards", "honors"},
    "languages": {"languages", "language skills"},
}
HEADING_LOOKUP = {
    alias: section for section, aliases in SECTION_ALIASES.items() for alias in aliases
}


def extract_sections(text: str) -> dict[str, str]:
    """Return recognized section headings and their following text."""
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in text.splitlines():
        normalized = re.sub(r"[\s:#-]+$", "", line.strip()).casefold()
        heading = HEADING_LOOKUP.get(normalized)
        if heading:
            current_section = heading
            sections.setdefault(heading, [])
        elif current_section and line.strip():
            sections[current_section].append(line.strip())

    return {
        section: "\n".join(lines).strip()
        for section, lines in sections.items()
        if lines
    }