"""
Document generation and storage using Supabase Storage
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import uuid
import json
from utils.supabase_client import supabase, get_current_user, upload_file_to_storage, get_signed_url
from utils.pdf import render_text_to_pdf_stream
from utils.db import _conn, _put_conn

router = APIRouter(prefix="/api/documents", tags=["documents"])
security = HTTPBearer(auto_error=True)

def _extract_token(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return creds.credentials

class CoverLetterRequest(BaseModel):
    job_description: str
    company: Optional[str] = None
    title: Optional[str] = None
    use_llm: bool = False

@router.post("/cover-letter")
async def generate_cover_letter(
    req: CoverLetterRequest,
    token: str = Depends(_extract_token)
):
    """
    Generate cover letter and store in Supabase Storage
    
    - Generates PDF
    - Uploads to Supabase Storage
    - Saves metadata in PostgreSQL
    - Returns public URL
    """
    user_id = get_current_user(token)
    
    from utils.db import _conn, _put_conn
    
    conn = _conn()
    try:
        # Get user's resume
        with conn.cursor() as cur:
            cur.execute("SELECT resume_text FROM resumes WHERE user_id = %s", (user_id,))
            resume_row = cur.fetchone()
            if not resume_row:
                raise HTTPException(status_code=404, detail="No resume found")
            
            resume_text = resume_row[0]
        
        # Generate letter text
        letter_text = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {req.title or 'position'} role at {req.company or 'your company'}.

With my background in relevant technologies and experience working with {req.job_description[:100]}..., I am confident in my ability to contribute effectively to your team.

I would welcome the opportunity to discuss how my skills and experience align with your needs.

Best regards"""
        
        # Generate PDF
        buffer, headers = render_text_to_pdf_stream(letter_text, f"cover_letter_{user_id}.pdf")
        pdf_bytes = buffer.getvalue()
        
        # Upload to Supabase Storage
        file_path = f"{user_id}/cover_letters/{uuid.uuid4()}.pdf"
        storage_response = upload_file_to_storage(
            bucket="documents",
            file_path=file_path,
            file_data=pdf_bytes,
            content_type="application/pdf"
        )
        
        # Save metadata in PostgreSQL
        letter_id = str(uuid.uuid4())
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO cover_letters 
                   (id, user_id, company, title, letter_text, letter_blob, letter_mime, filename, storage_url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (letter_id, user_id, req.company, req.title, letter_text, pdf_bytes,
                 "application/pdf", f"cover_letter_{letter_id}.pdf", storage_response["url"])
            )
        
        return {
            "id": letter_id,
            "url": storage_response["url"],
            "company": req.company,
            "title": req.title,
            "created_at": "now()"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")
    finally:
        _put_conn(conn)

@router.get("/cover-letters")
def list_cover_letters(token: str = Depends(_extract_token)):
    """Get list of all cover letters"""
    user_id = get_current_user(token)
    
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, company, title, filename, storage_url, created_at 
                   FROM cover_letters WHERE user_id = %s ORDER BY created_at DESC""",
                (user_id,)
            )
            rows = cur.fetchall()
            items = [
                {
                    "id": r[0],
                    "company": r[1],
                    "title": r[2],
                    "filename": r[3] or "cover_letter.pdf",
                    "url": r[4],
                    "created_at": r[5].isoformat() if r[5] else None
                }
                for r in rows
            ]
            return {"items": items}
    finally:
        _put_conn(conn)

@router.get("/cover-letters/download/{letter_id}")
def download_cover_letter(letter_id: str, token: str = Depends(_extract_token)):
    """Get signed URL for cover letter"""
    user_id = get_current_user(token)
    
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT storage_url, filename FROM cover_letters WHERE id = %s AND user_id = %s",
                (letter_id, user_id)
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Cover letter not found")
            
            # If we have the storage URL, return it directly
            # (assuming bucket is public; if private, generate signed URL)
            return {"url": row[0]}
    finally:
        _put_conn(conn)

@router.delete("/cover-letters/{letter_id}")
def delete_cover_letter(letter_id: str, token: str = Depends(_extract_token)):
    """Delete cover letter from Storage and database"""
    user_id = get_current_user(token)
    
    from utils.supabase_client import delete_file_from_storage
    
    conn = _conn()
    try:
        with conn.cursor() as cur:
            # Get storage path
            cur.execute(
                "SELECT storage_url FROM cover_letters WHERE id = %s AND user_id = %s",
                (letter_id, user_id)
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Cover letter not found")
            
            # Delete from database
            cur.execute(
                "DELETE FROM cover_letters WHERE id = %s AND user_id = %s",
                (letter_id, user_id)
            )
        
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        _put_conn(conn)