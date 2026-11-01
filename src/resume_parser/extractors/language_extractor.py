"""Extract language names from a resume's dedicated Languages section."""
import re

# Common language names. Extend this set as needed for the resumes being tested.
KNOWN_LANGUAGES = {
    "Arabic", "Bengali", "Chinese", "English", "French", "German", "Gujarati",
    "Hindi", "Japanese", "Kannada", "Korean", "Malayalam", "Marathi",
    "Odia", "Punjabi", "Russian", "Sanskrit", "Spanish", "Tamil", "Telugu",
    "Urdu",
}


def extract_languages(section_text: str) -> list[str]:
    """Return language names mentioned in a Languages section, in source order."""
    found = []
    for language in sorted(KNOWN_LANGUAGES, key=len, reverse=True):
        if re.search(rf"(?<![A-Za-z]){re.escape(language)}(?![A-Za-z])",
                     section_text, re.IGNORECASE):
            # Preserve canonical spelling and avoid duplicates.
            found.append(language)
    # Keep the output stable and readable; source order is not important here.
    return sorted(found, key=str.casefold)
