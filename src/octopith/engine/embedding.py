import logging
from datetime import datetime, timedelta
from typing import Optional

from octopith.db.store import Store
from octopith.engine.inference import InferenceAdapter

logger = logging.getLogger(__name__)


class EmbeddingEngine:
    def __init__(self, store: Store, adapter: InferenceAdapter):
        self.store = store
        self.adapter = adapter

    async def run(self, duration: Optional[timedelta] = None):
        """Run the embedding pipeline for threads and summaries."""
        start_time = datetime.now()

        # 1. Embed Threads (Issue Title + Body)
        threads = self.store.get_threads_needing_embedding()
        logger.info(f"Found {len(threads)} threads needing embedding")
        for thread in threads:
            if duration and datetime.now() - start_time > duration:
                logger.info("Duration reached. Stopping embedding.")
                return

            text = f"{thread.title}\n\n{thread.body}"
            try:
                vector = await self.adapter.embed(text)
                self.store.add_thread_embedding(thread.id, vector)
                logger.debug(f"Embedded thread {thread.id}")
            except Exception as e:
                logger.error(f"Failed to embed thread {thread.id}: {e}")

        # 2. Embed Summaries
        summaries = self.store.get_summaries_needing_embedding()
        logger.info(f"Found {len(summaries)} summaries needing embedding")
        for summary in summaries:
            if duration and datetime.now() - start_time > duration:
                logger.info("Duration reached. Stopping embedding.")
                return

            try:
                vector = await self.adapter.embed(summary.content)
                self.store.add_summary_embedding(summary.id, vector)
                logger.debug(f"Embedded summary {summary.id}")
            except Exception as e:
                logger.error(f"Failed to embed summary {summary.id}: {e}")

        logger.info("Embedding pipeline completed.")
