"""Compare resume skills with skills requested in a job description."""

from dataclasses import dataclass

from resume_parser.extractors.skills_extractor import SkillCatalog, extract_skills
from resume_parser.models.resume import Resume


@dataclass(frozen=True)
class JobMatch:
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: float


def match_job(
    resume: Resume,
    job_description: str,
    skills_catalog: SkillCatalog | None = None,
) -> JobMatch:
    """Calculate the percentage of recognized job skills present in a resume."""
    required = extract_skills(job_description, skills_catalog)
    resume_skills = {skill.casefold() for skill in resume.skills}
    matched = [skill for skill in required if skill.casefold() in resume_skills]
    missing = [skill for skill in required if skill.casefold() not in resume_skills]
    score = len(matched) / len(required) * 100 if required else 0.0
    return JobMatch(required, matched, missing, score)