from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from agents.ecosystem.agent import EcosystemAgent
from agents.ecosystem.schemas import (
    EcosystemAgentInput,
    EcosystemIndicator,
    Location,
    PhysicalObservation,
    TimeRange,
)
from agents.ecosystem.tools import (
    ChlorophyllObservation,
    EcosystemGridPoint,
    SSTObservation,
    get_chlorophyll,
    get_fronts,
    get_mhw,
    get_upwelling,
)


UTC = timezone.utc


def make_time_range() -> TimeRange:
    """Create a valid ORCA test time range."""

    start = datetime(2026, 8, 1, tzinfo=UTC)
    end = datetime(2026, 8, 10, tzinfo=UTC)

    return TimeRange(start=start, end=end)


def make_input(
    indicator: EcosystemIndicator,
) -> EcosystemAgentInput:
    """Create a valid ecosystem-agent request."""

    return EcosystemAgentInput(
        request_id=uuid4(),
        location=Location(
            lat=13.0827,
            lon=80.2707,
            region_name="Chennai",
        ),
        indicator=indicator,
        time_range=make_time_range(),
    )


def test_chlorophyll_processing_returns_summary() -> None:
    """Chlorophyll observations should be validated and summarized."""

    observations = [
        ChlorophyllObservation(
            value=1.2,
            observed_at=datetime(2026, 8, 1, tzinfo=UTC),
        ),
        ChlorophyllObservation(
            value=2.0,
            observed_at=datetime(2026, 8, 2, tzinfo=UTC),
        ),
        ChlorophyllObservation(
            value=1.8,
            observed_at=datetime(2026, 8, 3, tzinfo=UTC),
        ),
    ]

    result = get_chlorophyll(observations)

    assert result["parameter"] == "chlorophyll_a"
    assert result["unit"] == "mg/m3"
    assert result["count"] == 3
    assert result["latest_value"] == pytest.approx(1.8)
    assert result["minimum"] == pytest.approx(1.2)
    assert result["maximum"] == pytest.approx(2.0)


def test_chlorophyll_rejects_non_positive_values() -> None:
    """Invalid chlorophyll values must not silently pass."""

    observations = [
        ChlorophyllObservation(
            value=0.0,
            observed_at=datetime(2026, 8, 1, tzinfo=UTC),
        )
    ]

    with pytest.raises(ValueError, match="greater than zero"):
        get_chlorophyll(observations)


def test_mhw_detects_five_qualifying_days() -> None:
    """
    The prototype MHW rule requires SST above the 90th percentile
    for at least five observations.
    """

    start = datetime(2026, 8, 1, tzinfo=UTC)

    values = [
        27.0,
        27.1,
        27.2,
        27.3,
        27.4,
        27.5,
        27.6,
        30.0,
        30.1,
        30.2,
        30.3,
        30.4,
        30.5,
        30.6,
        30.7,
        30.8,
        30.9,
        31.0,
        31.1,
        31.2,
    ]

    observations = [
        SSTObservation(
            value_celsius=value,
            observed_at=start + timedelta(days=index),
        )
        for index, value in enumerate(values)
    ]

    result = get_mhw(observations)

    assert result.threshold_celsius > 30.0
    assert result.qualifying_days >= 5
    assert result.detected is True


def test_mhw_does_not_detect_without_five_qualifying_days() -> None:
    """Fewer than five qualifying observations should not trigger MHW."""

    start = datetime(2026, 8, 1, tzinfo=UTC)

    values = [
        27.0,
        27.1,
        27.2,
        27.3,
        27.4,
        27.5,
        27.6,
        27.7,
        27.8,
        27.9,
        28.0,
        28.1,
        28.2,
        28.3,
        28.4,
        31.0,
    ]

    observations = [
        SSTObservation(
            value_celsius=value,
            observed_at=start + timedelta(days=index),
        )
        for index, value in enumerate(values)
    ]

    result = get_mhw(observations)

    assert result.detected is False


