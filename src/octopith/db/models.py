from datetime import datetime, timezone
from typing import ClassVar, Optional

from sqlmodel import Field, SQLModel


class Repository(SQLModel, table=True):
    __tablename__: ClassVar[str] = "repositories"
    id: str = Field(primary_key=True)
    api_url: str
    full_name: str = Field(unique=True, index=True)
    sync_newest_at: Optional[str] = None
    sync_oldest_at: Optional[str] = None
    repo_created_at: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Thread(SQLModel, table=True):
    __tablename__: ClassVar[str] = "threads"
    id: str = Field(primary_key=True)
    repo_id: str = Field(foreign_key="repositories.id", index=True)
    number: int
    type: str  # 'ISSUE', 'DISCUSSION'
    author: Optional[str] = None
    title: str
    body: Optional[str] = None
    url: Optional[str] = None
    last_known_updated_at: str = Field(index=True)
    title_hash: Optional[str] = None
    body_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Comment(SQLModel, table=True):
    __tablename__: ClassVar[str] = "comments"
    id: str = Field(primary_key=True)
    thread_id: str = Field(foreign_key="threads.id", index=True)
    author: Optional[str] = None
    body: Optional[str] = None
    url: Optional[str] = None
    created_at: str
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SummaryType(SQLModel, table=True):
    __tablename__: ClassVar[str] = "summary_types"
    id: str = Field(primary_key=True)  # 'THREAD_FULL', 'COMMENT_ATOM', etc.
    description: Optional[str] = None
    format_spec: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ModelVariant(SQLModel, table=True):
    __tablename__: ClassVar[str] = "model_variants"
    id: Optional[int] = Field(default=None, primary_key=True)
    engine: str
    model_name: str
    variant_tag: Optional[str] = None
    type: str  # 'summary', 'embedding'
    config_schema: str = "v1"
    config_data: str  # JSON string
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ModelAlias(SQLModel, table=True):
    __tablename__: ClassVar[str] = "models"
    id: str = Field(primary_key=True)  # alias
    variant_id: int = Field(foreign_key="model_variants.id")


class Summary(SQLModel, table=True):
    __tablename__: ClassVar[str] = "summaries"
    id: Optional[int] = Field(default=None, primary_key=True)
    target_id: str = Field(index=True)
    summary_type_id: str = Field(foreign_key="summary_types.id")
    model_variant_id: int = Field(foreign_key="model_variants.id")
    content: str
    prompt_version: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Config(SQLModel, table=True):
    __tablename__: ClassVar[str] = "configs"
    key: str = Field(primary_key=True)
    value: Optional[str] = None
    description: Optional[str] = None
