"""OSRM-backed road distance service for backend graph routing."""

from __future__ import annotations

import json
import logging
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from optimization.distance_cache import DEFAULT_DISTANCE_CACHE, DistanceCache

logger = logging.getLogger(__name__)

DEFAULT_OSRM_BASE_URL = "https://router.project-osrm.org"


def fetch_route_data(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    *,
    osrm_base_url: str = DEFAULT_OSRM_BASE_URL,
    timeout: float = 10.0,
    retries: int = 2,
) -> dict[str, Any] | None:
    """Fetch route data from OSRM for two latitude/longitude points.

    Returns ``None`` after retry exhaustion or when OSRM cannot provide a route.
    """
    query = urlencode({"overview": "false", "alternatives": "false", "steps": "false"})
    coordinates = f"{float(start_lon)},{float(start_lat)};{float(end_lon)},{float(end_lat)}"
    url = f"{osrm_base_url.rstrip('/')}/route/v1/driving/{coordinates}?{query}"

    for attempt in range(1, retries + 2):
        try:
            with urlopen(url, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            logger.warning("OSRM route fetch failed on attempt %s for %s: %s", attempt, coordinates, exc)
            if attempt <= retries:
                time.sleep(min(0.25 * attempt, 1.0))
            continue

        if payload.get("code") != "Ok" or not payload.get("routes"):
            logger.warning("OSRM returned no route for %s: %s", coordinates, payload.get("message", payload.get("code")))
            return None

        logger.info("Fetched OSRM route for %s", coordinates)
        return payload

    return None


def get_road_distance(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    *,
    cache: DistanceCache | None = DEFAULT_DISTANCE_CACHE,
    osrm_base_url: str = DEFAULT_OSRM_BASE_URL,
    timeout: float = 10.0,
    retries: int = 2,
) -> float | None:
    """Return the real road distance in kilometers between two points."""
    if cache:
        cached = cache.get(start_lat, start_lon, end_lat, end_lon)
        if cached is not None:
            return cached

    route_data = fetch_route_data(
        start_lat,
        start_lon,
        end_lat,
        end_lon,
        osrm_base_url=osrm_base_url,
        timeout=timeout,
        retries=retries,
    )
    if not route_data:
        return None

    try:
        distance_meters = float(route_data["routes"][0]["distance"])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        logger.warning("OSRM response missing route distance: %s", exc)
        return None

    distance_km = distance_meters / 1000.0
    if distance_km <= 0:
        logger.warning("Ignoring non-positive OSRM route distance: %.3f km", distance_km)
        return None

    logger.info(
        "Computed road distance %.3f km for %.6f,%.6f -> %.6f,%.6f",
        distance_km,
        start_lat,
        start_lon,
        end_lat,
        end_lon,
    )

    if cache:
        cache.set(start_lat, start_lon, end_lat, end_lon, distance_km)
        cache.save()

    return distance_km
