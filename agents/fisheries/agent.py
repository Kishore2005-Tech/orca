from __future__ import annotations

from datetime import datetime, timezone
from typing import Sequence

from .prompts import (
    DRIFT_ANALYSIS_PROMPT,
    FISHERIES_SYSTEM_PROMPT,
    HABITAT_ANALYSIS_PROMPT,
    PFZ_ANALYSIS_PROMPT,
)
from .schemas import (
    BathymetryInput,
    EvidenceItem,
    FisheriesAgentResult,
    FishingQuery,
    HabitatAssessment,
    OceanFishingInputs,
    PFZDrift,
    PFZPoint,
)
from .tools import (
    Bathymetry,
    PFZInputs,
    get_habitat_suitability,
    get_pfz,
    get_pfz_drift,
    project_pfz_coordinate,
)


class FisheriesAgent:
    """
    ORCA Fisheries and PFZ Intelligence Agent.

    This agent produces environmental fishing indicators, not guarantees.
    """

    agent_id = "fisheries"
    agent_name = "Fisheries & PFZ Intelligence Agent"

    def __init__(
        self,
        minimum_depth_m: float = 0.0,
        maximum_depth_m: float | None = None,
    ) -> None:
        if minimum_depth_m < 0:
            raise ValueError(
                "minimum_depth_m cannot be negative"
            )

        if (
            maximum_depth_m is not None
            and maximum_depth_m < minimum_depth_m
        ):
            raise ValueError(
                "maximum_depth_m must be >= minimum_depth_m"
            )

        self.minimum_depth_m = minimum_depth_m
        self.maximum_depth_m = maximum_depth_m

    def run(
        self,
        query: FishingQuery,
        *,
        ocean: OceanFishingInputs | None = None,
        bathymetry: BathymetryInput | None = None,
        drift_hours: float | None = None,
    ) -> FisheriesAgentResult:
        """
        Execute Fisheries Agent analysis.

        Required for PFZ processing:
            ocean
            bathymetry

        Drift is calculated when drift_hours is supplied and the ocean input
        contains current/wind information.
        """

        timestamp = datetime.now(timezone.utc)

        if ocean is None:
            return self._error_result(
                query,
                "ORCA_ERR_NO_DATA",
                "Ocean observations are required for PFZ analysis.",
                timestamp,
            )

        if bathymetry is None:
            return self._error_result(
                query,
                "ORCA_ERR_NO_DATA",
                "Bathymetry is required for habitat validation.",
                timestamp,
            )

        try:
            pfz_result = get_pfz(
                PFZInputs(
                    sst_celsius=ocean.sst_celsius,
                    chlorophyll_mg_m3=ocean.chlorophyll_mg_m3,
                    sst_gradient_c_per_km=ocean.sst_gradient_c_per_km,
                    thermal_front_detected=ocean.thermal_front_detected,
                )
            )

            habitat_result = get_habitat_suitability(
                pfz_result,
                Bathymetry(
                    depth_m=bathymetry.depth_m,
                    minimum_depth_m=(
                        bathymetry.min_depth_m
                    ),
                    maximum_depth_m=(
                        bathymetry.max_depth_m
                    ),
                ),
            )

            pfz = self._build_pfz(
                query,
                ocean,
                bathymetry,
                habitat_result,
            )

            drift = None

            if drift_hours is not None:
                drift = self._build_drift(
                    query,
                    ocean,
                    drift_hours,
                    timestamp,
                )

            evidence = self._build_evidence(
                query=query,
                ocean=ocean,
                timestamp=timestamp,
                drift=drift,
            )

            warnings = list(habitat_result.limitations)

            if not pfz_result.detected:
                warnings.append(
                    "The supplied environmental conditions did not meet "
                    "the configured PFZ indicator threshold."
                )

            interpretation = self._interpretation(
                pfz_score=habitat_result.score,
                habitat_category=habitat_result.category,
                depth_valid=habitat_result.depth_valid,
                drift=drift,
            )

            return FisheriesAgentResult(
                request_id=query.request_id,
                timestamp=timestamp,
                status="ok",
                location=query.location,
                pfz=pfz,
                habitat=HabitatAssessment(
                    score=habitat_result.score,
                    category=habitat_result.category,
                    depth_valid=habitat_result.depth_valid,
                    environmental_factors=list(
                        habitat_result.reasons
                    ),
                    limitations=list(
                        habitat_result.limitations
                    ),
                ),
                drift=drift,
                species=query.species,
                gear_type=query.gear_type,
                interpretation=interpretation,
                evidence=evidence,
                warnings=warnings,
                errors=[],
                is_informational_only=True,
            )

        except ValueError as exc:
            return self._error_result(
                query,
                "ORCA_ERR_SCHEMA_VALIDATION",
                str(exc),
                timestamp,
            )

    def _build_pfz(
        self,
        query: FishingQuery,
        ocean: OceanFishingInputs,
        bathymetry: BathymetryInput,
        habitat,
    ) -> PFZPoint:
        lat = query.location.lat

        lon = query.location.lon

        if lat is None or lon is None:
            raise ValueError(
                "latitude and longitude are required to return a PFZ point"
            )

        return PFZPoint(
            lat=lat,
            lon=lon,
            score=habitat.score,
            depth_m=bathymetry.depth_m,
        )

    def _build_drift(
        self,
        query: FishingQuery,
        ocean: OceanFishingInputs,
        drift_hours: float,
        timestamp: datetime,
    ) -> PFZDrift:
        drift_result = get_pfz_drift(
            current_speed_m_s=ocean.current_speed_m_s,
            current_direction_deg=ocean.current_direction_deg,
            wind_speed_m_s=ocean.wind_speed_m_s,
            wind_direction_deg=ocean.wind_direction_deg,
            hours=drift_hours,
        )

        return PFZDrift(
            displacement_km=drift_result.displacement_km,
            displacement_nm=drift_result.displacement_nm,
            direction_deg=drift_result.direction_deg,
            estimated_hours=drift_hours,
        )

    def project_drifted_location(
        self,
        query: FishingQuery,
        drift: PFZDrift,
    ) -> tuple[float, float]:
        """
        Return an approximate future PFZ coordinate.

        This is intentionally exposed separately so callers cannot mistake
        the ordinary PFZ coordinate for a forecasted navigation position.
        """

        if query.location.lat is None or query.location.lon is None:
            raise ValueError(
                "latitude and longitude are required"
            )

        from .tools import DriftResult

        result = DriftResult(
            displacement_km=drift.displacement_km,
            displacement_nm=drift.displacement_nm,
            direction_deg=drift.direction_deg,
        )

        return project_pfz_coordinate(
            latitude=query.location.lat,
            longitude=query.location.lon,
            drift=result,
        )

    def _build_evidence(
        self,
        query: FishingQuery,
        ocean: OceanFishingInputs,
        timestamp: datetime,
        drift: PFZDrift | None,
    ) -> list[EvidenceItem]:
        observed_at = ocean.observed_at or timestamp

        evidence = [
            EvidenceItem(
                source=ocean.source,
                source_type="observation",
                reference="ORCA-FISH-OCEAN-INPUT",
                observed_or_published_at=observed_at,
                retrieved_at=timestamp,
                value={
                    "sst_celsius": ocean.sst_celsius,
                    "chlorophyll_mg_m3": (
                        ocean.chlorophyll_mg_m3
                    ),
                    "sst_gradient_c_per_km": (
                        ocean.sst_gradient_c_per_km
                    ),
                    "thermal_front_detected": (
                        ocean.thermal_front_detected
                    ),
                },
            )
        ]

        if drift is not None:
            evidence.append(
                EvidenceItem(
                    source=ocean.source,
                    source_type="calculation",
                    reference="ORCA-FISH-PFZ-DRIFT",
                    observed_or_published_at=observed_at,
                    retrieved_at=timestamp,
                    value={
                        "displacement_km": (
                            drift.displacement_km
                        ),
                        "direction_deg": (
                            drift.direction_deg
                        ),
                        "hours": drift.estimated_hours,
                    },
                )
            )

        return evidence

    def _interpretation(
        self,
        *,
        pfz_score: int,
        habitat_category: str,
        depth_valid: bool,
        drift: PFZDrift | None,
    ) -> str:
        parts = [
            PFZ_ANALYSIS_PROMPT.strip(),
            HABITAT_ANALYSIS_PROMPT.strip(),
        ]

        parts.append(
            f"Current environmental indicator score: {pfz_score}/100."
        )

        parts.append(
            f"Habitat suitability category: {habitat_category}."
        )

        parts.append(
            "Bathymetry is within the supplied range."
            if depth_valid
            else "Bathymetry is outside the supplied range."
        )

        if drift is not None:
            parts.extend(
                [
                    DRIFT_ANALYSIS_PROMPT.strip(),
                    (
                        f"Estimated PFZ displacement over "
                        f"{drift.estimated_hours:g} hours: "
                        f"{drift.displacement_km:.2f} km."
                    ),
                ]
            )

        parts.append(
            "This result is informational and does not guarantee "
            "fish presence, abundance, or catch."
        )

        return "\n\n".join(parts)

    def _error_result(
        self,
        query: FishingQuery,
        code: str,
        message: str,
        timestamp: datetime,
    ) -> FisheriesAgentResult:
        return FisheriesAgentResult(
            request_id=query.request_id,
            timestamp=timestamp,
            status="error",
            location=query.location,
            pfz=None,
            habitat=None,
            drift=None,
            species=query.species,
            gear_type=query.gear_type,
            interpretation=None,
            evidence=[],
            warnings=[],
            errors=[
                f"{code}: {message}"
            ],
            is_informational_only=True,
        )
