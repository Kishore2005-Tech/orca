from uuid import uuid4

import pytest

from agents.geospatial.agent import GeospatialAgent
from agents.geospatial.schemas import (
    ConfidenceLevel,
    EvidenceItem,
    GeospatialCandidate,
    GeospatialQuery,
    QueryType,
)
from agents.geospatial.tools import (
    Feature,
    Coordinate,
    check_coverage,
    check_resolution,
    haversine_distance_km,
    normalize_longitude,
    validate_coordinates,
)


@pytest.fixture
def agent() -> GeospatialAgent:
    return GeospatialAgent()


def make_candidate(
    name: str,
    lat: float,
    lon: float,
    *,
    jurisdiction: str | None = None,
    maritime_zone: str | None = None,
) -> GeospatialCandidate:
    return GeospatialCandidate(
        canonical_name=name,
        lat=lat,
        lon=lon,
        jurisdiction=jurisdiction,
        maritime_zone=maritime_zone,
        boundary_dataset="ORCA-Test-Boundaries",
        boundary_dataset_vintage="2026-01-01",
        confidence=ConfidenceLevel.HIGH,
        evidence=[
            EvidenceItem(
                source="ORCA test boundary source",
                dataset="ORCA-Test-Boundaries",
                vintage="2026-01-01",
                description="Test boundary evidence.",
            )
        ],
    )


def test_valid_wgs84_coordinates():
    coordinate = validate_coordinates(
        13.0827,
        80.2707,
    )

    assert coordinate.lat == pytest.approx(13.0827)
    assert coordinate.lon == pytest.approx(80.2707)


@pytest.mark.parametrize(
    "lat,lon",
    [
        (91.0, 80.0),
        (-91.0, 80.0),
        (13.0, 181.0),
        (13.0, -181.0),
    ],
)
def test_invalid_coordinates_are_rejected(lat, lon):
    with pytest.raises(ValueError):
        validate_coordinates(lat, lon)


def test_agent_coordinate_validation(agent):
    assert agent.validate_coordinate_pair(13.0, 80.0) is True
    assert agent.validate_coordinate_pair(95.0, 80.0) is False


def test_resolution_accepts_native_resolution():
    result = check_resolution(
        native_resolution_m=1000,
        requested_resolution_m=2000,
    )

    assert result.is_valid is True


def test_resolution_rejects_subgrid_request():
    result = check_resolution(
        native_resolution_m=1000,
        requested_resolution_m=500,
    )

    assert result.is_valid is False
    assert "sub-grid" in result.message


def test_coverage_flags_data_gap():
    result = check_coverage(
        13.0,
        80.0,
        data_available=False,
    )

    assert result.is_covered is False
    assert result.data_gap is True


def test_coverage_flags_coastal_contamination():
    result = check_coverage(
        13.0,
        80.0,
        is_ocean=True,
        coastal_contamination=True,
    )

    assert result.is_covered is True
    assert result.coastal_contamination is True


def test_distance_calculation():
    distance = haversine_distance_km(
        13.0827,
        80.2707,
        13.1000,
        80.3000,
    )

    assert distance > 0


def test_agent_geocode_success(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.GEOCODE,
        place_name="Chennai",
    )

    candidate = make_candidate(
        "Chennai",
        13.0827,
        80.2707,
        jurisdiction="Tamil Nadu, India",
    )

    result = agent.run(
        query,
        candidates=[candidate],
    )

    assert result.status == "success"
    assert result.is_ambiguous is False
    assert len(result.candidates) == 1
    assert result.candidates[0].canonical_name == "Chennai"


def test_multiple_candidates_are_marked_ambiguous(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.GEOCODE,
        place_name="Port",
    )

    candidates = [
        make_candidate("Port A", 13.0, 80.0),
        make_candidate("Port B", 12.0, 80.5),
    ]

    result = agent.run(
        query,
        candidates=candidates,
    )

    assert result.status == "success"
    assert result.is_ambiguous is True
    assert len(result.candidates) == 2


