import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from core.resume_parser import extract_text_from_pdf
from core.skills import load_skills, extract_skills


st.title("Upload Resume")

from pathlib import Path

SKILLS_CSV = Path(__file__).resolve().parents[2] / "data" / "skills.csv"
skills_list = load_skills(SKILLS_CSV)


mode = st.radio("Choose input method", ["Upload PDF", "Paste text"])

resume_text = ""

if mode == "Upload PDF":
    uploaded = st.file_uploader("Upload your resume PDF", type=["pdf"])
    if uploaded is not None:
        resume_text = extract_text_from_pdf(uploaded.read())
else:
    resume_text = st.text_area("Paste your resume text here", "", height=300)


if resume_text:
    st.subheader("Resume preview")
    st.text_area(
    "Resume preview (first 5,000 characters)",
    resume_text[:5000],
    height=400
)


    found = extract_skills(resume_text, skills_list)

    st.subheader("Skills found")
    st.write(f"Found {len(found)} skills")
    st.markdown(
    " ".join(f"`{skill}`" for skill in found)
)


    st.session_state["resume_text"] = resume_text
    st.session_state["resume_skills"] = found
