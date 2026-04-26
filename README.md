# JobFlow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

JobFlow is an autonomous agentic job application platform that streamlines your job hunt from start to finish. Upload your resume, scrape live job listings from LinkedIn, score fit with AI, and let JobFlow automatically generate tailored answers for application forms via a Chrome Extension — saving you time and effort.

---

## ✨ Features

- **Resume Upload** — Upload your PDF resume to power personalized job matching
- **LinkedIn Job Scraping** — Discover relevant job listings based on role and location
- **AI Fit Scoring** — Each job is scored based on how well it matches your resume
- **Application Auto-Filler** — Automatically fill job applications with your details
- **User-Friendly Interface** — Clean dashboard built for a smooth experience
- **Guidebook** — Step-by-step guide to help you get the most out of JobFlow

---

## 🚀 Tech Stack

- **Frontend:** Next.js (React)
- **Backend:** FastAPI (Python 3.12+)
- **Database:** PostgreSQL via SQLModel
- **Queue/Workers:** Redis + Celery (async tasks)
- **AI Models:** Groq API (Llama 3.1 for scoring, Llama 3.3 for answers)
- **Scraping & Parsing:** Apify (LinkedIn), Docling (PDFs)

---

## 🛠️ Project Setup

### 1. Backend

The backend utilizes Docker, Redis, and Celery for background processing and AI integrations. `uv` is recommended for dependency management.

```bash
cd backend
cp .env.example .env
```

Open `.env` and set your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
APIFY_API_TOKEN=your_apify_token_here
```

📚 **Note:** Refer to [`backend/docs/get-apify-token.md`](backend/docs/get-apify-token.md) for steps on getting your Apify token.

Run the setup script to start the DB and Redis containers, and apply DB migrations:
```bash
./setup.sh
```

**Start the API Server and Celery Worker (requires two terminals):**

**Terminal 1:**
```bash
cd backend
uv run uvicorn app.main:app --reload
```

**Terminal 2:**
```bash
cd backend
uv run celery -A app.worker.celery_app worker --loglevel=info
```
*(macOS users: If you encounter forking issues, add `--pool=solo` to the celery command).*

> 📖 **For detailed backend instructions, refer to [`backend/README.md`](backend/README.md).**

### 2. Frontend

The frontend provides the interactive user dashboard.

```bash
cd frontend
npm install
npm run dev
```

The frontend will be accessible at `http://localhost:3000`.

### 3. Chrome Extension

Load the `extension/` directory into your Chrome browser:
1. Go to `chrome://extensions/`
2. Enable **Developer mode** in the top right.
3. Click **Load unpacked** and select the `extension/` folder in your project.

---

## 📂 Project Structure

```text
JobFlow/
├── frontend/       # Web application (dashboard, guide, components)
├── backend/        # FastAPI API, Celery workers, DB models, and AI logic
└── extension/      # Chrome Extension for application autofilling
```

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/mehrinshamim/mini-project/issues). You can also take a look at the [contributing guide](CONTRIBUTING.md) and our [code of conduct](CODE_OF_CONDUCT.md).

## 📝 License

This project is [MIT](LICENSE) licensed.
