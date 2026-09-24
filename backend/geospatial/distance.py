"""
Deterministic geographic distance and vessel-position calculations.

All calculations use spherical-earth approximations and WGS84
latitude/longitude coordinates.

These functions do not use ML.
"""

from __future__ import annotations

import math
from typing import Tuple

from backend.geospatial.coordinate import (
    Coordinate,
    CoordinateError,
    validate_coordinate,
)


EARTH_RADIUS_KM = 6371.0088
KM_TO_NM = 0.539956803
NM_TO_KM = 1.852
KNOT_TO_KMH = 1.852


def _validate_pair(
    lat: float,
    lon: float,
) -> Coordinate:
    return validate_coordinate(lat, lon)


def haversine_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate great-circle distance between two WGS84 points.

    Returns
    -------
    float
        Distance in kilometres.
    """
    p1 = _validate_pair(lat1, lon1)
    p2 = _validate_pair(lat2, lon2)

    phi1 = math.radians(p1.latitude)
    phi2 = math.radians(p2.latitude)

    delta_phi = math.radians(
        p2.latitude - p1.latitude
    )

    delta_lambda = math.radians(
        p2.longitude - p1.longitude
    )

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(delta_lambda / 2.0) ** 2
    )

    a = min(1.0, max(0.0, a))

    c = 2.0 * math.atan2(
        math.sqrt(a),
        math.sqrt(1.0 - a),
    )

    return EARTH_RADIUS_KM * c


def haversine_distance_m(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Return great-circle distance in metres."""
    return haversine_distance_km(
        lat1,
        lon1,
        lat2,
        lon2,
    ) * 1000.0


