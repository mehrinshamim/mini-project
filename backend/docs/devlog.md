# Dev Log

---

## 2026-03-24 — Groq TPD Exhaustion During Job Scoring

### Error Encountered
```
Task app.worker.tasks.score_jobs_task[76a8e52f-...] retry: Retry in 15s:
RateLimitError("Error code: 429 - Rate limit reached for model
`llama-3.3-70b-versatile` on tokens per day (TPD): Limit 100000,
Used 99125, Requested 1218. Please try again in 4m56.352s.")
```

The task retried every 15s even though Groq said to wait ~5 minutes. All 3 retries were burned in 45 seconds on a limit that required a ~1300 second wait, causing the task to fail permanently.

### Root Causes
1. **Wrong model for scoring:** `llama-3.3-70b-versatile` has 100K TPD on Groq free tier. Exhausted after ~50 scoring calls.
2. **Hardcoded retry countdown:** `countdown=15` in the Celery retry ignores the actual wait time from Groq's error.
3. **No input truncation:** Full resume markdown from Docling (10K+ chars) sent with every call, inflating token usage.

### Decision: Three-Fix Approach

**Fix 1 — Smart retry countdown** (`tasks.py`)
- Add `_parse_retry_after(exc: groq.RateLimitError) -> int` helper
- Reads `exc.response.headers["retry-after"]` (integer seconds from Groq), falls back to regex on message string
- `score_jobs_task` catches `groq.RateLimitError` before bare `Exception`
- `max_retries` raised from 3 → 10

**Fix 2 — Use higher-quota model for scoring** (`config.py`, `reasoning.py`)
- Add `SCORING_MODEL = "llama-3.1-8b-instant"` (500K TPD, 20K TPM)
- `ReasoningService.score()` uses `SCORING_MODEL`
- `LLM_MODEL` (`llama-3.3-70b-versatile`) reserved for Phase 4 answer generation

**Fix 3 — Input truncation** (`reasoning.py`)
- `resume_markdown[:6000]`, `job_description[:4000]` at top of `score()`
- Reduces per-call tokens from ~3K to ~2.2K
- OK for scoring (rough filter); Phase 4 uses full content

### Phase 4 Note
`ExtensionService` (answer generation) must also implement smart retry using the same `_parse_retry_after` helper. It uses `LLM_MODEL` (70b) and sends full (untruncated) content, so it will hit TPD limits faster. Budget usage accordingly.
