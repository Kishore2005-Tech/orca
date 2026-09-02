# EVALUATION_AND_TESTING.md

## SIH26176 – ORCA
### Marine Ecosystems Reasoning with Collaborative Agents

**Organization:** ISRO  
**Category:** Software  
**Domain:** Marine Ecosystems + Earth Observation + AI + Agentic AI + Decision Intelligence

---

## 1. Purpose

This document defines the evaluation and testing methodology for ORCA.

ORCA must be evaluated on **two complementary dimensions**:

1. **Software correctness** — whether the platform retrieves, processes, serves, and presents data correctly and reliably.
2. **Scientific reasoning quality** — whether the system correctly interprets heterogeneous marine and Earth-observation information, grounds its conclusions in evidence, resolves conflicting signals, and produces scientifically defensible recommendations.

No evaluation result is assumed in this document. All metrics, datasets, scenarios, baselines, and success criteria describe **how results will be measured**.

---

# 2. Evaluation Principles

ORCA evaluation should follow these principles:

- **Evidence-first:** scientific claims must be traceable to supporting observations, datasets, or authoritative sources.
- **Ground-truth driven:** quantitative evaluation should use independently prepared reference answers or measurements.
- **Temporal validity:** time-sensitive marine information must be evaluated against the correct observation/forecast time.
- **Spatial validity:** coordinates, regions, grids, and distances must be checked against authoritative geographic references.
- **Reproducibility:** each experiment should record dataset version, timestamp, model version, agent configuration, prompts, and evaluation parameters.
- **No fabricated results:** results must be reported only after the corresponding experiment has actually been executed.
- **Separate correctness from usefulness:** a response can be technically correct but operationally unhelpful, so both should be measured.
- **Failure analysis:** incorrect outputs should be categorized rather than treated as a single aggregate error.

---

# 3. Evaluation Architecture

ORCA should be evaluated through the following pipeline:

```text
Test Dataset
    |
    v
Data Ingestion
    |
    v
Data Validation
    |
    v
Agent / Model Processing
    |
    v
Evidence Retrieval
    |
    v
Collaborative Reasoning
    |
    v
Conflict Resolution
    |
    v
Recommendation Generation
    |
    v
API Response
    |
    v
UI Presentation
    |
    v
Evaluation Harness
    |
    +--> Software Metrics
    |
    +--> Scientific Metrics
    |
    +--> Agent Metrics
    |
    +--> Human Evaluation
    |
    v
Evaluation Report
```

---

# 4. Evaluation Categories

| Category | Primary Objective |
|---|---|
| Data accuracy | Verify retrieved and processed marine data |
| Data freshness | Verify temporal currency of information |
| Spatial accuracy | Verify geographic correctness |
| Temporal accuracy | Verify correct time interpretation |
| Evidence attribution | Verify claims are supported by evidence |
| Reasoning accuracy | Verify scientific conclusions |
| Agent agreement | Measure consistency between agents |
| Conflict resolution | Evaluate handling of contradictory evidence |
| Hallucination rate | Detect unsupported claims |
| Confidence calibration | Measure whether confidence reflects correctness |
| Recommendation accuracy | Evaluate operational recommendations |
| API reliability | Verify backend robustness |
| Latency | Measure system response time |
| UI usability | Measure usability and task completion |

---

# 5. Test Dataset Strategy

ORCA should use multiple classes of datasets rather than relying on a single test source.

## 5.1 Dataset Classes

### A. Historical observation datasets

Used for testing known marine conditions.

Examples of variables:

- Sea Surface Temperature (SST)
- Sea Surface Salinity (SSS)
- Sea Surface Height (SSH)
- Chlorophyll-a
- Ocean currents
- Wind
- Wave height
- Mixed Layer Depth (MLD)
- Bathymetry
- Upwelling indicators
- Ocean fronts
- Eddy indicators

### B. Forecast datasets

Used to evaluate time-dependent predictions and operational queries.

Examples:

- Weather forecasts
- Wave forecasts
- Wind forecasts
- Ocean-current forecasts
- Tide predictions

### C. Geographic datasets

Used to validate:

- Coastlines
- Fishing locations
- Marine regions
- Bathymetry
- EEZ boundaries where applicable
- Distance calculations
- Spatial intersections

### D. Derived scientific datasets

Used to evaluate ORCA's interpretation of relationships between variables.

Examples:

- Potential Fishing Zone (PFZ) indicators
- Chlorophyll-temperature relationships
- Front detection
- Upwelling indicators
- Ocean productivity indicators

### E. Adversarial datasets

Designed specifically to test failure modes.

Examples:

- Missing values
- Stale observations
- Conflicting sources
- Different spatial resolutions
- Different timestamps
- Sensor anomalies
- Extreme weather
- Contradictory agent outputs
- Incomplete metadata

---

# 6. Dataset Splitting

