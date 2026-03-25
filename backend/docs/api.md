# API Reference — Job Autofiller Backend

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

---

## System Workflow

The complete flow for a frontend client:

```
1. POST /resumes/upload          → get resume_id, poll until parsed
2. POST /jobs/discover           → get task_id + search_id, poll until complete
3. POST /jobs/score/batch        → get task_id, poll until complete
4. GET  /jobs/                   → list scored jobs
5. POST /extension/answers       → get AI answers (REST)
   — or —
   WS   /extension/ws/{uid}/{jid} → stream AI answers (WebSocket)
```

---

## Health

### GET /health

Returns server status.

**Response**
```json
{ "status": "ok" }
```

---

## Resumes

### POST /resumes/upload

Upload a PDF resume. Parsing is asynchronous — poll `GET /resumes/{id}` until `markdown_content` is populated.

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | int | yes | User ID (default user: `1`) |

**Request Body** — `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `file` | file | PDF file only |

**Response** `200`
```json
{
  "resume_id": 1,
  "status": "parsing"
}
```

**Errors**
- `400` — file is not a PDF

---

### GET /resumes/{resume_id}

Retrieve a resume record. `markdown_content` will be empty string until the background parse task completes.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `resume_id` | int | Resume ID |

**Response** `200`
```json
{
  "id": 1,
  "user_id": 1,
  "filename": "john_doe_resume.pdf",
  "markdown_content": "# John Doe\n\n## Experience\n...",
  "created_at": "2026-03-25T10:00:00"
}
```

> **Polling pattern:** Call this endpoint every 2–3 seconds after upload until `markdown_content` is non-empty before proceeding to job discovery.

---

## Jobs

### POST /jobs/discover

Trigger a LinkedIn job search via Apify. Returns immediately — discovery runs in the background.

**Request Body** — `application/json`

```json
{
  "user_id": 1,
  "title": "Senior Backend Engineer",
  "location": "San Francisco, CA",
  "limit": 20
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `user_id` | int | yes | — | User ID |
| `title` | string | yes | — | Job title to search |
| `location` | string | yes | — | Location (city, state, country) |
| `limit` | int | no | `20` | Max number of jobs to fetch |

**Response** `200`
```json
{
  "task_id": "a3b1c2d4-...",
  "search_id": 1,
  "status": "discovering"
}
```

> Save both `task_id` (for polling status) and `search_id` (for scoped scoring and listing).

---

### GET /jobs/discover/{task_id}/status

Poll the status of a discovery task.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | string | Celery task UUID from `/jobs/discover` |

**Response** `200`
```json
{
  "task_id": "a3b1c2d4-...",
  "state": "SUCCESS"
}
```

**`state` values**

| State | Meaning |
|-------|---------|
| `PENDING` | Task queued, not yet started |
| `STARTED` | Worker is scraping jobs |
| `SUCCESS` | Jobs saved to DB — proceed to scoring |
| `FAILURE` | Scraping failed |
| `RETRY` | Transient error, retrying automatically |

---

### POST /jobs/score/batch

Score all discovered jobs against a resume. Each job gets a 1–10 fit score from Groq/Llama. Runs asynchronously with 8-second throttling between jobs.

**Request Body** — `application/json`

```json
{
  "user_id": 1,
  "resume_id": 1,
  "search_id": 1
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | int | yes | User ID |
| `resume_id` | int | yes | Resume to score against |
| `search_id` | int | no | If provided, scores only jobs from this search session; otherwise scores all pending jobs for the user |

**Response** `200`
```json
{
  "task_id": "f7e8d9c0-...",
  "job_count": 18,
  "status": "scoring"
}
```

> For 18 jobs with 8s throttle, expect ~2.5 minutes for full completion.

---

### GET /jobs/score/{task_id}/status

Poll the status of a scoring task.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | string | Celery task UUID from `/jobs/score/batch` |

**Response** `200`
```json
{
  "task_id": "f7e8d9c0-...",
  "state": "STARTED"
}
```

Same `state` values as discovery status.

---

### POST /jobs/{job_id}/score

Score a single job (triggers the same Celery task with one job).

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `job_id` | int | Job ID to score |

**Request Body** — `application/json`
```json
{ "resume_id": 1 }
```

**Response** `200`
```json
{
  "task_id": "c1a2b3d4-...",
  "job_id": 5,
  "status": "scoring"
}
```

---

### GET /jobs/

List jobs for a user, optionally filtered by search session.

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | int | yes | User ID |
| `search_id` | int | no | Filter to jobs from a specific search session |

**Response** `200`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Senior Backend Engineer",
    "company": "TechCorp",
    "description": "We are looking for...",
    "url": "https://www.linkedin.com/jobs/view/...",
    "score": 8,
    "fit_reasoning": "Strong match: candidate has 10 years Python experience and prior startup exposure matching the role requirements.",
    "status": "scored",
    "created_at": "2026-03-25T10:05:00"
  }
]
```

**`status` values**

| Status | Meaning |
|--------|---------|
| `pending` | Not yet scored |
| `scored` | Has `score` and `fit_reasoning` |
| `applied` | Application submitted |

**Score rubric (1–10)**

| Score | Match level |
|-------|-------------|
| 9–10 | Near-perfect match |
| 7–8 | Strong match |
| 5–6 | Partial match |
| 3–4 | Weak match |
| 1–2 | Poor match |

---

## Extension — Answer Generation

Two interfaces are available: REST (simple, blocking) and WebSocket (streaming, preferred for the Chrome Extension).

### POST /extension/answers

Generate answers for all application questions in one synchronous call. Returns when all answers are ready.

**Request Body** — `application/json`

```json
{
  "user_id": 1,
  "job_id": 1,
  "resume_id": 1,
  "questions": [
    "Why do you want to work here?",
    "Describe your biggest technical achievement.",
    "What is your expected salary?"
  ]
}
```

**Response** `200`
```json
{
  "answers": [
    {
      "question": "Why do you want to work here?",
      "answer": "I'm drawn to this role because TechCorp's focus on distributed systems aligns directly with my 5 years building high-throughput APIs. Your open-source contributions and engineering culture make this an environment where I can do my best work."
    },
    {
      "question": "Describe your biggest technical achievement.",
      "answer": "I led the redesign of our payment processing pipeline, reducing p99 latency from 800ms to 120ms by replacing synchronous DB calls with event-driven Celery tasks. The system now handles 10x the previous peak load without degradation."
    },
    {
      "question": "What is your expected salary?",
      "answer": "Based on my experience and the market rate for this role, I'm targeting $160,000–$180,000. I'm open to discussing total compensation including equity and benefits."
    }
  ]
}
```

**Errors**
- `404` — Resume or job not found, or does not belong to the user

> Answers are generated by Groq Llama 3.3-70b using the full resume and full job description (no truncation). Response time scales linearly with number of questions (~2–5 seconds each).

---

### WebSocket /extension/ws/{user_id}/{job_id}

Stream answers one-by-one as they are generated. Preferred for the Chrome Extension UI — shows progress in real time.

**WebSocket URL**
```
ws://localhost:8000/extension/ws/{user_id}/{job_id}
```

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | int | User ID |
| `job_id` | int | Job ID |

**Protocol**

1. Client connects to the WebSocket URL.
2. Client sends one JSON message:

```json
{
  "resume_id": 1,
  "questions": [
    "Why do you want to work here?",
    "Describe your biggest technical achievement."
  ]
}
```

3. Server streams one message per answer:

```json
{ "index": 0, "question": "Why do you want to work here?", "answer": "I'm drawn to..." }
{ "index": 1, "question": "Describe your biggest technical achievement.", "answer": "I led..." }
```

4. Server sends a final message and closes:

```json
{ "done": true }
```

5. On validation error, server sends and closes:

```json
{ "error": "Resume not found or does not belong to user" }
```

**JavaScript example**
```javascript
const ws = new WebSocket('ws://localhost:8000/extension/ws/1/5');

ws.onopen = () => {
  ws.send(JSON.stringify({
    resume_id: 1,
    questions: ['Why do you want this role?', 'Tell us about yourself.']
  }));
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.done) {
    console.log('All answers received');
    ws.close();
  } else if (msg.error) {
    console.error('Error:', msg.error);
  } else {
    console.log(`Q${msg.index}: ${msg.question}`);
    console.log(`A: ${msg.answer}`);
    // Populate form field at index msg.index
  }
};
```

**Test client:** `GET /extension/ws/test` — opens a browser-based WebSocket tester (no Chrome Extension needed).

---

## Data Models

### Resume

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Owner |
| `filename` | string | Original PDF filename |
| `markdown_content` | string | Parsed content (empty until task completes) |
| `created_at` | datetime | ISO 8601 |

### Job

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Owner |
| `title` | string | Job title |
| `company` | string | Company name |
| `description` | string | Full job description |
| `url` | string \| null | LinkedIn job URL |
| `score` | int \| null | Fit score 1–10 (null until scored) |
| `fit_reasoning` | string \| null | One-paragraph AI explanation |
| `status` | string | `pending` / `scored` / `applied` |
| `created_at` | datetime | ISO 8601 |

### JobSearch

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Primary key |
| `user_id` | int | Owner |
| `title` | string | Job title searched |
| `location` | string | Location searched |
| `task_id` | string | Celery task UUID |
| `created_at` | datetime | ISO 8601 |

---

## Complete Workflow Example

```
# 1. Upload resume
POST /resumes/upload?user_id=1
  → { "resume_id": 1, "status": "parsing" }

# 2. Poll until parsed
GET /resumes/1
  → { ..., "markdown_content": "# Jane Smith\n..." }   ← non-empty = ready

# 3. Discover jobs
POST /jobs/discover
  { "user_id": 1, "title": "Backend Engineer", "location": "Remote", "limit": 20 }
  → { "task_id": "aaa-111", "search_id": 2, "status": "discovering" }

# 4. Poll until discovered
GET /jobs/discover/aaa-111/status
  → { "state": "SUCCESS" }

# 5. Score all discovered jobs
POST /jobs/score/batch
  { "user_id": 1, "resume_id": 1, "search_id": 2 }
  → { "task_id": "bbb-222", "job_count": 17, "status": "scoring" }

# 6. Poll until scored (~2–3 min for 17 jobs)
GET /jobs/score/bbb-222/status
  → { "state": "SUCCESS" }

# 7. List scored jobs
GET /jobs/?user_id=1&search_id=2
  → [ { "id": 3, "score": 9, "fit_reasoning": "...", ... }, ... ]

# 8. Generate answers for top job (REST)
POST /extension/answers
  { "user_id": 1, "job_id": 3, "resume_id": 1, "questions": ["Why us?"] }
  → { "answers": [ { "question": "Why us?", "answer": "..." } ] }

# — or — Generate answers via WebSocket (streaming)
WS /extension/ws/1/3
  send: { "resume_id": 1, "questions": ["Why us?", "Tell us about yourself."] }
  recv: { "index": 0, "question": "Why us?", "answer": "..." }
  recv: { "index": 1, "question": "Tell us about yourself.", "answer": "..." }
  recv: { "done": true }
```

---

## Rate Limits & Timing

| Operation | Approximate duration |
|-----------|---------------------|
| Resume parse | 5–30 seconds (PDF size dependent) |
| Job discovery | 30–120 seconds (Apify scraping) |
| Batch scoring (20 jobs) | ~3 minutes (8s throttle between jobs) |
| Single answer (REST) | 2–5 seconds per question |
| Answer stream (WS) | 2–5 seconds per answer, streamed progressively |

Scoring uses `llama-3.1-8b-instant` (500K tokens/day). Answer generation uses `llama-3.3-70b-versatile` (100K tokens/day). If daily limits are hit, the system retries automatically using the `retry-after` header from Groq.
