from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ActivityType(str, Enum):
    """Fishing activity classification."""

    RECREATIONAL = "recreational"
    COMMERCIAL = "commercial"


class Location(BaseModel):
    """Resolved or user-supplied fishing location."""

    model_config = ConfigDict(extra="forbid")

    lat: float | None = Field(default=None, ge=-90.0, le=90.0)
    lon: float | None = Field(default=None, ge=-180.0, le=180.0)
    region_name: str | None = None
    jurisdiction: str | None = None

    @field_validator("region_name", "jurisdiction")
    @classmethod
    def validate_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("text fields cannot be empty")
        return value


class FishingQuery(BaseModel):
    """
    Fisheries Agent request.

    This follows the Fisheries Agent contract while allowing PFZ-specific
    processing through the supplied environmental observations.
    """

    model_config = ConfigDict(extra="forbid")

    request_id: UUID
    location: Location
    species: str | None = None
    gear_type: str | None = None
    activity_type: ActivityType
    date: datetime

    @field_validator("date")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("date must be timezone-aware")
        return value.astimezone(timezone.utc)

    @field_validator("species", "gear_type")
    @classmethod
    def normalize_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = " ".join(value.split())

        if not value:
            raise ValueError("text field cannot be empty")

        return value


class OceanFishingInputs(BaseModel):
    """
    Environmental observations required for PFZ/habitat analysis.
    """

    model_config = ConfigDict(extra="forbid")

    sst_celsius: float = Field(
        ge=-5.0,
        le=50.0,
    )
    chlorophyll_mg_m3: float = Field(
        ge=0.0,
    )
    sst_gradient_c_per_km: float = Field(
        ge=0.0,
    )
    thermal_front_detected: bool = False

    current_speed_m_s: float = Field(
        default=0.0,
        ge=0.0,
    )
    current_direction_deg: float = Field(
        default=0.0,
        ge=0.0,
        lt=360.0,
    )

    wind_speed_m_s: float = Field(
        default=0.0,
        ge=0.0,
    )
    wind_direction_deg: float = Field(
        default=0.0,
        ge=0.0,
        lt=360.0,
    )

    observed_at: datetime | None = None
    source: str = "ORCA supplied ocean dataset"

    @field_validator("observed_at")
    @classmethod
    def validate_observation_time(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")

        if value is not None:
            return value.astimezone(timezone.utc)

        return value

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("source cannot be empty")

        return value


class BathymetryInput(BaseModel):
    """Bathymetry information used for habitat/depth validation."""

    model_config = ConfigDict(extra="forbid")

    depth_m: float = Field(
        ge=0.0,
    )
    min_depth_m: float = Field(
        default=0.0,
        ge=0.0,
    )
    max_depth_m: float | None = Field(
        default=None,
        ge=0.0,
    )

    @field_validator("max_depth_m")
    @classmethod
    def validate_depth_range(
        cls,
        value: float | None,
        info,
    ) -> float | None:
        min_depth = info.data.get("min_depth_m", 0.0)

        if value is not None and value < min_depth:
            raise ValueError(
                "max_depth_m must be greater than or equal to min_depth_m"
            )

        return value


class DriftInput(BaseModel):
    """Wind/current inputs for PFZ displacement estimation."""

    model_config = ConfigDict(extra="forbid")

    hours: float = Field(
        gt=0.0,
        le=168.0,
    )
    current_speed_m_s: float = Field(
        ge=0.0,
    )
    current_direction_deg: float = Field(
        ge=0.0,
        lt=360.0,
    )
    wind_speed_m_s: float = Field(
        ge=0.0,
    )
    wind_direction_deg: float = Field(
        ge=0.0,
        lt=360.0,
    )


class EvidenceItem(BaseModel):
    """Traceable evidence attached to a fisheries result."""

    model_config = ConfigDict(extra="forbid")

    source: str
    source_type: Literal[
        "observation",
        "satellite",
        "model",
        "calculation",
        "regulatory",
        "document",
    ]
    reference: str
    observed_or_published_at: datetime
    retrieved_at: datetime
    value: str | float | int | dict[str, Any] | None = None

    @field_validator(
        "observed_or_published_at",
        "retrieved_at",
    )
    @classmethod
    def normalize_timestamp(
        cls,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None:
            raise ValueError("evidence timestamps must be timezone-aware")

        return value.astimezone(timezone.utc)


class HabitatAssessment(BaseModel):
    """Species-independent habitat suitability assessment."""

    model_config = ConfigDict(extra="forbid")

    score: int = Field(
        ge=0,
        le=100,
    )
    category: Literal[
        "high",
        "moderate",
        "low",
    ]
    depth_valid: bool
    environmental_factors: list[str] = Field(
        default_factory=list,
    )
    limitations: list[str] = Field(
        default_factory=list,
    )


class PFZPoint(BaseModel):
    """A candidate Potential Fishing Zone location."""

    model_config = ConfigDict(extra="forbid")

    lat: float = Field(
        ge=-90.0,
        le=90.0,
    )
    lon: float = Field(
        ge=-180.0,
        le=180.0,
    )
    score: int = Field(
        ge=0,
        le=100,
    )
    depth_m: float = Field(
        ge=0.0,
    )


class PFZDrift(BaseModel):
    """Estimated displacement of a PFZ."""

    model_config = ConfigDict(extra="forbid")

    displacement_km: float = Field(
        ge=0.0,
    )
    displacement_nm: float = Field(
        ge=0.0,
    )
    direction_deg: float = Field(
        ge=0.0,
        lt=360.0,
    )
    estimated_hours: float = Field(
        gt=0.0,
    )


class FisheriesAgentResult(BaseModel):
    """Structured ORCA Fisheries Agent result."""

    model_config = ConfigDict(extra="forbid")

    agent_id: Literal["fisheries"] = "fisheries"
    request_id: UUID
    timestamp: datetime
    status: Literal[
        "ok",
        "partial",
        "error",
    ]

    location: Location

    pfz: PFZPoint | None = None
    habitat: HabitatAssessment | None = None
    drift: PFZDrift | None = None

    species: str | None = None
    gear_type: str | None = None

    interpretation: str | None = None
    evidence: list[EvidenceItem] = Field(
        default_factory=list,
    )

    warnings: list[str] = Field(
        default_factory=list,
    )
    errors: list[str] = Field(
        default_factory=list,
    )

    is_informational_only: Literal[True] = True

    @field_validator("timestamp")
    @classmethod
    def normalize_timestamp(
        cls,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")

        return value.astimezone(timezone.utc)
