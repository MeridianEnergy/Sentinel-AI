
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


# INCIDENT PRIORITIES
class IncidentPriority(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


# INCIDENT STATUSES
class IncidentStatus(str, Enum):
    REPORTED = "Reported"
    AWAITING_DISPATCH = "Awaiting Dispatch"
    DISPATCHED = "Dispatched"
    ON_SCENE = "On Scene"
    CONTAINED = "Contained"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


# RESOURCE STATUSES
class ResourceStatus(str, Enum):
    AVAILABLE = "Available"
    ASSIGNED = "Assigned"
    DISPATCHED = "Dispatched"
    ON_SCENE = "On Scene"
    RETURNING = "Returning"
    OUT_OF_SERVICE = "Out of Service"


# INCIDENT INFORMATION
class IncidentCreate(BaseModel):
    incident_type: str
    priority: IncidentPriority
    address: str
    sector: str
    description: str
    hazards: list[str] = Field(default_factory=list)


# RESOURCE INFORMATION
class ResourceCreate(BaseModel):
    callsign: str
    resource_type: str
    crew_size: int = Field(ge=1)
    status: ResourceStatus = ResourceStatus.AVAILABLE
