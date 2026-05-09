from llm.explanation import generate_explanation
from ndma.priority import classify_priority


from datetime import datetime
from ndma.approval import (
    requires_approval,
    get_approval_status
)

def build_response(data):

    explanation = generate_explanation(data)

    priority = classify_priority(
        data["severity"]
    )

    return {

        "recommendation":
            "Dispatch optimized resources via selected route.",

        "explanation":
            explanation,

        "priority":
            priority,

        "requires_approval":
            requires_approval(priority),

        "severity":
            data["severity"],

        "generated_at":
            datetime.utcnow().isoformat(),
        "approval_status":
            get_approval_status(priority)
            
    }