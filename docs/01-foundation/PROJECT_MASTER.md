# PROJECT_MASTER.md

# ORCA — Marine Ecosystems Reasoning with Collaborative Agents

**SIH Problem ID:** SIH26176
**Project Name:** ORCA — Marine Ecosystems Reasoning with Collaborative Agents
**Organization:** Indian Space Research Organisation (ISRO)
**Category:** Software
**Domain:** Marine Ecosystems · Earth Observation · Artificial Intelligence · Agentic AI · Decision Intelligence
**Document Status:** Project Master / Single Source of Truth
**Version:** 1.0
**Last Updated:** 30 August 2026

---

## 0. Document Purpose

This document is the **single source of truth (SSOT)** for the ORCA project.

All architecture, implementation, research, UI/UX, datasets, AI-agent design, demonstrations, technical documentation, and future development should remain consistent with this document.

### Source Classification

Every important project statement should be interpreted according to one of the following classifications:

| Classification            | Meaning                                                                                                   |
| ------------------------- | --------------------------------------------------------------------------------------------------------- |
| **[OFFICIAL]**            | Directly supported by the official SIH problem statement or official source                               |
| **[PROPOSED]**            | Architecture, feature, workflow, or technical approach proposed by our team                               |
| **[ASSUMPTION]**          | A working assumption that has not yet been formally validated                                             |
| **[VALIDATION REQUIRED]** | Information that must be confirmed through authoritative sources, domain experts, or project stakeholders |
| **[FUTURE]**              | Capability intended for a production-scale or post-prototype system                                       |

### Critical Rule

The project must **never represent a proposed architecture, assumed requirement, or future capability as an official ISRO requirement**.

---

# 1. Project Identity

## 1.1 Project

**ORCA — Marine Ecosystems Reasoning with Collaborative Agents**

ORCA is a proposed AI-based decision-intelligence platform for reasoning over heterogeneous marine ecosystem information using collaborative AI agents and evidence-grounded analysis.

## 1.2 SIH Identity

* **Problem ID:** SIH26176
* **Organization:** ISRO
* **Category:** Software
* **Primary Domain:** Marine Ecosystems
* **Technology Areas:** Earth Observation, AI, Agentic AI, Multi-Agent Reasoning, Decision Intelligence

## 1.3 Project Vision

> **Transform heterogeneous marine observations into evidence-grounded ecosystem intelligence and actionable decision support through collaborative AI agents.**

## 1.4 Project Mission

ORCA aims to demonstrate how multiple specialized AI agents can collaboratively analyze marine ecosystem observations, identify relevant environmental patterns, connect observations with contextual information, reason over evidence, and produce transparent decision-support outputs.

---

# 2. Official Problem Statement

## 2.1 Official Source

**[OFFICIAL]**

The exact wording of the official SIH26176 problem statement must be maintained in the project's official-source repository/documentation and should be reproduced verbatim when required for presentations or submissions.

**Official problem statement text:**

> **[INSERT VERIFIED OFFICIAL SIH26176 PROBLEM STATEMENT HERE]**

## 2.2 Source Integrity Rule

The team must not paraphrase the official problem statement and subsequently present the paraphrased version as the official wording.

Any interpretation made by the team belongs under:

* Problem Understanding
* Core Problem
* Proposed Solution
* Assumptions
* Open Questions

---

# 3. Problem Understanding

## 3.1 Interpretation

**[PROPOSED INTERPRETATION]**

Marine ecosystems are dynamic systems influenced by multiple interacting environmental variables. Relevant information can originate from different observation platforms, datasets, spatial scales, temporal scales, and scientific domains.

Examples may include:

* Earth observation imagery
* Oceanographic observations
* Sea-surface conditions
* Marine environmental variables
* Biological/ecological observations
* Geographic information
* Time-series observations
* Scientific literature and domain knowledge
* External contextual information

The challenge is not merely collecting these datasets.

The deeper challenge is to **connect heterogeneous evidence and reason over it in a scientifically meaningful way**.

## 3.2 Reasoning Challenge

Traditional data-analysis workflows frequently require domain experts to manually:

1. Identify relevant datasets.
2. Retrieve observations.
3. Compare temporal and spatial patterns.
4. Correlate environmental variables.
5. Examine ecological context.
6. Interpret anomalies.
7. Search supporting scientific information.
8. Form a conclusion.
9. Communicate the result to decision-makers.

ORCA proposes a collaborative-agent approach in which these analytical responsibilities can be decomposed among specialized agents.

---

# 4. Core Problem

## 4.1 Problem Definition

**[PROPOSED]**

