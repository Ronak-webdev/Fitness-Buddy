"""
NutritionAgent — suggests personalised meal ideas using IBM Granite
and the static meals.json catalogue loaded at startup.

Temperature: 0.2 (structured output with meal recommendations).
"""
import json
import logging
import random
from pathlib import Path
from typing import Optional

from backend.agents.base_agent import BaseAgent
from backend.llm.granite_client import GraniteClient
from backend.models.user import UserProfile
from backend.models.chat import ChatMessage

logger = logging.getLogger(__name__)

# Keyword triggers for nutrition intent
NUTRITION_KEYWORDS = [
    "eat", "meal", "food", "diet", "nutrition", "breakfast", "lunch",
    "dinner", "snack", "recipe", "calories", "protein", "carb", "fat",
    "vegetarian", "vegan", "weight loss", "muscle", "healthy eating",
]

# Load meals catalogue once at module import (not per-request)
_MEALS_FILE = Path(__file__).parent.parent / "data" / "meals.json"
try:
    with open(_MEALS_FILE, "r", encoding="utf-8") as f:
        _MEALS_CATALOGUE: list[dict] = json.load(f)
    logger.info("NutritionAgent: loaded %d meals from catalogue.", len(_MEALS_CATALOGUE))
except FileNotFoundError:
    _MEALS_CATALOGUE = []
    logger.warning("NutritionAgent: meals.json not found — catalogue is empty.")


class NutritionAgent(BaseAgent):
    """Recommends personalised meals from the catalogue and adds coaching tips."""

    def __init__(self, granite_client: GraniteClient) -> None:
        self.llm = granite_client

    async def run(
        self,
        user_message: str,
        user_profile: UserProfile,
        chat_history: list[ChatMessage],
    ) -> dict:
        """
        Returns:
            {
                "type": "meal",
                "message": str,        # Granite coaching tip
                "data": {
                    "meals": [list of meal dicts],
                    "daily_calories": int,
                    "tip": str,
                }
            }
        """
        # Pick relevant meals from catalogue
        suitable_meals = self._select_meals(user_message, user_profile)

        # Ask Granite for a personalised coaching tip about these meals
        prompt = self._build_prompt(user_message, user_profile, suitable_meals, chat_history)
        coaching_tip = await self.llm.generate(prompt=prompt, temperature=0.2, max_new_tokens=300)

        # Calculate estimated daily calories
        daily_calories = self._estimate_daily_calories(user_profile)

        return {
            "type": "meal",
            "message": coaching_tip.strip(),
            "data": {
                "meals": suitable_meals,
                "daily_calories": daily_calories,
                "tip": coaching_tip.strip(),
            },
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _select_meals(self, user_message: str, profile: UserProfile) -> list[dict]:
        """
        Filter and return up to 3 meals matching:
        - User's goal (suitable_for field)
        - Dietary preference (vegetarian filter)
        - Requested meal time if mentioned in user_message
        """
        goal = profile.primary_goal.value  # e.g. "lose_weight"
        # Map user FitnessGoal to meals.json suitable_for tags
        goal_map = {
            "lose_weight": "weight_loss",
            "build_muscle": "muscle_gain",
            "improve_endurance": "general_fitness",
            "stay_active": "general_fitness",
            "general_health": "general_fitness",
        }
        target_goal = goal_map.get(goal, goal)


        is_vegetarian = profile.dietary_restrictions.lower() in ("vegetarian", "vegan")
        msg_lower = user_message.lower()

        # Determine desired category from message
        category_filter: Optional[str] = None
        for cat in ("breakfast", "lunch", "dinner", "snack"):
            if cat in msg_lower:
                category_filter = cat
                break

        candidates = []
        for meal in _MEALS_CATALOGUE:
            suitable = meal.get("suitable_for", [])
            if target_goal not in suitable and goal not in suitable and "maintenance" not in suitable:
                continue
            if is_vegetarian and any(
                m in meal.get("ingredients", [])
                for m in ("chicken", "tuna", "salmon", "turkey", "turkey mince")
            ):
                continue
            if category_filter and meal.get("category") != category_filter:
                continue
            candidates.append(meal)

        # If no candidates match filters, fall back to any suitable meal or all catalogue
        if not candidates:
            candidates = [
                m for m in _MEALS_CATALOGUE
                if target_goal in m.get("suitable_for", []) or "maintenance" in m.get("suitable_for", [])
            ] or _MEALS_CATALOGUE

        # Return up to 3 random selections for variety
        return random.sample(candidates, min(3, len(candidates))) if candidates else []


    def _build_prompt(
        self,
        user_message: str,
        profile: UserProfile,
        meals: list[dict],
        history: list[ChatMessage],
    ) -> str:
        meal_names = ", ".join(m["name"] for m in meals) if meals else "healthy home-cooked meals"
        history_text = "\n".join(
            f"{m.role.capitalize()}: {m.content}" for m in history[-2:]
        ) if history else ""

        return f"""User message: {user_message}

User profile:
- Goal: {profile.primary_goal.value}
- Dietary restrictions: {profile.dietary_restrictions}

Suggested meals: {meal_names}

Recent conversation:
{history_text}

Write a short, friendly 2-3 sentence coaching tip about why these meals are good for the user's goal.
Be specific, practical, and encouraging. Do not repeat the meal names in full."""

    def _estimate_daily_calories(self, profile: UserProfile) -> int:
        """
        Rough TDEE estimate using Mifflin-St Jeor BMR × activity multiplier.
        Returns a round number for display purposes.
        """
        # Since weight and height are no longer collected, use a generic baseline BMR
        bmr = 1600

        multipliers = {
            "beginner": 1.375,     # lightly active
            "intermediate": 1.55,  # moderately active
            "advanced": 1.725,     # very active
        }
        multiplier = multipliers.get(profile.fitness_level.value, 1.375)
        tdee = bmr * multiplier

        # Adjust for goal
        if profile.primary_goal.value == "lose_weight":
            tdee -= 300  # caloric deficit
        elif profile.primary_goal.value == "build_muscle":
            tdee += 200  # caloric surplus

        return max(1200, round(tdee / 50) * 50)  # Round to nearest 50, min 1200
