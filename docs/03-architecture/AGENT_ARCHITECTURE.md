# ORCA Agent Architecture

**ORCA** — Ocean Research, Conservation & Analytics platform.

This document defines the multi-agent architecture for ORCA: eight specialized agents, each with a narrow, non-overlapping mandate, coordinated by a central orchestrator. The design goal is **meaningful separation of concerns** — every agent exists because no other agent can safely or accurately perform its function. Where two candidate agents would have shared >60% of their tool/dataset surface, they were merged (see "Why Not More Agents" at the end).

---

## 1. Ocean Agent

**Purpose**
Answer questions about physical ocean state and forecasts: temperature, salinity, currents, waves, tides, sea level, and weather-at-sea.

**Responsibilities**
- Retrieve and interpret physical oceanographic data (SST, SSH, currents, wave height/period, tidal predictions).
- Generate short-term forecasts and trend summaries from model outputs.
- Flag anomalous physical conditions (marine heatwaves, unusual current shifts).

**Inputs**
- Lat/lon or region bounding box, time range, requested variable(s).
- User query text (natural language) routed from the Coordinator.

**Outputs**
- Structured physical-ocean data object (variable, value, unit, timestamp, location, source).
- Natural-language summary of conditions/forecast.
- Confidence-tagged anomaly flags.

**Tools**
- Ocean model/reanalysis API clients (e.g., HYCOM, Copernicus Marine Service style interfaces).
- Tide prediction calculator.
- Time-series interpolation/aggregation utilities.

**Datasets**
- Satellite altimetry and SST products.
- Buoy/mooring observation networks (e.g., NDBC-style).
- Numerical ocean forecast model output.
- Tide gauge and harmonic constituent tables.

**Algorithms**
- Harmonic tidal prediction.
- Climatological anomaly detection (z-score vs. historical baseline).
- Linear/seasonal trend fitting for short-horizon forecast summaries.

**Prompt Responsibilities**
- Convert raw numeric/gridded output into plain-language description.
- Explicitly state data recency and forecast horizon in every response.
- Never speculate about biological or fisheries impact — hand off, don't infer.

**Rules**
- Must report the data source and observation/forecast timestamp with every value.
- Must not average across incompatible depths or time windows without disclosure.
- Must decline to answer ecosystem, species, or regulatory questions and route them.

**Failure Conditions**
- No data available for requested location/time → return explicit "no data" status, not an estimate.
- Model output stale beyond defined freshness threshold → flag as stale, do not present as current.
- Conflicting values across sources → report both, do not silently pick one.

**Confidence**
- High: recent observational data, single consistent source.
- Medium: model-only or interpolated data.
- Low: extrapolated, out-of-region, or stale data — must be labeled.

**Evidence Requirements**
- Every quantitative claim must cite source dataset + timestamp.
- Forecasts must state model name and issuance time.

**Dependencies**
- Geospatial Agent (for region/coordinate resolution).
- Verification Agent (for cross-source consistency checks on disputed values).

**Forbidden Responsibilities**
- No ecosystem/species interpretation.
- No fisheries regulation guidance.
- No safety advisories (routes to Safety Agent even if physically related, e.g., rogue waves).

**Why this agent exists**
Physical oceanography is a distinct data domain (numerical models, altimetry, tides) with its own units, sources, and failure modes. Mixing it with biology or safety logic would force one agent to reason across incompatible data types and increase hallucination risk on numeric values.

---

## 2. Ecosystem Agent

**Purpose**
Answer questions about marine biology, habitats, biodiversity, and ecological condition (coral health, species distribution, harmful algal blooms, food-web relationships).

**Responsibilities**
- Interpret species occurrence, habitat, and biodiversity data.
- Summarize ecosystem health indicators (reef bleaching status, HAB presence, invasive species reports).
- Contextualize physical ocean anomalies (from Ocean Agent) in ecological terms, only when explicitly handed that data.

**Inputs**
- Species/taxon name, region, time range.
- Ecological indicator query (bleaching, bloom, biodiversity index).
- Optionally, physical-condition data passed from Ocean Agent via Coordinator.

