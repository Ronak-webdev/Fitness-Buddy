# AGENTS.md — Plan Mode

This file provides guidance to agents when working with code in this repository.

## Architectural Constraints

### Agent system
- Agents are **stateless** — all state lives in Db2 via MemoryAgent. Never store user state inside an agent instance.
- The Orchestrator is the **only entry point** from the API — agents must not call each other directly.
- Intent classification happens via a Granite call, not regex — this ensures natural language edge cases are handled.

### IBM Lite tier limits
- **watsonx.ai Lite:** ~50,000 tokens/month — keep prompts lean; no RAG unless explicitly needed.
- **Db2 Lite:** 200 MB — store only `user_id`, profile fields, and last 20 chat turns per user.
- **Code Engine:** Free tier has cold starts — backend must start in < 10 seconds (no heavy startup loading).

### Data flow constraint
- Static data files (`exercises.json`, `meals.json`) are loaded once at backend startup and held in memory — do not reload per-request.
- Chat history context window is capped at **5 turns** to stay within token budget.

### Frontend–backend contract
- The API response envelope is always `{ "type": str, "data": dict, "message": str }` — changing this breaks all frontend card components.
- The frontend does NOT manage user profile state locally — it always fetches from `GET /api/profile`.

### What NOT to add
- No vector database (Chroma, FAISS) unless the team explicitly needs RAG for extra credit.
- No user authentication beyond a username cookie — this is a demo project.
- No streaming responses — full response returned as JSON (simpler, more reliable on Lite tier).
