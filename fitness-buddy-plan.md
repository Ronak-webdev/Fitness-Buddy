# Fitness Buddy – Implementation Plan

> AICTE-2026 Problem Statement No. 13  
> **Fitness Buddy – Agentic AI Personal Fitness & Wellness Coach**

---

## Top-Level Overview

**Goal:** Build a conversational, agentic AI fitness coach that gives users personalized workout routines, meal suggestions, motivational tips, and habit-building guidance — all powered by IBM Granite via IBM watsonx.ai, deployed on IBM Cloud Lite services.

**Scope:**
- A FastAPI Python backend that orchestrates multiple specialized AI agents
- A clean, minimal React frontend (single-page chat + dashboard)
- IBM Granite (via watsonx.ai Lite) as the LLM backbone
- IBM Db2 on Cloud (Lite) for user profile and session persistence
- No mobile app, no payments, no social features — keep it focused

**Non-goals:**
- Real-time video workouts
- Wearable device integration
- Production-grade auth (a simple username-based session is enough for a demo)

---

## 1. Project Architecture

```
User (Browser)
    │
    ▼
React Frontend  ──────────────────────────────────────────────────────────────┐
    │  REST / WebSocket                                                        │
    ▼                                                                          │
FastAPI Backend (Orchestrator Agent)                                           │
    │                                                                          │
    ├── Intake Agent        ← collects/validates user profile                 │
    ├── Workout Agent       ← generates home workout plans                    │
    ├── Nutrition Agent     ← suggests simple, nutritious meals               │
    ├── Motivation Agent    ← delivers daily tips & streak encouragement      │
    └── Memory Agent        ← reads/writes user history from Db2              │
                                                                               │
    All agents call ──► IBM watsonx.ai (Granite-13b-instruct-v2 or similar)  │
                                                                               │
    IBM Db2 on Cloud (Lite) ── stores profiles, chat history, streaks ───────┘
```

**Request flow:**
1. User sends a message from the React chat UI
2. Orchestrator Agent classifies intent (workout / nutrition / motivation / profile)
3. Orchestrator delegates to the right specialized agent
4. Specialized agent fetches relevant user context from Memory Agent (Db2)
5. Agent calls IBM Granite with a crafted prompt + context
6. Response is returned, stored in Db2, and streamed back to the UI

---

## 2. Technology Stack

| Layer | Technology | Why |
|---|---|---|
| LLM | IBM Granite via watsonx.ai Python SDK | Required by problem statement |
| Backend | Python 3.11, FastAPI | Simple async API, good IBM SDK support |
| Agent framework | Custom lightweight agents (no LangChain needed) | Keeps it transparent for demo |
| Database | IBM Db2 on Cloud Lite (ibm_db Python driver) | IBM Cloud Lite compliant |
| Frontend | React 18 + Vite + Tailwind CSS | Fast, modern, minimal setup |
| Deployment | IBM Cloud Code Engine (free tier) or local Docker | IBM Cloud aligned |
| Environment | Python virtual env + `.env` for secrets | Standard, no complexity |

**IBM Cloud Lite services used:**
- `watsonx.ai` (Lite) — IBM Granite inference
- `Db2 on Cloud` (Lite) — persistent storage
- `IBM Cloud Code Engine` (free tier, optional) — serverless container hosting

---

## 3. Agent Architecture

### 3.1 Orchestrator Agent
**File:** `backend/agents/orchestrator.py`

Responsibilities:
- Receive raw user message
- Classify intent via a lightweight Granite call using a classification prompt
- Route to the correct specialized agent
- Assemble and return the final response

Intent classes: `WORKOUT | NUTRITION | MOTIVATION | PROFILE_UPDATE | GENERAL`

### 3.2 Intake / Profile Agent
**File:** `backend/agents/profile_agent.py`

Responsibilities:
- On first interaction, ask structured questions: age, fitness level, goals, equipment availability, dietary restrictions
- Validate and store answers in Db2 via Memory Agent
- Populate `UserProfile` dataclass used by all other agents

### 3.3 Workout Agent
**File:** `backend/agents/workout_agent.py`

Responsibilities:
- Accept `UserProfile` + user request
- Build a Granite prompt that requests a structured home workout (no equipment assumed by default)
- Return a structured workout plan: warm-up, main exercises, cooldown, duration
- Vary plans daily using a day-of-week seed in the prompt

