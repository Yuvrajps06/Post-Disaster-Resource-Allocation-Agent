# test.py

from llm.explanation import generate_explanation

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

print(generate_explanation(mock_data))