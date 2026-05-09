def requires_approval(priority):

    return priority in [
        "HIGH",
        "CRITICAL"
    ]


def get_approval_status(priority):

    if requires_approval(priority):
        return "PENDING"

    return "AUTO_APPROVED"