Where model training or tuning is involved, evaluation data must not be reused for training.

Recommended split:

```text
Training / Development
        |
        +--> Validation
        |
        +--> Held-out Test Set
                    |
                    +--> Final Evaluation
```

For time-series marine data, a **temporal holdout** should be preferred where possible.

Example:

```text
Historical period A -> Development
Historical period B -> Validation
Later unseen period -> Final Test
```

This reduces temporal leakage and provides a more realistic measure of operational performance.

---

# 7. Ground Truth

Ground truth is the reference against which ORCA outputs are evaluated.

## 7.1 Ground-truth sources

Ground truth may include:

- Authoritative observation datasets
- Official forecast products
- Verified geographic coordinates
- Expert-validated scientific interpretations
- Human-reviewed question-answer pairs
- Independently calculated physical quantities
- Official marine advisories where applicable
- Expert-reviewed recommendation labels

## 7.2 Ground-truth record

Each test case should contain:

```json
{
  "scenario_id": "ORCA-001",
  "query": "...",
  "location": {
    "latitude": 0.0,
    "longitude": 0.0
  },
  "reference_time": "...",
  "required_variables": [],
  "ground_truth": {},
  "acceptable_reasoning": [],
  "required_evidence": [],
  "expected_constraints": []
}
```

The actual values should come from the selected evaluation dataset and should not be fabricated.

---

# 8. Test Scenario Design

Each scenario should test one or more ORCA capabilities.

## Scenario 1 — Potential Fishing Zone Query

**Question:**

> "Where is the nearest Potential Fishing Zone today?"

Evaluate:

- Location correctness
- Data freshness
- PFZ evidence
- Distance calculation
- Scientific reasoning
- Confidence
- Recommendation quality

### Expected evaluation

The evaluator compares the response against the independently prepared PFZ reference for the corresponding date and region.

---

## Scenario 2 — Sea Safety Query

**Question:**

> "Is it safe to venture into the sea tomorrow morning?"

Evaluate:

- Forecast timestamp
- Wind
- Wave height
- Weather conditions
- Relevant marine warnings
- Uncertainty
- Evidence attribution
- Recommendation correctness

The system must not present a safety conclusion without considering the relevant available evidence.

---

## Scenario 3 — Local Marine Conditions

**Question:**

> "What are the tide, weather, and sea conditions near my fishing location?"

Evaluate:

- Correct location
- Correct temporal window
- Tide information
- Weather information
- Sea-state information
- Source attribution
- Unit consistency

---

## Scenario 4 — Conflicting Evidence

Provide agents with intentionally conflicting observations.

Example:

```text
Source A:
SST indicates a thermal feature.

Source B:
Recent observation does not show the same feature.

Source C:
Chlorophyll information is outdated.
```

Evaluate:

- Whether agents detect the conflict
- Whether stale data is identified
- Whether evidence is weighted appropriately
- Whether the final answer communicates uncertainty
- Whether the system avoids arbitrary agreement

---

## Scenario 5 — Missing Data

Remove one or more important variables.

Example:

```text
SST = available
Chlorophyll = unavailable
Wind = available
Wave = available
```

Evaluate whether ORCA:

- Detects missing information
- Avoids pretending the information exists
- Adjusts confidence
- Explains the limitation
- Produces only a defensible recommendation

---

## Scenario 6 — Temporal Mismatch

Provide:

```text
SST observation: T1
Chlorophyll observation: T2
Weather forecast: T3
User query: T4
```

Evaluate whether ORCA:

- Identifies observation age
- Aligns variables appropriately
- Avoids treating old observations as current
- Communicates temporal uncertainty

---

## Scenario 7 — Spatial Resolution Mismatch

Provide datasets with different resolutions.

Example:

```text
Dataset A: high-resolution SST
Dataset B: coarse-resolution chlorophyll
Dataset C: regional weather forecast
```

Evaluate:

- Spatial alignment
- Interpolation assumptions
- Region selection
- Distance calculations
- Confidence adjustment

---

# 9. Metric Definitions

## 9.1 Data Accuracy

Measures whether ORCA retrieves and represents source data correctly.

### Numeric variables

For continuous variables:

**MAE**

```text
MAE = (1/n) * Σ |prediction - ground_truth|
```

**RMSE**

```text
RMSE = sqrt((1/n) * Σ(prediction - ground_truth)^2)
```

**Relative Error**

```text
Relative Error = |prediction - ground_truth| / |ground_truth|
```

For categorical variables:

```text
Accuracy = Correct Predictions / Total Predictions
```

### Example

If the reference SST is 28.0°C and ORCA reports 28.2°C:

```text
Absolute Error = 0.2°C
```

The error should be compared against the predefined tolerance for that variable.

---

# 10. Data Freshness

Measures whether ORCA uses sufficiently recent information.

Define:

```text
Data Age = Query Time - Observation / Publication Time
```

