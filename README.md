# Smart resume parser

A local-first Streamlit application that extracts contact information, common
resume sections, and skills from text-based PDF files. It can compare extracted
skills with a pasted job description and export the parsed data as JSON.

## Requirements

- Python 3.10 or newer
- pip

## Run locally

From the project directory, create and activate a virtual environment, then
install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, upload a PDF (up to 10 MB), and choose
**Analyze resume**. Paste a job description in the same form to see a
catalog-based skill comparison. **Download parsed data** exports JSON with
`profile`, `education`, `technical_skills`, `projects`, `experience`,
`certifications`, `achievements`, and `metadata` fields. The section arrays
contain text blocks captured from recognized resume headings; they are not yet
normalized into structured school, role, or project fields. `metadata` contains
parser-generated file and processing details.

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) and
   connect the GitHub account that owns the repository.
3. Create an app from the repository's `main` branch and set the app file to
   `app.py`.
4. Deploy. Streamlit Cloud installs the packages listed in `requirements.txt`.

The app does not require API keys or secrets. The repository and deployed app
are public, and the app does not include sign-in or access control. Anyone who
can open the app can upload a resume for processing. Do not use a public
deployment for sensitive or real candidate data; restrict or avoid deployment
unless you have an appropriate privacy and access-control setup.

## What it extracts

- Name, email, phone number, LinkedIn, and GitHub when recognizable
- Summary, experience, education, skills, projects, certifications, awards,
  and language sections with recognized headings
- Skills and aliases listed in `data/skills.json`

The parser uses selectable PDF text; it does not perform OCR. Its contact,
section, and skill detection is heuristic and should be checked against the
original resume. Exported education, project, experience, certification, and
achievement entries preserve their section text as blocks. Job match
percentages represent only the overlap of recognized catalogued skills, not a
hiring recommendation.

## Privacy

Resume contents are processed by the app locally. Parsed data stays in the
current Streamlit session unless you explicitly select **Save parsed resume
locally**. Saved records are stored in `data/resumes.sqlite3`; that local
database is ignored by Git. Use the JSON download when you want a portable
export. Avoid deploying this app publicly without adding appropriate access
controls and data handling safeguards.

## Tests

Run the unit tests from the project directory:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

See [docs/architecture.md](docs/architecture.md) and
[docs/limitations.md](docs/limitations.md) for additional details.