"""State management for the application."""

from datetime import datetime
from datetime.timezone import timezone
import logging
import json
import os
from pathlib import Path
import tempfile
from typing import Any


LOG = logging.getLogger(__name__)


def _now_iso() -> str:
    """Get current time as ISO string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class DocumentState:
    """Simple JSON file store for processed documents."""


    def __init__(self, root: Path | str, name: str = "state.json"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.name = name

        # load state
        self._state = self.load() or {}

        self.created_at = self._state.get("created_at") or _now_iso()
        self.updated_at = self._state.get("updated_at") or _now_iso()

    @property
    def path(self) -> Path:
        """Get the path to the state file."""
        return self.root / self.name
    
    def load(self) -> dict[str, Any] | None:
        """Load state from JSON file; return None if not found."""

        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self) -> None:
        """Save state to JSON file atomically."""

        tmp_fd, tmp_name = tempfile.mkstemp(
            dir=str(self.root), prefix=self.path.name, suffix=".tmp"
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
                json.dump(self._state, fh, ensure_ascii=False, indent=2)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_name, self.path)  # atomic on POSIX
        finally:
            try:
                if os.path.exists(tmp_name):
                    os.remove(tmp_name)
            except Exception:  # best effort cleanup
                LOG.debug("Failed to cleanup tmp file: %s", tmp_name)

    def mark_processed(self, doc_id: str) -> None:
        """Mark a document as processed."""
        self._state[doc_id] = {"processed_at": _now_iso()}
        self.updated_at = _now_iso()
        self.save()
    
    def is_processed(self, doc_id: str) -> bool:
        """Check if a document has been processed."""
        return doc_id in self._state