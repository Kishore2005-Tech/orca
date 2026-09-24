"""
Raster and NetCDF utilities for ORCA.

Primary library:
    xarray

Supported workflow:
    NetCDF / xarray Dataset
        -> inspect
        -> spatial subset
        -> nearest native-grid cell extraction

Important:
    ORCA must not claim sub-grid precision when the source raster
    does not provide it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import math

import xarray as xr

from backend.geospatial.coordinate import (
    CoordinateError,
    validate_coordinate,
)


class RasterError(RuntimeError):
    """Raised when raster processing fails."""


@dataclass(frozen=True)
class RasterPointValue:
    """Value extracted from a native raster grid cell."""

    variable: str
    latitude: float
    longitude: float
    value: Any
    source_latitude: float
    source_longitude: float
    distance_degrees: float
    resolution_latitude_degrees: float | None
    resolution_longitude_degrees: float | None


@dataclass(frozen=True)
class RasterSubset:
    """Spatial subset of an xarray Dataset."""

    dataset: xr.Dataset
    min_latitude: float
    min_longitude: float
    max_latitude: float
    max_longitude: float


def _find_coordinate_name(
    dataset: xr.Dataset,
    candidates: tuple[str, ...],
) -> str:
    """
    Find a latitude/longitude coordinate using common naming conventions.
    """
    available = set(dataset.coords) | set(dataset.dims)

    for candidate in candidates:
        if candidate in available:
            return candidate

    raise RasterError(
        "Could not find required spatial coordinate. "
        f"Expected one of: {candidates}. "
        f"Available coordinates/dimensions: {sorted(available)}"
    )


def _get_lat_lon_names(
    dataset: xr.Dataset,
) -> tuple[str, str]:
    lat_name = _find_coordinate_name(
        dataset,
        (
            "lat",
            "latitude",
            "nav_lat",
            "y",
        ),
    )

    lon_name = _find_coordinate_name(
        dataset,
        (
            "lon",
            "longitude",
            "nav_lon",
            "x",
        ),
    )

    return lat_name, lon_name


def open_raster(
    path: str | Path,
) -> xr.Dataset:
    """
    Open a NetCDF/xarray-compatible dataset.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise RasterError(
            f"Raster file does not exist: {file_path}"
        )

    try:
        return xr.open_dataset(file_path)
    except Exception as exc:
        raise RasterError(
            f"Unable to open raster dataset: {file_path}"
        ) from exc


def inspect_raster(
    dataset: xr.Dataset,
) -> dict[str, Any]:
    """
    Inspect raster metadata without modifying the dataset.
    """
    lat_name, lon_name = _get_lat_lon_names(
        dataset
    )

    lat_values = dataset[lat_name].values
    lon_values = dataset[lon_name].values

    result: dict[str, Any] = {
        "latitude_coordinate": lat_name,
        "longitude_coordinate": lon_name,
        "variables": list(dataset.data_vars),
        "dimensions": {
            key: int(value)
            for key, value in dataset.sizes.items()
        },
        "latitude_min": float(lat_values.min()),
        "latitude_max": float(lat_values.max()),
        "longitude_min": float(lon_values.min()),
        "longitude_max": float(lon_values.max()),
        "crs": dataset.attrs.get(
            "crs",
            "EPSG:4326",
        ),
    }

    result["latitude_resolution_degrees"] = (
        _estimate_resolution(lat_values)
    )

    result["longitude_resolution_degrees"] = (
        _estimate_resolution(lon_values)
    )

    return result


def _estimate_resolution(
    values: Any,
) -> float | None:
    """
    Estimate native grid spacing.

    Returns None when a resolution cannot be determined.
    """
    flattened = [
        float(value)
        for value in values
        if math.isfinite(float(value))
    ]

    if len(flattened) < 2:
        return None

    flattened = sorted(set(flattened))

    if len(flattened) < 2:
        return None

    differences = [
        abs(flattened[index + 1] - flattened[index])
        for index in range(len(flattened) - 1)
    ]

    differences = [
        value
        for value in differences
        if value > 0
    ]

    if not differences:
        return None

    return min(differences)


def _slice_for_coordinate_range(
    coordinate: xr.DataArray,
    minimum: float,
    maximum: float,
) -> slice:
    """
    Build a slice that works for ascending or descending coordinates.
    """
    values = coordinate.values

    if len(values) < 2:
        return slice(minimum, maximum)

    ascending = float(values[0]) <= float(values[-1])

    if ascending:
        return slice(minimum, maximum)

    return slice(maximum, minimum)


