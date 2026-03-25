from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Resume(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    filename: str
    markdown_content: str  # Docling PDF -> Markdown output
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    company: str
    description: str
    url: Optional[str] = None
    score: Optional[int] = None          # 1-10 from Groq
    fit_reasoning: Optional[str] = None  # Groq explanation
    status: str = Field(default="pending")  # pending | scored | applied
    created_at: datetime = Field(default_factory=datetime.utcnow)


class JobSearch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    location: str
    task_id: str = Field(default="")  # Celery task UUID, set after enqueue
    created_at: datetime = Field(default_factory=datetime.utcnow)


class JobSearchResult(SQLModel, table=True):
    search_id: int = Field(foreign_key="jobsearch.id", primary_key=True)
    job_id: int = Field(foreign_key="job.id", primary_key=True)
