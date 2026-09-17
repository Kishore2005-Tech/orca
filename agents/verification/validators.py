from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Iterable, Optional


# Causal language is intentionally conservative.
# Verification flags causal wording unless the source evidence explicitly
# indicates that the claim is based on a causal study.
CAUSAL_PATTERNS = [
    r"\bcaused by\b",
    r"\bcauses\b",
    r"\bcaused\b",
    r"\bleads to\b",
    r"\bled to\b",
    r"\bresults in\b",
    r"\bresulted in\b",
    r"\bproduces\b",
    r"\bproduced\b",
    r"\bdrives\b",
    r"\bdrove\b",
    r"\bcreates\b",
    r"\bcreated\b",
    r"\bdue to\b",
    r"\bbecause of\b",
    r"\bresponsible for\b",
    r"\btherefore\b",
]


def as_dict(value: Any) -> dict:
    """
    Convert a Pydantic model or mapping into a plain dictionary.
    """
    if isinstance(value, dict):
        return value

    if hasattr(value, "model_dump"):
        return value.model_dump()

    if hasattr(value, "dict"):
        return value.dict()

    raise TypeError(
        f"Unsupported envelope type: {type(value).__name__}"
    )


def get_field(value: Any, field: str, default: Any = None) -> Any:
    """
    Read a field from either a dictionary or a Pydantic-like object.
    """
    if isinstance(value, dict):
        return value.get(field, default)

    return getattr(value, field, default)


def validate_envelope_structure(
    envelope: Any,
) -> tuple[bool, list[str]]:
    """
    Validate the minimum StandardResponseEnvelope structure required
    by Verification.

    Verification must fail closed when an envelope is malformed.
    """
    errors: list[str] = []

    required_fields = [
        "request_id",
        "timestamp",
        "contributing_agents",
        "final_confidence",
    ]

    for field in required_fields:
        if get_field(envelope, field) is None:
            errors.append(
                f"Missing required envelope field: {field}"
            )

    evidence = get_field(envelope, "evidence", None)
    observations = get_field(envelope, "observations", None)

    # Older ORCA backend envelopes use citations/zone_assessments while
    # the contract uses evidence/observations. Accept either representation
    # so Verification can validate envelopes during migration.
    if evidence is None and observations is None:
        if get_field(envelope, "citations", None) is None:
            errors.append(
                "Envelope contains neither evidence/observations nor citations."
            )

    return len(errors) == 0, errors


def extract_evidence(envelope: Any) -> list[Any]:
    """
    Return evidence from an envelope.

    The verifier only trusts explicit evidence arrays. It never treats
    reasoning prose as evidence.
    """
    evidence = get_field(envelope, "evidence", None)

    if evidence is None:
        return []

    if not isinstance(evidence, list):
        raise TypeError("envelope.evidence must be a list")

    return evidence


def evidence_source_reference(
    evidence: Any,
) -> str:
    """
    Extract a stable human-readable source reference.
    """
    source = (
        get_field(evidence, "source_id")
        or get_field(evidence, "source")
        or get_field(evidence, "source_name")
        or get_field(evidence, "issuing_authority")
        or get_field(evidence, "title")
    )

    return str(source) if source is not None else ""


def evidence_has_provenance(
    evidence: Any,
) -> bool:
    """
    Evidence must identify where it came from.

    A URL is useful but is not mandatory because some ORCA evidence
    sources may be internal datasets or operational feeds.
    """
    source = evidence_source_reference(evidence)

    if not source.strip():
        return False

    timestamp = (
        get_field(evidence, "observed_or_published_at")
        or get_field(evidence, "retrieved_at")
        or get_field(evidence, "issued_at")
        or get_field(evidence, "published_at")
    )

    return timestamp is not None


def extract_confidence_level(
    envelope: Any,
) -> Optional[str]:
    confidence = get_field(
        envelope,
        "final_confidence",
        None,
    )

    if confidence is None:
        confidence = get_field(
            envelope,
            "confidence",
            None,
        )

    if confidence is None:
        return None

    level = get_field(
        confidence,
        "level",
        None,
    )

    if level is None:
        return None

    return str(level).lower()


