# Job Autofiller: Intelligent Automated Job Application System

B.Tech Computer Science & Engineering — CSD334 Mini Project
Department of Computer Engineering, Model Engineering College, Ernakulam
March 2026

**Team:**
- 23CSA41 MDL23CS116 Mehrin Fathima Shamim
- 23CSA47 MDL23CS140 Noel Mathew Anil
- 23CSA19 MDL23CS063 Diya Jojo
- 23CSA50 MDL23CS146 Pranath Prasanth

---

## Certificate

This is to certify that the project titled **"Job Autofiller: Intelligent Automated Job Application System"** is a bonafide record of the mini-project work done by the students of the 6th semester, B.Tech Computer Science and Engineering (Cyber Security), Model Engineering College, Ernakulam, during the academic year 2025–2026.

The project has been carried out in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology in Computer Science and Engineering under APJ Abdul Kalam Technological University, Kerala.

---

## Acknowledgement

We express our sincere gratitude to the Department of Computer Engineering, Model Engineering College, Ernakulam, for providing us the opportunity to carry out this mini-project. We thank our project guide and faculty members for their continuous guidance, encouragement, and support throughout the project.

We also thank the open-source communities behind FastAPI, SQLModel, Docling, Celery, and the Groq API team for providing accessible, well-documented tools that made this project possible. Finally, we thank our classmates for constructive feedback during demos and code reviews.

---

## Abstract

The job application process is time-consuming and repetitive: candidates must manually search for relevant job postings, tailor their resume to each role, and fill out application forms that ask similar questions repeatedly. This project presents **Job Autofiller**, an autonomous agentic system that automates the majority of this pipeline using modern AI services and a microservice-based backend architecture.

The system ingests a user's PDF resume and converts it to structured Markdown using **Docling**, a document intelligence library that leverages layout-aware parsing. Job listings are discovered from LinkedIn via the **Apify** platform's `curious_coder/linkedin-jobs-scraper` actor. Each discovered job is then scored against the user's resume by **Groq's Llama 3.1-8b-instant** model, which returns a relevance score (1–10) and a fit-reasoning explanation. A companion **Chrome Extension** scrapes application form questions and sends them to the backend, where **Groq's Llama 3.3-70b-versatile** model generates tailored answers that are streamed back to the browser in real time via WebSocket.

The backend is built on **FastAPI** with **PostgreSQL** (via SQLModel) for persistence and **Redis + Celery** for asynchronous task execution. All long-running operations—resume parsing, job discovery, and batch scoring—run as idempotent Celery tasks, keeping the API layer non-blocking. The system is fully containerised using Docker Compose, making it easy to deploy and reproduce.

---

## 1. Introduction

Finding suitable employment is one of the most tedious challenges facing modern job seekers. A typical applicant may review dozens of job postings per session, manually assess each for relevance to their skills, and spend significant effort re-entering similar personal information across different application portals. Studies suggest that candidates spend an average of 20–40 hours per week on the job search process, with only a fraction of that time producing qualified applications.

The goal of Job Autofiller is to compress this effort through automation at every stage: discovery, evaluation, and form-filling. By connecting a resume parser, a job scraper, an AI scoring engine, and a browser extension into a single pipeline, the system allows a user to go from "I'm looking for a software engineering role in Bangalore" to a list of ranked, scored job opportunities in minutes, and then complete application forms with AI-drafted answers in seconds.

This project also serves as an exploration of agentic AI patterns—systems where LLM-based components make sequential decisions (e.g., rate-limit-aware retries, structured output parsing) rather than acting as simple question-answering endpoints. The combination of Groq's ultra-low-latency inference with Celery's robust task queue yields a system that is both fast and resilient.

The report is structured as follows: Section 2 describes the system architecture, Section 3 explains the data flows, Sections 4–8 detail individual modules, and Section 9 summarises the end-to-end activity flow.

---

## 2. System Architecture

The system follows a **layered architecture** consisting of five tiers: Client, API, Service, Worker, and Data. A sixth external tier covers third-party APIs. Figure 1 (`architecture.png`) illustrates this structure.

