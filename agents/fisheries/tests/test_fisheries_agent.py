from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest

from agents.fisheries.agent import FisheriesAgent
from agents.fisheries.schemas import (
    ActivityType,
    BathymetryInput,
    FishingQuery,
    Location,
    OceanFishingInputs,
)
from agents.fisheries.tools import (
    Bathymetry,
    PFZInputs,
    get_habitat_suitability,
    get_pfz,
    get_pfz_drift,
    validate_bathymetry,
)


UTC = timezone.utc


def make_query(
    *,
    species: str | None = None,
) -> FishingQuery:
    """Create a valid ORCA Fisheries request."""

    return FishingQuery(
        request_id=uuid4(),
        location=Location(
            lat=13.0827,
            lon=80.2707,
            region_name="Chennai",
            jurisdiction="Tamil Nadu",
        ),
        species=species,
        gear_type="gillnet",
        activity_type=ActivityType.COMMERCIAL,
        date=datetime(
            2026,
            9,
            17,
            tzinfo=UTC,
        ),
    )


def make_ocean_inputs() -> OceanFishingInputs:
    """Create representative environmental observations."""

    return OceanFishingInputs(
        sst_celsius=28.2,
        chlorophyll_mg_m3=0.85,
        sst_gradient_c_per_km=0.45,
        thermal_front_detected=True,
        current_speed_m_s=0.4,
        current_direction_deg=90.0,
        wind_speed_m_s=5.0,
        wind_direction_deg=60.0,
        observed_at=datetime(
            2026,
            9,
            17,
            4,
            0,
            tzinfo=UTC,
        ),
        source="ORCA test ocean dataset",
    )


def make_bathymetry() -> BathymetryInput:
    """Create a compatible pelagic depth range."""

    return BathymetryInput(
        depth_m=30.0,
        min_depth_m=15.0,
        max_depth_m=100.0,
    )


def test_pfz_generation_combines_environmental_indicators() -> None:
    """Strong SST/chlorophyll/front conditions should produce a PFZ."""

    result = get_pfz(
        PFZInputs(
            sst_celsius=28.2,
            chlorophyll_mg_m3=0.85,
            sst_gradient_c_per_km=0.45,
            thermal_front_detected=True,
        )
    )

    assert result.detected is True
    assert result.score >= 60
    assert result.score <= 100

    assert any(
        "chlorophyll" in reason.lower()
        for reason in result.reasons
    )

    assert any(
        "gradient" in reason.lower()
        or "front" in reason.lower()
        for reason in result.reasons
    )


def test_pfz_is_lower_when_environmental_conditions_are_weak() -> None:
    """Weak indicators should not automatically create a strong PFZ."""

    result = get_pfz(
        PFZInputs(
            sst_celsius=30.5,
            chlorophyll_mg_m3=0.1,
            sst_gradient_c_per_km=0.05,
            thermal_front_detected=False,
        )
    )

    assert result.detected is False
    assert result.score < 60


def test_bathymetry_validation_accepts_valid_depth() -> None:
    """Depth inside the supplied range should pass."""

    bathymetry = Bathymetry(
        depth_m=30.0,
        minimum_depth_m=15.0,
        maximum_depth_m=100.0,
    )

    assert validate_bathymetry(bathymetry) is True


def test_bathymetry_validation_rejects_shallow_location() -> None:
    """Depth below the configured minimum should fail."""

    bathymetry = Bathymetry(
        depth_m=8.0,
        minimum_depth_m=15.0,
        maximum_depth_m=100.0,
    )

    assert validate_bathymetry(bathymetry) is False


def test_bathymetry_validation_rejects_deep_location() -> None:
    """Depth above the configured maximum should fail."""

    bathymetry = Bathymetry(
        depth_m=150.0,
        minimum_depth_m=15.0,
        maximum_depth_m=100.0,
    )

    assert validate_bathymetry(bathymetry) is False


def test_habitat_suitability_uses_pfz_and_bathymetry() -> None:
    """Habitat score should account for depth compatibility."""

    pfz = get_pfz(
        PFZInputs(
            sst_celsius=28.2,
            chlorophyll_mg_m3=0.85,
            sst_gradient_c_per_km=0.45,
            thermal_front_detected=True,
        )
    )

    habitat = get_habitat_suitability(
        pfz,
        Bathymetry(
            depth_m=30.0,
            minimum_depth_m=15.0,
            maximum_depth_m=100.0,
        ),
    )

    assert habitat.depth_valid is True
    assert habitat.score == pfz.score
    assert habitat.category in {
        "high",
        "moderate",
        "low",
    }


