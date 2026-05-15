-- Core Tables
CREATE TABLE IF NOT EXISTS repositories (
    id TEXT PRIMARY KEY, -- node_id
    api_url TEXT NOT NULL,
    full_name TEXT NOT NULL UNIQUE,
    sync_newest_at TEXT, -- ISO8601
    sync_oldest_at TEXT, -- ISO8601
    repo_created_at TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS threads (
    id TEXT PRIMARY KEY, -- node_id
    repo_id TEXT NOT NULL,
    type TEXT NOT NULL, -- 'ISSUE', 'DISCUSSION'
    author TEXT,
    title TEXT NOT NULL,
    body TEXT,
    last_known_updated_at TEXT NOT NULL,
    title_hash TEXT,
    body_hash TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (repo_id) REFERENCES repositories(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_threads_repo_id ON threads(repo_id);
CREATE INDEX IF NOT EXISTS idx_threads_updated_at ON threads(last_known_updated_at);

CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY, -- node_id
    thread_id TEXT NOT NULL,
    author TEXT,
    body TEXT,
    created_at TEXT NOT NULL, -- Original created_at from GitHub
    collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_comments_thread_id ON comments(thread_id);

-- Intelligence Tables
CREATE TABLE IF NOT EXISTS summary_types (
    id TEXT PRIMARY KEY, -- 'THREAD_FULL', 'COMMENT_ATOM', 'TROUBLESHOOTING', etc.
    description TEXT,
    format_spec TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    engine TEXT NOT NULL, -- 'ollama', 'vllm', etc.
    model_name TEXT NOT NULL,
    variant_tag TEXT,
    type TEXT NOT NULL, -- 'summary', 'embedding'
    config_schema TEXT DEFAULT 'v1',
    config_data TEXT NOT NULL, -- JSON
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS models (
    id TEXT PRIMARY KEY, -- alias (e.g., 'qwen-std')
    variant_id INTEGER NOT NULL,
    FOREIGN KEY (variant_id) REFERENCES model_variants(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_id TEXT NOT NULL, -- thread_id or comment_id
    summary_type_id TEXT NOT NULL,
    model_variant_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    prompt_version TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (summary_type_id) REFERENCES summary_types(id),
    FOREIGN KEY (model_variant_id) REFERENCES model_variants(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_summaries_target_model ON summaries(target_id, model_variant_id);

-- Search Tables (Virtual)
-- FTS5 for threads and comments (we might want to combine them or keep them separate)
CREATE VIRTUAL TABLE IF NOT EXISTS threads_fts USING fts5(
    thread_id UNINDEXED,
    title,
    body,
    author,
    tokenize='trigram' -- Trigram is good for CJK and code
);

-- Configs
CREATE TABLE IF NOT EXISTS configs (
    key TEXT PRIMARY KEY,
    value TEXT,
    description TEXT
);

-- Triggers for FTS (Optional but recommended)
CREATE TRIGGER IF NOT EXISTS threads_ai AFTER INSERT ON threads BEGIN
    INSERT INTO threads_fts(thread_id, title, body, author) VALUES (new.id, new.title, new.body, new.author);
END;

CREATE TRIGGER IF NOT EXISTS threads_ad AFTER DELETE ON threads BEGIN
    DELETE FROM threads_fts WHERE thread_id = old.id;
END;

CREATE TRIGGER IF NOT EXISTS threads_au AFTER UPDATE ON threads BEGIN
    UPDATE threads_fts SET title = new.title, body = new.body, author = new.author WHERE thread_id = old.id;
END;
