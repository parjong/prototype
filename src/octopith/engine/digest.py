import logging
import time
from typing import Optional

from ..db.models import ModelVariant, Summary
from ..db.store import Store
from .summarizer import Summarizer

logger = logging.getLogger(__name__)


class DigestEngine:
    def __init__(self, store: Store, summarizer: Summarizer):
        self.store = store
        self.summarizer = summarizer

    async def run(self, duration_seconds: Optional[float] = None, model_alias: str = "default", repo_id: Optional[int] = None):
        start_time = time.time()

        model_variant = self._get_model_variant(model_alias)
        if not model_variant:
            logger.error(f"Model variant for alias '{model_alias}' not found.")
            return

        threads = self.store.get_threads_needing_summary(model_variant.id, repo_id=repo_id)

        logger.info(f"Found {len(threads)} threads needing summarization.")

        processed_count = 0
        for thread in threads:
            # Check duration
            if duration_seconds and (time.time() - start_time) > duration_seconds:
                logger.info("Duration reached. Stopping digest.")
                break

            logger.info(f"Summarizing thread {thread.id} (#{thread.number})")
            try:
                # Get comments and map to dicts for Summarizer
                comment_objs = self.store.get_comments_by_thread(thread.id)
                comments_data = [
                    {"author": c.author or "Unknown", "body": c.body or ""} for c in comment_objs
                ]

                # Perform summarization (await because it's async)
                summary_text = await self.summarizer.summarize_thread(
                    title=thread.title, body=thread.body or "", comments=comments_data
                )

                # Save to DB
                summary = Summary(
                    target_id=thread.id,
                    summary_type_id="THREAD_FULL",
                    model_variant_id=model_variant.id,
                    content=summary_text,
                    prompt_version="v1",
                )
                self.store.add_summary(summary)
                processed_count += 1

            except Exception as e:
                logger.error(f"Failed to summarize thread {thread.id}: {e}")

        logger.info(f"Digest completed. Processed {processed_count} threads.")

    def _get_model_variant(self, alias: str) -> Optional[ModelVariant]:
        # Dummy implementation: try to find any variant if alias is 'default'
        # In Phase 2, we should implement proper model management
        return self.store.get_model_variant_by_alias(alias)
