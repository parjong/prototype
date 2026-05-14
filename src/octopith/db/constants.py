from enum import Enum


class MatchType(str, Enum):
    FTS_TITLE = "fts_title"
    FTS_BODY = "fts_body"
    FTS_COMMENT = "fts_body"  # For comments, it's always the body
    VECTOR_CONTENT = "vector_content"
    VECTOR_SUMMARY = "vector_summary"
    HYBRID = "hybrid"

    @classmethod
    def to_label(cls, key: str) -> str:
        mapping: dict[str, str] = {
            cls.FTS_TITLE.value: "Keyword: Title",
            cls.FTS_BODY.value: "Keyword: Body",
            cls.VECTOR_CONTENT.value: "Semantic: Content",
            cls.VECTOR_SUMMARY.value: "Semantic: Summary",
            cls.HYBRID.value: "Hybrid Match",
        }
        return mapping.get(key, key)

    @classmethod
    def get_all_descriptions(cls) -> str:
        # \b at the start of each paragraph prevents Click from re-wrapping it.
        content = (
            "\b\n"
            "Search the collected GitHub knowledge base for relevant issues and discussions.\n"
            "\n"
            "\b\n"
            "OUTPUT INFORMATION (Agent-first):\n"
            "Each result provides structured JSON by default, including:\n"
            "  - identifier: Unique ID (<owner>/<repo>#<number>) for follow-up actions.\n"
            "  - type: Result object type (ISSUE, DISCUSSION, or COMMENT).\n"
            '  - match_sources: Structured list of match reason tags (e.g., ["fts_title", "vector_content"]).\n'
            "  - match_url: Direct URL to the specific matched item (issue or comment).\n"
            "\n"
            "\b\n"
            "MATCH SOURCE TAGS:\n"
            f"  - {cls.FTS_TITLE.value:16}: Found in the title using FTS5.\n"
            f"  - {cls.FTS_BODY.value:16}: Found in the body text (Issue or Comment).\n"
            f"  - {cls.VECTOR_CONTENT.value:16}: Found via semantic vector search on original content.\n"
            f"  - {cls.VECTOR_SUMMARY.value:16}: Found via semantic vector search on AI summaries.\n"
            f"  - {cls.HYBRID.value:16}: Combined keyword and semantic match (RRF scored)."
        )
        return content
