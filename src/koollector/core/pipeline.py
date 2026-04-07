"""Orchestrate multi step workflows for processing documents."""

import logging
from pathlib import Path

from .services.converter import convert
from .settings import OutputFormat, Preset
from .utils import make_output_path, write_output

LOG = logging.getLogger(__name__)


def process_documents():
    """Process documents from paperless, annotate them and upload them to openwebui."""

    # fetch form paperless

    # convert document

    # annotate frontmatter with metadata from paperless

    # upload to openwebui

    # push tags to openwebui RAG

    # mark as processed in state store


def convert_document(
    source: str, *, output_format: OutputFormat, profile: Preset, output_dir_override: Path
) -> str:
    """Convert document to markdown format."""
    # convert document
    try:
        result = convert(source, output_format=output_format)
    except Exception as exc:
        LOG.error("Failed to convert document: %s", exc)

    output_path = make_output_path(
        profile, dir_override=output_dir_override, source=source
    )
    write_output(output_path, result)