The core problem is:

> **How can heterogeneous marine ecosystem observations be transformed into transparent, evidence-grounded reasoning and decision support through collaborative AI agents?**

## 4.2 Problem Dimensions

The system must address several dimensions:

### Data Heterogeneity

Marine information can differ in:

* Format
* Resolution
* Spatial coverage
* Temporal frequency
* Measurement methodology
* Reliability
* Semantic meaning

### Temporal Reasoning

Marine ecosystem conditions change over time.

Therefore, ORCA should distinguish between:

* Historical baseline
* Recent observations
* Current conditions
* Trends
* Anomalies
* Persistent changes

### Spatial Reasoning

Marine phenomena are spatially distributed.

The system should support reasoning involving:

* Geographic coordinates
* Regions
* Ocean zones
* Coastal areas
* Spatial boundaries
* Observation footprints

### Multi-variable Reasoning

A meaningful ecosystem interpretation may require considering several variables simultaneously rather than analyzing one variable in isolation.

### Evidence Traceability

AI-generated conclusions should be traceable to the observations, datasets, calculations, or references that support them.

---

# 5. Proposed Solution

## 5.1 Solution Overview

**[PROPOSED]**

ORCA is proposed as a **collaborative AI reasoning platform for marine ecosystem intelligence**.

The platform will coordinate multiple specialized AI agents that perform different analytical functions.

A high-level workflow is:

```text
Marine / Earth Observation Data
            │
            ▼
      Data Ingestion
            │
            ▼
     Data Preparation
            │
            ▼
     Observation Layer
            │
            ▼
      Agent Coordinator
            │
     ┌──────┼────────┐
     ▼      ▼        ▼
  Earth    Ocean   Ecology
Observation Agent   Agent
  Agent
     │      │        │
     └──────┼────────┘
            ▼
    Evidence / Reasoning
            │
            ▼
    Decision Intelligence
            │
            ▼
      Human Decision Maker
```

## 5.2 Design Principle

ORCA should not behave as a generic chatbot that produces unsupported answers.

Its primary principle is:

> **Observe → Analyze → Correlate → Reason → Verify → Explain**

---

# 6. Target Users / Stakeholders

**[PROPOSED / VALIDATION REQUIRED]**

Potential stakeholders include:

### Primary Users

* Marine ecosystem researchers
* Oceanographers
* Earth observation analysts
* Environmental scientists
* Researchers studying marine environmental changes

### Institutional Stakeholders

* Space and Earth observation organizations
* Marine research organizations
* Environmental monitoring agencies
* Government decision-makers
* Disaster/environmental response teams
* Academic and research institutions

### Secondary Users

* Policy analysts
* Conservation organizations
* Data scientists
* Scientific educators
* Environmental intelligence teams

**Note:** Specific institutional users and operational responsibilities must be validated before being presented as official requirements.

---

# 7. Geographic Scope

## 7.1 Prototype Scope

**[PROPOSED]**

The prototype should initially use a **controlled geographic study area** rather than attempting to model the entire global ocean.

The selected region should:

* Have adequate data availability.
* Demonstrate meaningful marine/ecological patterns.
* Be computationally manageable.
* Support repeatable experiments.
* Allow the team to demonstrate the complete ORCA reasoning workflow.

## 7.2 Production Scope

**[FUTURE]**

A production system could potentially support:

* Regional marine ecosystems
* Coastal regions
* Indian Ocean regions
* Larger oceanic regions
* Multi-region analysis
* Global-scale marine monitoring

These are future possibilities and are **not official SIH requirements unless explicitly stated by the official problem statement**.

---

# 8. Scientific Scope

## 8.1 Core Scientific Areas

**[PROPOSED]**

ORCA may reason over:

* Oceanographic conditions
* Marine environmental variables
* Earth observation observations
* Temporal trends
* Spatial patterns
* Environmental anomalies
* Ecosystem indicators
* Relationships between environmental variables
* Ecological context

## 8.2 Evidence Hierarchy

ORCA should prioritize evidence according to reliability and relevance.

A conceptual hierarchy is:

```text
Direct Observations
       ↓
Derived Measurements
       ↓
Validated Analytical Results
       ↓
Scientific Literature / Knowledge
       ↓
AI Interpretation
       ↓
Decision Recommendation
```

The system should clearly distinguish measured evidence from AI interpretation.

## 8.3 Scientific Caution

ORCA must not automatically interpret correlation as causation.

For example:

```text
Variable A changed
+
Variable B changed
≠
A caused B
```

The system should communicate uncertainty whenever causal attribution cannot be scientifically established.

