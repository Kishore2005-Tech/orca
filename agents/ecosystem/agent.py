from __future__ import annotations

from datetime import datetime, timezone
from typing import Sequence

from .prompts import (
    CHLOROPHYLL_INTERPRETATION_PROMPT,
    FRONT_INTERPRETATION_PROMPT,
    MHW_INTERPRETATION_PROMPT,
    UPWELLING_INTERPRETATION_PROMPT,
)
from .schemas import (
    Confidence,
    EcosystemAgentInput,
    EcosystemAgentResult,
    EcosystemIndicator,
    EcosystemObservation,
    EvidenceItem,
    WarningItem,
)
from .tools import (
    ChlorophyllObservation,
    EcosystemGridPoint,
    SSTObservation,
    get_chlorophyll,
    get_fronts,
    get_mhw,
    get_upwelling,
)


class EcosystemAgent:
    """
    Process marine ecosystem indicators.

    Core calculations are deterministic and kept separate from I/O so that
    they can be tested without external services.
    """

    agent_id = "ecosystem"

    def __init__(
        self,
        monitoring_program: str = "ORCA processed ecosystem dataset",
    ) -> None:
        self.monitoring_program = monitoring_program

    def run(
        self,
        task: EcosystemAgentInput,
        *,
        chlorophyll: Sequence[ChlorophyllObservation] | None = None,
        sst: Sequence[SSTObservation] | None = None,
        grid_points: Sequence[EcosystemGridPoint] | None = None,
    ) -> EcosystemAgentResult:
        """
        Execute an ecosystem task.

        Input datasets are explicitly supplied by the Coordinator/data layer.
        The agent does not invent or silently retrieve unsupported data.
        """

        now = datetime.now(timezone.utc)

        task.time_range.validate_order()

        indicator = task.indicator

        if indicator is None:
            return self._error_result(
                task,
                "ORCA_ERR_NO_DATA",
                "No ecosystem indicator was requested.",
                now,
            )

        try:
            if indicator == EcosystemIndicator.CHLOROPHYLL:
                return self._process_chlorophyll(
                    task,
                    chlorophyll or [],
                    now,
                )

            if indicator == EcosystemIndicator.MHW:
                return self._process_mhw(
                    task,
                    sst or [],
                    now,
                )

            if indicator == EcosystemIndicator.FRONT:
                return self._process_fronts(
                    task,
                    grid_points or [],
                    now,
                )

            if indicator == EcosystemIndicator.UPWELLING:
                return self._process_upwelling(
                    task,
                    grid_points or [],
                    now,
                )

            return self._unsupported_indicator_result(
                task,
                now,
                indicator,
            )

        except ValueError as exc:
            return self._error_result(
                task,
                "ORCA_ERR_SCHEMA_VALIDATION",
                str(exc),
                now,
            )

    def _process_chlorophyll(
        self,
        task: EcosystemAgentInput,
        observations: Sequence[ChlorophyllObservation],
        now: datetime,
    ) -> EcosystemAgentResult:
        if not observations:
            return self._no_data_result(
                task,
                "No chlorophyll observations were supplied.",
                now,
            )

        summary = get_chlorophyll(observations)
        observed_at = summary["observed_at"]

        if not isinstance(observed_at, datetime):
            raise ValueError("invalid chlorophyll observation timestamp")

        value = float(summary["latest_value"])

        observation = EcosystemObservation(
            indicator=EcosystemIndicator.CHLOROPHYLL,
            taxon=task.taxon,
            status_value=f"Chlorophyll-a = {value:g} mg/m3",
            observed_at=observed_at,
            monitoring_program=self.monitoring_program,
            value=value,
            unit="mg/m3",
            interpretation=(
                CHLOROPHYLL_INTERPRETATION_PROMPT.strip()
            ),
        )

        evidence = [
            self._calculation_evidence(
                source=str(summary["source"]),
                observed_at=observed_at,
                value=value,
                now=now,
            )
        ]

        return self._success_result(
            task=task,
            observations=[observation],
            evidence=evidence,
            reasoning=(
                "Chlorophyll-a was processed as an ecosystem/productivity "
                "proxy. No fish-abundance inference was made."
            ),
            confidence=Confidence(
                level="high",
                score=0.85,
                basis="direct processed chlorophyll observation",
            ),
            timestamp=now,
        )

    def _process_mhw(
        self,
        task: EcosystemAgentInput,
        observations: Sequence[SSTObservation],
        now: datetime,
    ) -> EcosystemAgentResult:
        if not observations:
            return self._no_data_result(
                task,
                "No SST observations were supplied for MHW detection.",
                now,
            )

        result = get_mhw(observations)

        latest = max(
            observations,
            key=lambda item: item.observed_at,
        )

        status = (
            "candidate marine heatwave condition detected"
            if result.detected
            else "marine heatwave threshold condition not detected"
        )

        observation = EcosystemObservation(
            indicator=EcosystemIndicator.MHW,
            taxon=None,
            status_value=status,
            observed_at=latest.observed_at,
            monitoring_program=self.monitoring_program,
            value=result.threshold_celsius,
            unit="°C",
            interpretation=(
                f"{MHW_INTERPRETATION_PROMPT.strip()} "
                f"Calculated 90th-percentile threshold: "
                f"{result.threshold_celsius:.3f} °C; "
                f"qualifying days: {result.qualifying_days}."
            ),
        )

        evidence = [
            self._calculation_evidence(
                source=latest.source,
                observed_at=latest.observed_at,
                value=result.threshold_celsius,
                now=now,
            )
        ]

        return self._success_result(
            task=task,
            observations=[observation],
            evidence=evidence,
            reasoning=(
                "Marine heatwave detection used the ORCA prototype rule "
                "of SST above the 90th percentile for at least five "
                "qualifying observations."
            ),
            confidence=Confidence(
                level="medium",
                score=0.75,
                basis="derived indicator from supplied SST observations",
            ),
            timestamp=now,
        )

    def _process_fronts(
        self,
        task: EcosystemAgentInput,
        points: Sequence[EcosystemGridPoint],
        now: datetime,
    ) -> EcosystemAgentResult:
        if not points:
            return self._no_data_result(
                task,
                "No co-located SST/chlorophyll grid points were supplied.",
                now,
            )

        fronts = get_fronts(points)

        observations = [
            EcosystemObservation(
                indicator=EcosystemIndicator.FRONT,
                status_value="candidate ocean-front indicator",
                observed_at=now,
                monitoring_program=self.monitoring_program,
                value=front.magnitude,
                unit="gradient units per coordinate degree",
                interpretation=FRONT_INTERPRETATION_PROMPT.strip(),
            )
            for front in fronts
        ]

        evidence = [
            self._calculation_evidence(
                source="ORCA SST + chlorophyll gradient calculation",
                observed_at=now,
                value=front.magnitude,
                now=now,
            )
            for front in fronts
        ]

        if not observations:
            return self._success_result(
                task=task,
                observations=[],
                evidence=[],
                reasoning="No combined SST/chlorophyll front threshold was met.",
                confidence=Confidence(
                    level="medium",
                    score=0.65,
                    basis="derived spatial-gradient analysis",
                ),
                timestamp=now,
            )

        return self._success_result(
            task=task,
            observations=observations,
            evidence=evidence,
            reasoning=(
                "Candidate fronts were identified from combined spatial "
                "gradients in SST and chlorophyll."
            ),
            confidence=Confidence(
                level="medium",
                score=0.70,
                basis="derived SST and chlorophyll spatial gradients",
            ),
            timestamp=now,
        )

    def _process_upwelling(
        self,
        task: EcosystemAgentInput,
        points: Sequence[EcosystemGridPoint],
        now: datetime,
    ) -> EcosystemAgentResult:
        if not points:
            return self._no_data_result(
                task,
                "No co-located SST/chlorophyll grid points were supplied.",
                now,
            )

        sst_values = [point.sst_celsius for point in points]
        chl_values = [point.chlorophyll_mg_m3 for point in points]

        cold_threshold = sum(sst_values) / len(sst_values)
        chlorophyll_threshold = sum(chl_values) / len(chl_values)

        upwelling = get_upwelling(
            points,
            cold_sst_threshold_celsius=cold_threshold,
            high_chlorophyll_threshold_mg_m3=chlorophyll_threshold,
        )

        observations = [
            EcosystemObservation(
                indicator=EcosystemIndicator.UPWELLING,
                status_value="candidate upwelling condition",
                observed_at=now,
                monitoring_program=self.monitoring_program,
                interpretation=UPWELLING_INTERPRETATION_PROMPT.strip(),
                correlation_flag=self._physical_correlation(task),
            )
            for _ in upwelling
        ]

        evidence = [
            self._calculation_evidence(
                source="ORCA SST + chlorophyll upwelling calculation",
                observed_at=now,
                value=1,
                now=now,
            )
            for _ in upwelling
        ]

        return self._success_result(
            task=task,
            observations=observations,
            evidence=evidence,
            reasoning=(
                "Candidate upwelling conditions were identified using "
                "cold SST together with elevated chlorophyll."
            ),
            confidence=Confidence(
                level="medium",
                score=0.70,
                basis="derived SST and chlorophyll combination",
            ),
            timestamp=now,
        )

    def _physical_correlation(self, task: EcosystemAgentInput):
        if not task.physical_context:
            return None

        events = ", ".join(
            f"{item.parameter}={item.value:g}{item.unit}"
            for item in task.physical_context
        )

        from .schemas import CorrelationFlag

        return CorrelationFlag(
            related_physical_event=events,
            note=(
                "Physical context is reported as contextual correlation "
                "only; no causal relationship is asserted."
            ),
        )

    def _calculation_evidence(
        self,
        source: str,
        observed_at: datetime,
        value: float,
        now: datetime,
    ) -> EvidenceItem:
        return EvidenceItem(
            source=source,
            source_type="calculation",
            reference="ORCA-ECO-SCIENTIFIC-CALCULATION",
            observed_or_published_at=observed_at,
            retrieved_at=now,
            passage_or_value=value,
        )

    def _success_result(
        self,
        task: EcosystemAgentInput,
        observations: list[EcosystemObservation],
        evidence: list[EvidenceItem],
        reasoning: str,
        confidence: Confidence,
        timestamp: datetime,
    ) -> EcosystemAgentResult:
        status = "ok"

        if not observations:
            status = "partial"

        return EcosystemAgentResult(
            request_id=task.request_id,
            timestamp=timestamp,
            status=status,
            location=self._location_dict(task),
            observations=observations,
            reasoning=reasoning,
            evidence=evidence,
            confidence=confidence,
            warnings=[],
            errors=[],
        )

    def _no_data_result(
        self,
        task: EcosystemAgentInput,
        message: str,
        timestamp: datetime,
    ) -> EcosystemAgentResult:
        return self._error_result(
            task,
            "ORCA_ERR_NO_DATA",
            message,
            timestamp,
        )

    def _unsupported_indicator_result(
        self,
        task: EcosystemAgentInput,
        timestamp: datetime,
        indicator: EcosystemIndicator,
    ) -> EcosystemAgentResult:
        return self._error_result(
            task,
            "ORCA_ERR_OUT_OF_SCOPE",
            (
                f"Indicator '{indicator.value}' is defined by the "
                "Ecosystem Agent contract but its external monitoring "
                "adapter is not configured in this prototype."
            ),
            timestamp,
        )

    def _error_result(
        self,
        task: EcosystemAgentInput,
        code: str,
        message: str,
        timestamp: datetime,
    ) -> EcosystemAgentResult:
        from .schemas import ErrorItem

        return EcosystemAgentResult(
            request_id=task.request_id,
            timestamp=timestamp,
            status="error",
            location=self._location_dict(task),
            observations=[],
            reasoning=None,
            evidence=[],
            confidence=Confidence(
                level="low",
                score=0.0,
                basis="insufficient evidence",
            ),
            warnings=[],
            errors=[
                ErrorItem(
                    code=code,
                    message=message,
                    fatal=True,
                )
            ],
        )

    @staticmethod
    def _location_dict(
        task: EcosystemAgentInput,
    ) -> dict[str, object]:
        location = task.location

        return {
            "query": location.region_name,
            "resolved": {
                "lat": location.lat,
                "lon": location.lon,
                "region_name": location.region_name,
                "jurisdiction": location.jurisdiction,
                "maritime_zone": location.maritime_zone,
            },
        }
