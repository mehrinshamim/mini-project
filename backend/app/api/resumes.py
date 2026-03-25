import base64

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session

from app.core.db import get_session
from app.models.models import Resume
from app.worker.tasks import parse_resume_task

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload")
async def upload_resume(
    user_id: int,
    file: UploadFile,
    session: Session = Depends(get_session),
):
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    pdf_bytes = await file.read()

    resume = Resume(user_id=user_id, filename=file.filename, markdown_content="")
    session.add(resume)
    session.commit()
    session.refresh(resume)

    parse_resume_task.delay(resume.id, base64.b64encode(pdf_bytes).decode())

    return {"resume_id": resume.id, "status": "parsing"}


@router.get("/{resume_id}")
def get_resume(resume_id: int, session: Session = Depends(get_session)):
    resume = session.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    return resume
