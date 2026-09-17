from __future__ import annotations

from uuid import UUID

from .prompts import GEOSPATIAL_SYSTEM_PROMPT
from .schemas import (
    ConfidenceLevel,
    CoverageCheck,
    EvidenceItem,
    GeospatialAgentResult,
    GeospatialCandidate,
    GeospatialQuery,
    QueryType,
    ResolutionCheck,
    SpatialResult,
)
from .tools import (
    Feature,
    check_coverage,
    check_resolution,
    find_nearest_feature,
    haversine_distance_km,
    validate_coordinates,
)


class GeospatialAgent:
    """
    ORCA Geospatial Agent.

    Handles coordinate validation, geographic resolution,
    spatial calculations, coverage validation and ambiguity
    preservation.

    External geocoding and GIS providers can be connected through
    adapters later without changing the agent contract.
    """

    agent_id = "geospatial"
    agent_name = "Geospatial Intelligence Agent"

    system_prompt = GEOSPATIAL_SYSTEM_PROMPT

    def __init__(self) -> None:
        self.agent_id = "geospatial"
        self.agent_name = "Geospatial Intelligence Agent"

    def run(
        self,
        query: GeospatialQuery,
        *,
        candidates: list[GeospatialCandidate] | None = None,
        is_ocean: bool | None = None,
        data_available: bool = True,
        coastal_contamination: bool = False,
        native_resolution_m: float | None = None,
        requested_resolution_m: float | None = None,
        features: list[Feature] | None = None,
    ) -> GeospatialAgentResult:
        """
        Execute a geospatial request.

        External services should resolve place names/boundaries and
        pass their authoritative results through `candidates` and
        `features`.
        """

        try:
            self._validate_query_requirements(query)

            resolved_candidates = candidates or []

            if query.lat is not None and query.lon is not None:
                validate_coordinates(query.lat, query.lon)

            coverage = None
            resolution = None
            spatial_result = None

            if query.lat is not None and query.lon is not None:
                coverage_raw = check_coverage(
                    query.lat,
                    query.lon,
                    is_ocean=is_ocean,
                    data_available=data_available,
                    coastal_contamination=coastal_contamination,
                )

                coverage = CoverageCheck(
                    is_covered=coverage_raw.is_covered,
                    is_ocean=coverage_raw.is_ocean,
                    coastal_contamination=coverage_raw.coastal_contamination,
                    data_gap=coverage_raw.data_gap,
                    message=coverage_raw.message,
                )

            if (
                native_resolution_m is not None
                or requested_resolution_m is not None
            ):
                resolution_raw = check_resolution(
                    native_resolution_m=native_resolution_m,
                    requested_resolution_m=requested_resolution_m,
                )

                resolution = ResolutionCheck(
                    is_valid=resolution_raw.is_valid,
                    native_resolution_m=resolution_raw.native_resolution_m,
                    requested_resolution_m=resolution_raw.requested_resolution_m,
                    no_subgrid_inference=True,
                    message=resolution_raw.message,
                )

            if query.query_type == QueryType.DISTANCE:
                spatial_result = self._distance_operation(query, resolved_candidates)

            elif query.query_type == QueryType.CONTAINMENT:
                spatial_result = self._containment_operation(
                    query,
                    resolved_candidates,
                )

            elif query.query_type == QueryType.NEAREST_FEATURE:
                spatial_result = self._nearest_feature_operation(
                    query,
                    features or [],
                )

            ambiguity = len(resolved_candidates) > 1

            confidence = self._derive_confidence(
                resolved_candidates,
                ambiguous=ambiguity,
            )

            warnings = []

            if ambiguity:
                warnings.append(
                    "Multiple plausible geographic candidates were returned; "
                    "downstream components must disambiguate before relying "
                    "on jurisdiction-specific results."
                )

            if coverage and coverage.coastal_contamination:
                warnings.append(
                    "Coastal contamination is flagged for this spatial result."
                )

            if coverage and coverage.data_gap:
                warnings.append(
                    "A spatial data gap was detected."
                )

            if resolution and not resolution.is_valid:
                warnings.append(
                    "Requested spatial resolution exceeds the supported "
                    "native resolution."
                )

            evidence = self._collect_evidence(resolved_candidates)

            return GeospatialAgentResult(
                status="success",
                query_type=query.query_type,
                candidates=resolved_candidates,
                is_ambiguous=ambiguity,
                spatial_result=spatial_result,
                resolution=resolution,
                coverage=coverage,
                confidence=confidence,
                evidence=evidence,
                warnings=warnings,
            )

        except ValueError as exc:
            return self._error_result(
                query.query_type,
                "ORCA_ERR_NO_DATA",
                str(exc),
            )

        except Exception as exc:
            return self._error_result(
                query.query_type,
                "ORCA_ERR_SOURCE_UNAVAILABLE",
                str(exc),
            )

    def validate_coordinate_pair(
        self,
        lat: float,
        lon: float,
    ) -> bool:
        """
        Validate a WGS84 coordinate pair.
        """

        try:
            validate_coordinates(lat, lon)
            return True
        except ValueError:
            return False

    def calculate_distance(
        self,
        first_lat: float,
        first_lon: float,
        second_lat: float,
        second_lon: float,
    ) -> float:
        """
        Calculate great-circle distance in kilometres.
        """

        return haversine_distance_km(
            first_lat,
            first_lon,
            second_lat,
            second_lon,
        )

    def _validate_query_requirements(
        self,
        query: GeospatialQuery,
    ) -> None:
        if query.query_type == QueryType.GEOCODE:
            if not query.place_name:
                raise ValueError(
                    "place_name is required for geocode requests."
                )

        elif query.query_type == QueryType.REVERSE_GEOCODE:
            if query.lat is None or query.lon is None:
                raise ValueError(
                    "lat and lon are required for reverse_geocode requests."
                )

        elif query.query_type == QueryType.JURISDICTION_LOOKUP:
            if (
                query.lat is None
                and query.lon is None
                and not query.place_name
                and not query.geometry_ref
            ):
                raise ValueError(
                    "A coordinate, place_name, or geometry_ref is required "
                    "for jurisdiction lookup."
                )

        elif query.query_type in {
            QueryType.CONTAINMENT,
            QueryType.DISTANCE,
            QueryType.NEAREST_FEATURE,
        }:
            if query.lat is None or query.lon is None:
                raise ValueError(
                    f"lat and lon are required for {query.query_type.value}."
                )

    def _distance_operation(
        self,
        query: GeospatialQuery,
        candidates: list[GeospatialCandidate],
    ) -> SpatialResult:
        if query.lat is None or query.lon is None:
            raise ValueError("Distance operation requires coordinates.")

        if not candidates:
            raise ValueError(
                "Distance operation requires at least one resolved candidate."
            )

        candidate = candidates[0]

        distance = haversine_distance_km(
            query.lat,
            query.lon,
            candidate.lat,
            candidate.lon,
        )

        return SpatialResult(
            distance_km=distance,
        )

    def _containment_operation(
        self,
        query: GeospatialQuery,
        candidates: list[GeospatialCandidate],
    ) -> SpatialResult:
        """
        Containment is normally supplied by an authoritative GIS
        polygon operation.

        This method does not invent polygon geometry. If a candidate
        exists, its presence is reported as unresolved containment
        rather than being treated as proof of containment.
        """

        if not candidates:
            return SpatialResult(
                contains=None,
            )

        return SpatialResult(
            contains=None,
        )

    def _nearest_feature_operation(
        self,
        query: GeospatialQuery,
        features: list[Feature],
    ) -> SpatialResult:
        if query.lat is None or query.lon is None:
            raise ValueError(
                "Nearest-feature operation requires coordinates."
            )

        feature, distance = find_nearest_feature(
            query.lat,
            query.lon,
            features,
        )

        if feature is None:
            raise ValueError(
                "No feature with usable geographic coordinates was supplied."
            )

        return SpatialResult(
            nearest_feature_name=feature.name,
            distance_km=distance,
        )

    def _derive_confidence(
        self,
        candidates: list[GeospatialCandidate],
        *,
        ambiguous: bool,
    ) -> ConfidenceLevel | None:
        if not candidates:
            return None

        if ambiguous:
            return ConfidenceLevel.MEDIUM

        return candidates[0].confidence

    def _collect_evidence(
        self,
        candidates: list[GeospatialCandidate],
    ) -> list[EvidenceItem]:
        evidence: list[EvidenceItem] = []

        for candidate in candidates:
            evidence.extend(candidate.evidence)

        return evidence

    def _error_result(
        self,
        query_type: QueryType,
        code: str,
        message: str,
    ) -> GeospatialAgentResult:
        return GeospatialAgentResult(
            status="error",
            query_type=query_type,
            candidates=[],
            is_ambiguous=False,
            confidence=None,
            evidence=[],
            errors=[f"{code}: {message}"],
        )
