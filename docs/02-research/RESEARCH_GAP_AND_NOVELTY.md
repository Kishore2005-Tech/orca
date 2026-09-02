# RESEARCH_GAP_AND_NOVELTY.md

# SIH26176 – ORCA
## Research Gap and Novelty Assessment

**Project:** ORCA – Marine Ecosystems Reasoning with Collaborative Agents  
**Organization:** ISRO  
**Domain:** Marine Ecosystems + Earth Observation + AI + Agentic AI + Decision Intelligence  
**Document purpose:** Establish what already exists, identify defensible research and product gaps, and define ORCA's legitimate novelty without making unsupported originality claims.

---

## 1. Executive Summary

ORCA should **not** claim novelty from any single technology such as:

- a chatbot,
- an LLM,
- RAG,
- multi-agent orchestration,
- marine data fusion,
- knowledge graphs,
- spatial reasoning,
- uncertainty estimation,
- explainable AI, or
- what-if analysis.

All of these capabilities, individually or in closely related combinations, already appear in research and operational systems.

The defensible research gap is instead a **system-level integration gap**:

> **Existing marine systems provide authoritative observations, forecasts, advisories, models, maps, and domain knowledge, while recent AI research provides marine reasoning, knowledge graphs, agentic workflows, and scientific assistants. What remains insufficiently addressed is a unified, evidence-grounded decision-intelligence workflow that coordinates specialized marine reasoning roles across heterogeneous live data, aligns spatial and temporal context, verifies evidence, handles conflicting signals explicitly, quantifies uncertainty, and exposes the reasoning behind a decision to the end user.**

This is a stronger and more defensible positioning than claiming that ORCA invents marine AI reasoning or multi-agent AI.

### Core novelty position

ORCA's strongest legitimate novelty is:

> **A domain-specialized collaborative reasoning layer that integrates heterogeneous marine evidence and converts it into traceable, uncertainty-aware, context-specific decision support.**

This should be treated as a **system/integration novelty**, not a claim that every underlying algorithm is individually novel.

---

# 2. Research Baseline

## 2.1 Existing marine information infrastructure

The marine domain already has mature information services.

### INCOIS PFZ

INCOIS operationally generates Potential Fishing Zone (PFZ) advisories using satellite-derived ocean information, including SST and chlorophyll. Its PFZ products include geographic information and are designed to reduce fishing search time and effort.

**What this establishes:**  
Marine remote sensing is already operationally connected to fisheries decision support.

**What ORCA must not claim:**  
That ORCA invented satellite-derived fishing-zone intelligence.

---

### INCOIS marine services / SAMUDRA ecosystem

INCOIS already provides access to multiple marine parameters and services, including combinations of:

- PFZ information
- currents
- waves
- wind
- tides
- mixed layer depth
- marine heat-wave information
- tsunami information
- other ocean-state products

**Implication:**  
ORCA cannot claim novelty merely because it combines these parameters in a single interface.

The legitimate opportunity is to move from **service access** to **cross-service reasoning**.

---

### INCOIS WebGIS and geospatial marine layers

Interactive marine GIS systems already expose spatial layers such as:

- SST
- chlorophyll
- PFZ
- bathymetry
- EEZ
- landing centres
- other geographic information

**Implication:**  
A marine map is not novel.

ORCA's proposed difference must be the computational reasoning layer operating over those layers.

---

### ISRO / Oceansat and Earth Observation

Indian Earth-observation missions already provide ocean observations relevant to:

- ocean colour
- SST
- wind/scatterometer measurements
- fisheries applications
- marine environmental monitoring

**Implication:**  
ORCA is not a new ocean-observation system. It is an intelligence layer over existing observations.

---

### NASA Ocean Color

NASA provides established ocean-colour products and derived marine indicators, including chlorophyll-related information.

**Implication:**  
ORCA should consume authoritative ocean observations rather than claim to create the underlying scientific measurements.

---

### NOAA IOOS

The U.S. Integrated Ocean Observing System demonstrates mature heterogeneous ocean-data integration across:

- satellites
- buoys
- tide gauges
- radar
- underwater vehicles
- models
- data portals

NOAA explicitly describes the challenge of understanding current and future marine conditions from disparate and complex datasets.

**Implication:**  
Heterogeneous ocean-data integration itself is **not novel**.

The potential gap is how those heterogeneous observations are converted into user-specific, evidence-traceable reasoning.

---

