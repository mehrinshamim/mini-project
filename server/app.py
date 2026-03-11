"""
FastAPI server with Supabase Auth + PostgreSQL + Storage
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Your API with Supabase",
    version="0.1.0",
    description="FastAPI backend using Supabase Auth, PostgreSQL, and Storage"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize database on startup
@app.on_event("startup")
def startup():
    """Initialize database schema on startup"""
    from utils.db import _init_db, _conn, _put_conn
    
    _init_db()
    
    # Create tables if they don't exist
    conn = _conn()
    try:
        with conn.cursor() as cur:
            # pgvector extension
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # Users table (stores profile data, Supabase Auth handles passwords)
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id text PRIMARY KEY,
                    email text UNIQUE NOT NULL,
                    first_name text NOT NULL,
                    last_name text NOT NULL,
                    phone text,
                    location text,
                    urls jsonb DEFAULT '[]'::jsonb,
                    resume_url text,
                    resume_filename text,
                    created_at timestamptz NOT NULL DEFAULT now(),
                    updated_at timestamptz NOT NULL DEFAULT now()
                );
                """
            )
            
            # Resumes table (embeddings stored here)
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS resumes (
                    user_id text PRIMARY KEY,
                    resume_text text NOT NULL,
                    embedding vector(384),
                    resume_keywords text[],
                    resume_blob bytea,
                    resume_mime text,
                    resume_filename text,
                    updated_at timestamptz NOT NULL DEFAULT now()
                );
                """
            )
            
            # Create vector index for similarity search
            try:
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS resumes_embedding_idx ON resumes USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);"
                )
            except:
                pass
            
            # Job applications table
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS job_applications (
                    id text PRIMARY KEY,
                    user_id text NOT NULL,
                    company text NOT NULL,
                    title text NOT NULL,
                    location text,
                    source text,
                    url text,
                    status text NOT NULL DEFAULT 'saved',
                    notes text,
                    jd_text text,
                    next_action_date date,
                    created_at timestamptz NOT NULL DEFAULT now(),
                    updated_at timestamptz NOT NULL DEFAULT now()
                );
                """
            )
            
            cur.execute(
                "CREATE INDEX IF NOT EXISTS job_applications_user_idx ON job_applications (user_id, updated_at DESC);"
            )
            
            # Cover letters table
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS cover_letters (
                    id text PRIMARY KEY,
                    user_id text NOT NULL,
                    company text,
                    title text,
                    letter_text text NOT NULL,
                    letter_blob bytea,
                    letter_mime text,
                    filename text,
                    storage_url text,
                    created_at timestamptz NOT NULL DEFAULT now()
                );
                """
            )
    finally:
        _put_conn(conn)

# Import and include routers
from routes import auth, user, matching, jobs, documents

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(matching.router)
app.include_router(jobs.router)
app.include_router(documents.router)

# Health check
@app.get("/healthz")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)