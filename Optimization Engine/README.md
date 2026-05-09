# Post-Disaster Resource Allocation Optimization Engine

Backend optimization and routing engine for post-disaster logistics and resource allocation using real-world road-network distances.

---

# Overview

This project implements a backend graph optimization system designed for disaster-response logistics.

Instead of relying on:

* straight-line geometry
* Euclidean distance
* manually assigned edge weights

the engine dynamically computes:

* real drivable road distances
* realistic transportation costs
* actual route-based graph weights

using:

* OpenStreetMap (OSM)
* OSRM routing backend
* NetworkX graph algorithms

The system is intended for:

* disaster logistics
* relief supply routing
* medical resource allocation
* flood-response planning
* optimization research

---

# Core Features

## Real Road-Based Graph Routing

All graph edge weights are computed dynamically using actual road networks.

Features:

* real drivable routes
* OSRM-based routing
* road-aware edge generation
* dynamic edge-weight updates

---

## NetworkX Integration

Supports:

* Dijkstra shortest path
* A* search
* weighted graph optimization
* routing simulations

All pathfinding operates exclusively on routing-derived road distances.

---

## Modular Backend Architecture

Suggested structure:

```text
Optimization Engine/
│
├── routing_service.py
├── graph_builder.py
├── distance_cache.py
├── test_routing.py
├── test_optimisation.py
├── requirements.txt
└── README.md
```

---

# Node Schema

```json
{
  "id": "warehouse_guwahati",
  "lat": 26.1445,
  "lon": 91.7362
}
```

---

# Edge Schema

```json
{
  "from": "warehouse_guwahati",
  "to": "medical_depot_nagaon"
}
```

Edge weights are dynamically computed from real road distances.

---

# Backend Components

## routing_service.py

Responsible for:

* fetching route data
* querying OSRM
* calculating road distances
* handling routing failures

Key functions:

```python
get_road_distance(...)
fetch_route_data(...)
```

---

## graph_builder.py

Responsible for:

* constructing weighted NetworkX graphs
* updating edge weights
* integrating routing distances

Key functions:

```python
build_weighted_graph(...)
update_edge_weights(...)
```

---

## distance_cache.py

Responsible for:

* caching previously computed routes
* reducing repeated routing requests
* improving performance

---

## test_routing.py

Standalone backend test utility.

Features:

* creates sample graphs
* computes real road distances
* prints computed weights
* validates routing logic
* tests shortest-path algorithms

---

## test_optimisation.py

Optimization testing module.

Features:

* shortest-path simulations
* optimization benchmarking
* disaster-routing scenarios
* graph behavior validation

---

# Routing Engine

Preferred backend:

* OSRM (Open Source Routing Machine)

Data source:

* OpenStreetMap

---

# Installation

## Clone Repository

```bash
git clone <repo-url>
cd "Optimization Engine"
```

---

## Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate:

### Linux/macOS (fish shell)

```bash
source .venv/bin/activate.fish
```

### Bash/Zsh

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Example Dependencies

```text
networkx
requests
aiohttp
numpy
```

---

# Running Tests

## Routing Test

```bash
python test_routing.py
```

This will:

* create sample nodes
* fetch real road distances
* construct weighted graphs
* compute shortest paths

---

## Optimization Test

```bash
python test_optimisation.py
```

---

# Design Goals

The backend is designed to:

* simulate realistic logistics routing
* support disaster-response optimization
* avoid unrealistic straight-line assumptions
* operate independently from frontend rendering

---

# Error Handling

The system supports:

* failed route retries
* invalid-edge skipping
* async-safe routing behavior
* logging of routing failures

---

# Caching

Optional route caching is included to:

* reduce redundant OSRM calls
* improve graph-generation performance
* persist computed edge distances

---

# Important Notes

This repository only contains:

* backend graph logic
* optimization systems
* routing computation

Frontend visualization is handled separately.

---

# Future Improvements

Potential extensions:

* traffic-aware routing
* vehicle constraints
* flood-blocked roads
* multi-agent optimization
* live disaster feeds
* route-risk scoring
* time-aware logistics planning

---

# Expected Outcome

The optimization engine behaves like a real logistics-routing system where:

* all graph edges reflect actual roads
* all weights are dynamically computed
* all pathfinding is road-aware
* optimization results are realistic and usable for disaster-response scenarios
