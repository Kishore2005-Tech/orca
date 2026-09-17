from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EcosystemIndicator(str, Enum):
    """Supported ecosystem indicators."""

    BLEACHING = "bleaching"
    HAB = "hab"
    BIODIVERSITY = "biodiversity"
    INVASIVE_SPECIES = "invasive_species"
    CONSERVATION_STATUS = "conservation_status"
    CHLOROPHYLL = "chlorophyll"
    MHW = "mhw"
    FRONT = "front"
    UPWELLING = "upwelling"


class Location(BaseModel):
    """Geographic query location."""

    model_config = ConfigDict(extra="forbid")

    lat: float | None = Field(default=None, ge=-90.0, le=90.0)
    lon: float | None = Field(default=None, ge=-180.0, le=180.0)
    region_name: str | None = None
    jurisdiction: str | None = None
    maritime_zone: str | None = None

    @field_validator("region_name")
    @classmethod
    def validate_region_name(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("region_name cannot be empty")
        return value


class TimeRange(BaseModel):
    """Inclusive temporal scope for an ecosystem query."""

    model_config = ConfigDict(extra="forbid")

    start: datetime
    end: datetime

    @field_validator("start", "end")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamps must be timezone-aware")
        return value.astimezone(timezone.utc)

    def validate_order(self) -> None:
        if self.start > self.end:
            raise ValueError("time_range.start must not be after time_range.end")


class PhysicalObservation(BaseModel):
    """
    Physical observation handed to the Ecosystem Agent by the Coordinator.

    It is contextual evidence only. The Ecosystem Agent must not convert it
    into an ecological fact or causal claim.
    """

    model_config = ConfigDict(extra="allow")

    parameter: str
    value: float
    unit: str
    observed_at: datetime
    source: str | None = None


class EcosystemAgentInput(BaseModel):
    """Input contract for the Ecosystem Agent."""

    model_config = ConfigDict(extra="forbid")

    request_id: UUID
    location: Location
    taxon: str | None = None
    indicator: EcosystemIndicator | None = None
    time_range: TimeRange
    physical_context: list[PhysicalObservation] | None = None

    @field_validator("taxon")
    @classmethod
    def normalize_taxon(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = " ".join(value.split())

        if not normalized:
            raise ValueError("taxon cannot be empty")

        return normalized


class EvidenceItem(BaseModel):
    """Shared evidence item required by the ORCA agent contract."""

    model_config = ConfigDict(extra="forbid")

    source: str
    source_type: Literal[
        "observation",
        "model",
        "satellite",
        "registry",
        "advisory_feed",
        "document",
        "calculation",
    ]
    reference: str
    observed_or_published_at: datetime
    retrieved_at: datetime
    passage_or_value: str | float | int | None = None

    @field_validator("observed_or_published_at", "retrieved_at")
    @classmethod
    def normalize_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("evidence timestamps must be timezone-aware")
        return value.astimezone(timezone.utc)


class Confidence(BaseModel):
    """Deterministic confidence information."""

    model_config = ConfigDict(extra="forbid")

    level: Literal["high", "medium", "low"]
    score: float = Field(ge=0.0, le=1.0)
    basis: str


class WarningItem(BaseModel):
    """Non-fatal warning."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str


class ErrorItem(BaseModel):
    """Structured agent error."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    fatal: bool


class CorrelationFlag(BaseModel):
    """
    Relationship between an ecological observation and physical context.

    Causation is deliberately impossible through this model.
    """

    model_config = ConfigDict(extra="forbid")

    related_physical_event: str | None = None
    is_causal_claim: Literal[False] = False
    note: str


class EcosystemObservation(BaseModel):
    """One structured ecosystem finding."""

    model_config = ConfigDict(extra="forbid")

    indicator: EcosystemIndicator
    taxon: str | None = None
    status_value: str
    observed_at: datetime
    monitoring_program: str
    value: float | None = None
    unit: str | None = None
    interpretation: str | None = None
    correlation_flag: CorrelationFlag | None = None


class EcosystemAgentResult(BaseModel):
    """
    Standard ORCA response envelope specialized for Ecosystem observations.
    """

    model_config = ConfigDict(extra="forbid")

    agent_id: Literal["ecosystem"] = "ecosystem"
    request_id: UUID
    timestamp: datetime
    status: Literal["ok", "partial", "error"]

    location: dict[str, Any] | None = None
    observations: list[EcosystemObservation] = Field(default_factory=list)
    reasoning: str | None = None
    evidence: list[EvidenceItem] = Field(default_factory=list)
    confidence: Confidence
    warnings: list[WarningItem] = Field(default_factory=list)
    errors: list[ErrorItem] = Field(default_factory=list)

    @field_validator("timestamp")
    @classmethod
    def normalize_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        return value.astimezone(timezone.utc)

    @field_validator("errors")
    @classmethod
    def validate_error_status(
        cls,
        value: list[ErrorItem],
    ) -> list[ErrorItem]:
        return value