### Copernicus Marine

Copernicus Marine provides global and regional physical and biogeochemical ocean information.

**Implication:**  
Global multi-parameter marine data infrastructure already exists.

ORCA should therefore be positioned as a reasoning/decision layer rather than another data portal.

---

# 3. Existing Marine AI Research

## 3.1 Marine-domain large language models

Recent research has already moved beyond generic LLMs.

Examples include:

- OceanGPT and other ocean-domain language-model research
- marine knowledge-graph-enhanced LLMs
- marine-domain QA systems
- MarineGPT-style marine knowledge systems
- aquaculture-oriented large models

Therefore:

> **"LLM for marine science" is not novel.**

---

## 3.2 Marine reasoning large model

A 2026 paper, **"Building a marine reasoning large model: a method based on structured chain-of-thought fine-tuning and knowledge graph"**, presents a marine-domain reasoning model using:

- a marine corpus,
- knowledge graph construction,
- structured reasoning,
- task decomposition,
- fine-tuning,
- direct preference optimization,
- external knowledge retrieval.

The system explicitly addresses marine-domain multi-step reasoning and reports improved performance when its knowledge graph is used as an external reference.

This is critical prior art.

### Consequence for ORCA

ORCA must **not** claim:

> "ORCA introduces reasoning to marine AI."

That claim is demonstrably false.

A defensible distinction is:

> **ORCA focuses on runtime collaborative reasoning over heterogeneous operational marine data and decision context, rather than primarily training a single marine reasoning foundation model.**

---

# 4. Existing Agentic AI and Multi-Agent Research

## 4.1 Multi-agent systems in marine ecosystem management

Multi-agent approaches have been studied in marine ecosystem management for years.

Prior work has explored:

- environmental agents,
- predator/prey agents,
- fishing agents,
- distributed constraints,
- ecosystem simulation,
- management strategies,
- multi-agent decision support.

Therefore:

> **"Multi-agent AI for marine ecosystems" is not novel by itself.**

---

## 4.2 Multi-agent maritime systems

Recent marine research also applies multi-agent reinforcement learning to:

- autonomous surface vessels,
- cooperative navigation,
- collision avoidance,
- marine debris collection,
- maritime logistics,
- fleet coordination.

Therefore, agent collaboration in a marine environment is an established research direction.

---

## 4.3 Multi-agent LLM systems for Earth science

Recent Earth-science research describes supervisor-agent architectures that dynamically create specialized agents for:

- oceanography,
- geology,
- climatology,
- ecology,
- data retrieval,
- RAG,
- visualization,
- analysis.

Therefore:

> **"A supervisor coordinates specialized scientific agents" is not sufficient novelty.**

---

## 4.4 Agentic AI for ecological and fisheries modelling

Recent work has also investigated agentic AI for automating ecological and fisheries modelling workflows.

This further reduces the defensibility of claiming agentic AI itself as ORCA's novelty.

---

# 5. Existing Decision-Support Systems

Marine decision support is a mature field.

Existing systems already support:

- fisheries management,
- PFZ identification,
- marine hazard assessment,
- ocean forecasting,
- habitat modelling,
- ecosystem modelling,
- navigation,
- search and rescue,
- coastal management,
- environmental impact assessment.

Traditional decision-support systems may use:

- numerical models,
- rules,
- optimization,
- GIS,
- simulation,
- statistical models,
- expert knowledge,
- multi-agent systems.

Therefore:

> **"Decision support for marine management" is not novel.**

ORCA's contribution must be the **architecture and reasoning workflow** connecting these capabilities.

---

# 6. Actual Limitations in Existing Systems

The following limitations are the basis for ORCA's research-gap argument.

## 6.1 Fragmentation of services

Authoritative marine information exists across multiple systems, organizations, formats and APIs.

A user may need to inspect:

- PFZ information,
- SST,
- chlorophyll,
- currents,
- wind,
- waves,
- tides,
- weather,
- bathymetry,
- historical observations,
- forecasts,
- ecosystem indicators.

### Gap

The user often receives **multiple information products**, not one integrated evidence-to-decision workflow.

---

## 6.2 Heterogeneous data semantics

Different datasets can differ in:

- units,
- spatial resolution,
- temporal resolution,
- coordinate reference systems,
- uncertainty,
- observation versus forecast status,
- update frequency,
- provenance,
- quality-control status.

### Gap

