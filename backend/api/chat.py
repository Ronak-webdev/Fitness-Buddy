"""
backend/api/chat.py
-------------------
POST /api/chat — main conversational endpoint.

Request flow:
  1. Read username from session cookie
  2. Load UserProfile + recent history from MemoryAgent
  3. Call OrchestratorAgent.run()
  4. Persist both user message and assistant response via MemoryAgent
  5. Return ChatResponse
"""

import logging
from typing import Optional

from fastapi import APIRouter, Cookie, HTTPException, Request, status

from models.chat import ChatMessage, ChatRequest, ChatResponse, MessageRole, ResponseType

router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def post_chat(
    body: ChatRequest,
    request: Request,
    username: Optional[str] = Cookie(default=None),
) -> ChatResponse:
    """
    Send a message to the Fitness Buddy AI coach.

    The response `type` field tells the frontend which card component to render:
      - "text"       → plain message bubble
      - "workout"    → WorkoutCard with structured exercise plan
      - "meal"       → MealCard with meal suggestions
      - "motivation" → styled motivation bubble with streak info
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session cookie 'username' is required. Visit /api/profile/start first.",
        )

    orchestrator = request.app.state.orchestrator
    memory_agent = request.app.state.memory_agent

    # ------------------------------------------------------------------
    # 1. Load user context from Db2
    # ------------------------------------------------------------------
    user_profile = await memory_agent.get_profile(username)
    chat_history = await memory_agent.get_history(username)

    # ------------------------------------------------------------------
    # 2. Persist the incoming user message
    # ------------------------------------------------------------------
    user_msg = ChatMessage(
        user_id=username,
        role=MessageRole.USER,
        content=body.message,
    )
    await memory_agent.save_message(username, user_msg)

    # ------------------------------------------------------------------
    # 3. Route through OrchestratorAgent
    # ------------------------------------------------------------------
    try:
        result = await orchestrator.run(
            user_message=body.message,
            user_profile=user_profile,
            chat_history=chat_history,
        )
    except Exception as exc:
        logger.exception("OrchestratorAgent failed for user=%s: %s", username, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The AI coach encountered an error. Please try again.",
        ) from exc

    # ------------------------------------------------------------------
    # 4. Persist the assistant response
    # ------------------------------------------------------------------
    resp_type = ResponseType(result.get("type", "text"))
    assistant_msg = ChatMessage(
        user_id=username,
        role=MessageRole.ASSISTANT,
        content=result.get("message", ""),
        type=resp_type,
        data=result.get("data"),
    )
    await memory_agent.save_message(username, assistant_msg)

    # If a workout was returned, log it for streak tracking
    if resp_type == ResponseType.WORKOUT:
        await memory_agent.log_workout(username)

    # ------------------------------------------------------------------
    # 5. Return the response envelope
    # ------------------------------------------------------------------
    return ChatResponse(
        type=resp_type,
        message=result.get("message", ""),
        data=result.get("data"),
    )