---

# 9. Prototype Scope

## 9.1 Objective

**[PROPOSED]**

The prototype should demonstrate the complete reasoning loop rather than attempting to implement every possible marine intelligence capability.

## 9.2 Minimum Viable Prototype

The prototype should demonstrate:

1. Data ingestion.
2. Data preprocessing.
3. Geographic selection.
4. Temporal selection.
5. Observation retrieval.
6. Multi-variable analysis.
7. Specialized AI agents.
8. Agent collaboration.
9. Evidence collection.
10. Reasoning synthesis.
11. Confidence/uncertainty representation.
12. Explainable results.
13. Visualization.
14. Human-readable decision support.

## 9.3 Prototype Demonstration

A successful demonstration should allow a user to provide a marine/ecological question such as:

> "Analyze the environmental conditions in the selected marine region during the specified period and identify significant changes or anomalies."

ORCA should then:

```text
Understand Query
      ↓
Identify Required Evidence
      ↓
Retrieve Relevant Data
      ↓
Analyze Variables
      ↓
Compare Spatial/Temporal Patterns
      ↓
Collaborate Across Agents
      ↓
Cross-check Evidence
      ↓
Generate Explanation
      ↓
Present Decision Intelligence
```

## 9.4 Prototype Priority

The team should prioritize:

**Reasoning quality > agent count**

and

**Evidence traceability > flashy AI output**

and

**End-to-end functionality > excessive feature breadth**

---

# 10. Out-of-Scope Items

The following should not be treated as mandatory prototype requirements unless explicitly required by the official problem statement.

### 10.1 Global Real-Time Marine Monitoring

**[OUT OF PROTOTYPE SCOPE]**

Building a global, real-time marine monitoring infrastructure is unnecessary for the initial prototype.

### 10.2 Fully Autonomous Decision-Making

ORCA should not autonomously make high-impact environmental or governmental decisions.

It is a **decision-support system**, not a replacement for scientific or institutional decision-makers.

### 10.3 Unverified Causal Claims

The prototype must not present AI-generated causal relationships as scientific facts without appropriate evidence.

### 10.4 Complete Ocean Digital Twin

A full-scale digital twin of marine ecosystems is outside the initial prototype scope.

### 10.5 Unlimited Data Integration

The prototype should use a controlled and documented set of datasets.

### 10.6 Fully Autonomous Field Operations

ORCA will not directly control:

* Satellites
* Ships
* Drones
* Autonomous underwater vehicles
* Industrial control systems

unless explicitly introduced as a future integration.

---

# 11. Key Use Cases

## Use Case 1 — Marine Environmental Analysis

**Goal:** Understand environmental conditions within a selected marine region.

```text
User selects region + time period
        ↓
ORCA retrieves observations
        ↓
Agents analyze variables
        ↓
System identifies patterns
        ↓
Evidence-grounded summary
```

---

## Use Case 2 — Anomaly Detection

**Goal:** Identify unusual environmental conditions.

```text
Historical baseline
       +
Recent observation
       ↓
Anomaly analysis
       ↓
Spatial/temporal validation
       ↓
Evidence-backed explanation
```

---

## Use Case 3 — Multi-variable Ecosystem Reasoning

**Goal:** Analyze relationships between multiple environmental indicators.

The system can compare multiple variables and determine whether their changes are:

* Temporally aligned
* Spatially aligned
* Independent
* Potentially related
* Insufficiently supported

---

## Use Case 4 — Scientific Question Answering

A researcher asks:

> "What environmental changes occurred in this region during this period?"

ORCA identifies relevant evidence and produces a structured explanation.

---

## Use Case 5 — Evidence-backed Decision Support

The system converts analytical results into:

* Key observations
* Detected patterns
* Supporting evidence
* Confidence
* Uncertainty
* Possible implications
* Recommended next analytical steps

Recommendations should remain appropriately qualified.

---

# 12. Core ORCA Workflow

## 12.1 End-to-End Workflow

```text
                    ┌───────────────────────┐
                    │      USER QUERY       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  QUERY UNDERSTANDING  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ EVIDENCE REQUIREMENTS │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   DATA ORCHESTRATION  │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
       Earth Observation    Ocean Analysis    Ecology Analysis
            Agent               Agent              Agent
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼
                    ┌───────────────────────┐
                    │ EVIDENCE SYNTHESIS    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ CROSS-AGENT VALIDATION │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ REASONING ENGINE      │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ DECISION INTELLIGENCE │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ HUMAN INTERPRETATION  │
                    └───────────────────────┘
```

## 12.2 Reasoning Loop