The **Client tier** includes the user's HTTP client (curl, frontend, or testing tool) and the Chrome Extension. The **API tier** is a single FastAPI application exposing four routers: `resumes.py`, `jobs.py`, `extension_rest.py`, and `extension_ws.py`. Routers are intentionally thin—they validate HTTP input, delegate to a service or Celery task, and return a response. No business logic lives in a router.

The **Service tier** contains four stateless service classes that encapsulate all business logic. Each service takes plain Python inputs and returns plain Python outputs, making them independently testable. The **Worker tier** is a Celery application backed by Redis that executes the three long-running tasks asynchronously. Finally, the **Data tier** comprises PostgreSQL (persistent relational storage) and Redis (Celery broker and result backend).

### 2.1 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web framework | FastAPI (Python 3.12+) | HTTP API + WebSocket |
| ORM / Models | SQLModel | Combines Pydantic + SQLAlchemy |
| Database | PostgreSQL 16 | Persistent relational storage |
| Task queue | Celery 5 + Redis 7 | Async background tasks |
| PDF parsing | Docling | Layout-aware PDF → Markdown |
| Job scraping | Apify | LinkedIn job discovery via actor |
| AI scoring | Groq (Llama 3.1-8b-instant) | Resume–JD relevance scoring |
| AI answers | Groq (Llama 3.3-70b-versatile) | Application answer generation |
| Browser client | Chrome Extension | Form scraping + WebSocket |
| Containerisation | Docker Compose | Reproducible deployment |
| Package manager | uv | Fast Python dependency management |

### 2.2 Component Overview

API routes are kept deliberately thin. A route handler's responsibility is limited to: parsing and validating the HTTP request body (using Pydantic/SQLModel), calling either a service method or enqueuing a Celery task, and returning a well-formed HTTP response. This separation ensures that the service layer can be called from tests, CLI scripts, or future frontends without any HTTP overhead.

Services are stateless classes. `ParsingService` accepts raw PDF bytes and returns a Markdown string. `DiscoveryService` accepts a job title and location string and returns a list of raw job dictionaries from Apify. `ReasoningService` accepts a resume Markdown string and a job description and returns a structured `ScoringResult` Pydantic object. `ExtensionService` accepts a question, a resume, and a job description, and returns a generated answer string. None of these services hold session state or database handles; sessions are injected via FastAPI's dependency injection system where needed.

---

## 3. Data Flow

The system's data flows are documented at three levels of abstraction.

**Level 0 (Context Diagram, `dfd0.png`)** treats the entire system as a single process and shows the five external entities it interacts with: the User, the Chrome Extension, the Groq API, the Apify/LinkedIn platform, and the PostgreSQL database. Each entity exchanges clearly labelled data flows with the central process.

**Level 1 (`dfd1.png`)** explodes the system into four main processes corresponding to the four services: P1 Resume Processing, P2 Job Discovery, P3 Job Scoring, and P4 Answer Generation. Two shared data stores—the Resume Store and the Job Store—are shown as open-ended rectangles per DFD convention. This diagram makes clear how P3 and P4 both consume data from the Resume Store and how P2 populates the Job Store consumed by P3.

**Level 2 (`dfd2.png`)** zooms into P3 (Job Scoring) to show its seven internal sub-processes: fetching pending jobs (P3.1), fetching resume markdown (P3.2), truncating inputs (P3.3), calling the Groq API (P3.4), parsing and validating the response with Pydantic (P3.5), updating the job record in the database (P3.6), and handling rate-limit errors with smart retry logic (P3.7).

The end-to-end five-step workflow can be summarised as:

1. **Resume ingestion** — User uploads PDF → `parse_resume_task` (Docling) → Markdown stored in `Resume` table.
2. **Job discovery** — User provides search parameters → `discover_jobs_task` (Apify) → `Job` records created.
3. **Job scoring** — User triggers batch scoring → `score_jobs_task` (Groq) → scores and reasoning stored.
4. **View and select** — User views ranked list (GET /jobs/) → selects target role.
5. **Application filling** — Chrome Extension scrapes questions → `ExtensionService` (Groq Llama 3.3) → answers streamed via WebSocket → human review → form submitted.