Simply placing heterogeneous datasets on one map does not guarantee scientifically valid reasoning across them.

ORCA must explicitly normalize metadata and provenance before reasoning.

---

## 6.3 Spatial heterogeneity

Marine variables exist at different:

- grid resolutions,
- geographic extents,
- observation locations,
- model grids,
- coastal/offshore coverage levels.

A query such as:

> "What is the best fishing area near this location?"

requires more than retrieving a single point.

It can require:

1. locating the relevant spatial region,
2. identifying nearby observations,
3. intersecting multiple layers,
4. accounting for distance,
5. applying geographic constraints,
6. comparing candidate areas.

### Gap

Existing GIS provides the layers, but the reasoning process that converts spatial relationships into a user-specific recommendation is not generally exposed as a unified conversational decision workflow.

---

## 6.4 Temporal heterogeneity

Marine data can include:

- real-time observations,
- hourly measurements,
- daily advisories,
- forecasts,
- historical climatology,
- seasonal patterns.

A question such as:

> "Is it safe tomorrow morning?"

requires temporal alignment.

The system must distinguish:

- current state,
- forecast state,
- historical baseline,
- forecast horizon,
- data timestamp,
- validity period.

### Gap

A generic RAG system is not sufficient for this problem because temporal validity is part of the meaning of the evidence.

---

## 6.5 Cross-domain ecological reasoning

Marine ecosystems are coupled systems.

For example:

```text
SST
 ↓
Front / upwelling / stratification
 ↓
Phytoplankton conditions
 ↓
Zooplankton / productivity
 ↓
Fish habitat suitability
 ↓
Potential fishing opportunity
```

At the same time:

```text
Wind + waves + currents + weather
 ↓
Operational safety
```

A fishing recommendation therefore requires both:

- ecological suitability, and
- operational feasibility/safety.

### Gap

Individual services typically optimize or report a particular domain rather than expose a unified cross-domain reasoning chain.

---

# 7. Reasoning Gaps

## 7.1 From retrieval to reasoning

Many systems retrieve information.

ORCA's target is:

```text
Retrieve → Correlate → Interpret → Validate → Resolve conflicts → Decide → Explain
```

The gap is not retrieval itself.

It is **evidence synthesis under heterogeneous constraints**.

---

## 7.2 From single-model reasoning to distributed expertise

Different marine variables require different scientific interpretations.

Examples:

- Oceanographic interpretation
- Ecological interpretation
- Fisheries interpretation
- Weather/safety interpretation
- Geospatial interpretation

A single generic model may not expose these perspectives separately.

ORCA proposes specialized reasoning roles.

However, specialized agents alone are not novel.

The novelty opportunity is their **evidence-aware coordination and adjudication**.

---

# 8. Evidence-Grounding Gaps

Marine decisions are highly sensitive to:

- source quality,
- timestamp,
- spatial validity,
- forecast horizon,
- model version,
- uncertainty,
- conflicting observations.

A fluent LLM answer without provenance is not sufficient.

## Desired ORCA evidence chain

```text
Claim
 ↓
Evidence
 ↓
Source
 ↓
Timestamp
 ↓
Spatial validity
 ↓
Transformation / calculation
 ↓
Reasoning step
 ↓
Recommendation
```

### Research gap

Existing marine AI research has demonstrated knowledge grounding through:

- knowledge graphs,
- domain corpora,
- retrieval,
- external references.

ORCA should therefore not claim evidence grounding as an invention.

The defensible contribution is:

> **Operational, cross-source evidence grounding connected directly to a decision graph and user-specific marine context.**

---

# 9. Spatiotemporal Reasoning Gaps

## 9.1 Spatial reasoning

ORCA may need to answer:

- nearest PFZ,
- distance from a landing centre,
- overlap between high chlorophyll and favourable SST,
- proximity to hazardous conditions,
- whether a location lies inside an allowed geographic region,
- whether a candidate area satisfies multiple spatial constraints.

This requires structured geospatial computation, not just LLM text generation.

---

## 9.2 Temporal reasoning

ORCA may need to distinguish:

```text
Observed now
      ↓
Forecast later
      ↓
Historical baseline
      ↓
Anomaly
      ↓
Expected trend
```

A scientifically valid answer must avoid mixing these temporal states.

---

## 9.3 Combined spatiotemporal reasoning

The strongest ORCA opportunity is the intersection:

> **Where + when + under what marine conditions?**

For example:

