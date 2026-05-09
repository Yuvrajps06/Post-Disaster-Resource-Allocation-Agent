"""Severity scoring utilities for disaster incidents."""

from __future__ import annotations

from typing import Any


def calculate_severity(
    population_affected: float,
    weather_score: float,
    damage_score: float,
) -> dict[str, float | str]:
    """Calculate severity score and priority level for an incident.

    Args:
        population_affected: Number of people affected.
        weather_score: Weather severity score.
        damage_score: Infrastructure or asset damage score.

    Returns:
        Severity score capped at 10.0 and mapped priority label.
    """
    severity = (
        (max(float(population_affected), 0.0) / 10000 * 0.5)
        + (max(float(weather_score), 0.0) * 0.3)
        + (max(float(damage_score), 0.0) * 0.2)
    )
    severity = min(severity, 10.0)

    if severity >= 8.0:
        priority = "CRITICAL"
    elif severity >= 6.0:
        priority = "HIGH"
    elif severity >= 4.0:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "severity_score": round(severity, 2),
        "priority": priority,
    }


def score_from_incident(incident: dict[str, Any]) -> dict[str, float | str]:
    """Calculate severity score from an incident dictionary.

    Args:
        incident: Incident with ``population_affected``, ``weather_score``,
            and ``damage_score`` keys.

    Returns:
        Severity score and priority level.
    """
    return calculate_severity(
        incident.get("population_affected", 0.0),
        incident.get("weather_score", 0.0),
        incident.get("damage_score", 0.0),
    )
