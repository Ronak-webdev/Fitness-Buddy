"""
MotivationAgent — generates personalised motivational messages using IBM Granite.

Draws on user profile (name, goal, streak) and chat context to make messages
feel personal and relevant, not generic.

Temperature: 0.7 (creative, warm text).
"""
import logging

from backend.agents.base_agent import BaseAgent
from backend.llm.granite_client import GraniteClient
from backend.models.user import UserProfile
from backend.models.chat import ChatMessage

logger = logging.getLogger(__name__)

# Keyword triggers for motivation intent
MOTIVATION_KEYWORDS = [
    "motivat", "inspire", "lazy", "tired", "give up", "quit", "help",
    "encourage", "habit", "consistency", "cheer", "support", "mood",
    "down", "unmotivat", "tip", "daily",
]


class MotivationAgent(BaseAgent):
    """Generates personalised motivational tips and daily inspiration."""

    def __init__(self, granite_client: GraniteClient) -> None:
        self.llm = granite_client

    async def run(
        self,
        user_message: str,
        user_profile: UserProfile,
        chat_history: list[ChatMessage],
        streak: int = 0,
    ) -> dict:
        """
        Returns:
            {
                "type": "motivation",
                "message": str,    # The motivational message
                "data": {
                    "streak": int,
                    "badge": str | None
                }
            }
        """
        prompt = self._build_prompt(user_message, user_profile, chat_history, streak)
        message = await self.llm.generate(prompt=prompt, temperature=0.7, max_new_tokens=250)

        badge = self._get_streak_badge(streak)

        return {
            "type": "motivation",
            "message": message.strip(),
            "data": {
                "streak": streak,
                "badge": badge,
            },
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_prompt(
        self,
        user_message: str,
        profile: UserProfile,
        history: list[ChatMessage],
        streak: int,
    ) -> str:
        name = profile.name or "Champion"
        goal_map = {
            "weight_loss": "lose weight",
            "muscle_gain": "build muscle",
            "maintenance": "maintain fitness",
            "general_fitness": "improve overall fitness",
            "flexibility": "improve flexibility",
        }
        goal_text = goal_map.get(profile.primary_goal.value, "achieve your fitness goals")

        streak_text = ""
        if streak > 0:
            streak_text = f"They have been active for {streak} consecutive day(s). Acknowledge this achievement."
        elif streak == 0:
            streak_text = "They are just getting started or getting back on track."

        history_text = ""
        if history:
            history_text = "\n".join(
                f"{m.role.capitalize()}: {m.content}" for m in history[-2:]
            )

        return f"""User name: {name}
User goal: {goal_text}
{streak_text}
User message: {user_message}

Recent conversation:
{history_text}

Write a short, personalised motivational message (3-5 sentences) for {name}.
Be warm, direct, and energetic. Address them by name at least once.
Connect the encouragement to their specific goal ({goal_text}).
Do not use generic phrases like "You've got this" alone — be specific and creative.
End with one concrete, actionable tip they can do today."""

    def _get_streak_badge(self, streak: int) -> str | None:
        """Return an emoji badge based on the workout streak."""
        if streak >= 30:
            return "🏆 30-Day Legend"
        elif streak >= 14:
            return "🥇 2-Week Warrior"
        elif streak >= 7:
            return "🔥 Week Streak"
        elif streak >= 3:
            return "⚡ 3-Day Streak"
        elif streak >= 1:
            return "🌱 Getting Started"
        return None
