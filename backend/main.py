
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import FastAPI
from backend.schemas import IncidentCreate, ResourceCreate
from backend.audit import record_event, get_audit_events


app = FastAPI(
    title="SENTINEL AI",
    description="AI-assisted Emergency Operations and Coordination Platform",
    version="0.1.0"
)

# Temporary simulated data storage
incidents = []
resources = []


@app.get("/")
def home():
    return {
        "system": "SENTINEL AI",
        "status": "online",
        "message": "SENTINEL AI backend is operational."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "SENTINEL AI"
    }


# INCIDENT MANAGEMENT

@app.post("/incidents")
def create_incident(incident: IncidentCreate):
    record = incident.model_dump(mode="json")

    record["id"] = str(uuid4())
    record["status"] = "Reported"
    record["created_at"] = datetime.now(timezone.utc).isoformat()

    incidents.append(record)

    record_event(
        action="INCIDENT_CREATED",
        description="A new incident was registered.",
        entity_type="INCIDENT",
        entity_id=record["id"]
    )

    return {
        "message": "Incident registered successfully",
        "incident": record
    }


@app.get("/incidents")
def get_incidents():
    return {
        "total": len(incidents),
        "incidents": incidents
    }


# RESOURCE MANAGEMENT

@app.post("/resources")
def create_resource(resource: ResourceCreate):
    record = resource.model_dump(mode="json")
    record["id"] = str(uuid4())

    resources.append(record)

    record_event(
        action="RESOURCE_CREATED",
        description="A new emergency resource was registered.",
        entity_type="RESOURCE",
        entity_id=record["id"]
    )

    return {
        "message": "Resource registered successfully",
        "resource": record
    }


@app.get("/resources")
def get_resources():
    return {
        "total": len(resources),
        "resources": resources
    }


# AUDIT MANAGEMENT

@app.get("/audit")
def get_system_audit():
    events = get_audit_events()

    return {
        "total": len(events),
        "events": events
    }