**Outputs**
- Species/habitat status object (taxon, status, region, confidence, source).
- Ecosystem health narrative summary.
- Cross-reference flags when ecological status may relate to a physical anomaly (advisory only, not causal claim).

**Tools**
- Biodiversity database query client (e.g., OBIS/GBIF-style interfaces).
- Bleaching/HAB alert feed reader.
- Taxonomic lookup/normalization utility.

**Datasets**
- Species occurrence records.
- Coral reef monitoring networks.
- Harmful algal bloom alert systems.
- IUCN-style conservation status lists.

**Algorithms**
- Species range/occurrence density mapping.
- Bleaching alert-level classification (degree heating weeks style thresholds, if sourced).
- Simple correlation flagging between environmental anomaly and reported ecological event (explicitly labeled as correlation, not causation).

**Prompt Responsibilities**
- Distinguish observed fact from modeled/predicted ecological status.
- Never assert causation between a physical event and an ecological outcome without cited evidence.
- Use conservation-status terminology precisely (e.g., "vulnerable" vs. "endangered" per source taxonomy).

**Rules**
- Must cite the specific monitoring program/dataset for any health status claim.
- Must not issue fishing or harvest recommendations (routes to Fisheries Agent).
- Must not issue human safety warnings (routes to Safety Agent), even for HABs with human health impact.

**Failure Conditions**
- No occurrence/monitoring data for region → state absence, do not infer presence.
- Taxonomic mismatch/ambiguous species name → ask for disambiguation via Coordinator rather than guessing.

**Confidence**
- High: direct recent monitoring/survey data.
- Medium: modeled distribution or older survey data.
- Low: single anecdotal report or out-of-region proxy data.

**Evidence Requirements**
- Every status claim tied to a named dataset/program and date.
- Correlation claims must show both datasets referenced, explicitly flagged as non-causal.

**Dependencies**
- Ocean Agent (physical context, only as supplied, never self-fetched).
- Geospatial Agent (region resolution, habitat boundary lookup).
- Verification Agent (for any cross-domain causal-sounding claim).

**Forbidden Responsibilities**
- No fisheries quota/regulation content.
- No human safety guidance.
- No independent fetching of physical ocean data (must request via Coordinator).

**Why this agent exists**
Ecological interpretation requires domain-specific taxonomies, conservation frameworks, and a different evidentiary standard than physical data (it must firmly avoid causal overreach). Combining this with Fisheries would blur the line between conservation status and harvest legality, which are governed by different authorities and often in tension.

---

## 3. Fisheries Agent

**Purpose**
Answer questions about commercial/recreational fishing: regulations, quotas, seasons, licensing, catch reporting, and gear restrictions.

**Responsibilities**
- Retrieve current fishing regulations by species, region, and jurisdiction.
- Summarize season/quota status.
- Explain licensing and gear-restriction requirements.

**Inputs**
- Species, region/jurisdiction, date, gear type.
- User intent (recreational vs. commercial).

**Outputs**
- Regulation summary object (jurisdiction, species, rule, effective dates, source authority).
- Season/quota status.
- Plain-language compliance guidance (informational, not legal advice).

**Tools**
- Regulatory database/API client (national and regional fisheries authorities).
- Jurisdiction boundary resolver (via Geospatial Agent).
- Effective-date/versioning checker for regulation text.

**Datasets**
- National/regional fisheries regulation registries.
- Quota and stock-status reports.
- Licensing requirement tables.

**Algorithms**
- Jurisdiction-and-date matching to select the currently effective rule version.
- Quota-remaining calculation from reported landings vs. cap, where source data provides both.

**Prompt Responsibilities**
- Always state jurisdiction and effective date alongside any rule.
- Clearly label output as informational and direct users to the authoritative regulator for legal certainty.
- Never infer a rule for a jurisdiction/species pair that has no direct source match.

