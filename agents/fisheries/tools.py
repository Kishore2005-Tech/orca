from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin, sqrt


@dataclass(frozen=True)
class PFZInputs:
    """Inputs used to calculate a PFZ suitability indicator."""

    sst_celsius: float
    chlorophyll_mg_m3: float
    sst_gradient_c_per_km: float
    thermal_front_detected: bool = False


@dataclass(frozen=True)
class Bathymetry:
    """Bathymetry/depth constraint."""

    depth_m: float
    minimum_depth_m: float = 0.0
    maximum_depth_m: float | None = None


@dataclass(frozen=True)
class PFZResult:
    """PFZ calculation result."""

    score: int
    detected: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class HabitatResult:
    """Habitat suitability result."""

    score: int
    category: str
    depth_valid: bool
    reasons: tuple[str, ...]
    limitations: tuple[str, ...]


@dataclass(frozen=True)
class DriftResult:
    """PFZ drift estimate."""

    displacement_km: float
    displacement_nm: float
    direction_deg: float


def validate_pfz_inputs(inputs: PFZInputs) -> None:
    """Validate scientific input ranges."""

    if not -5.0 <= inputs.sst_celsius <= 50.0:
        raise ValueError("SST must be between -5 and 50 °C")

    if inputs.chlorophyll_mg_m3 < 0:
        raise ValueError("chlorophyll cannot be negative")

    if inputs.sst_gradient_c_per_km < 0:
        raise ValueError("SST gradient cannot be negative")


def get_pfz(inputs: PFZInputs) -> PFZResult:
    """
    Generate a deterministic PFZ indicator.

    The scoring combines:
    - SST suitability
    - chlorophyll concentration
    - SST gradient
    - thermal-front evidence

    This is an operational indicator, not a fish-presence guarantee.
    """

    validate_pfz_inputs(inputs)

    score = 0
    reasons: list[str] = []

    # SST component.
    if 27.5 <= inputs.sst_celsius <= 28.6:
        score += 30
        reasons.append("SST is within the configured pelagic suitability range.")
    elif 27.0 <= inputs.sst_celsius <= 29.0:
        score += 15
        reasons.append("SST is near the configured suitability range.")
    else:
        reasons.append(
            "SST is outside the configured primary suitability range."
        )

    # Chlorophyll component.
    if inputs.chlorophyll_mg_m3 >= 0.8:
        score += 30
        reasons.append("Elevated chlorophyll-a was observed.")
    elif inputs.chlorophyll_mg_m3 >= 0.5:
        score += 18
        reasons.append("Moderate chlorophyll-a concentration was observed.")
    else:
        reasons.append("Chlorophyll-a concentration is relatively low.")

    # Thermal gradient component.
    if inputs.sst_gradient_c_per_km >= 0.4:
        score += 25
        reasons.append("A strong SST spatial gradient was observed.")
    elif inputs.sst_gradient_c_per_km >= 0.25:
        score += 12
        reasons.append("A moderate SST spatial gradient was observed.")
    else:
        reasons.append("The SST spatial gradient is weak.")

    # Front evidence.
    if inputs.thermal_front_detected:
        score += 15
        reasons.append("An independently detected thermal front is present.")

    score = min(100, max(0, score))

    return PFZResult(
        score=score,
        detected=score >= 60,
        reasons=tuple(reasons),
    )


def validate_bathymetry(
    bathymetry: Bathymetry,
) -> bool:
    """
    Check whether a candidate PFZ lies inside the requested depth range.
    """

    if bathymetry.depth_m < 0:
        raise ValueError("depth cannot be negative")

    if bathymetry.minimum_depth_m < 0:
        raise ValueError("minimum depth cannot be negative")

    if (
        bathymetry.maximum_depth_m is not None
        and bathymetry.maximum_depth_m < bathymetry.minimum_depth_m
    ):
        raise ValueError(
            "maximum depth must be >= minimum depth"
        )

    if bathymetry.depth_m < bathymetry.minimum_depth_m:
        return False

    if (
        bathymetry.maximum_depth_m is not None
        and bathymetry.depth_m > bathymetry.maximum_depth_m
    ):
        return False

    return True


