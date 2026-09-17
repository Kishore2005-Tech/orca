from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import hypot
from statistics import quantiles
from typing import Sequence


@dataclass(frozen=True)
class ChlorophyllObservation:
    """A chlorophyll-a observation."""

    value: float
    observed_at: datetime
    lat: float | None = None
    lon: float | None = None
    source: str = "processed_chlorophyll_dataset"
    unit: str = "mg/m3"


@dataclass(frozen=True)
class SSTObservation:
    """A sea-surface-temperature observation."""

    value_celsius: float
    observed_at: datetime
    lat: float | None = None
    lon: float | None = None
    source: str = "processed_sst_dataset"


@dataclass(frozen=True)
class EcosystemGridPoint:
    """One co-located SST/chlorophyll point used for derived indicators."""

    lat: float
    lon: float
    sst_celsius: float
    chlorophyll_mg_m3: float


@dataclass(frozen=True)
class MarineHeatwaveResult:
    """Result of the prototype MHW detection algorithm."""

    detected: bool
    threshold_celsius: float
    qualifying_days: int
    total_days: int


@dataclass(frozen=True)
class GradientResult:
    """Spatial gradient result."""

    magnitude: float
    lat: float
    lon: float


@dataclass(frozen=True)
class UpwellingResult:
    """Result of the upwelling heuristic."""

    detected: bool
    reason: str


def validate_chlorophyll_observations(
    observations: Sequence[ChlorophyllObservation],
) -> list[ChlorophyllObservation]:
    """
    Validate and sort chlorophyll observations.

    ORCA's data dictionary requires positive chlorophyll-a values.
    Non-positive values are rejected instead of silently corrected.
    """

    valid: list[ChlorophyllObservation] = []

    for observation in observations:
        if observation.value <= 0:
            raise ValueError(
                "chlorophyll-a concentration must be greater than zero"
            )

        valid.append(observation)

    return sorted(valid, key=lambda item: item.observed_at)


def get_chlorophyll(
    observations: Sequence[ChlorophyllObservation],
) -> dict[str, object]:
    """
    Process chlorophyll-a observations.

    Returns summary statistics without interpreting chlorophyll as fish
    abundance. Chlorophyll is treated as an ecosystem/productivity proxy.
    """

    validated = validate_chlorophyll_observations(observations)

    if not validated:
        raise ValueError("no chlorophyll observations supplied")

    values = [item.value for item in validated]

    return {
        "parameter": "chlorophyll_a",
        "unit": validated[0].unit,
        "count": len(values),
        "latest_value": validated[-1].value,
        "minimum": min(values),
        "maximum": max(values),
        "mean": sum(values) / len(values),
        "observed_at": validated[-1].observed_at,
        "source": validated[-1].source,
    }


def calculate_percentile_threshold(
    values: Sequence[float],
    percentile: float = 90.0,
) -> float:
    """Calculate a percentile threshold from a numeric series."""

    if not values:
        raise ValueError("values cannot be empty")

    if not 0.0 <= percentile <= 100.0:
        raise ValueError("percentile must be between 0 and 100")

    ordered = sorted(values)

    if len(ordered) == 1:
        return ordered[0]

    if percentile == 0:
        return ordered[0]

    if percentile == 100:
        return ordered[-1]

    position = (len(ordered) - 1) * percentile / 100.0
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower

    return ordered[lower] + (
        ordered[upper] - ordered[lower]
    ) * fraction


