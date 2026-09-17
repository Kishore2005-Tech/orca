from __future__ import annotations

from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class QueryType(str, Enum):
    GEOCODE = "geocode"
    REVERSE_GEOCODE = "reverse_geocode"
    JURISDICTION_LOOKUP = "jurisdiction_lookup"
    CONTAINMENT = "containment"
    DISTANCE = "distance"
    NEAREST_FEATURE = "nearest_feature"


class FeatureType(str, Enum):
    EEZ = "eez"
    TERRITORIAL_SEA = "territorial_sea"
    MPA = "mpa"
    ADMIN_BOUNDARY = "admin_boundary"


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class GeospatialQuery(BaseModel):
    """
    Input contract for the ORCA Geospatial Agent.
    """

    model_config = ConfigDict(extra="forbid")

    request_id: UUID = Field(default_factory=uuid4)
    query_type: QueryType

    place_name: str | None = None

    lat: float | None = Field(default=None, ge=-90.0, le=90.0)
    lon: float | None = Field(default=None, ge=-180.0, le=180.0)

    geometry_ref: str | None = None
    feature_type: FeatureType | None = None

    @field_validator("place_name")
    @classmethod
    def validate_place_name(cls, value: str | None) -> str | None:
        if value is None:
            return value

        cleaned = value.strip()
        return cleaned if cleaned else None


class Coordinate(BaseModel):
    """
    WGS84 geographic coordinate.
    """

    model_config = ConfigDict(extra="forbid")

    lat: float = Field(ge=-90.0, le=90.0)
    lon: float = Field(ge=-180.0, le=180.0)


class EvidenceItem(BaseModel):
    """
    Evidence supporting a spatial/jurisdictional result.
    """

    model_config = ConfigDict(extra="forbid")

    source: str
    dataset: str | None = None
    vintage: str | None = None
    section: str | None = None
    description: str


class GeospatialCandidate(BaseModel):
    """
    A possible geospatial resolution for a place or coordinate.
    """

    model_config = ConfigDict(extra="forbid")

    canonical_name: str
    lat: float = Field(ge=-90.0, le=90.0)
    lon: float = Field(ge=-180.0, le=180.0)

    jurisdiction: str | None = None
    maritime_zone: str | None = None

    boundary_dataset: str
    boundary_dataset_vintage: str

    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM

    evidence: list[EvidenceItem] = Field(default_factory=list)


class SpatialResult(BaseModel):
    """
    Result of a spatial operation.
    """

    model_config = ConfigDict(extra="forbid")

    contains: bool | None = None
    distance_km: float | None = Field(default=None, ge=0.0)
    nearest_feature_name: str | None = None


class ResolutionCheck(BaseModel):
    """
    Describes whether requested spatial detail is compatible
    with the native resolution of the source dataset.
    """

    model_config = ConfigDict(extra="forbid")

    requested_resolution_m: float | None = Field(default=None, gt=0.0)
    native_resolution_m: float | None = Field(default=None, gt=0.0)

    is_valid: bool
    no_subgrid_inference: bool = True

    message: str


class CoverageCheck(BaseModel):
    """
    Dataset coverage and quality information.
    """

    model_config = ConfigDict(extra="forbid")

    is_covered: bool
    is_ocean: bool | None = None
    coastal_contamination: bool = False
    data_gap: bool = False

    message: str


class GeospatialAgentResult(BaseModel):
    """
    Standard result produced by the Geospatial Agent.
    """

    model_config = ConfigDict(extra="forbid")

    status: Literal["success", "error"]

    query_type: QueryType

    candidates: list[GeospatialCandidate] = Field(default_factory=list)

    is_ambiguous: bool = False

    spatial_result: SpatialResult | None = None

    resolution: ResolutionCheck | None = None
    coverage: CoverageCheck | None = None

    confidence: ConfidenceLevel | None = None

    evidence: list[EvidenceItem] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
