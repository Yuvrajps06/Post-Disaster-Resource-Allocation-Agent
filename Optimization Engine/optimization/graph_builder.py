"""NetworkX graph construction using OSRM-derived road distances."""

from __future__ import annotations

import logging
from typing import Any, Callable

import networkx as nx

from optimization.distance_cache import DEFAULT_DISTANCE_CACHE, DistanceCache
from optimization.routing_service import DEFAULT_OSRM_BASE_URL, get_road_distance

logger = logging.getLogger(__name__)

RoadDistanceProvider = Callable[[float, float, float, float], float | None]


def build_weighted_graph(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    *,
    cache: DistanceCache | None = DEFAULT_DISTANCE_CACHE,
    osrm_base_url: str = DEFAULT_OSRM_BASE_URL,
    route_provider: RoadDistanceProvider | None = None,
) -> nx.Graph:
    """Build a NetworkX graph with edge weights from real road distances.

    Incoming edge ``weight`` values are intentionally ignored.
    """
    graph = nx.Graph()

    for node in nodes:
        node_id = node.get("id")
        if not node_id:
            logger.warning("Skipping node without id: %s", node)
            continue
        graph.add_node(node_id, id=node_id, lat=node.get("lat"), lon=node.get("lon"))

    for edge in edges:
        source = edge.get("from")
        target = edge.get("to")
        if not source or not target:
            logger.warning("Skipping invalid edge without endpoints: %s", edge)
            continue
        if source not in graph or target not in graph:
            logger.warning("Skipping edge with unknown node: %s -> %s", source, target)
            continue
        graph.add_edge(source, target)

    return update_edge_weights(
        graph,
        cache=cache,
        osrm_base_url=osrm_base_url,
        route_provider=route_provider,
    )


def update_edge_weights(
    graph: nx.Graph,
    *,
    cache: DistanceCache | None = DEFAULT_DISTANCE_CACHE,
    osrm_base_url: str = DEFAULT_OSRM_BASE_URL,
    route_provider: RoadDistanceProvider | None = None,
) -> nx.Graph:
    """Refresh graph edge weights using OSRM road distances.

    Edges with invalid coordinates or failed routing lookups are removed so
    shortest-path calculations cannot accidentally use stale or fake weights.
    """
    failed_edges: list[tuple[Any, Any]] = []

    for source, target in list(graph.edges()):
        start = graph.nodes[source]
        end = graph.nodes[target]

        coordinates = _extract_coordinates(start, end)
        if coordinates is None:
            logger.warning("Skipping edge with invalid coordinates: %s -> %s", source, target)
            failed_edges.append((source, target))
            continue

        start_lat, start_lon, end_lat, end_lon = coordinates
        distance_km = _resolve_distance(
            start_lat,
            start_lon,
            end_lat,
            end_lon,
            cache=cache,
            osrm_base_url=osrm_base_url,
            route_provider=route_provider,
        )

        if distance_km is None:
            logger.warning("Skipping edge after failed routing: %s -> %s", source, target)
            failed_edges.append((source, target))
            continue

        graph.edges[source, target]["weight"] = float(distance_km)
        graph.edges[source, target]["distance_km"] = float(distance_km)
        graph.edges[source, target]["distance_source"] = "osrm"
        logger.info("Updated edge %s -> %s with %.3f km", source, target, distance_km)

    for source, target in failed_edges:
        if graph.has_edge(source, target):
            graph.remove_edge(source, target)

    return graph


def _resolve_distance(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    *,
    cache: DistanceCache | None,
    osrm_base_url: str,
    route_provider: RoadDistanceProvider | None,
) -> float | None:
    if route_provider:
        try:
            distance = route_provider(start_lat, start_lon, end_lat, end_lon)
        except Exception as exc:
            logger.warning("Route provider failed: %s", exc)
            return None
        if distance is None or float(distance) <= 0:
            return None
        return float(distance)

    return get_road_distance(
        start_lat,
        start_lon,
        end_lat,
        end_lon,
        cache=cache,
        osrm_base_url=osrm_base_url,
    )


def _extract_coordinates(
    start: dict[str, Any],
    end: dict[str, Any],
) -> tuple[float, float, float, float] | None:
    try:
        return (
            float(start["lat"]),
            float(start["lon"]),
            float(end["lat"]),
            float(end["lon"]),
        )
    except (KeyError, TypeError, ValueError):
        return None
