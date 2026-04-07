"""Configure logging for the application."""

import logging
import sys

import click
from click import UsageError

from koollector.core.settings import Settings, BUILTIN_PRESETS


def load_settings(yaml_file: str | None = None) -> Settings:
    """Load settings from a YAML file."""
    try:
        if yaml_file:
            return Settings(_yaml_file=yaml_file)
        return Settings()
    except Exception as exc:
        raise click.ClickException(f"Invalid configuration: {exc}") from exc


def setup_logging(verbose: bool = False) -> None:
    """Configure application logging."""

    root = logging.getLogger()  # root logger

    if root.handlers:
        return

    level = logging.DEBUG if verbose else logging.INFO

    handler = logging.StreamHandler(sys.stderr)

    if verbose:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        formatter = logging.Formatter("%(levelname)s: %(message)s")

    handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(handler)


def resolve_conversion_config(preset_name, fmt, settings: Settings):
    if preset_name and fmt:
        raise UsageError("Use either --preset or --format, not both")

    if preset_name:
        return settings.profiles.get(preset_name)

    if fmt:
        return BUILTIN_PRESETS.get(fmt)

    raise UsageError("You must specify --preset or --format")