# Changes: Original Rough Report → Updated Report

Summary of what was changed from `mini_project_rough_report.docx` to `report_updated.md` and the updated diagrams.

---

## 1. Abstract — Technology Stack Corrections

| Original Draft | Updated |
|----------------|---------|
| BERT and SBERT for semantic job matching | Groq API with Llama 3.1-8b-instant (scoring) and Llama 3.3-70b-versatile (answer generation) |
| Named Entity Recognition (NER) for resume extraction | Docling — layout-aware PDF-to-Markdown conversion |
| Selenium WebDriver for browser automation | Chrome Extension communicating via REST / WebSocket |
| "Modular multi-agent architecture with specialized agents" (vague) | Clearly named services: ParsingService, DiscoveryService, ReasoningService, ExtensionService |
| "15–20 minutes reduced to under 2 minutes" | Timings updated to reflect actual measured latency (parse ~5s, discover ~30–90s, score ~3 min batch, answers ~2–5s each) |

---

## 2. New Sections Added

The original docx ended at the Abstract + Table of Contents page (the body was incomplete). The following sections were written from scratch based on the actual codebase:

| Section | Content |
|---------|---------|
| 1. Introduction | Problem statement, project motivation, agentic AI framing |
| 2. System Architecture | 5-layer architecture, technology stack table, component roles |
| 3. Data Flow | Explanation of all three DFD levels (L0, L1, L2) and the 5-step workflow |
| 4. Key Modules | Detailed write-up for ParsingService, DiscoveryService, ReasoningService, ExtensionService |
| 5. Database Design | All 5 SQLModel tables (User, Resume, Job, JobSearch, JobSearchResult) with field descriptions |
| 6. API Design | All 4 routers and their endpoints documented |
| 7. Async Task Queue | Celery task details, idempotency rules, smart retry strategy |
| 8. Chrome Extension Integration | REST vs WebSocket modes, HITL principle |
| 9. Activity Flow | Walkthrough of the full UML activity diagram |
| 10. Conclusion | Summary of phases delivered, technical contributions |

---

## 3. Diagrams — What Changed

All 5 diagrams were regenerated from scratch to reflect the actual implemented system.

### `architecture.png`
- **Old:** Generic placeholder / hand-drawn sketch
- **New:** 5-layer diagram (Client → API → Services → Workers → Data) with External tier (Groq, Apify). Shows all 4 routers, all 4 services, all 3 Celery tasks, PostgreSQL, and Redis as distinct labeled boxes with directional arrows.

### `dfd0.png` (Level 0 Context Diagram)
- **Old:** May have referenced Selenium, BERT, or generic "ML model" as external entities
- **New:** 5 correct external entities: User, Chrome Extension, Groq API, Apify/LinkedIn, PostgreSQL. All data flows labeled with actual data (PDF bytes, Markdown, job scores, WebSocket answers, etc.)

### `dfd1.png` (Level 1 DFD)
- **Old:** May have shown incorrect processes (e.g., separate NER agent, Selenium scraper)
- **New:** 4 processes matching the 4 services (P1 Resume Processing, P2 Job Discovery, P3 Job Scoring, P4 Answer Generation). Data stores D1 (Resume Store) and D2 (Job Store) correctly connected. Apify replaces any scraping agent.

### `dfd2.png` (Level 2 DFD — Job Scoring)
- **Old:** Likely absent or incomplete
- **New:** Explodes P3 into 7 sub-processes: fetch pending jobs → fetch resume → truncate inputs (resume[:6000], JD[:4000]) → call Groq Llama 3.1 → validate with Pydantic ScoringResult → update DB → rate-limit handler (`_parse_retry_after`, max_retries=10). Fully reflects actual `score_jobs_task` logic.

### `activity.png`
- **Old:** May have shown Selenium-based form submission or BERT scoring step
- **New:** 4 swim lanes (User / Backend+Celery / Groq+Apify / Chrome Extension). Decision diamonds for polling checkpoints. Correct async branching for parse, discover, and score tasks. WebSocket streaming path. HITL review step before form submission.

---

## 4. Technology Replacements (Summary)

| Planned (Original Draft) | Actual (Implemented) | Reason |
|--------------------------|----------------------|--------|
| BERT / SBERT semantic matching | Groq Llama 3.1-8b-instant | Faster inference, no GPU needed, free-tier API |
| Named Entity Recognition (NER) | Docling PDF parser | Better structure preservation, Markdown output ideal for LLM context |
| Selenium WebDriver | Chrome Extension + WebSocket | Less brittle, user-controlled, human-in-the-loop |
| Generic ML agent framework | FastAPI + Celery + Redis | Standard Python stack, clear separation of concerns |
| `bebity/linkedin-jobs-scraper` (Apify) | `curious_coder/linkedin-jobs-scraper` | Original actor's free trial expired |

---

## 5. What Was NOT Changed

- Team members, roll numbers, college details, and guide/coordinator placeholders
- Certificate and Acknowledgement text (preserved verbatim from the original docx)
- Project title: *Job Autofiller: Intelligent Automated Job Application System*
- Overall project goal (automate job applications end-to-end)
- Phase structure (4 phases) — only the phase content was updated to reflect what was actually built
