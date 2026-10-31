import unittest

from resume_parser.extractors.contact_extractor import extract_contact_info


class ContactExtractorTests(unittest.TestCase):
    def test_extracts_contact_fields(self):
        text = (
            "Ada Lovelace\n"
            "ada@example.com | +1 (555) 123-4567\n"
            "linkedin.com/in/ada-lovelace\n"
            "github.com/adalovelace"
        )
        result = extract_contact_info(text)
        self.assertEqual(result["name"], "Ada Lovelace")
        self.assertEqual(result["email"], "ada@example.com")
        self.assertEqual(result["phone"], "+1 (555) 123-4567")
        self.assertEqual(result["linkedin"], "linkedin.com/in/ada-lovelace")
        self.assertEqual(result["github"], "github.com/adalovelace")

    def test_missing_contact_fields_are_none(self):
        result = extract_contact_info("No contact details here.")
        self.assertIsNone(result["email"])
        self.assertIsNone(result["phone"])
        self.assertIsNone(result["linkedin"])
        self.assertIsNone(result["github"])


if __name__ == "__main__":
    unittest.main()