---

## 4. Key Modules

### 4.1 Resume Parsing (ParsingService)

`ParsingService` (located at `app/services/parsing.py`) wraps the **Docling** library to convert PDF byte streams into clean Markdown text. Docling performs layout-aware document analysis: it identifies headings, paragraphs, bullet lists, and tables from the PDF's structural information, producing Markdown that preserves semantic hierarchy far better than naive text extraction.

The service is deliberately simple: it accepts raw `bytes` (the PDF file content), constructs a `DocumentConverter` with `do_ocr=False` (OCR is disabled because uploaded resumes are typically digitally-created PDFs, not scans), and returns the resulting Markdown string. Parsing a typical one-page resume takes approximately 3–7 seconds on the development environment.

Crucially, the parsing is performed inside a **Celery task** (`parse_resume_task`) rather than synchronously in the HTTP request. This keeps the `/resumes/upload` endpoint non-blocking: it enqueues the task and returns the `task_id` immediately, allowing the client to poll for completion. The resulting Markdown is stored in the `Resume.markdown_content` column and reused by both `ReasoningService` and `ExtensionService`.

### 4.2 Job Discovery (DiscoveryService)

`DiscoveryService` (at `app/services/discovery.py`) triggers an **Apify** actor run using the `curious_coder/linkedin-jobs-scraper` actor. The actor is launched via the Apify REST API with a search payload containing the desired `title` and `location`. After the actor completes its run (typically 30–90 seconds for a LinkedIn crawl), the service fetches the dataset items and maps each raw job JSON to the system's internal field schema: `title`, `company`, `description`, and `url`.

The discovery flow is similarly offloaded to `discover_jobs_task`. The task creates a `JobSearch` record first (capturing the search parameters and Celery `task_id`), then calls the discovery service, and finally bulk-inserts `Job` records and `JobSearchResult` join records into the database. This design allows the same job to appear in multiple searches without duplication issues and provides a full audit trail of what was searched and when.

### 4.3 Job Scoring (ReasoningService)

`ReasoningService` (at `app/services/reasoning.py`) uses the **Groq API** with the `llama-3.1-8b-instant` model to score each job's fit against the user's resume. The model receives a structured prompt asking it to evaluate fit on a 1–10 integer scale and provide a one-paragraph `fit_reasoning` explanation. The response is validated using a Pydantic `ScoringResult` schema before being written to the database, ensuring that any malformed LLM output is caught and retried rather than silently corrupting data.

A critical design decision is **input truncation**: the resume markdown is capped at 6,000 characters (~1,500 tokens) and the job description at 4,000 characters (~1,000 tokens) before the API call. This keeps each scoring request well within the model's context window and the Groq free-tier TPM limit, enabling batch scoring of dozens of jobs within the same minute.

The `score_jobs_task` Celery task implements a **smart retry** strategy for Groq rate-limit errors. When a `groq.RateLimitError` is raised, the task reads the `retry-after` header from the response (with a regex fallback on the error message body) via the `_parse_retry_after()` helper, then schedules a retry with the exact wait time. `max_retries=10` accommodates legitimate long waits on the Groq free tier while preventing infinite retry loops.

### 4.4 Answer Generation (ExtensionService)

`ExtensionService` (at `app/services/extension.py`) powers the Chrome Extension's form-filling capability. It uses the **Groq API** with `llama-3.3-70b-versatile`, the larger and more capable model reserved for answer generation. Unlike the scoring path, answer generation deliberately does **not** truncate the resume: the full Markdown is provided so the model can draw on all relevant experience, projects, and skills when crafting a nuanced, tailored answer to each application question.

The service is exposed via two endpoints: a synchronous REST endpoint (`POST /extension/answers`) for simple single-question requests, and a **WebSocket endpoint** (`WS /extension/ws/{user_id}/{job_id}`) that streams the answer token-by-token as the model generates it. The streaming approach gives users immediate visual feedback in the browser extension UI without waiting for the complete response, which may take several seconds for long-form answers. After the stream is complete, the extension displays the answer in the form field and prompts the user to review and optionally edit before submitting.

