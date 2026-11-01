"""Coordinate the resume extraction pipeline."""

import hashlib
from datetime import datetime, timezone
from pathlib import Path

from resume_parser.extractors.contact_extractor import extract_contact_info
from resume_parser.extractors.pdf_extractor import extract_text_from_pdf
from resume_parser.extractors.section_extractor import extract_sections
from resume_parser.extractors.skills_extractor import SkillCatalog, extract_skills
from resume_parser.extractors.language_extractor import extract_languages
from resume_parser.models.resume import Resume


def parse_resume(
    pdf_bytes: bytes,
    filename: str = "resume.pdf",
    skills_catalog: SkillCatalog | None = None,
) -> Resume:
    """Parse contact details, sections, and skills from a PDF resume."""
    text = extract_text_from_pdf(pdf_bytes)
    contact = extract_contact_info(text)
    parsed_at = datetime.now(timezone.utc).isoformat()
    sections = extract_sections(text)
    return Resume(
        **contact,
        skills=extract_skills(text, skills_catalog),
        sections=sections,
        languages=extract_languages(sections.get("languages", "")),
        filename=Path(filename).name,
        created_at=parsed_at,
        parsed_at=parsed_at,
        file_hash=hashlib.sha256(pdf_bytes).hexdigest(),
        file_size_bytes=len(pdf_bytes),
    )