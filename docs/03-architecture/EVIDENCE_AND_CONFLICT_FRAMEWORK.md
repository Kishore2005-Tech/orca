# ORCA Evidence & Conflict Framework

This document defines two interconnected systems that sit underneath every stage of `REASONING_FRAMEWORK.md` and every agent defined in `AGENT_ARCHITECTURE.md` / `AGENT_CONTRACTS.md`:

- **Part A — Evidence Grounding**: the mandatory structure every important conclusion must trace back to.
- **Part B — Agent Conflict Resolution**: what happens when agents disagree, including the specific case of Ocean Agent = `HIGH`, Fisheries Agent = `HIGH`, Safety Agent = `DANGEROUS`.

**Governing rule for this whole document:** conflict resolution is a deterministic function of evidence properties (source reliability, freshness, agreement, domain precedence) — never an LLM's free choice of "which agent to believe." Every resolution path below terminates in code, not in a model's discretion. Where the LLM appears, it is producing *explanatory text about a resolution already computed*, never computing the resolution itself.

---

# PART A — Evidence Grounding

## A.1 What Counts as an "Important Conclusion"

Grounding is mandatory for:
- Any `observations[]` item an agent returns (per `AGENT_CONTRACTS.md`).
- Any `interpretations[]` statement (Scientific Interpretation, `REASONING_FRAMEWORK.md` §2.7).
- Any `combined_statements[]` (Cross-Agent Reasoning, §2.8).
- Any `confidence` level/score assignment.
- Any `recommendation` text.
- Any advisory, severity rating, regulatory rule, or ecological status label.

Grounding is **not** required for: purely conversational scaffolding ("Here's what I found:"), restatement of the user's own question, or generic definitions already covered by Knowledge/RAG Agent's own citation mechanism (which has its own grounding — see A.6).

## A.2 The Evidence Grounding Record

Every important conclusion must trace to at least one **Evidence Grounding Record (EGR)** with all nine fields populated:

```json
{
  "source": "string — the organization/program/authority (e.g. 'NOAA NDBC', 'IUCN Red List', 'State of California Dept. of Fish and Wildlife')",
  "dataset": "string — the specific dataset/feed/table name (e.g. 'Buoy 46042 hourly observations', 'CA Recreational Fishing Regulations 2026')",
  "parameter": "string — the exact variable/field measured or asserted (e.g. 'sea_surface_temperature', 'bleaching_alert_level', 'daily_bag_limit')",
  "value": "number | string — the raw value as reported by the source, unmodified",
  "unit": "string | null — physical unit (e.g. 'degC', 'm', 'count'); null only for inherently unitless/categorical values (e.g. an alert level enum)",
  "location": {
    "lat": "number | null",
    "lon": "number | null",
    "region_name": "string | null",
    "jurisdiction": "string | null"
  },
  "timestamp": "string (ISO 8601 UTC) — when the value was observed/published, NOT when ORCA retrieved it",
  "quality": "enum[verified, provisional, estimated, flagged]",
  "retrieval_method": "enum[api_call, database_query, feed_subscription, calculation, document_retrieval]"
}
```

**Relationship to `AGENT_CONTRACTS.md`'s `EvidenceItem`:** the EGR is the fuller grounding record; `EvidenceItem` (envelope-level) is its compact transport form. Mapping:

| EGR field | EvidenceItem field |
|---|---|
| `source` + `dataset` | `source` |
| — | `source_type` (derived from `retrieval_method` + `quality`, see A.4) |
| `dataset` (+ parameter context) | `reference` |
| `timestamp` | `observed_or_published_at` |
| — | `retrieved_at` (added at collection time, not part of EGR itself) |
| `value` | `passage_or_value` |

Every `EvidenceItem` an agent emits must be reconstructable back into a full EGR — if any of the nine EGR fields cannot be populated, the underlying observation is **not eligible** to ground a conclusion (see A.3).

## A.3 Completeness Validation (deterministic, mandatory)