---

## 5. Database Design

The database uses five **SQLModel** tables, defined in `app/models/models.py`.

**User** stores the authenticated user's identity (`id`, `email`, `created_at`). In the current implementation a default seed user is created at startup via `seed_default_user()` in `app/core/db.py`, simplifying single-user operation during the mini-project phase.

**Resume** stores one or more parsed resumes per user (`id`, `user_id` FK, `filename`, `markdown_content`, `created_at`). The `markdown_content` column holds the full Docling output and is the central artifact consumed by both the scoring and answer-generation pipelines.

**Job** is the core entity (`id`, `user_id`, `title`, `company`, `description`, `url`, `score`, `fit_reasoning`, `status`, `created_at`). The `status` field transitions from `"pending"` to `"scored"` after the Groq scoring task completes, and to `"applied"` after the user submits the application. The `score` (integer 1–10) and `fit_reasoning` (text) columns are populated by `ReasoningService`.

**JobSearch** records each discrete search session (`id`, `user_id`, `title`, `location`, `task_id`, `created_at`). The `task_id` column stores the Celery task UUID, enabling the frontend to poll task status.

**JobSearchResult** is a many-to-many join table (`search_id`, `job_id`) linking each search to the jobs it discovered. This allows the same job posting to be returned by multiple searches without data duplication.

The entity relationships are: User 1→N Resume, User 1→N Job, User 1→N JobSearch, JobSearch N↔M Job (via JobSearchResult).

---

## 6. API Design

The API surface is divided into four routers, each in its own file under `app/api/`.

**`resumes.py`** exposes:
- `POST /resumes/upload` — accepts a `multipart/form-data` PDF file, enqueues `parse_resume_task`, returns `{"task_id": "..."}`.
- `GET /resumes/{resume_id}` — returns the stored resume record including `markdown_content`.

**`jobs.py`** exposes:
- `POST /jobs/discover` — accepts `{"title": str, "location": str}`, enqueues `discover_jobs_task`, returns `{"task_id": "...", "search_id": int}`.
- `POST /jobs/score/batch` — accepts `{"job_ids": [int, ...]}`, enqueues `score_jobs_task`, returns task metadata.
- `GET /jobs/` — returns all jobs for the authenticated user, ordered by `score DESC`.

**`extension_rest.py`** exposes:
- `POST /extension/answers` — synchronous endpoint; accepts `{question, job_id, resume_id}`, calls `ExtensionService.generate_answer()`, returns `{"answer": str}`.

**`extension_ws.py`** exposes:
- `WS /extension/ws/{user_id}/{job_id}` — WebSocket endpoint; accepts an initial JSON message containing the question text, streams the generated answer tokens as individual WebSocket text frames, closes cleanly on completion.

All REST endpoints use FastAPI's dependency injection (`Depends(get_session)`) to receive a database session scoped to the request lifetime. Request and response bodies are validated with Pydantic models (or SQLModel, which is a superset).

---

## 7. Async Task Queue

Long-running operations are handled by **Celery** workers, configured in `app/worker/celery_app.py` to use Redis as both the message broker and the result backend. Three tasks are defined in `app/worker/tasks.py`.

**`parse_resume_task(resume_id)`** is triggered after a resume record is created with an empty `markdown_content`. It retrieves the PDF bytes (stored temporarily or passed by reference), calls `ParsingService.parse()`, and writes the resulting Markdown back to the `Resume` record. The task is idempotent: if called twice for the same `resume_id`, the Markdown is simply overwritten with the same content.

**`discover_jobs_task(search_id)`** reads the `JobSearch` record to obtain search parameters, calls `DiscoveryService.discover()`, and inserts the resulting job records. Idempotency is maintained by checking for existing (company, title, user_id) combinations before insertion to avoid duplicates.

