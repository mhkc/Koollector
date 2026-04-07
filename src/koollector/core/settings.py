"""Manage configuration for the application."""

from enum import StrEnum

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SourceType(StrEnum):
    """Supported source types."""

    PAPERLESS = "paperless"
    FILESYSTEM = "filesystem"


class OutputFormat(StrEnum):
    """Supported ouptut formats."""

    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"
    TEXT = "text"
    DOCTAGS = "doctags"


class FileSystemSource(BaseModel):
    """Configuration for fetching documents from the filesystem."""
    type: SourceType = SourceType.FILESYSTEM
    paths: list[str] = Field(default_factory=list)  # List of file paths or directories
    extensions: list[str] | None = None


class PaperlessSource(BaseModel):
    """Configuration for fetching documents from Paperless."""

    type: SourceType = SourceType.PAPERLESS
    query: str | None = None           # e.g. "tag:invoice"
    tags: list[str] | None = None
    correspondent: str | None = None
    document_type: str | None = None


class ConvertConfig(BaseModel):
    """Configuration for document conversion."""

    output_format: OutputFormat = OutputFormat.MARKDOWN
    ocr: bool = False
    language: str | None = None


class RagConfig(BaseModel):
    """Configuration for OpenWebUi RAG processing."""

    enabled: bool = True
    collection: str
    base_tags: list[str] = Field(default_factory=list)
    push_metadata: bool = True


class OutputConfig(BaseModel):
    """Configuration for output storage."""

    directory: str | None = None
    output_format: OutputFormat = OutputFormat.MARKDOWN
    filename_template: str = "{source_name}_{created_at}"
    overwrite: bool = False


class Preset(BaseModel):
    """A preset defines how documents are sourced, converted, and ingested."""

    description: str | None = None

    source: FileSystemSource | PaperlessSource
    convert: ConvertConfig
    rag: RagConfig | None = None
    output: OutputConfig | None = None

    enabled: bool = True


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    paperless_api_url: str | None = None
    paperless_api_token: str | None = None

    presets: dict[str, Preset] = Field(default_factory=dict)