### 3.4 Nutrition Agent
**File:** `backend/agents/nutrition_agent.py`

Responsibilities:
- Accept `UserProfile` + user request
- Build a Granite prompt for a simple, nutritious meal plan (breakfast/lunch/dinner/snack)
- Respect dietary restrictions from profile
- Suggest meals from common, accessible Indian/global ingredients

### 3.5 Motivation Agent
**File:** `backend/agents/motivation_agent.py`

Responsibilities:
- Generate a daily motivational message tailored to user streak and goal
- Provide habit-building micro-tips
- Track and display current streak from Db2

### 3.6 Memory Agent (shared utility)
**File:** `backend/agents/memory_agent.py`

Responsibilities:
- Read/write `UserProfile` to Db2
- Read/write chat history (last N turns for context window)
- Increment workout/streak counters
- Provide context bundle to other agents

---

## 4. IBM Granite Integration

**Model:** `ibm/granite-13b-instruct-v2` (available on watsonx.ai Lite)  
**Fallback:** `ibm/granite-3-8b-instruct` if 13b is not on Lite tier

**SDK:** `ibm-watsonx-ai` Python package

**Authentication pattern:**
```
WATSONX_API_KEY=<IBM Cloud API key>
WATSONX_PROJECT_ID=<watsonx.ai project ID>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Prompt engineering approach:**
- System prompt defines agent persona and output format
- User context (profile, history) injected into the prompt as structured text
- Output is requested in JSON for structured responses (workout plans, meal plans)
- Temperature 0.7 for motivational content, 0.2 for structured plans

**File:** `backend/llm/granite_client.py` — single wrapper class around the IBM SDK that all agents use

**Rate limiting:** Lite tier has limits; implement a simple retry with backoff in the wrapper

---

## 5. IBM Cloud Lite Integration

### Db2 on Cloud (Lite)
- Free tier: 200 MB storage — more than enough for a demo
- Connection via `ibm_db` Python driver
- Schema: 3 tables — `users`, `chat_history`, `daily_logs`
- Connection string stored in `.env`

**File:** `backend/db/db2_client.py` — connection pool wrapper  
**File:** `backend/db/schema.sql` — table definitions and seed data

### watsonx.ai (Lite)
- Free tier: 50,000 tokens/month — sufficient for a demo
- API key from IBM Cloud console

### Optional: IBM Cloud Code Engine
- Deploy backend container for public demo URL
- Dockerfile provided in repo

---

## 6. Data / RAG Approach

For this student project, **full RAG is not required**. Instead:

**Profile-augmented prompting** (simpler, works great for this scope):
- User profile + last 5 chat turns are prepended to every Granite prompt
- This gives "memory" without vector databases
- 5 turns ≈ ~800 tokens — well within Lite tier limits

**Static knowledge files (optional enhancement):**
- `backend/data/exercises.json` — curated list of 50 home exercises with descriptions
- `backend/data/meals.json` — curated list of 30 quick healthy meal ideas
- These are injected into the Workout/Nutrition agent prompts as a reference list
- This improves response quality without needing a vector DB

If the team wants to show RAG for extra credit, they can use a lightweight in-memory vector store (`chromadb` or `faiss`) with these JSON files — but this is optional.

---

## 7. User Input and Output Flow

### First-time user flow
```
User opens app
    → Frontend shows welcome screen
    → User clicks "Start"
    → Intake Agent asks 5 onboarding questions (one at a time)
    → Profile saved to Db2
    → Dashboard unlocked
```

### Returning user flow
```
User opens app
    → Profile loaded from Db2
    → Dashboard shows today's streak, last workout, daily tip
    → User types in chat: "Give me a 20-minute leg workout"
    → Orchestrator → Workout Agent → Granite → structured plan
    → Response shown as formatted card in chat
