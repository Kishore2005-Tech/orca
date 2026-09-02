# PRD.md

# ORCA — Marine Ecosystems Reasoning with Collaborative Agents
## Product Requirements Document

**SIH Problem ID:** SIH26176
**Organization:** Indian Space Research Organisation (ISRO)
**Document Status:** Draft PRD — derived from PROJECT_MASTER.md, PROBLEM_STATEMENT.md, DOMAIN_KNOWLEDGE.md, and approved research documents
**Version:** 1.0
**Last Updated:** 30 August 2026

---

## 0. How to Read This Document

Every requirement below carries a classification inherited from the source documents:

| Tag | Meaning |
|---|---|
| **[OFFICIAL]** | Traceable to the official SIH26176 problem statement |
| **[PROPOSED]** | Team-proposed design decision, not an official mandate |
| **[ASSUMPTION]** | Working assumption pending validation |

No requirement in this PRD should be treated as an official ISRO mandate unless tagged **[OFFICIAL]**. Per PROJECT_MASTER.md's Source Integrity Rule, proposed architecture must never be silently presented as an official requirement.

Every requirement (FR/NFR) includes a testable **Acceptance Criterion**. Requirements that could not be phrased as testable were excluded rather than included in vague form.

---

## 1. Product Vision

**[PROPOSED — from PROJECT_MASTER.md §1.3–1.4 and PROBLEM_STATEMENT.md §27]**

> Transform heterogeneous marine, Earth Observation, and oceanographic information into evidence-grounded, explainable answers to natural-language marine questions — through collaborative AI agents that reason across space, time, and scientific domains, without replacing the authoritative institutions (ISRO, INCOIS, national weather services) that produce the underlying data.

ORCA is **not** a new observation network, a replacement for INCOIS/ISRO services, or an autonomous decision-maker. It is an **orchestration and reasoning layer** that sits above existing marine information infrastructure and converts fragmented, multi-source data into a single, traceable, spatially and temporally correct answer.

Mission statement (from PROJECT_MASTER.md §1.4): ORCA demonstrates how multiple specialized AI agents can collaboratively analyze marine ecosystem observations, connect them with context, reason over evidence, and produce transparent decision support.

---

## 2. Target Users

**[PROPOSED / VALIDATION REQUIRED — PROJECT_MASTER.md §6, PROBLEM_STATEMENT.md §12]**

