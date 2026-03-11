from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt, bcrypt, uuid, os
from utils.db import _conn, _put_conn

router = APIRouter(prefix="/api/auth", tags=["auth"])
JWT_KEY = os.getenv("JWT_KEY", "dev-secret")
JWT_EXPIRES_IN_MIN = int(os.getenv("JWT_EXPIRES_IN_MIN", 60))

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str = ""
    location: str = ""

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(req: SignupRequest):
    """Create new user account"""
    user_id = str(uuid.uuid4())
    password_hash = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt(12)).decode()
    
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO users 
                   (id, first_name, last_name, email, password_hash, phone, location) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (user_id, req.first_name, req.last_name, req.email, password_hash, 
                 req.phone, req.location)
            )
        token = jwt.encode(
            {"_id": user_id, "email": req.email},
            JWT_KEY, algorithm="HS256"
        )
        return {"token": token, "user": {"id": user_id, "email": req.email}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signup failed: {str(e)}")
    finally:
        _put_conn(conn)

@router.post("/login")
def login(req: LoginRequest):
    """Login with email and password"""
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (req.email,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            user_id, password_hash = row
            if not bcrypt.checkpw(req.password.encode(), password_hash.encode()):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
        token = jwt.encode({"_id": user_id, "email": req.email}, JWT_KEY, algorithm="HS256")
        return {"token": token}
    finally:
        _put_conn(conn)