from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from agents.verification.agent import VerificationAgent
from agents.verification.confidence import (
    confidence_label_consistent,
    downgrade_for_verdict,
    minimum_confidence,
)
from agents.verification.conflict_checker import (
    check_consistency,
    values_conflict,
)
from agents.verification.validators import (
    causal_language_has_explicit_citation,
    contains_unsupported_causal_language,
    evidence_has_provenance,
    timestamp_is_valid,
)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def make_evidence(
    *,
    source_id="INCOIS",
    source_name="INCOIS Ocean Observation",
):
    return {
        "source_id": source_id,
        "source_name": source_name,
        "data_type": "observation",
        "retrieved_at": now_iso(),
        "raw_value": 28.2,
        "spatial_relevance": 0.95,
        "temporal_relevance": 0.95,
        "provenance_url": "https://example.org/source",
    }


def make_envelope(
    *,
    agent_id="ocean",
    final_answer="SST is 28.2 degC.",
    confidence="high",
    observations=None,
    evidence=None,
):
    if observations is None:
        observations = [
            {
                "variable": "sst",
                "value": 28.2,
                "unit": "degC",
                "valid_at": now_iso(),
                "is_forecast": False,
            }
        ]

    if evidence is None:
        evidence = [
            make_evidence()
        ]

    return {
        "request_id": str(uuid4()),
        "query": "Ocean conditions",
        "timestamp": now_iso(),
        "intent": "fact_lookup",
        "final_answer": final_answer,
        "contributing_agents": [agent_id],
        "verification_verdict": "PASS",
        "final_confidence": {
            "level": confidence,
            "score": 0.85,
            "tier_weight_component": 0.9,
            "spatial_coverage_component": 0.95,
            "temporal_freshness_component": 0.95,
            "basis": "Recent authoritative observation.",
        },
        "reasoning_trace": [],
        "observations": observations,
        "evidence": evidence,
        "citations": [],
        "caveats": [],
        "unresolved_conflicts": [],
    }


def test_agent_identity():
    agent = VerificationAgent()

    assert agent.agent_id == "verification"


def test_claim_extraction():
    agent = VerificationAgent()

    claims = agent.extract_claims(
        "SST is 28.2 degC. "
        "Wave height is 1.2 m. "
        "Check official warnings."
    )

    assert len(claims) == 3
    assert claims[0] == "SST is 28.2 degC."


def test_empty_draft_fails_closed():
    agent = VerificationAgent()

    result = agent.run(
        request_id=uuid4(),
        draft_answer="",
        contributing_envelopes=[
            make_envelope()
        ],
    )

    assert result["overall_verdict"] == "fail"


def test_no_envelopes_fails_closed():
    agent = VerificationAgent()

    result = agent.run(
        request_id=uuid4(),
        draft_answer="SST is 28.2 degC.",
        contributing_envelopes=[],
    )

    assert result["overall_verdict"] == "fail"


def test_supported_claim_passes():
    agent = VerificationAgent()

    envelope = make_envelope()

    result = agent.run(
        request_id=uuid4(),
        draft_answer="SST is 28.2 degC.",
        contributing_envelopes=[
            envelope
        ],
    )

    assert result["overall_verdict"] == "pass"
    assert len(result["claim_checks"]) == 1

    check = result["claim_checks"][0]

    assert check["traceable_to_evidence"] is True
    assert check["verdict"] == "pass"


def test_unsupported_claim_fails():
    agent = VerificationAgent()

    envelope = make_envelope()

    result = agent.run(
        request_id=uuid4(),
        draft_answer=(
            "SST is 28.2 degC. "
            "There are definitely tuna in this location."
        ),
        contributing_envelopes=[
            envelope
        ],
    )

    assert result["overall_verdict"] == "fail"

    failed = [
        check
        for check in result["claim_checks"]
        if "tuna" in check["claim_text"].lower()
    ]

    assert failed
    assert failed[0]["traceable_to_evidence"] is False
    assert failed[0]["verdict"] == "fail"


def test_reasoning_is_not_evidence_without_evidence_array():
    agent = VerificationAgent()

    envelope = make_envelope(
        evidence=[],
    )

    result = agent.run(
        request_id=uuid4(),
        draft_answer="SST is 28.2 degC.",
        contributing_envelopes=[
            envelope
        ],
    )

    assert result["overall_verdict"] == "fail"


def test_causal_language_is_detected():
    assert contains_unsupported_causal_language(
        "High chlorophyll caused fish abundance."
    )


def test_causal_language_without_causal_evidence_fails():
    agent = VerificationAgent()

    envelope = make_envelope(
        final_answer=(
            "High chlorophyll caused increased fish abundance."
        ),
    )

    result = agent.run(
        request_id=uuid4(),
        draft_answer=(
            "High chlorophyll caused increased fish abundance."
        ),
        contributing_envelopes=[
            envelope
        ],
    )

    assert result["overall_verdict"] == "fail"

    claim = result["claim_checks"][0]

    assert claim["unsupported_causal_language"] is True
    assert claim["verdict"] == "fail"


def test_causal_language_with_explicit_causal_source():
    evidence = make_evidence()

    evidence["source_type"] = "causal study"
    evidence["data_type"] = "causal study"

    assert causal_language_has_explicit_citation(
        "The study found that X caused Y.",
        [evidence],
    )


def test_confidence_minimum():
    assert minimum_confidence(
        ["high", "moderate"]
    ) == "moderate"

    assert minimum_confidence(
        ["high", "low"]
    ) == "low"


def test_confidence_never_increases():
    assert minimum_confidence(
        ["low", "high", "high"]
    ) == "low"


