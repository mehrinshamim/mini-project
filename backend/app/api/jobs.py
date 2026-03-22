from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.db import get_session
from app.models.models import Job
from app.worker.tasks import discover_jobs_task

router = APIRouter(prefix="/jobs", tags=["jobs"])


class DiscoverRequest(BaseModel):
    user_id: int
    title: str
    location: str
    limit: int = 20


@router.post("/discover")
def discover_jobs(body: DiscoverRequest):
    task = discover_jobs_task.delay(body.user_id, body.title, body.location, body.limit)
    return {"task_id": task.id, "status": "discovering"}


@router.get("/")
def list_jobs(user_id: int, session: Session = Depends(get_session)):
    jobs = session.exec(select(Job).where(Job.user_id == user_id)).all()
    return jobs
