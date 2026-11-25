
# SENTINEL AI - THREAT ASSESSMENT ENGINE

THREAT_LEVELS = {
    "GREEN": "Normal Operations",
    "YELLOW": "Elevated Activity",
    "ORANGE": "Major Incident Activity",
    "RED": "Multiple Critical Incidents",
    "BLACK": "Disaster Mode"
}


def assess_threat(active_incidents, critical_incidents):

    active = len(active_incidents)
    critical = len(critical_incidents)

    if critical >= 3 or active >= 10:
        level = "RED"
        reason = "Multiple critical incidents or high incident volume."

    elif critical >= 1 or active >= 6:
        level = "ORANGE"
        reason = "Critical incident detected or major operational activity."

    elif active >= 3:
        level = "YELLOW"
        reason = "Elevated incident activity detected."

    else:
        level = "GREEN"
        reason = "Normal simulated operational activity."

    return {
        "level": level,
        "description": THREAT_LEVELS[level],
        "reason": reason,
        "active_incidents": active,
        "critical_incidents": critical,
        "environment": "SIMULATION"
    }
