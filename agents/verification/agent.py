from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Iterable, Optional
from uuid import UUID

from .confidence import (
    confidence_label_consistent,
    downgrade_for_verdict,
    minimum_confidence,
)
from .conflict_checker import Conflict, check_consistency
from .validators import (
    as_dict,
    causal_language_has_explicit_citation,
    claim_appears_in_text,
    contains_unsupported_causal_language,
    envelope_agent_id,
    extract_evidence,
    get_field,
    validate_envelope_structure,
)


class VerificationAgent:
    """
    ORCA Verification Agent.

    Responsibility:
        Evaluate a draft answer against the raw contributing agent
        envelopes.

    Non-responsibilities:
        - Does not generate new scientific facts.
        - Does not select the "correct" source during a conflict.
        - Does not resolve regulatory disputes.
        - Does not replace the Safety Agent.
        - Does not increase confidence.
        - Does not use external datasets.

    The implementation is deliberately deterministic.
    """

    def __init__(self):
        self.agent_id = "verification"
        self.agent_name = "Verification & Consistency Agent"

    def run(
        self,
        *,
        request_id: UUID | str,
        draft_answer: str,
        contributing_envelopes: Iterable[Any],
    ) -> dict:
        """
        Verify a draft answer.

        On internal failure the agent fails closed:
            overall_verdict = "fail"
        """
        try:
            return self._run_internal(
                request_id=request_id,
                draft_answer=draft_answer,
                contributing_envelopes=list(
                    contributing_envelopes
                ),
            )

        except Exception as exc:
            return self._failure_result(
                request_id=request_id,
                message=(
                    "Verification failed closed because an internal "
                    f"verification error occurred: {exc}"
                ),
            )

    def _run_internal(
        self,
        *,
        request_id: UUID | str,
        draft_answer: str,
        contributing_envelopes: list[Any],
    ) -> dict:
        flags: list[dict[str, str]] = []
        claim_checks: list[dict[str, Any]] = []

        if not str(draft_answer).strip():
            return self._failure_result(
                request_id=request_id,
                message=(
                    "draft_answer cannot be empty."
                ),
            )

        if not contributing_envelopes:
            return self._failure_result(
                request_id=request_id,
                message=(
                    "At least one contributing envelope is required."
                ),
            )

        # ------------------------------------------------------------
        # 1. Validate every contributing envelope.
        # ------------------------------------------------------------
        for index, envelope in enumerate(
            contributing_envelopes
        ):
            valid, errors = validate_envelope_structure(
                envelope
            )

            if not valid:
                for error in errors:
                    flags.append(
                        {
                            "code": "ORCA_ERR_SCHEMA_VALIDATION",
                            "message": (
                                f"Envelope {index}: {error}"
                            ),
                            "affected_claim": "",
                        }
                    )

        if flags:
            return {
                "overall_verdict": "fail",
                "claim_checks": [],
                "flags": flags,
                "pass_count": 0,
                "fail_count": 0,
                "caveat_count": len(flags),
                "request_id": str(request_id),
            }

        # ------------------------------------------------------------
        # 2. Extract claims.
        # ------------------------------------------------------------
        claims = self.extract_claims(
            draft_answer
        )

        if not claims:
            flags.append(
                {
                    "code": "ORCA_ERR_NO_CLAIMS",
                    "message": (
                        "No checkable claims were extracted from "
                        "draft_answer."
                    ),
                    "affected_claim": "",
                }
            )

            return {
                "overall_verdict": "pass_with_caveats",
                "claim_checks": [],
                "flags": flags,
                "pass_count": 0,
                "fail_count": 0,
                "caveat_count": 1,
                "request_id": str(request_id),
            }

        # ------------------------------------------------------------
        # 3. Check each claim.
        # ------------------------------------------------------------
        for claim in claims:
            check = self._check_claim(
                claim=claim,
                draft_answer=draft_answer,
                envelopes=contributing_envelopes,
            )

            claim_checks.append(check)

            if not check["traceable_to_evidence"]:
                flags.append(
                    {
                        "code": "ORCA_ERR_UNSUPPORTED_CLAIM",
                        "message": (
                            "Claim could not be traced to explicit "
                            "contributing evidence."
                        ),
                        "affected_claim": claim,
                    }
                )

            if check["contradiction_detected"]:
                flags.append(
                    {
                        "code": "ORCA_ERR_CONFLICTING_SOURCES",
                        "message": (
                            "Contributing agents contain a conflict "
                            "affecting this claim."
                        ),
                        "affected_claim": claim,
                    }
                )

            if not check["confidence_label_consistent"]:
                flags.append(
                    {
                        "code": "ORCA_ERR_CONFIDENCE_MISMATCH",
                        "message": (
                            "The source confidence label is not "
                            "consistent with the available evidence."
                        ),
                        "affected_claim": claim,
                    }
                )

            if check["unsupported_causal_language"]:
                flags.append(
                    {
                        "code": "ORCA_ERR_UNSUPPORTED_CAUSAL_LANGUAGE",
                        "message": (
                            "Causal language was detected without "
                            "explicit causal evidence."
                        ),
                        "affected_claim": claim,
                    }
                )

        # ------------------------------------------------------------
        # 4. Cross-agent consistency.
        # ------------------------------------------------------------
        conflicts = check_consistency(
            contributing_envelopes
        )

        if conflicts:
            self._append_conflict_flags(
                conflicts=conflicts,
                flags=flags,
            )

        # ------------------------------------------------------------
        # 5. Determine final verdict.
        # ------------------------------------------------------------
        overall_verdict = self._overall_verdict(
            claim_checks=claim_checks,
            conflicts=conflicts,
        )

        pass_count = sum(
            check["verdict"] == "pass"
            for check in claim_checks
        )

        fail_count = sum(
            check["verdict"] == "fail"
            for check in claim_checks
        )

        caveat_count = len(flags)

        return {
            "overall_verdict": overall_verdict,
            "claim_checks": claim_checks,
            "flags": flags,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "caveat_count": caveat_count,
            "request_id": str(request_id),
        }

    # -----------------------------------------------------------------
    # Claim extraction
    # -----------------------------------------------------------------

    def extract_claims(
        self,
        draft_answer: str,
    ) -> list[str]:
        """
        Deterministic claim extraction.

        The architecture allows an LLM to split prose into claims, but
        the repository implementation deliberately uses deterministic
        sentence parsing so verification remains testable without an
        external model.

        The verifier never creates a fact that wasn't present in the
        draft.
        """
        text = str(draft_answer).strip()

        # Split on sentence boundaries.
        raw_sentences = re.split(
            r"(?<=[.!?])\s+|\n+",
            text,
        )

        claims: list[str] = []

        for sentence in raw_sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            # Remove markdown bullets/headings.
            sentence = re.sub(
                r"^[#>*\-\d.)\s]+",
                "",
                sentence,
            ).strip()

            if not sentence:
                continue

            # Ignore obvious section labels.
            if len(sentence.split()) < 3:
                continue

            if sentence.endswith(":"):
                continue

            claims.append(sentence)

        return claims

    # -----------------------------------------------------------------
    # Claim checking
    # -----------------------------------------------------------------

    def _check_claim(
        self,
        *,
        claim: str,
        draft_answer: str,
        envelopes: list[Any],
    ) -> dict[str, Any]:
        supporting_agents: list[str] = []
        supporting_evidence: list[int] = []

        confidence_consistent = False
        contradiction_detected = False
        contradicting_agent_id: Optional[str] = None

        all_evidence: list[tuple[str, Any]] = []

        for envelope in envelopes:
            agent_id = envelope_agent_id(
                envelope
            )

            try:
                evidence = extract_evidence(
                    envelope
                )
            except (TypeError, ValueError):
                evidence = []

            for evidence_index, item in enumerate(
                evidence
            ):
                all_evidence.append(
                    (
                        agent_id,
                        item,
                    )
                )

            # Check explicit claim/prose fields in the source envelope.
            source_text = self._envelope_search_text(
                envelope
            )

            if claim_appears_in_text(
                claim,
                source_text,
            ):
                if agent_id not in supporting_agents:
                    supporting_agents.append(
                        agent_id
                    )

        # Conservative evidence linkage:
        #
        # A claim is considered traceable when:
        # 1. the exact normalized claim exists in a contributing envelope,
        #    AND
        # 2. that envelope contains explicit evidence.
        #
        # Reasoning prose alone is never treated as evidence.
        for envelope in envelopes:
            agent_id = envelope_agent_id(
                envelope
            )

            source_text = self._envelope_search_text(
                envelope
            )

            if not claim_appears_in_text(
                claim,
                source_text,
            ):
                continue

            try:
                evidence = extract_evidence(
                    envelope
                )
            except (TypeError, ValueError):
                continue

            if not evidence:
                continue

            if agent_id not in supporting_agents:
                supporting_agents.append(
                    agent_id
                )

            for index in range(
                len(evidence)
            ):
                supporting_evidence.append(
                    index
                )

            confidence_consistent = (
                confidence_consistent
                or confidence_label_consistent(
                    claim,
                    envelope,
                )
            )

        traceable = bool(
            supporting_agents
            and supporting_evidence
        )

        # If an envelope contains evidence but the exact claim isn't
        # repeated, allow structured observation support when the claim
        # clearly contains a variable/value represented by the evidence.
        if not traceable:
            structured_support = self._find_structured_support(
                claim=claim,
                envelopes=envelopes,
            )

            if structured_support:
                supporting_agents.extend(
                    agent
                    for agent in structured_support["agents"]
                    if agent not in supporting_agents
                )

                supporting_evidence.extend(
                    structured_support["evidence_indices"]
                )

                traceable = True
                confidence_consistent = all(
                    structured_support["confidence"]
                )

        # Causal-language check.
        unsupported_causal = (
            contains_unsupported_causal_language(
                claim
            )
            and not causal_language_has_explicit_citation(
                claim,
                [
                    item
                    for _, item in all_evidence
                ],
            )
        )

        # Conflict check only when this claim has multiple supporting
        # sources or when global conflicts touch its terminology.
        relevant_conflicts = self._find_relevant_conflicts(
            claim,
            envelopes,
        )

        if relevant_conflicts:
            contradiction_detected = True

            contradicting_agent_id = (
                relevant_conflicts[0].source_b
                if relevant_conflicts[0].source_a
                in supporting_agents
                else relevant_conflicts[0].source_a
            )

        verdict = "pass"

        if (
            not traceable
            or contradiction_detected
            or unsupported_causal
        ):
            verdict = "fail"

        # A confidence mismatch alone does not necessarily invalidate
        # the factual claim, but the contract requires the claim check
        # to fail when its evidence/confidence state is inconsistent.
        if traceable and not confidence_consistent:
            verdict = "fail"

        source_agent_id = (
            supporting_agents[0]
            if supporting_agents
            else "unknown"
        )

        return {
            "claim_text": claim,
            "source_agent_id": source_agent_id,
            "traceable_to_evidence": traceable,
            "evidence_indices": sorted(
                set(supporting_evidence)
            ),
            "contradiction_detected": contradiction_detected,
            "contradicting_agent_id": (
                contradicting_agent_id
            ),
            "confidence_label_consistent": (
                confidence_consistent
            ),
            "unsupported_causal_language": (
                unsupported_causal
            ),
            "verdict": verdict,
        }

    # -----------------------------------------------------------------
    # Structured support
    # -----------------------------------------------------------------

    def _find_structured_support(
        self,
        *,
        claim: str,
        envelopes: list[Any],
    ) -> Optional[dict[str, Any]]:
        """
        Match simple variable/value statements against structured
        observations.

        This does not perform semantic inference. It only checks whether
        a numeric value and a variable represented in an observation
        appear in the claim.
        """
        normalized_claim = claim.lower()

        agents: list[str] = []
        evidence_indices: list[int] = []
        confidence_values: list[bool] = []

        for envelope in envelopes:
            agent_id = envelope_agent_id(
                envelope
            )

            observations = get_field(
                envelope,
                "observations",
                [],
            )

            if not isinstance(
                observations,
                list,
            ):
                continue

            evidence = get_field(
                envelope,
                "evidence",
                [],
            )

            if not isinstance(
                evidence,
                list,
            ):
                evidence = []

            confidence_ok = (
                confidence_label_consistent(
                    claim,
                    envelope,
                )
            )

            for observation_index, observation in enumerate(
                observations
            ):
                variable = (
                    get_field(
                        observation,
                        "variable",
                        None,
                    )
                    or get_field(
                        observation,
                        "indicator",
                        None,
                    )
                )

                value = get_field(
                    observation,
                    "value",
                    None,
                )

                if variable is None or value is None:
                    continue

                variable_text = str(
                    variable
                ).lower()

                value_text = str(
                    value
                ).lower()

                variable_match = (
                    variable_text in normalized_claim
                )

                value_match = (
                    value_text in normalized_claim
                )

                if not (
                    variable_match
                    and value_match
                ):
                    continue

                agents.append(
                    agent_id
                )

                if evidence:
                    evidence_indices.append(
                        min(
                            observation_index,
                            len(evidence) - 1,
                        )
                    )

                confidence_values.append(
                    confidence_ok
                )

        if not agents or not evidence_indices:
            return None

        return {
            "agents": agents,
            "evidence_indices": evidence_indices,
            "confidence": confidence_values,
        }

    # -----------------------------------------------------------------
    # Conflict relevance
    # -----------------------------------------------------------------

    def _find_relevant_conflicts(
        self,
        claim: str,
        envelopes: list[Any],
    ) -> list[Conflict]:
        conflicts = check_consistency(
            envelopes
        )

        normalized = claim.lower()

        return [
            conflict
            for conflict in conflicts
            if (
                conflict.claim_a.lower() in normalized
                or conflict.claim_b.lower() in normalized
                or any(
                    token in normalized
                    for token in (
                        conflict.claim_a.lower()
                        .replace("=", " ")
                        .split()
                    )
                )
            )
        ]

    def _envelope_search_text(
        self,
        envelope: Any,
    ) -> str:
        """
        Build searchable source text.

        Important:
        this is only used to locate a claim. The actual evidence gate
        still requires a non-empty evidence[] array.
        """
        fields = [
            "final_answer",
            "synthesized_answer",
            "reasoning",
            "query",
        ]

        parts: list[str] = []

        for field in fields:
            value = get_field(
                envelope,
                field,
                None,
            )

            if isinstance(value, str):
                parts.append(value)

        observations = get_field(
            envelope,
            "observations",
            None,
        )

        if isinstance(
            observations,
            list,
        ):
            parts.extend(
                str(observation)
                for observation in observations
            )

        return "\n".join(parts)

    # -----------------------------------------------------------------
    # Overall verdict
    # -----------------------------------------------------------------

    def _overall_verdict(
        self,
        *,
        claim_checks: list[dict[str, Any]],
        conflicts: list[Conflict],
    ) -> str:
        if not claim_checks:
            return "pass_with_caveats"

        if any(
            check["verdict"] == "fail"
            for check in claim_checks
        ):
            # A contradiction or unsupported load-bearing claim is fail.
            return "fail"

        if conflicts:
            return "pass_with_caveats"

        return "pass"

    def _append_conflict_flags(
        self,
        *,
        conflicts: list[Conflict],
        flags: list[dict[str, str]],
    ) -> None:
        for conflict in conflicts:
            flags.append(
                {
                    "code": "ORCA_ERR_CONFLICTING_SOURCES",
                    "message": conflict.reason,
                    "affected_claim": (
                        f"{conflict.claim_a} vs "
                        f"{conflict.claim_b}"
                    ),
                }
            )

    # -----------------------------------------------------------------
    # Fail closed
    # -----------------------------------------------------------------

    def _failure_result(
        self,
        *,
        request_id: UUID | str,
        message: str,
    ) -> dict[str, Any]:
        return {
            "overall_verdict": "fail",
            "claim_checks": [],
            "flags": [
                {
                    "code": "ORCA_ERR_SCHEMA_VALIDATION",
                    "message": message,
                    "affected_claim": "",
                }
            ],
            "pass_count": 0,
            "fail_count": 0,
            "caveat_count": 1,
            "request_id": str(request_id),
        }


__all__ = [
    "VerificationAgent",
]