def get_mhw(
    sst_observations: Sequence[SSTObservation],
    percentile: float = 90.0,
    minimum_qualifying_days: int = 5,
) -> MarineHeatwaveResult:
    """
    Detect a prototype marine heatwave condition.

    ORCA's implementation plan uses the simplified rule:
    SST > 90th percentile for >= 5 days.

    This is an indicator, not a claim about ecological damage.
    """

    if minimum_qualifying_days <= 0:
        raise ValueError("minimum_qualifying_days must be positive")

    if not sst_observations:
        raise ValueError("no SST observations supplied")

    ordered = sorted(
        sst_observations,
        key=lambda item: item.observed_at,
    )

    threshold = calculate_percentile_threshold(
        [item.value_celsius for item in ordered],
        percentile,
    )

    qualifying = [
        item
        for item in ordered
        if item.value_celsius > threshold
    ]

    qualifying_days = len(qualifying)

    return MarineHeatwaveResult(
        detected=qualifying_days >= minimum_qualifying_days,
        threshold_celsius=threshold,
        qualifying_days=qualifying_days,
        total_days=len(ordered),
    )


def calculate_spatial_gradient(
    points: Sequence[EcosystemGridPoint],
    attribute: str,
) -> list[GradientResult]:
    """
    Calculate a simple nearest-neighbour gradient.

    This is intentionally a lightweight prototype calculation.
    It identifies strong spatial changes but does not claim that every
    detected gradient is an oceanographic front.
    """

    if attribute not in {"sst_celsius", "chlorophyll_mg_m3"}:
        raise ValueError(
            "attribute must be 'sst_celsius' or 'chlorophyll_mg_m3'"
        )

    if len(points) < 2:
        return []

    results: list[GradientResult] = []

    for index, point in enumerate(points):
        nearest: EcosystemGridPoint | None = None
        nearest_distance: float | None = None

        for candidate_index, candidate in enumerate(points):
            if index == candidate_index:
                continue

            distance = hypot(
                point.lat - candidate.lat,
                point.lon - candidate.lon,
            )

            if nearest_distance is None or distance < nearest_distance:
                nearest_distance = distance
                nearest = candidate

        if nearest is None or nearest_distance in (None, 0):
            continue

        point_value = getattr(point, attribute)
        nearest_value = getattr(nearest, attribute)

        gradient = abs(point_value - nearest_value) / nearest_distance

        results.append(
            GradientResult(
                magnitude=gradient,
                lat=point.lat,
                lon=point.lon,
            )
        )

    return results


def get_fronts(
    points: Sequence[EcosystemGridPoint],
    sst_gradient_threshold: float = 0.5,
    chlorophyll_gradient_threshold: float = 0.5,
) -> list[GradientResult]:
    """
    Identify candidate ocean-front locations.

    A point is considered a candidate when both SST and chlorophyll
    spatial gradients exceed their configured thresholds.

    The result is a derived indicator, not a causal ecological statement.
    """

    if not points:
        return []

    sst_gradients = calculate_spatial_gradient(
        points,
        "sst_celsius",
    )

    chl_gradients = calculate_spatial_gradient(
        points,
        "chlorophyll_mg_m3",
    )

    chl_by_location = {
        (item.lat, item.lon): item.magnitude
        for item in chl_gradients
    }

    return [
        item
        for item in sst_gradients
        if item.magnitude >= sst_gradient_threshold
        and chl_by_location.get((item.lat, item.lon), 0.0)
        >= chlorophyll_gradient_threshold
    ]


def get_upwelling(
    points: Sequence[EcosystemGridPoint],
    cold_sst_threshold_celsius: float,
    high_chlorophyll_threshold_mg_m3: float,
) -> list[UpwellingResult]:
    """
    Identify candidate upwelling conditions.

    Prototype rule:
      cold SST + high chlorophyll.

    The function deliberately does not state that fish abundance or catch
    will increase.
    """

    if not points:
        return []

    results: list[UpwellingResult] = []

    for point in points:
        cold = point.sst_celsius <= cold_sst_threshold_celsius
        chlorophyll_high = (
            point.chlorophyll_mg_m3
            >= high_chlorophyll_threshold_mg_m3
        )

        if cold and chlorophyll_high:
            results.append(
                UpwellingResult(
                    detected=True,
                    reason=(
                        "Cold SST and elevated chlorophyll were "
                        "observed at the same grid point."
                    ),
                )
            )

    return results
