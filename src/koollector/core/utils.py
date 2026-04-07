"""Various utility functions for Koolector."""

from datetime import datetime
from pathlib import Path


def make_output_path(profile, *, dir_override: Path | None = None, **kwargs) -> Path:
    """Generate output path based on profile and optional directory override."""

    output_dir = dir_override or profile.output_location
    return output_dir / profile.output_filename_template.format(
        source_name=Path(kwargs.get("source", "")).stem,
        format=profile.output_format.value,
        timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
    )


def write_output(path: Path, content: str) -> None:
    """Write content to the specified path, creating parent directories if needed."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
