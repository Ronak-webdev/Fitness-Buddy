# Fitness Buddy - Final Project Report

## Project Identification
**Problem Statement No:** 13 (Fitness Buddy)
**Hackathon:** AICTE-2026
**Tech Stack:** React, FastAPI, IBM Granite, IBM Db2

## Executive Summary
Fitness Buddy is an Agentic AI personal fitness coach that provides tailored workout routines, healthy meal suggestions, and daily motivation. The system leverages an orchestrator pattern to classify user intent and route queries to specialized agents, utilizing IBM Granite (watsonx.ai) for natural language understanding and generation.

## Accomplishments
- **Agentic Architecture**: Implemented a multi-agent backend consisting of an Orchestrator, WorkoutAgent, NutritionAgent, MotivationAgent, and ProfileAgent.
- **Robust Prompting**: Enforced structured JSON output from IBM Granite for complex domains (Workouts, Nutrition) using low temperature (0.2), while using higher temperatures (0.7) for motivational text.
- **Resilient Infrastructure**: Created a graceful fallback mechanism for IBM Db2, allowing the application to run entirely in-memory for local development when credentials are not available.
- **Modern Frontend**: Built a responsive React + Tailwind frontend featuring a personalized dashboard, streak tracking, and specialized rendering components for workout and meal cards.

## Code Quality & Testing
- Fully typed Python backend using `pydantic` for strict data validation (`UserProfile`, `WorkoutPlan`, `ChatMessage`).
- 100% passing test suite (17 tests) using `pytest` and `pytest-asyncio` that verifies application logic through comprehensive mocks of external services.
- Adherence to IBM Cloud Lite tier limitations by strictly capping `max_new_tokens` and implementing a robust token tracking mechanism in `GraniteClient`.

## Alignment with Problem Statement
The project successfully addresses all officially defined requirements for Problem Statement No. 13:
1. **Recommend home workouts**: Supported via `WorkoutAgent` and structured `WorkoutPlan` rendering.
2. **Personalized motivational tips**: Supported via `MotivationAgent` and streak tracking.
3. **Nutritious meal ideas**: Supported via `NutritionAgent`.
4. **Encourage habit-building**: Supported via daily streak tracking.
5. **On-demand access**: Supported via web UI.
6. **Use IBM Granite**: Integrated via `ibm-watsonx-ai` REST calls in `GraniteClient`.
7. **Use IBM Cloud Lite**: Optimized for the Lite tier token limits and Db2 storage constraints.