**Rules**
- Must not fabricate or extrapolate regulations across jurisdictions.
- Must flag when a regulation may have changed since last verified fetch.
- Must not offer legal certification of compliance — informational only.

**Failure Conditions**
- No regulation found for the jurisdiction/species pair → say so explicitly; do not infer from a neighboring jurisdiction.
- Source regulation text ambiguous or contradictory → escalate to Verification Agent rather than resolve unilaterally.

**Confidence**
- High: directly sourced, dated regulation text from the named authority.
- Medium: aggregator-sourced regulation pending primary-source confirmation.
- Low: regulation inferred by analogy — must not be presented without heavy caveat, and ideally suppressed in favor of "unknown."

**Evidence Requirements**
- Every rule cited with authority name, document/section reference, and effective date.

**Dependencies**
- Geospatial Agent (jurisdiction/boundary resolution).
- Ecosystem Agent (species conservation status, referenced not asserted).
- Verification Agent (regulation currency/consistency checks).

**Forbidden Responsibilities**
- No legal advice or compliance certification.
- No ecological health assessments.
- No safety-at-sea guidance.

**Why this agent exists**
Fisheries regulation is a legal/administrative domain with jurisdiction-specific authority and strict currency requirements — fundamentally different from ecological science or physical oceanography. Errors here have direct legal/financial consequences for users, warranting isolation and stricter evidence rules than a general ecosystem agent would apply.

---

## 4. Safety Agent

**Purpose**
Provide human safety information for marine activity: hazardous conditions, advisories, warnings, and emergency guidance.

**Responsibilities**
- Surface active marine hazard advisories (storms, rip currents, rogue waves, HAB human-health advisories, shark activity alerts).
- Translate physical/ecological hazard data into actionable safety guidance.
- Identify when a query indicates a possible in-progress emergency and prioritize accordingly.

**Inputs**
- Region, activity type (swimming, diving, boating, fishing), time.
- Hazard data supplied by Ocean Agent / Ecosystem Agent via Coordinator.

**Outputs**
- Active advisory list (type, severity, region, issuing authority, expiry).
- Plain-language safety guidance.
- Emergency escalation notice when applicable (directing to local emergency services — never a substitute for them).

**Tools**
- Marine advisory/warning feed reader (coast guard / meteorological authority style).
- Severity classification utility.

**Datasets**
- Government marine warning/advisory feeds.
- Coast guard notice-to-mariners feeds.
- HAB human-health advisory feeds.

**Algorithms**
- Severity ranking/deduplication across overlapping advisories.
- Time-to-expiry and freshness checking.

**Prompt Responsibilities**
- Always lead with the most severe active advisory, if any.
- Never downplay severity; when uncertain, escalate caution rather than reassure.
- Always include a clear statement that this is not a substitute for official emergency services or a Coast Guard channel.

**Rules**
- Must not generate safety guidance without a sourced advisory or clearly labeled general best-practice content.
- Must not suppress or soften an active warning for phrasing/brevity.
- Must treat any apparent real-time emergency signal from the user as highest priority and respond with immediate, direct guidance to contact local emergency services first.

**Failure Conditions**
- Advisory feed unavailable/stale → explicitly state inability to confirm current hazard status; do not imply "all clear."
- Ambiguous location → ask for clarification rather than guess, given the stakes.

**Confidence**
- High: active, dated advisory directly from issuing authority.
- Medium: general seasonal/statistical hazard pattern (e.g., "rip currents common on this coast").
- Low: inferred hazard with no direct advisory — must be labeled as general guidance, not an alert.

**Evidence Requirements**
- Every advisory cited with issuing authority, issue time, and expiry/review time.

**Dependencies**
- Ocean Agent (physical hazard data).
- Ecosystem Agent (biological hazard data, e.g., HABs, dangerous marine life).
- Geospatial Agent (precise hazard-zone boundaries).

**Forbidden Responsibilities**
- No regulatory/fisheries content.
- No ecological research interpretation beyond what's needed for the hazard itself.
- Never claims to be, or replaces, an emergency responder.

