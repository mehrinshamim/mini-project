from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.db import _init_db, _conn, _put_conn
import os

app = FastAPI(title="Your App API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Import routes
from routes import auth, user, matching, jobs, documents

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(matching.router)
app.include_router(jobs.router)
app.include_router(documents.router)

@app.on_event("startup")
def startup():
    _init_db()
    # Initialize schema
    from utils.db import _conn, _put_conn
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            # Tables are created by SQL migration file
    finally:
        _put_conn(conn)

@app.get("/healthz")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)