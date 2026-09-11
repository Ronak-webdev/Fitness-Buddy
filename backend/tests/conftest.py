"""
Test configuration and shared fixtures for FitnessBuddy backend tests.
Uses SQLite as a test double for Db2 (Db2 not available in CI).
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from backend.models.user import UserProfile, FitnessLevel, FitnessGoal
from backend.models.chat import ChatMessage, MessageRole


@pytest.fixture
def sample_profile() -> UserProfile:
    """A standard user profile for use across all tests."""
    return UserProfile(
        user_id="test-user-001",
        name="Priya",
        age=22,
        fitness_level=FitnessLevel.BEGINNER,
        primary_goal=FitnessGoal.LOSE_WEIGHT,
        equipment="yoga_mat",
        dietary_restrictions="vegetarian",
        current_streak=0,
        onboarding_complete=True,
    )


@pytest.fixture
def sample_chat_history() -> list[ChatMessage]:
    """A short 2-turn chat history."""
    return [
        ChatMessage(user_id="test-user-001", role=MessageRole.USER, content="Hello"),
        ChatMessage(user_id="test-user-001", role=MessageRole.ASSISTANT, content="Hi! I'm your Fitness Buddy."),
    ]


@pytest.fixture
def mock_granite_client():
    """Mock GraniteClient that returns a preset response."""
    client = MagicMock()
    client.generate = AsyncMock(return_value="Mocked Granite response.")
    client.token_usage = 0
    return client


@pytest.fixture
def mock_db_client():
    """Mock Db2Client with no-op async methods."""
    client = MagicMock()
    client.save_profile = AsyncMock(return_value=True)
    client.get_profile = AsyncMock(return_value=None)
    client.save_message = AsyncMock(return_value=True)
    client.get_history = AsyncMock(return_value=[])
    client.save_daily_log = AsyncMock(return_value=True)
    return client
