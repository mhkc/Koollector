"""CLI entry point for Koolector."""

import click

from .common import setup_logging
from .process import process_documents
from .convert import convert_documents


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging.")
@click.pass_context
def cli(ctx, verbose):
    """Koollector: A document collection and processing tool."""

    setup_logging(verbose)


# Add commands to the CLI group
cli.add_command(process_documents)
cli.add_command(convert_documents)