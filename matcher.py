from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_semantic_score(resume_text: str, jd_text: str) -> float:
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(jd_text, convert_to_tensor=True)
    sim = util.cos_sim(emb1, emb2).item()
    return round(sim * 100, 2)

def compute_skill_score(resume_skills, jd_skills):
    resume_set = set(map(str.lower, resume_skills))
    jd_set = set(map(str.lower, jd_skills))
    if not jd_set:
        return 0
    matched = resume_set & jd_set
    return round(len(matched) / len(jd_set) * 100, 2)

def compute_final_score(resume_text, resume_skills, jd_text):
    jd_skills = ["python", "sql", "html", "css", "teamwork", "communication"]

    semantic_score = compute_semantic_score(resume_text, jd_text)
    skill_score = compute_skill_score(resume_skills, jd_skills)

    final = round((semantic_score * 0.8 + skill_score * 0.7), 2)
    return final

