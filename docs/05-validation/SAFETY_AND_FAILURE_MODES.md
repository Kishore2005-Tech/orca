# SAFETY_AND_FAILURE_MODES.md

# ORCA — Safety and Failure Modes

**Project:** SIH26176 – ORCA
**Full Name:** Marine Ecosystems Reasoning with Collaborative Agents
**Organization:** ISRO
**Category:** Software
**Domain:** Marine Ecosystems + Earth Observation + AI + Agentic AI + Decision Intelligence

---

## 1. Purpose

ORCA is a marine decision-support and scientific reasoning system that integrates heterogeneous Earth Observation, oceanographic, meteorological, and contextual data to generate evidence-grounded insights.

Because ORCA may be used to understand:

* Potential Fishing Zones (PFZ)
* sea and weather conditions
* oceanographic conditions
* marine ecosystem indicators
* cyclone and high-wave conditions
* fishing-related environmental intelligence
* spatiotemporal marine patterns
* scenario-based decision support

a failure can have consequences beyond ordinary software malfunction.

Therefore, ORCA must be designed around the principle:

> **When evidence is insufficient, ORCA must reduce the scope of its answer rather than increase the certainty of its claim.**

ORCA must never convert missing, stale, contradictory, or low-quality evidence into a confident recommendation.

---

# 2. Core Safety Principles

## 2.1 Evidence Before Reasoning

ORCA must establish that relevant evidence exists before attempting scientific reasoning.

The system should evaluate:

1. Dataset identity
2. Source authority
3. Spatial coverage
4. Temporal coverage
5. Timestamp
6. Data freshness
7. Data quality
8. Completeness
9. Cross-source consistency
10. Scientific relevance

Only then should reasoning agents operate.

---

## 2.2 Uncertainty Must Propagate

If input data is uncertain, downstream conclusions must not appear more certain than their evidence.

For example:

```text
Uncertain SST
      ↓
Uncertain thermal-front detection
      ↓
Uncertain ecological interpretation
      ↓
Low-confidence decision support
```

The system must not produce:

```text
Low-quality data → confident recommendation
```

---

## 2.3 No Fabricated Evidence

ORCA must never:

* invent a dataset
* invent a measurement
* invent a timestamp
* invent a location
* invent a scientific source
* invent an API response
* invent an agent result
* invent a confidence score
* claim that a source was consulted when it was not
* fabricate missing observations

---

## 2.4 No False Safety Guarantees

ORCA must never state or imply:

* "The sea is safe."
* "It is completely safe to fish."
* "There is no cyclone risk."
* "You are guaranteed to be safe."
* "The system guarantees safe navigation."
* "No dangerous conditions exist."

Instead, ORCA should communicate evidence and uncertainty.

Example:

> "Current available data does not indicate elevated wave conditions at the selected location, but ORCA cannot guarantee sea safety. Conditions can change rapidly; consult authoritative marine and weather warnings before making operational decisions."

---

# 3. Failure Severity Classification

| Severity | Meaning       | Example                                  |
| -------- | ------------- | ---------------------------------------- |
| S0       | Informational | Minor metadata issue                     |
| S1       | Low           | Non-critical visualization issue         |
| S2       | Moderate      | Partial data degradation                 |
| S3       | High          | Incorrect scientific interpretation      |
| S4       | Critical      | Potentially unsafe marine recommendation |

Any failure capable of producing a materially unsafe recommendation must be treated as **S4**.

---

# 4. Failure Mode Matrix

## 4.1 Wrong Dataset

### Failure

ORCA retrieves or processes a dataset that is not appropriate for the requested scientific question.

### Cause

Possible causes:

* incorrect dataset mapping
* semantic retrieval error
* incorrect API endpoint
* dataset version mismatch
* metadata corruption
* agent selecting an inappropriate source
* ambiguous user query

### Detection

Validate:

* dataset identifier
* variable name
* units
* spatial resolution
* temporal resolution
* geographic coverage
* dataset description
* source organization
* expected variable availability

The system should perform schema validation before reasoning.

### Severity

**S3 — High**

May become **S4** if the incorrect dataset influences an operational safety recommendation.

### System Response

* stop downstream reasoning
* mark evidence as invalid
* prevent recommendation generation
* attempt retrieval from an approved alternative source
* recalculate evidence quality

### Fallback

Use a validated alternative dataset.

If no suitable dataset exists:

