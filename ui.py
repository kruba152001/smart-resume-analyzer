import streamlit as st
import tempfile
import os
from resume_parser import clean_text, extract_skills_nlp, extract_text_from_pdf
from nlp_extractor import extract_candidate_terms , filter_candidate_terms

from nlp_extractor import extract_skills_from_text

st.set_page_config(page_title="Smart Resume Analyzer", layout="centered")

st.title("🧠 Smart Resume Analyzer")
st.write("Upload your resume and see how well it matches the job requirements.")
st.subheader("Paste Job Description")
job_description = st.text_area("Enter the job description here", height=200)
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    st.success("Resume uploaded successfully!")

    # Now process the resume
    raw_text = extract_text_from_pdf(temp_path)
    cleaned_text = clean_text(raw_text)
    # Make sure user entered a Job Description
    if not job_description.strip():
        st.warning("Please paste a Job Description to analyze against.")
        st.stop()

    # Clean the job description text
    cleaned_jd = clean_text(job_description)

    # Extract candidate skills from Job Description using NLP
    # raw_jd_terms = extract_candidate_terms(cleaned_jd)
    # job_skills = filter_candidate_terms(raw_jd_terms)
    job_skills = extract_skills_from_text(cleaned_jd)

    # Safety check: if NLP finds nothing useful
    if not job_skills:
        st.warning("Could not extract skills from the Job Description. Please provide a more detailed JD.")
        st.stop()


    # Define job skills (for now, same as before)
    # job_skills = {
    #     "python", "java", "sql", "javascript", "html", "css",
    #     "aws", "docker", "kubernetes", "git"
    # }

    # matched_skills = extract_skills_nlp(cleaned_text, job_skills)
    resume_skills = extract_skills_from_text(cleaned_text)

    matched_skills = resume_skills.intersection(job_skills)

    # Calculate match percentage
    match_percentage = (len(matched_skills) / len(job_skills)) * 100

    # Calculate missing skills
    missing_skills = job_skills - set(matched_skills)

    # Decision message
    if match_percentage >= 70:
        decision_message = "The candidate is a good fit for the job."
    elif match_percentage >= 40:
        decision_message = "The candidate is a partial match and needs improvement."
    else:
        decision_message = "The candidate is a low match for the job."

    # Display results
    st.subheader("Results")
    st.subheader("Matched Skills")
    for skill in sorted(matched_skills):
        st.write(f"• {skill}")

    st.subheader("Missing Skills")
    if missing_skills:
        for skill in sorted(missing_skills):
            st.write(f"• {skill}")
    else:
        st.write("None 🎉")
    st.write(f"Matched Skills Percentage: {match_percentage:.2f}%")
   
    st.write("Decision:", decision_message)

    # Clean up temp file
    os.remove(temp_path)