> "Where is the most promising area tomorrow morning within 30 km of this landing centre, while avoiding unsafe wave and wind conditions?"

This is substantially more demanding than answering a static marine-data question.

---

# 10. Conflict-Resolution Gaps

Marine datasets and models can disagree.

Examples:

- satellite observation versus model estimate,
- forecast versus latest observation,
- different model products,
- ecological suitability versus safety constraints,
- historical pattern versus current anomaly.

A conventional dashboard displays the values.

A generic chatbot may select one value implicitly.

ORCA should make disagreement explicit.

## Proposed conflict workflow

```text
Agent A → Evidence + interpretation
Agent B → Evidence + interpretation
Agent C → Evidence + interpretation
             ↓
       Conflict Detector
             ↓
       Evidence Validator
             ↓
       Source / freshness / quality weighting
             ↓
       Consensus or unresolved disagreement
             ↓
       Confidence estimate
             ↓
       Recommendation
```

### Important novelty qualification

Agent conflict resolution is **not novel in the general multi-agent literature**.

Its potential novelty lies in applying a **marine-domain evidence adjudication policy** that considers:

- source authority,
- freshness,
- spatial validity,
- temporal validity,
- measurement/model distinction,
- uncertainty,
- safety constraints.

That is a more defensible claim.

---

# 11. Explainability Gaps

## Existing explainability

Explainable AI is an established field.

Citations, confidence scores, feature importance, rules and model explanations already exist.

Therefore:

> **"Explainable AI" is not novel.**

## ORCA's proposed contribution

ORCA can expose a **marine decision graph**:

```text
User Question
      ↓
Intent / Constraints
      ↓
Relevant Data
      ↓
Ocean Conditions
      ↓
Ecological Conditions
      ↓
Fisheries Conditions
      ↓
Safety Conditions
      ↓
Conflicts / Uncertainty
      ↓
Evidence Validation
      ↓
Recommendation
```

The value is not merely visual explainability.

The graph can act as a **traceability structure connecting evidence to a decision**.

This is more defensible as a system-level contribution.

---

# 12. User-Interface Gaps

Existing marine portals commonly expose:

- maps,
- charts,
- layers,
- advisories,
- dashboards,
- reports,
- data portals.

These are useful but can require domain expertise.

Conversational interfaces reduce the barrier to expressing complex questions.

However:

> **A conversational marine interface is not novel by itself.**

The potential ORCA distinction is:

> **Conversational access to a verifiable multi-step marine decision workflow.**

The user should be able to ask:

> "Is it suitable to go fishing tomorrow morning from this location?"

and receive:

1. interpreted intent,
2. selected evidence,
3. spatial context,
4. temporal context,
5. agent assessments,
6. conflicts,
7. uncertainty,
8. recommendation,
9. reasoning graph,
10. source trace.

---

# 13. Novelty Evaluation Matrix

The following classifications are intentionally conservative.

| Proposed differentiator | Classification | Reason |
|---|---|---|
| Collaborative marine agents | **PARTIALLY NOVEL** | Multi-agent marine ecosystem and maritime research already exists. ORCA can differentiate through specialized agents coordinated around live heterogeneous evidence and decision context. |
| Heterogeneous data fusion | **EXISTING** | IOOS, Copernicus Marine, INCOIS and many oceanographic systems already integrate heterogeneous observations/models. |
| Evidence-grounded reasoning | **PARTIALLY NOVEL** | Marine reasoning research already uses knowledge graphs and external knowledge; RAG/evidence grounding is established. ORCA can differentiate through operational source/provenance/temporal/spatial grounding tied to decisions. |
| Agent conflict resolution | **PARTIALLY NOVEL** | Multi-agent coordination, negotiation and constraint resolution are established. Marine evidence adjudication using source authority, freshness, uncertainty and safety constraints is a stronger ORCA-specific integration opportunity. |
| Confidence / uncertainty | **EXISTING** | Uncertainty estimation and confidence-aware decision support are established research areas. |
| Temporal reasoning | **EXISTING** | Time-series reasoning, forecasting, temporal databases and spatiotemporal analysis are established. |
| Spatial reasoning | **EXISTING** | GIS, spatial databases, geospatial analysis and spatial decision support are mature fields. |
| Explainable decision graph | **PARTIALLY NOVEL** | Explainability and provenance graphs exist; a domain-specific graph connecting heterogeneous marine evidence, agent assessments, conflicts and final decisions is a defensible system-level contribution. |
| What-if analysis | **EXISTING** | Scenario analysis, simulation, digital twins and decision-support systems already support hypothetical scenarios. |
| Cross-domain marine decision intelligence | **PARTIALLY NOVEL** | Individual pieces exist, but ORCA's potential contribution is their unified evidence-grounded orchestration across oceanography, ecology, fisheries, weather, safety and geospatial context. |
| User-specific contextual marine recommendations | **PARTIALLY NOVEL** | Decision-support personalization exists, but combining user constraints with live marine evidence and traceable reasoning creates a stronger integrated contribution. |
| Evidence → conflict → uncertainty → decision chain | **PARTIALLY NOVEL** | Each component is established; the potential contribution is the integrated marine-specific workflow. |

