"""Streamlit interface for parsing resumes and comparing job requirements."""

import json
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from resume_parser.config import MAX_UPLOAD_SIZE_MB
from resume_parser.extractors.pdf_extractor import PDFExtractionError
from resume_parser.extractors.skills_extractor import load_skills_catalog
from resume_parser.models.resume import Resume
from resume_parser.repositories.resume_repository import ResumeRepository
from resume_parser.services.job_matcher import match_job
from resume_parser.services.resume_parser_service import parse_resume


st.set_page_config(page_title="Smart resume parser", page_icon=":material/description:")
st.title("Smart resume parser")
st.write(
    "Upload a text-based PDF to extract contact details, resume sections, and skills. "
    "Compare those skills with a job description."
)
st.caption(
    "Files are processed in this app session and are not saved unless you choose "
    "“Save parsed resume locally.” Scanned PDFs are not OCR-processed."
)

with st.form("resume_analysis"):
    uploaded_file = st.file_uploader(
        "Choose a resume PDF",
        type=["pdf"],
        max_upload_size=MAX_UPLOAD_SIZE_MB,
    )
    job_description = st.text_area(
        "Job description (optional)",
        placeholder="Paste the job description to compare its required skills.",
        height=180,
    )
    submitted = st.form_submit_button("Analyze resume", type="primary")

if submitted:
    if uploaded_file is None:
        st.error("Choose a PDF file before analyzing.")
    else:
        try:
            with st.spinner("Extracting resume details..."):
                resume = parse_resume(
                    uploaded_file.getvalue(),
                    filename=uploaded_file.name,
                )
            st.session_state["parsed_resume"] = resume.to_dict()
            st.session_state["job_description"] = job_description
            st.success("Resume analyzed.")
        except PDFExtractionError as error:
            st.error(str(error))

resume_data = st.session_state.get("parsed_resume")
if resume_data:
    resume = Resume.from_dict(resume_data)
    st.subheader("Extracted profile")
    profile_columns = st.columns(2)
    profile_fields = (
        ("Name", resume.name),
        ("Email", resume.email),
        ("Phone", resume.phone),
        ("LinkedIn", resume.linkedin),
        ("GitHub", resume.github),
    )
    for index, (label, value) in enumerate(profile_fields):
        with profile_columns[index % 2]:
            st.write(f"**{label}:** {value or 'Not found'}")

    st.subheader("Skills")
    if resume.skills:
        st.write(", ".join(resume.skills))
    else:
        st.info("No skills from the current catalog were found.")

    if resume.sections:
        st.subheader("Resume sections")
        for section, content in resume.sections.items():
            with st.expander(section.replace("_", " ").title()):
                st.text(content)
    else:
        st.info("No recognized resume section headings were found.")

    saved_job_description = st.session_state.get("job_description", "")
    if saved_job_description.strip():
        st.subheader("Job skill match")
        match = match_job(resume, saved_job_description, load_skills_catalog())
        if match.required_skills:
            st.metric("Recognized skill match", f"{match.match_score:.0f}%")
            st.write(f"**Matched:** {', '.join(match.matched_skills) or 'None'}")
            st.write(f"**Not found in resume:** {', '.join(match.missing_skills) or 'None'}")
            st.caption(
                "This score compares catalogued skills only; it is not an overall "
                "qualification or hiring recommendation."
            )
        else:
            st.info("No catalogued skills were recognized in the job description.")

    st.subheader("Export and save")
    export_json = json.dumps(resume.to_export_dict(), indent=2, ensure_ascii=False)
    safe_stem = Path(resume.filename).stem or "resume"
    st.download_button(
        "Download parsed data",
        data=export_json,
        file_name=f"{safe_stem}-parsed.json",
        mime="application/json",
    )
    if st.button("Save parsed resume locally", icon=":material/save:"):
        record_id = ResumeRepository().save(resume)
        st.success(f"Saved locally as record {record_id}.")