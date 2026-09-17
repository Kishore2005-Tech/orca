from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional

from .schemas import AdvisoryType, Severity


SEVERITY_ORDER = {
    Severity.LOW: 1,
    Severity.MODERATE: 2,
    Severity.HIGH: 3,
    Severity.EXTREME: 4,
}


@dataclass(frozen=True)
class AdvisoryFeedItem:
    advisory_type: AdvisoryType
    severity: Severity
    region: str
    issuing_authority: str
    issued_at: datetime
    expires_at: Optional[datetime]
    guidance_text: str
    source_reference: str
    source_type: str


@dataclass(frozen=True)
class SeverityResult:
    severity: Severity
    reason: str


@dataclass(frozen=True)
class ExpiryResult:
    active: bool
    expired: bool
    reason: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def classify_wave_severity(
    wave_height_m: float,
) -> SeverityResult:
    """
    ORCA implementation-plan thresholds:

    < 2.5 m  -> low/moderate physical concern
    2.5–3.0 m -> high-wave watch range
    > 3.0 m -> high-wave alert range

    This classification is a hazard signal. It is not by itself
    an official government advisory.
    """
    if wave_height_m < 0:
        raise ValueError("wave_height_m cannot be negative")

    if wave_height_m > 3.0:
        return SeverityResult(
            severity=Severity.HIGH,
            reason=(
                "Significant wave height exceeds the ORCA "
                "High Wave Alert threshold of 3.0 m."
            ),
        )

    if wave_height_m >= 2.5:
        return SeverityResult(
            severity=Severity.MODERATE,
            reason=(
                "Significant wave height is within the ORCA "
                "High Wave Watch range of 2.5–3.0 m."
            ),
        )

    return SeverityResult(
        severity=Severity.LOW,
        reason=(
            "Significant wave height is below the configured "
            "High Wave Watch threshold."
        ),
    )


def classify_wind_severity(
    wind_speed_knots: float,
) -> SeverityResult:
    """
    Conservative physical hazard classification.

    This is a screening utility only. Official advisories always
    take precedence over this derived classification.
    """
    if wind_speed_knots < 0:
        raise ValueError("wind_speed_knots cannot be negative")

    if wind_speed_knots >= 34.0:
        return SeverityResult(
            severity=Severity.EXTREME,
            reason="Wind speed reaches the severe marine-hazard screening range.",
        )

    if wind_speed_knots >= 25.0:
        return SeverityResult(
            severity=Severity.HIGH,
            reason="Wind speed reaches the high marine-hazard screening range.",
        )

    if wind_speed_knots >= 18.0:
        return SeverityResult(
            severity=Severity.MODERATE,
            reason="Wind speed reaches the moderate marine-hazard screening range.",
        )

    return SeverityResult(
        severity=Severity.LOW,
        reason="Wind speed is below the configured hazard screening threshold.",
    )


def classify_severity_from_context(
    *,
    wave_height_m: Optional[float] = None,
    wind_speed_knots: Optional[float] = None,
) -> SeverityResult:
    """
    Combine physical hazard indicators without silently overriding
    an official advisory.
    """
    results = []

    if wave_height_m is not None:
        results.append(
            classify_wave_severity(wave_height_m)
        )

    if wind_speed_knots is not None:
        results.append(
            classify_wind_severity(wind_speed_knots)
        )

    if not results:
        return SeverityResult(
            severity=Severity.LOW,
            reason="No physical hazard indicator was supplied.",
        )

    highest = max(
        results,
        key=lambda result: SEVERITY_ORDER[result.severity],
    )

    return highest


def check_expiry(
    expires_at: Optional[datetime],
    *,
    now: Optional[datetime] = None,
) -> ExpiryResult:
    """
    An advisory with no expiry remains active only if the source
    explicitly allows open-ended validity.

    For ORCA, an explicit past expiry always invalidates the advisory.
    """
    current_time = now or utc_now()

    if expires_at is None:
        return ExpiryResult(
            active=True,
            expired=False,
            reason="No expiry time supplied by source.",
        )

    if expires_at.tzinfo is None:
        raise ValueError("expires_at must be timezone-aware")

    if expires_at <= current_time:
        return ExpiryResult(
            active=False,
            expired=True,
            reason="Advisory has passed its expiry time.",
        )

    return ExpiryResult(
        active=True,
        expired=False,
        reason="Advisory remains within its validity period.",
    )


def is_stale(
    issued_at: datetime,
    *,
    max_age_hours: float = 12.0,
    now: Optional[datetime] = None,
) -> bool:
    if issued_at.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")

    if max_age_hours < 0:
        raise ValueError("max_age_hours cannot be negative")

    current_time = now or utc_now()

    age_hours = (
        current_time - issued_at
    ).total_seconds() / 3600.0

    return age_hours > max_age_hours


def rank_advisories(
    advisories: Iterable[AdvisoryFeedItem],
) -> list[AdvisoryFeedItem]:
    """
    Sort active advisories by severity.

    This is ranking for hazard processing, not a user recommendation.
    """
    return sorted(
        advisories,
        key=lambda advisory: (
            -SEVERITY_ORDER[advisory.severity],
            -advisory.issued_at.timestamp(),
        ),
    )


def deduplicate_advisories(
    advisories: Iterable[AdvisoryFeedItem],
) -> list[AdvisoryFeedItem]:
    """
    Remove exact duplicate advisories while preserving the strongest
    distinct advisory.
    """
    seen: set[tuple] = set()
    result: list[AdvisoryFeedItem] = []

    for advisory in advisories:
        key = (
            advisory.advisory_type,
            advisory.region,
            advisory.issuing_authority,
            advisory.issued_at,
            advisory.expires_at,
            advisory.source_reference,
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(advisory)

    return result


def severity_must_not_be_downgraded(
    source_severity: Severity,
    computed_severity: Severity,
) -> Severity:
    """
    Official source severity always wins.

    If the source says HIGH and a local calculation says MODERATE,
    the result remains HIGH.
    """
    if (
        SEVERITY_ORDER[source_severity]
        >= SEVERITY_ORDER[computed_severity]
    ):
        return source_severity

    return computed_severity


def emergency_instruction() -> str:
    return (
        "Possible emergency detected. Contact local emergency services "
        "or the appropriate Coast Guard/maritime emergency channel "
        "immediately. Do not rely on ORCA as a substitute for emergency "
        "responders."
    )


def unavailable_source_instruction() -> str:
    return (
        "ORCA is unable to confirm the current hazard status from the "
        "required advisory source. This is not an all-clear. Check the "
        "latest official marine warning or Coast Guard channel before "
        "starting or continuing the activity."
    )


def extract_wave_height(
    physical_context,
) -> Optional[float]:
    for item in physical_context or []:
        variable = item.variable.lower().strip()

        if variable in {
            "wave_height",
            "significant_wave_height",
            "swh",
            "hs",
        }:
            return item.value

    return None


def extract_wind_speed(
    physical_context,
) -> Optional[float]:
    for item in physical_context or []:
        variable = item.variable.lower().strip()

        if variable in {
            "wind_speed",
            "wind_speed_knots",
            "wind",
        }:
            return item.value

    return None
