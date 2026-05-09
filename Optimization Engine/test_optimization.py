"""Print-based tests for the optimization package."""

from pprint import pprint

from optimization import (
    allocate_resources,
    build_graph,
    calculate_severity,
    get_best_route,
    prioritize_allocation,
    replan_route,
    run_optimization,
)


def print_section(title):
    """Print a labeled test section header."""
    print(f"\n=== {title} ===")


def build_sample_graph():
    """Build a sample Assam disaster response road graph."""
    nodes = [
        {"id": "warehouse_guwahati", "lat": 26.1445, "lon": 91.7362},
        {"id": "nh27_junction", "lat": 26.2006, "lon": 91.9801},
        {"id": "barpeta_relief_camp", "lat": 26.3229, "lon": 91.0063},
        {"id": "kaziranga_checkpoint", "lat": 26.5775, "lon": 93.1711},
        {"id": "flood_zone_assam", "lat": 26.4521, "lon": 92.0308},
        {"id": "medical_depot_nagaon", "lat": 26.3480, "lon": 92.6838},
    ]
    edges = [
        {"from": "warehouse_guwahati", "to": "nh27_junction"},
        {"from": "nh27_junction", "to": "flood_zone_assam"},
        {"from": "warehouse_guwahati", "to": "barpeta_relief_camp"},
        {"from": "barpeta_relief_camp", "to": "flood_zone_assam"},
        {"from": "nh27_junction", "to": "medical_depot_nagaon"},
        {"from": "medical_depot_nagaon", "to": "flood_zone_assam"},
        {"from": "medical_depot_nagaon", "to": "kaziranga_checkpoint"},
        {"from": "kaziranga_checkpoint", "to": "flood_zone_assam"},
    ]
    return build_graph(nodes, edges)


def main():
    """Run all optimization tests with clean labeled output."""
    graph = build_sample_graph()

    print_section("1. Sample Graph")
    print(f"Nodes: {list(graph.nodes)}")
    print(f"Edges: {list(graph.edges(data=True))}")

    print_section("2. Best Route With No Blockage")
    route = get_best_route(graph, "warehouse_guwahati", "flood_zone_assam", [])
    pprint(route)

    print_section("3. Best Route With One Blocked Road")
    blocked_route = get_best_route(
        graph,
        "warehouse_guwahati",
        "flood_zone_assam",
        [["nh27_junction", "flood_zone_assam"]],
    )
    pprint(blocked_route)

    print_section("4. Replanned Route After Mid-Demo Block")
    replanned = replan_route(
        graph,
        "warehouse_guwahati",
        "flood_zone_assam",
        [["nh27_junction", "flood_zone_assam"]],
        ["medical_depot_nagaon", "flood_zone_assam"],
    )
    pprint(replanned)

    print_section("5. Resource Allocation With Full Supply")
    full_allocation = allocate_resources(
        {"water": 5000, "food": 3000, "medical": 120},
        {"water": 8000, "food": 5000, "medical": 200},
    )
    pprint(full_allocation)

    print_section("6. Resource Allocation With Partial Supply")
    partial_allocation = allocate_resources(
        {"water": 5000, "food": 3000, "medical": 120},
        {"water": 8000, "food": 2000, "medical": 200},
    )
    pprint(partial_allocation)

    print_section("7. Prioritized Allocation")
    priority_results = prioritize_allocation(
        [
            {
                "id": "incident_barpeta",
                "severity_score": 5.5,
                "resources_needed": {"water": 2000, "food": 1000, "medical": 50},
            },
            {
                "id": "incident_assam_flood",
                "severity_score": 8.7,
                "resources_needed": {"water": 5000, "food": 3000, "medical": 120},
            },
        ],
        {"water": 6000, "food": 3500, "medical": 140},
    )
    pprint(priority_results)

    print_section("8. Severity Priority Levels")
    severity_cases = {
        "LOW": calculate_severity(5000, 2.0, 2.0),
        "MEDIUM": calculate_severity(30000, 5.0, 5.0),
        "HIGH": calculate_severity(70000, 5.0, 6.0),
        "CRITICAL": calculate_severity(120000, 8.0, 8.0),
    }
    pprint(severity_cases)

    print_section("9. End-to-End Optimization")
    incident = {
        "warehouse_node": "warehouse_guwahati",
        "disaster_node": "flood_zone_assam",
        "roads_blocked": [["nh27_junction", "flood_zone_assam"]],
        "resources_needed": {"water": 5000, "food": 3000, "medical": 120},
        "population_affected": 25000,
        "weather_score": 7.0,
        "damage_score": 6.5,
    }
    output = run_optimization(
        incident,
        graph,
        {"water": 8000, "food": 2000, "medical": 200},
    )
    pprint(output)


if __name__ == "__main__":
    main()
