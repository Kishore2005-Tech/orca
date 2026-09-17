from __future__ import annotations

from typing import Any, Iterable, Optional

from .validators import (
    confidence_rank,
    extract_confidence_level,
    get_field,
)


CONFIDENCE_LEVELS = (
    "uncertain",
    "low",
    "moderate",
    "medium",
    "high",
)


def minimum_confidence(
    levels: Iterable[Optional[str]],
) -> str:
    """
    ORCA rule:
    confidence can hold or decrease across stages, never increase.

    If any contributor is uncertain, the combined result is uncertain.
    """
    normalized = [
        str(level).lower()
        for level in levels
        if level is not None
    ]

    if not normalized:
        return "uncertain"

    known = [
        level
        for level in normalized
        if level in CONFIDENCE_LEVELS
    ]

    if not known:
        return "uncertain"

    lowest = min(
        known,
        key=confidence_rank,
    )

    # Contract uses both "moderate" and "medium" in different parts
    # of the current codebase. Normalize to "moderate".
    if lowest == "medium":
        return "moderate"

    return lowest


def collect_confidence_levels(
    envelopes: Iterable[Any],
) -> list[str]:
    levels = []

    for envelope in envelopes:
        level = extract_confidence_level(envelope)

        if level is not None:
            levels.append(level)

    return levels


def confidence_label_consistent(
    claim: str,
    envelope: Any,
) -> bool:
    """
    Check whether a claim is being presented at a confidence level
    supported by the available evidence.

    A high-confidence label requires:
    - a known high/moderate source confidence
    - at least one evidence item
    - provenance on evidence
    """
    confidence = extract_confidence_level(
        envelope
    )

    if confidence is None:
        return False

    confidence = confidence.lower()

    evidence = get_field(
        envelope,
        "evidence",
        [],
    )

    if not isinstance(evidence, list):
        return False

    if not evidence:
        return False

    if confidence == "high":
        return len(evidence) >= 1

    if confidence in {
        "moderate",
        "medium",
        "low",
        "uncertain",
    }:
        return True

    return False


def downgrade_for_verdict(
    base_level: str,
    verdict: str,
) -> str:
    """
    Verification can only downgrade confidence.
    """
    normalized = base_level.lower()

    if normalized == "medium":
        normalized = "moderate"

    rank = confidence_rank(normalized)

    if verdict == "pass":
        return normalized

    if verdict == "pass_with_caveats":
        target_rank = max(
            0,
            rank - 1,
        )

        for level in (
            "uncertain",
            "low",
            "moderate",
            "high",
        ):
            if confidence_rank(level) == target_rank:
                return level

        return "low"

    # fail
    return "low"


def confidence_score_from_level(
    level: str,
) -> float:
    scores = {
        "uncertain": 0.0,
        "low": 0.35,
        "moderate": 0.60,
        "medium": 0.60,
        "high": 0.85,
    }

    return scores.get(
        level.lower(),
        0.0,
    )