### Primary Users
- Fishermen and fishing communities (official problem statement's representative questions center on this group)
- Marine ecosystem researchers and oceanographers
- Earth observation / environmental analysts

### Institutional Stakeholders
- Coastal authorities and disaster management agencies
- Maritime operators (vessel routing, sea-state context)
- Fisheries stakeholders and government decision-makers
- Academic and research institutions

### Secondary Users
- Policy analysts and conservation organizations
- Scientific educators and environmental intelligence teams

**Note:** Per PROJECT_MASTER.md §6, specific institutional users and operational responsibilities require validation before being presented as confirmed requirements.

---

## 3. Personas

**[PROPOSED — synthesized from PROBLEM_STATEMENT.md §1, §12, §21; no user research has been conducted, so these are illustrative, not validated]**

### Persona 1 — Ravi, Coastal Fisherman
- **Context:** Operates a small fishing vessel out of a coastal town; decisions are time-sensitive and made early morning.
- **Representative question:** "Is it safe to venture into the sea tomorrow morning?" / "Where is the nearest Potential Fishing Zone today?"
- **Needs:** Fast, simple, low-jargon answers; regional-language support; high reliability since safety is at stake.
- **Constraints:** May have limited technical literacy; likely mobile-first access; low tolerance for ambiguous answers.

### Persona 2 — Dr. Meera, Marine Researcher
- **Context:** Studies coastal ecosystem productivity and environmental anomalies for a research institution.
- **Representative question:** "What environmental changes occurred in this region during this period?" / "Why has fish productivity declined in a particular coastal region?"
- **Needs:** Evidence traceability, access to underlying datasets, ability to inspect confidence/uncertainty, reproducibility.
- **Constraints:** Requires scientific rigor; will not accept unqualified causal claims.

### Persona 3 — Arjun, Coastal Disaster Management Officer
- **Context:** Monitors hazard alerts (cyclone, lightning, high waves) affecting a jurisdiction.
- **Representative question:** "Are there lightning or cyclone alerts in my area?" / "Which fishing zones should be avoided due to hazardous conditions?"
- **Needs:** Timely, authoritative alert aggregation; cannot rely on unverified AI-generated hazard claims.
- **Constraints:** Requires ORCA to clearly attribute alerts to the authoritative source system, not to fabricate hazard determinations.

---

## 4. User Problems

**[Interpretation — PROBLEM_STATEMENT.md §11, §15]**

| ID | Problem | Source |
|---|---|---|
| UP-01 | Users think in natural-language questions; marine information is exposed as datasets, layers, and products | PROBLEM_STATEMENT.md §2.1, §15 Problem 1 |
| UP-02 | A single operational question (e.g., "can I fish tomorrow?") requires combining multiple independent data sources (SST, chlorophyll, wind, waves, tide, alerts) | PROBLEM_STATEMENT.md §5.2, §9 |
| UP-03 | Marine data varies by location; a value from one location is not valid for another | PROBLEM_STATEMENT.md §6 |
| UP-04 | Marine data varies by time (observation vs. forecast vs. historical); undifferentiated data leads to wrong conclusions | PROBLEM_STATEMENT.md §7 |
| UP-05 | Users cannot easily tell which evidence supports a given recommendation | PROBLEM_STATEMENT.md §11.7 |
| UP-06 | Technical/oceanographic terminology and multiple disjoint dashboards create a usability barrier for non-specialist users | PROBLEM_STATEMENT.md §10, §11.5–11.6 |
| UP-07 | Regional-language users are underserved by English-only marine information interfaces | PROBLEM_STATEMENT.md §1, §11.8 |

---

## 5. User Journeys

**[PROPOSED]**

### Journey A — Fisherman Safety Check (Persona: Ravi)
1. Opens ORCA conversational interface (mobile).
2. Asks in natural language (optionally regional language): "Is it safe to fish near [location] tomorrow morning?"
3. ORCA resolves location + time window.
4. ORCA retrieves wind, wave, tide, and hazard-alert data relevant to that location/time.
5. ORCA returns a plain-language answer with a confidence indicator and a link/reference to the source alert or advisory.
6. Ravi can ask a follow-up ("what about the day after?") without repeating context.

### Journey B — Researcher Anomaly Investigation (Persona: Meera)
1. Selects a region and time period via map/timeline UI or conversational query.
2. Asks ORCA to identify significant environmental anomalies in that window.
3. ORCA's agents retrieve historical baseline and recent observations, run comparison, and flag anomalies.
4. ORCA presents evidence panel: which datasets, which agent, what confidence, what remains uncertain.
5. Meera inspects the evidence chain and exports the analytical summary.

### Journey C — Disaster Officer Alert Check (Persona: Arjun)
1. Asks ORCA: "Are there any cyclone or lightning alerts for [region] right now?"
2. ORCA queries hazard/advisory sources and aggregates active alerts for that region.
3. ORCA presents alerts with explicit source attribution and validity window; does not generate its own hazard prediction.

---

## 6. Core Use Cases

**[PROPOSED — PROJECT_MASTER.md §11, PROBLEM_STATEMENT.md §19, §25]**

| ID | Use Case | Goal |
|---|---|---|
| UC-01 | Marine Environmental Analysis | Understand environmental conditions in a selected region/time |
| UC-02 | Anomaly Detection | Identify unusual conditions vs. historical baseline |
| UC-03 | Multi-variable Ecosystem Reasoning | Determine whether changes across variables are related, aligned, or independent |
| UC-04 | Scientific Question Answering | Answer a structured research question with evidence |
| UC-05 | Evidence-backed Decision Support | Convert analysis into a qualified recommendation with confidence/uncertainty |
| UC-06 | Fishing Safety / PFZ Query | Answer "is it safe" / "where should I fish" style operational questions (official representative questions) |
| UC-07 | Hazard/Alert Aggregation | Surface active cyclone, lightning, or high-wave alerts for a location, attributed to source |
| UC-08 | Route Advisory Query | Provide weather/sea-state context along a vessel route |

---

## 7. Functional Requirements

Each FR is independently testable.

### Query Understanding

- **FR-001**: The system shall accept a natural-language marine query as input and extract a structured intent containing, at minimum, a location and a time reference when present in the query.
  *Acceptance:* Given a query containing an explicit location and time phrase, the extracted intent object contains non-null location and time fields matching the input.

- **FR-002**: The system shall support multi-turn conversation, retaining location/time context from a prior turn when a follow-up query omits it.
  *Acceptance:* Given a first query specifying location X, a follow-up query with no location produces a response scoped to location X.

- **FR-003 [OFFICIAL]**: The system shall support query input in at least one Indian regional language in addition to English, per the official SIH26176 requirement for regional-language interaction.
  *Acceptance:* A query submitted in the supported regional language returns a response in the same language.

### Data Retrieval & Orchestration

- **FR-004**: The system shall route a structured intent to the specialized agent(s) whose declared domain matches the intent's required evidence categories (e.g., oceanographic, weather/hazard, ecological).
  *Acceptance:* For a query requiring only hazard-alert data, only the hazard/advisory agent is invoked (verifiable via orchestration logs).

- **FR-005**: The system shall retrieve data only from documented, cataloged data sources with recorded provider, access method, spatial resolution, temporal resolution, and coverage (per PROJECT_MASTER.md §14.3).
  *Acceptance:* Every dataset referenced in a response has a corresponding entry in the data source catalog.

- **FR-006**: The system shall filter retrieved observations to the spatial extent implied by the user's query location, within a documented tolerance radius.
  *Acceptance:* Given a query for location X, no returned observation lies outside the documented tolerance radius of X.

- **FR-007**: The system shall label each retrieved data point as one of: observation, forecast, nowcast, or advisory, and shall not merge these categories without labeling.
  *Acceptance:* Every data point cited in a response carries a visible type label from the defined set.

### Reasoning & Validation

- **FR-008**: The system shall not present a correlation between two variables as a causal relationship without an explicit qualifying statement of uncertainty.
  *Acceptance:* A test query designed to elicit a correlation-based finding produces an output containing an uncertainty/qualification statement alongside the correlation.

- **FR-009**: The system shall route each agent's preliminary conclusion through a validation/critic stage before it is included in the final response.
  *Acceptance:* For any response containing an analytical conclusion, an orchestration log entry shows a validation step executed after the originating agent and before final synthesis.

- **FR-010**: When two agents or data sources produce conflicting values for the same variable, location, and time, the system shall surface the conflict rather than silently resolving it.
  *Acceptance:* Given seeded conflicting test data for the same location/time/variable, the response text or evidence panel explicitly states that a conflict exists.

### Evidence & Explainability

- **FR-011**: Every conclusion presented to the user shall be traceable to at least one named data source, dataset, or prior calculation.
  *Acceptance:* For each conclusion sentence in a response, an associated evidence reference (source name + dataset) is retrievable via the evidence panel/API.

- **FR-012**: The system shall present a confidence or qualitative certainty indicator alongside every non-trivial analytical conclusion (excludes simple data lookups).
  *Acceptance:* A response classified as "analytical" (per UC-01–UC-05) includes a confidence field that is non-null.

- **FR-013**: The system shall explicitly state known uncertainty or evidence gaps when available evidence is insufficient to fully answer the query.
  *Acceptance:* Given a query for a region/time with deliberately incomplete seeded data, the response includes an uncertainty statement referencing the missing evidence.

### Output & Presentation

- **FR-014**: The system shall structure every substantive response according to the ORCA output contract: question, observations, analysis, evidence, confidence, uncertainty, implications, and recommended next step (PROJECT_MASTER.md §26).
  *Acceptance:* A response to a UC-01–UC-05 query contains all eight named sections, each non-empty or explicitly marked "not applicable."

- **FR-015**: The system shall render a map-based spatial visualization when the query response includes location-bound data.
  *Acceptance:* For any response containing at least one geolocated data point, a map visualization is returned alongside the text response.

- **FR-016 [OFFICIAL]**: The system shall aggregate and present active hazard alerts (e.g., cyclone, lightning) for a queried location, with explicit attribution to the issuing authoritative source.
  *Acceptance:* Given a seeded active alert for a test location, a query about that location returns the alert text with a visible source-system attribution field.

- **FR-017**: The system shall never generate its own hazard warning (cyclone, storm, high-wave) that is not attributable to an ingested authoritative source.
  *Acceptance:* A code/prompt review plus a test suite of hazard queries with no seeded authoritative alert confirms no hazard claim is generated in the response.

### Data Quality

- **FR-018**: The system shall flag a retrieved observation as low-confidence when its source metadata indicates missing values, temporal mismatch beyond a documented threshold, or resolution mismatch with the query's requirements.
  *Acceptance:* A seeded observation with a metadata flag (e.g., staleness beyond threshold) is marked low-confidence in the evidence panel.

---

## 8. Non-Functional Requirements

- **NFR-001 (Latency)**: For a single-region, single-time-window query, the system shall return an initial response within a documented target time (e.g., ≤ 15 seconds for prototype), measured end-to-end from query submission.
  *Acceptance:* 95th percentile response time for a defined benchmark query set is measured and does not exceed the documented target.

- **NFR-002 (Traceability)**: 100% of conclusions returned in a response shall carry at least one evidence reference, per FR-011.
  *Acceptance:* Automated evidence-audit script run over a benchmark query set reports zero conclusions without an evidence reference.

- **NFR-003 (Reproducibility)**: Given identical query, location, time window, and underlying dataset snapshot, the system shall produce analytically consistent conclusions across repeated runs (allowing for non-deterministic phrasing but not contradictory findings).
  *Acceptance:* Running the same benchmark query 5 times against a frozen dataset snapshot yields conclusions that do not contradict each other on the core finding (e.g., anomaly present/absent).

- **NFR-004 (Availability of Documented Sources)**: The system shall degrade gracefully — clearly informing the user which evidence category is unavailable — when a documented data source is unreachable, rather than failing silently or fabricating a value.
  *Acceptance:* With a data source intentionally disabled in a test environment, the response explicitly states that data category is unavailable and does not include a fabricated value for it.

- **NFR-005 (Auditability)**: Every orchestration run shall produce a retrievable log capturing which agents were invoked, which data sources were queried, and which validation steps executed.
  *Acceptance:* For any given response, the corresponding orchestration log can be retrieved and contains all three elements.

- **NFR-006 (Scientific Language Constraint)**: The system shall not use causal language ("causes," "results in," "due to") to describe a statistical correlation, per P3 in PROJECT_MASTER.md §24.
  *Acceptance:* An automated lint/check over a benchmark set of correlation-based responses finds zero instances of unqualified causal language.

- **NFR-007 (Multilingual Consistency)**: A response generated in a supported regional language shall convey the same core conclusion (same confidence level, same evidence set) as the English-language response to the equivalent query.
  *Acceptance:* Paired English/regional-language test queries on identical inputs produce conclusions with matching confidence labels and evidence source lists.

- **NFR-008 (Prototype Cost/Scale Constraint)**: The prototype shall operate within a documented compute/LLM-cost budget per query, avoiding unnecessary agent invocations (per PROJECT_MASTER.md §22 R8 mitigation).
  *Acceptance:* Measured average number of agent invocations per benchmark query does not exceed the documented budget ceiling.

---

## 9. MVP Requirements

**[PROPOSED — PROJECT_MASTER.md §9.2, §9.4]**

The MVP is the smallest system that demonstrates the full reasoning loop for one controlled geographic region and a small set of variables, prioritizing **reasoning quality and evidence traceability over agent count or feature breadth**.

MVP must include:
- FR-001, FR-002 (query understanding, multi-turn)
- FR-004, FR-005, FR-006, FR-007 (retrieval + labeling, for a small documented dataset catalog)
- FR-008, FR-009, FR-011, FR-012, FR-013 (reasoning safeguards + evidence + confidence + uncertainty)
- FR-014 (output contract)
- FR-015 (basic map visualization)
- NFR-001 (documented, even if generous, latency target), NFR-002, NFR-005

MVP explicitly excludes: regional-language support (FR-003), hazard alert aggregation (FR-016/FR-017), route intelligence (UC-08), and multi-region support — these are deferred to Prototype/Future scope below unless validated as feasible within timeline.

**Acceptance for MVP as a whole:** A user can submit a natural-language question about one pre-selected demonstration region and time window and receive a response satisfying FR-001, FR-002, FR-004–FR-009, FR-011–FR-015 end-to-end, using only the documented MVP dataset catalog.

---

## 10. Prototype Requirements

**[PROPOSED — PROJECT_MASTER.md §9.2, full 14-item list]**

Building on the MVP, the SIH demonstration prototype additionally includes:
- FR-003 (at least one regional language, if validated feasible — else documented as a known gap, per PROJECT_MASTER.md Q-list)
- FR-010 (conflict surfacing across at least two data sources)
- FR-016, FR-017 (hazard alert aggregation with attribution, for representative official use cases in PROBLEM_STATEMENT.md §1)
- FR-018 (basic data-quality flagging)
- NFR-003, NFR-004, NFR-006, NFR-008

**Prototype demonstration acceptance (PROJECT_MASTER.md §19.5):** The demo must be able to answer, for a live or scripted query: what question ORCA received, what evidence it used, what each agent discovered, how findings were validated, and why the final conclusion was reached — each verifiable by inspecting the orchestration log and evidence panel.

---

## 11. Future Requirements

**[FUTURE — PROJECT_MASTER.md §23, PROBLEM_STATEMENT.md §18]**

Not committed for MVP or prototype; listed for roadmap traceability only:
- Additional specialized agents: Climate, Biodiversity, Fisheries, Pollution, Ocean Circulation, Scientific Literature, Causal Inference, Uncertainty Quantification agents
- Route Intelligence Agent for full vessel-route weather/sea-state advisories (UC-08)
- Multi-region / national-scale coverage beyond the prototype's controlled study area
- Production-grade streaming data infrastructure and knowledge-graph-based reasoning
- Operational integration with institutional dashboards/alerting systems (requires institutional authorization — PROJECT_MASTER.md §23.5)
- Predictive/probabilistic and counterfactual reasoning capabilities

Future items are not to be built speculatively; per the project's core instruction, features are added only where they provide measurable analytical value.

---

## 12. Acceptance Criteria (Summary)

Acceptance criteria are stated per-requirement in Sections 7 and 8. At the product level, ORCA's MVP is considered accepted when:

1. All MVP-tagged FRs and NFRs (Section 9) pass their individual acceptance tests against the documented MVP dataset catalog.
2. Zero unqualified causal claims are found in a benchmark run (NFR-006).
3. 100% evidence traceability holds across the benchmark query set (NFR-002).
4. The full reasoning loop (Observe → Understand → Analyze → Correlate → Challenge → Verify → Synthesize → Explain, per PROJECT_MASTER.md §12.2) is demonstrably exercised end-to-end for at least one scripted query, verifiable via orchestration logs.

---

## 13. Constraints

**[From PROJECT_MASTER.md §20]**

- **Data constraints:** Dataset availability, API limitations, historical coverage, spatial/temporal resolution, missing observations, inconsistent measurement standards across sources.
- **Computational constraints:** Limited prototype infrastructure, LLM inference cost, large geospatial dataset handling, processing latency, storage.
- **Scientific constraints:** Correlation does not establish causation; observational uncertainty; incompatible dataset resolutions; ecological complexity; risk of AI misinterpretation.
- **AI constraints:** Hallucination risk, incorrect reasoning chains, tool-use errors, agent coordination failures, overconfidence, context window limitations.
- **Time constraint:** SIH prototype timeline requires prioritizing the smallest system that convincingly demonstrates Evidence → Collaboration → Reasoning → Decision Intelligence (§20.5).

---

## 14. Dependencies

**[Interpretation — PROBLEM_STATEMENT.md §4, §28]**

- Availability and continued access to ISRO Earth Observation products (ocean colour, SST-related, sea-state, PFZ-related outputs).
- Availability and continued access to INCOIS ocean information services (ecosystem services, hazard/multi-hazard services, forecast/nowcast services).
- Availability of weather/hazard advisory feeds (cyclone, lightning) from authoritative national sources.
- A documented, versioned data source catalog (per PROJECT_MASTER.md §14) must exist and be maintained before FR-005 can be satisfied.
- LLM/agent orchestration framework and model provider selection (open per PROJECT_MASTER.md Q10).
- Verified official wording of SIH26176 (currently a placeholder in PROJECT_MASTER.md §2.1 — open per Q1) — required to finalize FR-003, FR-016 scope.
- Domain-expert review for A4/A5 assumptions in PROJECT_MASTER.md §21 before ecosystem-level analytical claims (UC-03/UC-04) are finalized.

---

## 15. Success Metrics

**[PROPOSED — derived from PROJECT_MASTER.md §19]**

| Metric | Definition | Target (prototype) |
|---|---|---|
| Evidence traceability rate | % of conclusions with a retrievable evidence reference | 100% |
| Causal-language violation rate | Count of unqualified causal claims per benchmark run | 0 |
| End-to-end completion rate | % of benchmark queries that complete the full reasoning loop without error | ≥ documented threshold (to be set during prototype testing) |
| Response latency (p95) | Time from query submission to first complete response | ≤ documented target (NFR-001) |
| Conflict-surfacing accuracy | % of seeded data conflicts correctly surfaced to the user | 100% on seeded test set |
| Demonstration criteria pass rate | % of PROJECT_MASTER.md §19.5 questions answerable via logs/evidence panel for a scripted demo query | 100% |

Quantitative user-facing metrics (e.g., user satisfaction, adoption) are explicitly **not** set as prototype success metrics, since no user study has been conducted (per §6 validation-required note); adding such targets now would misrepresent unvalidated assumptions as commitments.

---

## 16. Out-of-Scope

**[From PROJECT_MASTER.md §10 and PROBLEM_STATEMENT.md §18]**

- Global, real-time marine monitoring infrastructure.
- Fully autonomous decision-making; ORCA is decision-support only, never an autonomous authority over operational/safety/regulatory decisions.
- Presenting unverified causal claims as scientific fact.
- Building a complete ocean digital twin.
- Unlimited/uncontrolled data integration; the prototype uses a controlled, documented dataset set only.
- Direct control of satellites, ships, drones, AUVs, or industrial control systems.
- Replacing INCOIS, ISRO, national weather services, or official warning systems — ORCA consumes and orchestrates their outputs, it does not supersede them.
- Deploying new physical ocean-observation infrastructure (buoys, Argo floats, sensors).
- Acting as a generic chatbot whose primary value is conversational fluency rather than evidence-grounded reasoning.
- Universal prediction claims across all marine phenomena.

---

## 17. Open Items Requiring Resolution Before Final Sign-off

Carried forward from PROJECT_MASTER.md §29–30 as they directly affect PRD scope:

- Q1: Verified official wording of SIH26176 (currently unconfirmed placeholder).
- Q5: Final prototype geographic region selection.
- Q7: Final MVP environmental variable list.
- Q10: AI-agent framework / model provider / infrastructure selection.
- A1–A8 (PROJECT_MASTER.md §30): All listed as "Pending" validation; MVP/Prototype requirements above should be re-checked once these are resolved.
