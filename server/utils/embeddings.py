import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.db import _conn, _put_conn
import uuid

model = SentenceTransformer('all-MiniLM-L6-v2')

def _embed(text: str) -> np.ndarray:
    return np.asarray(model.encode(text), dtype=np.float32)

def _normalize(vec: np.ndarray) -> np.ndarray:
    v = vec.astype(np.float32, copy=True)
    norm = float(np.linalg.norm(v))
    return v / norm if norm != 0.0 else v

def embed_and_store_resume(user_id: str, resume_text: str, blob=None, mime=None, filename=None):
    """Embed and store resume in pgvector"""
    embedding = _normalize(_embed(resume_text))
    keywords = extract_keywords(resume_text, "")
    
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO resumes (user_id, resume_text, embedding, resume_keywords, resume_blob, resume_mime, resume_filename)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (user_id) DO UPDATE SET 
                   resume_text = %s, embedding = %s, resume_keywords = %s, resume_blob = %s""",
                (user_id, resume_text, embedding, keywords, blob, mime, filename,
                 resume_text, embedding, keywords, blob)
            )
    finally:
        _put_conn(conn)

def compute_similarity(resume_embedding, job_description: str):
    """Compute cosine similarity between resume and JD"""
    jd_embedding = _normalize(_embed(job_description))
    
    # Cosine similarity via dot product (vectors are normalized)
    score = float(np.dot(resume_embedding, jd_embedding))
    percent = max(0, score * 100)
    
    return score, percent

def extract_keywords(resume_text: str, jd_text: str):
    """Extract matching and missing tech keywords"""
    tech_keywords = {
        "Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript",
        "React", "Vue", "Angular", "Django", "FastAPI", "Spring",
        "AWS", "GCP", "Azure", "Docker", "Kubernetes", "PostgreSQL"
    }
    
    resume_words = set(word.lower() for word in resume_text.split() if len(word) > 3)
    jd_words = set(word.lower() for word in jd_text.split() if len(word) > 3)
    
    matching = [kw for kw in tech_keywords if kw.lower() in resume_words and kw.lower() in jd_words]
    missing = [kw for kw in tech_keywords if kw.lower() in jd_words and kw.lower() not in resume_words]
    
    return matching, missing