from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Iterable, Optional

from .validators import (
    as_dict,
    envelope_agent_id,
    get_field,
)


@dataclass(frozen=True)
class Conflict:
    claim_a: str
    claim_b: str
    source_a: str
    source_b: str
    reason: str
    resolvable: bool = False


NUMERIC_PATTERN = re.compile(
    r"(?P<value>-?\d+(?:\.\d+)?)\s*"
    r"(?P<unit>[a-zA-Z°/%]+)?"
)


def _observations(envelope: Any) -> list[Any]:
    observations = get_field(
        envelope,
        "observations",
        None,
    )

    if isinstance(observations, list):
        return observations

    # Compatibility with the current ORCA backend, which may place
    # structured values inside zone assessments.
    zone_assessments = get_field(
        envelope,
        "zone_assessments",
        None,
    )

    if isinstance(zone_assessments, list):
        flattened = []

        for zone in zone_assessments:
            if isinstance(zone, dict):
                flattened.append(zone)
            elif hasattr(zone, "model_dump"):
                flattened.append(zone.model_dump())
            elif hasattr(zone, "dict"):
                flattened.append(zone.dict())

        return flattened

    return []


def _observation_variable(
    observation: Any,
) -> Optional[str]:
    variable = (
        get_field(observation, "variable", None)
        or get_field(observation, "indicator", None)
        or get_field(observation, "field", None)
    )

    if variable is None:
        return None

    return str(variable).lower().strip()


def _observation_value(
    observation: Any,
) -> Optional[float]:
    value = get_field(
        observation,
        "value",
        None,
    )

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _observation_location(
    observation: Any,
) -> Optional[tuple[float, float]]:
    lat = get_field(observation, "latitude", None)
    lon = get_field(observation, "longitude", None)

    if lat is None or lon is None:
        return None

    try:
        return float(lat), float(lon)
    except (TypeError, ValueError):
        return None


def _observation_time(
    observation: Any,
) -> Optional[str]:
    return (
        get_field(observation, "valid_at", None)
        or get_field(observation, "observed_at", None)
        or get_field(observation, "timestamp", None)
    )


def values_conflict(
    value_a: float,
    value_b: float,
    *,
    absolute_tolerance: float = 0.5,
    relative_tolerance: float = 0.05,
) -> bool:
    difference = abs(value_a - value_b)

    if difference <= absolute_tolerance:
        return False

    denominator = max(
        abs(value_a),
        abs(value_b),
        1e-9,
    )

    return (
        difference / denominator
        > relative_tolerance
    )


def check_numeric_conflicts(
    envelopes: Iterable[Any],
) -> list[Conflict]:
    """
    Detect conflicting numeric observations from different agents.

    Verification reports conflicts. It does not decide which source is
    scientifically correct.
    """
    indexed: dict[str, list[tuple[str, Any]]] = {}

    for envelope in envelopes:
        agent_id = envelope_agent_id(envelope)

        for observation in _observations(envelope):
            variable = _observation_variable(observation)

            if variable is None:
                continue

            value = _observation_value(observation)

            if value is None:
                continue

            indexed.setdefault(variable, []).append(
                (agent_id, observation)
            )

    conflicts: list[Conflict] = []

    for variable, items in indexed.items():
        for index in range(len(items)):
            agent_a, observation_a = items[index]
            value_a = _observation_value(observation_a)

            if value_a is None:
                continue

            for other_index in range(index + 1, len(items)):
                agent_b, observation_b = items[other_index]

                if agent_a == agent_b:
                    continue

                value_b = _observation_value(observation_b)

                if value_b is None:
                    continue

                if not values_conflict(
                    value_a,
                    value_b,
                ):
                    continue

                conflicts.append(
                    Conflict(
                        claim_a=(
                            f"{variable} = {value_a}"
                        ),
                        claim_b=(
                            f"{variable} = {value_b}"
                        ),
                        source_a=agent_a,
                        source_b=agent_b,
                        reason=(
                            f"Different agents reported conflicting "
                            f"{variable} values beyond tolerance."
                        ),
                        resolvable=False,
                    )
                )

    return conflicts


def _text_claims(
    envelope: Any,
) -> list[str]:
    claims: list[str] = []

    for field in (
        "final_answer",
        "synthesized_answer",
        "reasoning",
    ):
        value = get_field(
            envelope,
            field,
            None,
        )

        if isinstance(value, str) and value.strip():
            claims.append(value.strip())

    return claims


def detect_textual_conflicts(
    envelopes: Iterable[Any],
) -> list[Conflict]:
    """
    Detect explicit textual contradiction patterns.

    This is intentionally conservative. It flags obvious opposing
    statements and leaves scientific resolution to the Coordinator.
    """
    negative_patterns = [
        re.compile(
            r"\b(no|not|absent|none|false|below|decreased)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(low|weak|poor)\b",
            re.IGNORECASE,
        ),
    ]

    positive_patterns = [
        re.compile(
            r"\b(present|detected|exists|true|above|increased)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(high|strong|good)\b",
            re.IGNORECASE,
        ),
    ]

    records: list[
        tuple[str, str, bool, bool]
    ] = []

    for envelope in envelopes:
        agent_id = envelope_agent_id(envelope)

        for claim in _text_claims(envelope):
            positive = any(
                pattern.search(claim)
                for pattern in positive_patterns
            )

            negative = any(
                pattern.search(claim)
                for pattern in negative_patterns
            )

            if positive or negative:
                records.append(
                    (
                        agent_id,
                        claim,
                        positive,
                        negative,
                    )
                )

    conflicts: list[Conflict] = []

    for index in range(len(records)):
        (
            agent_a,
            claim_a,
            positive_a,
            negative_a,
        ) = records[index]

        for other_index in range(index + 1, len(records)):
            (
                agent_b,
                claim_b,
                positive_b,
                negative_b,
            ) = records[other_index]

            if agent_a == agent_b:
                continue

            if (
                positive_a
                and negative_b
            ) or (
                negative_a
                and positive_b
            ):
                conflicts.append(
                    Conflict(
                        claim_a=claim_a,
                        claim_b=claim_b,
                        source_a=agent_a,
                        source_b=agent_b,
                        reason=(
                            "Contributing envelopes contain "
                            "potentially contradictory textual claims."
                        ),
                        resolvable=False,
                    )
                )

    return conflicts


def check_consistency(
    envelopes: Iterable[Any],
) -> list[Conflict]:
    """
    Run all deterministic conflict checks.
    """
    envelope_list = list(envelopes)

    return (
        check_numeric_conflicts(envelope_list)
        + detect_textual_conflicts(envelope_list)
    )
