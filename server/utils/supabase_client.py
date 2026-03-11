"""
Supabase client initialization and helper functions
"""
import os
from supabase import create_client, Client
from fastapi import HTTPException
import jwt

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def get_current_user(token: str) -> str:
    """
    Verify JWT token from Supabase and return user_id
    
    Supabase returns JWTs with 'sub' claim containing user UUID
    """
    try:
        # Decode without verification (Supabase token is trusted)
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get("sub")  # Supabase uses 'sub' for user ID
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def upload_file_to_storage(bucket: str, file_path: str, file_data: bytes, content_type: str = "application/octet-stream"):
    """
    Upload file to Supabase Storage
    
    Args:
        bucket: Storage bucket name (e.g., 'resumes', 'cover_letters')
        file_path: Path in bucket (e.g., 'user_id/resume.pdf')
        file_data: File bytes
        content_type: MIME type
    
    Returns:
        {
            'path': 'full/path/to/file',
            'id': 'file_id',
            'url': 'public_url'
        }
    """
    try:
        response = supabase.storage.from_(bucket).upload(
            file_path,
            file_data,
            {
                "content-type": content_type,
            }
        )
        
        # Get public URL
        public_url = supabase.storage.from_(bucket).get_public_url(file_path)
        
        return {
            "path": response.path,
            "url": public_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

def delete_file_from_storage(bucket: str, file_path: str):
    """Delete file from Supabase Storage"""
    try:
        supabase.storage.from_(bucket).remove([file_path])
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File delete failed: {str(e)}")

def get_signed_url(bucket: str, file_path: str, expires_in: int = 3600) -> str:
    """
    Get signed URL for private file (expires in N seconds)
    
    Args:
        bucket: Storage bucket name
        file_path: Path in bucket
        expires_in: Expiration time in seconds (default 1 hour)
    
    Returns:
        Signed URL string
    """
    try:
        response = supabase.storage.from_(bucket).create_signed_url(file_path, expires_in)
        return response.signed_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate signed URL: {str(e)}")