from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from agents.ocean.agent import OceanAgent
from agents.ocean.schemas import (
    OceanQuery,
    OceanVariable,
    Location,
    TimeRange,
)
from agents.ocean.tools import (
    OceanDataPoint,
    calculate_z_score,
    detect_thermal_front,
    is_stale_observation,
    validate_physical_value,
)


def make_query(
    variables=None,
    *,
    forecast=False,
):
    now = datetime.now(timezone.utc)

    return OceanQuery(
        request_id=uuid4(),
        location=Location(
            lat=13.0827,
            lon=80.2707,
        ),
        time_range=TimeRange(
            start=now - timedelta(hours=6),
            end=now + timedelta(hours=6),
        ),
        variables=variables or [
            OceanVariable.SST,
        ],
        forecast=forecast,
    )


def make_sst_point(
    *,
    value=28.4,
    hours_old=1,
    forecast=False,
):
    now = datetime.now(timezone.utc)

    return OceanDataPoint(
        variable=OceanVariable.SST,
        value=value,
        unit="degC",
        valid_at=now + timedelta(hours=12) if forecast
        else now - timedelta(hours=hours_old),
        source="Test Ocean Dataset",
        source_type="observation" if not forecast else "model",
        reference="test-ocean-001",
        is_forecast=forecast,
    )


def test_valid_sst_range():
    result = validate_physical_value(
        OceanVariable.SST,
        28.5,
    )

    assert result.valid is True


def test_invalid_sst_is_rejected():
    result = validate_physical_value(
        OceanVariable.SST,
        55.0,
    )

    assert result.valid is False


def test_invalid_salinity_is_rejected():
    result = validate_physical_value(
        OceanVariable.SALINITY,
        60.0,
    )

    assert result.valid is False


def test_future_observation_is_rejected():
    point = make_sst_point(forecast=False)

    future_point = OceanDataPoint(
        variable=point.variable,
        value=point.value,
        unit=point.unit,
        valid_at=datetime.now(timezone.utc) + timedelta(hours=2),
        source=point.source,
        source_type=point.source_type,
        reference=point.reference,
        is_forecast=False,
    )

    agent = OceanAgent()

    valid, message = agent.validate_observation(
        future_point,
    )

    assert valid is False
    assert "future" in message.lower()


def test_future_forecast_is_valid():
    point = make_sst_point(forecast=True)

    agent = OceanAgent()

    valid, message = agent.validate_observation(point)

    assert valid is True


def test_stale_observation_detection():
    old_time = datetime.now(timezone.utc) - timedelta(hours=30)

    assert (
        is_stale_observation(
            old_time,
            max_age_hours=24,
        )
        is True
    )


def test_recent_observation_is_not_stale():
    recent_time = datetime.now(timezone.utc) - timedelta(hours=2)

    assert (
        is_stale_observation(
            recent_time,
            max_age_hours=24,
        )
        is False
    )


def test_sst_gradient():
    agent = OceanAgent()

    result = agent.calculate_sst_gradient(
        sst_a_celsius=28.0,
        sst_b_celsius=30.0,
        distance_km=10.0,
    )

    assert result["value"] == pytest.approx(0.2)
    assert result["unit"] == "degC/km"


def test_thermal_front_detection():
    assert detect_thermal_front(
        0.25,
        threshold_c_per_km=0.2,
    ) is True


def test_no_thermal_front_below_threshold():
    assert detect_thermal_front(
        0.10,
        threshold_c_per_km=0.2,
    ) is False


def test_anomaly_z_score():
    z = calculate_z_score(
        value=30.0,
        baseline_mean=28.0,
        baseline_std=1.0,
    )

    assert z == pytest.approx(2.0)


def test_zero_baseline_std_returns_none():
    z = calculate_z_score(
        value=30.0,
        baseline_mean=28.0,
        baseline_std=0.0,
    )

    assert z is None


def test_agent_processes_sst():
    agent = OceanAgent()

    result = agent.run(
        make_query(),
        data_points=[
            make_sst_point(
                value=28.5,
                hours_old=1,
            )
        ],
    )

    assert result.status == "ok"
    assert len(result.observations) == 1
    assert result.observations[0].variable == OceanVariable.SST
    assert result.observations[0].value == 28.5


def test_agent_preserves_source_evidence():
    agent = OceanAgent()

    result = agent.run(
        make_query(),
        data_points=[
            make_sst_point(),
        ],
    )

    assert len(result.evidence) == 1
    assert result.evidence[0].source == "Test Ocean Dataset"
    assert result.evidence[0].reference == "test-ocean-001"


