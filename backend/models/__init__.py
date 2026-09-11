"""
backend/models/__init__.py
--------------------------
Re-exports all models for convenient imports throughout the backend.
"""

from .user import UserProfile, FitnessLevel, FitnessGoal
from .chat import ChatMessage, ChatRequest, ChatResponse, MessageRole, ResponseType
from .workout import WorkoutPlan, WorkoutSection, Exercise

__all__ = [
    "UserProfile",
    "FitnessLevel",
    "FitnessGoal",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "MessageRole",
    "ResponseType",
    "WorkoutPlan",
    "WorkoutSection",
    "Exercise",
]
