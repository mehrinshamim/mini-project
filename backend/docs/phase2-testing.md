# Phase 2 Testing Guide

Manual steps to verify ParsingService, DiscoveryService, and Celery tasks are working.

## Prerequisites
- `.env` filled with real `GROQ_API_KEY` and `APIFY_API_TOKEN`
- Docker running with `db` and `redis` containers up
- A sample PDF resume on your machine

---

## Step 1 — Start infrastructure
```bash
docker-compose up -d db redis
```

## Step 2 — Start the Celery worker (separate terminal)
```bash
uv run celery -A app.worker.celery_app worker --loglevel=info
```
You should see:
```
[tasks]
  . app.worker.tasks.parse_resume_task
  . app.worker.tasks.discover_jobs_task
```

## Step 3 — Start the API server (separate terminal)
```bash
uv run uvicorn app.main:app --reload
```

---

## Test A — Resume Upload & Parsing

### Upload a PDF
```bash
curl -X POST "http://localhost:8000/resumes/upload?user_id=1" \
  -F "file=@/path/to/your/resume.pdf"
```
Expected response:
```json
{"resume_id": 1, "status": "parsing"}
```

### Poll until parsed
```bash
curl http://localhost:8000/resumes/1
```
- Initially: `"markdown_content": ""`
- After Celery task completes: `"markdown_content"` will contain the full Markdown from Docling

> The Celery worker terminal will show the task running and completing.

---

## Test B — Job Discovery

### Trigger a discovery run
```bash
curl -X POST http://localhost:8000/jobs/discover \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "title": "software engineer", "location": "London", "limit": 5}'
```
Expected response:
```json
{"task_id": "<celery-task-uuid>", "status": "discovering"}
```

### Check discovered jobs (after task completes)
```bash
curl "http://localhost:8000/jobs/?user_id=1"
```
Expected: list of Job objects with `title`, `company`, `description`, `url` populated.

> Apify runs take ~1–3 minutes. Watch the Celery worker terminal for progress.

---

## Verify via API docs
All endpoints are browsable at: `http://localhost:8000/docs`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Celery worker not picking up tasks | Ensure Redis is running: `docker-compose ps` |
| `markdown_content` stays empty | Check Celery worker logs for Docling errors |
| Jobs list empty after discovery | Apify actor may still be running — wait and retry `GET /jobs/` |
| `422 Unprocessable Entity` on upload | Ensure you're sending `multipart/form-data` and file is a `.pdf` |
| Apify actor error | Verify `APIFY_API_TOKEN` and `APIFY_ACTOR_ID` in `.env` — see [get-apify-token.md](./get-apify-token.md) |
