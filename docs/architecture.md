# Architecture

The project separates the Streamlit interface from parsing logic:

- `app.py` provides PDF upload, result display, job matching, JSON export, and
  optional local persistence.
- `src/resume_parser/extractors/` contains PDF, contact, section, and skill
  extractors.
- `src/resume_parser/services/` composes extractors and computes job-skill
  overlap.
- `src/resume_parser/models/resume.py` defines the parsed resume data model.
- `src/resume_parser/repositories/resume_repository.py` stores parsed records
  in SQLite only after an explicit save action.
- `data/skills.json` defines canonical skill names and recognized aliases.

The parser is deterministic and does not send documents to external services.
The Streamlit app holds the current result in per-session state; the repository
is used only when the user chooses to save locally.