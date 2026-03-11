from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import jwt, os
from utils.db import _conn, _put_conn
from utils.embeddings import compute_similarity, extract_keywords

router = APIRouter(prefix="/api/match", tags=["matching"])
security = HTTPBearer(auto_error=True)
JWT_KEY = os.getenv("JWT_KEY", "dev-secret")

class MatchRequest(BaseModel):
    jobDescription: str

def _current_user(creds) -> str:
    try:
        payload = jwt.decode(creds.credentials, JWT_KEY, algorithms=["HS256"])
        return payload.get("_id")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/")
def match_resume(req: MatchRequest, user_id: str = Depends(_current_user)):
    """Compute resume-to-JD match score"""
    if not req.jobDescription.strip():
        raise HTTPException(status_code=400, detail="jobDescription required")
    
    conn = _conn()
    try:
        with conn.cursor() as cur:
            # Get user's resume embedding from pgvector
            cur.execute(
                "SELECT resume_text, embedding FROM resumes WHERE user_id = %s", 
                (user_id,)
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="No resume found")
            
            resume_text, resume_embedding = row
            
            # Compute similarity
            score, percent = compute_similarity(resume_embedding, req.jobDescription)
            
            # Extract keywords
            matching_words, missing_words = extract_keywords(resume_text, req.jobDescription)
            
            return {
                "score": float(score),
                "percent": round(float(percent), 2),
                "matchingWords": matching_words,
                "missingWords": missing_words
            }
    finally:
        _put_conn(conn)