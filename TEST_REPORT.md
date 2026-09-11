# Fitness Buddy - Test Report

## Overview
This document summarizes the testing strategy, execution, and results for the Fitness Buddy application (AICTE-2026 Problem Statement No. 13). 

The test suite is built using `pytest` and uses `pytest-asyncio` for asynchronous endpoint testing. It separates tests into components that are purely logic-driven and components that require external integrations.

## Test Results
**Total Tests**: 17
**Status**: PASSED (17/17)
**Framework**: `pytest`

### Tests Passing Without External Credentials (Mocked/Local)
These tests validate application logic, state routing, agent prompts, and JSON parsing without making network requests to IBM Cloud:

1. **Orchestrator Agent Routing**
   - `test_classify_workout_intent`: Verifies user messages about workouts are routed to `WorkoutAgent`.
   - `test_classify_meal_intent`: Verifies user messages about food/meals are routed to `NutritionAgent`.
   - `test_classify_motivation_intent`: Verifies motivation queries are routed to `MotivationAgent`.
   - `test_classify_profile_intent`: Verifies onboarding/profile queries are routed to `ProfileAgent`.
2. **Specialized Agents**
   - `test_run_returns_correct_type` (WorkoutAgent): Verifies structured output is parsed into a `WorkoutPlan`.
   - `test_run_returns_fallback_on_parse_error` (WorkoutAgent): Verifies graceful fallback on malformed JSON.
   - `test_run_returns_meal_type` (NutritionAgent): Verifies meal requests return `type="meal"`.
   - `test_run_returns_motivation_type` (MotivationAgent): Verifies motivation requests return `type="motivation"`.
3. **API Endpoints**
   - `test_health_check`: Validates the `/api/health` endpoint.
   - `test_get_profile_returns_404_for_unknown_user`: Checks error handling for non-existent sessions.
   - `test_start_session_creates_user`: Validates user creation logic using the in-memory fallback database.
   - `test_chat_requires_session`: Ensures the chat endpoint rejects unauthenticated requests.
   - `test_chat_returns_200`: Validates the chat endpoint returns a properly structured `ChatResponse`.
4. **IBM Granite Client (Mocked)**
   - `test_init_sets_model_id`: Verifies config loading.
   - `test_generate_returns_string`: Verifies return types when mocked.
   - `test_generate_tracks_token_usage`: Ensures the `token_usage` counter properly increments based on mocked HTTP responses.
   - `test_generate_raises_on_empty_response`: Verifies error handling.

### Tests Requiring Live Credentials (Manual Validation)
The following components require valid IBM Db2 and Granite credentials in the `.env` file to fully validate in production:

1. **IBM Db2 Integration**
   - Real database queries in `db2_client.py` using `ibm_db` (currently falling back to in-memory dicts in local dev).
   - Validation of `schema.sql` migration against the live instance.
2. **IBM Granite Integration**
   - `_call_watsonx` function in `granite_client.py` which makes live HTTP requests to `us-south.ml.cloud.ibm.com`.
   - Token usage and rate limit compliance under the Lite tier (~50k tokens/month).

## Remaining Manual Setup
To transition this project from local mocked development to a fully integrated live deployment:

1. **Provision Db2**: Create a Db2 on Cloud Lite instance on IBM Cloud.
2. **Apply Schema**: Run the SQL commands in `backend/db/schema.sql` on the live Db2 instance.
3. **Configure .env**: Populate `DB2_DSN`, `DB2_USER`, and `DB2_PASSWORD` in the root `.env` file.
4. **Verify Live Fallbacks**: Start the backend and verify that `db2_client.py` connects to Db2 successfully instead of falling back to the in-memory store.