def confidence_rank(level: Optional[str]) -> int:
    """
    Higher number = stronger confidence.

    Unknown values receive -1 so they can never accidentally pass
    as a known confidence level.
    """
    if level is None:
        return -1

    normalized = level.lower().strip()

    ranks = {
        "uncertain": 0,
        "low": 1,
        "moderate": 2,
        "medium": 2,
        "high": 3,
    }

    return ranks.get(normalized, -1)


def contains_unsupported_causal_language(
    claim: str,
) -> bool:
    """
    Detect causal-sounding language.

    This is deliberately lexical and deterministic. Verification does
    not use an LLM to decide whether a causal phrase is present.
    """
    normalized = claim.lower()

    for pattern in CAUSAL_PATTERNS:
        if re.search(pattern, normalized):
            return True

    return False


def causal_language_has_explicit_citation(
    claim: str,
    evidence: Iterable[Any],
) -> bool:
    """
    A causal statement can only pass when evidence explicitly identifies
    a study/source supporting causal interpretation.

    This function does not infer causality from ordinary observations.
    """
    if not contains_unsupported_causal_language(claim):
        return True

    for item in evidence:
        source_type = str(
            get_field(item, "source_type", "")
        ).lower()

        evidence_type = str(
            get_field(item, "data_type", "")
            or get_field(item, "evidence_type", "")
        ).lower()

        title = str(
            get_field(item, "source_name", "")
            or get_field(item, "title", "")
        ).lower()

        causal_markers = (
            "causal",
            "causality",
            "experimental study",
            "causal study",
        )

        if (
            any(marker in source_type for marker in causal_markers)
            or any(marker in evidence_type for marker in causal_markers)
            or any(marker in title for marker in causal_markers)
        ):
            return True

    return False


def normalize_claim_text(claim: str) -> str:
    """
    Normalize a claim only for comparison.

    The original claim text is always retained in the final verification
    output.
    """
    return " ".join(
        claim.lower().strip().split()
    )


def claim_appears_in_text(
    claim: str,
    text: str,
) -> bool:
    """
    Conservative substring check.

    Verification must not invent claims. A claim is considered traceable
    to the draft only when its normalized text can be found in the source
    text, or when a bounded sentence match exists.
    """
    if not claim.strip() or not text.strip():
        return False

    normalized_claim = normalize_claim_text(claim)
    normalized_text = normalize_claim_text(text)

    return normalized_claim in normalized_text


def parse_timestamp(
    value: Any,
) -> Optional[datetime]:
    if value is None:
        return None

    if isinstance(value, datetime):
        timestamp = value
    else:
        text = str(value).strip()

        if not text:
            return None

        try:
            timestamp = datetime.fromisoformat(
                text.replace("Z", "+00:00")
            )
        except ValueError:
            return None

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(
            tzinfo=timezone.utc
        )

    return timestamp


def timestamp_is_valid(
    value: Any,
    *,
    now: Optional[datetime] = None,
) -> bool:
    timestamp = parse_timestamp(value)

    if timestamp is None:
        return False

    current = now or datetime.now(timezone.utc)

    # A response timestamp may not be in the future.
    return timestamp <= current


def evidence_is_current(
    evidence: Any,
    *,
    now: Optional[datetime] = None,
    max_age_hours: Optional[float] = None,
) -> bool:
    """
    Generic freshness check.

    Agent-specific freshness rules should still be enforced by the
    originating agent. Verification only checks obviously invalid
    timestamps and optional age constraints supplied by the caller.
    """
    timestamp = (
        get_field(evidence, "observed_or_published_at")
        or get_field(evidence, "retrieved_at")
        or get_field(evidence, "issued_at")
        or get_field(evidence, "published_at")
    )

    parsed = parse_timestamp(timestamp)

    if parsed is None:
        return False

    current = now or datetime.now(timezone.utc)

    if parsed > current:
        return False

    if max_age_hours is None:
        return True

    age_hours = (
        current - parsed
    ).total_seconds() / 3600

    return age_hours <= max_age_hours


def envelope_agent_id(
    envelope: Any,
) -> str:
    agents = get_field(
        envelope,
        "contributing_agents",
        None,
    )

    if isinstance(agents, list) and agents:
        return str(agents[0])

    agent_id = get_field(
        envelope,
        "agent_id",
        None,
    )

    return str(agent_id) if agent_id else "unknown"