Measure:

- Median data age
- Mean data age
- Maximum data age
- Percentage of responses within freshness threshold
- Percentage of stale-data detections

### Example

If a user asks for today's marine conditions and the selected observation is several days old, the system should identify that age and avoid presenting it as a current observation.

---

# 11. Spatial Accuracy

Measures correctness of geographic interpretation.

Metrics:

### Coordinate error

```text
Distance Error = Haversine(predicted_coordinate, reference_coordinate)
```

Report:

- Mean distance error
- Median distance error
- 95th percentile distance error
- Percentage within predefined spatial tolerance

### Region accuracy

```text
Region Accuracy =
Correct Region Predictions / Total Region Predictions
```

### Example

If ORCA identifies a PFZ location, compare the predicted location with the independently validated reference location or reference region.

---

# 12. Temporal Accuracy

Measures whether ORCA interprets and aligns timestamps correctly.

Metrics:

- Timestamp parsing accuracy
- Time-zone conversion accuracy
- Forecast-window accuracy
- Observation-window accuracy
- Temporal alignment error
- Percentage of responses using correct time window

### Example

A request for:

> "tomorrow morning"

must be mapped to the correct local date and predefined morning interval.

The evaluation should verify both the date and the applicable time window.

---

# 13. Evidence Attribution

Measures whether scientific claims are traceable to supporting evidence.

For every factual claim, evaluate:

```text
Claim
  |
  +--> Evidence exists?
  |
  +--> Evidence is relevant?
  |
  +--> Evidence supports claim?
  |
  +--> Source is correctly identified?
```

### Metrics

**Evidence Coverage**

```text
Evidence Coverage =
Supported Factual Claims / Total Factual Claims
```

**Attribution Precision**

```text
Attribution Precision =
Correctly Attributed Evidence / Total Evidence Attributions
```

**Attribution Recall**

```text
Attribution Recall =
Required Supporting Evidence Retrieved /
Total Required Supporting Evidence
```

### Example

Claim:

> "The region has elevated chlorophyll-a."

The evaluator checks whether the cited chlorophyll dataset actually supports that statement for the stated location and time.

---

# 14. Reasoning Accuracy

Reasoning accuracy evaluates the scientific conclusion rather than only individual data values.

Each reasoning test should define:

1. Input evidence
2. Scientific relationship
3. Expected conclusion
4. Acceptable alternative conclusions
5. Conditions that invalidate the conclusion

### Evaluation methods

- Expert-validated labels
- Rule-based reference reasoning
- Structured answer keys
- Pairwise comparison with expert answers
- Rubric-based scoring

### Example rubric

| Criterion | Score |
|---|---:|
| Correct evidence identification | 0–2 |
| Correct scientific interpretation | 0–3 |
| Correct handling of uncertainty | 0–2 |
| Correct final conclusion | 0–3 |
| **Total** | **10** |

The rubric must be defined before evaluation to reduce evaluator bias.

---

# 15. Agent Agreement

ORCA may use multiple specialized agents.

Examples:

- Oceanography Agent
- Marine Biology Agent
- Weather Agent
- Spatial Agent
- Temporal Agent
- Safety Agent
- Evidence Agent

Agent agreement should not mean that agents simply produce identical answers.

Measure:

### Agreement Rate

```text
Agreement Rate =
Cases with Consistent Conclusions / Total Multi-Agent Cases
```

Also measure:

- Variable-level agreement
- Conclusion-level agreement
- Evidence agreement
- Confidence agreement

### Important distinction

High agreement is **not automatically good**.

If all agents make the same incorrect assumption, agreement can be high while correctness is low.

Therefore:

```text
Agent Agreement + Ground Truth Accuracy
```

must be evaluated together.

---

# 16. Conflict Resolution

Conflict-resolution testing measures whether ORCA handles contradictory evidence correctly.

## Conflict types

1. Different values from different sources
2. Different timestamps
3. Different spatial resolutions
4. Observation vs forecast disagreement
5. Agent-to-agent disagreement
6. Missing metadata
7. Low-confidence source vs high-confidence source

### Metrics

**Conflict Detection Rate**

```text
Detected Conflicts / Injected Conflicts
```

**Resolution Accuracy**

```text
Correct Resolutions / Detected Conflicts
```

**Uncertainty Communication Rate**

```text
Conflicts with Explicit Uncertainty /
Total Relevant Conflicts
```

### Example

If one agent reports favorable sea conditions while another identifies hazardous waves, ORCA should not simply average the conclusions.

The evaluator checks whether the system:

- Identifies the disagreement
- Examines source quality
- Considers recency
- Considers spatial and temporal alignment
- Resolves or preserves the conflict appropriately
- Communicates uncertainty

---

# 17. Hallucination Rate

Hallucination testing measures unsupported or fabricated information.

## Definition

A hallucination is a factual claim that:

