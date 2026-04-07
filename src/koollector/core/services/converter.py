"""Convert documents to markdown files."""

from docling.document_converter import DocumentConverter

from koollector.core.settings import OutputFormat


def convert(source: str, output_format: OutputFormat = OutputFormat.MARKDOWN):
    """Convert the input document to markdown format."""
    converter = DocumentConverter()
    doc = converter.convert(source).document

    if output_format == OutputFormat.MARKDOWN:
        return doc.to_markdown()
    elif output_format == OutputFormat.HTML:
        return doc.to_html()
    elif output_format == OutputFormat.JSON:
        return doc.to_json()
    elif output_format == OutputFormat.TEXT:
        return doc.to_text()
    elif output_format == OutputFormat.DOCTAGS:
        return doc.to_doctags()
    else:
        raise ValueError(f"Unsupported output format: {output_format}")
