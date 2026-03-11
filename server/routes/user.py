from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt, os
from utils.db import _conn, _put_conn
from utils.embeddings import embed_and_store_resume

router = APIRouter(prefix="/api/user", tags=["user"])
security = HTTPBearer(auto_error=True)
JWT_KEY = os.getenv("JWT_KEY", "dev-secret")

def _current_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(creds.credentials, JWT_KEY, algorithms=["HS256"])
        return payload.get("_id")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/profile")
def get_user(user_id: str = Depends(_current_user)):
    """Get user profile"""
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, first_name, last_name, email, phone, location, urls FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="User not found")
            return {
                "id": row[0], "first_name": row[1], "last_name": row[2],
                "email": row[3], "phone": row[4], "location": row[5], "urls": row[6]
            }
    finally:
        _put_conn(conn)

@router.patch("/profile")
async def update_user(
    user_id: str = Depends(_current_user),
    first_name: str = Form(None),
    last_name: str = Form(None),
    phone: str = Form(None),
    location: str = Form(None),
    urls: str = Form(None),
    resume: UploadFile = File(None)
):
    """Update user profile and optionally upload resume"""
    conn = _conn()
    try:
        if resume:
            # Parse and embed resume
            content = await resume.read()
            from pdfminer.high_level import extract_text
            from io import BytesIO
            resume_text = extract_text(BytesIO(content))
            
            embed_and_store_resume(user_id, resume_text, content, resume.content_type, resume.filename)
        
        # Update user fields
        with conn.cursor() as cur:
            updates = []
            params = []
            if first_name:
                updates.append("first_name = %s")
                params.append(first_name)
            if last_name:
                updates.append("last_name = %s")
                params.append(last_name)
            if phone:
                updates.append("phone = %s")
                params.append(phone)
            if location:
                updates.append("location = %s")
                params.append(location)
            if urls:
                updates.append("urls = %s::jsonb")
                params.append(urls)
            
            if updates:
                params.append(user_id)
                cur.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = %s", tuple(params))
        
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        _put_conn(conn)

@router.get("/resume")
def get_resume(user_id: str = Depends(_current_user)):
    """Get resume text"""
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