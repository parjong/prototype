import logging
from datetime import datetime, timezone
from typing import Optional

from ..db.models import Comment, Repository, Thread
from ..db.store import Store
from .github import ISSUE_SEARCH_QUERY, GitHubClient

logger = logging.getLogger(__name__)


class SyncEngine:
    def __init__(self, store: Store, github_client: GitHubClient):
        self.store = store
        self.gh = github_client

    async def sync_repository(self, repo_url: str, duration_seconds: Optional[float] = None):
        # 1. Resolve repository info
        repo_name = repo_url.replace("https://github.com/", "").strip("/")
        repo = self.store.get_repository_by_name(repo_name)

        if not repo:
            # Need to fetch repo info first
            repo_info = await self._fetch_repo_info(repo_name)
            repo = Repository(
                id=repo_info["id"],
                api_url=repo_info["url"],
                full_name=repo_name,
                repo_created_at=repo_info["createdAt"],
            )
            self.store.upsert_repository(repo)

        start_time = datetime.now(timezone.utc)

        # 2. Incremental Sync (Newest)
        await self._sync_incremental(repo, start_time, duration_seconds)

        # 3. Backfill Sync (Oldest)
        if duration_seconds:
            elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
            remaining = duration_seconds - elapsed
            if remaining > 0:
                await self._sync_backfill(repo, start_time, remaining)
        else:
            await self._sync_backfill(repo, start_time, None)

    async def _fetch_repo_info(self, repo_name: str):
        owner, name = repo_name.split("/")
        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            id
            url
            createdAt
          }
        }
        """
        data = await self.gh.execute(query, {"owner": owner, "name": name})
        return data["repository"]

    async def _sync_incremental(
        self, repo: Repository, start_time: datetime, duration: Optional[float]
    ):
        logger.info(f"Starting incremental sync for {repo.full_name}")
        updated_after = repo.sync_newest_at
        query_string = self.gh.build_search_query(repo.full_name, updated_after=updated_after)

        cursor = None
        newest_at = repo.sync_newest_at

        while True:
            if duration and (datetime.now(timezone.utc) - start_time).total_seconds() > duration:
                logger.info("Duration reached during incremental sync")
                break

            data = await self.gh.execute(
                ISSUE_SEARCH_QUERY, {"queryString": query_string, "cursor": cursor}
            )
            search_data = data["search"]
            nodes = search_data["nodes"]

            for node in nodes:
                self._save_node(repo.id, node)
                updated_at = node["updatedAt"]
                if not newest_at or updated_at > newest_at:
                    newest_at = updated_at

            # Update sync_newest_at after each page
            if newest_at:
                repo.sync_newest_at = newest_at
                self.store.upsert_repository(repo)

            page_info = search_data["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]

    async def _sync_backfill(
        self, repo: Repository, start_time: datetime, duration: Optional[float]
    ):
        logger.info(f"Starting backfill sync for {repo.full_name}")
        updated_before = repo.sync_oldest_at or datetime.now(timezone.utc).isoformat()

        if repo.sync_oldest_at and repo.sync_oldest_at <= repo.repo_created_at:
            logger.info("Backfill already complete")
            return

        query_string = self.gh.build_search_query(repo.full_name, updated_before=updated_before)

        cursor = None
        oldest_at = repo.sync_oldest_at

        while True:
            if duration and (datetime.now(timezone.utc) - start_time).total_seconds() > duration:
                logger.info("Duration reached during backfill sync")
                break

            data = await self.gh.execute(
                ISSUE_SEARCH_QUERY, {"queryString": query_string, "cursor": cursor}
            )
            search_data = data["search"]
            nodes = search_data["nodes"]

            if not nodes:
                break

            for node in nodes:
                self._save_node(repo.id, node)
                updated_at = node["updatedAt"]
                if not oldest_at or updated_at < oldest_at:
                    oldest_at = updated_at

            # Update sync_oldest_at after each page
            if oldest_at:
                repo.sync_oldest_at = oldest_at
                self.store.upsert_repository(repo)

            page_info = search_data["pageInfo"]
            if not page_info["hasNextPage"]:
                # If no more pages, it means we reached the beginning
                repo.sync_oldest_at = repo.repo_created_at
                self.store.upsert_repository(repo)
                break
            cursor = page_info["endCursor"]

    def _save_node(self, repo_id: str, node: dict):
        # Save Issue/Thread
        thread = Thread(
            id=node["id"],
            repo_id=repo_id,
            number=node["number"],
            type="ISSUE",
            author=node["author"]["login"] if node["author"] else None,
            title=node["title"],
            body=node["body"],
            url=node.get("url"),
            last_known_updated_at=node["updatedAt"],
        )
        self.store.upsert_thread(thread)

        # Save Comments
        for comment_node in node["comments"]["nodes"]:
            comment = Comment(
                id=comment_node["id"],
                thread_id=thread.id,
                author=comment_node["author"]["login"] if comment_node["author"] else None,
                body=comment_node["body"],
                url=comment_node.get("url"),
                created_at=comment_node["createdAt"],
            )
            self.store.upsert_comment(comment)

        # TODO: Handle comment pagination if there are more than 100 comments