> **Insufficient evidence**

### User Communication

> "The available dataset is not suitable for answering this question reliably. ORCA cannot provide a scientifically supported conclusion from this data."

### Logging

Record:

* requested variable
* selected dataset
* dataset identifier
* source
* validation result
* reason for rejection
* fallback dataset
* affected agents
* final system state

---

# 4.2 Stale Dataset

### Failure

ORCA uses data that is older than the acceptable freshness window for the requested task.

### Cause

* delayed provider update
* API synchronization failure
* caching
* ingestion failure
* outdated local copy
* provider outage

### Detection

Compare:

```text
current_time - observation_time
```

against the variable-specific freshness threshold.

Freshness requirements must be defined per variable and use case rather than using one universal threshold.

### Severity

**S3–S4**

### System Response

* calculate data age
* downgrade evidence quality
* prevent stale data from being represented as current
* search for newer observations
* distinguish observation time from retrieval time

### Fallback

Use:

1. newer validated source
2. secondary authoritative source
3. historical analysis explicitly labeled as historical

If current conditions cannot be established:

> **Insufficient evidence**

### User Communication

> "The latest available observation is older than the required freshness window. ORCA cannot reliably describe current conditions."

### Logging

Store:

* observation timestamp
* retrieval timestamp
* data age
* freshness threshold
* source
* freshness status
* fallback attempt

---

# 4.3 Missing Data

### Failure

Required observations are unavailable for the requested location or time.

### Cause

* satellite coverage gap
* cloud contamination
* sensor failure
* API outage
* geographic coverage limitation
* missing timestamp
* incomplete ingestion
* quality-control rejection

### Detection

Check for:

* null values
* missing variables
* missing spatial cells
* missing time steps
* invalid quality flags
* incomplete records

### Severity

**S2–S4**, depending on downstream impact.

### System Response

ORCA must explicitly identify which evidence is missing.

The reasoning engine must not silently substitute missing values with invented values.

### Fallback

Possible fallbacks:

* alternate validated dataset
* interpolation for non-safety analytical use cases
* historical context
* broader spatial analysis

Interpolation must not silently replace observations in safety-critical decisions.

### User Communication

> "Required data for this location/time is unavailable. ORCA cannot establish the requested condition with sufficient evidence."

### Logging

Record:

* missing variable
* location
* timestamp
* source
* missing-data reason
* fallback method
* whether interpolation was used

---

# 4.4 Conflicting Data

### Failure

Two or more credible sources provide materially different observations or forecasts.

### Cause

* different spatial resolutions
* different temporal resolutions
* different instruments
* model-vs-observation differences
* asynchronous observations
* calibration differences
* processing differences
* genuine environmental variability

### Detection

Perform:

* temporal alignment
* spatial alignment
* unit normalization
* quality assessment
* source comparison
* discrepancy threshold analysis

### Severity

**S3–S4**

### System Response

ORCA must not arbitrarily select the result that supports a preferred conclusion.

The system should:

1. identify the conflict
2. preserve both observations
3. assess source reliability
4. quantify disagreement where possible
5. ask additional agents for independent assessment
6. reduce confidence
7. determine whether the disagreement affects the requested decision

### Fallback

If one source has demonstrably superior validity:

Use it while explicitly reporting the conflict.

If conflict cannot be resolved:

> **Insufficient evidence**

### User Communication

> "Available sources disagree on the relevant marine condition. ORCA cannot resolve the discrepancy with sufficient confidence."

### Logging

Record:

* sources
* values
* timestamps
* spatial areas
* discrepancy magnitude
* quality flags
* conflict-resolution process
* final confidence

---

# 4.5 Wrong Location

### Failure

Data or reasoning is associated with the wrong geographic location.

### Cause

* coordinate parsing error
* latitude/longitude reversal
* incorrect coordinate reference system
* geocoding error
* user entering ambiguous location
* agent misinterpreting place name
* bounding-box error

### Detection

Validate:

* latitude range
* longitude range
* coordinate reference system
* location identity
* expected ocean/land classification
* distance from requested coordinates
* spatial intersection

### Severity

**S4 — Critical**

A geographically incorrect marine recommendation can be unsafe.

### System Response

Immediately halt location-dependent reasoning.

Revalidate coordinates before proceeding.

### Fallback

Ask the user to confirm the location if ambiguity remains.

If location cannot be established:

> **Insufficient evidence**

### User Communication