- Is unsupported by available evidence,
- Contradicts the supplied evidence,
- Invents a source,
- Invents a measurement,
- Invents an observation,
- Or claims unavailable data was retrieved.

### Metric

```text
Hallucination Rate =
Unsupported / Incorrect Factual Claims /
Total Factual Claims
```

Also track:

- Source hallucination rate
- Numerical hallucination rate
- Location hallucination rate
- Temporal hallucination rate
- Scientific reasoning hallucination rate

### Adversarial test

Ask ORCA a question for which the required dataset is intentionally unavailable.

Expected behavior:

```text
"I do not have sufficient evidence to determine this."
```

rather than fabricated data.

---

# 18. Confidence Calibration

Confidence should correspond to actual correctness.

For each response record:

```text
Predicted Confidence
Actual Correctness
```

## Metrics

### Expected Calibration Error (ECE)

Group predictions into confidence bins and calculate:

```text
ECE = Σ (|Bin| / N) * |Accuracy(Bin) - Confidence(Bin)|
```

Lower ECE indicates better calibration.

### Brier Score

For binary correctness:

```text
Brier Score =
(1/N) * Σ(confidence - outcome)^2
```

where:

```text
outcome = 1 if correct
outcome = 0 if incorrect
```

### Calibration requirement

High-confidence answers should have demonstrably higher empirical correctness than low-confidence answers.

---

# 19. Recommendation Accuracy

Recommendations must be evaluated separately from factual answers.

Examples:

- Suggested fishing region
- Suggested departure timing
- Sea-condition warning
- Need for additional verification
- Avoidance recommendation

### Evaluation

Each recommendation should be compared against:

- Ground-truth scenario conditions
- Expert judgment
- Defined operational rules
- Relevant safety constraints

### Metrics

**Recommendation Accuracy**

```text
Correct Recommendations / Total Recommendations
```

**Unsafe Recommendation Rate**

```text
Unsafe Recommendations / Total Safety-Critical Recommendations
```

**Appropriate Abstention Rate**

```text
Correct Abstentions / Cases Requiring Abstention
```

For safety-related outputs, avoiding an unsupported recommendation is an important success criterion.

---

# 20. API Reliability

Evaluate all critical APIs and service dependencies.

## Metrics

### Availability

```text
Availability =
Successful Requests / Total Requests
```

### Error Rate

```text
Error Rate =
Failed Requests / Total Requests
```

### Timeout Rate

```text
Timeout Rate =
Timed-Out Requests / Total Requests
```

### Data Integrity

Verify:

- HTTP status correctness
- Schema correctness
- Required fields
- Units
- Coordinate ranges
- Timestamp format
- Null handling
- Error responses

### Load testing

Test at increasing request volumes and record:

- Requests per second
- Error rate
- Resource utilization
- Response latency
- Timeout behavior

---

# 21. Latency

Measure end-to-end response time.

Break latency into:

```text
Total Latency =
API Request
+ Data Retrieval
+ Preprocessing
+ Agent Execution
+ Evidence Retrieval
+ Conflict Resolution
+ Recommendation Generation
+ Response Serialization
```

## Metrics

Report:

- Mean latency
- Median latency
- P90 latency
- P95 latency
- P99 latency
- Maximum latency

### Example

Instead of reporting only:

```text
Average latency = X
```

report:

```text
P50 = ...
P90 = ...
P95 = ...
P99 = ...
```

The values must be filled only after actual testing.

---

# 22. UI Usability

Evaluate whether users can successfully complete marine-information tasks.

## Target task categories

### Task A
Find today's PFZ information.

### Task B
Check sea conditions for tomorrow morning.

### Task C
Inspect evidence supporting a recommendation.

### Task D
Understand uncertainty or conflicting evidence.

### Task E
Locate a recommended region on the map.

## Metrics

### Task Completion Rate

```text
Completed Tasks / Total Tasks
```

### Time on Task

Measure time from task start to successful completion.

### Error Rate

```text
User Errors / Total Tasks
```

### System Usability Scale

Use the standard **System Usability Scale (SUS)** questionnaire.

### Qualitative feedback

Collect:

- Clarity
- Trust
- Evidence transparency
- Map comprehension
- Recommendation usefulness
- Cognitive load
- Perceived confidence
- Ease of interaction

---

# 23. Software Correctness Test Suite

## 23.1 Unit Tests

Test individual components:

- Data parsers
- Coordinate conversion
- Unit conversion
- Timestamp conversion
- Distance calculation
- Data validation
- Agent functions
- Evidence extraction
- Confidence calculation

---

## 23.2 Integration Tests

Test:

```text
Data Source
    ->
Data Adapter
    ->
Processing Layer
    ->
Agent
    ->
Evidence Layer
    ->
Decision Layer
    ->
API
```

Verify that each component passes valid data and errors correctly to the next layer.

---

## 23.3 End-to-End Tests

