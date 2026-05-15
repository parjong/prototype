from unittest.mock import AsyncMock, MagicMock

import pytest

from octopith.db.store import Store
from octopith.engine.sync import SyncEngine


@pytest.fixture
def mock_store():
    store = MagicMock(spec=Store)
    return store


@pytest.fixture
def mock_gh_client():
    client = MagicMock()
    client.execute = AsyncMock()
    client.build_search_query.return_value = "repo:owner/repo is:issue"
    return client


@pytest.mark.asyncio
async def test_sync_repository_new_repo(mock_store, mock_gh_client):
    # Setup
    mock_store.get_repository_by_name.return_value = None
    mock_gh_client.execute.side_effect = [
        # Fetch repo info
        {
            "repository": {
                "id": "repo_123",
                "url": "https://url",
                "createdAt": "2020-01-01T00:00:00Z",
            }
        },
        # Incremental sync (empty)
        {"search": {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}},
        # Backfill sync (1 issue)
        {
            "search": {
                "nodes": [
                    {
                        "id": "issue_1",
                        "title": "Test Issue",
                        "body": "Body",
                        "updatedAt": "2024-05-15T00:00:00Z",
                        "createdAt": "2024-05-15T00:00:00Z",
                        "author": {"login": "user1"},
                        "comments": {"nodes": []},
                    }
                ],
                "pageInfo": {"hasNextPage": False, "endCursor": None},
            }
        },
    ]

    engine = SyncEngine(mock_store, mock_gh_client)
    await engine.sync_repository("https://github.com/owner/repo")

    # Assertions
    mock_store.upsert_repository.assert_called()
    mock_store.upsert_thread.assert_called()
    assert mock_store.upsert_thread.call_args[0][0].title == "Test Issue"


@pytest.mark.asyncio
async def test_save_node_with_comments(mock_store, mock_gh_client):
    engine = SyncEngine(mock_store, mock_gh_client)

    node = {
        "id": "thread_1",
        "title": "Title",
        "body": "Body",
        "updatedAt": "2024-05-15T00:00:00Z",
        "author": {"login": "author1"},
        "comments": {
            "nodes": [
                {
                    "id": "comment_1",
                    "body": "Comment Body",
                    "author": {"login": "commenter1"},
                    "createdAt": "2024-05-15T00:01:00Z",
                }
            ]
        },
    }

    engine._save_node("repo_1", node)

    # Assert thread saved
    mock_store.upsert_thread.assert_called_once()
    thread = mock_store.upsert_thread.call_args[0][0]
    assert thread.id == "thread_1"

    # Assert comment saved
    mock_store.upsert_comment.assert_called_once()
    comment = mock_store.upsert_comment.call_args[0][0]
    assert comment.id == "comment_1"
    assert comment.thread_id == "thread_1"
