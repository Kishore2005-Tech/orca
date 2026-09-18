"""
Coordinate validation and normalization utilities for ORCA.

ORCA uses WGS84 / EPSG:4326 as its canonical geographic coordinate
reference system.

Rules
-----
Latitude:
    -90 <= latitude <= 90

Longitude:
    -180 <= longitude <= 180

Longitudes supplied outside the canonical range may be normalized
because longitude wraps around the antimeridian.

Latitudes are never wrapped because latitude does not wrap.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Mapping, Tuple


WGS84_EPSG = 4326


class CoordinateError(ValueError):
    """Raised when geographic coordinates are invalid."""


@dataclass(frozen=True)
class Coordinate:
    """Validated WGS84 geographic coordinate."""

    latitude: float
    longitude: float
    crs: str = "EPSG:4326"

    def __post_init__(self) -> None:
        validate_latitude(self.latitude)
        validate_longitude(self.longitude)

        if self.crs.upper() not in {
            "EPSG:4326",
            "WGS84",
        }:
            raise CoordinateError(
                f"ORCA currently expects WGS84/EPSG:4326 coordinates. "
                f"Received CRS={self.crs!r}."
            )

    @property
    def lat(self) -> float:
        return self.latitude

    @property
    def lon(self) -> float:
        return self.longitude

    def as_tuple(self) -> Tuple[float, float]:
        """Return ``(latitude, longitude)``."""
        return self.latitude, self.longitude

    def as_geojson_coordinates(self) -> list[float]:
        """
        Return GeoJSON coordinate order.

        GeoJSON uses:
            [longitude, latitude]
        """
        return [self.longitude, self.latitude]

    def as_dict(self) -> dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "crs": self.crs,
        }


def _to_float(value: Any, field_name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise CoordinateError(
            f"{field_name} must be a numeric value."
        ) from exc

    if not math.isfinite(result):
        raise CoordinateError(
            f"{field_name} must be finite. Received {value!r}."
        )

    return result


def validate_latitude(latitude: Any) -> float:
    """
    Validate latitude and return it as float.
    """
    value = _to_float(latitude, "latitude")

    if not -90.0 <= value <= 90.0:
        raise CoordinateError(
            f"Latitude must be between -90 and 90 degrees. "
            f"Received {value}."
        )

    return value


def validate_longitude(longitude: Any) -> float:
    """
    Validate longitude and return it as float.

    This function validates the canonical WGS84 longitude range.
    Use ``normalize_longitude`` if values outside this range need
    to be converted first.
    """
    value = _to_float(longitude, "longitude")

    if not -180.0 <= value <= 180.0:
        raise CoordinateError(
            f"Longitude must be between -180 and 180 degrees. "
            f"Received {value}."
        )

    return value


def normalize_longitude(longitude: Any) -> float:
    """
    Normalize longitude to [-180, 180].

    Examples
    --------
    181  -> -179
    360  -> 0
    -181 -> 179
    """
    value = _to_float(longitude, "longitude")

    normalized = ((value + 180.0) % 360.0) - 180.0

    # Preserve +180 instead of converting it to -180 when supplied
    # exactly as 180.
    if value == 180.0:
        return 180.0

    return normalized


def validate_coordinate(
    latitude: Any,
    longitude: Any,
    *,
    normalize_lon: bool = False,
) -> Coordinate:
    """
    Validate a WGS84 coordinate.

    Parameters
    ----------
    latitude:
        Latitude in degrees.

    longitude:
        Longitude in degrees.

    normalize_lon:
        If True, longitude is normalized into [-180, 180].
        If False, an out-of-range longitude raises CoordinateError.
    """
    lat = validate_latitude(latitude)

    lon = (
        normalize_longitude(longitude)
        if normalize_lon
        else validate_longitude(longitude)
    )

    return Coordinate(
        latitude=lat,
        longitude=lon,
        crs="EPSG:4326",
    )


def coordinate_from_mapping(
    value: Mapping[str, Any],
) -> Coordinate:
    """
    Create a Coordinate from common dictionary formats.

    Supported keys:
        latitude / longitude
        lat / lon
    """
    if "latitude" in value:
        latitude = value["latitude"]
    elif "lat" in value:
        latitude = value["lat"]
    else:
        raise CoordinateError(
            "Coordinate mapping must contain 'latitude' or 'lat'."
        )

    if "longitude" in value:
        longitude = value["longitude"]
    elif "lon" in value:
        longitude = value["lon"]
    else:
        raise CoordinateError(
            "Coordinate mapping must contain 'longitude' or 'lon'."
        )

    return validate_coordinate(latitude, longitude)


def coordinate_from_sequence(
    value: Any,
    *,
    order: str = "latlon",
) -> Coordinate:
    """
    Create a Coordinate from a two-element sequence.

    Parameters
    ----------
    order:
        ``latlon`` for (latitude, longitude)

        ``lonlat`` for (longitude, latitude)
    """
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise CoordinateError(
            "Coordinate sequence must contain exactly two values."
        )

    if order.lower() == "latlon":
        return validate_coordinate(value[0], value[1])

    if order.lower() == "lonlat":
        return validate_coordinate(value[1], value[0])

    raise CoordinateError(
        "order must be either 'latlon' or 'lonlat'."
    )


def coerce_coordinate(
    value: Any,
    *,
    sequence_order: str = "latlon",
) -> Coordinate:
    """
    Convert common coordinate representations into a validated Coordinate.
    """
    if isinstance(value, Coordinate):
        return value

    if isinstance(value, Mapping):
        return coordinate_from_mapping(value)

    if isinstance(value, (list, tuple)):
        return coordinate_from_sequence(
            value,
            order=sequence_order,
        )

    raise CoordinateError(
        "Unsupported coordinate representation. "
        "Expected Coordinate, mapping, list, or tuple."
    )