def test_front_detection_uses_sst_and_chlorophyll_gradients() -> None:
    """Candidate fronts require both spatial gradients."""

    points = [
        EcosystemGridPoint(
            lat=13.0,
            lon=80.0,
            sst_celsius=26.0,
            chlorophyll_mg_m3=1.0,
        ),
        EcosystemGridPoint(
            lat=13.0,
            lon=80.1,
            sst_celsius=28.0,
            chlorophyll_mg_m3=3.0,
        ),
        EcosystemGridPoint(
            lat=13.0,
            lon=80.2,
            sst_celsius=26.1,
            chlorophyll_mg_m3=1.1,
        ),
    ]

    result = get_fronts(
        points,
        sst_gradient_threshold=5.0,
        chlorophyll_gradient_threshold=5.0,
    )

    assert result
    assert all(item.magnitude > 0 for item in result)


def test_upwelling_detection_requires_cold_sst_and_high_chlorophyll() -> None:
    """Upwelling candidates require both conditions."""

    points = [
        EcosystemGridPoint(
            lat=13.0,
            lon=80.0,
            sst_celsius=24.0,
            chlorophyll_mg_m3=4.0,
        ),
        EcosystemGridPoint(
            lat=13.1,
            lon=80.1,
            sst_celsius=29.0,
            chlorophyll_mg_m3=0.5,
        ),
    ]

    result = get_upwelling(
        points,
        cold_sst_threshold_celsius=25.0,
        high_chlorophyll_threshold_mg_m3=3.0,
    )

    assert len(result) == 1
    assert result[0].detected is True


def test_agent_returns_structured_chlorophyll_result() -> None:
    """The agent must return the ORCA structured response envelope."""

    task = make_input(EcosystemIndicator.CHLOROPHYLL)

    observations = [
        ChlorophyllObservation(
            value=2.0,
            observed_at=datetime(2026, 8, 3, tzinfo=UTC),
            source="ORCA test dataset",
        )
    ]

    result = EcosystemAgent().run(
        task,
        chlorophyll=observations,
    )

    assert result.agent_id == "ecosystem"
    assert result.status == "ok"
    assert result.request_id == task.request_id
    assert len(result.observations) == 1
    assert len(result.evidence) == 1
    assert result.observations[0].indicator == (
        EcosystemIndicator.CHLOROPHYLL
    )


def test_agent_returns_error_when_data_is_missing() -> None:
    """The agent must fail explicitly instead of fabricating data."""

    task = make_input(EcosystemIndicator.CHLOROPHYLL)

    result = EcosystemAgent().run(task)

    assert result.status == "error"
    assert result.observations == []
    assert result.errors
    assert result.errors[0].code == "ORCA_ERR_NO_DATA"
    assert result.errors[0].fatal is True


def test_physical_context_is_not_a_causal_claim() -> None:
    """
    Physical context may create a correlation flag, but causal claims
    must remain false.
    """

    task = make_input(EcosystemIndicator.UPWELLING)

    task.physical_context = [
        PhysicalObservation(
            parameter="sea_surface_temperature",
            value=24.0,
            unit="°C",
            observed_at=datetime(2026, 8, 3, tzinfo=UTC),
            source="ORCA test ocean dataset",
        )
    ]

    points = [
        EcosystemGridPoint(
            lat=13.0,
            lon=80.0,
            sst_celsius=24.0,
            chlorophyll_mg_m3=4.0,
        )
    ]

    result = EcosystemAgent().run(
        task,
        grid_points=points,
    )

    assert result.status == "ok"
    assert result.observations

    correlation = result.observations[0].correlation_flag

    assert correlation is not None
    assert correlation.is_causal_claim is False


def test_fishing_claim_is_not_generated_by_ecosystem_agent() -> None:
    """The ecosystem result must not turn chlorophyll into fish abundance."""

    task = make_input(EcosystemIndicator.CHLOROPHYLL)

    observations = [
        ChlorophyllObservation(
            value=3.0,
            observed_at=datetime(2026, 8, 3, tzinfo=UTC),
        )
    ]

    result = EcosystemAgent().run(
        task,
        chlorophyll=observations,
    )

    text = (
        result.reasoning or ""
    ).lower()

    assert "guaranteed catch" not in text
    assert "fish abundance" not in text
