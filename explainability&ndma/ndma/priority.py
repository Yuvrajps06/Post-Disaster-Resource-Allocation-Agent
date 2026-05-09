def classify_priority(severity):

    if severity >= 8:
        return "CRITICAL"

    elif severity >= 6:
        return "HIGH"

    elif severity >= 4:
        return "MODERATE"

    return "LOW"