ORCA's conceptual reasoning loop:

```text
OBSERVE
   ↓
UNDERSTAND
   ↓
ANALYZE
   ↓
CORRELATE
   ↓
CHALLENGE
   ↓
VERIFY
   ↓
SYNTHESIZE
   ↓
EXPLAIN
```

The **CHALLENGE** stage is important: one agent or validation layer should be capable of questioning unsupported conclusions from another agent.

---

# 13. Proposed AI Agents

All agents below are **[PROPOSED]** and must not be represented as official ISRO-required components.

## 13.1 Orchestrator Agent

### Responsibility

* Understand the user request.
* Decompose the problem.
* Determine which agents are required.
* Coordinate execution.
* Maintain workflow state.
* Combine intermediate results.

---

## 13.2 Earth Observation Agent

### Responsibility

Analyze relevant Earth observation information.

Potential functions:

* Identify relevant imagery/products.
* Extract observations.
* Perform spatial comparisons.
* Analyze temporal changes.
* Detect observable patterns.

---

## 13.3 Ocean Analysis Agent

### Responsibility

Analyze oceanographic/environmental variables.

Potential functions:

* Time-series analysis.
* Spatial analysis.
* Trend detection.
* Baseline comparison.
* Anomaly identification.

---

## 13.4 Ecosystem Reasoning Agent

### Responsibility

Connect environmental observations with ecosystem context.

Potential functions:

* Interpret environmental patterns.
* Identify potentially relevant ecological relationships.
* Compare multiple variables.
* Identify evidence gaps.

---

## 13.5 Data Quality Agent

### Responsibility

Evaluate the quality and validity of evidence.

Potential checks:

* Missing values
* Temporal mismatch
* Spatial mismatch
* Outliers
* Resolution mismatch
* Dataset coverage
* Data freshness
* Source reliability

---

## 13.6 Evidence Agent

### Responsibility

Maintain evidence provenance.

Each major conclusion should ideally reference:

```text
Claim
 ↓
Supporting Observation
 ↓
Dataset
 ↓
Processing / Calculation
 ↓
Evidence Strength
```

---

## 13.7 Critic / Validation Agent

### Responsibility

Challenge intermediate conclusions.

It should ask:

* Is the evidence sufficient?
* Are variables temporally aligned?
* Are spatial regions comparable?
* Is this correlation or causation?
* Could another explanation exist?
* Is the confidence appropriate?

---

## 13.8 Synthesis Agent

### Responsibility

Convert validated outputs into a coherent final response.

Output should contain:

* Question
* Observations
* Analysis
* Evidence
* Reasoning
* Confidence
* Uncertainty
* Implications
* Recommended next steps

---

# 14. Data Sources

## 14.1 Data Philosophy

**[PROPOSED]**

ORCA should prioritize authoritative, documented, scientifically appropriate datasets.

The prototype should avoid uncontrolled scraping and undocumented datasets wherever possible.

## 14.2 Potential Data Categories

Potential categories include:

### Earth Observation

* Satellite-derived marine/environmental products
* Ocean colour observations
* Sea-surface observations
* Remote-sensing products

### Oceanographic Data

* Temperature
* Salinity
* Currents
* Sea-level-related variables
* Other available oceanographic measurements

### Ecological Data

* Marine ecosystem indicators
* Species/biological observations
* Biodiversity-related datasets

### Contextual Data

* Geographic information
* Scientific literature
* Environmental records
* Historical observations

## 14.3 Source Validation

Every dataset used in the prototype should have documented:

* Provider
* Dataset name
* Access method
* Spatial resolution
* Temporal resolution
* Coverage
* Units
* Known limitations
* Licensing/usage restrictions

## 14.4 Data Provenance

The system should preserve:

```text
Source
 → Dataset
 → Query
 → Transformation
 → Analysis
 → Result
```

This is essential for evidence-grounded reasoning.

---

# 15. Technology Stack

Technology choices are **[PROPOSED]** and may change based on implementation constraints.

## 15.1 Frontend

Potential technologies:

* Next.js
* React
* TypeScript
* Modern component/UI framework
* Interactive geospatial visualization

## 15.2 Backend

Potential technologies:

* Python and/or TypeScript
* API-based service architecture
* Data-processing services
* Agent orchestration services

## 15.3 AI Layer

Potential components:

* Large Language Models
* Tool-using AI agents
* Agent orchestration framework
* Retrieval-Augmented Generation
* Scientific reasoning workflows
* Structured-output generation

The specific model/provider should remain implementation-dependent.

## 15.4 Data Layer

Potential components:

