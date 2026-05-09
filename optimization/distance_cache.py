"""Distance cache utilities for backend road-routing calls."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class DistanceCache:
    """Cache road distances by normalized coordinate pairs.

    The cache is undirected because road-network distance is expected to be
    equivalent for the simple bidirectional graph edges used by this package.
    """

    def __init__(self, path: str | Path | None = None) -> None:
        """Initialize the cache, optionally loading persisted JSON data."""
        self.path = Path(path) if path else None
        self._values: dict[str, float] = {}
        if self.path:
            self.load()

    def get(self, start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> float | None:
        """Return a cached distance in kilometers when present."""
        key = self.make_key(start_lat, start_lon, end_lat, end_lon)
        value = self._values.get(key)
        if value is not None:
            logger.info("Distance cache hit for %s: %.3f km", key, value)
        return value

    def set(
        self,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float,
        distance_km: float,
    ) -> None:
        """Store a distance in kilometers."""
        key = self.make_key(start_lat, start_lon, end_lat, end_lon)
        self._values[key] = float(distance_km)

    def load(self) -> None:
        """Load persisted distances from disk if the cache file exists."""
        if not self.path or not self.path.exists():
            return

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to load distance cache %s: %s", self.path, exc)
            return

        if isinstance(raw, dict):
            self._values = {str(key): float(value) for key, value in raw.items()}

    def save(self) -> None:
        """Persist cached distances to disk when a path was configured."""
        if not self.path:
            return

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self._values, indent=2, sort_keys=True), encoding="utf-8")
        except OSError as exc:
            logger.warning("Failed to save distance cache %s: %s", self.path, exc)

    @staticmethod
    def make_key(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> str:
        """Build a stable undirected key for two coordinate pairs."""
        first = f"{float(start_lat):.6f},{float(start_lon):.6f}"
        second = f"{float(end_lat):.6f},{float(end_lon):.6f}"
        ordered = sorted([first, second])
        return "|".join(ordered)

    def as_dict(self) -> dict[str, Any]:
        """Return a plain dict copy of cached values."""
        return dict(self._values)


DEFAULT_DISTANCE_CACHE = DistanceCache()
