"""
Unit tests for GraniteClient.
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from backend.llm.granite_client import GraniteClient


class TestGraniteClient:

    def test_init_sets_model_id(self):
        """GraniteClient must store the model_id from config."""
        with patch("backend.llm.granite_client.settings") as mock_settings:
            mock_settings.WATSONX_MODEL_ID = "ibm/granite-13b-instruct-v2"
            mock_settings.WATSONX_API_KEY = "fake-key"
            mock_settings.WATSONX_PROJECT_ID = "fake-project"
            mock_settings.WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
            client = GraniteClient()
            assert client.model_id == "ibm/granite-13b-instruct-v2"

    @pytest.mark.asyncio
    async def test_generate_returns_string(self):
        """generate() must always return a non-empty string."""
        with patch("backend.llm.granite_client.settings") as mock_settings:
            mock_settings.WATSONX_MODEL_ID = "ibm/granite-13b-instruct-v2"
            mock_settings.WATSONX_API_KEY = "fake-key"
            mock_settings.WATSONX_PROJECT_ID = "fake-project"
            mock_settings.WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
            client = GraniteClient()
            # Patch the internal IBM SDK call
            with patch.object(client, "_call_watsonx", new_callable=AsyncMock) as mock_call:
                mock_call.return_value = "Generated workout plan."
                result = await client.generate(
                    prompt="Create a workout plan",
                    temperature=0.2,
                    max_new_tokens=500,
                )
                assert isinstance(result, str)
                assert len(result) > 0

    @pytest.mark.asyncio
    async def test_generate_tracks_token_usage(self):
        """generate() must increment token_usage after each call."""
        with patch("backend.llm.granite_client.settings") as mock_settings:
            mock_settings.WATSONX_MODEL_ID = "ibm/granite-13b-instruct-v2"
            mock_settings.WATSONX_API_KEY = "fake-key"
            mock_settings.WATSONX_PROJECT_ID = "fake-project"
            mock_settings.WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
            client = GraniteClient()
            
            with patch.object(client._http_client, "post", new_callable=AsyncMock) as mock_post:
                client._iam_token = "fake-token"
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "results": [{
                        "generated_token_count": 10,
                        "input_token_count": 5,
                        "generated_text": "Some response"
                    }]
                }
                mock_post.return_value = mock_response
                
                assert client.token_usage == 0
                await client.generate("test prompt", temperature=0.7)
                assert client.token_usage == 15

    @pytest.mark.asyncio
    async def test_generate_raises_on_empty_response(self):
        """generate() must raise ValueError if Granite returns empty string."""
        with patch("backend.llm.granite_client.settings") as mock_settings:
            mock_settings.WATSONX_MODEL_ID = "ibm/granite-13b-instruct-v2"
            mock_settings.WATSONX_API_KEY = "fake-key"
            mock_settings.WATSONX_PROJECT_ID = "fake-project"
            mock_settings.WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
            client = GraniteClient()
            with patch.object(client, "_call_watsonx", new_callable=AsyncMock) as mock_call:
                mock_call.return_value = ""
                with pytest.raises(ValueError, match="empty"):
                    await client.generate("test prompt", temperature=0.2)
