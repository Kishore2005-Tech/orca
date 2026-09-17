from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from math import sqrt
from typing import Dict, Iterable, Optional

from .schemas import OceanVariable


# Physical plausibility limits.
# These are validation bounds, not estimates.
PHYSICAL_RANGES = {
    OceanVariable.SST: (-2.0, 40.0, "degC"),
    OceanVariable.SALINITY: (0.0, 45.0, "PSU"),
    OceanVariable.CURRENTS: (0.0, 5.0, "m/s"),
    OceanVariable.WAVE_HEIGHT: (0.0, 30.0, "m"),
    OceanVariable.WAVE_PERIOD: (0.0, 40.0, "s"),
    OceanVariable.TIDE: (-20.0, 20.0, "m"),
    OceanVariable.SEA_LEVEL: (-20.0, 20.0, "m"),
}


@dataclass(frozen=True)
class OceanDataPoint:
    variable: OceanVariable
    value: float
    unit: str
    valid_at: datetime
    source: str
    source_type: str
    reference: str
    depth_m: Optional[float] = None
    is_forecast: bool = False
    anomaly_z_score: Optional[float] = None
    baseline_period: Optional[str] = None


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    message: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def validate_physical_value(
    variable: OceanVariable,
    value: float,
) -> ValidationResult:
    """
    Validate a value against ORCA's hard physical plausibility range.

    This function never clips, replaces, or estimates invalid values.
    """
    if variable not in PHYSICAL_RANGES:
        return ValidationResult(
            valid=False,
            message=f"Unsupported ocean variable: {variable}",
        )

    minimum, maximum, _ = PHYSICAL_RANGES[variable]

    if value < minimum or value > maximum:
        return ValidationResult(
            valid=False,
            message=(
                f"{variable.value} value {value} is outside the "
                f"physical range [{minimum}, {maximum}]"
            ),
        )

    return ValidationResult(valid=True, message="Value is physically plausible")


def expected_unit(variable: OceanVariable) -> str:
    return PHYSICAL_RANGES[variable][2]


def validate_unit(
    variable: OceanVariable,
    unit: str,
) -> ValidationResult:
    expected = expected_unit(variable)

    if unit != expected:
        return ValidationResult(
            valid=False,
            message=(
                f"{variable.value} requires unit '{expected}', "
                f"received '{unit}'"
            ),
        )

    return ValidationResult(valid=True, message="Unit is valid")


def validate_timestamp(
    valid_at: datetime,
    is_forecast: bool,
    now: Optional[datetime] = None,
) -> ValidationResult:
    """
    Observations cannot have a future timestamp.
    Forecast values may legitimately have future valid_at timestamps.
    """
    current_time = now or utc_now()

    if valid_at.tzinfo is None:
        return ValidationResult(
            valid=False,
            message="valid_at must be timezone-aware",
        )

    if valid_at > current_time and not is_forecast:
        return ValidationResult(
            valid=False,
            message="Non-forecast observation cannot have a future valid_at",
        )

    return ValidationResult(valid=True, message="Timestamp is valid")


def validate_data_point(
    data_point: OceanDataPoint,
    now: Optional[datetime] = None,
) -> ValidationResult:
    value_check = validate_physical_value(
        data_point.variable,
        data_point.value,
    )

    if not value_check.valid:
        return value_check

    unit_check = validate_unit(
        data_point.variable,
        data_point.unit,
    )

    if not unit_check.valid:
        return unit_check

    timestamp_check = validate_timestamp(
        data_point.valid_at,
        data_point.is_forecast,
        now=now,
    )

    if not timestamp_check.valid:
        return timestamp_check

    if data_point.depth_m is not None and data_point.depth_m < 0:
        return ValidationResult(
            valid=False,
            message="depth_m cannot be negative",
        )

    return ValidationResult(valid=True, message="Ocean data point is valid")