---

# 14. Why the Strongest Claim Is Not "Multi-Agent AI"

A weak ORCA novelty statement would be:

> "ORCA uses multiple AI agents."

This is insufficient because:

- multi-agent systems are established,
- marine multi-agent systems exist,
- multi-agent reinforcement learning is active in maritime applications,
- multi-agent LLM systems are now common,
- Earth-science multi-agent architectures already use specialized agents.

A stronger statement is:

> **ORCA uses specialized marine agents as an evidence-adjudication architecture rather than merely as parallel chatbots.**

The agents should have explicit scientific responsibilities and produce structured evidence objects.

---

# 15. ORCA's Legitimate Novelty

## 15.1 Primary novelty

### Evidence-grounded collaborative marine reasoning

ORCA's central novelty should be framed as:

> **A domain-specialized collaborative reasoning layer that orchestrates heterogeneous marine observations, forecasts, advisories and scientific knowledge into traceable, uncertainty-aware decisions.**

This is a **system-level novelty claim**.

It does not claim that any single component is new.

---

## 15.2 Secondary novelty

### Marine evidence adjudication

ORCA can implement a structured policy for deciding how conflicting marine evidence should be treated.

Potential dimensions:

- source authority,
- timestamp,
- forecast horizon,
- spatial match,
- temporal match,
- quality-control status,
- observation versus model,
- uncertainty,
- safety relevance.

This creates a principled bridge between multi-agent outputs and decision support.

---

## 15.3 Secondary novelty

### Decision graph as an evidence structure

Rather than presenting a generic explanation, ORCA can represent:

```text
Question
  ↓
Constraints
  ↓
Data sources
  ↓
Derived indicators
  ↓
Agent assessments
  ↓
Conflicts
  ↓
Resolution
  ↓
Confidence
  ↓
Recommendation
```

This graph can make the recommendation auditable.

---

## 15.4 Secondary novelty

### Cross-domain marine context

ORCA should reason across:

```text
Physical Oceanography
        +
Marine Biology
        +
Fisheries
        +
Weather / Hazards
        +
Geospatial Context
        +
Historical / Forecast Context
```

The novelty is not that these disciplines exist.

The novelty opportunity is the **joint reasoning workflow** that treats them as interacting evidence sources for one decision.

---

# 16. What ORCA Should Explicitly NOT Claim

To preserve scientific credibility, ORCA should avoid claims such as:

### ❌ "ORCA is the first marine AI system."

False.

### ❌ "ORCA invents multi-agent marine intelligence."

False.

### ❌ "ORCA is the first marine reasoning model."

False.

Recent marine reasoning-model research already exists.

### ❌ "ORCA is the first system to fuse ocean datasets."

False.

Operational observing systems already perform heterogeneous data integration.

### ❌ "ORCA invented uncertainty-aware decision support."

False.

Uncertainty-aware decision support is established.

### ❌ "ORCA invented explainable AI."

False.

Explainable AI is a mature research area.

### ❌ "ORCA invented what-if analysis."

False.

Scenario analysis and digital twins already support what-if reasoning.

---

# 17. Recommended Novelty Statement

## Short version

> **ORCA is an evidence-grounded collaborative marine reasoning engine that integrates heterogeneous oceanographic, ecological, fisheries, weather and geospatial evidence, coordinates specialized domain agents, explicitly resolves conflicting evidence, estimates uncertainty, and exposes a traceable decision graph for context-specific marine decisions.**

---

## Research-oriented version