**Why this agent exists**
Safety-critical output requires a distinct, stricter behavioral posture (bias toward caution, mandatory escalation language, zero tolerance for stale "all clear" implications) than any research-oriented agent should apply to its normal output. Isolating it prevents safety rules from being diluted by, or bleeding into, general informational agents.

---

## 5. Geospatial Agent

**Purpose**
Resolve, transform, and validate all location, boundary, and spatial-relationship data used by other agents.

**Responsibilities**
- Resolve place names, coordinates, and regions to canonical geospatial identifiers.
- Determine jurisdiction, maritime zone (EEZ, territorial waters, high seas), and habitat/marine-protected-area boundaries.
- Perform spatial queries (distance, containment, intersection) requested by other agents.

**Inputs**
- Place name, coordinate pair, bounding box, or shapefile/geometry reference.
- Spatial query type (containment, distance, nearest-feature).

**Outputs**
- Canonical location object (coordinates, standardized name, jurisdiction, maritime zone).
- Spatial query result (boolean containment, distance value, nearest feature list).

**Tools**
- Geocoding/reverse-geocoding client.
- Maritime boundary (EEZ/territorial sea) lookup.
- GIS spatial-operations library (containment, buffer, distance).

**Datasets**
- Maritime boundary datasets (EEZ, territorial waters).
- Marine protected area registries.
- Administrative/jurisdictional boundary datasets.
- Bathymetry/coastline reference data.

**Algorithms**
- Point-in-polygon containment testing.
- Great-circle distance calculation.
- Coordinate reference system transformation/normalization.

**Prompt Responsibilities**
- Return structured data, not narrative interpretation — this agent supports other agents, it does not answer end users directly except for pure "where is X" queries.
- Always disambiguate ambiguous place names by returning candidates rather than guessing one.

**Rules**
- Must not infer jurisdiction from an outdated boundary dataset without flagging the dataset's vintage.
- Must return all matching candidates when a place name is ambiguous.

**Failure Conditions**
- Unresolvable location string → return explicit failure, not a best-guess coordinate.
- Boundary dataset missing for the requested region → state coverage gap.

**Confidence**
- High: exact coordinate match against current boundary data.
- Medium: place-name geocoding requiring disambiguation.
- Low: fuzzy/partial name match — must be confirmed before use downstream.

**Evidence Requirements**
- Boundary/jurisdiction claims cite the source boundary dataset and its publication/update date.

**Dependencies**
- None upstream (foundational service agent) — consumed by Ocean, Ecosystem, Fisheries, and Safety Agents.

**Forbidden Responsibilities**
- No interpretation of what a location's ocean, ecological, regulatory, or safety status means — pure spatial resolution only.

**Why this agent exists**
Every other domain agent needs consistent, correct spatial resolution (jurisdiction, containment, distance), and getting this wrong silently corrupts downstream answers. Centralizing it avoids four agents each implementing their own (possibly inconsistent) geocoding and boundary logic.

---

## 6. Knowledge/RAG Agent

**Purpose**
Retrieve and synthesize information from ORCA's curated document corpus (research papers, reports, historical records, institutional knowledge) to answer questions not covered by live data feeds.

**Responsibilities**
- Perform retrieval-augmented generation over the ORCA knowledge base.
- Provide background/explanatory context (e.g., "what is a marine heatwave," historical event summaries).
- Supply supporting citations from the document corpus for other agents' claims when requested.

**Inputs**
- Natural-language query.
- Optional filters (document type, date range, topic).

**Outputs**
- Synthesized answer with inline citations to retrieved passages.
- Ranked list of source documents/passages with relevance scores.

**Tools**
- Vector/embedding search over the document corpus.
- Passage re-ranking utility.
- Citation formatter.

**Datasets**
- Curated corpus: peer-reviewed marine science literature, government reports, historical monitoring archives, ORCA-internal documentation.

**Algorithms**
- Dense retrieval (embedding similarity search).
- Re-ranking of retrieved passages by relevance/recency.
- Extractive citation alignment (mapping generated claims back to source passages).

