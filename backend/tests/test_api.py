"""
Integration tests for the FastAPI endpoints.
Uses TestClient (sync) and mocks all external dependencies via app.state.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from backend.main import app

def setup_mock_state():
    app.state.orchestrator = MagicMock()
    app.state.memory_agent = MagicMock()

class TestChatEndpoint:

    def test_chat_returns_200(self):
        """POST /api/chat must return 200 with correct envelope."""
        setup_mock_state()
        app.state.orchestrator.run = AsyncMock(return_value={
            "type": "text",
            "message": "Hello! I am your Fitness Buddy.",
            "data": None,
        })
        app.state.memory_agent.get_profile = AsyncMock(return_value=MagicMock())
        app.state.memory_agent.get_history = AsyncMock(return_value=[])
        app.state.memory_agent.save_message = AsyncMock(return_value=True)

        client = TestClient(app)
        # Mock the session cookie
        client.cookies.set("username", "test-001")
        response = client.post("/api/chat", json={
            "message": "Hello",
        })
        assert response.status_code == 200
        body = response.json()
        assert body["type"] in ("text", "workout", "meal", "motivation")
        assert "message" in body

    def test_chat_requires_session(self):
        """POST /api/chat must return 401 if 'username' cookie is missing."""
        setup_mock_state()
        client = TestClient(app)
        response = client.post("/api/chat", json={"message": "Hello"})
        assert response.status_code == 401


class TestProfileEndpoint:

    def test_get_profile_returns_404_for_unknown_user(self):
        """GET /api/profile must return 404 for unknown user in session."""
        setup_mock_state()
        app.state.memory_agent.get_profile = AsyncMock(return_value=None)
        
        client = TestClient(app)
        client.cookies.set("username", "unknown-user-999")
        response = client.get("/api/profile")
        assert response.status_code == 404

    def test_start_session_creates_user(self):
        """POST /api/profile/start must return 200 and set cookie."""
        setup_mock_state()
        app.state.memory_agent.get_profile = AsyncMock(return_value=None)
        app.state.memory_agent.save_profile = AsyncMock(return_value=True)
        
        client = TestClient(app)
        response = client.post("/api/profile/start?username=Arjun")
        assert response.status_code == 200
        assert response.json()["is_new_user"] is True
        assert "username" in client.cookies


class TestHealthEndpoint:

    def test_health_check(self):
        """GET /health must return 200 with status ok."""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