```

### Chat input types
| User says | Routed to |
|---|---|
| "workout", "exercise", "routine" | Workout Agent |
| "eat", "meal", "food", "diet" | Nutrition Agent |
| "motivate me", "I feel lazy", "tip" | Motivation Agent |
| "update my goal", "I'm now intermediate" | Profile Agent |
| anything else | General (Orchestrator handles directly) |

---

## 8. Project Folder/File Structure

```
FitnessBuddy/
├── fitness-buddy-plan.md          ← this file
├── AGENTS.md                      ← project guidance for AI agents
├── README.md                      ← project overview and setup steps
├── .env.example                   ← template for environment variables
├── .gitignore
│
├── backend/
│   ├── main.py                    ← FastAPI app entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py        ← routes requests to specialized agents
│   │   ├── profile_agent.py       ← onboarding and profile management
│   │   ├── workout_agent.py       ← generates workout plans
│   │   ├── nutrition_agent.py     ← generates meal suggestions
│   │   ├── motivation_agent.py    ← motivational tips and streaks
│   │   └── memory_agent.py        ← Db2 read/write helpers
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── granite_client.py      ← IBM Granite / watsonx.ai wrapper
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── db2_client.py          ← Db2 connection and query helpers
│   │   └── schema.sql             ← CREATE TABLE statements
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                ← UserProfile dataclass
│   │   ├── workout.py             ← WorkoutPlan dataclass
│   │   └── chat.py                ← ChatMessage dataclass
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py                ← POST /chat endpoint
│   │   ├── profile.py             ← GET/POST /profile endpoints
│   │   └── dashboard.py           ← GET /dashboard endpoint
│   │
│   └── data/
│       ├── exercises.json         ← curated home exercise list
│       └── meals.json             ← curated healthy meal list
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    │
    └── src/
        ├── main.jsx
        ├── App.jsx
        │
        ├── components/
        │   ├── ChatWindow.jsx     ← main chat interface
        │   ├── MessageBubble.jsx  ← individual message display
        │   ├── WorkoutCard.jsx    ← formatted workout plan card
        │   ├── MealCard.jsx       ← formatted meal suggestion card
        │   ├── Dashboard.jsx      ← streak, goals, quick actions
        │   └── OnboardingForm.jsx ← first-time setup questions
        │
        ├── hooks/
        │   └── useChat.js         ← API call logic
        │
        └── styles/
            └── index.css          ← Tailwind base styles
```

---

## 9. UI Design

**Layout:** Two-column on desktop, stacked on mobile
- Left/top: Dashboard panel (streak, today's goal, quick action buttons)
- Right/bottom: Chat window (conversation history + input box)

**Chat response cards:**
- **Workout card:** Exercise list with sets/reps, duration badge, difficulty indicator
- **Meal card:** Meal name, ingredients list, simple emoji for food type
- **Motivation card:** Inspirational quote box with a pastel background

**Color palette:** Clean, energetic — white background, green accents (#22c55e), dark text
**Font:** Inter (clean, modern, readable)
**Icons:** Lucide React (lightweight, consistent)

**Key screens:**
1. **Welcome / Onboarding** — centered card, step-by-step questions
2. **Main App** — dashboard + chat
3. **Profile page** — view/edit fitness profile

---

## 10. Testing Strategy

### Backend tests
**Framework:** `pytest`  
**Location:** `backend/tests/`

| Test file | What it tests |
|---|---|
| `test_granite_client.py` | Mock IBM API call, verify prompt structure |
| `test_orchestrator.py` | Intent classification accuracy |
| `test_workout_agent.py` | Plan generation with mock Granite response |
| `test_nutrition_agent.py` | Meal generation with dietary restrictions |
| `test_db2_client.py` | Db2 read/write with test database |
| `test_api_chat.py` | End-to-end API endpoint with mocked agents |

**Run all tests:** `cd backend && pytest`  
**Run single test:** `cd backend && pytest tests/test_orchestrator.py -v`  
**Run with coverage:** `cd backend && pytest --cov=. --cov-report=term-missing`

### Frontend tests
**Framework:** Vitest + React Testing Library  
**Location:** `frontend/src/__tests__/`

| Test file | What it tests |
|---|---|
| `ChatWindow.test.jsx` | Message rendering and scroll behavior |
| `WorkoutCard.test.jsx` | Structured plan display |
| `useChat.test.js` | API hook logic |

**Run:** `cd frontend && npm test`

### Manual demo test cases (documented in README)
1. New user onboarding flow
2. Workout request for beginner with no equipment
3. Vegetarian meal suggestion
4. Motivational message when streak = 0
5. Profile update flow

---

## 11. Final Demonstration Plan

**Demo format:** Live walkthrough (5–7 minutes) + poster/README

**Demo script:**
1. **Intro** (30s): "Fitness Buddy is an agentic AI coach powered by IBM Granite"
2. **Onboarding** (1 min): Show first-time user setup — answer 5 questions, profile saved
3. **Workout agent** (1.5 min): Ask for a "20-minute beginner home workout" — show structured Workout Card response
4. **Nutrition agent** (1 min): Ask for "a healthy breakfast suggestion" — show Meal Card
5. **Motivation agent** (30s): Click "Motivate Me" button — show streak + personalized tip
6. **Agentic routing** (1 min): Show that asking "I updated my goal to lose weight" triggers Profile Agent
7. **IBM stack** (1 min): Show IBM Cloud console — watsonx.ai project, Db2 instance, token usage

**Key talking points:**
- Agentic AI: multiple specialized agents, orchestration pattern
- IBM Granite: IBM's enterprise-grade LLM
- IBM Cloud Lite: fully free-tier compliant
- Profile-augmented prompting: personalized without a vector DB

---

## 12. Dependencies and Setup Requirements

### Prerequisites
- IBM Cloud account (free): https://cloud.ibm.com/registration
- watsonx.ai project created with IBM Granite model enabled
- Db2 on Cloud Lite instance provisioned
- Python 3.11+
- Node.js 18+

### Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env         # fill in IBM credentials
python main.py                  # starts on http://localhost:8000
```

