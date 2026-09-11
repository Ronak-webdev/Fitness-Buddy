# AGENTS.md — Ask Mode

This file provides guidance to agents when working with code in this repository.

## Key Documentation Locations
- **Full architecture and sub-tasks:** `fitness-buddy-plan.md`
- **IBM Granite usage:** `backend/llm/granite_client.py` is the canonical reference
- **Database schema:** `backend/db/schema.sql` (single source of truth for table structure)
- **Agent routing logic:** `backend/agents/orchestrator.py` (intent → agent mapping)
- **Curated fitness data:** `backend/data/exercises.json`, `backend/data/meals.json`

## Non-Obvious Context
- The project uses **profile-augmented prompting**, not RAG — user profile + last 5 chat turns are prepended to every Granite prompt.
- IBM watsonx.ai Lite is ~50,000 tokens/month free — token logging is built into `GraniteClient`.
- IBM Db2 on Cloud Lite is 200 MB free — sufficient for a demo with hundreds of users.
- The frontend `type` field in API responses drives which React component renders (not a content-type header).
- "Memory Agent" is not a separate service — it is a utility class called by other agents to abstract Db2 access.