Simulate complete user workflows.

Example:

```text
User Query
   ->
Intent Detection
   ->
Data Retrieval
   ->
Multi-Agent Analysis
   ->
Evidence Validation
   ->
Conflict Resolution
   ->
Recommendation
   ->
UI Response
```

---

## 23.4 Regression Tests

Every bug discovered in production or testing should become a permanent regression test.

Example:

```text
Bug:
Incorrect timezone conversion for local marine forecast.

Regression test:
Input timestamp + timezone
Expected local timestamp
```

---

# 24. Scientific Validation Tests

Scientific validation should be performed independently of UI testing.

## 24.1 Variable-level validation

Test each variable independently:

- SST
- SSS
- SSH
- Chlorophyll-a
- Current
- Wind
- Wave height
- MLD
- Bathymetry
- Tide

Check:

- Value
- Unit
- Timestamp
- Coordinate
- Source
- Missing-value handling

---

## 24.2 Relationship-level validation

Test scientifically meaningful relationships.

Examples:

```text
SST + Chlorophyll-a
SST + Ocean Front
Wind + Wave Height
SSH + Eddy Indicators
Wind + Upwelling
Bathymetry + Fishing Region
```

The evaluation should verify that ORCA does not infer causation merely from correlation.

---

# 25. Baselines

ORCA should be compared against appropriate baselines.

## Baseline 1 — Raw Data Dashboard

A conventional dashboard that displays datasets without collaborative reasoning.

Measures whether ORCA provides value beyond visualization.

---

## Baseline 2 — Single-Agent LLM

Use one general-purpose model to answer the same questions using the same available evidence.

Compare:

- Reasoning accuracy
- Evidence attribution
- Hallucination rate
- Confidence calibration
- Recommendation accuracy

---

## Baseline 3 — Rule-Based System

Use predefined marine rules without multi-agent reasoning.

Compare:

- Deterministic correctness
- Interpretability
- Conflict handling
- Recommendation quality

---

## Baseline 4 — Retrieval-Augmented Single Agent

Provide retrieved evidence to one agent but without specialized collaborative agents.

This isolates the value of:

```text
RAG
vs
Multi-Agent Reasoning
```

---

## Baseline 5 — Human Expert

Where feasible, qualified marine-domain evaluators should independently answer selected scenarios.

Human evaluation is not necessarily the "ground truth" for every numerical variable, but it can provide a strong reference for scientific interpretation and operational usefulness.

---

# 26. Comparative Evaluation Matrix

| Capability | Dashboard | Rule System | Single Agent | RAG Agent | ORCA |
|---|---:|---:|---:|---:|---:|
| Multi-source data integration | Evaluate | Evaluate | Evaluate | Evaluate | Evaluate |
| Evidence attribution | Evaluate | Evaluate | Evaluate | Evaluate | Evaluate |
| Multi-agent reasoning | No | No | No | No | Yes |
| Conflict resolution | Limited | Rule-defined | Limited | Limited | Evaluate |
| Spatial reasoning | Evaluate | Evaluate | Evaluate | Evaluate | Evaluate |
| Temporal reasoning | Evaluate | Evaluate | Evaluate | Evaluate | Evaluate |
| Recommendation generation | Limited | Evaluate | Evaluate | Evaluate | Evaluate |
| Explainability | Evaluate | High | Evaluate | Evaluate | Evaluate |
| Uncertainty handling | Evaluate | Rule-defined | Evaluate | Evaluate | Evaluate |

No performance values should be inserted until the experiments are executed.

---

# 27. Ablation Testing

Ablation tests determine which ORCA components actually contribute to performance.

## Ablation A — Remove Multi-Agent Collaboration

```text
Full ORCA
vs
Single Agent
```

Measure:

- Reasoning accuracy
- Evidence attribution
- Conflict resolution
- Hallucination rate
- Recommendation accuracy

---

## Ablation B — Remove Evidence Retrieval

```text
Full ORCA
vs
ORCA without evidence retrieval
```

Measure:

- Hallucination rate
- Evidence coverage
- Reasoning accuracy
- Confidence calibration

---

## Ablation C — Remove Conflict Resolution

```text
Full ORCA
vs
No conflict-resolution layer
```

Use intentionally conflicting datasets.

Measure:

- Conflict detection
- Resolution accuracy
- Recommendation accuracy
- Uncertainty communication

---

## Ablation D — Remove Temporal Reasoning

Test whether the system incorrectly mixes:

- Historical observations
- Current observations
- Forecasts
- Future conditions

Measure temporal accuracy and scientific reasoning accuracy.

---

## Ablation E — Remove Spatial Reasoning

Test:

- Coordinate interpretation
- Region matching
- Distance calculations
- Spatial joins
- PFZ localization

---

## Ablation F — Remove Confidence Calibration

Compare raw model confidence with calibrated confidence.

