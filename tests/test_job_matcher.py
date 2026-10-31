import unittest

from resume_parser.models.resume import Resume
from resume_parser.services.job_matcher import match_job


class JobMatcherTests(unittest.TestCase):
    def test_computes_matched_and_missing_skills(self):
        resume = Resume(skills=["Python", "SQL"])
        result = match_job(
            resume,
            "We need Python, SQL, and AWS.",
            {"Python": [], "SQL": [], "AWS": []},
        )
        self.assertEqual(result.required_skills, ["Python", "SQL", "AWS"])
        self.assertEqual(result.matched_skills, ["Python", "SQL"])
        self.assertEqual(result.missing_skills, ["AWS"])
        self.assertAlmostEqual(result.match_score, 200 / 3)

    def test_empty_job_skills_have_zero_score(self):
        result = match_job(Resume(skills=["Python"]), "Great communication skills.")
        self.assertEqual(result.required_skills, [])
        self.assertEqual(result.match_score, 0)


if __name__ == "__main__":
    unittest.main()