> "ORCA could not reliably validate the selected location. Please verify the coordinates or location before continuing."

### Logging

Record:

* original location
* normalized location
* coordinate system
* validation result
* detected discrepancy
* corrected location if applicable

---

# 4.6 Wrong Timestamp

### Failure

ORCA uses observations or forecasts associated with an incorrect time.

### Cause

* timezone conversion
* UTC/local-time confusion
* timestamp parsing
* forecast initialization mismatch
* stale cache
* incorrect temporal alignment

### Detection

Validate:

* UTC timestamp
* local timestamp
* forecast issue time
* forecast valid time
* observation time
* ingestion time

### Severity

**S3–S4**

### System Response

* reject ambiguous timestamps
* normalize all internal timestamps to UTC
* display user-facing local time where appropriate
* distinguish observation time from forecast valid time

### Fallback

Use only temporally validated evidence.

If temporal alignment cannot be established:

> **Insufficient evidence**

### User Communication

> "The available information could not be reliably aligned with the requested time."

### Logging

Store all original and normalized timestamps.

---

# 4.7 LLM Hallucination

### Failure

An LLM generates unsupported facts, observations, explanations, sources, or recommendations.

### Cause

* unconstrained generation
* insufficient retrieval
* ambiguous prompt
* missing evidence
* model overconfidence
* incorrect context construction

### Detection

Every factual claim should be checked against retrieved evidence where feasible.

Use:

* evidence-to-claim matching
* citation validation
* source existence validation
* structured output schemas
* numerical consistency checks
* prohibited unsupported-claim detection

### Severity

**S4 — Critical**

### System Response

* reject unsupported claim
* regenerate using evidence-only context
* reduce confidence
* require source attribution
* prevent unsupported recommendation

### Fallback

Return the available evidence without generating an unsupported interpretation.

> **Insufficient evidence**

### User Communication

> "ORCA does not have sufficient evidence to support that conclusion."

### Logging

Record:

* model
* prompt/context identifier
* retrieved evidence
* generated claim
* validation result
* rejected content
* final response

---

# 4.8 Incorrect Scientific Inference

### Failure

The underlying observations are valid, but ORCA derives an incorrect scientific conclusion.

### Cause

Examples:

* confusing correlation with causation
* incorrect oceanographic interpretation
* inappropriate ecological assumptions
* incorrect variable relationships
* invalid threshold
* extrapolation outside model validity
* agent reasoning error

### Detection

Use:

* domain rules
* scientific constraints
* independent reasoning agents
* known relationships
* unit checks
* range checks
* expert-authored validation rules
* cross-agent disagreement detection

### Severity

**S3–S4**

### System Response

Do not allow a single unconstrained LLM inference to become an operational recommendation.

Require evidence-backed reasoning.

### Fallback

Present observations separately from interpretation.

Example:

> "Observed SST is X°C and chlorophyll-a is Y. The available evidence does not establish that this combination indicates a productive fishing zone."

### User Communication

> "The observed variables are available, but ORCA cannot establish the requested scientific relationship with sufficient confidence."

### Logging

Record:

* input variables
* scientific rules
* agent reasoning outputs
* disagreement
* validation results
* final conclusion

---

# 4.9 Agent Failure

### Failure

One or more specialized ORCA agents fail, return malformed output, disagree unexpectedly, or become unavailable.

### Cause

* model failure
* timeout
* malformed structured output
* service outage
* context loss
* reasoning error
* tool failure

### Detection

Use:

* schema validation
* heartbeat/status checks
* timeout detection
* output completeness checks
* confidence validation
* cross-agent consistency checks

### Severity

**S2–S4**

### System Response

ORCA should distinguish:

```text
Agent unavailable
```

from:

```text
Agent concluded that evidence is insufficient
```

These are not equivalent.

### Fallback

* retry
* use another validated agent
* reduce ensemble size
* return evidence-only response

If the failed agent is essential to the requested decision:

> **Insufficient evidence**

### User Communication

> "One or more reasoning components were unavailable, so ORCA cannot provide the requested conclusion reliably."

### Logging

Record:

* agent ID
* task
* status
* latency
* error
* retry count
* fallback agent
* final decision

---

# 4.10 API Failure

### Failure

An external data/API service fails or returns invalid data.

### Cause

* timeout
* HTTP error
* rate limiting
* authentication failure
* provider outage
* malformed response
* schema change
* network failure