def subset_raster(
    dataset: xr.Dataset,
    *,
    min_latitude: float,
    min_longitude: float,
    max_latitude: float,
    max_longitude: float,
) -> RasterSubset:
    """
    Spatially subset a raster using its native coordinates.
    """
    validate_coordinate(
        min_latitude,
        min_longitude,
    )

    validate_coordinate(
        max_latitude,
        max_longitude,
    )

    if min_latitude > max_latitude:
        raise RasterError(
            "min_latitude cannot exceed max_latitude."
        )

    if min_longitude > max_longitude:
        raise RasterError(
            "min_longitude cannot exceed max_longitude."
        )

    lat_name, lon_name = _get_lat_lon_names(
        dataset
    )

    lat_slice = _slice_for_coordinate_range(
        dataset[lat_name],
        min_latitude,
        max_latitude,
    )

    lon_slice = _slice_for_coordinate_range(
        dataset[lon_name],
        min_longitude,
        max_longitude,
    )

    try:
        subset = dataset.sel(
            {
                lat_name: lat_slice,
                lon_name: lon_slice,
            }
        )
    except Exception as exc:
        raise RasterError(
            "Unable to subset raster using latitude/longitude."
        ) from exc

    return RasterSubset(
        dataset=subset,
        min_latitude=min_latitude,
        min_longitude=min_longitude,
        max_latitude=max_latitude,
        max_longitude=max_longitude,
    )


def extract_point_value(
    dataset: xr.Dataset,
    *,
    variable: str,
    latitude: float,
    longitude: float,
) -> RasterPointValue:
    """
    Extract the nearest native-grid value.

    No interpolation is performed.

    This distinction is important for ORCA because the result must
    not imply a finer spatial resolution than the source dataset.
    """
    point = validate_coordinate(
        latitude,
        longitude,
        normalize_lon=True,
    )

    if variable not in dataset.data_vars:
        raise RasterError(
            f"Variable {variable!r} not found in dataset. "
            f"Available variables: {list(dataset.data_vars)}"
        )

    lat_name, lon_name = _get_lat_lon_names(
        dataset
    )

    try:
        selected = dataset[variable].sel(
            {
                lat_name: point.latitude,
                lon_name: point.longitude,
            },
            method="nearest",
        )
    except Exception as exc:
        raise RasterError(
            f"Unable to extract variable {variable!r} "
            "at requested coordinate."
        ) from exc

    source_latitude = float(
        selected[lat_name].values
    )

    source_longitude = float(
        selected[lon_name].values
    )

    raw_value = selected.values

    # Convert scalar numpy values into ordinary Python values
    # where possible.
    try:
        if getattr(raw_value, "ndim", 0) == 0:
            raw_value = raw_value.item()
    except Exception:
        pass

    resolution_lat = _estimate_resolution(
        dataset[lat_name].values
    )

    resolution_lon = _estimate_resolution(
        dataset[lon_name].values
    )

    distance_degrees = math.sqrt(
        (
            point.latitude
            - source_latitude
        ) ** 2
        +
        (
            point.longitude
            - source_longitude
        ) ** 2
    )

    return RasterPointValue(
        variable=variable,
        latitude=point.latitude,
        longitude=point.longitude,
        value=raw_value,
        source_latitude=source_latitude,
        source_longitude=source_longitude,
        distance_degrees=distance_degrees,
        resolution_latitude_degrees=resolution_lat,
        resolution_longitude_degrees=resolution_lon,
    )


def check_raster_coverage(
    dataset: xr.Dataset,
    *,
    latitude: float,
    longitude: float,
) -> bool:
    """
    Check whether a coordinate falls within the raster's spatial extent.

    This checks geographic coverage only; it does not guarantee that
    the selected cell contains a non-null scientific value.
    """
    point = validate_coordinate(
        latitude,
        longitude,
        normalize_lon=True,
    )

    lat_name, lon_name = _get_lat_lon_names(
        dataset
    )

    lat_values = dataset[lat_name].values
    lon_values = dataset[lon_name].values

    lat_min = float(lat_values.min())
    lat_max = float(lat_values.max())
    lon_min = float(lon_values.min())
    lon_max = float(lon_values.max())

    return (
        lat_min <= point.latitude <= lat_max
        and
        lon_min <= point.longitude <= lon_max
    )


def close_raster(
    dataset: xr.Dataset,
) -> None:
    """Close an xarray dataset when it owns an open file."""
    try:
        dataset.close()
    except Exception:
        pass
