import fitz  # PyMuPDF
import docx
import io
from transformers import pipeline
import re
import spacy

# Load NER models
nlp_small = spacy.load("en_core_web_sm")
ner_trf = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

def extract_text_from_pdf(file_bytes):
    text = ""
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)

def extract_resume_data(text):
    # Entities with spaCy
    doc = nlp_small(text)
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "Not Found")

    # Email & phone regex
    email = next(iter(re.findall(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+", text)), "Not Found")
    phone = next(iter(re.findall(r"\+?\d[\d\s\-()]{8,}\d", text)), "Not Found")

    # Transformer NER (job titles, orgs, etc.)
    ner_results = ner_trf(text[:10000])  # limit length
    roles = list({ent['word'] for ent in ner_results if ent['entity_group'] in ("PER", "ORG", "MISC")})

    # Skill extraction
    known_skills = [
        "python", "java", "c++", "html", "css", "javascript",
        "sql", "excel", "machine learning", "deep learning",
        "flask", "django", "react", "node.js", "pandas", "numpy",
        "git", "linux", "communication", "teamwork"
    ]
    skills = [s for s in known_skills if s.lower() in text.lower()]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "roles": roles,
        "skills": skills
    }

def parse_resume(file_bytes, filename):
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format")

    parsed = extract_resume_data(text)
    return parsed, text  # return both