### Frontend setup
```bash
cd frontend
npm install
npm run dev                     # starts on http://localhost:5173
```

### Environment variables (.env.example)
```
# IBM watsonx.ai
WATSONX_API_KEY=
WATSONX_PROJECT_ID=
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# IBM Db2 on Cloud
DB2_DSN=
DB2_USER=
DB2_PASSWORD=

# App settings
APP_SECRET_KEY=fitness-buddy-dev-key
CORS_ORIGIN=http://localhost:5173
```

### Key Python packages (requirements.txt)
```
fastapi==0.111.0
uvicorn==0.29.0
ibm-watsonx-ai==1.0.4
ibm_db==3.2.3
pydantic==2.7.0
python-dotenv==1.0.1
httpx==0.27.0
pytest==8.2.0
pytest-cov==5.0.0
pytest-asyncio==0.23.6
```

### Key npm packages (package.json)
```json
{
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "lucide-react": "^0.395.0",
    "axios": "^1.7.0"
  },
  "devDependencies": {
    "vite": "^5.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "tailwindcss": "^3.4.0",
    "vitest": "^1.6.0",
    "@testing-library/react": "^16.0.0"
  }
}
```

---

## Sub-Tasks (Implementation Order)

### Sub-Task 1: Project Scaffolding
**Intent:** Create all directories, config files, and empty stubs so the structure is in place before writing logic.  
**Expected Outcomes:** All folders and placeholder files exist; `git init` done; `.env.example` created.  
**Todo:**
1. Create directory structure as shown in Section 8
2. Initialize Python venv and `requirements.txt`
3. Initialize `package.json` for frontend with Vite + React + Tailwind
4. Create `.env.example` with all required keys
5. Create `.gitignore`
6. Create `README.md` with setup instructions
**Status:** [ ] pending

---

### Sub-Task 2: IBM Granite Client
**Intent:** Build the single reusable wrapper around the IBM watsonx.ai SDK that all agents will call.  
**Expected Outcomes:** `backend/llm/granite_client.py` works — can send a prompt to IBM Granite and receive a response. Mock test passes.  
**Todo:**
1. Implement `GraniteClient` class in `backend/llm/granite_client.py`
2. Add `generate(prompt, system_prompt, temperature, max_tokens)` method
3. Add retry logic with exponential backoff for rate-limit errors
4. Add token usage logging (important for Lite tier awareness)
5. Write `backend/tests/test_granite_client.py` with mocked IBM SDK
**Relevant context:** `ibm-watsonx-ai` SDK, `ibm_watson_machine_learning` legacy SDK also works
**Status:** [ ] pending

---

