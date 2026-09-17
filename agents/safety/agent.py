from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional

from .prompts import (
    ADVISORY_PROMPT,
    EMERGENCY_PROMPT,
    FALLBACK_PROMPT,
    PHYSICAL_HAZARD_PROMPT,
    SAFETY_SYSTEM_PROMPT,
)
from .schemas import (
    AdvisoryType,
    ConfidenceLevel,
    EmergencyEscalation,
    ErrorItem,
    EvidenceItem,
    SafetyAdvisory,
    SafetyAgentResult,
    SafetyQuery,
    Severity,
    WarningItem,
)
from .tools import (
    AdvisoryFeedItem,
    SEVERITY_ORDER,
    classify_severity_from_context,
    check_expiry,
    deduplicate_advisories,
    emergency_instruction,
    extract_wave_height,
    extract_wind_speed,
    is_stale,
    rank_advisories,
    severity_must_not_be_downgraded,
    unavailable_source_instruction,
)


class SafetyAgent:
    """
    ORCA Safety Agent.

    Handles marine hazard advisories and emergency escalation.

    The agent does not directly call live government feeds in this
    implementation. Feed readers should provide AdvisoryFeedItem values.
    """

    def __init__(
        self,
        advisory_freshness_hours: float = 12.0,
    ):
        self.agent_id = "safety"
        self.agent_name = "Maritime Safety & Hazard Agent"

        self.advisory_freshness_hours = advisory_freshness_hours

    def run(
        self,
        query: SafetyQuery,
        *,
        advisories: Optional[Iterable[AdvisoryFeedItem]] = None,
        source_available: bool = True,
        now: Optional[datetime] = None,
    ) -> SafetyAgentResult:
        current_time = now or datetime.now(timezone.utc)

        # Emergency trigger has priority.
        if query.possible_emergency:
            emergency = EmergencyEscalation(
                required=True,
                instruction=emergency_instruction(),
            )
        else:
            emergency = EmergencyEscalation(
                required=False,
                instruction="No possible in-progress emergency was indicated.",
            )

        location_error = self._validate_location(query)

        if location_error:
            return self._error_result(
                query,
                code=location_error[0],
                message=location_error[1],
                timestamp=current_time,
                emergency=emergency,
            )

        # A source outage must never be interpreted as an all-clear.
        if not source_available:
            return self._source_unavailable_result(
                query,
                timestamp=current_time,
                emergency=emergency,
            )

        supplied_advisories = list(advisories or [])

        active_advisories: list[AdvisoryFeedItem] = []
        warnings: list[WarningItem] = []
        errors: list[ErrorItem] = []

        for advisory in supplied_advisories:
            try:
                expiry = check_expiry(
                    advisory.expires_at,
                    now=current_time,
                )
            except ValueError as exc:
                warnings.append(
                    WarningItem(
                        code="ORCA_ERR_SCHEMA_VALIDATION",
                        message=str(exc),
                    )
                )
                continue

            if expiry.expired:
                warnings.append(
                    WarningItem(
                        code="ORCA_ERR_STALE_DATA",
                        message=(
                            f"Expired advisory from "
                            f"{advisory.issuing_authority} was excluded."
                        ),
                    )
                )
                continue

            if advisory.issued_at.tzinfo is None:
                warnings.append(
                    WarningItem(
                        code="ORCA_ERR_SCHEMA_VALIDATION",
                        message=(
                            f"Advisory {advisory.source_reference} has "
                            "a timezone-naive issued_at timestamp."
                        ),
                    )
                )
                continue

            # Freshness warning is informational; explicit expiry remains
            # the hard validity boundary.
            if is_stale(
                advisory.issued_at,
                max_age_hours=self.advisory_freshness_hours,
                now=current_time,
            ):
                warnings.append(
                    WarningItem(
                        code="ORCA_ERR_STALE_DATA",
                        message=(
                            f"Advisory {advisory.source_reference} is older "
                            f"than {self.advisory_freshness_hours:g} hours."
                        ),
                    )
                )

            active_advisories.append(advisory)

        active_advisories = deduplicate_advisories(
            active_advisories
        )

        ranked_advisories = rank_advisories(
            active_advisories
        )

        # If we have an active official advisory, it is the primary result.
        if ranked_advisories:
            return self._build_advisory_result(
                query=query,
                ranked_advisories=ranked_advisories,
                warnings=warnings,
                errors=errors,
                emergency=emergency,
                timestamp=current_time,
            )

        # No active official advisory. Physical context can provide
        # general guidance, but not an "all clear."
        return self._build_context_result(
            query=query,
            warnings=warnings,
            errors=errors,
            emergency=emergency,
            timestamp=current_time,
        )

    def classify_physical_hazard(
        self,
        query: SafetyQuery,
    ) -> dict:
        """
        Convert Ocean Agent physical context into a hazard-screening signal.

        This is general hazard guidance, not an official advisory.
        """
        wave_height = extract_wave_height(
            query.physical_context
        )

        wind_speed = extract_wind_speed(
            query.physical_context
        )

        result = classify_severity_from_context(
            wave_height_m=wave_height,
            wind_speed_knots=wind_speed,
        )

        return {
            "severity": result.severity.value,
            "reason": result.reason,
            "wave_height_m": wave_height,
            "wind_speed_knots": wind_speed,
            "is_official_advisory": False,
        }

    def validate_advisory(
        self,
        advisory: AdvisoryFeedItem,
        *,
        now: Optional[datetime] = None,
    ) -> tuple[bool, str]:
        current_time = now or datetime.now(timezone.utc)

        if not advisory.region.strip():
            return False, "Advisory region cannot be empty."

        if not advisory.issuing_authority.strip():
            return False, "Issuing authority cannot be empty."

        if advisory.issued_at.tzinfo is None:
            return False, "issued_at must be timezone-aware."

        if advisory.expires_at is not None:
            if advisory.expires_at.tzinfo is None:
                return False, "expires_at must be timezone-aware."

            if advisory.expires_at <= current_time:
                return False, "Advisory has expired."

        return True, "Advisory is valid."

    def _build_advisory_result(
        self,
        *,
        query: SafetyQuery,
        ranked_advisories: list[AdvisoryFeedItem],
        warnings: list[WarningItem],
        errors: list[ErrorItem],
        emergency: EmergencyEscalation,
        timestamp: datetime,
    ) -> SafetyAgentResult:
        primary = ranked_advisories[0]

        safety_advisories: list[SafetyAdvisory] = []
        evidence: list[EvidenceItem] = []

        for index, advisory in enumerate(ranked_advisories):
            safety_advisories.append(
                SafetyAdvisory(
                    advisory_type=advisory.advisory_type,
                    severity=advisory.severity,
                    region=advisory.region,
                    issuing_authority=advisory.issuing_authority,
                    issued_at=advisory.issued_at,
                    expires_at=advisory.expires_at,
                    guidance_text=advisory.guidance_text,
                    evidence_index=index,
                )
            )

            evidence.append(
                EvidenceItem(
                    issuing_authority=advisory.issuing_authority,
                    issued_at=advisory.issued_at,
                    expires_at=advisory.expires_at,
                    source_reference=advisory.source_reference,
                    source_type=self._normalize_source_type(
                        advisory.source_type
                    ),
                )
            )

        confidence_level = ConfidenceLevel.HIGH
        confidence_score = 0.95

        if warnings:
            confidence_score = 0.85

        status = "ok"

        if warnings or errors:
            status = "partial"

        guidance = self._activity_guidance(
            activity=query.activity_type.value,
            advisory=primary,
        )

        # possible_emergency=true can never be removed.
        if query.possible_emergency:
            guidance = (
                emergency.instruction
                + " "
                + guidance
            )

        return SafetyAgentResult(
            request_id=query.request_id,
            timestamp=timestamp,
            status=status,
            advisories=safety_advisories,
            advisory_type=primary.advisory_type,
            severity=primary.severity,
            issuing_authority=primary.issuing_authority,
            issued_at=primary.issued_at,
            expires_at=primary.expires_at,
            guidance_text=guidance,
            emergency_escalation=emergency,
            evidence=evidence,
            confidence_level=confidence_level,
            confidence_score=confidence_score,
            warnings=warnings,
            errors=errors,
        )

    def _build_context_result(
        self,
        *,
        query: SafetyQuery,
        warnings: list[WarningItem],
        errors: list[ErrorItem],
        emergency: EmergencyEscalation,
        timestamp: datetime,
    ) -> SafetyAgentResult:
        physical = self.classify_physical_hazard(query)

        severity = Severity(physical["severity"])

        if severity in {
            Severity.HIGH,
            Severity.EXTREME,
        }:
            guidance = (
                "General hazard guidance: supplied physical conditions "
                "indicate elevated marine hazard potential. Follow the "
                "latest official marine warning and Coast Guard guidance "
                "before undertaking the activity."
            )
        elif severity == Severity.MODERATE:
            guidance = (
                "General guidance: supplied physical conditions indicate "
                "moderate hazard potential. Check the latest official "
                "marine advisory before undertaking the activity."
            )
        else:
            guidance = (
                "No active official advisory was supplied. ORCA cannot "
                "treat this as an all-clear. Check the latest official "
                "marine warning before undertaking the activity."
            )

        if query.possible_emergency:
            guidance = (
                emergency.instruction
                + " "
                + guidance
            )

        return SafetyAgentResult(
            request_id=query.request_id,
            timestamp=timestamp,
            status="partial" if warnings else "ok",
            advisories=[],
            advisory_type=AdvisoryType.OTHER,
            severity=severity,
            issuing_authority="Derived physical context",
            issued_at=timestamp,
            expires_at=None,
            guidance_text=guidance,
            emergency_escalation=emergency,
            evidence=self._context_evidence(query),
            confidence_level=ConfidenceLevel.LOW,
            confidence_score=0.45,
            warnings=warnings,
            errors=errors,
        )

    def _source_unavailable_result(
        self,
        query: SafetyQuery,
        *,
        timestamp: datetime,
        emergency: EmergencyEscalation,
    ) -> SafetyAgentResult:
        warnings = [
            WarningItem(
                code="ORCA_ERR_SOURCE_UNAVAILABLE",
                message=(
                    "Unable to confirm current hazard status from the "
                    "required advisory source. This is not an all-clear."
                ),
            )
        ]

        guidance = unavailable_source_instruction()

        if query.possible_emergency:
            guidance = (
                emergency.instruction
                + " "
                + guidance
            )

        return SafetyAgentResult(
            request_id=query.request_id,
            timestamp=timestamp,
            status="error",
            advisories=[],
            advisory_type=AdvisoryType.OTHER,
            severity=Severity.EXTREME
            if query.possible_emergency
            else Severity.LOW,
            issuing_authority="Unavailable",
            issued_at=timestamp,
            expires_at=None,
            guidance_text=guidance,
            emergency_escalation=emergency,
            evidence=[],
            confidence_level=ConfidenceLevel.LOW,
            confidence_score=0.0,
            warnings=warnings,
            errors=[
                ErrorItem(
                    code="ORCA_ERR_SOURCE_UNAVAILABLE",
                    message=(
                        "Current marine hazard status could not be "
                        "confirmed."
                    ),
                    fatal=True,
                )
            ],
        )

    def _validate_location(
        self,
        query: SafetyQuery,
    ) -> Optional[tuple[str, str]]:
        if not query.location.has_location():
            return (
                "ORCA_ERR_AMBIGUOUS_LOCATION",
                (
                    "Safety Agent requires a resolved location. "
                    "Ambiguous locations cannot be guessed because "
                    "safety decisions depend on the exact hazard area."
                ),
            )

        return None

    def _error_result(
        self,
        query: SafetyQuery,
        *,
        code: str,
        message: str,
        timestamp: datetime,
        emergency: EmergencyEscalation,
    ) -> SafetyAgentResult:
        return SafetyAgentResult(
            request_id=query.request_id,
            timestamp=timestamp,
            status="error",
            advisories=[],
            advisory_type=AdvisoryType.OTHER,
            severity=Severity.EXTREME
            if query.possible_emergency
            else Severity.LOW,
            issuing_authority="Unavailable",
            issued_at=timestamp,
            expires_at=None,
            guidance_text=(
                emergency.instruction
                if query.possible_emergency
                else message
            ),
            emergency_escalation=emergency,
            evidence=[],
            confidence_level=ConfidenceLevel.LOW,
            confidence_score=0.0,
            warnings=[],
            errors=[
                ErrorItem(
                    code=code,
                    message=message,
                    fatal=True,
                )
            ],
        )

    def _activity_guidance(
        self,
        *,
        activity: str,
        advisory: AdvisoryFeedItem,
    ) -> str:
        activity_text = {
            "swimming": "swimming",
            "diving": "diving",
            "boating": "boating",
            "fishing": "fishing",
            "general": "marine activity",
        }.get(activity, "marine activity")

        return (
            f"Active {advisory.severity.value} {advisory.advisory_type.value} "
            f"advisory for {advisory.region}. "
            f"For {activity_text}, follow the issuing authority's guidance: "
            f"{advisory.guidance_text} "
            "This information does not replace official emergency services "
            "or Coast Guard instructions."
        )

    def _context_evidence(
        self,
        query: SafetyQuery,
    ) -> list[EvidenceItem]:
        evidence = []

        for item in query.physical_context or []:
            if item.source:
                evidence.append(
                    EvidenceItem(
                        issuing_authority=item.source,
                        issued_at=item.observed_at,
                        expires_at=None,
                        source_reference=(
                            f"physical-context:{item.variable}"
                        ),
                        source_type="ocean_data",
                    )
                )

        for item in query.ecological_context or []:
            if item.source:
                evidence.append(
                    EvidenceItem(
                        issuing_authority=item.source,
                        issued_at=item.observed_at,
                        expires_at=None,
                        source_reference=(
                            f"ecological-context:{item.hazard_type}"
                        ),
                        source_type="ecosystem_data",
                    )
                )

        return evidence

    @staticmethod
    def _normalize_source_type(source_type: str) -> str:
        mapping = {
            "government": "government_advisory",
            "official": "government_advisory",
            "coast_guard": "coast_guard",
            "meteorological": "meteorological_authority",
            "health": "health_advisory",
        }

        return mapping.get(
            source_type.lower(),
            "government_advisory",
        )


__all__ = [
    "SafetyAgent",
    "AdvisoryFeedItem",
    "SAFETY_SYSTEM_PROMPT",
    "ADVISORY_PROMPT",
    "PHYSICAL_HAZARD_PROMPT",
    "EMERGENCY_PROMPT",
    "FALLBACK_PROMPT",
]
