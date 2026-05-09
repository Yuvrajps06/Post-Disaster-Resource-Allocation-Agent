"""Graph-based pathfinding utilities for disaster response logistics."""

from __future__ import annotations

from typing import Any

import networkx as nx

from optimization.graph_builder import build_weighted_graph


def build_graph(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], **kwargs: Any) -> nx.Graph:
    """Build a road-weighted NetworkX graph from node and edge dictionaries.

    Args:
        nodes: Node dictionaries with ``id``, ``lat``, and ``lon`` keys.
        edges: Edge dictionaries with ``from`` and ``to`` keys. Any incoming
            ``weight`` values are ignored.
        **kwargs: Optional arguments forwarded to ``build_weighted_graph``.

    Returns:
        A NetworkX graph with latitude/longitude node attributes and OSRM
        road-distance edge weights.
    """
    return build_weighted_graph(nodes, edges, **kwargs)


def get_best_route(
    graph: nx.Graph,
    source: str,
    target: str,
    blocked_roads: list[list[str]],
) -> dict[str, Any]:
    """Find the shortest route while avoiding blocked roads.

    Args:
        graph: Weighted NetworkX graph.
        source: Starting node ID.
        target: Destination node ID.
        blocked_roads: Pairs of node IDs representing blocked roads.

    Returns:
        A route result containing path, total distance, avoided blocked roads,
        and status.
    """
    blocked_roads_avoided = [list(edge) for edge in blocked_roads]
    route_graph = graph.copy()

    for edge in blocked_roads:
        if len(edge) == 2 and route_graph.has_edge(edge[0], edge[1]):
            route_graph.remove_edge(edge[0], edge[1])

    try:
        path = nx.dijkstra_path(route_graph, source, target, weight="weight")
        total_distance = nx.dijkstra_path_length(route_graph, source, target, weight="weight")
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return {
            "path": [],
            "total_distance": 0.0,
            "blocked_roads_avoided": blocked_roads_avoided,
            "status": "no_path_found",
        }

    return {
        "path": path,
        "total_distance": float(total_distance),
        "blocked_roads_avoided": blocked_roads_avoided,
        "status": "success",
    }


def replan_route(
    graph: nx.Graph,
    source: str,
    target: str,
    old_blocked: list[list[str]],
    new_blocked_edge: list[str],
) -> dict[str, Any]:
    """Recalculate a route after a new road blockage appears.

    Args:
        graph: Weighted NetworkX graph.
        source: Starting node ID.
        target: Destination node ID.
        old_blocked: Existing blocked road pairs.
        new_blocked_edge: Newly blocked road pair.

    Returns:
        The same route structure as ``get_best_route`` with ``replanned`` set
        to ``True``.
    """
    updated_blocked = [list(edge) for edge in old_blocked]
    updated_blocked.append(list(new_blocked_edge))

    result = get_best_route(graph, source, target, updated_blocked)
    result["replanned"] = True
    return result
