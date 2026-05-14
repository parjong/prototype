from unittest.mock import AsyncMock, MagicMock

import pytest

from octopith.engine.summarizer import Summarizer


@pytest.mark.asyncio
async def test_summarize_thread_tldr():
    mock_adapter = MagicMock()
    mock_adapter.chat = AsyncMock(return_value="This is a TLDR.")

    summarizer = Summarizer(mock_adapter)
    title = "Test Issue"
    body = "Test Body"
    comments = [{"author": "user1", "body": "Comment 1"}]

    result = await summarizer.summarize_thread(title, body, comments, summary_type="TLDR")

    assert result == "This is a TLDR."
    mock_adapter.chat.assert_called_once()
    prompt = mock_adapter.chat.call_args[0][0][1]["content"]
    assert "TLDR" in prompt
    assert "Test Issue" in prompt


@pytest.mark.asyncio
async def test_summarize_thread_troubleshooting():
    mock_adapter = MagicMock()
    mock_adapter.chat = AsyncMock(return_value="Solution: Fix it.")

    summarizer = Summarizer(mock_adapter)
    title = "Bug Report"
    body = "It crashes."
    comments = [{"author": "dev", "body": "Fixed in v2."}]

    result = await summarizer.summarize_thread(
        title, body, comments, summary_type="TROUBLESHOOTING"
    )

    assert result == "Solution: Fix it."
    mock_adapter.chat.assert_called_once()
    prompt = mock_adapter.chat.call_args[0][0][1]["content"]
    assert "Troubleshooting" in prompt
    assert "Bug Report" in prompt
