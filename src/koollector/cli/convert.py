"""Document conversion command for Koolector CLI."""

import logging

import click

from koollector.core.pipeline import convert_document
from koollector.core.settings import OutputFormat

from .common import load_settings, resolve_conversion_config

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
@click.option(
    "-p",
    "--preset",
    "preset_name",
    type=str,
    help="Name of the profile to use from the configuration.",
)
@click.argument("sources", nargs=-1, type=click.Path(exists=True))
def convert_documents(config_file, output_format, output_dir, preset_name: str, sources: str):
    """Convert documents based on the specified profile."""

    LOG.info("Using configuration file: %s", config_file)
    LOG.info("Profile: %s", preset_name)
    LOG.info("Output directory: %s", output_dir)
    LOG.info("Input files: %s", sources)

    settings = load_settings(config_file)
    preset = resolve_conversion_config(preset_name, output_format, settings)

    # read file from source
    for source in sources:
        LOG.info("Processing source: %s", source)
        out_fmt = output_format or preset.output_format
        convert_document(source, output_format=out_fmt, preset=preset, output_dir_override=output_dir)
