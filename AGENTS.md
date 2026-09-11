# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Identity
**Fitness Buddy** — AICTE-2026 Problem Statement No. 13  
Agentic AI personal fitness coach powered by IBM Granite (watsonx.ai) and IBM Cloud Lite.

## Stack
- **Backend:** Python 3.11, FastAPI, `ibm-watsonx-ai` SDK, `ibm_db` (Db2)
- **Frontend:** React 18 + Vite + Tailwind CSS
- **LLM:** `ibm/granite-13b-instruct-v2` via IBM watsonx.ai Lite
- **Database:** IBM Db2 on Cloud Lite (3 tables: `users`, `chat_history`, `daily_logs`)

## Essential Commands
```bash
# Backend (run from backend/)
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py                          # starts on :8000

# Run all tests
cd backend && pytest
# Run single test file
cd backend && pytest tests/test_orchestrator.py -v
# Run with coverage
cd backend && pytest --cov=. --cov-report=term-missing

# Frontend (run from frontend/)
npm install
npm run dev                             # starts on :5173
cd frontend && npm test
```

## Non-Obvious Project Rules

### IBM Granite client
- **All LLM calls go through `backend/llm/granite_client.py`** — never call the IBM SDK directly from agents.
- Temperature must be `0.2` for structured outputs (workouts, meals) and `0.7` for motivational text.
- The Lite tier limit is ~50,000 tokens/month — log usage in every call via `granite_client.py`.
- Retry with exponential backoff is mandatory — IBM Lite rate-limits aggressively.

### Agents
- Every agent `run()` method signature must be: `run(user_message: str, user_profile: UserProfile, chat_history: list[ChatMessage]) -> dict`
- The Orchestrator classifies intent before any agent is called — never bypass it.
- Intent classes are: `WORKOUT | NUTRITION | MOTIVATION | PROFILE_UPDATE | GENERAL`

### Db2
- Use `backend/db/db2_client.py` wrappers — never write raw `ibm_db` calls in agents.
- In tests, substitute SQLite as a test double for Db2 (Db2 is not available in CI).
- Schema is defined in `backend/db/schema.sql` — always migrate via that file.

### Data files
- `backend/data/exercises.json` and `backend/data/meals.json` are injected into Granite prompts — do not delete or restructure them.
- The Workout and Nutrition agents read these files at startup and cache them in memory.

### Frontend
- Chat responses include a `type` field (`text | workout | meal | motivation`) — `MessageBubble.jsx` switches rendering based on this.
- All API calls go through `frontend/src/hooks/useChat.js` — do not call `axios` directly from components.

## Environment Variables (required)
See `.env.example` — all four IBM credentials must be set before the backend starts:
`WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL`, `DB2_DSN`, `DB2_USER`, `DB2_PASSWORD`

## Implementation Plan
Full architecture, sub-tasks, and demo script: **`fitness-buddy-plan.md`**
