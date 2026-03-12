import csv

import spacy
from spacy.matcher import PhraseMatcher
from aliases import normalize_with_aliases

nlp = spacy.load("en_core_web_sm")

# ─────────────────────────────────────────
#  Load Skills DB
# ─────────────────────────────────────────
def load_skills_db(path="Data/data.csv"):
    skills = set()
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            skill = row.get("skill", "").strip().lower()
            if skill:
                skills.add(skill)
    return skills

SKILLS_DB = load_skills_db()

# ─────────────────────────────────────────
#  Build PhraseMatcher from skills DB
#  Built ONCE at module load — efficient
# ─────────────────────────────────────────
def build_phrase_matcher(skills: set) -> PhraseMatcher:
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in skills]
    matcher.add("SKILLS", patterns)
    return matcher

PHRASE_MATCHER = build_phrase_matcher(SKILLS_DB)

# ─────────────────────────────────────────
#  Generic / Role words to filter out
# ─────────────────────────────────────────
GENERIC_WORDS = {
    "experience", "knowledge", "ability", "abilities", "preferred", "years", "year",
    "tasks", "task", "responsibility", "responsibilities", "process", "work", "working",
    "candidate", "role", "skills", "skill", "requirements", "requirement",
    "qualification", "qualifications", "familiarity", "proficiency", "proficient",
    "strong", "good", "excellent", "solid", "basic", "advanced", "understanding",
    "capability", "experienced", "knowledgeable",
}

ROLE_WORDS = {
    "developer", "engineer", "manager", "analyst", "lead", "intern", "architect"
}

# ─────────────────────────────────────────
#  Method 1: PhraseMatcher  (PRIMARY)
#  Fast, accurate, catches multi-word skills
# ─────────────────────────────────────────
def extract_with_phrase_matcher(text: str) -> set:
    doc = nlp(text)
    matches = PHRASE_MATCHER(doc)
    found = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found.add(span.text.lower())
    return found

# ─────────────────────────────────────────
#  Method 2: Noun chunk extraction (FALLBACK)
#  Catches skills that PhraseMatcher may miss
#  due to slight wording variations
# ─────────────────────────────────────────
def extract_candidate_terms(text: str) -> set:
    doc = nlp(text)
    candidates = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()
        if len(phrase) > 1:
            candidates.add(phrase)

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
        if len(term) < 3:
            continue
        if term in GENERIC_WORDS:
            continue
        is_role = any(role_word in term for role_word in ROLE_WORDS)
        if is_role:
            continue
        filtered.add(term)
    return filtered

# ─────────────────────────────────────────
#  Main extraction function
#  Called by ui.py — interface unchanged
# ─────────────────────────────────────────
def extract_skills_from_text(text: str) -> set:
    # Step 1: Normalize aliases FIRST (js → javascript, k8s → kubernetes etc.)
    text = normalize_with_aliases(text)

    # Step 2: PhraseMatcher — primary method
    phrase_matched = extract_with_phrase_matcher(text)

    # Step 3: Noun chunk fallback — catches anything PhraseMatcher missed
    raw_candidates = extract_candidate_terms(text)
    filtered_candidates = filter_candidate_terms(raw_candidates)
    fallback_skills = {
        term for term in filtered_candidates
        if term in SKILLS_DB
    }

    # Step 4: Combine both — union gives best coverage
    final_skills = phrase_matched | fallback_skills

    return final_skills