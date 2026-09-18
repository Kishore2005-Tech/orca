"""
ORCA Geospatial Utilities.

This package contains deterministic geospatial utilities used by
ORCA's domain agents and orchestration layer.

Modules
-------
coordinate
    Coordinate validation and normalization.

distance
    Geographic distance, bearing, and projected-position calculations.

boundaries
    Polygon/vector boundary validation and point-in-polygon operations.

raster
    Raster/NetCDF spatial subsetting and point extraction.

spatial_query
    PostGIS spatial query helpers.
"""

from backend.geospatial.coordinate import (
    Coordinate,
    CoordinateError,
    normalize_longitude,
    validate_coordinate,
    validate_latitude,
    validate_longitude,
)

from backend.geospatial.distance import (
    haversine_distance_km,
    haversine_distance_nm,
    haversine_distance_m,
    initial_bearing_degrees,
    destination_point,
    project_position,
)

from backend.geospatial.boundaries import (
    BoundingBox,
    PointCoverageResult,
    point_in_polygon,
    point_in_bbox,
    validate_polygon,
    polygon_bbox,
)

from backend.geospatial.raster import (
    RasterError,
    RasterPointValue,
    RasterSubset,
    inspect_raster,
    extract_point_value,
    subset_raster,
)

from backend.geospatial.spatial_query import (
    SpatialQueryError,
    build_observation_radius_query,
    build_point_distance_query,
    build_boundary_intersection_query,
    build_boundary_containment_query,
)

__all__ = [
    "Coordinate",
    "CoordinateError",
    "normalize_longitude",
    "validate_coordinate",
    "validate_latitude",
    "validate_longitude",
    "haversine_distance_km",
    "haversine_distance_nm",
    "haversine_distance_m",
    "initial_bearing_degrees",
    "destination_point",
    "project_position",
    "BoundingBox",
    "PointCoverageResult",
    "point_in_polygon",
    "point_in_bbox",
    "validate_polygon",
    "polygon_bbox",
    "RasterError",
    "RasterPointValue",
    "RasterSubset",
    "inspect_raster",
    "extract_point_value",
    "subset_raster",
    "SpatialQueryError",
    "build_observation_radius_query",
    "build_point_distance_query",
    "build_boundary_intersection_query",
    "build_boundary_containment_query",
]