def calculate_sst_gradient(
    sst_a_celsius: float,
    sst_b_celsius: float,
    distance_km: float,
) -> float:
    """
    Calculate absolute SST gradient in degC/km.

    This is a physical derived indicator. It does not by itself prove
    an upwelling zone, PFZ, fish presence, or ecosystem response.
    """
    if distance_km <= 0:
        raise ValueError("distance_km must be greater than zero")

    validate_physical_value(
        OceanVariable.SST,
        sst_a_celsius,
    )
    validate_physical_value(
        OceanVariable.SST,
        sst_b_celsius,
    )

    return abs(sst_a_celsius - sst_b_celsius) / distance_km


def detect_thermal_front(
    sst_gradient_c_per_km: float,
    threshold_c_per_km: float = 0.2,
) -> bool:
    """
    Flag a possible thermal front from a supplied SST gradient.

    The threshold is an operational heuristic and should not be presented
    as proof of a biological front or fish aggregation.
    """
    if sst_gradient_c_per_km < 0:
        raise ValueError("SST gradient cannot be negative")

    if threshold_c_per_km <= 0:
        raise ValueError("threshold must be greater than zero")

    return sst_gradient_c_per_km >= threshold_c_per_km


def interpolate_linear(
    start_value: float,
    end_value: float,
    fraction: float,
) -> float:
    """
    Linear interpolation utility for time-series processing.

    fraction must be in [0, 1].
    """
    if not 0.0 <= fraction <= 1.0:
        raise ValueError("fraction must be between 0 and 1")

    return start_value + (
        end_value - start_value
    ) * fraction


def aggregate_mean(values: Iterable[float]) -> float:
    values = list(values)

    if not values:
        raise ValueError("Cannot calculate mean of empty values")

    return sum(values) / len(values)


def calculate_z_score(
    value: float,
    baseline_mean: float,
    baseline_std: float,
) -> Optional[float]:
    """
    Calculate a climatological-style z-score.

    Returns None when the baseline standard deviation is zero.
    """
    if baseline_std < 0:
        raise ValueError("baseline_std cannot be negative")

    if baseline_std == 0:
        return None

    return (value - baseline_mean) / baseline_std


def anomaly_from_z_score(
    z_score: Optional[float],
    threshold: float = 2.0,
) -> Optional[bool]:
    if z_score is None:
        return None

    if threshold <= 0:
        raise ValueError("threshold must be greater than zero")

    return abs(z_score) >= threshold


def freshness_hours(
    observed_at: datetime,
    now: Optional[datetime] = None,
) -> float:
    """
    Calculate age of a source value in hours.
    """
    current_time = now or utc_now()

    if observed_at.tzinfo is None:
        raise ValueError("observed_at must be timezone-aware")

    return max(
        0.0,
        (current_time - observed_at).total_seconds() / 3600.0,
    )


def is_stale_observation(
    observed_at: datetime,
    max_age_hours: float = 24.0,
    now: Optional[datetime] = None,
) -> bool:
    if max_age_hours < 0:
        raise ValueError("max_age_hours cannot be negative")

    return freshness_hours(observed_at, now=now) > max_age_hours


def choose_confidence(
    *,
    is_observation: bool,
    is_stale: bool,
    interpolated: bool = False,
    conflicting_sources: bool = False,
) -> tuple[str, float, str]:
    """
    Deterministic confidence classification.

    This does not represent statistical model confidence.
    """
    if conflicting_sources:
        return (
            "low",
            0.40,
            "Conflicting source values require Verification Agent review",
        )

    if is_stale:
        return (
            "low",
            0.45,
            "Source data exceeds the Ocean Agent freshness threshold",
        )

    if is_observation and not interpolated:
        return (
            "high",
            0.90,
            "Recent observational data from a supplied source",
        )

    if interpolated:
        return (
            "medium",
            0.70,
            "Value is derived through time-series interpolation",
        )

    return (
        "medium",
        0.65,
        "Model or processed ocean data supplied to the agent",
    )


def group_by_variable(
    data_points: Iterable[OceanDataPoint],
) -> Dict[OceanVariable, list[OceanDataPoint]]:
    grouped: Dict[OceanVariable, list[OceanDataPoint]] = {}

    for point in data_points:
        grouped.setdefault(point.variable, []).append(point)

    return grouped
