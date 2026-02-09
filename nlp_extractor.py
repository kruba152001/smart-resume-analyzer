import spacy
import en_core_web_sm


nlp = spacy.load("en_core_web_sm")
def extract_candidate_terms(text: str) -> dict:
    doc = nlp(text)
    candidates = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()
        if len(phrase) > 1: 
            candidates.add(phrase)
    
    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"] and not token.is_stop:
            word = token.text.strip().lower()
            if len(word) > 2:
                candidates.add(word)
    return  candidates