### Detection

Monitor:

* HTTP status
* response schema
* response latency
* data completeness
* timestamp validity
* provider health

### Severity

**S2–S4**

### System Response

* retry with bounded exponential backoff
* use circuit breaker
* avoid infinite retries
* mark source unavailable
* prevent failed response from entering reasoning

### Fallback

Use an approved secondary source if available.

Otherwise:

> **Insufficient evidence**

### User Communication

> "The required external data service is currently unavailable. ORCA cannot verify the requested condition."

### Logging

Record:

* endpoint
* status code
* latency
* error
* retry count
* provider
* fallback source

---

# 4.11 Malicious Input

### Failure

A user intentionally or unintentionally provides input designed to manipulate, disrupt, or exploit ORCA.

### Cause

Examples:

* malformed coordinates
* extreme numerical values
* oversized requests
* malicious strings
* command-like input
* resource exhaustion attempts
* attempts to bypass validation

### Detection

Apply:

* input validation
* length limits
* type checking
* coordinate bounds
* request-rate controls
* anomaly detection
* schema validation

### Severity

**S2–S4**

### System Response

Reject unsafe input before it reaches downstream tools.

Never pass unvalidated user input directly into:

* shell commands
* database queries
* system prompts
* API endpoints
* tool execution

### Fallback

Ask the user to provide valid input.

### User Communication

> "The supplied input could not be validated. Please provide a valid location, time, or query."

### Logging

Log security-relevant metadata without unnecessarily storing sensitive user information.

---

# 4.12 Prompt Injection

### Failure

External content or user input attempts to manipulate the behavior of an ORCA LLM or agent.

### Cause

Examples:

* malicious instructions embedded in retrieved documents
* poisoned metadata
* malicious API content
* user prompts attempting to override system policies
* tool-result injection

### Detection

Treat retrieved content as **data, not instructions**.

Use:

* trusted system instructions
* instruction/data separation
* tool permission boundaries
* output validation
* prompt-injection classifiers where appropriate
* least-privilege tool access

### Severity

**S4 — Critical**

### System Response

The agent must never allow external content to override:

* system safety rules
* evidence requirements
* authorization boundaries
* tool restrictions
* confidence rules

### Fallback

Discard compromised context and regenerate from trusted evidence.

If safe reasoning cannot continue:

> **Insufficient evidence**

### User Communication

Normally do not expose internal security mechanisms.

Use:

> "ORCA could not safely process part of the supplied information and has excluded it from the analysis."

### Logging

Record:

* injection detection event
* affected source
* affected agent
* blocked action
* security classification
* recovery action

Do not log sensitive payloads unnecessarily.

---

# 4.13 Incorrect Confidence

### Failure

ORCA reports confidence that is inconsistent with the quality or amount of evidence.

### Cause

* model-calculated confidence treated as probability
* insufficient calibration
* confidence inherited from one agent
* correlated agents counted as independent
* missing uncertainty propagation

### Detection

Evaluate confidence using:

* historical calibration
* Brier score
* reliability diagrams
* expected calibration error
* ensemble agreement
* evidence quality
* data freshness
* source consistency

### Severity

**S3–S4**

### System Response

Confidence must be constrained by evidence quality.

A high model confidence cannot override:

* stale data
* conflicting sources
* missing critical variables
* poor spatial resolution
* poor temporal resolution

### Fallback

Use qualitative evidence states:

```text
High evidence support
Moderate evidence support
Low evidence support
Insufficient evidence
```

Avoid presenting confidence as a guarantee of correctness.

### User Communication

> "Confidence is limited because the available evidence is incomplete and/or conflicting."

### Logging

Record:

* raw model confidence
* calibrated confidence
* evidence quality
* calibration version
* agent agreement
* final confidence state

---

# 4.14 Unsafe Recommendation

### Failure

ORCA generates a recommendation that could reasonably contribute to unsafe marine action.

### Cause

* incorrect data
* scientific inference error
* missing hazard data
* excessive confidence
* outdated forecast
* ignored uncertainty
* recommendation optimization without safety constraints

### Detection

Apply a dedicated recommendation safety gate.

Before issuing an operational recommendation, verify:

1. location validity
2. time validity
3. weather evidence
4. wave evidence
5. cyclone/storm information
6. data freshness
7. source consistency
8. confidence
9. hazard indicators
10. recommendation policy

### Severity

**S4 — Critical**

