"""
backend/api/dashboard.py
-------------------------
GET /api/dashboard — returns the data for the Dashboard panel.

Payload:
  {
    "streak":            int,
    "goal":              str,
    "fitness_level":     str,
    "last_workout_date": str | null,
    "daily_tip":         str
  }
"""

import logging
from typing import Optional

from fastapi import APIRouter, Cookie, HTTPException, Request, status

router = APIRouter(tags=["dashboard"])
logger = logging.getLogger(__name__)


@router.get("/dashboard")
async def get_dashboard(
    request: Request,
    username: Optional[str] = Cookie(default=None),
) -> dict:
    """
    Return summary data for the Dashboard panel in the frontend.
    Called on every page load to refresh streak, goal, and daily tip.
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active session.",
        )

    memory_agent = request.app.state.memory_agent
    motivation_agent = request.app.state.motivation_agent

    # ------------------------------------------------------------------
    # 1. Load profile
    # ------------------------------------------------------------------
    profile = await memory_agent.get_profile(username)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Visit /api/profile/start first.",
        )

    # ------------------------------------------------------------------
    # 2. Get current streak from daily_logs
    # ------------------------------------------------------------------
    streak = await memory_agent.get_streak(username)

    # ------------------------------------------------------------------
    # 3. Generate a personalised daily tip via MotivationAgent
    # ------------------------------------------------------------------
    try:
        tip_result = await motivation_agent.run(
            user_message="Give me a short daily tip",
            user_profile=profile,
            chat_history=[],
            streak=streak,
        )
        daily_tip = tip_result.get("message", "Stay consistent — every session counts!")
    except Exception as exc:
        logger.warning("MotivationAgent failed for dashboard tip: %s", exc)
        daily_tip = "Stay consistent — every session counts!"

    # ------------------------------------------------------------------
    # 4. Return dashboard payload
    # ------------------------------------------------------------------
    return {
        "streak": streak,
        "goal": profile.primary_goal.value,
        "fitness_level": profile.fitness_level.value,
        "onboarding_complete": profile.onboarding_complete,
        "daily_tip": daily_tip,
    }