def test_reverse_geocode_requires_coordinates(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.REVERSE_GEOCODE,
    )

    result = agent.run(query)

    assert result.status == "error"
    assert "ORCA_ERR_NO_DATA" in result.errors[0]


def test_reverse_geocode_with_coordinates(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.REVERSE_GEOCODE,
        lat=13.0827,
        lon=80.2707,
    )

    candidate = make_candidate(
        "Chennai",
        13.0827,
        80.2707,
        jurisdiction="Tamil Nadu, India",
    )

    result = agent.run(
        query,
        candidates=[candidate],
        is_ocean=False,
    )

    assert result.status == "success"
    assert result.coverage is not None
    assert result.coverage.is_ocean is False


def test_jurisdiction_evidence_is_preserved(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.JURISDICTION_LOOKUP,
        lat=13.0,
        lon=80.0,
    )

    candidate = make_candidate(
        "Chennai Coast",
        13.0,
        80.0,
        jurisdiction="Tamil Nadu, India",
        maritime_zone="Territorial Sea",
    )

    result = agent.run(
        query,
        candidates=[candidate],
        is_ocean=True,
    )

    assert result.status == "success"
    assert result.candidates[0].jurisdiction == "Tamil Nadu, India"
    assert result.candidates[0].maritime_zone == "Territorial Sea"
    assert len(result.evidence) == 1


def test_distance_query(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.DISTANCE,
        lat=13.0827,
        lon=80.2707,
    )

    candidate = make_candidate(
        "Reference Point",
        13.1000,
        80.3000,
    )

    result = agent.run(
        query,
        candidates=[candidate],
    )

    assert result.status == "success"
    assert result.spatial_result is not None
    assert result.spatial_result.distance_km is not None
    assert result.spatial_result.distance_km > 0


def test_nearest_feature(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.NEAREST_FEATURE,
        lat=13.0827,
        lon=80.2707,
    )

    features = [
        Feature(
            name="Far Feature",
            feature_type="mpa",
            center=Coordinate(
                lat=15.0,
                lon=82.0,
            ),
        ),
        Feature(
            name="Nearest Feature",
            feature_type="mpa",
            center=Coordinate(
                lat=13.09,
                lon=80.28,
            ),
        ),
    ]

    result = agent.run(
        query,
        features=features,
    )

    assert result.status == "success"
    assert result.spatial_result is not None
    assert result.spatial_result.nearest_feature_name == "Nearest Feature"


def test_missing_nearest_feature_data_returns_error(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.NEAREST_FEATURE,
        lat=13.0,
        lon=80.0,
    )

    result = agent.run(
        query,
        features=[],
    )

    assert result.status == "error"
    assert "ORCA_ERR_NO_DATA" in result.errors[0]


def test_land_classification_is_preserved(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.REVERSE_GEOCODE,
        lat=13.0827,
        lon=80.2707,
    )

    result = agent.run(
        query,
        candidates=[],
        is_ocean=False,
    )

    assert result.status == "success"
    assert result.coverage is not None
    assert result.coverage.is_ocean is False


def test_subgrid_resolution_warning(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.REVERSE_GEOCODE,
        lat=13.0827,
        lon=80.2707,
    )

    result = agent.run(
        query,
        native_resolution_m=1000,
        requested_resolution_m=250,
    )

    assert result.status == "success"
    assert result.resolution is not None
    assert result.resolution.is_valid is False
    assert len(result.warnings) > 0


def test_longitude_normalization():
    assert normalize_longitude(190) == pytest.approx(-170)
    assert normalize_longitude(-190) == pytest.approx(170)
    assert normalize_longitude(80) == pytest.approx(80)


def test_no_best_guess_when_multiple_candidates(agent):
    query = GeospatialQuery(
        request_id=uuid4(),
        query_type=QueryType.GEOCODE,
        place_name="Springfield",
    )

    candidates = [
        make_candidate("Springfield A", 10.0, 20.0),
        make_candidate("Springfield B", 30.0, 40.0),
    ]

    result = agent.run(
        query,
        candidates=candidates,
    )

    assert result.is_ambiguous is True
    assert len(result.candidates) == 2
