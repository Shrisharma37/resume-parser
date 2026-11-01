"""Parsed resume data model."""

from dataclasses import asdict, dataclass, field
import re
from typing import Any


@dataclass
class Resume:
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    skills: list[str] = field(default_factory=list)
    sections: dict[str, str] = field(default_factory=dict)
    filename: str = "resume.pdf"
    parser_version: str = "1.0"
    status: str = "completed"
    created_at: str | None = None
    parsed_at: str | None = None
    file_hash: str | None = None
    file_size_bytes: int | None = None
    ai_called_for_projects_or_experience: bool = False
    is_scanned_pdf: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)

    def to_export_dict(self) -> dict[str, Any]:
        """Return resume data in the structured JSON export format."""
        return {
            "profile": {
                "full_name": self.name,
                "email": self.email,
                "phone": self.phone,
                "location": None,
                "linkedin_url": self.linkedin,
                "github_url": self.github,
                "portfolio_url": None,
                "summary": self.sections.get("summary") or None,
            },
            "education": self._section_entries("education"),
            "technical_skills": {"technologies": list(self.skills)},
            "projects": self._section_entries("projects"),
            "experience": self._section_entries("experience"),
            "certifications": self._section_entries("certifications"),
            "achievements": self._section_entries("awards"),
            "metadata": {
                "parser_version": self.parser_version,
                "status": self.status,
                "created_at": self.created_at,
                "parsed_at": self.parsed_at,
                "file_name": self.filename,
                "file_hash": self.file_hash,
                "file_size_bytes": self.file_size_bytes,
                "ai_called_for_projects_or_experience": (
                    self.ai_called_for_projects_or_experience
                ),
                "is_scanned_pdf": self.is_scanned_pdf,
            },
        }

    def _section_entries(self, section: str) -> list[str]:
        content = self.sections.get(section, "").strip()
        return [
            entry.strip()
            for entry in re.split(r"\n\s*\n", content)
            if entry.strip()
        ]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Resume":
        """Build a model from a previously serialized representation."""
        return cls(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            linkedin=data.get("linkedin"),
            github=data.get("github"),
            skills=list(data.get("skills", [])),
            sections=dict(data.get("sections", {})),
            filename=data.get("filename", "resume.pdf"),
            parser_version=data.get("parser_version", "1.0"),
            status=data.get("status", "completed"),
            created_at=data.get("created_at"),
            parsed_at=data.get("parsed_at"),
            file_hash=data.get("file_hash"),
            file_size_bytes=data.get("file_size_bytes"),
            ai_called_for_projects_or_experience=data.get(
                "ai_called_for_projects_or_experience", False
            ),
            is_scanned_pdf=data.get("is_scanned_pdf", False),
        )