> **The proposed contribution is a system-level architecture for evidence-grounded collaborative marine decision intelligence. Rather than developing another marine data portal, domain LLM, or generic multi-agent chatbot, ORCA coordinates specialized domain agents over heterogeneous operational and scientific marine data, performs spatiotemporal context alignment, validates provenance and evidence, adjudicates conflicting assessments, propagates uncertainty into the recommendation, and exposes the resulting evidence-to-decision chain through an explainable decision graph.**

---

# 18. Novelty Decomposition

ORCA's novelty should be decomposed into layers.

```text
                 ORCA
                   │
       ┌───────────┴───────────┐
       │                       │
   Existing primitives     Integration layer
       │                       │
       ├─ LLM                  ├─ Marine agent roles
       ├─ RAG                  ├─ Evidence objects
       ├─ GIS                  ├─ Cross-domain reasoning
       ├─ Data fusion          ├─ Conflict adjudication
       ├─ Forecasting          ├─ Uncertainty propagation
       ├─ Knowledge graphs     ├─ Decision graph
       ├─ Explainability       └─ Context-aware decisions
       └─ What-if analysis
```

### Key principle

> **ORCA's novelty is primarily in the integration and orchestration of established technologies around a marine evidence-to-decision workflow.**

---

# 19. Research Gap → ORCA Response Mapping

| Research / system gap | ORCA response |
|---|---|
| Marine services are distributed | Unified reasoning layer |
| Multiple scientific domains | Specialized marine agents |
| Heterogeneous data formats | Data normalization + evidence abstraction |
| Different spatial resolutions | Spatial alignment and geospatial computation |
| Different temporal resolutions | Temporal alignment and validity checks |
| Multiple forecasts/observations | Evidence ranking and validation |
| Agent/model disagreement | Conflict detection and adjudication |
| LLM hallucination risk | Evidence-grounded generation |
| Uncertain marine conditions | Confidence / uncertainty representation |
| Expert interpretation barrier | Natural-language interaction |
| Black-box recommendation | Explainable decision graph |
| Static information | Context-aware recommendations |
| Need to explore scenarios | What-if analysis |
| Multiple stakeholders | Role/context-aware decision support |

---

# 20. Required Technical Behavior for the Novelty to Be Real

The novelty claim is only credible if the prototype actually demonstrates the corresponding mechanisms.

## Minimum architecture

```text
User
  ↓
Intent + Constraints
  ↓
ORCA Coordinator
  ↓
┌────────┬──────────┬──────────┬────────┬──────────┐
│ Ocean  │ Ecology  │ Fishery  │ Safety │ Geo      │
│ Agent  │ Agent    │ Agent    │ Agent  │ Agent    │
└────────┴──────────┴──────────┴────────┴──────────┘
  ↓
Evidence Normalization
  ↓
Evidence Validation
  ↓
Conflict Detection
  ↓
Conflict Resolution
  ↓
Uncertainty / Confidence
  ↓
Decision Synthesis
  ↓
Explainable Decision Graph
  ↓
User
```

---

# 21. Evidence Object Requirement

Each agent should ideally return structured evidence rather than free-form prose.

Example conceptual object:

```json
{
  "agent": "OceanAgent",
  "parameter": "SST",
  "value": 28.4,
  "unit": "°C",
  "location": {
    "lat": 13.0,
    "lon": 80.3
  },
  "timestamp": "2026-08-30T12:00:00Z",
  "source": "authoritative_source",
  "source_type": "observation",
  "quality": "validated",
  "confidence": 0.91,
  "interpretation": "..."
}
```

The exact schema can evolve.

The important architectural principle is:

> **Reason over structured evidence, not only over natural-language summaries.**

---

# 22. Conflict Resolution Requirement

ORCA should not silently choose between conflicting outputs.

Example:

```text
Satellite observation:
SST = 29.1°C

Model forecast:
SST = 28.5°C

Historical baseline:
SST = 27.8°C
```

ORCA should identify:

- observation/model distinction,
- timestamp differences,
- forecast horizon,
- uncertainty,
- relevance to the user's requested time,
- whether the disagreement materially changes the decision.

The output should communicate uncertainty rather than hide it.

---

# 23. Confidence Requirement

A confidence score should not be presented as an arbitrary LLM probability.

A defensible ORCA confidence model could incorporate:

```text
Source reliability
        +
Freshness
        +
Spatial match
        +
Temporal match
        +
Data quality
        +
Agent agreement
        +
Model uncertainty
        +
Decision sensitivity
```

The exact mathematical formulation is a future implementation and evaluation task.

