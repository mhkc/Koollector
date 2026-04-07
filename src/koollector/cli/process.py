"""Document processing command for Koolector CLI."""

import logging

import click

from .common import load_settings
from koollector.core.pipeline import process_documents as process_documents_pipeline

LOG = logging.getLogger(__name__)


@click.command("process")
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=True),
    help="Path to the configuration file.",
)
@click.option(
    "-p",
    "--profile",
    "profile_names",
    multiple=True,
    help="Name of the profile to use from the configuration.",
)
def process_documents(config_file, profile_names):
    """Process documents from paperless, annotate them and upload them to openwebui."""

    LOG.info("Using configuration file: %s", config_file)

    names = ", ".join(profile_names) if profile_names else "all"
    LOG.info("Using profiles: %s", names)

    settings = load_settings(config_file)
    for name, profile in settings.presets.items():
        if profile_names and name not in profile_names:
            LOG.info("Skipping profile: %s", name)
            continue

        LOG.info("Syncing profile: %s", name)
        process_documents_pipeline()