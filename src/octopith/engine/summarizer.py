import logging
from typing import Dict, List, Optional

from .inference import InferenceAdapter

logger = logging.getLogger(__name__)


class Summarizer:
    def __init__(self, adapter: InferenceAdapter):
        self.adapter = adapter

    async def summarize_thread(
        self,
        title: str,
        body: str,
        comments: List[Dict[str, str]],
        summary_type: str = "TLDR",
    ) -> str:
        """
        Summarize a thread and its comments.
        summary_type: 'TLDR' (general summary) or 'TROUBLESHOOTING' (focus on solutions)
        """
        prompt = self._build_prompt(title, body, comments, summary_type)
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes GitHub issues. You MUST always respond in English, regardless of the language of the input."},
            {"role": "user", "content": prompt},
        ]
        
        return await self.adapter.chat(messages)

    def _build_prompt(
        self,
        title: str,
        body: str,
        comments: List[Dict[str, str]],
        summary_type: str,
    ) -> str:
        comment_text = "\n".join(
            [f"- {c['author']}: {c['body']}" for c in comments]
        )
        
        context = f"Title: {title}\nBody: {body}\nComments:\n{comment_text}"
        
        if summary_type == "TROUBLESHOOTING":
            return f"""
The following is a GitHub issue and its discussion. 
Please provide a troubleshooting guide based on this discussion. 
Identify the core problem and the final solution or workarounds discussed.
IMPORTANT: You MUST write the summary in English, even if the input text is in Korean or any other language.

{context}

Troubleshooting Guide (in English):
"""
        else: # Default TLDR
            return f"""
The following is a GitHub issue and its discussion. 
Please provide a concise TLDR summary (maximum 3 sentences).
IMPORTANT: You MUST write the summary in English, even if the input text is in Korean or any other language.

{context}

TLDR (in English):
"""
