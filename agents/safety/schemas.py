from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ActivityType(str, Enum):
    SWIMMING = "swimming"
    DIVING = "diving"
    BOATING = "boating"
    FISHING = "fishing"
    GENERAL = "general"


class AdvisoryType(str, Enum):
    STORM = "storm"
    RIP_CURRENT = "rip_current"
    ROGUE_WAVE = "rogue_wave"
    HAB_HEALTH = "hab_health"
    WILDLIFE_HAZARD = "wildlife_hazard"
    OTHER = "other"


class Severity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EXTREME = "extreme"


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Location(BaseModel):
    lat: Optional[float] = Field(default=None, ge=-90, le=90)
    lon: Optional[float] = Field(default=None, ge=-180, le=180)
    region_name: Optional[str] = None

    @field_validator("region_name")
    @classmethod
    def validate_region_name(
        cls,
        value: Optional[str],
    ) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("region_name cannot be empty")

        return value.strip() if value else value

    def has_coordinates(self) -> bool:
        return self.lat is not None and self.lon is not None

    def has_location(self) -> bool:
        return self.has_coordinates() or bool(self.region_name)


class PhysicalContext(BaseModel):
    variable: str
    value: float
    unit: str
    observed_at: datetime
    source: Optional[str] = None


class EcologicalContext(BaseModel):
    hazard_type: str
    value: Optional[str | float] = None
    observed_at: datetime
    source: Optional[str] = None


class SafetyQuery(BaseModel):
    request_id: UUID
    location: Location
    activity_type: ActivityType
    physical_context: Optional[List[PhysicalContext]] = None
    ecological_context: Optional[List[EcologicalContext]] = None
    possible_emergency: bool = False


class EmergencyEscalation(BaseModel):
    required: bool
    instruction: str


class EvidenceItem(BaseModel):
    issuing_authority: str
    issued_at: datetime
    expires_at: Optional[datetime] = None
    review_time: Optional[datetime] = None
    source_reference: str
    source_type: Literal[
        "government_advisory",
        "coast_guard",
        "meteorological_authority",
        "health_advisory",
        "ocean_data",
        "ecosystem_data",
    ]


class SafetyAdvisory(BaseModel):
    advisory_type: AdvisoryType
    severity: Severity
    region: str
    issuing_authority: str
    issued_at: datetime
    expires_at: Optional[datetime] = None
    guidance_text: str
    evidence_index: int


class WarningItem(BaseModel):
    code: str
    message: str


class ErrorItem(BaseModel):
    code: str
    message: str
    fatal: bool = True


class SafetyAgentResult(BaseModel):
    agent_id: Literal["safety"] = "safety"
    request_id: UUID
    timestamp: datetime
    status: Literal["ok", "partial", "error"]

    advisories: List[SafetyAdvisory] = Field(default_factory=list)

    # Required contract fields for the primary/current advisory.
    advisory_type: AdvisoryType
    severity: Severity
    issuing_authority: str
    issued_at: datetime
    expires_at: Optional[datetime] = None
    guidance_text: str

    emergency_escalation: EmergencyEscalation

    evidence: List[EvidenceItem] = Field(default_factory=list)

    confidence_level: ConfidenceLevel
    confidence_score: float = Field(ge=0.0, le=1.0)

    warnings: List[WarningItem] = Field(default_factory=list)
    errors: List[ErrorItem] = Field(default_factory=list)