* PostgreSQL
* PostGIS
* Object storage
* Time-series storage
* Vector search where scientifically justified

## 15.5 Data Processing

Potential technologies:

* Python
* NumPy
* Pandas
* Xarray
* Geospatial processing libraries
* Scientific computing libraries

## 15.6 Visualization

Potential capabilities:

* Interactive maps
* Time-series charts
* Spatial overlays
* Anomaly maps
* Evidence panels
* Agent reasoning timeline

## 15.7 Deployment

Potential technologies:

* Containerized services
* Cloud deployment
* CI/CD
* API gateway
* Observability infrastructure

Exact infrastructure should be decided according to prototype requirements rather than prematurely locking the architecture.

---

# 16. Core Innovation

## 16.1 Proposed Innovation

ORCA's central innovation is **not simply using AI for marine data**.

The proposed innovation is the combination of:

> **Heterogeneous marine evidence + specialized collaborative agents + evidence-grounded reasoning + validation + decision intelligence**

## 16.2 Reasoning-Centric Architecture

Instead of:

```text
Data → ML Model → Prediction
```

ORCA proposes:

```text
Question
   ↓
Evidence Discovery
   ↓
Specialized Analysis
   ↓
Cross-Agent Reasoning
   ↓
Evidence Validation
   ↓
Uncertainty Assessment
   ↓
Explainable Decision Intelligence
```

## 16.3 Evidence as a First-Class Object

Evidence should not be treated as an invisible backend detail.

The system should expose:

* Where evidence came from.
* What was observed.
* How it was processed.
* Which agent used it.
* How it supports the conclusion.
* What uncertainty remains.

---

# 17. Major Differentiators

These are **[PROPOSED DIFFERENTIATORS]**, not claims of uniqueness in the global research landscape.

## 17.1 Collaborative Specialized Agents

Different analytical responsibilities are distributed across specialized agents rather than relying on a single general-purpose reasoning component.

## 17.2 Evidence-Grounded Reasoning

AI conclusions should be grounded in observable data and traceable evidence.

## 17.3 Cross-Agent Validation

The system can introduce an explicit validation/critic stage to challenge unsupported conclusions.

## 17.4 Spatial + Temporal + Semantic Reasoning

ORCA is intended to reason across:

* Geography
* Time
* Environmental variables
* Ecological context
* Scientific evidence

## 17.5 Uncertainty-Aware Output

The system should communicate uncertainty rather than presenting every generated conclusion as fact.

## 17.6 Human-in-the-Loop Decision Intelligence

The system supports experts rather than replacing them.

## 17.7 Reproducible Analytical Chain

The reasoning process should ideally be reproducible from:

```text
Input
 → Data
 → Processing
 → Evidence
 → Reasoning
 → Output
```

---

# 18. Expected Outputs

## 18.1 Primary Output

A structured marine ecosystem intelligence report.

## 18.2 Output Components

### Executive Summary

A concise answer to the user's question.

### Key Observations

What the data directly indicates.

### Detected Patterns

Observed spatial or temporal patterns.

### Evidence

Datasets, measurements, calculations, and supporting sources.

### Agent Analysis

Summary of relevant agent findings.

### Cross-Agent Validation

Areas of agreement and disagreement.

### Confidence

A qualitative or quantitative confidence representation where appropriate.

### Uncertainty

Known limitations and evidence gaps.

### Implications

Potential scientific/ecological significance, carefully qualified.

### Recommended Next Steps

Suggested further investigation or validation.

---

# 19. Prototype Success Criteria

The prototype should be evaluated against measurable criteria.

## 19.1 Functional Criteria

The prototype should demonstrate:

* Successful data ingestion.
* Successful query processing.
* Successful agent coordination.
* Successful multi-variable analysis.
* Successful evidence retrieval.
* Successful result synthesis.
* Interactive visualization.
* End-to-end execution.

## 19.2 Evidence Criteria

For important conclusions:

* Supporting evidence should be identifiable.
* Source information should be available.
* Calculations should be reproducible where practical.
* Unsupported claims should be flagged.
* Uncertainty should be communicated.

## 19.3 Reasoning Criteria

The system should demonstrate:

* Multi-step reasoning.
* Agent specialization.
* Agent collaboration.
* Cross-checking.
* Contradiction handling.
* Evidence prioritization.

## 19.4 User Experience Criteria

A user should be able to:

1. Define a question.
2. Select a region/time period.
3. Start analysis.
4. Observe system progress.
5. Inspect evidence.
6. Understand the final conclusion.

## 19.5 Demonstration Criteria

The demo should clearly answer:

> **What question did ORCA receive?**

