"""
backend/models/workout.py
-------------------------
WorkoutPlan — the structured output from the Workout Agent.

Granite is prompted to return JSON conforming to this shape.
The `data` field of ChatResponse is populated with WorkoutPlan.model_dump().
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class Exercise(BaseModel):
    name: str
    sets: Optional[int] = None
    reps: Optional[str] = None          # e.g. "10-12" or "30 seconds"
    description: str = ""
    muscles_targeted: str = ""


class WorkoutSection(BaseModel):
    """One phase of a workout (warm-up, main, cooldown)."""
    section: str                         # "Warm-up", "Main Workout", "Cooldown"
    duration_minutes: int
    exercises: List[Exercise]


class WorkoutPlan(BaseModel):
    """
    Full structured workout plan returned by WorkoutAgent.
    Serialised into ChatResponse.data for the frontend WorkoutCard component.
    """

    title: str = Field(..., description="e.g. '20-Minute Beginner Full-Body Workout'")
    total_duration_minutes: int
    difficulty: str = "beginner"         # beginner / intermediate / advanced
    equipment_needed: str = "None (bodyweight)"
    sections: List[WorkoutSection]
    notes: str = ""                      # coach's tip or safety reminder
