# Command Log

| # | Command | Explanation |
|---|---------|-------------|
| 1 | `uv init --no-workspace` | Initializes a new uv-managed Python project, creating `pyproject.toml` |
| 2 | `uv add fastapi uvicorn[standard] sqlmodel psycopg2-binary celery redis python-dotenv groq apify-client pydantic-settings alembic` | Installs all core backend dependencies and locks them in `pyproject.toml` |
| 3 | `mkdir -p app/{api,core,models,services,worker} tests` | Creates the full project directory structure |
| 4 | `chmod +x setup.sh` | Makes the setup script executable |
| 5 | `uv run alembic init alembic` | Initializes Alembic migration framework with config and versions directory |

---

## Phase 1 Complete — Files Created

| File | Purpose |
|------|---------|
| `app/models/models.py` | `User`, `Resume`, `Job` SQLModel tables |
| `app/main.py` | FastAPI entry point + DB init on startup |
| `app/core/config.py` | Settings from `.env` |
| `app/core/db.py` | Engine + session + table creation |
| `docker-compose.yml` | `db`, `redis`, `api`, `worker` containers |
| `Dockerfile` | uv-based image |
| `setup.sh` | One-command team bootstrap |
| `.env.example` | Env var template |
| `alembic/` | DB migrations wired to SQLModel metadata |

---

## Phase 2 Commands

| # | Command | Explanation |
|---|---------|-------------|
| 6 | `uv add docling python-multipart` | Adds Docling (PDF → Markdown) and multipart form support for file uploads |

## Phase 2 Complete — Files Created

| File | Purpose |
|------|---------|
| `app/services/parsing.py` | `ParsingService` — Docling: PDF bytes → Markdown string |
| `app/services/discovery.py` | `DiscoveryService` — Apify actor trigger → list of job postings |
| `app/worker/celery_app.py` | Celery app initialized with Redis broker/backend |
| `app/worker/tasks.py` | `parse_resume_task` and `discover_jobs_task` Celery tasks |
| `app/api/resumes.py` | `POST /resumes/upload`, `GET /resumes/{id}` |
| `app/api/jobs.py` | `POST /jobs/discover`, `GET /jobs/` |
| `app/core/config.py` | Added `APIFY_ACTOR_ID` and `LLM_MODEL` settings |
| `app/main.py` | Registered resumes and jobs routers |

---

## Why These Technology Choices

### Docling over PyMuPDF
PyMuPDF extracts raw text — it dumps characters in reading order but loses structure (tables, sections, bullet points become a flat blob). Docling understands document layout and exports clean Markdown, which gives the LLM much better context when scoring a resume against a job description. The structure (e.g. "Experience", "Skills" headings) matters for Groq/Llama to reason accurately.

### uv over pip / poetry
`uv` is a Rust-based package manager orders of magnitude faster than pip. It handles virtual environments, dependency locking, and running scripts (`uv run`) without manually activating a venv. In 2026 it's the standard for new Python projects. `uv sync` installs everything from `uv.lock` in seconds.

Memory efficiency is another key advantage — uv uses a global package cache and hardlinks packages into each project's venv instead of copying them. Installing the same package across multiple projects costs near-zero extra disk space. pip copies files every time, so three projects with the same dependencies means three full copies on disk. uv avoids that entirely.

### Docker + Docker Compose
PostgreSQL and Redis can't run as Python packages — they're separate processes. Docker Compose lets the whole team spin up `db` and `redis` with one command (`docker-compose up -d db redis`) without installing them natively. It also matches a production-like environment so there are no "works on my machine" issues.

### Celery + Redis
Resume parsing (Docling) and job scraping (Apify) are slow — they can take 10–60 seconds. Running them synchronously in a FastAPI route would block the request and time out. Celery offloads these to background workers; the API returns immediately with a task ID, and the worker processes it async. Redis acts as the message broker (task queue) and result backend.

---

## What `setup.sh` Does

Runs once to bootstrap the environment for any team member:

