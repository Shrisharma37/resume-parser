"""Extract common contact fields from resume text."""

import re


EMAIL_PATTERN = re.compile(
    r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])",
    re.IGNORECASE,
)
PHONE_PATTERN = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")
LINKEDIN_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Z0-9-_%]+",
    re.IGNORECASE,
)
GITHUB_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/[A-Z0-9-]+",
    re.IGNORECASE,
)
NON_NAME_HEADINGS = {
    "resume",
    "curriculum vitae",
    "contact",
    "contact information",
    "professional summary",
    "summary",
    "profile",
}


def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(0).strip() if match else None


def _extract_name(text: str) -> str | None:
    for line in text.splitlines():
        candidate = line.strip().strip("|,;")
        if not candidate:
            continue
        if candidate.casefold().rstrip(":") in NON_NAME_HEADINGS:
            continue
        if "@" in candidate or "://" in candidate or re.search(r"\d", candidate):
            continue
        words = candidate.split()
        if 1 <= len(words) <= 5 and all(
            re.fullmatch(r"[A-Za-z][A-Za-z.'’-]*", word) for word in words
        ):
            return candidate
    return None


def extract_contact_info(text: str) -> dict[str, str | None]:
    """Return best-effort name, email, phone, LinkedIn, and GitHub fields."""
    return {
        "name": _extract_name(text),
        "email": _first_match(EMAIL_PATTERN, text),
        "phone": _first_match(PHONE_PATTERN, text),
        "linkedin": _first_match(LINKEDIN_PATTERN, text),
        "github": _first_match(GITHUB_PATTERN, text),
    }