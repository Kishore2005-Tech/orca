# ORCA Agent Contracts

Machine-readable I/O contracts for every ORCA agent. This document is normative: any agent implementation that does not conform to these schemas is non-compliant. **No agent may return free-form text where a structured field is defined.** Natural-language content is only permitted inside explicitly-typed `string` fields designed to hold prose (e.g., `reasoning`, `summary`), never as a substitute for structured data the Coordinator needs to parse.

All schemas are JSON Schema–style pseudocode for readability; types are `string`, `number`, `boolean`, `object`, `array`, `enum`, or `null`. `?` marks an optional field. All other fields are required.

---

## 0. Standard Response Envelope

Every agent's output — regardless of domain — **must** be wrapped in this envelope. This is what lets the Coordinator consume all eight agents' outputs consistently without agent-specific parsing branches.

```json
{
  "agent_id": "enum[ocean, ecosystem, fisheries, safety, geospatial, knowledge_rag, verification, coordinator]",
  "request_id": "string (uuid v4)",
  "timestamp": "string (ISO 8601 UTC, e.g. 2026-08-31T10:15:00Z)",
  "status": "enum[ok, partial, error]",
  "location": {
    "query": "string | null",
    "resolved": {
      "lat": "number | null",
      "lon": "number | null",
      "region_name": "string | null",
      "jurisdiction": "string | null",
      "maritime_zone": "string | null"
    } | null
  },
  "observations": "array<object> (agent-specific schema, see below)",
  "reasoning": "string | null (short plain-language justification, NOT a substitute for observations/evidence)",
  "evidence": "array<EvidenceItem> (see below)",
  "confidence": {
    "level": "enum[high, medium, low]",
    "score": "number (0.0-1.0)",
    "basis": "string (short, e.g. 'single stale model source')"
  },
  "warnings": "array<{code: string, message: string}>",
  "errors": "array<{code: string, message: string, fatal: boolean}>"
}
```

