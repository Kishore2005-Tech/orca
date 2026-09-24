"""
PostGIS spatial query helpers for ORCA.

The functions in this module generate parameterized SQLAlchemy
statements. They do not execute queries themselves.

Why this separation?
--------------------
The geospatial layer defines WHAT spatial operation is required.
The repository/database layer decides HOW and WHEN the query
is executed.

This keeps the deterministic spatial logic testable.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause


class SpatialQueryError(ValueError):
    """Raised when a spatial query cannot be constructed safely."""


def build_observation_radius_query(
    *,
    variable_type: str | None = None,
    data_type: str | None = None,
    limit: int = 500,
) -> TextClause:
    """
    Build ORCA's canonical observation-radius query.

    Spatial tolerance comes from the DataSource record.

    Conceptually:

        observation
            -> source spatial tolerance
            -> requested location
            -> ST_DWithin

    Parameters are bound safely through SQLAlchemy.
    """
    if limit <= 0:
        raise SpatialQueryError(
            "limit must be greater than zero."
        )

    if limit > 5000:
        raise SpatialQueryError(
            "limit cannot exceed 5000."
        )

    conditions = [
        """
        ST_DWithin(
            o.geom::geography,
            l.geom::geography,
            COALESCE(ds.spatial_tolerance_m, 0)
        )
        """
    ]

    if variable_type is not None:
        conditions.append(
            "o.variable_type = :variable_type"
        )

    if data_type is not None:
        conditions.append(
            "o.data_type = :data_type"
        )

    where_clause = " AND ".join(
        f"({condition})"
        for condition in conditions
    )

    query = f"""
        SELECT
            o.observation_id,
            o.source_id,
            o.location_id,
            o.geom,
            o.variable_type,
            o.value,
            o.unit,
            o.data_type,
            o.observed_at,
            o.valid_until,
            o.retrieved_at,
            o.quality_flag,
            o.raw_payload,
            ds.provider_name,
            ds.dataset_name,
            ds.spatial_tolerance_m,
            ST_Distance(
                o.geom::geography,
                l.geom::geography
            ) AS distance_m
        FROM observations AS o
        JOIN data_sources AS ds
            ON ds.source_id = o.source_id
        CROSS JOIN locations AS l
        WHERE l.location_id = :location_id
          AND ds.is_active = TRUE
          AND {where_clause}
        ORDER BY distance_m ASC, o.observed_at DESC
        LIMIT :limit
    """

    return text(query).bindparams(
        limit=limit,
    )


def build_point_distance_query(
    *,
    table_name: str,
    geometry_column: str = "geom",
    limit: int = 100,
) -> TextClause:
    """
    Build a generic nearest-feature query.

    IMPORTANT:
        table_name and geometry_column are identifiers, not values,
        so they are deliberately restricted to safe SQL identifier
        characters.
    """
    _validate_identifier(
        table_name,
        "table_name",
    )

    _validate_identifier(
        geometry_column,
        "geometry_column",
    )

    if limit <= 0:
        raise SpatialQueryError(
            "limit must be greater than zero."
        )

    if limit > 5000:
        raise SpatialQueryError(
            "limit cannot exceed 5000."
        )

    query = f"""
        SELECT
            t.*,
            ST_Distance(
                t.{geometry_column}::geography,
                ST_SetSRID(
                    ST_MakePoint(
                        :longitude,
                        :latitude
                    ),
                    4326
                )::geography
            ) AS distance_m
        FROM {table_name} AS t
        WHERE t.{geometry_column} IS NOT NULL
        ORDER BY distance_m ASC
        LIMIT :limit
    """

    return text(query).bindparams(
        limit=limit,
    )


def build_boundary_intersection_query(
    *,
    table_name: str,
    geometry_column: str = "geom",
) -> TextClause:
    """
    Build a PostGIS ST_Intersects query.

    Useful for:
        - PFZ overlap
        - marine protected areas
        - hazard areas
        - fishing restrictions
        - vessel tracks vs boundaries
    """
    _validate_identifier(
        table_name,
        "table_name",
    )

    _validate_identifier(
        geometry_column,
        "geometry_column",
    )

    query = f"""
        SELECT
            t.*
        FROM {table_name} AS t
        WHERE t.{geometry_column} IS NOT NULL
          AND ST_Intersects(
              t.{geometry_column}::geography,
              ST_SetSRID(
                  ST_GeomFromText(
                      :geometry_wkt
                  ),
                  4326
              )::geography
          )
    """

    return text(query)


def build_boundary_containment_query(
    *,
    table_name: str,
    geometry_column: str = "geom",
) -> TextClause:
    """
    Build a PostGIS ST_Contains query for point containment.

    Useful for:
        - EEZ membership
        - MPA containment
        - PFZ membership
        - administrative/marine zone checks
    """
    _validate_identifier(
        table_name,
        "table_name",
    )

    _validate_identifier(
        geometry_column,
        "geometry_column",
    )

    query = f"""
        SELECT
            t.*
        FROM {table_name} AS t
        WHERE t.{geometry_column} IS NOT NULL
          AND ST_Contains(
              t.{geometry_column},
              ST_SetSRID(
                  ST_MakePoint(
                      :longitude,
                      :latitude
                  ),
                  4326
              )
          )
    """

    return text(query)


def build_distance_to_boundary_query(
    *,
    table_name: str,
    geometry_column: str = "geom",
) -> TextClause:
    """
    Build a query returning distance from a point to each boundary.

    Distance is returned in metres.
    """
    _validate_identifier(
        table_name,
        "table_name",
    )

    _validate_identifier(
        geometry_column,
        "geometry_column",
    )

    query = f"""
        SELECT
            t.*,
            ST_Distance(
                t.{geometry_column}::geography,
                ST_SetSRID(
                    ST_MakePoint(
                        :longitude,
                        :latitude
                    ),
                    4326
                )::geography
            ) AS distance_m
        FROM {table_name} AS t
        WHERE t.{geometry_column} IS NOT NULL
        ORDER BY distance_m ASC
    """

    return text(query)


def _validate_identifier(
    value: str,
    field_name: str,
) -> None:
    """
    Validate an SQL identifier.

    SQLAlchemy parameters cannot safely parameterize table/column
    names, so these values must be validated before interpolation.
    """
    if not value:
        raise SpatialQueryError(
            f"{field_name} cannot be empty."
        )

    if not value.replace("_", "").isalnum():
        raise SpatialQueryError(
            f"Unsafe SQL identifier for {field_name}: {value!r}"
        )

    if not (
        value[0].isalpha()
        or value[0] == "_"
    ):
        raise SpatialQueryError(
            f"Invalid SQL identifier for {field_name}: {value!r}"
        )
