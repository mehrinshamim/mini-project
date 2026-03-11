"""
User profile management with Supabase
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import uuid
from utils.supabase_client import supabase, get_current_user, upload_file_to_storage, delete_file_from_storage
from utils.embeddings import embed_and_store_resume
from pdfminer.high_level import extract_text
from io import BytesIO

router = APIRouter(prefix="/api/user", tags=["user"])
security = HTTPBearer(auto_error=True)

def _extract_token(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return creds.credentials

class UserProfile(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    urls: Optional[list] = None
    resume_url: Optional[str] = None
    updated_at: Optional[str] = None

@router.get("/profile", response_model=UserProfile)
def get_user(token: str = Depends(_extract_token)):
    """Get user profile from Supabase"""
    user_id = get_current_user(token)
    
    try:
        # Fetch from public.users table
        response = supabase.table("users").select("*").eq("id", user_id).single().execute()
        user_data = response.data
        
        return UserProfile(**user_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

@router.patch("/profile")
async def update_user(
    token: str = Depends(_extract_token),
    first_name: str = Form(None),
    last_name: str = Form(None),
    phone: str = Form(None),
    location: str = Form(None),
    urls: str = Form(None),
    resume: UploadFile = File(None)
):
    """
    Update user profile and optionally upload resume
    
    - Uses Supabase Storage for resume file
    - Stores metadata in public.users table
    - Embeds resume and stores in PostgreSQL resumes table
    """
    user_id = get_current_user(token)
    
    try:
        updates = {}
        
        # Update basic profile fields
        if first_name:
            updates["first_name"] = first_name
        if last_name:
            updates["last_name"] = last_name
        if phone:
            updates["phone"] = phone
        if location:
            updates["location"] = location
        if urls:
            updates["urls"] = urls
        
        # Handle resume upload
        resume_url = None
        if resume:
            # Read file
            content = await resume.read()
            
            # Extract text from PDF
            resume_text = extract_text(BytesIO(content))
            
            # Upload to Supabase Storage (bucket: 'resumes')
            file_path = f"{user_id}/{resume.filename}"
            storage_response = upload_file_to_storage(
                bucket="resumes",
                file_path=file_path,
                file_data=content,
                content_type=resume.content_type or "application/pdf"
            )
            resume_url = storage_response["url"]
            
            # Embed and store in PostgreSQL
            embed_and_store_resume(
                user_id=user_id,
                resume_text=resume_text,
                blob=content,
                mime=resume.content_type,
                filename=resume.filename
            )
            
            # Update resume URL in user profile
            updates["resume_url"] = resume_url
            updates["resume_filename"] = resume.filename
        
        # Update user record in public.users table
        if updates:
            supabase.table("users").update(updates).eq("id", user_id).execute()
        
        return {"ok": True, "resume_url": resume_url}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

@router.get("/resume")
def get_resume(token: str = Depends(_extract_token)):
    """Get resume text from PostgreSQL"""
    user_id = get_current_user(token)
    
    from utils.db import _conn, _put_conn
    
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT resume_text FROM resumes WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="No resume found")
            return {"resume_text": row[0]}
    finally:
        _put_conn(conn)

@router.get("/resume/download")
def download_resume(token: str = Depends(_extract_token)):
    """
    Get signed URL for resume from Supabase Storage
    (expires in 1 hour)
    """
    user_id = get_current_user(token)
    
    try:
        # Get user profile to find resume filename
        user = supabase.table("users").select("resume_filename").eq("id", user_id).single().execute()
        
        if not user.data or not user.data.get("resume_filename"):
            raise HTTPException(status_code=404, detail="No resume found")
        
        file_path = f"{user_id}/{user.data['resume_filename']}"
        
        # Generate signed URL
        from utils.supabase_client import get_signed_url
        signed_url = get_signed_url(bucket="resumes", file_path=file_path, expires_in=3600)
        
        return {"url": signed_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {str(e)}")

@router.delete("/resume")
def delete_resume(token: str = Depends(_extract_token)):
    """Delete resume from Storage and PostgreSQL"""
    user_id = get_current_user(token)
    
    from utils.db import _conn, _put_conn
    
    try:
        # Get filename from user profile
        user = supabase.table("users").select("resume_filename").eq("id", user_id).single().execute()
        
        if user.data and user.data.get("resume_filename"):
            file_path = f"{user_id}/{user.data['resume_filename']}"
            # Delete from Storage
            delete_file_from_storage(bucket="resumes", file_path=file_path)
        
        # Delete from PostgreSQL
        conn = _conn()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM resumes WHERE user_id = %s", (user_id,))
        finally:
            _put_conn(conn)
        
        # Clear resume URL in user profile
        supabase.table("users").update({
            "resume_url": None,
            "resume_filename": None
        }).eq("id", user_id).execute()
        
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")