"""
backend/models/chat.py
----------------------
ChatMessage — represents a single turn in the conversation history.

The `type` field controls which React component renders the response:
  - "text"       → plain MessageBubble
  - "workout"    → WorkoutCard
  - "meal"       → MealCard
  - "motivation" → MotivationCard (styled bubble)
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ResponseType(str, Enum):
    """Controls which React component renders the response on the frontend."""
    TEXT = "text"
    WORKOUT = "workout"
    MEAL = "meal"
    MOTIVATION = "motivation"


class ChatMessage(BaseModel):
    """
    Stored in the `chat_history` Db2 table.
    Also used as the response envelope returned by POST /api/chat.
    """

    user_id: str
    role: MessageRole
    content: str
    # Only set on assistant messages — drives frontend card rendering
    type: ResponseType = ResponseType.TEXT
    # Structured data (WorkoutPlan / MealPlan dict) — None for plain text
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(use_enum_values=True)


class ChatRequest(BaseModel):
    """Incoming request body for POST /api/chat."""
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    """
    Standard API response envelope.
    Frontend reads `type` to decide which component to render,
    then uses `data` for structured content or `message` for plain text.
    """

    type: ResponseType
    message: str
    data: Optional[Dict[str, Any]] = None
