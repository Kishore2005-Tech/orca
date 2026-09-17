from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from agents.safety.agent import AdvisoryFeedItem, SafetyAgent
from agents.safety.schemas import (
    ActivityType,
    AdvisoryType,
    Location,
    PhysicalContext,
    SafetyQuery,
    Severity,
)
from agents.safety.tools import (
    classify_wave_severity,
    classify_wind_severity,
    check_expiry,
    deduplicate_advisories,
)


def now():
    return datetime.now(timezone.utc)


def make_query(
    *,
    activity=ActivityType.FISHING,
    possible_emergency=False,
    physical_context=None,
):
    return SafetyQuery(
        request_id=uuid4(),
        location=Location(
            lat=13.0827,
            lon=80.2707,
        ),
        activity_type=activity,
        physical_context=physical_context,
        possible_emergency=possible_emergency,
    )


def make_advisory(
    *,
    severity=Severity.HIGH,
    advisory_type=AdvisoryType.STORM,
    hours_until_expiry=6,
):
    current = now()

    return AdvisoryFeedItem(
        advisory_type=advisory_type,
        severity=severity,
        region="Chennai Coast",
        issuing_authority="Official Marine Authority",
        issued_at=current - timedelta(hours=1),
        expires_at=current + timedelta(hours=hours_until_expiry),
        guidance_text="Avoid exposed marine activity until conditions improve.",
        source_reference="TEST-ADVISORY-001",
        source_type="government",
    )


def test_wave_below_watch_threshold():
    result = classify_wave_severity(2.0)

    assert result.severity == Severity.LOW


def test_wave_watch_range():
    result = classify_wave_severity(2.7)

    assert result.severity == Severity.MODERATE


def test_wave_alert_threshold():
    result = classify_wave_severity(3.2)

    assert result.severity == Severity.HIGH


def test_negative_wave_height_rejected():
    with pytest.raises(ValueError):
        classify_wave_severity(-1.0)


def test_wind_low():
    result = classify_wind_severity(12.0)

    assert result.severity == Severity.LOW


def test_wind_moderate():
    result = classify_wind_severity(20.0)

    assert result.severity == Severity.MODERATE


def test_wind_high():
    result = classify_wind_severity(28.0)

    assert result.severity == Severity.HIGH


def test_wind_extreme():
    result = classify_wind_severity(40.0)

    assert result.severity == Severity.EXTREME


def test_expired_advisory():
    result = check_expiry(
        now() - timedelta(hours=1),
        now=now(),
    )

    assert result.expired is True
    assert result.active is False


def test_active_advisory():
    result = check_expiry(
        now() + timedelta(hours=2),
        now=now(),
    )

    assert result.active is True
    assert result.expired is False


def test_duplicate_advisories_removed():
    advisory = make_advisory()

    result = deduplicate_advisories(
        [advisory, advisory]
    )

    assert len(result) == 1


def test_agent_returns_active_advisory():
    agent = SafetyAgent()

    result = agent.run(
        make_query(),
        advisories=[
            make_advisory(
                severity=Severity.HIGH,
            )
        ],
    )

    assert result.status == "ok"
    assert len(result.advisories) == 1
    assert result.severity == Severity.HIGH
    assert result.issuing_authority == "Official Marine Authority"


def test_active_advisory_contains_evidence():
    agent = SafetyAgent()

    result = agent.run(
        make_query(),
        advisories=[
            make_advisory(),
        ],
    )

    assert len(result.evidence) == 1
    assert (
        result.evidence[0].issuing_authority
        == "Official Marine Authority"
    )
    assert (
        result.evidence[0].source_reference
        == "TEST-ADVISORY-001"
    )


def test_expired_advisory_is_not_presented_as_active():
    agent = SafetyAgent()

    expired = AdvisoryFeedItem(
        advisory_type=AdvisoryType.STORM,
        severity=Severity.EXTREME,
        region="Chennai Coast",
        issuing_authority="Official Marine Authority",
        issued_at=now() - timedelta(hours=5),
        expires_at=now() - timedelta(hours=1),
        guidance_text="Expired warning.",
        source_reference="EXPIRED-001",
        source_type="government",
    )

    result = agent.run(
        make_query(),
        advisories=[expired],
    )

    assert len(result.advisories) == 0
    assert any(
        warning.code == "ORCA_ERR_STALE_DATA"
        for warning in result.warnings
    )


def test_source_unavailable_does_not_become_all_clear():
    agent = SafetyAgent()

    result = agent.run(
        make_query(),
        source_available=False,
    )

    assert result.status == "error"

    assert "unable to confirm" in (
        result.guidance_text.lower()
    )

    assert "all-clear" in (
        result.guidance_text.lower()
    )

    assert not (
        result.guidance_text.lower()
        .startswith("safe")
    )


