import sqlite3
import tomllib
from datetime import datetime
from pathlib import Path

import sqlite_vec
from sqlalchemy import event
from sqlmodel import SQLModel, create_engine

SCHEMA_VERSION = "v1.1.0"  # Increment version for vector support


class DBManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.version_file = db_path.with_suffix(".toml")
        self.engine = create_engine(f"sqlite:///{db_path}")

        # Load sqlite-vec extension for every connection
        @event.listens_for(self.engine, "connect")
        def load_extension(dbapi_conn, connection_record):
            dbapi_conn.enable_load_extension(True)
            sqlite_vec.load(dbapi_conn)
            dbapi_conn.enable_load_extension(False)

    def initialize(self):
        """Initialize the database and schema version file."""
        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create tables using SQLModel
        SQLModel.metadata.create_all(self.engine)

        # Additional setup (FTS5, Vectors, Triggers) using raw sqlite3
        # Always run this to ensure virtual tables/triggers exist
        self._setup_raw_sqlite()

        # Create or update version file
        self._update_version_file()

    def _setup_raw_sqlite(self):
        with sqlite3.connect(self.db_path) as conn:
            # Enable loadable extensions
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)

            # Enable WAL mode
            conn.execute("PRAGMA journal_mode=WAL;")

            # Create FTS5 tables
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS threads_fts USING fts5(
                    thread_id UNINDEXED,
                    title,
                    body,
                    author,
                    tokenize='trigram'
                );
            """)
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS comments_fts USING fts5(
                    comment_id UNINDEXED,
                    body,
                    author,
                    tokenize='trigram'
                );
            """)

            # Create Vector tables (768 dimensions for nomic-embed-text)
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS vec_threads USING vec0(
                    thread_id integer primary key,
                    embedding float[768]
                );
            """)
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS vec_summaries USING vec0(
                    summary_id integer primary key,
                    embedding float[768]
                );
            """)

            # Create ID Mapping table for string-to-int conversion (for threads, etc.)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS id_mapping (
                    int_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    string_id TEXT UNIQUE
                );
            """)

            # Migration: Ensure url columns exist
            try:
                conn.execute("ALTER TABLE threads ADD COLUMN url TEXT;")
            except sqlite3.OperationalError:
                pass
            try:
                conn.execute("ALTER TABLE comments ADD COLUMN url TEXT;")
            except sqlite3.OperationalError:
                pass

            # Create triggers for threads
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS threads_ai AFTER INSERT ON threads BEGIN
                    INSERT INTO threads_fts(thread_id, title, body, author)
                    VALUES (new.id, new.title, new.body, new.author);
                END;
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS threads_ad AFTER DELETE ON threads BEGIN
                    DELETE FROM threads_fts WHERE thread_id = old.id;
                END;
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS threads_au AFTER UPDATE ON threads BEGIN
                    UPDATE threads_fts
                    SET title = new.title, body = new.body, author = new.author
                    WHERE thread_id = old.id;
                END;
            """)

            # Create triggers for comments
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS comments_ai AFTER INSERT ON comments BEGIN
                    INSERT INTO comments_fts(comment_id, body, author)
                    VALUES (new.id, new.body, new.author);
                END;
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS comments_ad AFTER DELETE ON comments BEGIN
                    DELETE FROM comments_fts WHERE comment_id = old.id;
                END;
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS comments_au AFTER UPDATE ON comments BEGIN
                    UPDATE comments_fts
                    SET body = new.body, author = new.author
                    WHERE comment_id = old.id;
                END;
            """)
            conn.commit()

    def _update_version_file(self):
        content = f"""schema_version = "{SCHEMA_VERSION}"
migration_at = "{datetime.now().isoformat()}"
"""
        self.version_file.write_text(content)

    def check_version(self) -> bool:
        if not self.version_file.exists():
            return False

        with self.version_file.open("rb") as f:
            data = tomllib.load(f)
            return data.get("schema_version") == SCHEMA_VERSION

    def get_engine(self):
        return self.engine
