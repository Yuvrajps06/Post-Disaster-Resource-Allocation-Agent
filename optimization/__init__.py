"""Optimization Engine package for disaster management decision support."""

from __future__ import annotations

from typing import Any

import networkx as nx

from optimization.allocation import allocate_resources, prioritize_allocation
from optimization.graph_builder import build_weighted_graph, update_edge_weights
from optimization.routing import build_graph, get_best_route, replan_route
from optimization.routing_service import fetch_route_data, get_road_distance
from optimization.severity import calculate_severity, score_from_incident

__all__ = [
    "allocate_resources",
    "build_graph",
    "build_weighted_graph",
    "calculate_severity",
    "fetch_route_data",
    "get_best_route",
    "get_road_distance",
    "prioritize_allocation",
    "replan_route",
    "run_optimization",
    "score_from_incident",
    "update_edge_weights",
]


def run_optimization(incident: dict[str, Any], graph: nx.Graph, supply: dict[str, float]) -> dict[str, Any]:
    """Run routing, allocation, and severity scoring for one incident.

    Args:
        incident: Incident details including source/destination nodes, blocked
            roads, resource demand, and severity inputs.
        graph: Weighted NetworkX road graph.
        supply: Available quantities by resource type.

    Returns:
        Combined optimization result for backend use.
    """
    route = get_best_route(
        graph,
        incident.get("warehouse_node"),
        incident.get("disaster_node"),
        incident.get("roads_blocked", []),
    )
    allocation = allocate_resources(incident.get("resources_needed", {}), supply)
    severity = score_from_incident(incident)

    requires_approval = severity["priority"] == "CRITICAL" or allocation["status"] == "partial"

    return {
        "route": route,
        "allocation": allocation,
        "severity": severity,
        "requires_approval": requires_approval,
    }
