We are adopting a **Service-Oriented Architecture**. This keeps FastAPI routes thin and moves all the "Agentic" logic into isolated, reusable Python modules.

By using **`uv`**, you get nearly instantaneous dependency resolution and a clean project structure.

---

### **1. Project Structure**
The structure separates data models from logic to prevent redundant code and keep concerns clearly organized.

```text
/backend
├── app/
│   ├── api/            # FastAPI routes (thin — HTTP concerns only)
│   ├── core/           # Config, Docker setup, and DB session
│   ├── models/         # SQLModel definitions
│   ├── services/       # Business logic (Docling, Groq, Apify)
│   └── worker/         # Celery task definitions
├── tests/
├── pyproject.toml      # Managed by uv
└── docker-compose.yml
```

---

### **2. Step-by-Step Implementation Guide**

#### **Phase 1: The Foundation (Infrastructure)**
Initialize a FastAPI project using `uv`. Set up a `docker-compose.yml` with PostgreSQL and Redis. Define SQLModel models for `User`, `Resume` (storing Markdown text), and `Job` (storing match scores and status).

* **Key Efficiency:** Use **SQLModel** — it combines Pydantic and SQLAlchemy, cutting model boilerplate in half.
* **Next Step:** Run `setup.sh` to verify the containers are up.

#### **Phase 2: Data Collection (Parsing & Discovery)**
Implement a `ParsingService` using Docling to convert PDF bytes to Markdown. Implement a `DiscoveryService` that triggers an Apify actor to scrape LinkedIn job listings. Wrap both in Celery tasks so they run asynchronously.

* **Logic:** Use the Markdown export from Docling to keep LLM input clean and structured.
* **Optimization:** Don't save files locally — pass byte streams directly to Docling to keep the Docker container stateless and light.

#### **Phase 3: The Decision-Brain (Groq Scoring)**
Implement a `ReasoningService` that uses the Groq API with Llama 3.3 to compare a Markdown resume against a Job Description. It returns a JSON object with a `score` (1–10) and a `fit_reasoning` string.

* **Efficiency:** Use a single, well-crafted system prompt instructing the model to act as a "Technical Recruiter".
* **Validation:** Define a Pydantic schema for the LLM output to guard against malformed responses crashing the backend.

#### **Phase 4: Collaboration (Extension Support)**
Implement a FastAPI router for the Chrome Extension with an endpoint that receives `scraped_questions` (a list of strings) and a `job_id`. It uses Groq to generate tailored answers based on the user's resume stored in the DB.

* **Efficiency:** Use **WebSockets** so the backend can push generated answers to the extension one by one as they are ready, making the UI feel faster.

---

### **3. `setup.sh`**
This script lets any team member start the backend with one command.

```bash
#!/bin/bash
# setup.sh - Fast environment bootstrap

uv sync  # Installs all dependencies from pyproject.toml instantly

docker-compose up -d db redis

uv run alembic upgrade head
```

---

### **4. Development Guidelines**
* **Use `uv run`**: Avoid manually activating virtual environments. Run scripts with `uv run python main.py`.
* **Stateless Services**: Services in `services/` must not store state — they take an input (e.g. a resume string) and return an output. This makes debugging significantly easier.
* **Idempotent Tasks**: Celery tasks must be safe to retry without side effects.
* **Validate LLM Output**: Always parse Groq responses through a Pydantic schema before using them downstream.
