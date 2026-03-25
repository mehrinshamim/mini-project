This update integrates **Docker** for containerization and **`uv`** as your high-performance Python package manager. Using `uv` is a smart choice for 2026; it is significantly faster than `pip` and handles virtual environments and dependency locking seamlessly.

---

## 1. Final Software Requirements Specification (SRS)

### 1.1 Project Objective
To develop an autonomous, agentic job application system that uses **Groq** for high-speed reasoning and **Docling** for structured resume analysis. The system focuses on reducing application friction through intelligent "Question Sniffing" via a Chrome Extension and context-aware response generation.

### 1.2 Functional Requirements (FR)
* **FR-1: Resume Intelligence:** Must use **Docling** to parse PDF resumes into Markdown for optimal LLM context.
* **FR-2: Strategic Scoring:** Must rank scraped jobs from **Apify** using **Groq (Llama 3.3)**.
* **FR-3: Extension-Led Extraction:** A Chrome Extension must capture on-screen application questions and transmit them to the FastAPI backend.
* **FR-4: Human-in-the-Loop (HITL):** Users must approve or edit AI-generated responses before final submission.

### 1.3 Technical Stack
* **Frontend:** Next.js 15 (TypeScript), Tailwind CSS.
* **Backend:** FastAPI (Python 3.12+), **`uv`** (Package Manager).
* **Data/Tasks:** PostgreSQL, Redis, Celery.
* **Infrastructure:** **Docker**, **Docker Compose**.
* **AI/Tools:** Groq API, Docling, Apify.

---

## 2. Software Design Document (SDD)

### 2.1 System Architecture
The architecture is a **Distributed Hybrid Agent**. The "Brain" is centralized in FastAPI, while the "Sensors" are distributed across Apify (web-wide search) and the Chrome Extension (site-specific search).



### 2.2 Component Roles
* **`uv`**: Manages the Python environment and ensures reproducible builds across the team.
* **Docker Compose**: Orchestrates four main containers: `api` (FastAPI), `worker` (Celery), `redis` (Broker), and `db` (Postgres).
* **Chrome Extension**: Scrapes internal application labels and provides the "Autofill" UI.

---

## 3. Iterative Implementation Plan

We will implement this in modules to ensure a working product at every stage.

### **Phase 1: V1.0 - The Core & Infrastructure**
* **Goal**: Get the environment running with Docker and `uv`.
* **Module**: Setup `docker-compose.yml` and `pyproject.toml` (via `uv init`).
* **Module**: Define PostgreSQL models for `User`, `Resume`, and `Job`.

### **Phase 2: V2.0 - Parsing & Discovery**
* **Goal**: Upload a resume and see scraped jobs.
* **Module**: Integrate **Docling** service for PDF-to-Markdown parsing.
* **Module**: Integrate **Apify** for job scraping.
* **Module**: Setup **Celery** tasks to handle these long-running processes.

### **Phase 3: V3.0 - The Scoring Agent**
* **Goal**: AI-ranked job list.
* **Module**: Build the **Groq/Llama 3.3** scoring engine.
* **Module**: UI update: Next.js dashboard showing "Match Scores."

### **Phase 4: V4.0 - The Extension & Execution**
* **Goal**: Live application assistance.
* **Module**: Backend API for the Chrome Extension.
* **Module**: Generation logic for form responses and cover letters.

---

## 4. Setup & Infrastructure Scripts

### **`setup.sh`**
This script automates the environment setup for your team members.

```bash
#!/bin/bash

echo "🚀 Starting Job Autofiller Setup..."

# 1. Check for uv
if ! command -v uv &> /dev/null
then
    echo "📦 'uv' not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 2. Initialize Python Environment
echo "🐍 Creating virtual environment with uv..."
uv venv
source .venv/bin/activate

# 3. Install Dependencies
echo "🛠️ Installing backend dependencies..."
uv pip install -r requirements.txt

# 4. Environment Variables
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update your .env file with Groq/Apify keys!"
fi

# 5. Docker Containers
echo "🐳 Starting Docker containers (DB, Redis)..."
docker-compose up -d

echo "✅ Setup Complete! Run 'uvicorn main:app --reload' to start the backend."
```

### **`docker-compose.yml` (Backend Preview)**
```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: job_autofiller
    ports:
      - "5432:5432"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  api:
    build: .
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db/job_autofiller
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"
```

