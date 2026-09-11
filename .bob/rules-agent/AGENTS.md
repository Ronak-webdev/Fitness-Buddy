# AGENTS.md — Agent (Coding) Mode

This file provides guidance to agents when working with code in this repository.

## Critical Coding Rules

### IBM Granite
- `GraniteClient.generate()` is the ONLY way to call the LLM — no direct SDK calls in agents.
- Always pass `system_prompt` separately; never concatenate it into `prompt`.
- Structured outputs (WorkoutPlan, MealPlan) must request JSON in the system prompt and parse with `json.loads()` wrapped in a try/except.

### Agent contract
- All agents live in `backend/agents/` and inherit nothing — they are plain classes.
- Required method signature: `run(user_message, user_profile, chat_history) -> dict`
- Response dict must always contain `type` key: `"text" | "workout" | "meal" | "motivation"`.

### Db2
- Connection is a module-level singleton in `db2_client.py` — do not instantiate per-request.
- Use parameterized queries only (`?` placeholders) — never f-string SQL.
- In test files, mock `Db2Client` entirely; don't connect to real Db2 in pytest.

### FastAPI
- All endpoints are prefixed `/api/` — do not add bare routes.
- CORS origin is read from `CORS_ORIGIN` env var, not hardcoded.
- Session is cookie-based (`username` cookie) — no JWT needed.

### Frontend
- Tailwind only — no inline styles, no CSS modules.
- All API base URL comes from `import.meta.env.VITE_API_URL` (default `http://localhost:8000`).
- `WorkoutCard.jsx` and `MealCard.jsx` receive the raw dict from the API response `data` field.
