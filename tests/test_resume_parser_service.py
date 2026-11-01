import unittest
import fitz

from resume_parser.services.resume_parser_service import parse_resume


class ResumeParserServiceTests(unittest.TestCase):
    def test_extracts_summary_education_and_languages_from_pdf(self):
        document = fitz.open()
        page = document.new_page()
        page.insert_text(
            (50, 50),
            "Ada Lovelace\nada@example.com\n\n"
            "PROFILE SUMMARY\nMotivated developer.\n\n"
            "EDUCATION DETAILS\nB.Tech Computer Science\n\n"
            "LANGUAGES KNOWN\nEnglish, Hindi",
        )
        pdf_bytes = document.tobytes()
        document.close()

        resume = parse_resume(pdf_bytes, "sample.pdf")
        exported = resume.to_export_dict()

        self.assertEqual(exported["profile"]["summary"], "Motivated developer.")
        self.assertTrue(any("B.Tech" in item for item in exported["education"]))
        self.assertEqual(exported["languages"], ["English", "Hindi"])


if __name__ == "__main__":
    unittest.main()