> **What evidence did it use?**

> **What did each agent discover?**

> **How were the findings validated?**

> **Why did ORCA produce the final conclusion?**

---

# 20. Major Constraints

## 20.1 Data Constraints

* Dataset availability.
* API limitations.
* Historical coverage.
* Spatial resolution.
* Temporal resolution.
* Missing observations.
* Different measurement standards.

## 20.2 Computational Constraints

* Limited prototype infrastructure.
* Model inference cost.
* Large geospatial datasets.
* Processing latency.
* Storage requirements.

## 20.3 Scientific Constraints

* Correlation does not establish causation.
* Observational data may contain uncertainty.
* Different datasets may have incompatible resolutions.
* Ecological systems are complex.
* AI interpretation can introduce errors.

## 20.4 AI Constraints

* Hallucination.
* Incorrect reasoning.
* Tool-use errors.
* Agent coordination failures.
* Overconfident conclusions.
* Context limitations.

## 20.5 Prototype Time Constraints

The team should prioritize the smallest system that convincingly demonstrates:

> **Evidence → Collaboration → Reasoning → Decision Intelligence**

---

# 21. Known Assumptions

The following are working assumptions and **must not be presented as official requirements**.

## A1 — Data Availability

**[ASSUMPTION]**

Relevant marine/Earth observation datasets can be accessed for the selected prototype region.

**Validation:** Dataset/API verification required.

---

## A2 — Multi-Agent Architecture

**[ASSUMPTION / PROPOSED]**

A collaborative-agent architecture can provide meaningful value compared with a single-agent workflow.

**Validation:** Prototype evaluation required.

---

## A3 — Evidence Traceability

**[ASSUMPTION]**

A structured evidence/provenance layer can be integrated into the prototype without making the system impractically complex.

**Validation:** Implementation testing required.

---

## A4 — Domain Interpretation

**[ASSUMPTION]**

Available environmental observations can support meaningful ecosystem-level analytical questions within the selected use cases.

**Validation:** Domain expert review required.

---

## A5 — Prototype Geographic Area

**[ASSUMPTION]**

A smaller representative geographic area will be sufficient to demonstrate the ORCA workflow.

**Validation:** Dataset and demonstration planning required.

---

# 22. Risks

## R1 — Hallucinated Scientific Conclusions

**Risk:** AI generates unsupported scientific claims.

**Mitigation:**

* Evidence grounding.
* Structured outputs.
* Citation/provenance.
* Critic agent.
* Confidence reporting.
* Human review.

---

## R2 — Data Quality Problems

**Risk:** Poor-quality or incomplete observations lead to incorrect conclusions.

**Mitigation:**

* Data Quality Agent.
* Dataset metadata.
* Missing-data detection.
* Quality flags.

---

## R3 — Spatial/Temporal Misalignment

**Risk:** Comparing observations from different locations or time periods incorrectly.

**Mitigation:**

* Explicit spatial/temporal alignment.
* Validation checks.
* Metadata-aware processing.

---

## R4 — Correlation Presented as Causation

**Risk:** The system incorrectly states that one environmental variable caused another.

**Mitigation:**

* Scientific reasoning constraints.
* Causal-language restrictions.
* Evidence qualification.

---

## R5 — Agent Agreement Without Correctness

**Risk:** Multiple agents independently produce the same incorrect interpretation.

**Mitigation:**

* Evidence-based validation.
* Independent analytical methods.
* Data-level verification.
* External scientific references where appropriate.

---

## R6 — Excessive Prototype Complexity

**Risk:** Too many agents and integrations reduce reliability.

**Mitigation:**

Start with a small number of high-value agents and expand only when justified.

---

## R7 — API/Data Availability

**Risk:** External data services become unavailable or impose restrictions.

**Mitigation:**

* Cache prototype datasets.
* Maintain fallback datasets.
* Document data dependencies.

---

## R8 — LLM Cost/Latency

**Risk:** Multi-agent inference becomes expensive or slow.

**Mitigation:**

* Selective agent activation.
* Structured workflows.
* Caching.
* Smaller models for deterministic subtasks.
* Minimize unnecessary agent calls.

---

# 23. Future Production Scope

All items in this section are **[FUTURE]** and are not current prototype commitments.

## 23.1 Expanded Data Ecosystem

Potential integration of:

* Additional satellite products.
* Additional oceanographic datasets.
* Ecological observations.
* Scientific literature.
* Historical records.
* Additional geospatial datasets.

---

## 23.2 Advanced Agent Ecosystem

Potential future agents:

