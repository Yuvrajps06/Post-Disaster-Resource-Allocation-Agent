"""Standalone backend road-routing checks using OSRM-derived distances."""

from pprint import pprint

from optimization import build_weighted_graph, get_best_route


def print_section(title):
    """Print a labeled test section header."""
    print(f"\n=== {title} ===")


def main():
    """Fetch real road distances, build a graph, and run pathfinding."""
    nodes = [
        {"id": "warehouse_guwahati", "lat": 26.1445, "lon": 91.7362},
        {"id": "nh27_junction", "lat": 26.2006, "lon": 91.9801},
        {"id": "barpeta_relief_camp", "lat": 26.3229, "lon": 91.0063},
        {"id": "flood_zone_assam", "lat": 26.4521, "lon": 92.0308},
        {"id": "medical_depot_nagaon", "lat": 26.3480, "lon": 92.6838},
        {"id": "invalid_missing_coords", "lat": None, "lon": None},
    ]
    edges = [
        {"from": "warehouse_guwahati", "to": "nh27_junction"},
        {"from": "nh27_junction", "to": "flood_zone_assam"},
        {"from": "warehouse_guwahati", "to": "barpeta_relief_camp"},
        {"from": "barpeta_relief_camp", "to": "flood_zone_assam"},
        {"from": "nh27_junction", "to": "medical_depot_nagaon"},
        {"from": "medical_depot_nagaon", "to": "flood_zone_assam"},
        {"from": "warehouse_guwahati", "to": "invalid_missing_coords"},
    ]

    print_section("Build Weighted Graph From OSRM Road Distances")
    graph = build_weighted_graph(nodes, edges)
    if graph.number_of_edges() == 0:
        print("WARNING: No routable edges were returned. Check OSRM/network availability.")
        return

    print_section("Computed Edge Weights")
    for source, target, data in graph.edges(data=True):
        weight = data.get("weight")
        print(f"{source} -> {target}: {weight:.3f} km ({data.get('distance_source')})")
        assert weight is not None and weight > 0
        assert weight < 1000

    print_section("Shortest Path")
    result = get_best_route(graph, "warehouse_guwahati", "flood_zone_assam", [])
    pprint(result)
    if result["status"] == "success":
        assert result["total_distance"] > 0
    else:
        print("WARNING: Graph built, but no connected road path was available for this sample.")

    print_section("Blocked Road Path")
    blocked = get_best_route(
        graph,
        "warehouse_guwahati",
        "flood_zone_assam",
        [["nh27_junction", "flood_zone_assam"]],
    )
    pprint(blocked)


if __name__ == "__main__":
    main()
