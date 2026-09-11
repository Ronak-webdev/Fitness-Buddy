"""
backend/main.py
---------------
FastAPI application entry point.

Startup lifecycle:
  1. Connect GraniteClient (IAM token exchange)
  2. Connect Db2Client
  3. Instantiate all agents and store on app.state
  4. Register routers

Singleton agents are accessed in route handlers via request.app.state.*
"""

import logging
import sys
from pathlib import Path

# Ensure both repository root and backend directory are in sys.path
_backend_dir = Path(__file__).resolve().parent
_repo_root = _backend_dir.parent
for _p in (str(_repo_root), str(_backend_dir)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

try:
    from backend.config import settings
    from backend.api.chat import router as chat_router
    from backend.api.profile import router as profile_router
    from backend.api.dashboard import router as dashboard_router
except ImportError:
    from config import settings
    from api.chat import router as chat_router
    from api.profile import router as profile_router
    from api.dashboard import router as dashboard_router

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Configure logging before anything else
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Application lifespan (replaces deprecated on_event handlers)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: connect IBM clients and instantiate all agents.
    Shutdown: close connections gracefully.
    """
    # ---- STARTUP ----
    logger.info("=== Fitness Buddy API starting up ===")

    # Import here to avoid circular imports at module level
    try:
        from backend.llm.granite_client import GraniteClient
        from backend.db.db2_client import Db2Client
        from backend.agents.memory_agent import MemoryAgent
        from backend.agents.workout_agent import WorkoutAgent
        from backend.agents.nutrition_agent import NutritionAgent
        from backend.agents.motivation_agent import MotivationAgent
        from backend.agents.profile_agent import ProfileAgent
        from backend.agents.orchestrator import OrchestratorAgent
    except ImportError:
        from llm.granite_client import GraniteClient
        from db.db2_client import Db2Client
        from agents.memory_agent import MemoryAgent
        from agents.workout_agent import WorkoutAgent
        from agents.nutrition_agent import NutritionAgent
        from agents.motivation_agent import MotivationAgent
        from agents.profile_agent import ProfileAgent
        from agents.orchestrator import OrchestratorAgent

    # 1. IBM Granite (watsonx.ai)
    granite = GraniteClient(
        api_key=settings.watsonx_api_key,
        project_id=settings.watsonx_project_id,
        watsonx_url=settings.watsonx_url,
        model_id=settings.granite_model_id,
    )
    logger.info("GraniteClient initialised (model=%s)", settings.granite_model_id)

    # 2. IBM Db2 on Cloud
    db2 = Db2Client(
        dsn=settings.db2_dsn,
        user=settings.db2_user,
        password=settings.db2_password,
    )
    await db2.connect()
    logger.info("Db2Client connected")

    # 3. Agents
    memory_agent = MemoryAgent(db_client=db2)
    workout_agent = WorkoutAgent(granite_client=granite)
    nutrition_agent = NutritionAgent(granite_client=granite)
    motivation_agent = MotivationAgent(granite_client=granite)
    profile_agent = ProfileAgent(granite_client=granite, memory_agent=memory_agent)
    orchestrator = OrchestratorAgent(
        granite_client=granite,
        workout_agent=workout_agent,
        nutrition_agent=nutrition_agent,
        motivation_agent=motivation_agent,
        profile_agent=profile_agent,
        memory_agent=memory_agent,
    )
    logger.info("All agents instantiated")

    # 4. Attach to app.state so route handlers can access them
    app.state.granite = granite
    app.state.db2 = db2
    app.state.memory_agent = memory_agent
    app.state.workout_agent = workout_agent
    app.state.nutrition_agent = nutrition_agent
    app.state.motivation_agent = motivation_agent
    app.state.profile_agent = profile_agent
    app.state.orchestrator = orchestrator

    logger.info("=== Fitness Buddy API ready ===")

    yield  # Application runs here

    # ---- SHUTDOWN ----
    logger.info("=== Fitness Buddy API shutting down ===")
    try:
        await db2.disconnect()
        logger.info("Db2Client disconnected")
    except Exception as exc:
        logger.warning("Error during Db2 disconnect: %s", exc)


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Fitness Buddy API",
    description=(
        "Agentic AI Personal Fitness & Wellness Coach — "
        "AICTE 2026 Problem Statement No. 13"
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow the React dev server (and any configured origin)
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(chat_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Liveness probe — returns OK when the server is running."""
    return {"status": "ok", "service": "fitness-buddy-api", "version": "0.1.0"}


# ---------------------------------------------------------------------------
# Dev server entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