Measure:

- ECE
- Brier score
- Overconfidence rate
- Underconfidence rate

---

# 28. Error Taxonomy

Every failed test should be assigned one or more categories.

```text
DATA_ERROR
SOURCE_ERROR
FRESHNESS_ERROR
SPATIAL_ERROR
TEMPORAL_ERROR
UNIT_ERROR
EVIDENCE_ERROR
REASONING_ERROR
AGENT_DISAGREEMENT
CONFLICT_RESOLUTION_ERROR
HALLUCINATION
CONFIDENCE_ERROR
RECOMMENDATION_ERROR
API_ERROR
LATENCY_ERROR
UI_ERROR
```

This makes failure analysis actionable.

---

# 29. Quantitative Success Criteria

The following are **proposed evaluation targets**, not measured results.

Final thresholds should be validated against dataset difficulty, domain requirements, and expert review.

| Metric | Proposed Success Criterion |
|---|---|
| Data accuracy | Meet predefined variable-specific tolerance |
| Data freshness | ≥ 95% of time-sensitive responses use data within defined freshness limits |
| Spatial accuracy | ≥ 95% within scenario-specific spatial tolerance |
| Temporal accuracy | ≥ 95% correct time interpretation |
| Evidence attribution | ≥ 95% of factual claims correctly supported |
| Reasoning accuracy | ≥ 85% on expert-validated reasoning benchmark |
| Agent agreement | ≥ 90% consistency on non-conflicting scenarios |
| Conflict resolution | ≥ 85% correct resolution or appropriate abstention |
| Hallucination rate | ≤ 5% factual-claim hallucination rate |
| Confidence calibration | ECE ≤ 0.10 |
| Recommendation accuracy | ≥ 85% on validated recommendation scenarios |
| API reliability | ≥ 99% successful requests in controlled reliability testing |
| P95 latency | Define target based on deployment architecture; measure experimentally |
| UI task completion | ≥ 90% successful completion on defined usability tasks |

**Important:** These are target thresholds for evaluation planning. They must not be presented as achieved ORCA results.

---

# 30. Qualitative Evaluation

Quantitative metrics alone cannot establish scientific usefulness.

Expert reviewers should assess:

## Scientific quality

- Is the interpretation scientifically defensible?
- Are relevant variables considered?
- Are relationships explained correctly?
- Are limitations acknowledged?

## Evidence quality

- Can the reviewer trace claims to evidence?
- Are sources relevant?
- Are timestamps and locations clear?

## Reasoning quality

- Is the chain of reasoning coherent?
- Does the system distinguish observation from inference?
- Does it avoid unjustified causal claims?

## Recommendation quality

- Is the recommendation actionable?
- Is uncertainty communicated?
- Does the recommendation respect safety constraints?

## User trust

- Can users understand why a recommendation was produced?
- Can they inspect supporting evidence?
- Can they recognize uncertainty?

---

# 31. Human Expert Evaluation Protocol

A domain-expert panel may evaluate a representative subset of scenarios.

Each expert should independently score:

```text
Scientific correctness: 1–5
Evidence quality: 1–5
Reasoning quality: 1–5
Recommendation usefulness: 1–5
Uncertainty communication: 1–5
Overall usefulness: 1–5
```

For stronger evaluation, reviewers should score outputs **without seeing ORCA's internal confidence score**.

Inter-rater agreement can be measured using an appropriate statistic such as:

- Cohen's kappa for two raters and categorical labels
- Fleiss' kappa for multiple raters
- Krippendorff's alpha for broader annotation settings

The selected statistic should match the annotation design.

---

# 32. Test Case Format

Each test case should contain:

```yaml
id: ORCA-TEST-001
category: reasoning
query: "Where is the nearest Potential Fishing Zone today?"
location:
  latitude: <reference>
  longitude: <reference>
reference_time: <reference>
datasets:
  - <dataset-id>
ground_truth:
  <reference-values>
expected_evidence:
  - <source-id>
expected_reasoning:
  - <validated-condition>
expected_output:
  <reference-answer-or-label>
tolerances:
  spatial: <defined-threshold>
  temporal: <defined-threshold>
  numeric: <variable-specific-threshold>
```

Values represented by placeholders must be populated from actual evaluation data.

---

# 33. Evaluation Run Metadata

Every experiment should record:

```yaml
experiment_id: <unique-id>
date: <execution-date>
dataset_versions:
  - <dataset>
model_versions:
  - <model>
agent_configuration: <configuration>
prompt_version: <version>
retrieval_configuration: <configuration>
evaluation_suite_version: <version>
random_seed: <if applicable>
hardware: <environment>
software_commit: <git-commit>
```

This allows results to be reproduced and compared.

---

# 34. Evaluation Procedure

## Step 1 — Prepare Dataset

- Freeze test data
- Record dataset versions
- Validate ground truth
- Define tolerances