### System Response

If any critical safety evidence is missing, the recommendation must be blocked.

ORCA should provide:

* evidence
* uncertainty
* relevant hazards
* authoritative-source verification guidance

rather than an unsafe directive.

### Fallback

Evidence-only response.

Example:

> "ORCA can summarize the available ocean and weather conditions, but it cannot determine whether it is safe to venture into the sea from the available evidence."

### User Communication

ORCA must clearly distinguish:

```text
Observed condition
Forecast condition
Model interpretation
Decision-support insight
Safety determination
```

ORCA should not claim to provide a guaranteed safety determination.

### Logging

Record:

* recommendation request
* evidence set
* hazard checks
* safety-gate result
* blocked/approved status
* final user-facing response

---

# 4.15 Cyclone / High-Wave Scenario

### Failure

A user requests marine guidance during potentially hazardous conditions such as:

* cyclone
* severe storm
* high waves
* storm surge
* extreme winds
* severe weather warnings
* rapidly deteriorating sea state

### Cause

Environmental hazard rather than software malfunction, but it represents a high-risk decision context.

### Detection

Integrate validated hazard information where available:

* cyclone warnings
* storm warnings
* wave forecasts
* wind forecasts
* storm surge information
* official marine warnings
* extreme-condition thresholds

### Severity

**S4 — Critical**

### System Response

ORCA must enter **Hazard-Aware Mode**.

In this mode:

* safety checks take priority over optimization
* PFZ-style productivity reasoning must not override hazard information
* uncertainty must be prominently displayed
* stale hazard information must be rejected
* unsupported safety conclusions must be blocked
* the system should direct users toward current official warnings

### Fallback

If hazard status cannot be established:

> **Insufficient evidence**

If severe conditions are indicated:

ORCA should avoid telling the user to proceed.

### User Communication

Example:

> "Potentially hazardous marine conditions are indicated in the selected area. ORCA cannot guarantee safety or determine that it is safe to venture into the sea. Check the latest official weather and marine warnings and follow instructions from the relevant authorities."

If current hazard evidence itself is unavailable:

> "Insufficient evidence to assess current marine hazard conditions. ORCA cannot determine whether conditions are safe."

### Logging

Record:

* hazard source
* warning timestamp
* valid period
* location
* hazard type
* severity
* data freshness
* safety-gate decision
* user-facing warning

---

# 5. "Insufficient Evidence" Policy

## 5.1 Mandatory Refusal Conditions

ORCA must return:

> **Insufficient evidence**

when any critical condition prevents a defensible conclusion.

Examples include:

### Location

* location cannot be validated
* coordinates are ambiguous
* requested location is outside data coverage

### Time

* requested time cannot be established
* timestamps conflict
* forecast valid time is unavailable

### Data

* critical variable is missing
* required dataset is stale
* source has failed
* data quality is unacceptable

### Conflict

* authoritative sources materially disagree
* conflict cannot be resolved
* uncertainty is too high for the requested conclusion

### Scientific Reasoning

* available observations do not support the requested inference
* scientific relationship is uncertain
* evidence is insufficient to distinguish competing hypotheses

### Agentic Reasoning

* required reasoning agent fails
* agents disagree on a critical conclusion
* no trustworthy consensus can be established

### Safety

* current hazard status cannot be established
* cyclone/high-wave information is unavailable when relevant
* critical safety evidence is stale
* the system cannot validate the requested safety-related conclusion

---

# 6. Insufficient Evidence Is Not a System Failure

ORCA should distinguish between:

```text
System Failure
```

and:

```text
Scientifically Correct Abstention
```

For example:

```text
API unavailable
        ↓
Cannot obtain current wave data
        ↓
Cannot establish sea condition
        ↓
Insufficient evidence
```

This is preferable to:

```text
API unavailable
        ↓
Guess wave condition
        ↓
Generate recommendation
```

The second behavior is unacceptable.

---

# 7. Evidence State Model

Every ORCA response should internally classify evidence.

```text
VALID
  ↓
SUFFICIENT
  ↓
CONSISTENT
  ↓
SCIENTIFICALLY RELEVANT
  ↓
REASONING ALLOWED
```

Possible final states:

```text
EVIDENCE_SUFFICIENT
EVIDENCE_LIMITED
EVIDENCE_CONFLICTING
EVIDENCE_STALE
EVIDENCE_MISSING
EVIDENCE_INVALID
EVIDENCE_UNAVAILABLE
```

