import tempfile
import unittest
from pathlib import Path

from resume_parser.models.resume import Resume
from resume_parser.repositories.resume_repository import ResumeRepository


class ResumeRepositoryTests(unittest.TestCase):
    def test_save_get_list_and_delete(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = ResumeRepository(Path(directory) / "resumes.sqlite3")
            resume = Resume(name="Ada Lovelace", skills=["Python"])

            resume_id = repository.save(resume)

            self.assertEqual(repository.get(resume_id), resume)
            self.assertEqual(repository.list_resumes()[0]["name"], "Ada Lovelace")
            self.assertTrue(repository.delete(resume_id))
            self.assertIsNone(repository.get(resume_id))
            self.assertFalse(repository.delete(resume_id))

    def test_structured_export_uses_requested_schema(self):
        resume = Resume(
            name="Ada Lovelace",
            email="ada@example.com",
            phone="+1 555 123 4567",
            linkedin="linkedin.com/in/ada",
            github="github.com/ada",
            skills=["Python"],
            languages=["English", "Hindi"],
            sections={"summary": "Builds reliable software."},
            filename="ada-resume.pdf",
            created_at="2026-10-28T11:22:38+00:00",
            parsed_at="2026-10-28T11:22:38+00:00",
            file_hash="abc123",
            file_size_bytes=100,
        )

        self.assertEqual(
            resume.to_export_dict(),
            {
                "profile": {
                    "full_name": "Ada Lovelace",
                    "email": "ada@example.com",
                    "phone": "+1 555 123 4567",
                    "location": None,
                    "linkedin_url": "linkedin.com/in/ada",
                    "github_url": "github.com/ada",
                    "portfolio_url": None,
                    "summary": "Builds reliable software.",
                },
                "education": [],
                "languages": ["English", "Hindi"],
                "technical_skills": {"technologies": ["Python"]},
                "projects": [],
                "experience": [],
                "certifications": [],
                "achievements": [],
                "metadata": {
                    "parser_version": "1.1",
                    "status": "completed",
                    "created_at": "2026-10-28T11:22:38+00:00",
                    "parsed_at": "2026-10-28T11:22:38+00:00",
                    "file_name": "ada-resume.pdf",
                    "file_hash": "abc123",
                    "file_size_bytes": 100,
                    "ai_called_for_projects_or_experience": False,
                    "is_scanned_pdf": False,
                },
            },
        )

    def test_structured_export_includes_extracted_sections(self):
        resume = Resume(
            sections={
                "education": "BSc Computer Science\nUniversity of Example",
                "projects": "Resume Parser\nBuilt a parser.",
                "experience": "Software Engineer\nExample Company",
                "certifications": "Python Certificate",
                "awards": "Dean's List",
            }
        )

        exported = resume.to_export_dict()

        self.assertEqual(
            exported["education"], ["BSc Computer Science\nUniversity of Example"]
        )
        self.assertEqual(
            exported["projects"], ["Resume Parser\nBuilt a parser."]
        )
        self.assertEqual(
            exported["experience"], ["Software Engineer\nExample Company"]
        )
        self.assertEqual(exported["certifications"], ["Python Certificate"])
        self.assertEqual(exported["achievements"], ["Dean's List"])


if __name__ == "__main__":
    unittest.main()
