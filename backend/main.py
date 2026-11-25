
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.schemas import IncidentCreate, ResourceCreate
from backend.audit import record_event, get_audit_events


app = FastAPI(
    title="SENTINEL AI",
    description="AI-assisted Emergency Operations and Coordination Platform",
    version="0.1.0"
)

incidents = []
resources = []


class IncidentStatusUpdate(BaseModel):
    status: str


VALID_STATUSES = [
    "Reported",
    "Awaiting Dispatch",
    "Dispatched",
    "On Scene",
    "Contained",
    "Resolved",
    "Closed"
]


@app.get("/")
def home():
    return {
        "system": "SENTINEL AI",
        "status": "online"
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


@app.patch("/incidents/{incident_id}/status")
def update_incident_status(
    incident_id: str,
    update: IncidentStatusUpdate
):
    if update.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid incident status."
        )

    for incident in incidents:
        if incident["id"] == incident_id:
            old_status = incident["status"]

            incident["status"] = update.status
            incident["updated_at"] = datetime.now(
                timezone.utc
            ).isoformat()

            record_event(
                action="INCIDENT_STATUS_UPDATED",
                description=f"Status changed from {old_status} to {update.status}.",
                entity_type="INCIDENT",
                entity_id=incident_id
            )

            return {
                "message": "Incident status updated.",
                "incident": incident
            }

    raise HTTPException(
        status_code=404,
        detail="Incident not found."
    )


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

# RESOURCE ASSIGNMENT

class ResourceAssignment(BaseModel):
    resource_id: str


@app.post("/incidents/{incident_id}/assign-resource")
def assign_resource(
    incident_id: str,
    assignment: ResourceAssignment
):
    incident = next(
        (item for item in incidents if item["id"] == incident_id),
        None
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found."
        )

    resource = next(
        (
            item for item in resources
            if item["id"] == assignment.resource_id
        ),
        None
    )

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found."
        )

    if resource["status"] != "Available":
        raise HTTPException(
            status_code=400,
            detail="Resource is not available for assignment."
        )

    if "assigned_resources" not in incident:
        incident["assigned_resources"] = []

    resource["status"] = "Assigned"
    resource["assigned_incident_id"] = incident_id

    incident["assigned_resources"].append(resource["id"])

    record_event(
        action="RESOURCE_ASSIGNED",
        description="A resource was assigned to an incident.",
        entity_type="INCIDENT",
        entity_id=incident_id
    )

    return {
        "message": "Resource assigned successfully.",
        "incident_id": incident_id,
        "resource": resource
    }

# OPERATIONAL DASHBOARD

@app.get("/dashboard")
def get_dashboard():

    active_incidents = [
        incident for incident in incidents
        if incident["status"] not in ["Resolved", "Closed"]
    ]

    critical_incidents = [
        incident for incident in active_incidents
        if incident["priority"] == "Critical"
    ]

    awaiting_dispatch = [
        incident for incident in active_incidents
        if incident["status"] == "Awaiting Dispatch"
    ]

    available_resources = [
        resource for resource in resources
        if resource["status"] == "Available"
    ]

    dispatched_resources = [
        resource for resource in resources
        if resource["status"] == "Dispatched"
    ]

    on_scene_resources = [
        resource for resource in resources
        if resource["status"] == "On Scene"
    ]

    total_resources = len(resources)

    if total_resources > 0:
        readiness = round(
            len(available_resources) / total_resources * 100,
            1
        )
    else:
        readiness = 0

    return {
        "system": "SENTINEL AI",
        "environment": "SIMULATION",
        "incidents": {
            "active": len(active_incidents),
            "critical": len(critical_incidents),
            "awaiting_dispatch": len(awaiting_dispatch)
        },
        "resources": {
            "total": total_resources,
            "available": len(available_resources),
            "dispatched": len(dispatched_resources),
            "on_scene": len(on_scene_resources)
        },
        "readiness_percentage": readiness
    }