def test_confidence_downgrade_with_caveats():
    assert downgrade_for_verdict(
        "high",
        "pass_with_caveats",
    ) == "moderate"


def test_confidence_downgrade_on_fail():
    assert downgrade_for_verdict(
        "high",
        "fail",
    ) == "low"


def test_confidence_label_requires_evidence():
    envelope = make_envelope(
        confidence="high",
        evidence=[],
    )

    assert confidence_label_consistent(
        "SST is 28.2 degC.",
        envelope,
    ) is False


def test_evidence_provenance():
    evidence = make_evidence()

    assert evidence_has_provenance(
        evidence
    ) is True


def test_missing_evidence_provenance():
    evidence = {
        "raw_value": 28.2,
        "retrieved_at": now_iso(),
    }

    assert evidence_has_provenance(
        evidence
    ) is False


def test_future_timestamp_invalid():
    future = (
        datetime.now(timezone.utc)
        + timedelta(hours=1)
    )

    assert timestamp_is_valid(
        future
    ) is False


def test_current_timestamp_valid():
    current = datetime.now(timezone.utc)

    assert timestamp_is_valid(
        current
    ) is True


def test_numeric_values_within_tolerance_do_not_conflict():
    assert values_conflict(
        28.0,
        28.2,
        absolute_tolerance=0.5,
    ) is False


def test_numeric_values_beyond_tolerance_conflict():
    assert values_conflict(
        26.0,
        30.0,
        absolute_tolerance=0.5,
    ) is True


def test_cross_agent_conflict_is_detected():
    ocean = make_envelope(
        agent_id="ocean",
        observations=[
            {
                "variable": "sst",
                "value": 26.0,
                "unit": "degC",
                "valid_at": now_iso(),
                "is_forecast": False,
            }
        ],
    )

    second_ocean = make_envelope(
        agent_id="ecosystem",
        observations=[
            {
                "variable": "sst",
                "value": 30.0,
                "unit": "degC",
                "valid_at": now_iso(),
                "is_forecast": False,
            }
        ],
    )

    conflicts = check_consistency(
        [
            ocean,
            second_ocean,
        ]
    )

    assert conflicts
    assert (
        conflicts[0].source_a
        != conflicts[0].source_b
    )


def test_conflict_produces_caveat_or_fail():
    agent = VerificationAgent()

    ocean = make_envelope(
        agent_id="ocean",
        final_answer="SST is 26.0 degC.",
        observations=[
            {
                "variable": "sst",
                "value": 26.0,
                "unit": "degC",
                "valid_at": now_iso(),
                "is_forecast": False,
            }
        ],
    )

    ecosystem = make_envelope(
        agent_id="ecosystem",
        final_answer="SST is 30.0 degC.",
        observations=[
            {
                "variable": "sst",
                "value": 30.0,
                "unit": "degC",
                "valid_at": now_iso(),
                "is_forecast": False,
            }
        ],
    )

    result = agent.run(
        request_id=uuid4(),
        draft_answer="SST is 26.0 degC.",
        contributing_envelopes=[
            ocean,
            ecosystem,
        ],
    )

    assert result["overall_verdict"] in {
        "fail",
        "pass_with_caveats",
    }

    assert any(
        flag["code"]
        == "ORCA_ERR_CONFLICTING_SOURCES"
        for flag in result["flags"]
    )


def test_verification_does_not_invent_claims():
    agent = VerificationAgent()

    envelope = make_envelope()

    draft = "SST is 28.2 degC."

    result = agent.run(
        request_id=uuid4(),
        draft_answer=draft,
        contributing_envelopes=[
            envelope
        ],
    )

    for check in result["claim_checks"]:
        assert (
            check["claim_text"]
            in draft
        )


def test_evidence_indices_are_reported():
    agent = VerificationAgent()

    envelope = make_envelope()

    result = agent.run(
        request_id=uuid4(),
        draft_answer="SST is 28.2 degC.",
        contributing_envelopes=[
            envelope
        ],
    )

    check = result["claim_checks"][0]

    assert "evidence_indices" in check
    assert check["evidence_indices"]


def test_multiple_supported_claims():
    agent = VerificationAgent()

    envelope = make_envelope(
        final_answer=(
            "SST is 28.2 degC. "
            "Wave height is 1.2 m."
        ),
        observations=[
            {
                "variable": "sst",
                "value": 28.2,
                "unit": "degC",
                "valid_at": now_iso(),
                "is_forecast": False,
            },
            {
                "variable": "wave_height",
                "value": 1.2,
                "unit": "m",
                "valid_at": now_iso(),
                "is_forecast": False,
            },
        ],
        evidence=[
            make_evidence(
                source_id="INCOIS-SST"
            ),
            make_evidence(
                source_id="INCOIS-WAVE"
            ),
        ],
    )

    result = agent.run(
        request_id=uuid4(),
        draft_answer=(
            "SST is 28.2 degC. "
            "Wave height is 1.2 m."
        ),
        contributing_envelopes=[
            envelope
        ],
    )

    assert result["overall_verdict"] == "pass"
    assert result["pass_count"] == 2


def test_malformed_envelope_fails_closed():
    agent = VerificationAgent()

    malformed = {
        "request_id": str(uuid4()),
    }

    result = agent.run(
        request_id=uuid4(),
        draft_answer="SST is 28.2 degC.",
        contributing_envelopes=[
            malformed
        ],
    )

    assert result["overall_verdict"] == "fail"

    assert any(
        flag["code"]
        == "ORCA_ERR_SCHEMA_VALIDATION"
        for flag in result["flags"]
    )
