from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, radians, sin, sqrt


EARTH_RADIUS_KM = 6371.0088


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float


@dataclass(frozen=True)
class ResolutionResult:
    is_valid: bool
    native_resolution_m: float | None
    requested_resolution_m: float | None
    message: str


@dataclass(frozen=True)
class CoverageResult:
    is_covered: bool
    is_ocean: bool | None
    coastal_contamination: bool
    data_gap: bool
    message: str


@dataclass(frozen=True)
class Feature:
    name: str
    feature_type: str
    geometry_ref: str | None = None
    center: Coordinate | None = None


def validate_coordinates(lat: float, lon: float) -> Coordinate:
    """
    Validate WGS84 latitude/longitude.

    Latitude:
        -90 <= lat <= 90

    Longitude:
        -180 <= lon <= 180
    """

    if not isinstance(lat, (int, float)):
        raise ValueError("Latitude must be numeric.")

    if not isinstance(lon, (int, float)):
        raise ValueError("Longitude must be numeric.")

    if not -90.0 <= float(lat) <= 90.0:
        raise ValueError("Latitude must be between -90 and 90 degrees.")

    if not -180.0 <= float(lon) <= 180.0:
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    return Coordinate(
        lat=float(lat),
        lon=float(lon),
    )


def check_resolution(
    native_resolution_m: float | None,
    requested_resolution_m: float | None,
) -> ResolutionResult:
    """
    Check whether a requested spatial resolution is compatible
    with the native resolution of the dataset.

    ORCA must not infer information below the native resolution.
    """

    if native_resolution_m is None:
        return ResolutionResult(
            is_valid=True,
            native_resolution_m=None,
            requested_resolution_m=requested_resolution_m,
            message="Native resolution is unknown; no sub-grid inference is performed.",
        )

    if native_resolution_m <= 0:
        return ResolutionResult(
            is_valid=False,
            native_resolution_m=native_resolution_m,
            requested_resolution_m=requested_resolution_m,
            message="Native resolution must be greater than zero.",
        )

    if requested_resolution_m is None:
        return ResolutionResult(
            is_valid=True,
            native_resolution_m=native_resolution_m,
            requested_resolution_m=None,
            message="No finer resolution was requested.",
        )

    if requested_resolution_m <= 0:
        return ResolutionResult(
            is_valid=False,
            native_resolution_m=native_resolution_m,
            requested_resolution_m=requested_resolution_m,
            message="Requested resolution must be greater than zero.",
        )

    # A request for a finer resolution than the native dataset
    # would require unsupported sub-grid inference.
    if requested_resolution_m < native_resolution_m:
        return ResolutionResult(
            is_valid=False,
            native_resolution_m=native_resolution_m,
            requested_resolution_m=requested_resolution_m,
            message=(
                "Requested resolution is finer than the dataset's native "
                "resolution; sub-grid inference is not permitted."
            ),
        )

    return ResolutionResult(
        is_valid=True,
        native_resolution_m=native_resolution_m,
        requested_resolution_m=requested_resolution_m,
        message="Requested resolution is compatible with the native dataset resolution.",
    )


def check_coverage(
    lat: float,
    lon: float,
    *,
    is_ocean: bool | None = None,
    data_available: bool = True,
    coastal_contamination: bool = False,
) -> CoverageResult:
    """
    Validate whether a coordinate is covered by the available
    geospatial data.

    `is_ocean` should come from an authoritative coastline/ocean mask
    when available. It is intentionally not guessed here.
    """

    validate_coordinates(lat, lon)

    if not data_available:
        return CoverageResult(
            is_covered=False,
            is_ocean=is_ocean,
            coastal_contamination=coastal_contamination,
            data_gap=True,
            message="No source data is available for the requested coordinate.",
        )

    if is_ocean is False:
        return CoverageResult(
            is_covered=True,
            is_ocean=False,
            coastal_contamination=coastal_contamination,
            data_gap=False,
            message="Coordinate is classified as land by the supplied spatial mask.",
        )

    if coastal_contamination:
        return CoverageResult(
            is_covered=True,
            is_ocean=is_ocean,
            coastal_contamination=True,
            data_gap=False,
            message="Coordinate is covered, but coastal contamination is flagged.",
        )

    return CoverageResult(
        is_covered=True,
        is_ocean=is_ocean,
        coastal_contamination=False,
        data_gap=False,
        message="Coordinate is covered by the available spatial data.",
    )


def haversine_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Great-circle distance between two WGS84 coordinates.

    This is appropriate for ORCA's general distance calculations;
    it does not replace a specialized projected GIS calculation
    for high-precision local surveying.
    """

    validate_coordinates(lat1, lon1)
    validate_coordinates(lat2, lon2)

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1_rad)
        * cos(lat2_rad)
        * sin(delta_lon / 2) ** 2
    )

    a = min(1.0, max(0.0, a))

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def point_in_bbox(
    lat: float,
    lon: float,
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float,
) -> bool:
    """
    Simple bounding-box containment utility.

    This is intended as a lightweight fallback. For real EEZ/MPA
    boundary containment, an authoritative GIS polygon operation
    should be used.
    """

    validate_coordinates(lat, lon)
    validate_coordinates(min_lat, min_lon)
    validate_coordinates(max_lat, max_lon)

    if min_lat > max_lat:
        raise ValueError("min_lat cannot be greater than max_lat.")

    if min_lon > max_lon:
        raise ValueError("min_lon cannot be greater than max_lon.")

    return (
        min_lat <= lat <= max_lat
        and min_lon <= lon <= max_lon
    )


def find_nearest_feature(
    lat: float,
    lon: float,
    features: list[Feature],
) -> tuple[Feature | None, float | None]:
    """
    Find the nearest feature from features that have a known center.

    Returns:
        (feature, distance_km)
    """

    validate_coordinates(lat, lon)

    nearest: Feature | None = None
    nearest_distance: float | None = None

    for feature in features:
        if feature.center is None:
            continue

        distance = haversine_distance_km(
            lat,
            lon,
            feature.center.lat,
            feature.center.lon,
        )

        if nearest_distance is None or distance < nearest_distance:
            nearest = feature
            nearest_distance = distance

    return nearest, nearest_distance


def normalize_longitude(lon: float) -> float:
    """
    Normalize longitude into the [-180, 180] range.
    """

    if not isinstance(lon, (int, float)):
        raise ValueError("Longitude must be numeric.")

    normalized = ((float(lon) + 180.0) % 360.0) - 180.0

    # Keep positive 180 when the original value is exactly +180.
    if normalized == -180.0 and float(lon) > 0:
        return 180.0

    return normalized
