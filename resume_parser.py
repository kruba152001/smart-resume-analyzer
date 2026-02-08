import pdfplumber
import re 

def extract_text_from_pdf(file_path):
    page_texts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                page_texts.append(text)
    return "\n".join(page_texts)

def clean_text(text:str)-> str:
    text=text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text=' '.join(text.split())
    return text

def extract_skills(text: str, skills_list: set) -> list:
    found_skills = set()
    for skill in skills_list:
        if skill in text:
            found_skills.add(skill)
    return list(found_skills)