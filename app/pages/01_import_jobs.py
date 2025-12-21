import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from core.remotive_client import fetch_jobs
from core.skills import load_skills, extract_skills

st.title("Import Jobs")
skills_list = load_skills("data/skills.csv")
resume_skills = st.session_state.get("resume_skills", [])
st.info("Upload your resume first on the Upload Resume page to enable skill matching here.")

search_term = st.text_input("Search term", "data analyst")
limit = st.slider("Max jobs to display", min_value=5, max_value=100, value=25, step=5)

if st.button("Fetch jobs"):
    jobs = fetch_jobs(search=search_term)
    resume_set = set(resume_skills)

    st.success(f"Found {len(jobs)} jobs")

    if not resume_set:
        st.warning(
            "No resume skills found yet. "
            "Go to Upload Resume and upload your resume first."
        )

    if len(jobs) == 0:
        st.warning(
            "Try a different keyword. Example: analytics, sql, power bi, business intelligence."
        )
    else:
        rows = []

        for j in jobs[:limit]:
            job_text = (j.get("description") or "") + " " + " ".join(j.get("tags") or [])
            job_skills = extract_skills(job_text, skills_list)

            matched = sorted(set(job_skills) & resume_set)
            missing = sorted(set(job_skills) - resume_set)

            if len(job_skills) == 0:
                match_pct = 0.0
            else:
                match_pct = (len(matched) / len(job_skills)) * 100

            rows.append(
                {
                    "Match %": round(match_pct, 1),
                    "Matched skills": ", ".join(matched[:20]),
                    "Missing skills": ", ".join(missing[:20]),
                    "Title": j.get("title", ""),
                    "Company": j.get("company_name", ""),
                    "Category": j.get("category", ""),
                    "Location": j.get("candidate_required_location", ""),
                    "Published": j.get("publication_date", ""),
                    "Remotive URL": j.get("url", ""),
                }
            )

        df = pd.DataFrame(rows)

        if "Match %" in df.columns:
            df = df.sort_values("Match %", ascending=False)

        st.caption("Source: Remotive. Each job links back to Remotive as required.")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Match %": st.column_config.NumberColumn("Match %", format="%.1f"),
                "Remotive URL": st.column_config.LinkColumn("Remotive URL"),
            },
        )