def get_habitat_suitability(
    pfz: PFZResult,
    bathymetry: Bathymetry,
) -> HabitatResult:
    """
    Combine PFZ indicator with bathymetric suitability.

    Depth acts as a validation constraint rather than a reason to claim
    that a particular species is definitely present.
    """

    depth_valid = validate_bathymetry(bathymetry)

    reasons = list(pfz.reasons)
    limitations: list[str] = []

    score = pfz.score

    if not depth_valid:
        score = max(0, score - 30)
        limitations.append(
            "Candidate location is outside the supplied bathymetric range."
        )
    else:
        reasons.append("Bathymetry is compatible with the supplied depth range.")

    if score >= 75:
        category = "high"
    elif score >= 50:
        category = "moderate"
    else:
        category = "low"

    limitations.append(
        "Habitat suitability is an environmental indicator and does not "
        "guarantee fish presence, abundance, or catch."
    )

    return HabitatResult(
        score=score,
        category=category,
        depth_valid=depth_valid,
        reasons=tuple(reasons),
        limitations=tuple(limitations),
    )


def get_pfz_drift(
    *,
    current_speed_m_s: float,
    current_direction_deg: float,
    wind_speed_m_s: float,
    wind_direction_deg: float,
    hours: float,
    wind_factor: float = 0.03,
) -> DriftResult:
    """
    Estimate PFZ displacement from current plus a small wind-driven component.

    The calculation is intentionally transparent and approximate.

    current displacement:
        current speed × elapsed time

    wind contribution:
        wind speed × wind_factor × elapsed time
    """

    if current_speed_m_s < 0:
        raise ValueError("current speed cannot be negative")

    if wind_speed_m_s < 0:
        raise ValueError("wind speed cannot be negative")

    if hours <= 0:
        raise ValueError("hours must be positive")

    if not 0 <= current_direction_deg < 360:
        raise ValueError(
            "current direction must be in [0, 360)"
        )

    if not 0 <= wind_direction_deg < 360:
        raise ValueError(
            "wind direction must be in [0, 360)"
        )

    if not 0 <= wind_factor <= 1:
        raise ValueError(
            "wind_factor must be between 0 and 1"
        )

    seconds = hours * 3600.0

    current_velocity = (
        current_speed_m_s
        * sin(radians(current_direction_deg)),
        current_speed_m_s
        * cos(radians(current_direction_deg)),
    )

    wind_velocity = (
        wind_speed_m_s
        * wind_factor
        * sin(radians(wind_direction_deg)),
        wind_speed_m_s
        * wind_factor
        * cos(radians(wind_direction_deg)),
    )

    east_velocity = current_velocity[0] + wind_velocity[0]
    north_velocity = current_velocity[1] + wind_velocity[1]

    east_displacement_m = east_velocity * seconds
    north_displacement_m = north_velocity * seconds

    displacement_m = sqrt(
        east_displacement_m**2
        + north_displacement_m**2
    )

    displacement_km = displacement_m / 1000.0
    displacement_nm = displacement_km / 1.852

    direction = (
        __import__("math").degrees(
            __import__("math").atan2(
                east_displacement_m,
                north_displacement_m,
            )
        )
        + 360.0
    ) % 360.0

    return DriftResult(
        displacement_km=displacement_km,
        displacement_nm=displacement_nm,
        direction_deg=direction,
    )


def project_pfz_coordinate(
    *,
    latitude: float,
    longitude: float,
    drift: DriftResult,
) -> tuple[float, float]:
    """
    Project a PFZ point using a simple spherical-Earth approximation.

    This should not replace a geospatial library for production-grade
    navigation calculations.
    """

    if not -90 <= latitude <= 90:
        raise ValueError("latitude must be between -90 and 90")

    if not -180 <= longitude <= 180:
        raise ValueError("longitude must be between -180 and 180")

    earth_radius_km = 6371.0

    east_km = drift.displacement_km * sin(
        radians(drift.direction_deg)
    )
    north_km = drift.displacement_km * cos(
        radians(drift.direction_deg)
    )

    new_latitude = latitude + (
        north_km / earth_radius_km
    ) * (180.0 / __import__("math").pi)

    latitude_factor = cos(radians(latitude))

    if abs(latitude_factor) < 1e-8:
        new_longitude = longitude
    else:
        new_longitude = longitude + (
            east_km
            / (earth_radius_km * latitude_factor)
        ) * (180.0 / __import__("math").pi)

    new_longitude = (
        (new_longitude + 180.0) % 360.0
    ) - 180.0

    new_latitude = max(-90.0, min(90.0, new_latitude))

    return new_latitude, new_longitude
