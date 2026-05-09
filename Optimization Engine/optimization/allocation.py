"""Resource allocation logic for disaster response incidents."""

from __future__ import annotations

from typing import Any


def allocate_resources(demand: dict[str, float], supply: dict[str, float]) -> dict[str, Any]:
    """Allocate available supply against requested resource demand.

    Args:
        demand: Requested quantities by resource type.
        supply: Available quantities by resource type.

    Returns:
        Dispatch plan, shortfalls, fulfillment percentage, and allocation
        status.
    """
    dispatch_plan: dict[str, float] = {}
    shortfall: dict[str, float] = {}

    total_demand = 0.0
    total_dispatched = 0.0

    for resource, requested in demand.items():
        requested_amount = max(float(requested), 0.0)
        available_amount = max(float(supply.get(resource, 0.0)), 0.0)
        dispatched = min(requested_amount, available_amount)

        dispatch_plan[resource] = _clean_number(dispatched)
        total_demand += requested_amount
        total_dispatched += dispatched

        missing = requested_amount - dispatched
        if missing > 0:
            shortfall[resource] = _clean_number(missing)

    fulfillment_percentage = 100.0
    if total_demand > 0:
        fulfillment_percentage = round((total_dispatched / total_demand) * 100, 1)

    return {
        "dispatch_plan": dispatch_plan,
        "shortfall": shortfall,
        "fulfillment_percentage": fulfillment_percentage,
        "status": "full" if not shortfall else "partial",
    }


def prioritize_allocation(
    incidents: list[dict[str, Any]],
    supply: dict[str, float],
) -> list[dict[str, Any]]:
    """Allocate resources greedily to incidents in severity order.

    Args:
        incidents: Incident dictionaries containing ``severity_score`` and
            ``resources_needed``.
        supply: Available quantities by resource type.

    Returns:
        Allocation result dictionaries in priority order. Each result includes
        incident metadata when available.
    """
    remaining_supply = {resource: max(float(amount), 0.0) for resource, amount in supply.items()}
    prioritized = sorted(
        incidents,
        key=lambda incident: float(incident.get("severity_score", 0.0)),
        reverse=True,
    )
    results: list[dict[str, Any]] = []

    for incident in prioritized:
        allocation = allocate_resources(incident.get("resources_needed", {}), remaining_supply)

        for resource, dispatched in allocation["dispatch_plan"].items():
            remaining_supply[resource] = max(remaining_supply.get(resource, 0.0) - float(dispatched), 0.0)

        allocation["incident_id"] = incident.get("id")
        allocation["severity_score"] = incident.get("severity_score", 0.0)
        results.append(allocation)

    return results


def _clean_number(value: float) -> float | int:
    """Return integers without a decimal part for cleaner output."""
    if value.is_integer():
        return int(value)
    return value