```
function validate_egr(record):
    required = ["source", "dataset", "parameter", "value", "timestamp", "location", "quality", "retrieval_method"]
    # "unit" is the one field allowed to be null; all others must be non-null.
    for field in required:
        if record[field] is None or record[field] == "":
            return INVALID(missing=field)

    if record.location.lat is None and record.location.region_name is None:
        return INVALID(missing="location.lat/region_name")

    if record.quality not in [verified, provisional, estimated, flagged]:
        return INVALID(bad_enum="quality")

    if record.retrieval_method not in [api_call, database_query, feed_subscription, calculation, document_retrieval]:
        return INVALID(bad_enum="retrieval_method")

    return VALID(record)
```

This check runs at Evidence Collection (`REASONING_FRAMEWORK.md` §2.6). Any observation whose EGR fails validation is excluded from grounding an important conclusion — it may still be logged for debugging, but it cannot support an `interpretation`, a `combined_statement`, a `confidence` claim, or a `recommendation`.

## A.4 Evidence Quality Tiers

`quality` is assigned deterministically at ingestion, never chosen by an LLM:

| Quality | Definition | Assignment rule |
|---|---|---|
| `verified` | Direct sensor/observational reading that passed the source's own QC flag | `retrieval_method in [api_call, feed_subscription]` AND source-provided QC flag = pass |
| `provisional` | Model output, or an observation not yet QC-flagged by the source | `retrieval_method = api_call` AND (no QC flag present OR QC flag = pending) |
| `estimated` | Interpolated, extrapolated, or derived via ORCA's own calculation | `retrieval_method = calculation` |
| `flagged` | Failed the source's QC, or failed ORCA's own plausibility check (`REASONING_FRAMEWORK.md` §5) but retained for audit trail | source QC flag = fail, OR ORCA range/plausibility check failed |

**Rule:** a `flagged` EGR can never ground a conclusion presented to the user as fact. It may only ground an internal warning (e.g., "a reading was received but rejected as implausible").

## A.5 Grounding Coverage Requirements by Conclusion Type