* Climate Analysis Agent
* Biodiversity Agent
* Fisheries Agent
* Pollution Analysis Agent
* Climate Impact Agent
* Ocean Circulation Agent
* Remote Sensing Specialist Agent
* Scientific Literature Agent
* Causal Inference Agent
* Uncertainty Quantification Agent

Agents should only be added where they provide measurable analytical value.

---

## 23.3 Advanced Reasoning

Potential capabilities:

* Longitudinal ecosystem reasoning.
* Causal inference.
* Counterfactual analysis.
* Scenario analysis.
* Predictive modeling.
* Probabilistic reasoning.
* Scientific knowledge graphs.

---

## 23.4 Production-Grade Data Infrastructure

Potential future infrastructure:

```text
Satellite / Sensor Data
        ↓
Streaming / Batch Ingestion
        ↓
Data Lake
        ↓
Geospatial + Time-Series Layer
        ↓
Feature / Knowledge Layer
        ↓
Agentic Reasoning Platform
        ↓
Decision Intelligence
```

---

## 23.5 Operational Integration

Potential future integration with authorized institutional systems could include:

* Monitoring dashboards.
* Scientific analysis platforms.
* Alerting systems.
* Research workflows.
* Decision-support systems.

Any operational integration would require appropriate institutional authorization, validation, security, and governance.

---

# 24. Non-Negotiable Design Principles

These principles apply to the entire ORCA implementation.

## P1 — Evidence Before Explanation

The system should seek relevant evidence before generating conclusions.

## P2 — Observation ≠ Interpretation

Clearly distinguish:

```text
Observed
Derived
Inferred
Hypothesized
Recommended
```

## P3 — Correlation ≠ Causation

Never make unsupported causal claims.

## P4 — Traceability

Important conclusions should be traceable to evidence.

## P5 — Uncertainty Is a Feature

The system should explicitly communicate uncertainty where evidence is insufficient.

## P6 — Human Oversight

ORCA provides decision intelligence; it does not replace qualified scientific or institutional judgment.

## P7 — Modular Architecture

Agents and services should be replaceable without redesigning the entire system.

## P8 — Implementation Independence

The conceptual ORCA architecture should remain valid even if the specific programming language, framework, database, model provider, or deployment platform changes.

---

# 25. Conceptual Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                         USER / EXPERT                         │
└─────────────────────────────┬─────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                    ORCA INTERFACE LAYER                       │
│          Query · Map · Timeline · Evidence · Reports          │
└─────────────────────────────┬─────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                     ORCHESTRATION LAYER                       │
│              Planning · Routing · State · Coordination         │
└───────────────┬───────────────┬───────────────┬───────────────┘
                │               │               │
                ▼               ▼               ▼
        ┌────────────┐  ┌────────────┐  ┌────────────┐
        │ EO Agent   │  │Ocean Agent │  │Ecology     │
        │            │  │            │  │Agent       │
        └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                   ┌─────────────────────┐
                   │ Evidence Layer      │
                   │ Provenance · QA     │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Validation / Critic │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Reasoning /         │
                   │ Synthesis Layer     │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Decision Intelligence│
                   └──────────┬──────────┘
                              │
                              ▼
                         HUMAN USER
```

---

# 26. ORCA Output Contract

Every major analytical response should conceptually follow this structure:

```text
QUESTION
    ↓
SCOPE
    ↓
DATA USED
    ↓
OBSERVATIONS
    ↓
ANALYSIS
    ↓
CROSS-AGENT FINDINGS
    ↓
EVIDENCE
    ↓
VALIDATION
    ↓
CONCLUSION
    ↓
CONFIDENCE
    ↓
UNCERTAINTY
    ↓
POSSIBLE IMPLICATIONS
    ↓
