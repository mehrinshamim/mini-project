# Running the Backend Locally

## Prerequisites
Make sure you have these installed before starting:
- [Docker + Docker Compose](https://docs.docker.com/get-docker/)
- [uv](https://docs.astral.sh/uv/) — Python package manager

If you don't have `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

---

## Step 1 — Clone and navigate to the backend
```bash
cd repo/mini-project/backend
```

## Step 2 — Install dependencies
```bash
uv sync
```

## Step 3 — Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your keys:
```
GROQ_API_KEY=your_groq_api_key_here
APIFY_API_TOKEN=your_apify_token_here
```
Leave `DATABASE_URL` and `REDIS_URL` as-is if running locally with Docker.

> Need an Apify token? See [get-apify-token.md](./get-apify-token.md).

## Step 4 — Start the database and Redis
```bash
docker-compose up -d db redis
```
Verify containers are running:
```bash
docker-compose ps
```
You should see `db` and `redis` with status `running`.

## Step 5 — Run database migrations
```bash
uv run alembic upgrade head
```
This creates the `user`, `resume`, and `job` tables in Postgres.

## Step 6 — Start the API server and Celery worker

You need **two separate terminals** for this step.

**Terminal 1 — API server:**
```bash
uv run uvicorn app.main:app --reload
```

**Terminal 2 — Celery worker:**
```bash
uv run celery -A app.worker.celery_app worker --loglevel=info
```

The Celery worker handles async tasks like resume parsing, job scraping, and scoring. Both must be running for the full system to work.

## Step 7 — Verify it's working
Open your browser or run:
```bash
curl http://localhost:8000/health
```
Expected response:
```json
{"status": "ok"}
```

API docs are available at: `http://localhost:8000/docs`

---

## Stopping the backend
```bash
# Stop the API server: Ctrl+C

# Stop Docker containers
docker-compose down
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `psycopg2` connection error | Make sure Docker is running and `db` container is up |
| `uv: command not found` | Re-run the uv install command in Step 0 and restart terminal |
| Port 8000 already in use | Kill the process: `lsof -ti:8000 \| xargs kill` |
| Alembic error `can't connect to DB` | Ensure `DATABASE_URL` in `.env` matches your Docker setup |
