from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional
from uuid import UUID

from .prompts import (
    ANOMALY_PROMPT,
    FORECAST_PROMPT,
    GRADIENT_PROMPT,
    OBSERVATION_PROMPT,
    OCEAN_SYSTEM_PROMPT,
)
from .schemas import (
    Anomaly,
    Confidence,
    ConfidenceLevel,
    EvidenceItem,
    ErrorItem,
    LocationContext,
    OceanAgentResult,
    OceanObservation,
    OceanQuery,
    OceanVariable,
    ResolvedLocation,
    WarningItem,
)
from .tools import (
    OceanDataPoint,
    anomaly_from_z_score,
    calculate_sst_gradient,
    calculate_z_score,
    choose_confidence,
    detect_thermal_front,
    is_stale_observation,
    validate_data_point,
)


class OceanAgent:
    """
    ORCA Ocean Agent.

    Responsible for physical oceanographic data processing only.

    The agent intentionally does not fetch live external APIs here.
    The Coordinator/data pipeline should supply validated source data.
    """

    def __init__(
        self,
        freshness_threshold_hours: float = 24.0,
        thermal_front_threshold_c_per_km: float = 0.2,
    ):
        self.agent_id = "ocean"
        self.agent_name = "Ocean Intelligence Agent"

        self.freshness_threshold_hours = freshness_threshold_hours
        self.thermal_front_threshold_c_per_km = (
            thermal_front_threshold_c_per_km
        )

    def run(
        self,
        query: OceanQuery,
        data_points: Optional[Iterable[OceanDataPoint]] = None,
        *,
        resolved_location: Optional[ResolvedLocation] = None,
        now: Optional[datetime] = None,
    ) -> OceanAgentResult:
        """
        Main Ocean Agent entry point.

        `data_points` are expected to come from the ORCA data pipeline,
        model clients, satellite products, buoys, or tide services.
        """
        current_time = now or datetime.now(timezone.utc)

        location_check = self._validate_location(query)

        if location_check is not None:
            return self._error_result(
                query,
                location_check[0],
                location_check[1],
                resolved_location=resolved_location,
                timestamp=current_time,
            )

        supplied_points = list(data_points or [])

        if not supplied_points:
            return self._error_result(
                query,
                "ORCA_ERR_NO_DATA",
                "No ocean data was supplied for the requested scope.",
                resolved_location=resolved_location,
                timestamp=current_time,
            )

        observations: list[OceanObservation] = []
        evidence: list[EvidenceItem] = []
        warnings: list[WarningItem] = []
        errors: list[ErrorItem] = []

        requested_variables = set(query.variables)

        for point in supplied_points:
            if point.variable not in requested_variables:
                continue

            validation = validate_data_point(
                point,
                now=current_time,
            )

            if not validation.valid:
                errors.append(
                    ErrorItem(
                        code="ORCA_ERR_SCHEMA_VALIDATION",
                        message=(
                            f"{point.variable.value}: "
                            f"{validation.message}"
                        ),
                        fatal=False,
                    )
                )
                continue

            stale = (
                not point.is_forecast
                and is_stale_observation(
                    point.valid_at,
                    max_age_hours=self.freshness_threshold_hours,
                    now=current_time,
                )
            )

            if stale:
                warnings.append(
                    WarningItem(
                        code="ORCA_ERR_STALE_DATA",
                        message=(
                            f"{point.variable.value} data from "
                            f"{point.valid_at.isoformat()} exceeds the "
                            f"{self.freshness_threshold_hours:g}-hour "
                            "freshness threshold."
                        ),
                    )
                )

            anomaly = None

            if point.anomaly_z_score is not None:
                anomaly = Anomaly(
                    is_anomalous=abs(point.anomaly_z_score) >= 2.0,
                    z_score=point.anomaly_z_score,
                    baseline_period=point.baseline_period,
                )

            observations.append(
                OceanObservation(
                    variable=point.variable,
                    value=point.value,
                    unit=point.unit,
                    depth_m=point.depth_m,
                    valid_at=point.valid_at,
                    is_forecast=point.is_forecast,
                    anomaly=anomaly,
                )
            )

            evidence.append(
                EvidenceItem(
                    source=point.source,
                    source_type=point.source_type,
                    reference=point.reference,
                    observed_or_published_at=point.valid_at,
                    retrieved_at=current_time,
                    passage_or_value=point.value,
                )
            )

        if not observations:
            return self._error_result(
                query,
                "ORCA_ERR_NO_DATA",
                "No valid ocean observations remained after validation.",
                resolved_location=resolved_location,
                timestamp=current_time,
                warnings=warnings,
                errors=errors,
            )

        status = "ok"

        if errors or warnings:
            status = "partial"

        confidence_level, confidence_score, confidence_basis = (
            self._calculate_confidence(
                supplied_points=supplied_points,
                accepted_observations=observations,
                current_time=current_time,
            )
        )

        reasoning = self._build_reasoning(
            observations=observations,
            warnings=warnings,
            query=query,
        )

        return OceanAgentResult(
            request_id=query.request_id,
            timestamp=current_time,
            status=status,
            location=LocationContext(
                query=query.location.region_name,
                resolved=resolved_location,
            ),
            observations=observations,
            reasoning=reasoning,
            evidence=evidence,
            confidence=Confidence(
                level=ConfidenceLevel(confidence_level),
                score=confidence_score,
                basis=confidence_basis,
            ),
            warnings=warnings,
            errors=errors,
        )

    def calculate_sst_gradient(
        self,
        sst_a_celsius: float,
        sst_b_celsius: float,
        distance_km: float,
    ) -> dict:
        """
        Produce a physical SST-gradient indicator.

        This does not make a fisheries or ecological conclusion.
        """
        gradient = calculate_sst_gradient(
            sst_a_celsius,
            sst_b_celsius,
            distance_km,
        )

        possible_front = detect_thermal_front(
            gradient,
            threshold_c_per_km=self.thermal_front_threshold_c_per_km,
        )

        return {
            "variable": "sst_gradient",
            "value": gradient,
            "unit": "degC/km",
            "distance_km": distance_km,
            "possible_thermal_front": possible_front,
            "interpretation": (
                "Physical SST gradient exceeds the configured "
                "thermal-front threshold."
                if possible_front
                else
                "Physical SST gradient is below the configured "
                "thermal-front threshold."
            ),
        }

    def calculate_anomaly(
        self,
        value: float,
        baseline_mean: float,
        baseline_std: float,
        baseline_period: str,
    ) -> dict:
        """
        Calculate a deterministic baseline anomaly.
        """
        z_score = calculate_z_score(
            value=value,
            baseline_mean=baseline_mean,
            baseline_std=baseline_std,
        )

        is_anomalous = anomaly_from_z_score(z_score)

        return {
            "value": value,
            "baseline_mean": baseline_mean,
            "baseline_std": baseline_std,
            "z_score": z_score,
            "is_anomalous": is_anomalous,
            "baseline_period": baseline_period,
        }

    def validate_observation(
        self,
        data_point: OceanDataPoint,
        *,
        now: Optional[datetime] = None,
    ) -> tuple[bool, str]:
        """
        Public validation helper used by tests and data-pipeline callers.
        """
        result = validate_data_point(
            data_point,
            now=now,
        )

        return result.valid, result.message

    def _validate_location(
        self,
        query: OceanQuery,
    ) -> Optional[tuple[str, str]]:
        if not query.location.has_location():
            return (
                "ORCA_ERR_NO_DATA",
                (
                    "Ocean Agent requires a resolved latitude/longitude "
                    "or region_name from the Geospatial Agent."
                ),
            )

        return None

    def _calculate_confidence(
        self,
        *,
        supplied_points: list[OceanDataPoint],
        accepted_observations: list[OceanObservation],
        current_time: datetime,
    ) -> tuple[str, float, str]:
        if not accepted_observations:
            return (
                "low",
                0.20,
                "No valid observations were accepted",
            )

        stale = any(
            not point.is_forecast
            and is_stale_observation(
                point.valid_at,
                max_age_hours=self.freshness_threshold_hours,
                now=current_time,
            )
            for point in supplied_points
            if point.variable in {
                observation.variable
                for observation in accepted_observations
            }
        )

        all_observational = all(
            not point.is_forecast
            for point in supplied_points
            if point.variable in {
                observation.variable
                for observation in accepted_observations
            }
        )

        has_interpolation = any(
            point.source_type == "calculation"
            for point in supplied_points
        )

        return choose_confidence(
            is_observation=all_observational,
            is_stale=stale,
            interpolated=has_interpolation,
        )

    def _build_reasoning(
        self,
        *,
        observations: list[OceanObservation],
        warnings: list[WarningItem],
        query: OceanQuery,
    ) -> str:
        variable_names = sorted(
            {observation.variable.value for observation in observations}
        )

        forecast_count = sum(
            observation.is_forecast
            for observation in observations
        )

        observation_count = len(observations) - forecast_count

        summary = (
            f"Processed {len(observations)} physical ocean observation(s) "
            f"for variables: {', '.join(variable_names)}. "
            f"{observation_count} observation value(s) and "
            f"{forecast_count} forecast value(s) were accepted after "
            "physical-range and timestamp validation."
        )

        if warnings:
            summary += (
                " One or more values carry freshness or data-quality "
                "warnings."
            )

        return summary

    def _error_result(
        self,
        query: OceanQuery,
        code: str,
        message: str,
        *,
        resolved_location: Optional[ResolvedLocation],
        timestamp: datetime,
        warnings: Optional[list[WarningItem]] = None,
        errors: Optional[list[ErrorItem]] = None,
    ) -> OceanAgentResult:
        existing_errors = list(errors or [])

        existing_errors.append(
            ErrorItem(
                code=code,
                message=message,
                fatal=True,
            )
        )

        return OceanAgentResult(
            request_id=query.request_id,
            timestamp=timestamp,
            status="error",
            location=LocationContext(
                query=query.location.region_name,
                resolved=resolved_location,
            ),
            observations=[],
            reasoning=None,
            evidence=[],
            confidence=Confidence(
                level=ConfidenceLevel.LOW,
                score=0.0,
                basis=message,
            ),
            warnings=list(warnings or []),
            errors=existing_errors,
        )


__all__ = [
    "OceanAgent",
    "OceanDataPoint",
    "OCEAN_SYSTEM_PROMPT",
    "OBSERVATION_PROMPT",
    "FORECAST_PROMPT",
    "ANOMALY_PROMPT",
    "GRADIENT_PROMPT",
]