## Step 2 — Prepare Test Cases

- Create scenario set
- Include normal and adversarial cases
- Define expected evidence
- Define expected outcomes

## Step 3 — Run Baselines

Execute:

- Dashboard baseline
- Rule-based baseline
- Single-agent baseline
- RAG baseline

where applicable.

## Step 4 — Run ORCA

Execute the identical test cases using the specified ORCA configuration.

## Step 5 — Capture Outputs

Store:

- Input query
- Retrieved data
- Agent outputs
- Evidence
- Final reasoning
- Confidence
- Recommendation
- API timing
- Errors

## Step 6 — Automatic Evaluation

Calculate:

- Data errors
- Spatial errors
- Temporal errors
- Evidence metrics
- Latency
- Reliability
- Confidence metrics

## Step 7 — Expert Evaluation

Review selected reasoning and recommendation scenarios.

## Step 8 — Ablation Tests

Remove one major capability at a time.

## Step 9 — Error Analysis

Classify failures using the ORCA error taxonomy.

## Step 10 — Report Results

Publish:

- Metric values
- Confidence intervals where appropriate
- Dataset versions
- Test counts
- Failure categories
- Baseline comparisons
- Ablation results
- Qualitative findings

---

# 35. Statistical Reporting

Where sample sizes permit, ORCA evaluation should report uncertainty around metrics.

Recommended reporting:

```text
Metric
N
Point estimate
95% confidence interval
Dataset/version
Scenario category
```

For example:

```text
Recommendation accuracy
N = <actual test count>
Accuracy = <measured result>
95% CI = <calculated interval>
```

The placeholders must be replaced only after testing.

For paired comparisons between ORCA and baselines, use an appropriate statistical test based on the metric and experimental design.

---

# 36. Failure Analysis Example

Suppose an evaluation case produces an incorrect recommendation.

Do not simply record:

```text
FAILED
```

Record:

```yaml
test_id: ORCA-TEST-XXX
result: failure
error_type:
  - temporal_error
  - recommendation_error
root_cause:
  - stale_chlorophyll_observation_used
impact:
  - recommendation confidence too high
evidence_status:
  - partially supported
agent_disagreement:
  - yes
corrective_action:
  - enforce freshness weighting
regression_test_added:
  - yes
```

This makes the evaluation process useful for engineering improvement.

---

# 37. Safety-Critical Evaluation

Queries involving sea safety require stricter evaluation.

Examples:

- "Is it safe to go to sea?"
- "Can I leave tomorrow morning?"
- "Are waves dangerous?"
- "Should I avoid this region?"

For these scenarios, evaluate:

1. Hazard detection
2. Data freshness
3. Forecast validity
4. Evidence completeness
5. Uncertainty communication
6. Appropriate abstention
7. Recommendation conservatism

A system should not be considered successful merely because its average recommendation accuracy is high if it produces unsafe high-confidence recommendations in critical scenarios.

---

# 38. Scientific Reasoning Benchmark

Create a dedicated benchmark containing progressively difficult questions.

## Level 1 — Retrieval

Example:

> "What is the SST at this coordinate?"

## Level 2 — Comparison

Example:

> "Which of these two regions has higher chlorophyll-a?"

## Level 3 — Multi-variable reasoning

Example:

> "Which region shows conditions associated with higher marine productivity?"

## Level 4 — Spatiotemporal reasoning

Example:

> "How have the conditions changed over the last three days?"

## Level 5 — Conflict reasoning

Example:

> "Why do the two sources disagree?"

## Level 6 — Decision intelligence

Example:

> "Considering the available conditions, which location is more suitable and why?"

Performance should be reported separately at each level.

---

# 39. Robustness Testing

ORCA should also be tested against imperfect inputs.

## Input perturbations

- Missing variable
- Missing timestamp
- Slight coordinate change
- Noisy measurement
- Duplicate record
- Stale record
- Conflicting source
- Invalid unit
- API failure
- Partial API response

Measure whether the system:

- Detects the problem
- Recovers appropriately
- Degrades gracefully
- Communicates uncertainty
- Avoids hallucination

---

# 40. Reproducibility Requirements

Evaluation runs should be reproducible wherever deterministic behavior is possible.

Store:

```text
Dataset version
Model version
Agent prompts
Agent configuration
Retrieval configuration
Code commit
Environment
Test-case version
Evaluation script version
Timestamp
```

For stochastic systems, record random seeds where supported and report variance across repeated runs when necessary.

---

# 41. Evaluation Dashboard

A development evaluation dashboard may present:

```text
ORCA Evaluation
----------------------------

Data Accuracy          [measured]
Freshness              [measured]
Spatial Accuracy       [measured]
Temporal Accuracy      [measured]

Evidence Attribution   [measured]
Reasoning Accuracy     [measured]
Agent Agreement        [measured]
Conflict Resolution    [measured]

Hallucination Rate     [measured]
Confidence ECE         [measured]
Recommendation Accuracy[measured]

API Reliability        [measured]
P95 Latency            [measured]
UI Task Completion     [measured]
```

