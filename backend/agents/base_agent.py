"""
backend/agents/base_agent.py
----------------------------
Abstract base class that all specialized agents inherit.

Enforces the contract described in AGENTS.md:
  run(user_message, user_profile, chat_history) -> dict

Every concrete agent must implement `run()`.
The return dict must contain at minimum:
  {
    "type":    ResponseType value (str),
    "message": str (plain-text summary or fallback),
    "data":    dict | None  (structured payload for the frontend card)
  }
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from models.chat import ChatMessage, ResponseType
from models.user import UserProfile


class BaseAgent(ABC):
    """Abstract agent — implement `run()` in every subclass."""

    # Subclasses declare which ResponseType they produce
    response_type: ResponseType = ResponseType.TEXT

    @abstractmethod
    def run(
        self,
        user_message: str,
        user_profile: UserProfile,
        chat_history: List[ChatMessage],
    ) -> dict:
        """
        Process a user message and return a response dict.

        Parameters
        ----------
        user_message:   Raw text from the user.
        user_profile:   Full profile loaded from Db2 via MemoryAgent.
        chat_history:   Last N chat turns (N = settings.chat_history_window).

        Returns
        -------
        dict with keys:
            type    (str)         — maps to ResponseType enum value
            message (str)         — human-readable text
            data    (dict | None) — structured payload (WorkoutPlan, etc.)
        """
        ...
