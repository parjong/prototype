from unittest.mock import AsyncMock, patch

import pytest

from octopith.engine.inference import OllamaAdapter


@pytest.mark.asyncio
async def test_ollama_chat():
    with patch("ollama.AsyncClient") as MockClient:
        mock_client = MockClient.return_value
        mock_client.chat = AsyncMock(return_value={"message": {"content": "Hello! I am an AI."}})

        adapter = OllamaAdapter(model_name="qwen2.5:3b")
        messages = [{"role": "user", "content": "Hi"}]
        response = await adapter.chat(messages)

        assert response == "Hello! I am an AI."
        mock_client.chat.assert_called_once_with(model="qwen2.5:3b", messages=messages, options={})


@pytest.mark.asyncio
async def test_ollama_embed():
    with patch("ollama.AsyncClient") as MockClient:
        mock_client = MockClient.return_value
        mock_client.embed = AsyncMock(return_value={"embeddings": [[0.1, 0.2, 0.3]]})

        adapter = OllamaAdapter(model_name="nomic-embed-text")
        embedding = await adapter.embed("test text")

        assert embedding == [0.1, 0.2, 0.3]
        mock_client.embed.assert_called_once_with(model="nomic-embed-text", input="test text")
