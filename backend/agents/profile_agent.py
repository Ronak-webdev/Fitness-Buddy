"""
ProfileAgent — handles user onboarding and profile management.

Guides new users through a short intake conversation and builds
their UserProfile via a structured JSON extraction from Granite.

Temperature: 0.2 (structured extraction).
"""
import json
import logging
from typing import Optional

from backend.agents.base_agent import BaseAgent
from backend.llm.granite_client import GraniteClient
from backend.models.user import UserProfile, FitnessLevel, FitnessGoal
from backend.models.chat import ChatMessage

logger = logging.getLogger(__name__)

# Keyword triggers for profile/setup intent
PROFILE_KEYWORDS = [
    "name", "weight", "height", "age", "goal", "level", "beginner",
    "intermediate", "advanced", "vegetarian", "vegan", "update profile",
    "my info", "about me", "equipment", "health condition",
]

# The onboarding greeting shown to brand-new users
ONBOARDING_GREETING = (
    "👋 Welcome to **Fitness Buddy**! I'm your personal AI wellness coach.\n\n"
    "To give you the best personalised workouts and meal suggestions, "
    "I need to learn a little about you. Let's set up your profile!\n\n"
    "Please tell me:\n"
    "1. Your **name**\n"
    "2. Your **age**\n"
    "3. Your **weight** (kg) and **height** (cm)\n"
    "4. Your **fitness goal** (weight loss / muscle gain / general fitness / maintenance)\n"
    "5. Your current **fitness level** (beginner / intermediate / advanced)\n"
    "6. Any **dietary preference** (vegetarian / vegan / non-vegetarian)\n"
    "7. Any **equipment** you have at home (e.g. yoga mat, dumbbells — or none)\n\n"
    "You can answer in a single message or we can go step by step — your choice! 🏋️"
)


class ProfileAgent(BaseAgent):
    """Handles user onboarding and profile updates."""

    def __init__(
        self,
        granite_client: GraniteClient,
        memory_agent: Optional[object] = None,
    ) -> None:
        self.llm = granite_client
        self.memory_agent = memory_agent

    async def run(
        self,
        user_message: str,
        user_profile: Optional[UserProfile],
        chat_history: list[ChatMessage],
    ) -> dict:
        """
        If user_profile is None (new user), return the onboarding greeting.
        If user_profile exists and user wants to update, extract and return updated profile.

        Returns:
            {
                "type": "text",
                "message": str,
                "data": { "profile": UserProfile.model_dump() } | None
            }
        """
        # New user — show onboarding prompt
        if user_profile is None:
            return {
                "type": "text",
                "message": ONBOARDING_GREETING,
                "data": None,
            }

        # Existing user updating their profile
        prompt = self._build_extraction_prompt(user_message, user_profile)
        raw = await self.llm.generate(prompt=prompt, temperature=0.2, max_new_tokens=400)

        updated = self._parse_profile_update(raw, user_profile)
        if updated:
            return {
                "type": "text",
                "message": f"✅ Got it, {updated.name}! Your profile has been updated.",
                "data": {"profile": updated.model_dump()},
            }

        return {
            "type": "text",
            "message": "I couldn't parse that update. Could you please try again with clearer values?",
            "data": None,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_extraction_prompt(
        self, user_message: str, current: UserProfile
    ) -> str:
        return f"""Current user profile:
{current.model_dump_json(indent=2)}

User update message: {user_message}

Extract any profile fields the user wants to update and return ONLY a JSON object
with the updated fields. Use these exact field names:
name, age, fitness_level (beginner/intermediate/advanced),
primary_goal (lose_weight/build_muscle/improve_endurance/stay_active/general_health),
dietary_restrictions, equipment (list).

Only include fields that the user explicitly mentioned. Return valid JSON only."""

    def _parse_profile_update(
        self, raw: str, current: UserProfile
    ) -> Optional[UserProfile]:
        """Merge extracted fields into the current profile. Returns None on failure."""
        try:
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]

            updates = json.loads(cleaned)
            current_data = current.model_dump()
            current_data.update(updates)

            # Re-validate enums
            if isinstance(current_data.get("fitness_level"), str):
                current_data["fitness_level"] = FitnessLevel(current_data["fitness_level"])
            if isinstance(current_data.get("primary_goal"), str):
                current_data["primary_goal"] = FitnessGoal(current_data["primary_goal"])

            return UserProfile(**current_data)
        except Exception as exc:
            logger.warning("ProfileAgent: failed to parse update: %s", exc)
            return None
