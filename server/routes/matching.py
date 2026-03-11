"""
Resume-to-job matching (NO CHANGES - same as before)
Uses PostgreSQL pgvector for embeddings
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from utils.supabase_client import get_current_user
from utils.embeddings import compute_similarity, extract_keywords
from utils.db import _conn, _put_conn

router = APIRouter(prefix="/api/match", tags=["matching"])
security = HTTPBearer(auto_error=True)

def _extract_token(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return creds.credentials

class MatchRequest(BaseModel):
    jobDescription: str

@router.post("/")
def match_resume(
    req: MatchRequest,
    token: str = Depends(_extract_token)
):
    """Compute resume-to-JD match score using pgvector"""
    user_id = get_current_user(token)
    
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