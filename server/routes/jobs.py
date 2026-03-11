from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import jwt, os, uuid
from utils.db import _conn, _put_conn
from datetime import datetime

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

class JobCreate(BaseModel):
    company: str
    title: str
    location: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = "saved"
    notes: Optional[str] = None
    jd_text: Optional[str] = None

@router.post("/")
def create_job(req: JobCreate, user_id: str = Depends(_current_user)):
    """Create job tracker entry"""
    job_id = str(uuid.uuid4())
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO job_applications 
                   (id, user_id, company, title, location, source, url, status, notes, jd_text) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (job_id, user_id, req.company, req.title, req.location, req.source,
                 req.url, req.status, req.notes, req.jd_text)
            )
        return {"id": job_id, "status": "saved"}
    finally:
        _put_conn(conn)

@router.get("/")
def get_jobs(user_id: str = Depends(_current_user)):
    """Get all jobs for user"""
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, company, title, location, status, url, created_at 
                   FROM job_applications WHERE user_id = %s ORDER BY updated_at DESC""",
                (user_id,)
            )
            jobs = cur.fetchall()
            return [
                {
                    "id": j[0], "company": j[1], "title": j[2], "location": j[3],
                    "status": j[4], "url": j[5], "created_at": j[6].isoformat()
                }
                for j in jobs
            ]
    finally:
        _put_conn(conn)

@router.patch("/{job_id}")
def update_job(job_id: str, updates: dict, user_id: str = Depends(_current_user)):
    """Update job status"""
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE job_applications SET status = %s, updated_at = now() WHERE id = %s AND user_id = %s",
                (updates.get("status"), job_id, user_id)
            )
        return {"ok": True}
    finally:
        _put_conn(conn)