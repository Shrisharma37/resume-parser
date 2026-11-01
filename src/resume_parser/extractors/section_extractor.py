"""Extract common resume sections using normalized heading matching.

This is deliberately rule-based: unknown sections are preserved only when their
heading is recognized, and missing fields remain empty rather than fabricated.
"""
import re
import unicodedata

SECTION_ALIASES = {
    "summary": {
        "summary", "professional summary", "profile", "professional profile",
        "career objective", "objective", "about me", "profile summary",
        "personal profile", "career summary",
    },
    "experience": {
        "experience", "work experience", "professional experience",
        "employment history", "work history", "internship experience",
        "internships", "professional background",
    },
    "education": {
        "education", "educational background", "education details",
        "academic background", "academic qualification",
        "academic qualifications", "academics", "educational qualifications",
        "qualification", "qualifications", "academic details",
    },
    "skills": {
        "skills", "technical skills", "key skills", "core skills",
        "core competencies", "competencies", "technical expertise",
        "technologies", "technical knowledge",
    },
    "projects": {
        "projects", "personal projects", "project experience",
        "selected projects", "academic projects", "key projects",
    },
    "certifications": {
        "certification", "certifications", "certificates",
        "licenses and certifications", "courses and certifications",
    },
    "awards": {
        "achievement", "achievements", "awards", "honors", "honours",
        "accomplishments",
    },
    "languages": {
        "language", "languages", "language skills", "languages known",
        "known languages", "linguistic skills",
    },
}
HEADING_LOOKUP = {
    alias: section for section, aliases in SECTION_ALIASES.items()
    for alias in aliases
}


def _normalize_heading(line: str) -> tuple[str, str]:
    """Return (recognized heading, optional text on same line)."""
    value = unicodedata.normalize("NFKC", line).strip()
    value = re.sub(r"^[\s•*▪◦➢✓|]+", "", value)
    value = re.sub(r"[\s|]+$", "", value)
    value = re.sub(r"\s+", " ", value).strip()

    # Support headings such as "EDUCATION:" and "Education: B.Tech..."
    candidate = re.sub(r"[:：]+$", "", value).strip().casefold()
    if candidate in HEADING_LOOKUP:
        return HEADING_LOOKUP[candidate], ""

    if ":" in value:
        left, right = value.split(":", 1)
        key = re.sub(r"\s+", " ", left.strip()).casefold()
        if key in HEADING_LOOKUP:
            return HEADING_LOOKUP[key], right.strip()

    # Common decorated headings: "EDUCATION | QUALIFICATIONS"
    candidate = re.sub(r"\s+", " ", value.strip(" :-|")).casefold()
    if candidate in HEADING_LOOKUP:
        return HEADING_LOOKUP[candidate], ""
    return "", ""


def extract_sections(text: str) -> dict[str, str]:
    """Extract section contents while retaining original line text."""
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current and sections.get(current) and sections[current][-1] != "":
                sections[current].append("")
            continue

        heading, inline_content = _normalize_heading(line)
        if heading:
            current = heading
            sections.setdefault(current, [])
            if inline_content:
                sections[current].append(inline_content)
            continue

        if current:
            sections[current].append(line)

    result = {}
    for name, lines in sections.items():
        content = "\n".join(lines).strip()
        content = re.sub(r"\n{3,}", "\n\n", content)
        if content:
            result[name] = content
    return result