**Prompt Responsibilities**
- Ground every substantive claim in a retrieved passage; do not answer from parametric memory alone when the corpus is the intended source.
- State explicitly when the corpus has no relevant passage, rather than filling the gap from general knowledge.
- Keep quoted text minimal; prefer paraphrase with citation.

**Rules**
- Must not present live/real-time data as if from the static corpus (routes live queries elsewhere).
- Must not synthesize a claim that isn't traceable to at least one retrieved passage.

**Failure Conditions**
- No relevant passages retrieved above similarity threshold → state that the corpus doesn't cover the topic.
- Conflicting passages across sources → present both viewpoints with citations rather than resolving unilaterally.

**Confidence**
- High: multiple concordant, high-relevance passages.
- Medium: single relevant passage or older source.
- Low: only tangentially related passages retrieved — must be labeled as weak support.

**Evidence Requirements**
- Every claim cites the specific document and passage/section retrieved.

**Dependencies**
- Verification Agent (for claims that will be presented as authoritative/factual, especially cross-domain ones).

**Forbidden Responsibilities**
- No live data retrieval (that's Ocean/Ecosystem/Fisheries/Safety Agents' role).
- No spatial computation (routes to Geospatial Agent).

**Why this agent exists**
Retrieval over a static document corpus is a distinct technical pattern (embeddings, re-ranking, extractive grounding) from live API/data-feed querying, and needs its own strict citation discipline. Merging it into a domain agent would either weaken that discipline or force every domain agent to reimplement RAG.

---

## 7. Verification Agent

**Purpose**
Independently check factual claims, cross-source consistency, and evidence sufficiency before final output is returned to the user, acting as ORCA's quality-control layer.

**Responsibilities**
- Cross-check claims from multiple agents for contradiction.
- Confirm that every claim in a composed answer meets its originating agent's evidence requirements.
- Detect and flag unsupported causal language, stale data presented as current, or confidence mismatches.

**Inputs**
- Draft composed answer plus the structured outputs/citations from contributing agents.

**Outputs**
- Verification verdict (pass / pass-with-caveats / fail) per claim and overall.
- List of flagged issues (contradiction, missing citation, stale data, overreach) with suggested corrections.

**Tools**
- Claim-extraction utility (splits composed answer into checkable assertions).
- Cross-reference checker against contributing agents' cited sources.
- Consistency/contradiction detector.

**Datasets**
- None of its own — operates entirely on the outputs and citations of other agents. (Deliberately dataset-free to avoid becoming a competing source of truth.)

**Algorithms**
- Claim-to-citation matching (does each assertion trace to a supplied source?).
- Contradiction detection between two or more agents' outputs on the same fact.
- Confidence-label consistency check (does stated confidence match evidence strength?).

**Prompt Responsibilities**
- Never introduce new factual claims — only evaluate what's already been asserted.
- Be maximally conservative: unclear support should fail verification, not pass with benefit of the doubt.
- Produce specific, actionable flags, not vague "seems fine" judgments.

**Rules**
- Must not approve any claim lacking a traceable source from the originating agent.
- Must escalate unresolved contradictions to the Coordinator rather than picking a winner itself.
- Must run on every composed answer that mixes output from two or more domain agents.

**Failure Conditions**
- Contributing agent supplied no citation for a load-bearing claim → fail that claim.
- Two agents' claims directly contradict → fail overall, return to Coordinator for resolution (see Conflict Handling).

**Confidence**
- Verification itself outputs a verdict, not a confidence score — but records how many claims passed/failed/were caveated for the Coordinator's use.

**Evidence Requirements**
- Every verdict must cite exactly which claim and which source(s) were checked.

**Dependencies**
- Consumes output from all other agents; is itself consumed only by the Coordinator.

**Forbidden Responsibilities**
- No original research, retrieval, or data fetching.
- No direct user-facing responses — output goes to the Coordinator only.

