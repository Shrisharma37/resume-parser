import unittest

from resume_parser.extractors.language_extractor import extract_languages


class LanguageExtractorTests(unittest.TestCase):
    def test_extracts_english_and_hindi(self):
        self.assertEqual(extract_languages("English, Hindi"), ["English", "Hindi"])

    def test_does_not_match_partial_words(self):
        self.assertEqual(extract_languages("English-speaking"), ["English"])


if __name__ == "__main__":
    unittest.main()