1. Checks if `uv` is installed — installs it if missing
2. Runs `uv sync` — installs all Python dependencies from `pyproject.toml`
3. Copies `.env.example` → `.env` if no `.env` exists yet
4. Runs `docker-compose up -d db redis` — starts Postgres and Redis containers
5. Runs `uv run alembic upgrade head` — applies DB migrations to create tables

After `setup.sh`, only `uv run uvicorn app.main:app --reload` is needed to start the API.

---

## Errors Encountered

### `ForeignKeyViolation` on `POST /resumes/upload`

**Error:**
```
psycopg2.errors.ForeignKeyViolation: insert or update on table "resume" violates
foreign key constraint "resume_user_id_fkey"
DETAIL: Key (user_id)=(1) is not present in table "user".
```

**Cause:** `Resume.user_id` has a FK constraint → `user.id`. Calling the upload endpoint with `user_id=1` failed because no User row existed in the DB yet — there was no endpoint or mechanism to create one.

**Options considered:**
| Option | Verdict |
|--------|---------|
| Add `POST /users/` endpoint | Works but requires a manual extra step before every test |
| Remove `user_id` FK from models | Loses the user→resume link needed for Phase 3 scoring |
| Proper Supabase auth | Overkill for a local-only tool; separate concern |
| Seed a default user on startup | ✅ Chosen — zero friction, idempotent, reversible |

**Fix:** Added `seed_default_user()` to `app/core/db.py`. Called from `on_startup` in `app/main.py` after `create_db_and_tables()`. Checks if `user.id = 1` exists before inserting — safe to run on every restart.

**Files changed:** `app/core/db.py`, `app/main.py`

---

### Docling OCR overhead on ATS resumes

**Observed:** Parse task taking ~17 seconds with RapidOCR models being downloaded and initialised on every worker start.

**Before (default `DocumentConverter()`, OCR auto mode):**
```
Initializing pipeline for StandardPdfPipeline...
Registered ocr engines: ['auto', 'easyocr', 'ocrmac', 'rapidocr', ...]
Initiating download: .../ch_PP-OCRv4_det_infer.pth   (13.83MB)
Initiating download: .../ch_PP-OCRv4_rec_infer.pth   (25.67MB)
Auto OCR model selected rapidocr with torch.
Finished converting document resume.pdf in 17.43 sec.
Task parse_resume_task succeeded in 17.56s
```

**After (`do_ocr=False` via `PdfPipelineOptions`):**
```
detected formats: [<InputFormat.PDF: 'pdf'>]
Going to convert document batch...
Processing document resume.pdf
Finished converting document resume.pdf in 2.44 sec.
Task parse_resume_task succeeded in 2.46s
```

**Why:** OCR is for scanned/image PDFs — it converts a visual page into text. ATS-friendly resumes already have text embedded natively; running OCR on them downloads ~40MB of models and wastes ~15 seconds per parse for zero benefit.

**Fix:** `PdfPipelineOptions(do_ocr=False)` passed into `DocumentConverter` via `PdfFormatOption`. Parse time dropped from **17.5s → 2.4s**.

**Files changed:** `app/services/parsing.py`

---

### Apify actor free trial expired on `POST /jobs/discover`

**Status:** ⚠️ Unresolved — to be investigated.

**Observed:** `discover_jobs_task` retried 3 times then gave up with:
```
ApifyApiError: You must rent a paid Actor in order to run it after its free trial
has expired. To rent this Actor, go to https://console.apify.com/actors/BHzefUZlZRKWxkTck
```
London
**When:** Called `POST /jobs/discover` with `{"user_id": 1, "title": "software engineer intern", "location": "kochi,india", "limit": 5}`.

**Likely cause:** The Apify actor `bebity/linkedin-jobs-scraper` (set as `APIFY_ACTOR_ID` in `.env`) has a free trial that has expired. Apify's paid actors require an active rental to run beyond the trial period.

**To investigate:**
- Check the actor's rental status at `https://console.apify.com/actors/BHzefUZlZRKWxkTck`
- Look for a free alternative actor on Apify Store, or switch `APIFY_ACTOR_ID` in `.env` to a different LinkedIn jobs scraper that is free/included in the monthly credits