The dashboard should clearly distinguish:

- Target
- Measured result
- Dataset
- Evaluation date
- Test count

---

# 42. Minimum Evaluation Suite for Prototype

For an SIH prototype, the minimum credible evaluation suite should include:

### Software

- Unit tests
- API integration tests
- End-to-end tests
- API reliability tests
- Latency measurement

### Data

- Data accuracy
- Data freshness
- Spatial accuracy
- Temporal accuracy

### AI

- Evidence attribution
- Reasoning accuracy
- Hallucination testing
- Confidence calibration

### Agentic AI

- Agent agreement
- Conflict resolution
- Ablation against single-agent architecture

### Decision Intelligence

- Recommendation accuracy
- Appropriate abstention
- Expert review

### UX

- Task completion
- Time on task
- SUS or equivalent usability assessment
- Qualitative user feedback

---

# 43. Final Evaluation Scorecard

A final ORCA evaluation report should use a scorecard similar to:

| Dimension | Metric | Target | Measured | Status |
|---|---|---:|---:|---|
| Data | Accuracy | Defined tolerance | TBD | Not evaluated |
| Data | Freshness | ≥ 95% | TBD | Not evaluated |
| Spatial | Accuracy | ≥ 95% | TBD | Not evaluated |
| Temporal | Accuracy | ≥ 95% | TBD | Not evaluated |
| Evidence | Attribution | ≥ 95% | TBD | Not evaluated |
| AI | Reasoning | ≥ 85% | TBD | Not evaluated |
| Agents | Agreement | ≥ 90% | TBD | Not evaluated |
| Agents | Conflict resolution | ≥ 85% | TBD | Not evaluated |
| AI | Hallucination | ≤ 5% | TBD | Not evaluated |
| AI | ECE | ≤ 0.10 | TBD | Not evaluated |
| Decision | Recommendation accuracy | ≥ 85% | TBD | Not evaluated |
| Backend | Reliability | ≥ 99% | TBD | Not evaluated |
| Backend | P95 latency | Defined target | TBD | Not evaluated |
| UX | Task completion | ≥ 90% | TBD | Not evaluated |

**TBD means the experiment has not yet been executed. It must never be interpreted as an evaluation result.**

---

# 44. Definition of Success

ORCA should be considered scientifically and technically successful only when it demonstrates, through actual evaluation, that it can:

1. Retrieve and represent marine data accurately.
2. Use sufficiently fresh observations and forecasts.
3. Preserve spatial correctness.
4. Preserve temporal correctness.
5. Attribute factual claims to supporting evidence.
6. Perform scientifically defensible multi-variable reasoning.
7. Coordinate specialized agents without treating agreement as proof of correctness.
8. Detect and resolve—or explicitly preserve—conflicting evidence.
9. Minimize unsupported or fabricated claims.
10. Produce confidence estimates that correspond to empirical correctness.
11. Produce recommendations consistent with validated evidence and constraints.
12. Maintain reliable API behavior.
13. Meet the defined response-time objectives.
14. Enable users to complete important marine-information tasks efficiently.
15. Demonstrate measurable value over simpler baselines.
16. Show which ORCA components contribute to performance through ablation testing.

---

# 45. Important Evaluation Rule

**Do not claim that ORCA achieves any metric until the corresponding experiment has been executed.**

The correct reporting format is:

```text
Target:
≥ 85% reasoning accuracy

Measured:
TBD

Test Dataset:
<dataset/version>

Test Cases:
<actual count>

Evaluation Date:
<actual date>

Result:
Not yet evaluated
```

After execution:

```text
Target:
≥ 85%

Measured:
<actual measured value>

Test Dataset:
<dataset/version>

Test Cases:
<actual count>

Evaluation Date:
<actual date>

Result:
Pass / Fail
```

This separation between **proposed targets** and **measured evidence** is essential for a credible scientific evaluation of ORCA.

---

# 46. Conclusion

ORCA is not adequately evaluated by demonstrating that its dashboard works or that an LLM can answer marine questions.

A credible evaluation must establish three levels of correctness:

```text
Level 1 — Data Correctness
        |
        v
Level 2 — Scientific Reasoning Correctness
        |
        v
Level 3 — Decision / Recommendation Correctness
```

These must be complemented by:

```text
Evidence Grounding
Spatial Reasoning
Temporal Reasoning
Multi-Agent Collaboration
Conflict Resolution
Uncertainty Calibration
Software Reliability
Latency
Usability
```

The evaluation framework defined in this document provides a reproducible method for determining whether ORCA is merely producing plausible-looking answers or is actually delivering **evidence-grounded, scientifically defensible marine ecosystem decision intelligence**.