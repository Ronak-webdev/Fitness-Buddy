"""
backend/api/profile.py
-----------------------
Profile endpoints:
  GET  /api/profile        — return current user's profile
  POST /api/profile        — create or update profile fields
  POST /api/profile/start  — create a new session (set username cookie)
"""

import logging
from typing import Optional

from fastapi import APIRouter, Cookie, HTTPException, Request, Response, status

from models.user import UserProfile

router = APIRouter(tags=["profile"])
logger = logging.getLogger(__name__)


@router.post("/profile/start", status_code=status.HTTP_200_OK)
async def start_session(
    username: str,
    response: Response,
    request: Request,
) -> dict:
    """
    Create a new session cookie for the given username.
    This is the entry point for new and returning users.

    The username acts as the user_id throughout the application.
    (No password — this is a demo project.)
    """
    if not username or len(username.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username must be at least 2 characters.",
        )

    clean_username = username.strip().lower()
    memory_agent = request.app.state.memory_agent

    # Check if user already exists in Db2
    existing_profile = await memory_agent.get_profile(clean_username)
    is_new_user = existing_profile is None

    if is_new_user:
        # Create a minimal profile — onboarding will fill it in via chat
        new_profile = UserProfile(user_id=clean_username, name=clean_username)
        await memory_agent.save_profile(new_profile)
        logger.info("New user created: %s", clean_username)
    else:
        logger.info("Returning user session: %s (streak=%d)", clean_username, existing_profile.current_streak)

    # Set a session cookie (HttpOnly, SameSite=Lax)
    response.set_cookie(
        key="username",
        value=clean_username,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,  # 30 days
    )

    return {
        "message": f"Session started for '{clean_username}'",
        "is_new_user": is_new_user,
    }


@router.get("/profile", response_model=UserProfile)
async def get_profile(
    request: Request,
    username: Optional[str] = Cookie(default=None),
) -> UserProfile:
    """Return the current user's fitness profile."""
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active session. Visit /api/profile/start first.",
        )

    memory_agent = request.app.state.memory_agent
    profile = await memory_agent.get_profile(username)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile not found for user '{username}'. Visit /api/profile/start first.",
        )

    return profile


@router.post("/profile", response_model=UserProfile)
async def update_profile(
    updates: dict,
    request: Request,
    username: Optional[str] = Cookie(default=None),
) -> UserProfile:
    """Update one or more fields on the current user's profile."""
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active session.",
        )

    memory_agent = request.app.state.memory_agent
    existing = await memory_agent.get_profile(username)

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Visit /api/profile/start first.",
        )

    # Merge updates into the existing profile (ignore unknown fields)
    try:
        updated_data = existing.model_dump()
        # Only allow valid UserProfile fields — discard anything else
        valid_fields = set(UserProfile.model_fields.keys())
        for key, value in updates.items():
            if key in valid_fields and key != "user_id":  # user_id is immutable
                updated_data[key] = value
        updated_profile = UserProfile(**updated_data)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid profile data: {exc}",
        ) from exc

    await memory_agent.save_profile(updated_profile)
    return updated_profile