def test_agent_marks_stale_data():
    agent = OceanAgent()

    result = agent.run(
        make_query(),
        data_points=[
            make_sst_point(
                hours_old=30,
            )
        ],
    )

    assert result.status == "partial"
    assert any(
        warning.code == "ORCA_ERR_STALE_DATA"
        for warning in result.warnings
    )


def test_agent_rejects_invalid_physical_value():
    agent = OceanAgent()

    result = agent.run(
        make_query(),
        data_points=[
            make_sst_point(
                value=60.0,
            )
        ],
    )

    assert result.status == "error"
    assert len(result.observations) == 0
    assert any(
        error.code == "ORCA_ERR_SCHEMA_VALIDATION"
        for error in result.errors
    )


def test_agent_returns_no_data_when_empty():
    agent = OceanAgent()

    result = agent.run(
        make_query(),
        data_points=[],
    )

    assert result.status == "error"
    assert any(
        error.code == "ORCA_ERR_NO_DATA"
        for error in result.errors
    )


def test_agent_requires_location():
    now = datetime.now(timezone.utc)

    query = OceanQuery(
        request_id=uuid4(),
        location=Location(),
        time_range=TimeRange(
            start=now - timedelta(hours=1),
            end=now,
        ),
        variables=[OceanVariable.SST],
    )

    agent = OceanAgent()

    result = agent.run(
        query,
        data_points=[
            make_sst_point(),
        ],
    )

    assert result.status == "error"
    assert any(
        error.code == "ORCA_ERR_NO_DATA"
        for error in result.errors
    )


def test_forecast_is_marked_as_forecast():
    agent = OceanAgent()

    result = agent.run(
        make_query(
            forecast=True,
        ),
        data_points=[
            make_sst_point(
                value=29.0,
                forecast=True,
            )
        ],
    )

    assert result.status == "ok"
    assert result.observations[0].is_forecast is True


def test_agent_supports_multiple_variables():
    agent = OceanAgent()

    query = make_query(
        variables=[
            OceanVariable.SST,
            OceanVariable.SALINITY,
            OceanVariable.WAVE_HEIGHT,
        ]
    )

    now = datetime.now(timezone.utc)

    points = [
        OceanDataPoint(
            variable=OceanVariable.SST,
            value=28.4,
            unit="degC",
            valid_at=now - timedelta(hours=1),
            source="SST Dataset",
            source_type="satellite",
            reference="sst-001",
        ),
        OceanDataPoint(
            variable=OceanVariable.SALINITY,
            value=34.8,
            unit="PSU",
            valid_at=now - timedelta(hours=1),
            source="Salinity Dataset",
            source_type="observation",
            reference="salinity-001",
        ),
        OceanDataPoint(
            variable=OceanVariable.WAVE_HEIGHT,
            value=1.4,
            unit="m",
            valid_at=now - timedelta(hours=1),
            source="Wave Model",
            source_type="model",
            reference="wave-001",
        ),
    ]

    result = agent.run(
        query,
        data_points=points,
    )

    assert result.status == "ok"
    assert len(result.observations) == 3


def test_anomaly_information_is_preserved():
    now = datetime.now(timezone.utc)

    point = OceanDataPoint(
        variable=OceanVariable.SST,
        value=31.0,
        unit="degC",
        valid_at=now - timedelta(hours=1),
        source="SST Dataset",
        source_type="satellite",
        reference="sst-anomaly-001",
        anomaly_z_score=2.7,
        baseline_period="1991-2020",
    )

    agent = OceanAgent()

    result = agent.run(
        make_query(),
        data_points=[point],
    )

    anomaly = result.observations[0].anomaly

    assert anomaly is not None
    assert anomaly.is_anomalous is True
    assert anomaly.z_score == pytest.approx(2.7)
    assert anomaly.baseline_period == "1991-2020"


def test_agent_does_not_add_fisheries_claims():
    agent = OceanAgent()

    result = agent.run(
        make_query(),
        data_points=[
            make_sst_point(),
        ],
    )

    reasoning = (result.reasoning or "").lower()

    assert "catch probability" not in reasoning
    assert "fish presence" not in reasoning
    assert "guaranteed catch" not in reasoning


def test_result_contains_required_envelope_fields():
    agent = OceanAgent()

    result = agent.run(
        make_query(),
        data_points=[
            make_sst_point(),
        ],
    )

    assert result.agent_id == "ocean"
    assert result.request_id is not None
    assert result.timestamp is not None
    assert result.confidence is not None
    assert result.confidence.level is not None
    assert 0.0 <= result.confidence.score <= 1.0
