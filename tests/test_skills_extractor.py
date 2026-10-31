import unittest

from resume_parser.extractors.skills_extractor import extract_skills


class SkillsExtractorTests(unittest.TestCase):
    def test_matches_canonical_names_and_aliases_without_substrings(self):
        catalog = {
            "Python": ["python3"],
            "SQL": [],
            "C++": ["cpp"],
        }
        self.assertEqual(
            extract_skills("Python3 developer using C++ and MySQL", catalog),
            ["Python", "C++"],
        )

    def test_returns_no_skills_for_unmatched_text(self):
        self.assertEqual(extract_skills("People and communication", {"Python": []}), [])


if __name__ == "__main__":
    unittest.main()