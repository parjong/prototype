from datetime import datetime, timezone
from typing import List, Optional, Sequence

from sqlmodel import Session, col, select, text

from .constants import MatchType
from .models import Comment, ModelAlias, ModelVariant, Repository, Summary, SummaryType, Thread


class Store:
    def __init__(self, engine):
        self.engine = engine

    # Repository operations
    def upsert_repository(self, repo: Repository):
        with Session(self.engine) as session:
            existing = session.get(Repository, repo.id)
            if existing:
                for key, value in repo.model_dump(exclude={"id", "created_at"}).items():
                    setattr(existing, key, value)
            else:
                session.add(repo)
            session.commit()
            if existing:
                session.refresh(existing)
                return existing
            session.refresh(repo)
            return repo

    def get_repository(self, repo_id: str) -> Optional[Repository]:
        with Session(self.engine) as session:
            return session.get(Repository, repo_id)

    def get_repository_by_name(self, full_name: str) -> Optional[Repository]:
        with Session(self.engine) as session:
            statement = select(Repository).where(Repository.full_name == full_name)
            return session.exec(statement).first()

    def get_thread_summary(self, thread_id: str) -> Optional[Summary]:
        with Session(self.engine) as session:
            statement = (
                select(Summary)
                .where(Summary.target_id == thread_id)
                .order_by(Summary.created_at.desc())
            )
            return session.exec(statement).first()

    def get_threads_needing_summary(self, model_variant_id: int, repo_id: Optional[int] = None) -> Sequence[Thread]:
        with Session(self.engine) as session:
            # Subquery to find threads that already have a summary for this model
            subquery = select(Summary.target_id).where(
                Summary.model_variant_id == model_variant_id,
                Summary.summary_type_id == "THREAD_FULL",
            )

            # Find threads NOT in that subquery
            statement = select(Thread).where(col(Thread.id).not_in(subquery))
            if repo_id:
                statement = statement.where(Thread.repo_id == repo_id)
            return session.exec(statement).all()

    def get_comments_by_thread(self, thread_id: str) -> Sequence[Comment]:
        with Session(self.engine) as session:
            statement = (
                select(Comment).where(Comment.thread_id == thread_id).order_by(Comment.created_at)
            )
            return session.exec(statement).all()

    def add_summary(self, summary: Summary):
        with Session(self.engine) as session:
            # Check for existing summary to replace (SSOT principle)
            existing = session.exec(
                select(Summary).where(
                    Summary.target_id == summary.target_id,
                    Summary.summary_type_id == summary.summary_type_id,
                    Summary.model_variant_id == summary.model_variant_id,
                )
            ).first()

            if existing:
                existing.content = summary.content
                existing.created_at = datetime.now(timezone.utc)
                session.add(existing)
            else:
                session.add(summary)
            session.commit()

    def get_model_variant_by_alias(self, alias: str) -> Optional[ModelVariant]:
        with Session(self.engine) as session:
            # Join Alias with Variant
            statement = select(ModelVariant).join(ModelAlias).where(ModelAlias.id == alias)
            return session.exec(statement).first()

    def ensure_summary_types(self):
        with Session(self.engine) as session:
            types = ["THREAD_FULL", "COMMENT_ATOM"]
            for tid in types:
                existing = session.get(SummaryType, tid)
                if not existing:
                    session.add(SummaryType(id=tid, description=f"Automatic {tid} type"))
            session.commit()

    def list_repositories(self) -> List[Repository]:
        with Session(self.engine) as session:
            return list(session.exec(select(Repository)).all())

    # Thread operations
    def upsert_thread(self, thread: Thread):
        with Session(self.engine) as session:
            existing = session.get(Thread, thread.id)
            if existing:
                for key, value in thread.model_dump(
                    exclude={"id", "created_at", "repo_id"}
                ).items():
                    setattr(existing, key, value)
            else:
                session.add(thread)
            session.commit()
            if existing:
                session.refresh(existing)
                return existing
            session.refresh(thread)
            return thread

    def get_thread(self, thread_id: str) -> Optional[Thread]:
        with Session(self.engine) as session:
            return session.get(Thread, thread_id)

    # Comment operations
    def upsert_comment(self, comment: Comment):
        with Session(self.engine) as session:
            existing = session.get(Comment, comment.id)
            if existing:
                for key, value in comment.model_dump(
                    exclude={"id", "collected_at", "thread_id"}
                ).items():
                    setattr(existing, key, value)
            else:
                session.add(comment)
            session.commit()
            if existing:
                session.refresh(existing)
                return existing
            session.refresh(comment)
            return comment

    # Embedding operations
    def get_or_create_int_id(self, string_id: str) -> int:
        with Session(self.engine) as session:
            sql = "INSERT OR IGNORE INTO id_mapping (string_id) VALUES (:sid)"
            session.execute(text(sql), {"sid": string_id})
            sql = "SELECT int_id FROM id_mapping WHERE string_id = :sid"
            val = session.execute(text(sql), {"sid": string_id}).scalar()
            session.commit()
            return val

    def get_threads_needing_embedding(self) -> Sequence[Thread]:
        with Session(self.engine) as session:
            # Find threads whose mapped int_id is not in vec_threads
            sql = """
                SELECT id FROM threads 
                WHERE id NOT IN (
                    SELECT string_id FROM id_mapping 
                    JOIN vec_threads ON id_mapping.int_id = vec_threads.thread_id
                )
            """
            ids = session.execute(text(sql)).scalars().all()
            if not ids:
                return []
            return session.exec(select(Thread).where(col(Thread.id).in_(ids))).all()

    def add_thread_embedding(self, thread_oid: str, embedding: List[float]):
        import sqlite_vec

        int_id = self.get_or_create_int_id(thread_oid)
        with Session(self.engine) as session:
            sql = "INSERT OR REPLACE INTO vec_threads(thread_id, embedding) VALUES (:tid, :emb)"
            session.execute(
                text(sql), {"tid": int_id, "emb": sqlite_vec.serialize_float32(embedding)}
            )
            session.commit()

    def get_summaries_needing_embedding(self) -> Sequence[Summary]:
        with Session(self.engine) as session:
            sql = "SELECT id FROM summaries WHERE id NOT IN (SELECT summary_id FROM vec_summaries)"
            ids = session.execute(text(sql)).scalars().all()
            if not ids:
                return []
            return session.exec(select(Summary).where(col(Summary.id).in_(ids))).all()

    def add_summary_embedding(self, summary_id: int, embedding: List[float]):
        import sqlite_vec

        with Session(self.engine) as session:
            sql = "INSERT OR REPLACE INTO vec_summaries(summary_id, embedding) VALUES (:sid, :emb)"
            session.execute(
                text(sql), {"sid": summary_id, "emb": sqlite_vec.serialize_float32(embedding)}
            )
            session.commit()

    # FTS Search
    def search_fast(
        self, query: str, repo_ids: Optional[List[str]] = None, limit: int = 50
    ) -> List[dict]:
        import sqlite3

        db_path = str(self.engine.url).replace("sqlite:///", "")
        results = []
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            sql = """
                SELECT 
                    t.id, t.repo_id, t.number, t.type, t.author, t.title, 
                    t.last_known_updated_at, ? as match_key, fts.rank,
                    t.id as match_id, t.url as match_url
                FROM threads_fts fts
                JOIN threads t ON t.id = fts.thread_id
                WHERE threads_fts MATCH ?

                UNION ALL

                SELECT 
                    t.id, t.repo_id, t.number, t.type, t.author, t.title, 
                    t.last_known_updated_at, ? as match_key, fts.rank,
                    t.id as match_id, t.url as match_url
                FROM threads_fts fts
                JOIN threads t ON t.id = fts.thread_id
                WHERE threads_fts MATCH ?

                UNION ALL

                SELECT 
                    t.id, t.repo_id, t.number, 'COMMENT' as type, c.author, t.title, 
                    c.created_at as last_known_updated_at, ? as match_key, fts.rank,
                    c.id as match_id, c.url as match_url
                FROM comments_fts fts
                JOIN comments c ON c.id = fts.comment_id
                JOIN threads t ON t.id = c.thread_id
                WHERE comments_fts MATCH ?
            """
            # Quote query for FTS5 to handle hyphens and special characters
            # We escape double quotes by doubling them.
            safe_query = f'"{query.replace('"', '""')}"'

            params = [
                MatchType.FTS_TITLE.value,
                f"title:{safe_query}",
                MatchType.FTS_BODY.value,
                f"body:{safe_query}",
                MatchType.FTS_COMMENT.value,
                safe_query,
            ]

            # Since we use UNION ALL, we need to wrap it to apply repo filter and order
            wrapper_sql = f"""
                SELECT * FROM ({sql}) AS combined
            """
            if repo_ids:
                wrapper_sql += " WHERE repo_id IN (" + ",".join(["?"] * len(repo_ids)) + ")"
                params.extend(repo_ids)

            wrapper_sql += " ORDER BY rank LIMIT ?"
            params.append(limit)

            cursor = conn.execute(wrapper_sql, params)
            for row in cursor:
                d = dict(row)
                d["match_label"] = MatchType.to_label(d["match_key"])
                results.append(d)
        return results

    # Hybrid Search
    def search_vector(self, query_vector: List[float], limit: int = 20) -> List[dict]:
        import sqlite3

        import sqlite_vec

        db_path = str(self.engine.url).replace("sqlite:///", "")
        results = []
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)

            # 1. Search in threads
            sql_threads = f"""
                SELECT 
                    t.id, t.repo_id, t.number, t.type, t.author, t.title, 
                    t.last_known_updated_at, '{MatchType.VECTOR_CONTENT.value}' as match_key, distance,
                    t.id as match_id, t.url as match_url
                FROM vec_threads v
                JOIN id_mapping m ON m.int_id = v.thread_id
                JOIN threads t ON t.id = m.string_id
                WHERE embedding MATCH ? AND k = ?
            """
            cursor = conn.execute(sql_threads, [sqlite_vec.serialize_float32(query_vector), limit])
            for row in cursor:
                results.append(dict(row))

            # 2. Search in summaries
            sql_summaries = f"""
                SELECT 
                    t.id, t.repo_id, t.number, t.type, t.author, t.title, 
                    t.last_known_updated_at, '{MatchType.VECTOR_SUMMARY.value}' as match_key, distance,
                    t.id as match_id, t.url as match_url
                FROM vec_summaries v
                JOIN summaries s ON s.id = v.summary_id
                JOIN threads t ON t.id = s.target_id
                WHERE embedding MATCH ? AND k = ?
            """
            cursor = conn.execute(
                sql_summaries, [sqlite_vec.serialize_float32(query_vector), limit]
            )
            for row in cursor:
                results.append(dict(row))

        # Sort the combined results from threads and summaries globally by distance
        results.sort(key=lambda x: x["distance"])
        return results

    def search_hybrid(
        self,
        query_text: str,
        query_vector: List[float],
        repo_ids: Optional[List[str]] = None,
        limit: int = 20,
    ) -> List[dict]:
        # 1. Get Keyword Results
        fts_results = self.search_fast(query_text, repo_ids=repo_ids)

        # 2. Get Vector Results
        vec_results = self.search_vector(query_vector, limit=limit)
        if repo_ids:
            vec_results = [r for r in vec_results if r["repo_id"] in repo_ids]

        # 3. Apply RRF (Reciprocal Rank Fusion)
        k = 60
        scores = {}  # match_id -> score
        id_to_data = {}  # match_id -> row data

        for rank, res in enumerate(fts_results, 1):
            mid = res["match_id"]
            scores[mid] = scores.get(mid, 0) + (1.0 / (k + rank))
            if mid not in id_to_data:
                res["match_sources"] = [res.pop("match_key")]
                id_to_data[mid] = res
            else:
                key = res.pop("match_key")
                if key not in id_to_data[mid]["match_sources"]:
                    id_to_data[mid]["match_sources"].append(key)

        seen_vec_nodes = set()
        v_rank = 1
        for res in vec_results:
            mid = res["match_id"]
            key = res.pop("match_key")

            if mid not in id_to_data:
                res["match_sources"] = [key]
                id_to_data[mid] = res
            else:
                if key not in id_to_data[mid]["match_sources"]:
                    id_to_data[mid]["match_sources"].append(key)

            if mid in seen_vec_nodes:
                continue
            seen_vec_nodes.add(mid)
            scores[mid] = scores.get(mid, 0) + (1.0 / (k + v_rank))
            v_rank += 1

        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        final_results = []
        for mid in sorted_ids[:limit]:
            row = id_to_data[mid]
            row["score"] = scores[mid]
            # Create human-readable label
            row["match_label"] = " + ".join([MatchType.to_label(s) for s in row["match_sources"]])
            final_results.append(row)

        return final_results