def test_source_unavailable_error_code():
    agent = SafetyAgent()

    result = agent.run(
        make_query(),
        source_available=False,
    )

    assert any(
        error.code == "ORCA_ERR_SOURCE_UNAVAILABLE"
        for error in result.errors
    )


def test_possible_emergency_forces_escalation():
    agent = SafetyAgent()

    result = agent.run(
        make_query(
            possible_emergency=True,
        ),
        source_available=False,
    )

    assert result.emergency_escalation.required is True

    assert (
        "emergency services"
        in result.emergency_escalation.instruction.lower()
    )


def test_possible_emergency_even_with_low_severity():
    agent = SafetyAgent()

    result = agent.run(
        make_query(
            possible_emergency=True,
        ),
        advisories=[
            make_advisory(
                severity=Severity.LOW,
            )
        ],
    )

    assert result.emergency_escalation.required is True


def test_ambiguous_location_is_fatal():
    agent = SafetyAgent()

    query = SafetyQuery(
        request_id=uuid4(),
        location=Location(),
        activity_type=ActivityType.FISHING,
    )

    result = agent.run(
        query,
        advisories=[
            make_advisory(),
        ],
    )

    assert result.status == "error"

    assert any(
        error.code == "ORCA_ERR_AMBIGUOUS_LOCATION"
        for error in result.errors
    )


def test_highest_severity_advisory_is_primary():
    agent = SafetyAgent()

    low = make_advisory(
        severity=Severity.LOW,
        advisory_type=AdvisoryType.RIP_CURRENT,
    )

    extreme = make_advisory(
        severity=Severity.EXTREME,
        advisory_type=AdvisoryType.STORM,
    )

    result = agent.run(
        make_query(),
        advisories=[low, extreme],
    )

    assert result.severity == Severity.EXTREME
    assert result.advisory_type == AdvisoryType.STORM


def test_high_source_severity_is_preserved():
    """
    Official advisory severity must not be downgraded by physical
    context.
    """
    agent = SafetyAgent()

    result = agent.run(
        make_query(
            physical_context=[
                PhysicalContext(
                    variable="wave_height",
                    value=1.0,
                    unit="m",
                    observed_at=now(),
                    source="Ocean Agent",
                )
            ]
        ),
        advisories=[
            make_advisory(
                severity=Severity.HIGH,
            )
        ],
    )

    assert result.severity == Severity.HIGH


def test_physical_context_without_advisory_is_general_guidance():
    agent = SafetyAgent()

    query = make_query(
        physical_context=[
            PhysicalContext(
                variable="wave_height",
                value=3.4,
                unit="m",
                observed_at=now(),
                source="Ocean Agent",
            )
        ]
    )

    result = agent.run(
        query,
        advisories=[],
    )

    assert len(result.advisories) == 0
    assert result.confidence_level.value == "low"
    assert "general hazard guidance" in (
        result.guidance_text.lower()
    )


def test_physical_context_is_not_official_advisory():
    agent = SafetyAgent()

    query = make_query(
        physical_context=[
            PhysicalContext(
                variable="wave_height",
                value=3.5,
                unit="m",
                observed_at=now(),
                source="Ocean Agent",
            )
        ]
    )

    result = agent.run(
        query,
        advisories=[],
    )

    assert result.issuing_authority == "Derived physical context"


def test_fishing_activity_is_supported():
    agent = SafetyAgent()

    result = agent.run(
        make_query(
            activity=ActivityType.FISHING,
        ),
        advisories=[
            make_advisory(),
        ],
    )

    assert result.status == "ok"
    assert "fishing" in result.guidance_text.lower()


def test_swimming_activity_is_supported():
    agent = SafetyAgent()

    result = agent.run(
        make_query(
            activity=ActivityType.SWIMMING,
        ),
        advisories=[
            make_advisory(
                advisory_type=AdvisoryType.RIP_CURRENT,
            ),
        ],
    )

    assert result.status == "ok"
    assert "swimming" in result.guidance_text.lower()


def test_missing_advisory_does_not_claim_safe():
    agent = SafetyAgent()

    result = agent.run(
        make_query(),
        advisories=[],
    )

    text = result.guidance_text.lower()

    assert "safe" not in text
    assert "all-clear" in text or "official advisory" in text


def test_result_has_required_contract_fields():
    agent = SafetyAgent()

    result = agent.run(
        make_query(),
        advisories=[
            make_advisory(),
        ],
    )

    assert result.request_id is not None
    assert result.timestamp is not None
    assert result.advisory_type is not None
    assert result.severity is not None
    assert result.issuing_authority
    assert result.issued_at is not None
    assert result.guidance_text
    assert result.emergency_escalation is not None


def test_no_fake_fisheries_regulation():
    agent = SafetyAgent()

    result = agent.run(
        make_query(),
        advisories=[
            make_advisory(),
        ],
    )

    text = result.guidance_text.lower()

    assert "quota" not in text
    assert "license" not in text
    assert "fishing ban" not in text
