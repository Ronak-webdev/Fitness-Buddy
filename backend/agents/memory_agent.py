"""
MemoryAgent — manages all persistence via Db2Client.

This is the ONLY agent allowed to call Db2Client directly.
All other agents interact with chat history and profiles through this agent.
"""
import logging
from datetime import date
from typing import Optional

from backend.agents.base_agent import BaseAgent
from backend.db.db2_client import Db2Client
from backend.models.user import UserProfile
from backend.models.chat import ChatMessage, MessageRole

logger = logging.getLogger(__name__)


class MemoryAgent(BaseAgent):
    """
    Handles all read/write operations to IBM Db2 on Cloud.
    Acts as the single source of truth for user data and history.
    """

    def __init__(self, db_client: Db2Client) -> None:
        self.db = db_client

    async def run(
        self,
        user_message: str,
        user_profile: UserProfile,
        chat_history: list[ChatMessage],
    ) -> dict:
        """
        MemoryAgent does not generate responses — it's a utility agent.
        This method satisfies the BaseAgent contract but is not called by Orchestrator.
        """
        return {"type": "text", "message": "", "data": None}

    # ------------------------------------------------------------------
    # Profile operations
    # ------------------------------------------------------------------

    async def save_profile(self, profile: UserProfile) -> bool:
        return await self.db.save_profile(profile)

    async def get_profile(self, user_id: str) -> Optional[UserProfile]:
        return await self.db.get_profile(user_id)

    # ------------------------------------------------------------------
    # Chat history operations
    # ------------------------------------------------------------------

    async def save_message(self, user_id: str, message: ChatMessage) -> bool:
        return await self.db.save_message(user_id, message)

    async def get_history(self, user_id: str, limit: int = 5) -> list[ChatMessage]:
        return await self.db.get_history(user_id, limit)

    # ------------------------------------------------------------------
    # Daily log operations
    # ------------------------------------------------------------------

    async def log_workout(self, user_id: str) -> bool:
        """Mark today as a workout day for streak tracking."""
        return await self.db.save_daily_log(
            user_id=user_id,
            log_date=date.today(),
            workout_done=True,
        )

    async def get_streak(self, user_id: str) -> int:
        return await self.db.get_streak(user_id)
