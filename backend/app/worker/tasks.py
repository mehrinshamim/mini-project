import base64
import re
import time

import groq
from sqlmodel import Session, select

from app.core.db import engine
from app.models.models import Job, Resume
from app.services.discovery import DiscoveryService
from app.services.parsing import ParsingService
from app.services.reasoning import ReasoningService
from app.worker.celery_app import celery_app


def _parse_retry_after(exc: groq.RateLimitError) -> int:
    """Extract wait seconds from a Groq RateLimitError.

    Primary: retry-after response header (integer seconds).
    Fallback: parse human-readable message string.
    Last resort: 300 seconds.
    """
    try:
        val = exc.response.headers.get("retry-after")
        if val:
            return int(float(val)) + 5
    except (AttributeError, ValueError, TypeError):
        pass
    m = re.search(r"try again in (?:(\d+)m\s*)?(\d+(?:\.\d+)?)s", str(exc))
    if m:
        return int(int(m.group(1) or 0) * 60 + float(m.group(2))) + 5
    return 300


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
def discover_jobs_task(self, user_id: int, title: str, location: str, limit: int = 20, search_id: int | None = None) -> None:
    """Scrape jobs via Apify and persist as Job records, deduplicating by (user_id, url)."""
    from app.models.models import JobSearchResult
    try:
        jobs = DiscoveryService.discover(title, location, limit)
        with Session(engine) as session:
            for job in jobs:
                url = job["url"]
                existing = session.exec(
                    select(Job).where(Job.user_id == user_id, Job.url == url)
                ).first() if url else None

                if existing:
                    job_id = existing.id
                else:
                    new_job = Job(
                        user_id=user_id,
                        title=job["title"],
                        company=job["company"],
                        description=job["description"],
                        url=url,
                    )
                    session.add(new_job)
                    session.flush()
                    job_id = new_job.id

                if search_id is not None:
                    session.merge(JobSearchResult(search_id=search_id, job_id=job_id))

            session.commit()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)


@celery_app.task(bind=True, max_retries=10)
def score_jobs_task(self, job_ids: list[int], resume_id: int) -> None:
    """Score a list of jobs serially against one resume. One Groq call at a time."""
    try:
        with Session(engine) as session:
            resume = session.get(Resume, resume_id)
            if not resume:
                return

            for i, job_id in enumerate(job_ids):
                job = session.get(Job, job_id)
                if not job:
                    continue
                if i > 0:
                    time.sleep(8)  # 12K TPM limit / ~1500 tokens per call ≈ 8 calls/min
                result = ReasoningService.score(resume.markdown_content, job.description)
                job.score = result.score
                job.fit_reasoning = result.fit_reasoning
                job.status = "scored"
                session.add(job)
                session.commit()  # commit per job so partial progress survives a retry
    except groq.RateLimitError as exc:
        raise self.retry(exc=exc, countdown=_parse_retry_after(exc))
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)