---

# 24. What-If Analysis: Correct Positioning

What-if analysis is already established.

ORCA should therefore position it as an **application of existing scenario-analysis techniques to the evidence graph**.

Example:

> "What happens to the fishing recommendation if wave height increases by 0.8 m tomorrow morning?"

Possible workflow:

```text
Baseline evidence
       ↓
Modify scenario variable
       ↓
Recompute affected constraints
       ↓
Re-evaluate agents
       ↓
Resolve conflicts
       ↓
Recalculate confidence
       ↓
Compare with baseline
```

This becomes more distinctive when it is integrated with ORCA's evidence and decision graph.

---

# 25. Strongest Demonstration of Novelty

The strongest prototype demonstration should be a single realistic query.

### Example

> **"Is it suitable to go fishing tomorrow morning from this location, and where is the nearest promising fishing area?"**

ORCA should visibly demonstrate:

1. Natural-language intent extraction
2. Spatial constraint extraction
3. Temporal constraint extraction
4. Task decomposition
5. Specialized agent activation
6. Marine data retrieval
7. Evidence normalization
8. Cross-domain reasoning
9. Conflict detection
10. Conflict resolution
11. Confidence estimation
12. Recommendation generation
13. Source attribution
14. Explainable decision graph
15. Map update
16. Optional what-if analysis

This demonstration proves that the core innovation is the **reasoning workflow**, not the UI.

---

# 26. Novelty Claims: Final Classification

## NOVEL

None of the listed individual capabilities should be claimed as unqualified "NOVEL" based on the current evidence.

This is deliberate.

A defensible research document should prefer **"partially novel"** or **"system-level integration novelty"** over an unsupported first-of-its-kind claim.

---

## PARTIALLY NOVEL

The strongest candidates are:

1. **Collaborative marine agents**
   - Established concept.
   - Potentially differentiated by evidence-aware specialization and runtime coordination.

2. **Evidence-grounded reasoning**
   - Established through RAG, knowledge graphs and marine reasoning models.
   - Potential differentiation through operational provenance, spatial/temporal validity and decision traceability.

3. **Agent conflict resolution**
   - Established in multi-agent systems.
   - Potentially differentiated by marine-specific evidence adjudication.

4. **Explainable decision graph**
   - Explainability and provenance are established.
   - Potentially differentiated by linking marine evidence, agent assessments, conflicts, uncertainty and final decision.

5. **Cross-domain marine decision intelligence**
   - Individual components exist.
   - The integrated architecture remains the strongest ORCA positioning.

---

## EXISTING

The following should be treated as established capabilities:

- heterogeneous data fusion,
- uncertainty estimation,
- temporal reasoning,
- spatial reasoning,
- explainable AI in general,
- what-if analysis,
- marine data portals,
- GIS,
- RAG,
- knowledge graphs,
- LLM-based marine QA,
- multi-agent systems,
- marine ecosystem modelling,
- marine decision support.

ORCA may use these capabilities, but should not claim ownership of the underlying concepts.

---

## NOT SUFFICIENTLY NOVEL

The following, by themselves, are not enough to distinguish ORCA:

- "A chatbot for marine data"
- "An LLM for ocean science"
- "A multi-agent chatbot"
- "A dashboard combining SST and chlorophyll"
- "A map with PFZ"
- "RAG over marine documents"
- "A marine knowledge graph"
- "Confidence score on an LLM answer"
- "Spatial filtering"
- "Historical comparison"
- "What-if questions"
- "Explainable AI"
- "Multiple APIs connected to one interface"

---

# 27. Final Research-Gap Statement

> **The research gap addressed by ORCA is not the absence of marine data, marine AI, multi-agent systems, or decision-support technology. These capabilities already exist independently and, in some cases, in partial combinations. The gap is the lack of a unified, operationally grounded reasoning workflow that treats heterogeneous marine observations, forecasts, advisories, ecological indicators, geospatial constraints and scientific knowledge as explicit evidence; coordinates specialized domain reasoning over that evidence; identifies and adjudicates conflicts; accounts for spatiotemporal validity and uncertainty; and produces a traceable, user-specific decision rather than merely returning data or a generated answer.**

---

# 28. Final ORCA Novelty Statement

> **ORCA's legitimate novelty is a system-level evidence-to-decision architecture for marine intelligence: specialized marine agents collaborate over heterogeneous spatiotemporal evidence, their assessments are validated and reconciled, uncertainty is surfaced, and the resulting decision is presented as a traceable reasoning graph.**

