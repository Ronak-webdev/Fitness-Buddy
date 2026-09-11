# Fitness Buddy 🏋️

> **AICTE-2026 Problem Statement No. 13**  
> Agentic AI Personal Fitness & Wellness Coach

Fitness Buddy is a conversational AI-powered health and fitness coach that provides personalized workout routines, nutritious meal ideas, daily motivational tips, and habit-building guidance — all powered by **IBM Granite** via **IBM watsonx.ai** on IBM Cloud Lite.

---

## Features

- 🏃 **Personalized home workouts** — plans tailored to your fitness level, goals, and available equipment
- 🥗 **Meal suggestions** — simple, nutritious meal ideas respecting your dietary preferences
- 💪 **Daily motivation** — streak tracking, habit-building tips, and personalized encouragement
- 🤖 **Agentic AI** — multiple specialized agents (Workout, Nutrition, Motivation, Profile) orchestrated intelligently
- 💬 **Conversational interface** — natural chat UI, ask anything fitness-related

---

## Technology Stack

| Layer | Technology |
|---|---|
| **LLM** | IBM Granite (`ibm/granite-4-h-small`) via IBM watsonx.ai Lite |
| **Backend** | Python 3.11, FastAPI |
| **Database** | IBM Db2 on Cloud Lite |
| **Frontend** | React 18, Vite, Tailwind CSS |
| **Agent Framework** | Custom lightweight agents (no LangChain) |

---

## Project Structure

```
FitnessBuddy/
├── backend/            # Python FastAPI backend + AI agents
│   ├── agents/         # Orchestrator + 4 specialized agents
│   ├── api/            # FastAPI route handlers
│   ├── db/             # Db2 client + schema
│   ├── llm/            # IBM Granite client wrapper
│   ├── models/         # Pydantic data models
│   ├── data/           # Curated exercises and meals JSON
│   └── tests/          # pytest test suite
└── frontend/           # React + Vite frontend
    └── src/
        ├── components/ # UI components (Chat, Cards, Dashboard)
        ├── hooks/      # API communication hooks
        └── styles/     # Tailwind CSS
```

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- IBM Cloud account (free): https://cloud.ibm.com/registration
- watsonx.ai project with IBM Granite model enabled
- Db2 on Cloud Lite instance

### 1. Clone and configure environment

```bash
git clone https://github.com/Ronak-webdev/Fitness-Buddy.git
cd FitnessBuddy
cp .env.example .env
# Edit .env with your IBM Cloud credentials
```

### 2. Backend

```bash
cd backend
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
python main.py
# Backend starts at http://localhost:8000
# Health check: http://localhost:8000/health
# API docs:     http://localhost:8000/docs
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
# Frontend starts at http://localhost:5173
```

---

## Running Tests

```bash
# Backend tests (from backend/)
cd backend
pytest                                          # all tests
pytest tests/test_orchestrator.py -v           # single file
pytest --cov=. --cov-report=term-missing       # with coverage

# Frontend tests (from frontend/)
cd frontend
npm test
```

---

## IBM Cloud Services Used (All Free Tier)

| Service | Purpose |
|---|---|
| **watsonx.ai Lite** | IBM Granite LLM inference (~50k tokens/month free) |
| **Db2 on Cloud Lite** | User profiles, chat history, streaks (200 MB free) |
| **IBM Cloud Code Engine** | Optional: deploy for a public demo URL |

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

| Variable | Description |
|---|---|
| `WATSONX_API_KEY` | IBM Cloud API key |
| `WATSONX_PROJECT_ID` | watsonx.ai project ID |
| `WATSONX_URL` | watsonx.ai endpoint (default: us-south) |
| `DB2_DSN` | Db2 connection string |
| `DB2_USER` | Db2 username |
| `DB2_PASSWORD` | Db2 password |
| `CORS_ORIGIN` | Frontend origin (default: http://localhost:5173) |

> **Note on Local Development**: If you do not have live IBM Db2 credentials, the application will gracefully fall back to an **in-memory** data store. This allows you to test the UI and AI agents locally without setting up the database. IBM Granite credentials (`WATSONX_API_KEY`, etc.) are still required.

---

## Demo Scenarios

1. **New user onboarding** — complete the 5-question fitness profile setup
2. **Workout request** — ask for a "20-minute beginner home workout"
3. **Meal suggestion** — ask for "a healthy vegetarian breakfast"
4. **Daily motivation** — click "Motivate Me" to see streak + personalized tip
5. **Profile update** — say "I updated my goal to lose weight"

---

## Implementation Plan

See [`fitness-buddy-plan.md`](fitness-buddy-plan.md) for the full architecture, sub-task breakdown, and demo script.

---

## License

MIT — for educational/demonstration purposes (AICTE 2026 Hackathon)