**Why this agent exists**
A system aggregating six independent data domains needs a dedicated cross-check step; any single domain agent verifying its own work is a conflict of interest. Separating verification from generation is the standard way to catch contradictions and unsupported overreach before they reach the user.

---

## 8. ORCA Coordinator

**Purpose**
Route user queries to the correct agent(s), manage multi-agent execution, resolve conflicts, and compose the final response.

**Responsibilities**
- Parse user intent and decompose it into sub-tasks for one or more domain agents.
- Decide execution order (parallel vs. sequential) based on inter-agent dependencies.
- Invoke Verification Agent on any composed multi-agent answer.
- Resolve conflicts flagged by Verification Agent or arising from contradictory agent outputs.
- Compose and return the final user-facing answer.

**Inputs**
- Raw user query (and conversation context).
- All structured outputs from invoked agents.
- Verification Agent's verdict.

**Outputs**
- Final composed, user-facing answer.
- (Internally) execution plan/trace for logging and debugging.

**Tools**
- Intent classifier / task decomposition logic.
- Agent invocation/dispatch layer.
- Response composition/formatting layer.

**Datasets**
- None directly — the Coordinator is a control-plane agent, not a data-plane one.

**Algorithms**
- Dependency-graph construction for the current query (which agents need which other agents' output first).
- Conflict-resolution policy application (see Conflict Handling below).

**Prompt Responsibilities**
- Never answer a domain question directly using its own general knowledge when a domain agent exists for it — always route.
- Clearly attribute which parts of the final answer came from which domain when relevant to trust/citation.
- Surface Verification Agent caveats to the user rather than hiding them for a cleaner-looking answer.

**Rules**
- Must not fabricate or "smooth over" a conflict that Verification Agent flagged as unresolved — must either present both positions or ask the user a clarifying question.
- Must not skip Verification for any answer synthesized from more than one agent.
- Must not invoke an agent outside its defined responsibilities (e.g., must not ask Ocean Agent for a regulation).

**Failure Conditions**
- A required agent is unavailable/errors → inform the user which part of the answer is missing rather than silently omitting it.
- Verification Agent returns "fail" with no resolvable path → return a partial answer with explicit caveat, not a confident-sounding guess.

**Confidence**
- Reports the lowest confidence level among contributing agents as the overall answer confidence, unless Verification specifically downgrades further.

**Evidence Requirements**
- Final answer must preserve the citations/sources supplied by contributing agents; the Coordinator does not add unsourced content.

**Dependencies**
- All seven other agents.

**Forbidden Responsibilities**
- No original domain content generation.
- No bypassing Verification Agent for multi-agent answers.
- No direct dataset/tool access — it orchestrates, it doesn't fetch.

**Why this agent exists**
Someone has to own routing, dependency ordering, conflict resolution, and final composition — without this, every domain agent would need its own routing logic and the system would have no single place to enforce cross-cutting rules like "always verify multi-agent answers."

---

## Orchestration

The Coordinator is the sole entry point for user queries. On receiving a query it:
1. Classifies intent and identifies which domain agent(s) are relevant (Ocean, Ecosystem, Fisheries, Safety, Geospatial, Knowledge/RAG).
2. Builds a dependency graph for this specific query (e.g., "is it safe to fish for X near Y today" touches Geospatial → Ocean + Ecosystem + Safety + Fisheries → Verification → Coordinator composition).
3. Dispatches agents according to that graph, in parallel where possible and sequentially where a real dependency exists.
4. Passes all outputs to the Verification Agent before composing a final answer.
5. Resolves any flagged conflicts, then returns the final answer with preserved citations and confidence labeling.

### Parallel Execution
Agents with no data dependency on one another run concurrently. Example: for "what's the water like and are there any fishing restrictions near Monterey Bay," the Ocean Agent and Fisheries Agent can run in parallel once Geospatial Agent has resolved "Monterey Bay" to coordinates/jurisdiction — both only depend on Geospatial, not on each other.

### Sequential Execution
Agents run in sequence when one strictly requires another's output first:
- Geospatial Agent always resolves location before any domain agent that needs jurisdiction/coordinates runs.
- Safety Agent typically runs after Ocean and/or Ecosystem Agents when its hazard assessment depends on their data (e.g., HAB advisory context from Ecosystem Agent).
- Verification Agent always runs after all contributing domain agents have returned, never in parallel with them.
- The Coordinator's final composition step always runs last.

### Agent Communication
- All inter-agent communication passes through the Coordinator — agents do not call each other directly. This keeps the dependency graph explicit and auditable, and lets the Coordinator enforce the "forbidden responsibilities" boundaries.
- Communication uses structured objects (not free text) between agents wherever the output is going to another agent, so downstream agents parse fields rather than re-interpret prose. Natural-language summaries are generated only for the final user-facing step or when a human-readable field is explicitly part of an agent's defined output.
- Each agent output includes its confidence label and evidence citations as first-class fields, not embedded in prose, so Verification Agent and the Coordinator can process them programmatically.

### Conflict Handling
Conflicts arise when two agents report inconsistent facts (e.g., Ocean Agent's model shows normal temperatures while Ecosystem Agent's bleaching alert implies thermal stress), or when Verification Agent fails a claim.
1. Verification Agent is the first to detect and flag a conflict — it does not resolve it, only reports it with specifics.
2. The Coordinator applies a resolution policy in this order:
   a. Prefer the more recent, higher-confidence, primary-sourced claim if the conflict is a simple staleness/vintage mismatch.
   b. If both claims are current and well-sourced but genuinely disagree, present both to the user explicitly rather than picking one.
   c. If the conflict involves a safety-relevant claim, default to the more cautious interpretation regardless of confidence scores.
3. The Coordinator never silently discards a flagged conflict to produce a cleaner-looking answer.

### Verification
- Verification Agent runs on every answer that draws on more than one domain agent, and on any single-agent answer flagged as high-stakes (safety, regulatory) even if only one agent contributed.
- Verification checks: (1) every claim traces to a cited source, (2) no contradictions between contributing agents, (3) stated confidence matches evidence strength, (4) no causal language unsupported by evidence (particularly guarding Ecosystem Agent output).
- A "fail" verdict blocks composition until the Coordinator either resolves the issue (per Conflict Handling) or the final answer explicitly carries the caveat to the user.

### Coordinator Behavior
- Acts strictly as a control-plane/orchestration layer: it routes, sequences, resolves, and composes, but never originates domain facts.
- Enforces agent boundaries defined in each agent's "Forbidden Responsibilities" — it will not let, e.g., Ocean Agent's output be presented as a safety advisory without passing through Safety Agent.
- Always surfaces the weakest confidence level and any unresolved caveats in the final answer rather than presenting uniform confidence.
- Logs the full execution trace (which agents ran, in what order, what Verification found) for auditability, even though only the composed answer goes to the user.

---

## Why Not More Agents

A few plausible additional agents were deliberately **not** created, because they would not provide meaningful separation:

- **"Weather Agent"** — folded into Ocean Agent. Marine weather and physical ocean state share the same model sources, units, and forecast logic; splitting them would duplicate tooling for no gain in accuracy or clarity.
- **"Climate Agent"** — folded into Ocean Agent (for physical trends) and Knowledge/RAG Agent (for climate science background/context), since climate questions are either long-horizon physical data (Ocean Agent's domain) or literature synthesis (RAG's domain), not a distinct data domain of their own.
- **"Regulation-Lookup Agent" separate from Fisheries Agent** — regulatory lookup *is* the Fisheries Agent's core function; splitting lookup from interpretation would just add a hop with no new capability.
- **"Citation Agent" separate from Verification Agent** — citation-checking is inseparable from claim-verification; a standalone citation agent would need to re-derive the same claim-extraction logic Verification already performs.

The rule applied throughout: an agent earns its existence only if it owns a distinct dataset/tool surface, a distinct evidentiary standard, or a distinct behavioral posture (e.g., Safety Agent's mandatory-caution rule) that would otherwise dilute or be diluted by a neighboring agent.