Only appropriate states should allow recommendation generation.

---

# 8. Recommendation Safety Gate

Before ORCA generates a potentially consequential recommendation:

```text
User Query
    ↓
Location Validation
    ↓
Timestamp Validation
    ↓
Dataset Validation
    ↓
Freshness Validation
    ↓
Completeness Check
    ↓
Conflict Detection
    ↓
Hazard Check
    ↓
Scientific Reasoning
    ↓
Agent Agreement
    ↓
Confidence Calibration
    ↓
Safety Gate
    ↓
Recommendation OR Abstention
```

The safety gate must be **fail-closed**.

If the safety gate cannot establish that the required evidence is available:

```text
BLOCK RECOMMENDATION
        ↓
Insufficient evidence
```

---

# 9. Fallback Hierarchy

ORCA should use the following fallback hierarchy:

```text
Primary authoritative source
        ↓
Secondary validated source
        ↓
Historical/contextual information
        ↓
Evidence-only response
        ↓
Insufficient evidence
```

ORCA must never use:

```text
Guessing
Fabrication
Unsupported interpolation
Unverified web content
LLM prior knowledge presented as current observation
```

as a fallback for safety-critical information.

---

# 10. Graceful Degradation

ORCA should degrade capabilities rather than degrade truthfulness.

Example:

If current chlorophyll-a data is unavailable:

### Bad behavior

> "There is probably high chlorophyll concentration."

### Correct behavior

> "Current chlorophyll-a data is unavailable for the requested area, so ORCA cannot assess present productivity conditions."

The system may still provide other independently supported information.

---

# 11. Data Quality Gates

Every dataset entering ORCA should pass:

### Gate 1 — Identity

Is this the expected dataset?

### Gate 2 — Source

Is the provider trusted/approved?

### Gate 3 — Schema

Are variables and units correct?

### Gate 4 — Spatial

Does the dataset cover the requested location?

### Gate 5 — Temporal

Does it cover the requested time?

### Gate 6 — Freshness

Is it sufficiently current?

### Gate 7 — Quality

Are quality flags acceptable?

### Gate 8 — Completeness

Are critical values available?

### Gate 9 — Consistency

Does it materially conflict with other evidence?

### Gate 10 — Scientific Relevance

Can this variable actually support the requested inference?

---

# 12. Agent Safety Architecture

ORCA's agents should operate under least privilege.

An agent should receive only:

* required data
* validated metadata
* explicit task definition
* permitted tools
* evidence identifiers

Agents should not independently decide:

* whether safety requirements can be ignored
* whether missing data should be invented
* whether system policies should be overridden
* whether external instructions are trustworthy

A separate orchestration/safety layer should enforce these constraints.

---

# 13. Evidence Attribution

Every consequential claim should be traceable to evidence.

Recommended structure:

```text
Claim
 ├── Dataset
 ├── Variable
 ├── Observation/Forecast
 ├── Timestamp
 ├── Location
 ├── Source
 ├── Processing
 └── Reasoning
```

If a claim cannot be traced:

```text
CLAIM_NOT_SUPPORTED
```

The claim should not be presented as established fact.

---

# 14. Logging and Auditability

Safety-relevant events must be auditable.

Log:

* request ID
* timestamp
* location context
* data sources
* dataset versions
* observation timestamps
* retrieval timestamps
* data-quality status
* agent execution
* tool execution
* validation results
* conflicts
* confidence
* safety-gate result
* fallback path
* final response classification

Avoid logging unnecessary personal or sensitive information.

---

# 15. Failure Injection Testing

ORCA should deliberately test failure conditions.

Required scenarios include:

1. Remove SST data.
2. Remove chlorophyll-a data.
3. Return stale observations.
4. Return conflicting SST observations.
5. Swap latitude and longitude.
6. Shift timestamps by timezone.
7. Return malformed API JSON.
8. Force API timeout.
9. Make an agent unavailable.
10. Inject unsupported LLM claims.
11. Inject malicious retrieved content.
12. Inject prompt-injection instructions.
13. Provide extreme coordinates.
14. Provide cyclone conditions.
15. Provide high-wave conditions.
16. Remove all hazard information.
17. Produce artificially high agent confidence.
18. Create disagreement among agents.
19. Corrupt dataset metadata.
20. Provide incomplete spatial coverage.

