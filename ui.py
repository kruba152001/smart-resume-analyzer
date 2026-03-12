import streamlit as st
import tempfile
import os
import pandas as pd

from llm_client import generate_resume_suggestions
from resume_parser import clean_text, extract_text_from_pdf
from nlp_extractor import extract_skills_from_text
from skill_scorer import compute_skill_weights, compute_weighted_score

st.set_page_config(page_title="Smart Resume Analyzer", layout="centered")
st.title("🧠 Smart Resume Analyzer")
st.write("Upload your resume and see how well it matches the job requirements.")

st.subheader("Paste Job Description")
job_description = st.text_area("Enter the job description here", height=200)
uploaded_file   = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    st.success("Resume uploaded successfully!")

    raw_text     = extract_text_from_pdf(temp_path)
    cleaned_text = clean_text(raw_text)

    if not job_description.strip():
        st.warning("Please paste a Job Description to analyze against.")
        st.stop()

    cleaned_jd    = clean_text(job_description)
    job_skills    = extract_skills_from_text(cleaned_jd)

    if not job_skills:
        st.warning("Could not extract skills from the JD. Please provide a more detailed JD.")
        st.stop()

    resume_skills  = extract_skills_from_text(cleaned_text)
    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - matched_skills

    # ── SCORING ──────────────────────────────────────────
    skill_weights = compute_skill_weights(job_description, job_skills)
    score_data    = compute_weighted_score(matched_skills, skill_weights)

    weighted_pct    = score_data["weighted_pct"]
    score_out_of_10 = round(weighted_pct / 10, 1)

    # ── DECISION STRING ───────────────────────────────────
    if weighted_pct >= 70:
        decision = "🟢 Strong match — good fit for this role."
    elif weighted_pct >= 40:
        decision = "🟡 Partial match — some gaps to address."
    else:
        decision = "🔴 Low match — significant skill gaps."

    # ── DISPLAY SCORE ─────────────────────────────────────
    st.subheader("📊 Match Score")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Match Score", f"{score_out_of_10} / 10")
    with col2:
        st.metric("Match Percentage", f"{weighted_pct}%")

    st.info(decision)    # ← renders the decision string in a blue box

    # ── PRIORITY LABEL ────────────────────────────────────
    def get_priority_label(weight: float) -> str:
        if weight >= 3.0:
            return "🔴 Critical"
        elif weight >= 1.5:
            return "🟡 Important"
        else:
            return "🟢 Good to have"

    # ── SKILL BREAKDOWN TABLE ─────────────────────────────
    st.subheader("🔍 Skill Breakdown")
    rows = []
    for skill, weight in sorted(
        score_data["weights"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        status = "✅ Matched" if skill in matched_skills else "❌ Missing"
        rows.append({
            "Skill"   : skill,
            "Priority": get_priority_label(weight),
            "Status"  : status,
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch",
        hide_index=True
    )

    # ── TOP MISSING SKILLS ────────────────────────────────
    st.subheader("🎯 Focus On These Missing Skills First")
    if score_data["top_missing"]:
        for i, skill in enumerate(score_data["top_missing"][:5], 1):
            weight = score_data["weights"].get(skill, 0)
            label  = get_priority_label(weight)
            st.write(f"{i}. **{skill}** — {label}")
    else:
        st.success("You matched all skills! 🎉")

    # ── LLM SUGGESTIONS ───────────────────────────────────
    suggestions = generate_resume_suggestions(
        matched_skills,
        missing_skills,
        job_description,
        raw_text
    )
    st.subheader("💡 How to Improve Your Resume")
    st.write(suggestions)

    os.remove(temp_path)