def haversine_distance_nm(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Return great-circle distance in nautical miles."""
    return haversine_distance_km(
        lat1,
        lon1,
        lat2,
        lon2,
    ) * KM_TO_NM


def initial_bearing_degrees(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate initial great-circle bearing from point 1 to point 2.

    Returns:
        Bearing in degrees clockwise from true north [0, 360).
    """
    p1 = _validate_pair(lat1, lon1)
    p2 = _validate_pair(lat2, lon2)

    phi1 = math.radians(p1.latitude)
    phi2 = math.radians(p2.latitude)
    delta_lambda = math.radians(
        p2.longitude - p1.longitude
    )

    x = math.sin(delta_lambda) * math.cos(phi2)

    y = (
        math.cos(phi1) * math.sin(phi2)
        - math.sin(phi1)
        * math.cos(phi2)
        * math.cos(delta_lambda)
    )

    bearing = math.degrees(
        math.atan2(x, y)
    )

    return (bearing + 360.0) % 360.0


def destination_point(
    latitude: float,
    longitude: float,
    bearing_degrees: float,
    distance_km: float,
) -> Coordinate:
    """
    Calculate the point reached after travelling a given distance
    along a great-circle bearing.
    """
    origin = _validate_pair(
        latitude,
        longitude,
    )

    if not math.isfinite(bearing_degrees):
        raise CoordinateError(
            "Bearing must be finite."
        )

    if not math.isfinite(distance_km):
        raise CoordinateError(
            "Distance must be finite."
        )

    if distance_km < 0:
        raise CoordinateError(
            "Distance cannot be negative."
        )

    bearing = math.radians(
        bearing_degrees % 360.0
    )

    angular_distance = (
        distance_km / EARTH_RADIUS_KM
    )

    phi1 = math.radians(
        origin.latitude
    )
    lambda1 = math.radians(
        origin.longitude
    )

    phi2 = math.asin(
        math.sin(phi1)
        * math.cos(angular_distance)
        + math.cos(phi1)
        * math.sin(angular_distance)
        * math.cos(bearing)
    )

    lambda2 = lambda1 + math.atan2(
        math.sin(bearing)
        * math.sin(angular_distance)
        * math.cos(phi1),
        math.cos(angular_distance)
        - math.sin(phi1)
        * math.sin(phi2),
    )

    latitude2 = math.degrees(phi2)

    longitude2 = (
        math.degrees(lambda2) + 540.0
    ) % 360.0 - 180.0

    return validate_coordinate(
        latitude2,
        longitude2,
    )


def knots_to_kmh(knots: float) -> float:
    """Convert nautical speed from knots to km/h."""
    if not math.isfinite(knots):
        raise CoordinateError(
            "Speed must be finite."
        )

    return knots * KNOT_TO_KMH


def knots_to_km_per_second(knots: float) -> float:
    """Convert knots to km/s."""
    return knots_to_kmh(knots) / 3600.0


def project_position(
    latitude: float,
    longitude: float,
    *,
    heading_degrees: float,
    speed_knots: float,
    duration_hours: float,
    current_speed_knots: float = 0.0,
    current_direction_degrees: float | None = None,
) -> Coordinate:
    """
    Project a vessel position using vessel motion + ocean current.

    This is deterministic vector addition.

    Vessel motion:
        heading + speed

    Current:
        direction + current speed

    Parameters
    ----------
    heading_degrees:
        Vessel heading, clockwise from north.

    speed_knots:
        Vessel speed through water.

    duration_hours:
        Projection interval.

    current_speed_knots:
        Ocean-current speed.

    current_direction_degrees:
        Direction of the current vector, clockwise from north.

        If current_speed_knots > 0, this value must be supplied.

    Notes
    -----
    This is a short-horizon geographic projection. It is not a
    trained prediction model.
    """
    origin = _validate_pair(
        latitude,
        longitude,
    )

    numeric_values = {
        "heading_degrees": heading_degrees,
        "speed_knots": speed_knots,
        "duration_hours": duration_hours,
        "current_speed_knots": current_speed_knots,
    }

    for name, value in numeric_values.items():
        if not math.isfinite(value):
            raise CoordinateError(
                f"{name} must be finite."
            )

    if speed_knots < 0:
        raise CoordinateError(
            "speed_knots cannot be negative."
        )

    if current_speed_knots < 0:
        raise CoordinateError(
            "current_speed_knots cannot be negative."
        )

    if duration_hours < 0:
        raise CoordinateError(
            "duration_hours cannot be negative."
        )

    if (
        current_speed_knots > 0
        and current_direction_degrees is None
    ):
        raise CoordinateError(
            "current_direction_degrees is required "
            "when current_speed_knots > 0."
        )

    if duration_hours == 0:
        return origin

    # Convert speeds to km travelled during the projection period.
    vessel_distance_km = (
        knots_to_kmh(speed_knots)
        * duration_hours
    )

    vessel_end = destination_point(
        origin.latitude,
        origin.longitude,
        heading_degrees,
        vessel_distance_km,
    )

    if current_speed_knots == 0:
        return vessel_end

    current_distance_km = (
        knots_to_kmh(current_speed_knots)
        * duration_hours
    )

    current_end = destination_point(
        origin.latitude,
        origin.longitude,
        current_direction_degrees or 0.0,
        current_distance_km,
    )

    # Convert both displacement vectors into a local tangent-plane
    # approximation around the starting point.
    lat_scale = 111.32
    lon_scale = (
        111.32
        * math.cos(
            math.radians(origin.latitude)
        )
    )

    vessel_dx = (
        vessel_end.longitude
        - origin.longitude
    ) * lon_scale

    vessel_dy = (
        vessel_end.latitude
        - origin.latitude
    ) * lat_scale

    current_dx = (
        current_end.longitude
        - origin.longitude
    ) * lon_scale

    current_dy = (
        current_end.latitude
        - origin.latitude
    ) * lat_scale

    total_dx = vessel_dx + current_dx
    total_dy = vessel_dy + current_dy

    final_lat = origin.latitude + (
        total_dy / lat_scale
    )

    if abs(lon_scale) < 1e-12:
        final_lon = origin.longitude
    else:
        final_lon = origin.longitude + (
            total_dx / lon_scale
        )

    return validate_coordinate(
        final_lat,
        final_lon,
        normalize_lon=True,
    )