The expected behavior should be verified automatically.

---

# 16. Safety Test Oracle

For each failure test, the system should verify:

```text
Was the failure detected?
        ↓
Was unsafe reasoning blocked?
        ↓
Was the correct fallback selected?
        ↓
Was uncertainty communicated?
        ↓
Was the event logged?
```

A test should fail if ORCA produces a confident unsupported recommendation.

---

# 17. Example Safe Responses

## Missing Data

> "Insufficient evidence. Required oceanographic data is unavailable for the requested location and time."

## Conflicting Data

> "Insufficient evidence. Available sources provide materially different estimates, and ORCA cannot resolve the discrepancy reliably."

## Stale Data

> "Insufficient evidence. The latest available observation is too old to support a current-condition assessment."

## Unvalidated Location

> "Insufficient evidence. ORCA could not reliably validate the requested geographic location."

## Scientific Uncertainty

> "The available observations do not provide sufficient evidence to support that scientific inference."

## API Failure

> "Insufficient evidence. ORCA could not retrieve the required current data source."

## Safety-Critical Query

> "ORCA cannot establish that conditions are safe from the available evidence. Please consult the latest authoritative marine and weather warnings before making an operational decision."

## Cyclone / High-Wave Conditions

> "Potentially hazardous marine conditions are indicated. ORCA cannot guarantee safety or determine that it is safe to venture into the sea. Consult the latest official warnings and follow instructions from the relevant authorities."

---

# 18. Unsafe Response Patterns

ORCA must prevent statements such as:

> "It is safe to go fishing."

> "The sea will be safe tomorrow."

> "There is no cyclone risk."

> "You can safely travel through this area."

> "The PFZ guarantees a good catch."

> "The weather will definitely remain calm."

> "There is no danger."

> "The model is 99% certain, so it is safe."

These statements convert probabilistic environmental intelligence into unsupported guarantees.

---

# 19. PFZ-Specific Safety Considerations

A Potential Fishing Zone prediction is an **environmental intelligence output**, not a guarantee of:

* fish presence
* catch quantity
* fishing success
* navigational safety
* weather safety
* vessel safety

ORCA must therefore distinguish:

```text
Potential ecological productivity
```

from:

```text
Operational safety
```

For example:

> "Environmental indicators are consistent with conditions associated with potential productivity."

is acceptable.

> "This location is guaranteed to have fish and is safe to fish."

is unacceptable.

---

# 20. Decision Policy

ORCA should follow this fundamental policy:

```text
                    ┌─────────────────┐
                    │ User Question   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Validate Input  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Validate Data   │
                    └────────┬────────┘
                             ↓
                 ┌───────────┴───────────┐
                 │                       │
          Evidence Sufficient      Evidence Failed
                 │                       │
                 ↓                       ↓
          Scientific Reasoning    ┌───────────────────┐
                 │                 │ Insufficient      │
                 ↓                 │ Evidence          │
          Conflict Check          └───────────────────┘
                 │
          ┌──────┴──────┐
          │             │
       Resolved      Unresolved
          │             │
          ↓             ↓
    Safety Gate   Insufficient Evidence
          │
    ┌─────┴─────┐
    │           │
   Pass        Fail
    │           │
    ↓           ↓
Decision     Block
Support      Recommendation
```

---

# 21. Golden Safety Rule

The most important ORCA safety rule is:

> **ORCA must prefer an explicit "Insufficient evidence" response over a plausible but unsupported answer.**

In marine decision support:

```text
Unknown ≠ Safe
Missing ≠ Normal
Stale ≠ Current
Model confidence ≠ Physical certainty
Agent agreement ≠ Truth
Prediction ≠ Guarantee
PFZ ≠ Guaranteed catch
No warning detected ≠ No danger
```

---

# 22. Final Safety Position

ORCA is a **decision-support system**, not an autonomous authority for marine safety.

Its outputs should support human decision-making by providing:

* evidence
* observations
* forecasts
* scientific interpretations
* uncertainty
* source attribution
* conflicts
* limitations

ORCA must not claim to guarantee:

* safety
* navigation
* fishing success
* weather conditions
* cyclone absence
* absence of marine hazards
* accuracy of future environmental conditions

When evidence is inadequate, contradictory, stale, unavailable, or scientifically insufficient, the correct behavior is:

> **Insufficient evidence**

That behavior is a core feature of a trustworthy marine intelligence system—not a weakness.
