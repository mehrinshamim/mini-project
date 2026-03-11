from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import jwt, os, uuid
from utils.db import _conn, _put_conn
from utils.pdf import render_text_to_pdf_stream

router = APIRouter(prefix="/api/documents", tags=["documents"])

class CoverLetterRequest(BaseModel):
    job_description: str
    company: Optional[str] = None
    title: Optional[str] = None
    use_llm: bool = False

@router.post("/cover-letter")
def generate_cover_letter(req: CoverLetterRequest, user_id: str = Depends(_current_user)):
    """Generate cover letter from JD"""
    conn = _conn()
    try:
        with conn.cursor() as cur:
            # Get user's resume
            cur.execute("SELECT resume_text FROM resumes WHERE user_id = %s", (user_id,))
            resume_row = cur.fetchone()
            if not resume_row:
                raise HTTPException(status_code=404, detail="No resume found")
            
            resume_text = resume_row[0]
            
            # Generate letter (using LLM if enabled)
            if req.use_llm:
                from utils.llm import generate_letter
                letter_text = generate_letter(resume_text, req.job_description, req.company, req.title)
            else:
                letter_text = f"Cover Letter for {req.company}\n\nDear Hiring Manager,\n\nI am interested in the {req.title} position..."
            
            # Generate PDF
            buffer, headers = render_text_to_pdf_stream(letter_text, "cover_letter.pdf")
            
            # Save to DB
            letter_id = str(uuid.uuid4())
            cur.execute(
                """INSERT INTO cover_letters 
                   (id, user_id, company, title, letter_text, letter_blob, letter_mime, filename)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (letter_id, user_id, req.company, req.title, letter_text, buffer.getvalue(),
                 "application/pdf", "cover_letter.pdf")
            )
            
            return StreamingResponse(buffer, media_type="application/pdf", headers=headers)
    finally:
        _put_conn(conn)