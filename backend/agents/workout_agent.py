"""
WorkoutAgent — generates personalised home workout plans using IBM Granite.

Builds a structured prompt based on the user's fitness level, goal,
available equipment, and any health conditions, then parses the JSON
response into a WorkoutPlan model.

Temperature: 0.2 (structured JSON output).
"""
import json
import logging
from typing import Optional

from backend.agents.base_agent import BaseAgent
from backend.llm.granite_client import GraniteClient
from backend.models.user import UserProfile, FitnessLevel, FitnessGoal
from backend.models.chat import ChatMessage
from backend.models.workout import WorkoutPlan, WorkoutSection, Exercise

logger = logging.getLogger(__name__)

# Keywords that trigger workout intent (used by orchestrator keyword classifier)
WORKOUT_KEYWORDS = [
    "workout", "exercise", "train", "fitness", "routine", "session",
    "pushup", "squat", "plank", "cardio", "strength", "stretch", "warm",
    "cool down", "gym", "home workout", "work out",
]


class WorkoutAgent(BaseAgent):
    """Generates a personalised WorkoutPlan from a user request."""

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
                "type": "workout",
                "message": str,      # summary line
                "data": { WorkoutPlan as dict }
            }
        """
        prompt = self._build_prompt(user_message, user_profile, chat_history)
        raw = await self.llm.generate(prompt=prompt, temperature=0.2, max_new_tokens=700)

        workout_plan = self._parse_workout(raw, user_profile)
        if workout_plan:
            plan_dict = workout_plan.model_dump()
            # Frontend WorkoutCard uses `duration_minutes`; model stores `total_duration_minutes`
            plan_dict.setdefault("duration_minutes", plan_dict.get("total_duration_minutes", 0))
            return {
                "type": "workout",
                "message": f"Here is your personalised {workout_plan.title}! 💪",
                "data": plan_dict,
            }
        else:
            # Graceful degradation — return the raw text if JSON parsing failed
            logger.warning("WorkoutAgent: JSON parse failed — returning raw text.")
            return {
                "type": "text",
                "message": raw,
                "data": None,
            }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_prompt(
        self,
        user_message: str,
        profile: UserProfile,
        history: list[ChatMessage],
    ) -> str:
        equipment = profile.equipment if profile.equipment else "no equipment"

        history_text = ""
        if history:
            history_text = "\n".join(
                f"{m.role.capitalize()}: {m.content}" for m in history[-2:]
            )

        return f"""User request: {user_message}

User profile:
- Age: {profile.age}
- Goal: {profile.primary_goal.value}
- Level: {profile.fitness_level.value}
- Available equipment: {equipment}

Recent conversation:
{history_text}

Generate a home workout plan as valid JSON with this exact structure:
{{
  "title": "string",
  "duration_min": number,
  "sections": [
    {{
      "name": "string (e.g. Warm Up, Main Workout, Cool Down)",
      "exercises": [
        {{
          "name": "string",
          "sets": number,
          "reps_or_duration": "string (e.g. 10 reps or 30 sec)",
          "rest_sec": number,
          "instructions": "string (one sentence)"
        }}
      ]
    }}
  ],
  "notes": "string (1-2 sentences of encouragement)"
}}

Rules:
- All exercises must be doable at home with the equipment listed.
- Adapt intensity to the user's fitness level ({profile.fitness_level.value}).
- Total workout should be 20-30 minutes for beginner, 30-45 for intermediate, 45-60 for advanced.
- Include 3 sections: Warm Up (5 min), Main Workout, Cool Down (5 min).
- Respond ONLY with the JSON object, no other text."""

    def _parse_workout(self, raw: str, profile: UserProfile) -> Optional[WorkoutPlan]:
        """Parse Granite's JSON response into a WorkoutPlan. Returns None on failure."""
        try:
            # Strip any markdown code fences if Granite added them
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]

            data = json.loads(cleaned)
            sections = [
                WorkoutSection(
                    section=s.get("section", s.get("name", "Main Workout")),
                    duration_minutes=s.get("duration_minutes", 10),
                    exercises=[
                        Exercise(
                            name=e["name"],
                            sets=e.get("sets"),
                            reps=e.get("reps", e.get("reps_or_duration", "")),
                            description=e.get("description", e.get("instructions", "")),
                            muscles_targeted=e.get("muscles_targeted", "")
                        )
                        for e in s.get("exercises", [])
                    ],
                )
                for s in data.get("sections", [])
            ]
            return WorkoutPlan(
                title=data.get("title", "Home Workout"),
                total_duration_minutes=data.get("total_duration_minutes", data.get("duration_min", 30)),
                difficulty=data.get("difficulty", "beginner"),
                equipment_needed=data.get("equipment_needed", "None (bodyweight)"),
                sections=sections,
                notes=data.get("notes", ""),
            )
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            logger.warning("Failed to parse workout JSON: %s | Raw: %s", exc, raw[:200])
            return None
