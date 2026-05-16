import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    
    keywords = [
        token.text for token in doc
        if not token.is_stop and not token.is_punct and token.is_alpha
    ]
    return list(set(keywords))[:5]