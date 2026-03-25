# Running the Backend (Quick — via setup.sh)

## Prerequisites
- [Docker + Docker Compose](https://docs.docker.com/get-docker/)

`uv` will be auto-installed by `setup.sh` if not present.

---

## Step 1 — Navigate to the backend
```bash
cd repo/mini-project/backend
```

## Step 2 — Add your API keys
```bash
cp .env.example .env
```
Open `.env` and set:
```
GROQ_API_KEY=your_groq_api_key_here
APIFY_API_TOKEN=your_apify_token_here
```
> Need an Apify token? See [get-apify-token.md](./get-apify-token.md).

## Step 3 — Run setup
```bash
./setup.sh
```
This handles everything:
- Installs `uv` if missing
- Installs Python dependencies (`uv sync`)
- Starts Docker containers (`db`, `redis`)
- Runs DB migrations (`alembic upgrade head`)

## Step 4 — Start the API server and Celery worker

You need **two separate terminals** for this step.

**Terminal 1 — API server:**
```bash
uv run uvicorn app.main:app --reload
```

**Terminal 2 — Celery worker:**
```bash
uv run celery -A app.worker.celery_app worker --loglevel=info
```

The Celery worker handles async tasks (resume parsing, job scraping, scoring). Both must be running for the full system to work.

## Step 5 — Verify
```bash
curl http://localhost:8000/health
# {"status": "ok"}
```
API docs: `http://localhost:8000/docs`

---

## Stopping
```bash
# API server: Ctrl+C
docker-compose down
```