### In one sentence

> **ORCA does not invent marine data or AI; it aims to make existing marine intelligence computable as collaborative, evidence-grounded, uncertainty-aware decision reasoning.**

---

# 29. Evidence Base

The novelty assessment is based on the approved ORCA research material together with external primary/academic sources.

## Key sources

1. INCOIS – Potential Fishing Zone Advisory  
   https://incois.gov.in/MarineFisheries/PfzAdvisory

2. INCOIS – Marine Fishery Advisory  
   https://iioe-2.incois.gov.in/MarineFisheries/MarineFisheryAdvisory

3. NOAA – Integrated Ocean Observing System  
   https://oceanservice.noaa.gov/facts/ioos.html

4. NOAA IOOS  
   https://ioos.noaa.gov/

5. NOAA IOOS data access  
   https://ioos.noaa.gov/data/access-ioos-data/

6. Lin et al. (2026), "Building a marine reasoning large model: a method based on structured chain-of-thought fine-tuning and knowledge graph"  
   https://link.springer.com/article/10.1007/s44295-025-00091-2

7. Pantiukhin et al. (2025), "Accelerating earth science discovery via multi-agent LLM systems"  
   https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1674927/full

8. Ngisiange et al. (2016), "Multi-Agent Systems and Distributed Constraint Satisfaction for Decision Support in Marine Ecosystem Management"  
   https://www.researchgate.net/publication/308996424_Multi-Agent_Systems_and_Distributed_Constraint_Satisfaction_for_Decision_Support_in_Marine_Ecosystem_Management

9. NASA Earth Science and Technology Office – Coastal Zone Digital Twin  
   https://esto.nasa.gov/aist/coastal-zone-digital-twin-czdt-understanding-ocean-ecosystems-2/

10. Brown et al. (2026), "Automating Ecological and Fisheries Modelling With Agentic AI"  
    https://onlinelibrary.wiley.com/doi/epdf/10.1111/faf.70079

11. Spillias (2026), "A Prospectus on Generative Artificial Intelligence in Marine Ecosystem Modelling"  
    https://onlinelibrary.wiley.com/doi/full/10.1111/faf.70037

12. Millison et al. (2026), "State Machine Structured Agents for Physical Science Reasoning"  
    https://ojs.aaai.org/index.php/AAAI-SS/article/view/42579

13. Ishida (2026), "Integrating Large Language Models with Multi-Agent Deep Reinforcement Learning for Autonomous Marine Coordination"  
    https://www.jstage.jst.go.jp/article/fisheng/62/3/62_FE2525/_article/-char/en

14. Frontiers in Marine Science (2026), "From climate data to regulatory decisions: integrating climate AI into marine EIAs"  
    https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1870082/full

---

# 30. Governance Rule for Future Novelty Claims

Before adding any new ORCA novelty claim, the team should ask:

### Question 1
Does the capability already exist in marine science?

### Question 2
Does it already exist in general AI or agentic AI?

### Question 3
Does a current operational marine platform already provide it?

### Question 4
Does a recent paper demonstrate it?

### Question 5
Is ORCA actually introducing a new algorithm, architecture, benchmark, dataset, protocol or integration?

### Question 6
Can the claim be demonstrated experimentally?

If the answer to Questions 1–4 is "yes" and Questions 5–6 are "no", the feature should **not** be called novel.

---

# 31. Recommended Academic Position

ORCA should present itself as:

> **A novel system-level integration and reasoning architecture built from established marine science, Earth-observation, geospatial, AI and agentic-AI technologies.**

This is a stronger position than an exaggerated "first-ever" claim because it is:

- scientifically defensible,
- technically demonstrable,
- aligned with existing marine infrastructure,
- compatible with current AI research,
- easier to validate experimentally,
- less vulnerable to prior-art objections.

---

## Final Verdict

### ORCA's strongest legitimate contribution is:

**Evidence-grounded collaborative marine decision reasoning over heterogeneous spatiotemporal data.**

The novelty is **not** any one primitive.

It is the **combination, orchestration and traceability of those primitives around a marine evidence-to-decision workflow**.

That distinction should remain consistent across:

- the SIH pitch,
- architecture,
- prototype,
- research paper,
- presentation,
- README,
- technical documentation,
- evaluation plan,
- and future patent/research discussions.
