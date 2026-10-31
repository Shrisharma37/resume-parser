import unittest

from resume_parser.extractors.section_extractor import extract_sections


class SectionExtractorTests(unittest.TestCase):
    def test_extracts_and_normalizes_sections(self):
        text = (
            "Professional Summary\n"
            "Builds reliable software.\n\n"
            "WORK EXPERIENCE:\n"
            "Engineer at Example.\n"
            "Education\n"
            "BSc Computer Science"
        )
        self.assertEqual(
            extract_sections(text),
            {
                "summary": "Builds reliable software.",
                "experience": "Engineer at Example.",
                "education": "BSc Computer Science",
            },
        )


if __name__ == "__main__":
    unittest.main()
