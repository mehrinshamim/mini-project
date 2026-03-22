import base64

from sqlmodel import Session

from app.core.db import engine
from app.models.models import Job, Resume
from app.services.discovery import DiscoveryService
from app.services.parsing import ParsingService
from app.worker.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)
def parse_resume_task(self, resume_id: int, pdf_b64: str) -> None:
    """Parse PDF bytes and update Resume.markdown_content."""
    try:
        pdf_bytes = base64.b64decode(pdf_b64)
        markdown = ParsingService.parse(pdf_bytes)
        with Session(engine) as session:
            resume = session.get(Resume, resume_id)
            if resume:
                resume.markdown_content = markdown
                session.add(resume)
                session.commit()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)


@celery_app.task(bind=True, max_retries=3)
def discover_jobs_task(self, user_id: int, title: str, location: str, limit: int = 20) -> None:
    """Scrape jobs via Apify and persist as Job records."""
    try:
        jobs = DiscoveryService.discover(title, location, limit)
        with Session(engine) as session:
            for job in jobs:
                session.add(
                    Job(
                        user_id=user_id,
                        title=job["title"],
                        company=job["company"],
                        description=job["description"],
                        url=job["url"],
                    )
                )
            session.commit()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)
