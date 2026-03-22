from fastapi import FastAPI

from app.api import jobs, resumes
from app.core.db import create_db_and_tables, seed_default_user

app = FastAPI(title="Job Autofiller API", version="2.0.0")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_default_user()


app.include_router(resumes.router)
app.include_router(jobs.router)


@app.get("/health")
def health():
    return {"status": "ok"}
