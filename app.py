from resume_parser import clean_text, extract_skills, extract_text_from_pdf
#from flask import Flask, request, jsonify  

resume_path = "D:\smart resume analyser\sample resume\sample_resume.pdf"
raw_text = extract_text_from_pdf(resume_path)
cleaned_text = clean_text(raw_text)

job_skills = set(["python", "java", "git", "sql", "javascript", "html", "css", "aws", "docker", "kubernetes"])
matched_skills = extract_skills(cleaned_text, job_skills)
print("Matched Skills:", matched_skills)
matched_percentage = (len(matched_skills) / len(job_skills)) * 100
print(f"Matched Skills Percentage: {matched_percentage:.2f}%")

missing_skills = job_skills - set(matched_skills)
print("Missing Skills:", missing_skills)
if matched_percentage >=70:
    print("The candidate is a good fit for the job.")
elif matched_percentage >= 40:
    print("The candidate is a moderate fit for the job.")       
else:    print("The candidate is a poor fit for the job.")