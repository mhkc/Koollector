"""Document conversion command for Koolector CLI."""

import logging

import click

from koollector.core.pipeline import convert_document
from koollector.core.settings import OutputFormat

from .common import load_settings

LOG = logging.getLogger(__name__)


@click.command("convert")
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=True),
    help="Path to the configuration file.",
)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(OutputFormat),
    help="Output format for the converted documents.",
)
@click.option(
    "-o",
    "--output-dir",
    "output_dir",
    type=click.Path(exists=True),
    help="Path to the output directory.",
)
@click.argument("sources", nargs=-1, type=click.Path(exists=True))
def convert_documents(config_file, output_format, output_dir, sources: str):
    """Convert documents based on the specified profile."""

    LOG.info("Output directory: %s", output_dir)
    LOG.info("Input files: %s", sources)

    # read file from source
    for source in sources:
        LOG.info("Processing source: %s", source)
        out_fmt = output_format or profile.output_format
        convert_document(source, output_format=out_fmt, profile=profile, output_dir_override=output_dir)