def test_invalid_bathymetry_reduces_habitat_score() -> None:
    """An unsuitable depth should reduce the habitat indicator."""

    pfz = get_pfz(
        PFZInputs(
            sst_celsius=28.2,
            chlorophyll_mg_m3=0.85,
            sst_gradient_c_per_km=0.45,
            thermal_front_detected=True,
        )
    )

    habitat = get_habitat_suitability(
        pfz,
        Bathymetry(
            depth_m=5.0,
            minimum_depth_m=15.0,
            maximum_depth_m=100.0,
        ),
    )

    assert habitat.depth_valid is False
    assert habitat.score < pfz.score
    assert habitat.limitations


def test_pfz_drift_uses_current_and_wind() -> None:
    """Current and wind should produce a non-zero drift estimate."""

    drift = get_pfz_drift(
        current_speed_m_s=0.4,
        current_direction_deg=90.0,
        wind_speed_m_s=5.0,
        wind_direction_deg=60.0,
        hours=6.0,
    )

    assert drift.displacement_km > 0
    assert drift.displacement_nm > 0
    assert 0.0 <= drift.direction_deg < 360.0


def test_zero_environmental_velocity_has_zero_drift() -> None:
    """No current and no wind should produce no displacement."""

    drift = get_pfz_drift(
        current_speed_m_s=0.0,
        current_direction_deg=0.0,
        wind_speed_m_s=0.0,
        wind_direction_deg=0.0,
        hours=6.0,
    )

    assert drift.displacement_km == pytest.approx(0.0)
    assert drift.displacement_nm == pytest.approx(0.0)


def test_agent_returns_structured_pfz_result() -> None:
    """FisheriesAgent should return a structured ORCA result."""

    query = make_query(
        species="Indian Mackerel",
    )

    result = FisheriesAgent().run(
        query,
        ocean=make_ocean_inputs(),
        bathymetry=make_bathymetry(),
        drift_hours=6.0,
    )

    assert result.agent_id == "fisheries"
    assert result.status == "ok"
    assert result.request_id == query.request_id

    assert result.pfz is not None
    assert result.habitat is not None
    assert result.drift is not None

    assert result.pfz.score >= 0
    assert result.pfz.score <= 100

    assert result.habitat.depth_valid is True

    assert result.evidence

    assert result.is_informational_only is True


def test_agent_fails_when_ocean_data_is_missing() -> None:
    """The agent must not invent ocean observations."""

    query = make_query()

    result = FisheriesAgent().run(
        query,
        ocean=None,
        bathymetry=make_bathymetry(),
    )

    assert result.status == "error"
    assert result.pfz is None
    assert result.habitat is None
    assert result.errors

    assert "ORCA_ERR_NO_DATA" in result.errors[0]


def test_agent_fails_when_bathymetry_is_missing() -> None:
    """Bathymetry is required for the PFZ habitat validation step."""

    query = make_query()

    result = FisheriesAgent().run(
        query,
        ocean=make_ocean_inputs(),
        bathymetry=None,
    )

    assert result.status == "error"
    assert result.errors

    assert "ORCA_ERR_NO_DATA" in result.errors[0]


def test_agent_marks_result_informational_only() -> None:
    """The Fisheries Agent must never turn its output into an authority."""

    query = make_query()

    result = FisheriesAgent().run(
        query,
        ocean=make_ocean_inputs(),
        bathymetry=make_bathymetry(),
    )

    assert result.is_informational_only is True


def test_agent_does_not_guarantee_catch() -> None:
    """
    PFZ/habitat output must remain qualified.

    This prevents the Fisheries Agent from turning an environmental
    indicator into a deterministic catch prediction.
    """

    query = make_query(
        species="Indian Mackerel",
    )

    result = FisheriesAgent().run(
        query,
        ocean=make_ocean_inputs(),
        bathymetry=make_bathymetry(),
    )

    text = (
        result.interpretation or ""
    ).lower()

    assert "guarantee" in text
    assert "catch" in text

    assert "guaranteed catch" not in text


def test_drift_hours_must_be_positive() -> None:
    """Invalid drift duration should be rejected."""

    with pytest.raises(ValueError):
        get_pfz_drift(
            current_speed_m_s=0.4,
            current_direction_deg=90.0,
            wind_speed_m_s=5.0,
            wind_direction_deg=60.0,
            hours=0.0,
        )


def test_invalid_pfz_inputs_are_rejected() -> None:
    """Invalid environmental values must not silently pass."""

    with pytest.raises(ValueError):
        get_pfz(
            PFZInputs(
                sst_celsius=28.0,
                chlorophyll_mg_m3=-1.0,
                sst_gradient_c_per_km=0.4,
            )
        )
