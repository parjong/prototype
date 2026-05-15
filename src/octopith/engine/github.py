import logging
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)


class GitHubClient:
    def __init__(self, token: str, base_url: str = "https://api.github.com/graphql"):
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v4.idl",
        }

    async def execute(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json={"query": query, "variables": variables or {}},
                headers=self.headers,
                timeout=30.0,
            )

            if response.status_code != 200:
                logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                response.raise_for_status()

            data = response.json()
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                raise Exception(f"GraphQL error: {data['errors']}")

            # TODO: Handle rate limit headers
            # x-ratelimit-remaining, x-ratelimit-reset

            return data["data"]

    def build_search_query(
        self, repo: str, updated_after: Optional[str] = None, updated_before: Optional[str] = None
    ) -> str:
        parts = [f"repo:{repo}", "is:issue"]  # For now focus on issues
        if updated_after:
            parts.append(f"updated:>{updated_after}")
        if updated_before:
            parts.append(f"updated:<{updated_before}")
        return " ".join(parts)


ISSUE_SEARCH_QUERY = """
query ($queryString: String!, $cursor: String) {
  search(query: $queryString, type: ISSUE, first: 100, after: $cursor) {
    nodes {
      ... on Issue {
        id
        number
        title
        body
        updatedAt
        createdAt
        url
        author {
          login
        }
        repository {
          id
          url
          nameWithOwner
          createdAt
        }
        comments(first: 100) {
          nodes {
            id
            body
            author {
              login
            }
            createdAt
            url
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""