**`score_jobs_task(job_ids, resume_id)`** iterates over the provided job IDs, calling `ReasoningService.score()` for each. The Groq rate-limit retry strategy is the most complex part of this task: `groq.RateLimitError` is caught separately from other exceptions, the retry delay is read from the response header, and `self.retry(countdown=wait_seconds, max_retries=10)` is called. This strategy respects the Groq free-tier limits (500K tokens/day for Llama 3.1-8b-instant) while automatically resuming when capacity becomes available.

All tasks follow the project rule that Celery tasks must be **idempotent**: re-running a task with the same inputs should produce the same database state, not create duplicate records or double-increment values.

---

## 8. Chrome Extension Integration

The Chrome Extension acts as a **browser-side agent**: it observes when the user navigates to a job application form, scrapes the visible form question labels (using DOM queries), and sends them to the backend for AI-assisted answering.

Two integration modes are provided, each suited to a different use case:

**REST mode** (`POST /extension/answers`) is suitable for single questions or bulk pre-generation. The extension sends a JSON payload with the question text and relevant identifiers, waits for the HTTP response, and populates the form field. This is simpler to implement and debug, but has higher perceived latency because the user waits for the full answer before seeing anything.

**WebSocket mode** (`WS /extension/ws/{user_id}/{job_id}`) delivers a much better user experience for longer answers. The extension opens a persistent WebSocket connection when a job page is loaded. As the user tabs through form fields, the extension sends the current question as a text frame. The backend calls `ExtensionService.generate_answer()` and streams each token as it arrives from the Groq API back through the WebSocket. The extension appends tokens to the form field in real time, creating a "typing" effect.

In both modes, the **Human-in-the-Loop (HITL)** principle is maintained: the AI draft is placed in the form field but the user must explicitly review, edit if needed, and click submit. The system never auto-submits an application.

---

## 9. Activity Flow

The full end-to-end user journey is documented as a UML activity diagram (`activity.png`). The workflow spans four swim lanes: User, Backend (FastAPI + Celery), Groq API + Apify, and Chrome Extension.

The flow begins when the user uploads their PDF resume. The backend enqueues the parsing task and returns immediately; the user polls until parsing is complete (typically under 10 seconds). Next, the user provides a job title and location to trigger the discovery task. Apify's LinkedIn scraper runs in the background, and the user is notified when job records are available.

The user then triggers batch scoring, which enqueues `score_jobs_task`. Each job is scored against the resume by Groq Llama 3.1-8b-instant. If the Groq rate limit is hit, the smart retry handler waits for the server-specified cooldown before continuing. Once scoring is complete, the user views the ranked job list sorted by score descending.

The user selects a job and opens the application page in their browser. The Chrome Extension activates, scrapes the form's question fields, and sends them to the backend. `ExtensionService` generates tailored answers using Groq Llama 3.3-70b-versatile (with the full, untruncated resume for maximum relevance), streaming the output back via WebSocket. The user reviews and optionally edits each answer in the extension UI. Finally, the user submits the application and the system updates the job status to `"applied"` in the database.

---

## 10. Conclusion

This project successfully delivered an end-to-end autonomous job application assistant within a four-phase development cycle. All four phases were implemented and tested: Docker infrastructure and database models (Phase 1), resume parsing with Docling and job discovery with Apify (Phase 2), AI-powered job scoring with Groq Llama 3.1 and smart rate-limit handling (Phase 3), and Chrome Extension integration with real-time WebSocket answer streaming (Phase 4).

The key technical contributions of this project are: (1) a clean layered architecture that separates HTTP concerns from business logic and async execution; (2) a dual-model Groq strategy that uses a fast, high-volume model for scoring and a more capable model for answer generation, carefully managing the free-tier token budget; (3) a robust rate-limit retry mechanism that reads `retry-after` headers and schedules Celery retries accordingly; and (4) a WebSocket streaming interface that provides real-time feedback to the user during answer generation.

From an academic perspective, this project demonstrates the practical application of agentic AI patterns—structured output validation, tool-use via external APIs, and human-in-the-loop safeguards—in a production-grade Python microservices architecture. The system as built provides a solid foundation for future extensions, including multi-user support with authentication, a full frontend UI, application status tracking across multiple portals, and fine-tuning of the scoring rubric based on user feedback.