| Conclusion type | Minimum EGR coverage |
|---|---|
| Fact lookup (single value) | 1 valid EGR, `quality != flagged` |
| Forecast | 1 valid EGR with `retrieval_method = calculation` or `api_call` to a named model, plus the model's issuance time |
| Ecological/conservation status | 1 valid EGR from a named monitoring program, `quality in [verified, provisional]` |
| Regulatory rule | 1 valid EGR directly from the issuing authority (`retrieval_method = document_retrieval` or `api_call` to the authority's own system) — aggregator-only sourcing is insufficient for `high` confidence (see Part B, source reliability) |
| Safety advisory | 1 valid EGR directly from an authoritative issuing feed, `quality = verified` — estimated/derived safety advisories are not permitted to reach the user as active warnings |
| Cross-agent combined statement | 1 valid EGR **per contributing agent domain**, all sharing overlapping location/time (`REASONING_FRAMEWORK.md` §8) |
| Recommendation | Meets the full evidence-sufficiency gate in `REASONING_FRAMEWORK.md` §10, which itself requires all contributing observations to have valid EGRs |

## A.6 Knowledge/RAG Agent Special Case

Knowledge/RAG Agent's grounding uses the same nine fields with this mapping: `source` = corpus document title, `dataset` = corpus/collection name, `parameter` = the topic/claim the passage supports, `value` = the paraphrased claim text, `unit` = `null`, `timestamp` = document publication date, `quality` = `verified` if peer-reviewed/primary source, `provisional` otherwise, `retrieval_method` = `document_retrieval`. This keeps RAG citations structurally identical to live-data grounding rather than a separate, weaker citation system.

---

# PART B — Agent Conflict Resolution

## B.1 The Problem Statement

Consider a single query — "Is it safe to go fishing near [region] today?" — that invokes three agents, returning:

- **Ocean Agent**: wave-height/current risk = `HIGH`
- **Fisheries Agent**: season/quota status = `HIGH` (demand near cap, or a species close to its catch limit)
- **Safety Agent**: `DANGEROUS` (active small-craft advisory)

These three `HIGH`/`DANGEROUS` labels are **not commensurate** — they come from different domains, different scales, and different consequences. The system must not let an LLM "look at all three and decide what to tell the user." Resolution is a deterministic pipeline over evidence properties and a fixed domain-precedence hierarchy.

## B.2 Source Reliability Tiers

Every EGR's `source` is mapped to a fixed reliability tier at ingestion (not by the LLM):

| Tier | Weight | Definition | Examples |
|---|---|---|---|
| 1 | 1.00 | Primary authoritative source, direct feed | National weather/ocean services, coast guard advisories, national fisheries regulators |
| 2 | 0.80 | Vetted secondary source / peer-reviewed | Peer-reviewed journals, accredited monitoring networks |
| 3 | 0.55 | Modeled/derived/aggregator | Forecast models, data aggregators re-publishing Tier 1/2 data |
| 4 | 0.30 | Low-reliability / anecdotal | Crowd-sourced reports, unverified community submissions |

This table is maintained as static configuration, versioned, and changed only through an explicit config update — never inferred per-query by any agent or the LLM.

## B.3 Freshness Weighting

Each agent has a fixed `max_age` (from `AGENT_CONTRACTS.md` freshness thresholds) and `half_life` for decay:

```
freshness_factor(age_seconds, half_life_seconds) = 2 ^ ( -age_seconds / half_life_seconds )
```

- Ocean Agent (observational): `half_life` = 6h, hard cutoff (`max_age`) = 24h → beyond cutoff, `ORCA_ERR_STALE_DATA`, quality effectively treated as unusable for grounding an active claim.
- Fisheries Agent: `half_life` = 15 days, hard cutoff = 30 days (regulation re-verification window).
- Safety Agent: `half_life` = 1h, hard cutoff = advisory's own `expires_at` — past expiry, the record is dropped entirely, not decayed.

**Effective evidence weight:**
```
effective_weight = reliability_tier_weight * freshness_factor(age, half_life)
```
This is the number used in all comparisons below — never a raw "which agent do I trust more" heuristic.

## B.4 Agent Agreement Scoring

When two or more agents' evidence support the *same* underlying claim (same parameter class, overlapping location/time within tolerance), agreement can raise the evidence *score* within its confidence *level*'s band, but — per `REASONING_FRAMEWORK.md` §9 — can never raise the discrete confidence *level* above the weakest single contributor's level.

```
agreement_bonus = min(0.15, 0.05 * (num_corroborating_sources - 1))
adjusted_score = min(base_score + agreement_bonus, level_ceiling[base_level])
```
`level_ceiling` is a fixed constant per level (e.g., `medium` cannot exceed 0.79 regardless of corroboration — it cannot cross into `high` without new Tier-1/Tier-2 evidence being added to the pool, which is a data event, not a scoring trick).

## B.5 Contradictory Observations

**Detection (deterministic — same as `REASONING_FRAMEWORK.md` §2.9):** two EGRs contradict when `parameter` matches (or is a known-equivalent parameter), `location`/`timestamp` overlap within tolerance, and `value` differs beyond a defined tolerance band for that parameter.

**Resolution order (all deterministic, applied in sequence — stop at first that resolves):**
1. **Reliability tier comparison.** Higher-tier source wins if the gap is ≥ 1 full tier.
2. **Freshness comparison.** If tiers are equal (or within the same tier), higher `effective_weight` (fresher) wins.
3. **Both retained, presented as unresolved.** If tiers and freshness are effectively tied (`effective_weight` difference < 0.05), the conflict is **not** silently resolved — both claims are retained and surfaced to Verification/Coordinator as `unresolved`, forcing `low` confidence on that claim per `REASONING_FRAMEWORK.md` §9.
4. **Domain precedence (safety-relevant claims only).** If the contradiction concerns a safety-relevant fact and steps 1–3 leave it unresolved, the more cautious value is adopted for any user-facing guidance (never the less cautious one), while the unresolved status is still logged and surfaced as a caveat.

No step in this sequence is an LLM decision. The LLM may be asked afterward to *explain* which rule fired and why, for the `reasoning`/caveat text — never to select the winner itself.

## B.6 Missing Data

- **Absence is not negative evidence.** If Ecosystem Agent has no bleaching record for a reef, that means "no data," never "no bleaching."
- Missing data is encoded as an explicit `ORCA_ERR_NO_DATA` on the relevant agent envelope, propagated as a `warnings`/`errors` entry, never silently omitted or backfilled by LLM inference.
- Any conclusion that would require the missing parameter is blocked from reaching `high` or `medium` confidence and, per the Recommendation gate (`REASONING_FRAMEWORK.md` §10), a recommendation depending on that missing parameter is not generated — `blocked_reason: "insufficient evidence"`.

## B.7 Stale Data

- Each agent's freshness cutoff (B.3) is enforced at Evidence Collection. Data beyond `max_age` is not silently used — it is either (a) excluded and reported as `ORCA_ERR_STALE_DATA`/`ORCA_ERR_NO_DATA`, or (b) for Safety Agent specifically, always excluded outright once past `expires_at` (no stale safety data is ever presented as current, per `AGENT_CONTRACTS.md` §4 validation rule).
- Stale data that is retained for context (e.g., "last known reading, 3 days ago") must be explicitly labeled as stale in the output — `quality` is effectively downgraded for weighting purposes even if the source originally marked it `verified`.

## B.8 Safety Override

This is the deterministic rule that governs the exact scenario in B.1.

**Precedence hierarchy (fixed, not computed per-query):**
```
1. Safety Agent: DANGEROUS / advisory active   → BINDING override on any positive recommendation
2. Safety Agent: caution-level advisory         → BINDING modifier — recommendation must include the caution
3. Any domain agent's HIGH physical-risk signal → informational input to Safety Agent's own assessment,
                                                    NOT an independent competing verdict
4. Fisheries Agent's HIGH (administrative)      → never overrides or is overridden by Safety;
                                                    it is reported in its own domain lane (legal/quota context),
                                                    orthogonal to physical safety
5. Any domain agent's MEDIUM/LOW                → informational only
```

**Rule, stated precisely:** Safety Agent does not "compete" with Ocean Agent or Fisheries Agent for which verdict wins — it has structural veto authority over the Recommendation stage. If `safety.advisory_type` is active with `severity in [high, extreme]` (i.e., `DANGEROUS`-equivalent), the Recommendation gate (`REASONING_FRAMEWORK.md` §10) is **automatically forced closed** for any recommendation that would encourage the activity, regardless of what Ocean Agent or Fisheries Agent report.

```
function apply_safety_override(safety_envelope, ocean_envelope, fisheries_envelope):
    if safety_envelope.observations.any(o => o.severity in ["high", "extreme"] and not expired(o)):
        return {
            override: True,
            binding_guidance: "avoid activity — active hazard advisory",
            allow_positive_recommendation: False,
            fisheries_status: fisheries_envelope.observations,   # still reported, informationally
            ocean_status: ocean_envelope.observations,           # still reported, informationally
            confidence_in_override: confidence_from(safety_envelope)  # can be HIGH — the danger claim itself
                                                                       # is well-evidenced even though the
                                                                       # POSITIVE recommendation is blocked
        }
    return { override: False }
```

**Important distinction:** blocking a *positive* recommendation ("go ahead and fish") is not the same as having low confidence. If the Safety Agent's `DANGEROUS` advisory is itself Tier-1, fresh, `verified` evidence, ORCA can and should state the danger with **high confidence** — what's blocked is any recommendation that would contradict it, not the system's ability to say "conditions are dangerous" plainly.

**Worked resolution for B.1's scenario:**
1. Ocean = `HIGH` (wave/current risk) → treated as supporting evidence, folded into Safety's assessment context, not an independent verdict.
2. Fisheries = `HIGH` (quota/season status) → reported in its own lane: "season is open, approaching catch limit" — purely administrative, does not factor into the danger determination at all.
3. Safety = `DANGEROUS` (active advisory, assume Tier 1, fresh, `verified`) → override fires.
4. Final output: **high-confidence safety statement** ("an active small-craft/hazard advisory is in effect — conditions are dangerous"), Fisheries status reported separately as context only ("season is open" is not a green light), **no positive activity recommendation issued**, `blocked_reason: "safety override active"`.
5. `final_confidence` for the *danger claim* = `high` (well-sourced). `final_confidence` for any *activity recommendation* = N/A — none is generated.

This resolves the scenario without ever asking an LLM "which agent should win" — the override is a boolean gate driven by Safety Agent's own evidence tier and freshness, per B.2–B.3.

## B.9 Human Escalation

Deterministic triggers — any one is sufficient:

1. A safety-relevant contradiction reaches B.5 step 3 (unresolved, tied reliability/freshness) **and** the underlying claim concerns immediate physical danger.
2. All available EGRs for a safety-relevant claim are `quality = flagged` (nothing usable to ground the assessment either way).
3. The same contradiction persists across repeated retries within a session (configurable retry count, default 2) without resolving via B.5 steps 1–2.
4. An explicit user signal indicating a possible in-progress emergency (per `AGENT_ARCHITECTURE.md` Safety Agent rules and `AGENT_CONTRACTS.md` `possible_emergency` field).

**Escalation behavior (deterministic, not LLM-authored):**
```
function escalate(trigger_reason):
    return {
        recommendation: null,
        message: STANDARD_ESCALATION_TEXT[trigger_reason],  # fixed templates, not freely generated
        direct_to_authorities: True,
        log_for_human_review: True,
        allow_llm_elaboration: False   # no LLM paraphrase permitted on the safety-critical core message;
                                        # LLM may only add unrelated non-safety context around it, clearly separated
    }
```
The core escalation message itself is drawn from a fixed template set (`STANDARD_ESCALATION_TEXT`), precisely so that a moment of genuine ambiguity or danger is never subject to LLM paraphrase variance.

## B.10 Do Not Let the LLM Choose the Winner — Explicit Boundary List

Extending `REASONING_FRAMEWORK.md` §4 with conflict-specific boundaries:

1. **Reliability tier assignment** is static config, not inferred per-conflict by the LLM.
2. **Freshness/effective-weight computation** is arithmetic (B.3), not an LLM estimate of "how current does this feel."
3. **Contradiction resolution order** (B.5 steps 1–4) is fixed sequence, applied in code; the LLM never picks which step to apply.
4. **The safety override boolean** (B.8) is computed directly from `severity`/`expired()` fields — the LLM cannot decide that a `DANGEROUS` advisory is "probably fine to soften."
5. **Escalation trigger detection** (B.9) is rule-based; the LLM cannot decide a trigger condition doesn't apply once the deterministic check has fired.
6. **Escalation core messaging** uses fixed templates — no LLM-authored substitute for the safety-critical sentence itself.
7. **Domain precedence** (B.8's hierarchy) is a fixed ordering; the LLM cannot reweight Fisheries' administrative `HIGH` against Safety's `DANGEROUS` — they are not on the same axis, and the pipeline never asks the LLM to compare them.

Everywhere in this document, the LLM's permitted role is limited to: (a) phrasing an already-computed resolution in natural language, (b) extracting/parsing claims for the deterministic checkers to operate on, and (c) drafting non-binding `reasoning`/caveat text that accompanies — but never replaces — the structured, code-computed verdict.

---

## Summary: How Part A Feeds Part B

Every conflict resolved in Part B depends entirely on Part A's grounding fields:

- **Reliability tiering (B.2)** keys off `source` + `retrieval_method`.
- **Freshness weighting (B.3)** keys off `timestamp` (age) and the parameter's configured `half_life`.
- **Contradiction detection (B.5)** compares `parameter` + `location` + `timestamp` + `value`.
- **Safety override (B.8)** requires `quality = verified` and an unexpired `timestamp` on the Safety Agent's EGR before it's even eligible to bind.
- **Missing/stale/flagged data (B.6–B.7)** are direct consequences of `quality` and `timestamp` from Part A.

A conclusion with an incomplete Evidence Grounding Record (Part A) can never win a conflict in Part B — it simply isn't eligible to enter the comparison, which is what keeps the whole resolution process deterministic end to end.