from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class OceanVariable(str, Enum):
    SST = "sst"
    SALINITY = "salinity"
    CURRENTS = "currents"
    WAVE_HEIGHT = "wave_height"
    WAVE_PERIOD = "wave_period"
    TIDE = "tide"
    SEA_LEVEL = "sea_level"


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
    def validate_region_name(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("region_name cannot be empty")
        return value.strip() if value else value

    def has_location(self) -> bool:
        return (
            self.lat is not None
            and self.lon is not None
        ) or bool(self.region_name)


class TimeRange(BaseModel):
    start: datetime
    end: datetime

    @field_validator("end")
    @classmethod
    def validate_range(cls, value: datetime, info):
        start = info.data.get("start")
        if start is not None and value < start:
            raise ValueError("time_range.end must be >= time_range.start")
        return value


class OceanQuery(BaseModel):
    request_id: UUID
    location: Location
    time_range: TimeRange
    variables: List[OceanVariable] = Field(min_length=1)
    forecast: bool = False

    @field_validator("variables")
    @classmethod
    def remove_duplicates(cls, value: List[OceanVariable]) -> List[OceanVariable]:
        return list(dict.fromkeys(value))


class Anomaly(BaseModel):
    is_anomalous: bool
    z_score: Optional[float] = None
    baseline_period: Optional[str] = None


class OceanObservation(BaseModel):
    variable: OceanVariable
    value: float
    unit: str
    depth_m: Optional[float] = None
    valid_at: datetime
    is_forecast: bool
    anomaly: Optional[Anomaly] = None

    @field_validator("depth_m")
    @classmethod
    def validate_depth(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and value < 0:
            raise ValueError("depth_m cannot be negative")
        return value


class EvidenceItem(BaseModel):
    source: str
    source_type: Literal[
        "observation",
        "model",
        "satellite",
        "calculation",
    ]
    reference: str
    observed_or_published_at: datetime
    retrieved_at: datetime
    passage_or_value: Optional[str | float] = None


class Confidence(BaseModel):
    level: ConfidenceLevel
    score: float = Field(ge=0.0, le=1.0)
    basis: str


class WarningItem(BaseModel):
    code: str
    message: str


class ErrorItem(BaseModel):
    code: str
    message: str
    fatal: bool


class ResolvedLocation(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None
    region_name: Optional[str] = None
    jurisdiction: Optional[str] = None
    maritime_zone: Optional[str] = None


class LocationContext(BaseModel):
    query: Optional[str] = None
    resolved: Optional[ResolvedLocation] = None


class OceanAgentResult(BaseModel):
    agent_id: Literal["ocean"] = "ocean"
    request_id: UUID
    timestamp: datetime
    status: Literal["ok", "partial", "error"]

    location: Optional[LocationContext] = None

    observations: List[OceanObservation] = Field(default_factory=list)

    reasoning: Optional[str] = None

    evidence: List[EvidenceItem] = Field(default_factory=list)

    confidence: Confidence

    warnings: List[WarningItem] = Field(default_factory=list)
    errors: List[ErrorItem] = Field(default_factory=list)
