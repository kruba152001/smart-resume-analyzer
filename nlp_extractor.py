import spacy

nlp = spacy.load("en_core_web_sm")
def load_skills_db(path="Data/data.txt"):
    skills = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            skill = line.strip().lower()
            if skill:
                skills.add(skill)
    return skills


SKILLS_DB = load_skills_db()

GENERIC_WORDS = {
        "experience", "knowledge", "ability", "abilities", "preferred", "years", "year",
        "tasks", "task", "responsibility", "responsibilities", "process", "work", "working",
        "candidate", "role" , "skills", "skill", "requirements", "requirement", "qualification", "qualifications",
        "familiarity", "proficiency", "proficient", "strong", "good", "excellent", "solid", "basic", "advanced", "understanding", "understand", "ability", "capability", "experience", "experienced", "knowledge", "knowledgeable",
}

ROLE_WORDS = {
    "developer", "engineer", "manager", "analyst", "lead", "intern", "architect"
}

def extract_candidate_terms(text: str) -> set:
    doc = nlp(text)
    candidates = set()

    # Noun phrases (e.g., "machine learning", "rest api")
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()
        if len(phrase) > 1:
            candidates.add(phrase)

    # Single important words (nouns / proper nouns)
    for token in doc:
        if token.pos_ in {"PROPN", "NOUN"} and not token.is_stop:
            word = token.text.strip().lower()
            if len(word) > 2:
                candidates.add(word)

    return candidates


def filter_candidate_terms(terms: set) -> set:
    filtered = set()

    for term in terms:
        term = term.strip().lower()

        # Rule 1: skip very short terms
        if len(term) < 3:
            continue

        # Rule 2: skip generic junk words
        if term in GENERIC_WORDS:
            continue

        # Rule 3: skip role words (e.g., "backend developer")
        is_role = False
        for role_word in ROLE_WORDS:
            if role_word in term:
                is_role = True
                break

        if is_role:
            continue

        # If it passed all filters, keep it
        filtered.add(term)

    return filtered
def extract_skills_from_text(text: str) -> set:
    # 1. Extract candidate terms using spaCy
    raw_candidates = extract_candidate_terms(text)

    # 2. Filter junk terms
    filtered_candidates = filter_candidate_terms(raw_candidates)

    # 3. Keep only terms that exist in skills dataset
    final_skills = set()
    for term in filtered_candidates:
        term_clean = term.strip().lower()
        if term_clean in SKILLS_DB:
            final_skills.add(term_clean)

    return final_skills