RECOMMENDED NEXT STEP
```

This output contract should guide backend APIs, agent prompts, UI design, reports, and demonstrations.

---

# 27. Repository Governance

The repository should maintain a clear distinction between project truth and implementation details.

Recommended structure:

```text
/
├── PROJECT_MASTER.md
├── README.md
│
├── docs/
│   ├── official/
│   ├── research/
│   ├── architecture/
│   ├── datasets/
│   ├── experiments/
│   └── decisions/
│
├── src/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
│
├── agents/
│
├── experiments/
│
├── tests/
│
└── config/
```

## Governance Rule

If another document conflicts with `PROJECT_MASTER.md`, the team must:

1. Identify the conflict.
2. Determine whether the master document or implementation is outdated.
3. Validate the information.
4. Update the appropriate document.
5. Record significant architectural decisions.

---

# 28. Approved Decisions

This section records decisions that the team has explicitly approved.

### D1 — Project Identity

**Approved:** ORCA — Marine Ecosystems Reasoning with Collaborative Agents.

### D2 — Problem

**Approved:** SIH26176 is the project reference.

### D3 — Core Direction

**Approved:** The project will focus on marine ecosystem reasoning using collaborative AI agents.

### D4 — Evidence Grounding

**Approved:** Evidence-grounded reasoning is a core design principle.

### D5 — Human-in-the-Loop

**Approved:** ORCA is a decision-support platform rather than an autonomous decision-maker.

### D6 — Prototype Philosophy

**Approved:** Prioritize a convincing end-to-end prototype over excessive feature breadth.

### D7 — Scientific Integrity

**Approved:** Unsupported causal claims and fabricated evidence are prohibited.

### D8 — Official Requirement Handling

**Approved:** Proposed architecture and assumptions must never be presented as official ISRO requirements without verification.

---

# 29. Open Questions

These questions must be resolved before the architecture and prototype are considered fully finalized.

### Q1

What is the exact verified official wording of SIH26176?

### Q2

What specific marine ecosystem reasoning capabilities are explicitly required by the official problem statement?

### Q3

What datasets are officially recommended, required, or made available?

### Q4

Are there specific ISRO data platforms/APIs that should be prioritized?

### Q5

What geographic region should be selected for the prototype?

### Q6

What scientific use case provides the strongest demonstration of ORCA's reasoning capability?

### Q7

What environmental variables should be included in the MVP?

### Q8

What constitutes an acceptable confidence/evidence model for the prototype?

### Q9

What level of scientific validation is expected for the final SIH demonstration?

### Q10

Which AI-agent framework, model provider, and infrastructure should be selected after evaluating prototype requirements?

### Q11

What evaluation dataset or ground truth can be used to measure reasoning quality?

### Q12

What domain experts or authoritative organizations can validate the scientific assumptions?

---

# 30. Assumptions Requiring Validation

The following assumptions must be explicitly validated before being treated as project facts.

| ID | Assumption                                                   | Validation Method        | Status  |
| -- | ------------------------------------------------------------ | ------------------------ | ------- |
| A1 | Required marine datasets are accessible                      | Dataset/API verification | Pending |
| A2 | Selected region has sufficient data coverage                 | Data analysis            | Pending |
| A3 | Multi-agent reasoning provides measurable benefit            | Comparative experiment   | Pending |
| A4 | Evidence provenance can be maintained end-to-end             | Prototype implementation | Pending |
| A5 | Selected variables support meaningful ecosystem analysis     | Domain expert review     | Pending |
| A6 | Prototype latency is acceptable                              | Performance testing      | Pending |
| A7 | AI model reasoning is sufficiently reliable with grounding   | Evaluation               | Pending |
| A8 | Selected use case can be demonstrated within SIH constraints | Internal review          | Pending |

---

# 31. References

## 31.1 Official References

### SIH Problem Statement

**[OFFICIAL — REQUIRED]**

Add the verified official source for:

> SIH26176 — ORCA — Marine Ecosystems Reasoning with Collaborative Agents

**Reference:**
`[INSERT OFFICIAL SIH SOURCE URL / DOCUMENT HERE]`

---

## 31.2 ISRO / Official Data Sources

Use authoritative ISRO sources where applicable.

**Reference:**
`[INSERT VERIFIED ISRO SOURCE]`

---

## 31.3 Dataset References

Every dataset used in the project must be recorded here.

Recommended format:

```text
Dataset:
Provider:
URL:
Version:
Spatial Resolution:
Temporal Resolution:
Coverage:
Access Date:
License:
Known Limitations:
```

---

## 31.4 Scientific Literature

Research papers should be added only after verification.

Recommended format:

```text
Authors:
Title:
Journal / Conference:
Year:
DOI / Official URL:
How ORCA Uses This Research:
```

---

# 32. Final Source-of-Truth Rule

Before implementing or modifying any ORCA component, the team should answer:

> **Is this an official requirement, a proposed design decision, an assumption, or a future idea?**

If the answer is unclear, it must **not** be presented as an official requirement.

The ORCA project should continuously optimize for:

```text
SCIENTIFIC VALIDITY
        +
EVIDENCE TRACEABILITY
        +
COLLABORATIVE REASONING
        +
EXPLAINABILITY
        +
PRACTICAL DECISION SUPPORT
        +
DEMONSTRABLE PROTOTYPE VALUE
```

## ORCA Guiding Principle

> **Observe deeply. Reason collaboratively. Validate with evidence. Explain transparently.**

---
