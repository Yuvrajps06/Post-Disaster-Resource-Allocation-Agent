from formatter.response_builder import build_response

mock_data = {
    "route": {
        "path": ["Warehouse", "Route B"],
        "risk_score": 0.2
    },
    "allocation": {
        "water": 5000,
        "food": 3000
    },
    "severity": 8.1
}

print(build_response(mock_data))