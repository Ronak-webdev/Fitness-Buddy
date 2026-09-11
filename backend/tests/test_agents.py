"""
Unit tests for individual agents.
Uses mock GraniteClient and mock Db2Client from conftest.
"""
import pytest
from unittest.mock import patch, AsyncMock
from backend.agents.workout_agent import WorkoutAgent
from backend.agents.nutrition_agent import NutritionAgent
from backend.agents.motivation_agent import MotivationAgent
from backend.agents.orchestrator import OrchestratorAgent, Intent


class TestOrchestratorAgent:

    def test_classify_workout_intent(self, mock_granite_client):
        """Orchestrator should classify workout-related messages correctly."""
        agent = OrchestratorAgent(granite_client=mock_granite_client)
        # keyword-based classification (no LLM needed)
        intent = agent._classify_by_keywords("I want a workout for today")
        assert intent == Intent.WORKOUT

    def test_classify_meal_intent(self, mock_granite_client):
        intent = agent_classify = OrchestratorAgent(granite_client=mock_granite_client)
        intent = agent_classify._classify_by_keywords("what should I eat for breakfast")
        assert intent == Intent.NUTRITION

    def test_classify_motivation_intent(self, mock_granite_client):
        agent = OrchestratorAgent(granite_client=mock_granite_client)
        intent = agent._classify_by_keywords("I feel lazy today, motivate me")
        assert intent == Intent.MOTIVATION

    def test_classify_profile_intent(self, mock_granite_client):
        agent = OrchestratorAgent(granite_client=mock_granite_client)
        intent = agent._classify_by_keywords("update my weight to 65kg")
        assert intent == Intent.PROFILE


class TestWorkoutAgent:

    @pytest.mark.asyncio
    async def test_run_returns_correct_type(self, sample_profile, sample_chat_history, mock_granite_client):
        """WorkoutAgent.run() must return dict with type='workout'."""
        mock_granite_client.generate = AsyncMock(return_value=(
            '{"title": "Beginner Home Workout", "sections": [], "duration_min": 20, "notes": "Great for beginners"}'
        ))
        agent = WorkoutAgent(granite_client=mock_granite_client)
        result = await agent.run(
            user_message="Give me a beginner workout",
            user_profile=sample_profile,
            chat_history=sample_chat_history,
        )
        assert result["type"] == "workout"
        assert "message" in result

    @pytest.mark.asyncio
    async def test_run_returns_fallback_on_parse_error(self, sample_profile, sample_chat_history, mock_granite_client):
        """WorkoutAgent must return a text fallback if Granite returns non-JSON."""
        mock_granite_client.generate = AsyncMock(return_value="Here is your workout: do 10 pushups.")
        agent = WorkoutAgent(granite_client=mock_granite_client)
        result = await agent.run(
            user_message="Give me a workout",
            user_profile=sample_profile,
            chat_history=sample_chat_history,
        )
        # Must not raise — should degrade gracefully
        assert result["type"] in ("workout", "text")
        assert "message" in result


class TestNutritionAgent:

    @pytest.mark.asyncio
    async def test_run_returns_meal_type(self, sample_profile, sample_chat_history, mock_granite_client):
        """NutritionAgent.run() must return dict with type='meal'."""
        mock_granite_client.generate = AsyncMock(return_value="Meal suggestion: Rajma Rice with salad.")
        agent = NutritionAgent(granite_client=mock_granite_client)
        result = await agent.run(
            user_message="What should I eat for lunch?",
            user_profile=sample_profile,
            chat_history=sample_chat_history,
        )
        assert result["type"] == "meal"
        assert "message" in result


class TestMotivationAgent:

    @pytest.mark.asyncio
    async def test_run_returns_motivation_type(self, sample_profile, sample_chat_history, mock_granite_client):
        """MotivationAgent.run() must return dict with type='motivation'."""
        mock_granite_client.generate = AsyncMock(return_value="You are doing amazing! Keep pushing forward!")
        agent = MotivationAgent(granite_client=mock_granite_client)
        result = await agent.run(
            user_message="I feel unmotivated",
            user_profile=sample_profile,
            chat_history=sample_chat_history,
        )
        assert result["type"] == "motivation"
        assert "message" in result
        assert len(result["message"]) > 0
