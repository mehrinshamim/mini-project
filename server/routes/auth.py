"""
Authentication using Supabase Auth (no manual password hashing)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from utils.supabase_client import supabase
import traceback

router = APIRouter(prefix="/api/auth", tags=["auth"])

class SignupRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str = ""
    location: str = ""

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: dict

@router.post("/signup", response_model=AuthResponse)
def signup(req: SignupRequest):
    """
    Sign up with Supabase Auth
    
    - Supabase handles password hashing & validation
    - Creates auth.users record automatically
    - Returns JWT tokens
    """
    try:
        # Create user with Supabase Auth
        res = supabase.auth.sign_up({
            "email": req.email,
            "password": req.password,
        })
        
        user_id = res.user.id  # UUID from Supabase
        
        # Store additional profile data in public.users table
        profile_data = {
            "id": user_id,
            "email": req.email,
            "first_name": req.first_name,
            "last_name": req.last_name,
            "phone": req.phone,
            "location": req.location,
        }
        
        # Insert into your users table (RLS policy allows users to insert own profile)
        supabase.table("users").insert(profile_data).execute()
        
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user": {
                "id": user_id,
                "email": req.email,
                "first_name": req.first_name,
                "last_name": req.last_name,
            }
        }
    
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg:
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=400, detail=f"Signup failed: {error_msg}")

@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest):
    """
    Login with Supabase Auth
    
    - Supabase validates password
    - Returns JWT tokens
    """
    try:
        # Authenticate with Supabase
        res = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password,
        })
        
        user_id = res.user.id
        
        # Fetch user profile from your users table
        user_profile = supabase.table("users").select("*").eq("id", user_id).single().execute()
        
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user": user_profile.data
        }
    
    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg or "not found" in error_msg:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        raise HTTPException(status_code=401, detail=f"Login failed: {error_msg}")

@router.post("/refresh")
def refresh_token(refresh_token: str):
    """
    Refresh expired access token using refresh token
    """
    try:
        res = supabase.auth.refresh_session(refresh_token)
        
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Failed to refresh token")

@router.post("/logout")
def logout(access_token: str):
    """
    Sign out user from Supabase
    """
    try:
        supabase.auth.sign_out(access_token)
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Logout failed: {str(e)}")