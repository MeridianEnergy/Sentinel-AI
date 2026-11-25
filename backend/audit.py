
from datetime import datetime, timezone
from uuid import uuid4


# Temporary audit storage for development
audit_events = []


def record_event(
    action: str,
    description: str,
    actor: str = "SYSTEM",
    entity_type: str = "SYSTEM",
    entity_id: str = None
):
    event = {
        "event_id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "description": description,
        "actor": actor,
        "entity_type": entity_type,
        "entity_id": entity_id
    }

    audit_events.append(event)

    return event


def get_audit_events():
    return audit_events