### Sub-Task 3: Db2 Client and Schema
**Intent:** Set up persistent storage for user profiles and chat history.  
**Expected Outcomes:** `backend/db/db2_client.py` connects to Db2; `schema.sql` creates the 3 tables; seed data inserts correctly.  
**Todo:**
1. Write `backend/db/schema.sql` with `users`, `chat_history`, `daily_logs` tables
2. Implement `Db2Client` class with `execute_query`, `fetch_one`, `fetch_all` methods
3. Add connection pooling (simple retry on disconnect)
4. Write `backend/tests/test_db2_client.py` with SQLite as a test double
5. Run schema against real Db2 Lite instance to verify
**Status:** [ ] pending

---

### Sub-Task 4: Agent Implementations
**Intent:** Build all 5 agents using the Granite client and Memory Agent.  
**Expected Outcomes:** Each agent has a `run(user_message, user_profile, chat_history)` method that returns a structured response dict.  
**Todo:**
1. Implement `MemoryAgent` (Db2 read/write helpers)
2. Implement `ProfileAgent` (onboarding question flow, profile persistence)
3. Implement `WorkoutAgent` (structured workout plan generation)
4. Implement `NutritionAgent` (meal suggestion generation with dietary filters)
5. Implement `MotivationAgent` (streak-aware motivational message)
6. Implement `OrchestratorAgent` (intent classification + routing)
7. Write unit tests for each agent with mocked Granite responses
**Status:** [ ] pending

---

### Sub-Task 5: FastAPI Backend
**Intent:** Expose the agents via HTTP endpoints.  
**Expected Outcomes:** `POST /chat` returns a structured response; `GET /dashboard` returns streak and profile; `GET/POST /profile` manages user profile.  
**Todo:**
1. Create FastAPI app in `backend/main.py` with CORS configured
2. Implement `POST /api/chat` endpoint in `backend/api/chat.py`
3. Implement `GET/POST /api/profile` in `backend/api/profile.py`
4. Implement `GET /api/dashboard` in `backend/api/dashboard.py`
5. Add simple session management (cookie-based username, no auth needed for demo)
6. Write `backend/tests/test_api_chat.py` end-to-end test
7. Verify all endpoints with `curl` or Postman
**Status:** [ ] pending

---

### Sub-Task 6: React Frontend
**Intent:** Build the chat UI and dashboard.  
**Expected Outcomes:** User can open the app, complete onboarding, send chat messages, and see formatted workout/meal/motivation cards.  
**Todo:**
1. Set up Vite + React + Tailwind project in `frontend/`
2. Build `ChatWindow.jsx` with message history and input box
3. Build `MessageBubble.jsx` that renders plain text or structured cards based on message type
4. Build `WorkoutCard.jsx` and `MealCard.jsx` components
5. Build `Dashboard.jsx` with streak counter and quick-action buttons
6. Build `OnboardingForm.jsx` for first-time setup
7. Implement `useChat.js` hook for API communication
8. Wire up routing: `/onboarding` → `/app`
9. Run frontend tests with Vitest
**Status:** [ ] pending

---

### Sub-Task 7: Static Data Files
**Intent:** Create curated exercise and meal reference data to improve response quality.  
**Expected Outcomes:** `backend/data/exercises.json` and `backend/data/meals.json` exist with at least 20 entries each.  
**Todo:**
1. Create `exercises.json` with home-friendly exercises (name, description, muscles, difficulty)
2. Create `meals.json` with quick healthy meals (name, ingredients, prep_time, category, dietary_tags)
3. Update WorkoutAgent and NutritionAgent to inject this data into prompts
**Status:** [ ] pending

---

### Sub-Task 8: End-to-End Integration and Demo Prep
**Intent:** Verify the full system works end-to-end, fix integration bugs, and prepare the demo.  
**Expected Outcomes:** All 5 demo script scenarios from Section 11 work correctly. README is complete.  
**Todo:**
1. Run full end-to-end test of all 5 demo scenarios
2. Fix any integration bugs between frontend and backend
3. Update README with complete setup instructions and screenshots
4. Create a `demo-data.sql` seed script to pre-populate a demo user
5. Add a `Dockerfile` and `docker-compose.yml` for easy local startup
6. Optional: Deploy to IBM Cloud Code Engine for a public demo URL
**Status:** [ ] pending
