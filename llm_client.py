import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

Hf_TOKEN = os.environ.get("HF_TOKEN")

if not Hf_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables.")

client = InferenceClient(api_key=Hf_TOKEN)

MODEL_ID = "swiss-ai/Apertus-8B-Instruct-2509"


def generate_resume_suggestions(matched_skills, missing_skills, jd_text, resume_text) -> str:
    """
    Generate human-readable suggestions to improve the resume
    based on matched and missing skills.
    """

    prompt = f"""
You are a helpful career assistant. Only base your advice on the provided job description,
 resume text, and skill lists. Do not invent new technologies.

Job Description:
{jd_text}

Resume:
{resume_text}

Matched skills:
{", ".join(sorted(matched_skills)) if matched_skills else "None"}

Missing skills:
{", ".join(sorted(missing_skills)) if missing_skills else "None"}

Give:
1. A short assessment of the candidate's fit.
2. Clear suggestions on how to improve the resume.
3. Which missing skills to focus on first.

Keep the answer concise and practical.
"""

    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=1024
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    matched = {"python", "git", "docker"}
    missing = {"kubernetes", "postgresql"}

    jd_text = "We need a backend engineer with Python, Docker, Kubernetes, and PostgreSQL."
    resume_text = "I have experience with Python, Git, and Docker."

    print(generate_resume_suggestions(matched, missing, jd_text, resume_text))