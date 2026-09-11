"""
backend/models/user.py
----------------------
UserProfile — the central data object passed to every agent.

Fields reflect the 5 onboarding questions asked by the Profile Agent:
  1. Age
  2. Fitness level
  3. Primary goal
  4. Available equipment
  5. Dietary restrictions
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class FitnessLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class FitnessGoal(str, Enum):
    LOSE_WEIGHT = "lose_weight"
    BUILD_MUSCLE = "build_muscle"
    IMPROVE_ENDURANCE = "improve_endurance"
    STAY_ACTIVE = "stay_active"
    GENERAL_HEALTH = "general_health"


class UserProfile(BaseModel):
    """
    Persisted in the `users` Db2 table.
    Passed as context to every agent call.
    """

    user_id: str = Field(..., description="Unique identifier (username from cookie)")
    name: str = Field(default="Friend", description="Display name")
    age: Optional[int] = Field(default=None, ge=10, le=100)
    fitness_level: FitnessLevel = FitnessLevel.BEGINNER
    primary_goal: FitnessGoal = FitnessGoal.GENERAL_HEALTH
    # Comma-separated: "dumbbells, resistance bands" — empty means bodyweight only
    equipment: str = Field(default="", description="Available home equipment")
    # Comma-separated: "vegetarian", "vegan", "no dairy", etc.
    dietary_restrictions: str = Field(default="", description="Dietary restrictions")
    # Streak counter — incremented by MotivationAgent each day
    current_streak: int = Field(default=0, ge=0)
    # Whether the onboarding flow has been completed
    onboarding_complete: bool = False

    def is_new_user(self) -> bool:
        return not self.onboarding_complete

    def equipment_list(self) -> List[str]:
        if not self.equipment:
            return []
        return [e.strip() for e in self.equipment.split(",") if e.strip()]

    def dietary_list(self) -> List[str]:
        if not self.dietary_restrictions:
            return []
        return [d.strip() for d in self.dietary_restrictions.split(",") if d.strip()]