**EvidenceItem** (shared shape, used by every agent's `evidence` array):

```json
{
  "source": "string (dataset/program/authority name)",
  "source_type": "enum[observation, model, satellite, registry, advisory_feed, document, calculation]",
  "reference": "string (URL, doc ID, or feed ID)",
  "observed_or_published_at": "string (ISO 8601)",
  "retrieved_at": "string (ISO 8601)",
  "passage_or_value": "string | number | null"
}
```

### Standard field definitions

| Field | Meaning |
|---|---|
| `agent_id` | Which agent produced this envelope. Fixed enum — never a free string. |
| `timestamp` | When this envelope was generated (not the data's own timestamp — see `evidence.observed_or_published_at`). |
| `location` | Structured location context, always populated via Geospatial Agent resolution when location is relevant; `null` when not applicable to the query. |
| `evidence` | Every source backing this response. Empty array only permitted when `status = error` or `observations` is empty. |
| `observations` | The agent's structured findings — array of typed objects, schema defined per agent below. Never a prose blob. |
| `reasoning` | Optional short prose explaining how observations were derived or combined. Informational only — the Coordinator/Verification Agent must never parse facts out of this field. |
| `confidence` | Always present, always all three sub-fields populated. |
| `warnings` | Non-fatal issues (e.g., stale-but-usable data). Does not block consumption. |
| `errors` | Fatal or partial-fatal issues. `status` must be `error` if any `errors[].fatal == true`, `partial` if only non-fatal errors/warnings degrade the result. |

### Global error codes (shared across agents)

| Code | Meaning | Typical `fatal` |
|---|---|---|
| `ORCA_ERR_NO_DATA` | No data available for the request scope. | true |
| `ORCA_ERR_STALE_DATA` | Data exceeds freshness threshold. | false (warning-level unless safety-critical) |
| `ORCA_ERR_AMBIGUOUS_LOCATION` | Location string resolves to >1 candidate. | true |
| `ORCA_ERR_SOURCE_UNAVAILABLE` | Upstream API/feed/database unreachable. | true |
| `ORCA_ERR_TIMEOUT` | Agent exceeded its timeout budget. | true |
| `ORCA_ERR_OUT_OF_SCOPE` | Query falls outside this agent's forbidden-responsibilities boundary. | true |
| `ORCA_ERR_CONFLICTING_SOURCES` | Two+ sources disagree beyond tolerance. | false (reported, not fatal — routed to Verification) |
| `ORCA_ERR_SCHEMA_VALIDATION` | Agent's own output failed schema self-check before returning. | true |

Agent-specific error codes extend this table per agent below.

---

## 1. Ocean Agent

**INPUT SCHEMA**
```json
{
  "request_id": "string (uuid v4)",
  "location": { "lat": "number", "lon": "number" } | { "region_name": "string" },
  "time_range": { "start": "string (ISO 8601)", "end": "string (ISO 8601)" },
  "variables": "array<enum[sst, salinity, currents, wave_height, wave_period, tide, sea_level]>",
  "forecast": "boolean"
}
```

**OUTPUT SCHEMA** (envelope `observations[]` item shape)
```json
{
  "variable": "enum[sst, salinity, currents, wave_height, wave_period, tide, sea_level]",
  "value": "number",
  "unit": "string (e.g. 'degC', 'm', 'cm/s')",
  "depth_m": "number | null",
  "valid_at": "string (ISO 8601)",
  "is_forecast": "boolean",
  "anomaly": { "is_anomalous": "boolean", "z_score": "number | null", "baseline_period": "string | null" } | null
}
```

**TOOLS**: ocean reanalysis/model API client; tide harmonic calculator; time-series interpolation utility.

**DATA SOURCES**: satellite altimetry/SST products; buoy/mooring networks; numerical ocean forecast models; tide gauge/harmonic constituent tables.

**VALIDATION**
- `value` must fall within the variable's physically plausible range (e.g., `sst` in [-2, 40] degC) or the observation is rejected and an `ORCA_ERR_SCHEMA_VALIDATION` warning is attached.
- `valid_at` must not be in the future unless `is_forecast = true`.
- At least one of `location.lat/lon` or `location.region_name` must resolve via Geospatial Agent before this agent runs.

**ERRORS**: `ORCA_ERR_NO_DATA`, `ORCA_ERR_STALE_DATA` (freshness threshold: 24h for observations, per forecast model's stated cycle for forecasts), `ORCA_ERR_SOURCE_UNAVAILABLE`, `ORCA_ERR_CONFLICTING_SOURCES`, `ORCA_ERR_OUT_OF_SCOPE` (thrown if request asks for ecological/regulatory interpretation).

**CONFIDENCE**: `high` = single recent observational source; `medium` = model-only or interpolated; `low` = extrapolated/out-of-region/stale. `score` computed as a weighted function of source recency and source count agreement.

**EVIDENCE**: every `observations[]` item must have a matching `evidence[]` entry with `source_type` of `observation`, `model`, or `satellite`.

**TIMEOUT**: 8000 ms.

**FALLBACK**: on timeout or `ORCA_ERR_SOURCE_UNAVAILABLE`, return `status: "error"`, empty `observations`, and a single `errors[]` entry — never return a stale cached value without an explicit `ORCA_ERR_STALE_DATA` warning attached to it.

---

## 2. Ecosystem Agent

**INPUT SCHEMA**
```json
{
  "request_id": "string (uuid v4)",
  "location": { "lat": "number", "lon": "number" } | { "region_name": "string" },
  "taxon": "string | null",
  "indicator": "enum[bleaching, hab, biodiversity, invasive_species, conservation_status] | null",
  "time_range": { "start": "string (ISO 8601)", "end": "string (ISO 8601)" },
  "physical_context": "array<ObservationsFromOceanAgent> | null"
}
```

**OUTPUT SCHEMA**
```json
{
  "indicator": "enum[bleaching, hab, biodiversity, invasive_species, conservation_status]",
  "taxon": "string | null",
  "status_value": "string (e.g. 'Alert Level 2', 'present', 'vulnerable')",
  "observed_at": "string (ISO 8601)",
  "monitoring_program": "string",
  "correlation_flag": {
    "related_physical_event": "string | null",
    "is_causal_claim": "boolean (must always be false)",
    "note": "string"
  } | null
}
```

**TOOLS**: biodiversity database query client; bleaching/HAB alert feed reader; taxonomic normalization utility.

**DATA SOURCES**: species occurrence registries; coral reef monitoring networks; HAB alert systems; conservation status lists.

**VALIDATION**
- `is_causal_claim` must always be `false`; any attempt to set `true` is rejected at the schema level (hard-coded constant).
- `taxon` must resolve against the taxonomic normalization utility before being accepted; unresolved names return `ORCA_ERR_AMBIGUOUS_TAXON`.
- `physical_context` input is only used to populate `correlation_flag`, never merged into `status_value` as fact.

**ERRORS**: `ORCA_ERR_NO_DATA`, `ORCA_ERR_AMBIGUOUS_TAXON` (extends global set), `ORCA_ERR_SOURCE_UNAVAILABLE`, `ORCA_ERR_OUT_OF_SCOPE` (thrown for fisheries/safety-worded requests).

**CONFIDENCE**: `high` = direct recent monitoring/survey data; `medium` = modeled distribution or older survey; `low` = single anecdotal report or out-of-region proxy.

**EVIDENCE**: every `status_value` requires an `evidence[]` entry naming the specific monitoring program and date; `correlation_flag` (if present) requires two evidence entries — one per correlated dataset.

**TIMEOUT**: 8000 ms.

**FALLBACK**: on failure, return `status: "error"` with empty `observations`. Never infer species presence/absence from a neighboring region as a fallback.

---

## 3. Fisheries Agent

**INPUT SCHEMA**
```json
{
  "request_id": "string (uuid v4)",
  "location": { "lat": "number", "lon": "number" } | { "region_name": "string" },
  "jurisdiction": "string | null",
  "species": "string | null",
  "gear_type": "string | null",
  "activity_type": "enum[recreational, commercial]",
  "date": "string (ISO 8601)"
}
```

**OUTPUT SCHEMA**
```json
{
  "jurisdiction": "string",
  "species": "string | null",
  "rule_type": "enum[season, quota, gear_restriction, licensing, closure]",
  "rule_text": "string",
  "effective_from": "string (ISO 8601)",
  "effective_to": "string (ISO 8601) | null",
  "issuing_authority": "string",
  "quota_status": { "cap": "number | null", "landed": "number | null", "unit": "string | null", "remaining": "number | null" } | null,
  "is_informational_only": "boolean (must always be true)"
}
```

**TOOLS**: regulatory database/API client; jurisdiction boundary resolver (calls Geospatial Agent); regulation version/effective-date checker.

**DATA SOURCES**: national/regional fisheries regulation registries; quota/stock-status reports; licensing requirement tables.

**VALIDATION**
- `is_informational_only` is a hard-coded constant `true`; may never be overridden.
- `effective_from`/`effective_to` must bracket the requested `date`, else the rule is not returned (no extrapolation across date gaps).
- `jurisdiction` must match a Geospatial Agent–resolved jurisdiction string exactly — no fuzzy jurisdiction matching.

**ERRORS**: `ORCA_ERR_NO_DATA` (no rule found for jurisdiction/species pair — must not fall back to a neighboring jurisdiction), `ORCA_ERR_STALE_DATA` (regulation source not re-verified within 30 days), `ORCA_ERR_SOURCE_UNAVAILABLE`, `ORCA_ERR_AMBIGUOUS_REGULATION` (extends global set — contradictory source text), `ORCA_ERR_OUT_OF_SCOPE`.

**CONFIDENCE**: `high` = directly sourced dated text from named authority; `medium` = aggregator-sourced pending primary confirmation; `low` = inferred by analogy — in practice `low`-confidence Fisheries output should usually be suppressed in favor of `ORCA_ERR_NO_DATA` rather than returned.

**EVIDENCE**: every rule requires an `evidence[]` entry with `reference` pointing to the authority's document/section and `observed_or_published_at` as the regulation's effective date.

**TIMEOUT**: 6000 ms.

**FALLBACK**: on any failure, return `status: "error"`; never return a rule inferred from a different jurisdiction as a substitute.

---

## 4. Safety Agent

**INPUT SCHEMA**
```json
{
  "request_id": "string (uuid v4)",
  "location": { "lat": "number", "lon": "number" } | { "region_name": "string" },
  "activity_type": "enum[swimming, diving, boating, fishing, general]",
  "physical_context": "array<ObservationsFromOceanAgent> | null",
  "ecological_context": "array<ObservationsFromEcosystemAgent> | null",
  "possible_emergency": "boolean"
}
```

**OUTPUT SCHEMA**
```json
{
  "advisory_type": "enum[storm, rip_current, rogue_wave, hab_health, wildlife_hazard, other]",
  "severity": "enum[low, moderate, high, extreme]",
  "issuing_authority": "string",
  "issued_at": "string (ISO 8601)",
  "expires_at": "string (ISO 8601) | null",
  "guidance_text": "string",
  "emergency_escalation": { "required": "boolean", "instruction": "string" }
}
```

**TOOLS**: marine advisory/warning feed reader; severity classification utility.

**DATA SOURCES**: government marine warning/advisory feeds; coast guard notice-to-mariners feeds; HAB human-health advisory feeds.

**VALIDATION**
- If `possible_emergency == true` in the input, output **must** set `emergency_escalation.required = true` regardless of any other computed severity.
- `severity` must never be silently downgraded from the source feed's stated level.
- `expires_at` in the past at response time invalidates the advisory — it is dropped from `observations` and a warning is logged instead of being presented as active.

**ERRORS**: `ORCA_ERR_SOURCE_UNAVAILABLE` (must be surfaced as "unable to confirm current hazard status," never as implicit all-clear), `ORCA_ERR_AMBIGUOUS_LOCATION` (fatal — safety stakes forbid guessing), `ORCA_ERR_STALE_DATA`, `ORCA_ERR_OUT_OF_SCOPE`.

**CONFIDENCE**: `high` = active dated advisory from issuing authority; `medium` = general seasonal/statistical pattern; `low` = inferred hazard with no direct advisory (must be labeled general guidance, not an alert, in `guidance_text`).

**EVIDENCE**: every advisory requires an `evidence[]` entry with `issuing_authority`, `issued_at`, and `expires_at`/review time.

**TIMEOUT**: 5000 ms (shortest of all agents — safety responses must not be delayed by slow upstream feeds; a slow feed triggers fallback rather than a long wait).

**FALLBACK**: on timeout or source unavailability, return `status: "error"` with `warnings` explicitly stating hazard status could not be confirmed, plus static `emergency_escalation.instruction` directing to local emergency services. Never return "no active advisories" as a fallback default.

---

## 5. Geospatial Agent

**INPUT SCHEMA**
```json
{
  "request_id": "string (uuid v4)",
  "query_type": "enum[geocode, reverse_geocode, jurisdiction_lookup, containment, distance, nearest_feature]",
  "place_name": "string | null",
  "lat": "number | null",
  "lon": "number | null",
  "geometry_ref": "string | null",
  "feature_type": "enum[eez, territorial_sea, mpa, admin_boundary] | null"
}
```

**OUTPUT SCHEMA**
```json
{
  "query_type": "enum[geocode, reverse_geocode, jurisdiction_lookup, containment, distance, nearest_feature]",
  "candidates": [
    {
      "canonical_name": "string",
      "lat": "number",
      "lon": "number",
      "jurisdiction": "string | null",
      "maritime_zone": "string | null",
      "boundary_dataset": "string",
      "boundary_dataset_vintage": "string (ISO 8601 date)"
    }
  ],
  "is_ambiguous": "boolean",
  "spatial_result": { "contains": "boolean | null", "distance_km": "number | null", "nearest_feature_name": "string | null" } | null
}
```

**TOOLS**: geocoding/reverse-geocoding client; maritime boundary lookup; GIS spatial-operations library.

**DATA SOURCES**: maritime boundary datasets (EEZ, territorial waters); marine protected area registries; administrative boundary datasets; bathymetry/coastline references.

**VALIDATION**
- `is_ambiguous = true` whenever `candidates.length > 1`; the agent must never auto-select a "best guess" and set `is_ambiguous = false` when multiple plausible matches exist.
- `boundary_dataset_vintage` is mandatory on every candidate carrying jurisdiction/maritime_zone data.

**ERRORS**: `ORCA_ERR_NO_DATA` (unresolvable location string), `ORCA_ERR_AMBIGUOUS_LOCATION` (non-fatal here — returned as `candidates[]` for the caller to disambiguate, fatal only for downstream Safety Agent), `ORCA_ERR_SOURCE_UNAVAILABLE`.

**CONFIDENCE**: `high` = exact coordinate match against current boundary data; `medium` = place-name geocoding requiring disambiguation; `low` = fuzzy/partial match (must be confirmed downstream before use).

**EVIDENCE**: every `candidates[]` entry's `jurisdiction`/`maritime_zone` requires an `evidence[]` entry citing the boundary dataset and its vintage.

**TIMEOUT**: 3000 ms (foundational, blocking service — kept fast; other agents wait on it).

**FALLBACK**: on failure, return `status: "error"` with empty `candidates`; the Coordinator must halt any dependent agent invocation rather than guess a location.

---

## 6. Knowledge/RAG Agent

**INPUT SCHEMA**
```json
{
  "request_id": "string (uuid v4)",
  "query": "string",
  "filters": { "document_type": "string | null", "date_range": { "start": "string", "end": "string" } | null, "topic": "string | null" } | null,
  "top_k": "number (default 8)"
}
```

**OUTPUT SCHEMA**
```json
{
  "synthesized_answer": "string (must contain inline citation markers referencing evidence[] indices)",
  "passages": [
    {
      "document_title": "string",
      "document_id": "string",
      "section_ref": "string | null",
      "passage_text": "string (excerpt, minimal length)",
      "relevance_score": "number (0.0-1.0)",
      "published_at": "string (ISO 8601) | null"
    }
  ],
  "corpus_coverage": "enum[full, partial, none]"
}
```

**TOOLS**: dense vector/embedding search; passage re-ranker; citation formatter.

**DATA SOURCES**: curated corpus — peer-reviewed marine science literature, government reports, historical monitoring archives, ORCA-internal documentation.

**VALIDATION**
- `corpus_coverage = "none"` requires `passages = []` and `synthesized_answer` must state the corpus has no relevant material — it must not fall back to parametric/general knowledge silently.
- Every sentence-level claim in `synthesized_answer` must be traceable to at least one `passages[]` entry above the relevance threshold (0.55 default).
- `passage_text` excerpts must stay short (paraphrase preferred); this agent must not return long verbatim reproductions.

**ERRORS**: `ORCA_ERR_NO_DATA` (maps to `corpus_coverage: "none"`), `ORCA_ERR_SOURCE_UNAVAILABLE` (index/search backend down), `ORCA_ERR_OUT_OF_SCOPE` (live-data queries misrouted here).

**CONFIDENCE**: `high` = multiple concordant high-relevance passages; `medium` = single relevant passage or older source; `low` = only tangentially related passages (must be labeled weak support in `synthesized_answer`).

**EVIDENCE**: `evidence[]` mirrors `passages[]` one-to-one; every claim in `synthesized_answer` maps to at least one evidence index.

**TIMEOUT**: 7000 ms.

**FALLBACK**: on failure, return `status: "error"`, `corpus_coverage: "none"`, empty `passages`. Never substitute a non-corpus-grounded generative answer.

---

## 7. Verification Agent

**INPUT SCHEMA**
```json
{
  "request_id": "string (uuid v4)",
  "draft_answer": "string",
  "contributing_envelopes": "array<StandardResponseEnvelope> (raw outputs from all agents that contributed to draft_answer)"
}
```

**OUTPUT SCHEMA**
```json
{
  "overall_verdict": "enum[pass, pass_with_caveats, fail]",
  "claim_checks": [
    {
      "claim_text": "string",
      "source_agent_id": "string",
      "traceable_to_evidence": "boolean",
      "contradiction_detected": "boolean",
      "contradicting_agent_id": "string | null",
      "confidence_label_consistent": "boolean",
      "unsupported_causal_language": "boolean",
      "verdict": "enum[pass, fail]"
    }
  ],
  "flags": "array<{code: string, message: string, affected_claim: string}>"
}
```

**TOOLS**: claim-extraction utility; cross-reference checker; contradiction detector.

**DATA SOURCES**: none (operates only on `contributing_envelopes` — deliberately dataset-free, see Architecture doc rationale).

**VALIDATION**
- `overall_verdict = "fail"` if any `claim_checks[].traceable_to_evidence == false` for a load-bearing claim, or any `contradiction_detected == true` is unresolved.
- Verification must not add any `claim_text` not already present in `draft_answer` or `contributing_envelopes` — it evaluates, it does not generate.
- Must run on every `draft_answer` synthesized from ≥2 agents' envelopes, and on any single-agent safety/regulatory answer.

**ERRORS**: `ORCA_ERR_SCHEMA_VALIDATION` (a contributing envelope itself is malformed), `ORCA_ERR_CONFLICTING_SOURCES` (surfaced up, not resolved here).

**CONFIDENCE**: N/A as a scalar — Verification reports a verdict, not a confidence score, but its output includes a pass/fail/caveat count for the Coordinator to factor into final `confidence`.

**EVIDENCE**: every `claim_checks[]` entry cites which `contributing_envelopes[].evidence[]` index(es) it checked.

**TIMEOUT**: 4000 ms.

**FALLBACK**: on internal failure, `overall_verdict` defaults to `fail` (conservative default — verification failing closed, never open).

---

## 8. ORCA Coordinator

**INPUT SCHEMA** (from user-facing layer)
```json
{
  "request_id": "string (uuid v4)",
  "user_query": "string",
  "conversation_context": "array<{role: string, content: string}> | null"
}
```

**OUTPUT SCHEMA** (final, user-facing)
```json
{
  "request_id": "string (uuid v4)",
  "timestamp": "string (ISO 8601)",
  "final_answer": "string",
  "contributing_agents": "array<string (agent_id)>",
  "verification_verdict": "enum[pass, pass_with_caveats, fail]",
  "final_confidence": { "level": "enum[high, medium, low]", "score": "number", "basis": "string" },
  "citations": "array<EvidenceItem> (deduplicated union of contributing agents' evidence)",
  "caveats": "array<string>",
  "unresolved_conflicts": "array<{claim_a: string, claim_b: string, source_a: string, source_b: string}>"
}
```

**TOOLS**: intent classifier / task decomposer; agent dispatch layer; response composer.

**DATA SOURCES**: none directly — control-plane only.

**VALIDATION**
- `final_confidence.level` must equal the **lowest** level among contributing agents' `confidence.level`, unless Verification downgrades further.
- `verification_verdict` must be populated for every response that used ≥2 agents; `pass_with_caveats` requires `caveats[]` to be non-empty.
- `citations` must be a strict subset/union of the `evidence[]` arrays actually returned by contributing agents — the Coordinator introduces no new citations.
- Must never invoke an agent for a request outside that agent's documented scope (cross-checked against each agent's `ORCA_ERR_OUT_OF_SCOPE` boundary).

**ERRORS**: any agent-level fatal error is surfaced as a `caveats[]` entry naming which part of the answer is missing, not silently dropped.

**CONFIDENCE**: derived per the validation rule above — never independently asserted by the Coordinator.

**EVIDENCE**: `citations[]` is populated exclusively from contributing agents' `evidence[]`.

**TIMEOUT**: 20000 ms end-to-end (sum budget across the full dependency graph — individual agent timeouts are enforced independently within this).

**FALLBACK**: if `overall_verdict == "fail"` and no resolvable conflict-handling path applies (see AGENT_ARCHITECTURE.md § Conflict Handling), the Coordinator returns a `final_answer` that explicitly states which part could not be verified, sets `final_confidence.level = "low"`, and populates `unresolved_conflicts[]` rather than presenting a confident-sounding synthesized claim.

---

## Cross-Agent Consumption Guarantee

Because every agent (1–7) emits the **Standard Response Envelope** (§0) with identical top-level field names and types, the Coordinator can consume any agent's output through one shared parser:

```json
function consume(envelope) {
  assert(envelope.agent_id in KNOWN_AGENTS);
  assert(envelope.status in ["ok", "partial", "error"]);
  if (envelope.errors.some(e => e.fatal)) { markUnavailable(envelope.agent_id); }
  registerEvidence(envelope.evidence);
  registerConfidence(envelope.agent_id, envelope.confidence);
  return envelope.observations; // agent-specific typed array, schema per section above
}
```

`observations[]` item shape is the only part that varies per agent — everything else (`agent_id`, `timestamp`, `location`, `evidence`, `reasoning`, `confidence`, `warnings`, `errors`) is structurally identical across all seven domain/service agents, which is what makes uniform Coordinator consumption possible.