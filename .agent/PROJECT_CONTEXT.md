# PROJECT_CONTEXT.md

## ORCA – Marine Ecosystems Reasoning with Collaborative Agents  
**SIH26176 | ISRO | Software | Marine Ecosystems + Earth Observation + AI + Agentic AI + Decision Intelligence**

***

## 1. Project Identity

- **Project Name**: ORCA (Marine Ecosystems Reasoning with Collaborative Agents)
- **SIH Code**: SIH26176
- **Organization**: ISRO (Indian Space Research Organisation)
- **Category**: Software
- **Domain**: Marine Ecosystems, Earth Observation, Artificial Intelligence, Agentic AI, Decision Intelligence
- **Document Type**: Internal Context/Governance Document for AI Coding Agents
- **Version**: 1.0
- **Date**: 31 August 2026

***

## 2. Project Vision

ORCA is an evidence-grounded collaborative marine reasoning platform that integrates heterogeneous marine information through specialized agents to produce explainable decision intelligence.

ORCA does not claim to invent multi-agent AI, RAG, knowledge graphs, marine data, or LLM reasoning. Instead, ORCA applies these established techniques to the specific domain of marine ecosystems, with rigorous scientific validation, source attribution, and safety constraints.

***

## 3. Problem Definition

Marine stakeholders (fishermen, coastal communities, marine researchers, policymakers) face fragmented, heterogeneous, and difficult-to-interpret marine information. Satellite data, ocean models, forecasts, and scientific knowledge exist but are not integrated into actionable, explainable decision intelligence.

***

## 4. Core Problem

Marine decision-making is hindered by:

1. **Data Fragmentation**: Marine data is scattered across multiple sources (satellites, models, in-situ, advisories) with different formats, resolutions, and update cycles.
2. **Interpretation Gap**: Raw data (e.g., SST, chlorophyll) requires scientific expertise to interpret; end-users lack tools to translate data into actionable insights.
3. **Trust Deficit**: Black-box AI predictions without scientific attribution or uncertainty quantification reduce user trust and adoption.
4. **Safety Risks**: Marine operations (fishing, navigation) involve safety-critical decisions; incorrect or overconfident recommendations can endanger lives.
5. **Dynamic Environment**: Marine features (fronts, eddies, PFZ) shift rapidly; static information becomes stale within hours.

***

## 5. Why the Problem Exists

1. **Specialized Data Silos**: Oceanographic data is produced by specialized agencies (ISRO, INCOIS, NASA, NOAA, Copernicus) with different mandates and formats.
2. **Scientific Complexity**: Marine science requires domain expertise; general-purpose AI lacks scientific constraints and validation.
3. **Lack of Integrated Platforms**: Existing tools focus on single parameters (e.g., SST maps) or single use cases (e.g., PFZ advisories) without multi-parameter reasoning.
4. **Explainability Gap**: AI/ML models often produce predictions without traceable evidence, scientific rationale, or uncertainty bounds.
5. **Safety and Liability Concerns**: Marine safety recommendations require conservative handling, official source attribution, and clear disclaimers.

***

## 6. Proposed Solution

ORCA implements a **collaborative multi-agent architecture** where specialized agents handle distinct aspects of marine reasoning:

- **Ocean Agent**: Physical ocean parameters (SST, SSS, SSH, currents, wind, waves, MLD, bathymetry)
- **Ecosystem Agent**: Biological oceanography (chlorophyll-a, primary productivity, phytoplankton, MHW, fronts, upwelling, ecosystem anomalies)
- **Fisheries Agent**: Fisheries science (PFZ, fish habitat indicators, catch probability, species distribution)
- **Safety Agent**: Marine safety (wave height, wind, hazards, high wave alerts, fishing bans)
- **Geospatial Agent**: Spatial analysis (coordinates, resolution, geographic consistency, data coverage)
- **RAG Agent**: Scientific source attribution, literature retrieval, evidence synthesis
- **Verification Agent**: Scientific consistency, source provenance, timestamp, unsupported inference detection
- **Coordinator**: Multi-agent synthesis, evidence combination, traceable output generation

Agents collaborate through a structured reasoning flow: **Observed Data → Model Data → Forecast Data → Derived Indicators → AI Inference → Recommendation**.

***

## 7. Core Innovation

ORCA's innovation lies in:

1. **Domain-Specific Agentic Architecture**: Specialized agents for marine science subdomains, each with scientific constraints and validation rules.
2. **Evidence-Grounded Reasoning**: Every inference is traceable to authoritative sources (ISRO, INCOIS, NASA, NOAA, Copernicus, peer-reviewed literature).
3. **Explainable Decision Intelligence**: Outputs include evidence chain, confidence levels, uncertainty bounds, and source attribution.
4. **Safety-First Design**: Conservative handling of safety-critical recommendations, official source attribution, and clear disclaimers.
5. **Dynamic Temporal Reasoning**: Explicit handling of data freshness, forecast validity, and feature drift (e.g., PFZ shift with wind/currents).

***

## 8. Target Users

1. **Artisanal and Small-Scale Fishermen**: Need PFZ advisories, safety alerts, and interpretable marine information.
2. **Coastal Communities**: Require marine hazard warnings, ecosystem status, and livelihood-related decision support.
3. **Marine Researchers**: Benefit from integrated data access, scientific reasoning, and evidence synthesis.
4. **Policymakers and Managers**: Need ecosystem assessments, safety advisories, and data-driven decision support.
5. **Marine Industry Stakeholders**: Shipping, aquaculture, offshore operations requiring marine forecasts and safety information.

***

## 9. Stakeholders

1. **ISRO**: Project sponsor; provides satellite data (Oceansat, OCM) and technical oversight.
2. **INCOIS**: PFZ advisories, Ocean State Forecasts, High Wave Alerts, marine hazard warnings.
3. **MOSDAC**: Ocean color and SST data archival and distribution.
4. **NASA/NOAA/Copernicus**: Global ocean data products (SST, chlorophyll, SSH, currents, MHW).
5. **End Users**: Fishermen, coastal communities, researchers, policymakers.
6. **SIH Evaluation Panel**: Judges project quality, innovation, and impact.

***

## 10. Primary User Problems

1. **Fishermen**: "Where should I fish today? Is it safe? Will I find fish?"
2. **Coastal Communities**: "Are there marine hazards (cyclones, high waves)? How will ecosystems change?"
3. **Researchers**: "How do I integrate heterogeneous marine data? What does this data mean scientifically?"
4. **Policymakers**: "What is the ecosystem status? Are there safety risks? What actions should we take?"

***

## 11. ORCA's Main Objectives

1. **Integrate Heterogeneous Marine Data**: Combine satellite, model, forecast, and in-situ data into unified reasoning.
2. **Produce Explainable Decision Intelligence**: Generate recommendations with evidence chains, confidence levels, and source attribution.
3. **Ensure Scientific Validity**: Adhere to scientific rules (SCIENTIFIC_RULES.md) for all inferences and recommendations.
4. **Prioritize Safety**: Conservative handling of safety-critical outputs; official source attribution for hazards.
5. **Enable Multi-Agent Collaboration**: Coordinate specialized agents for comprehensive marine reasoning.

***

## 12. MVP Objectives

1. **Demonstrate Core Reasoning Flow**: Observed Data → Derived Indicators → AI Inference → Recommendation.
2. **Implement Key Agents**: Ocean, Ecosystem, Fisheries, Safety, Geospatial, RAG, Verification, Coordinator.
3. **Integrate Authoritative Data Sources**: ISRO/MOSDAC (OCM, SST), INCOIS (PFZ, OSF), NASA/NOAA/Copernicus (SST, chlorophyll, SSH).
4. **Produce Explainable Outputs**: Evidence chain, confidence levels, source attribution for all recommendations.
5. **Validate with Prototype Scenario**: Demonstrate PFZ recommendation with safety alerts and scientific rationale.

***

## 13. MVP Scope

**In Scope**:
- PFZ recommendation for Indian Ocean region (INCOIS coverage)
- SST and chlorophyll integration for front detection
- Ocean State Forecast (wave height, wind) for safety alerts
- High Wave Alert (INCOIS thresholds: Watch 2.5–3.0 m, Alert >3.0 m)
- Marine Heatwave detection (Hobday et al. 2016 criteria: SST > 90th percentile for ≥5 days)
- Geospatial validation (WGS84 coordinates, ocean domain check)
- RAG-based source attribution (ISRO, INCOIS, NASA, NOAA, Copernicus, peer-reviewed literature)
- Verification agent for scientific consistency and timestamp validation
- Coordinator for multi-agent synthesis and traceable output

**Out of Scope (MVP)**:
- Species-specific predictions (e.g., "sardines will be present")
- Subsurface oceanography (e.g., temperature at 50 m depth)
- Real-time data ingestion (use near-real-time or retrospective data)
- Mobile app deployment (web-based prototype only)
- User authentication and personalization
- Multi-language support (English only for MVP)
- Historical trend analysis (focus on current/near-future conditions)

***

## 14. Out-of-Scope Items

1. **Species-Specific Catch Predictions**: MVP does not predict specific species abundance without validated models.
2. **Subsurface Oceanography**: ORCA MVP uses surface data (SST, chlorophyll, SSH); subsurface inference is out of scope.
3. **Real-Time Data Ingestion**: MVP uses near-real-time or retrospective data; real-time streaming is future scope.
4. **Mobile App Deployment**: MVP is web-based; mobile app is future scope.
5. **User Authentication**: MVP does not implement user accounts or personalization.
6. **Multi-Language Support**: MVP is English-only; regional languages are future scope.
7. **Historical Trend Analysis**: MVP focuses on current/near-future conditions; long-term trends are future scope.
8. **Commercial Fishing Fleet Integration**: MVP targets artisanal/small-scale fishermen; industrial fleet features are future scope.

***

## 15. Core ORCA Capabilities

1. **Multi-Parameter Integration**: Combine SST, chlorophyll, SSH, wind, waves, bathymetry for comprehensive reasoning.
2. **Feature Detection**: Identify ocean fronts, eddies, upwelling, marine heatwaves from satellite data.
3. **PFZ Generation**: Integrate SST + chlorophyll to delineate Potential Fishing Zones (INCOIS methodology).
4. **Safety Alerts**: Generate High Wave Alerts (INCOIS thresholds) and marine hazard warnings.
5. **Explainable Outputs**: Provide evidence chains, confidence levels, and source attribution for all recommendations.
6. **Geospatial Validation**: Ensure coordinates are within ocean domain; respect data resolution and coverage.
7. **Temporal Reasoning**: Handle data freshness, forecast validity, and feature drift (e.g., PFZ shift with wind/currents).
8. **Scientific Validation**: Adhere to SCIENTIFIC_RULES.md for all inferences and recommendations.

***

## 16. Core Agents

1. **Ocean Agent**
2. **Ecosystem Agent**
3. **Fisheries Agent**
4. **Safety Agent**
5. **Geospatial Agent**
6. **RAG Agent**
7. **Verification Agent**
8. **Coordinator**

***

## 17. Responsibility of Each Agent

### 17.1 Ocean Agent

- **Purpose**: Process physical ocean parameters (SST, SSS, SSH, currents, wind, waves, MLD, bathymetry).
- **Inputs**: Satellite SST (AVHRR, MODIS), SSS (Copernicus), SSH (altimetry), currents (model), wind/waves (INCOIS OSF), MLD (model), bathymetry (GEBCO).
- **Data Sources**: ISRO/MOSDAC, INCOIS, NASA, NOAA, Copernicus, GEBCO.
- **Processing**: Validate data quality, detect gradients (fronts), compute anomalies (MHW), interpolate/aggregate to common resolution.
- **Expected Output**: Physical ocean indicators (e.g., "SST gradient = 2°C/10 km indicates front"; "Hs = 3.2 m triggers High Wave Alert").
- **Dependencies**: Geospatial Agent (coordinate validation), RAG Agent (source attribution), Verification Agent (consistency check).
- **Must NOT Assume**: Biological state from physical parameters alone (e.g., "High SST = low fish"); subsurface conditions from surface data.
- **Consumed By**: Coordinator (synthesizes with Ecosystem, Fisheries, Safety outputs).

### 17.2 Ecosystem Agent

- **Purpose**: Process biological oceanography parameters (chlorophyll-a, primary productivity, phytoplankton, MHW, fronts, upwelling, ecosystem anomalies).
- **Inputs**: Chlorophyll (OCM, MODIS), primary productivity (model), phytoplankton (inferred from chlorophyll), MHW (SST anomaly), fronts (SST/chlorophyll gradients), upwelling (cold SST + high chlorophyll), ecosystem anomalies (deviation from climatology).
- **Data Sources**: ISRO/MOSDAC (OCM), NASA (MODIS), Copernicus (chlorophyll, productivity), NOAA (MHW), INCOIS (fronts, upwelling).
- **Processing**: Validate quality flags, detect blooms, compute MHW (Hobday criteria), identify fronts/upwelling, compare to climatology.
- **Expected Output**: Ecosystem indicators (e.g., "Chlorophyll = 2 mg/m³ indicates elevated biomass"; "MHW detected: SST > 90th percentile for 7 days").
- **Dependencies**: Ocean Agent (SST for MHW, fronts), Geospatial Agent (coordinate validation), RAG Agent (source attribution), Verification Agent (consistency check).
- **Must NOT Assume**: Chlorophyll alone predicts fish abundance; coastal algorithm accuracy without quality flag check.
- **Consumed By**: Coordinator (synthesizes with Ocean, Fisheries, Safety outputs).

### 17.3 Fisheries Agent

- **Purpose**: Process fisheries science parameters (PFZ, fish habitat indicators, catch probability, species distribution).
- **Inputs**: SST, chlorophyll, fronts, bathymetry, currents, wind (for PFZ drift), PFZ advisories (INCOIS).
- **Data Sources**: INCOIS (PFZ), ISRO/MOSDAC (OCM, SST), NASA (MODIS), Copernicus (currents, bathymetry).
- **Processing**: Integrate SST + chlorophyll for PFZ (INCOIS methodology), validate against bathymetry, estimate drift using wind/currents, compute habitat suitability.
- **Expected Output**: PFZ coordinates, habitat indicators (e.g., "PFZ at 12°N, 78°E; may reduce search time for pelagic species"), catch probability (probabilistic, not deterministic).
- **Dependencies**: Ocean Agent (SST, currents, wind), Ecosystem Agent (chlorophyll, fronts), Geospatial Agent (coordinate validation), Safety Agent (fishing ban check), RAG Agent (source attribution), Verification Agent (consistency check).
- **Must NOT Assume**: PFZ guarantees catch; species-specific presence without validation; PFZ validity beyond 24–48 hours.
- **Consumed By**: Coordinator (synthesizes with Ocean, Ecosystem, Safety outputs for final recommendation).

### 17.4 Safety Agent

- **Purpose**: Process marine safety parameters (wave height, wind, hazards, high wave alerts, fishing bans).
- **Inputs**: Wave height (INCOIS OSF), wind (OSF), marine hazards (cyclones, tsunamis), fishing ban notifications.
- **Data Sources**: INCOIS (OSF, High Wave Alert, hazard warnings), IMD (cyclones), NOAA (tsunamis).
- **Processing**: Check wave height against thresholds (Watch 2.5–3.0 m, Alert >3.0 m), validate hazard warnings, check fishing ban status.
- **Expected Output**: Safety alerts (e.g., "High Wave Alert: Hs > 3.0 m; small vessels should exercise caution"), fishing ban notifications.
- **Dependencies**: Ocean Agent (wind, waves), Geospatial Agent (coordinate validation), RAG Agent (source attribution), Verification Agent (timestamp check).
- **Must NOT Assume**: Guaranteed safety or unsafe conditions; override official warnings; generate independent hazard predictions.
- **Consumed By**: Coordinator (integrates safety alerts into final recommendation; suspends PFZ during bans/hazards).

### 17.5 Geospatial Agent

- **Purpose**: Validate spatial aspects (coordinates, resolution, geographic consistency, data coverage).
- **Inputs**: Coordinates (lat/lon), data resolution, coverage masks, land/sea masks.
- **Data Sources**: GEBCO (bathymetry, land/sea mask), ISRO/MOSDAC (data coverage), Copernicus (coverage flags).
- **Processing**: Validate WGS84 coordinates, check ocean domain (not land), respect native resolution, flag coastal contamination, check data gaps (clouds, sun glint).
- **Expected Output**: Geospatial validation (e.g., "Coordinates 12°N, 78°E are within Indian Ocean; chlorophyll data available at 1 km resolution; quality flag: good").
- **Dependencies**: Ocean Agent (data resolution), Ecosystem Agent (coastal algorithm flags), RAG Agent (source attribution).
- **Must NOT Assume**: Sub-grid features (e.g., 100 m precision from 4 km data); data availability without coverage check.
- **Consumed By**: All agents (coordinate validation before processing); Coordinator (final output includes geospatial metadata).

### 17.6 RAG Agent

- **Purpose**: Retrieve and attribute scientific sources (ISRO, INCOIS, NASA, NOAA, Copernicus, peer-reviewed literature).
- **Inputs**: Query (e.g., "PFZ methodology", "MHW definition"), context (agent outputs).
- **Data Sources**: ISRO/MOSDAC documentation, INCOIS technical reports, NASA/NOAA product guides, Copernicus PUMs, peer-reviewed papers (Hobday et al. 2016, etc.).
- **Processing**: Retrieve relevant documents, extract key information (definitions, methodologies, thresholds), format citations.
- **Expected Output**: Source attribution (e.g., "PFZ methodology: INCOIS "; "MHW definition: Hobday et al. 2016 "). [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Dependencies**: External knowledge base (SCIENTIFIC_RULES.md references), Verification Agent (citation validation).
- **Must NOT Assume**: Unverified sources (blogs, social media); invent citations; use outdated references.
- **Consumed By**: All agents (source attribution for outputs); Coordinator (final output includes citations).

### 17.7 Verification Agent

- **Purpose**: Validate scientific consistency, source provenance, timestamp, unsupported inference detection.
- **Inputs**: Agent outputs (Ocean, Ecosystem, Fisheries, Safety, Geospatial, RAG), SCIENTIFIC_RULES.md.
- **Data Sources**: SCIENTIFIC_RULES.md, agent outputs, data provenance metadata.
- **Processing**: Check scientific consistency (e.g., SST + chlorophyll agree on front), verify source provenance, validate timestamps, flag unsupported inferences.
- **Expected Output**: Validation report (e.g., "PFZ inference validated: SST + chlorophyll integration per INCOIS methodology; timestamp: 31 Aug 2026 (fresh); quality flags: good").
- **Dependencies**: All agents (outputs to validate), SCIENTIFIC_RULES.md (validation criteria).
- **Must NOT Assume**: Scientific validity without check; ignore timestamp or quality flag issues.
- **Consumed By**: Coordinator (uses validation report to adjust confidence or reject invalid inferences).

### 17.8 Coordinator

- **Purpose**: Synthesize multi-agent outputs into traceable, explainable decision intelligence.
- **Inputs**: Ocean, Ecosystem, Fisheries, Safety, Geospatial, RAG, Verification agent outputs.
- **Data Sources**: Aggregated agent outputs, SCIENTIFIC_RULES.md, PROJECT_CONTEXT.md.
- **Processing**: Combine evidence, resolve conflicts, propagate uncertainty, generate evidence chain (Observation → Indicator → Interpretation → Inference → Recommendation), assign confidence levels.
- **Expected Output**: Final recommendation (e.g., "PFZ at 12°N, 78°E; may reduce search time for pelagic species; High Wave Alert: Hs > 3.0 m ; confidence: medium (chlorophyll cloud gaps)"). [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Dependencies**: All agents (outputs to synthesize), Verification Agent (validation report), SCIENTIFIC_RULES.md (confidence policy).
- **Must NOT Assume**: Invent scientific relationships; collapse evidence chain; ignore safety alerts or verification flags.
- **Consumed By**: End user (final output); logging/audit trail (for post-hoc analysis).

***

## 18. Agent Collaboration Model

Agents collaborate through a **structured reasoning flow**:

1. **Observed Data**: Satellite/measured data (SST, chlorophyll, SSH, wind, waves) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **Model Data**: Derived/modelled data (currents, MLD, primary productivity) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf)
3. **Forecast Data**: Predicted future state (OSF wave/wind forecast, PFZ drift) 
4. **Derived Indicators**: Scientific features (fronts, eddies, MHW, PFZ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
5. **AI Inference**: Probabilistic interpretation (habitat suitability, catch probability, safety risk) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
6. **Recommendation**: Actionable guidance (target PFZ, exercise caution, monitor updates) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Flow**:
- Ocean/Ecosystem/Fisheries/Safety Agents process Observed/Model/Forecast Data → Derived Indicators
- Verification Agent validates consistency, provenance, timestamp
- RAG Agent attributes sources
- Coordinator synthesizes → AI Inference → Recommendation
- Geospatial Agent validates coordinates throughout

**Conflict Resolution**:
- If agents disagree (e.g., SST indicates front, chlorophyll does not), Coordinator reduces confidence and flags discrepancy.
- If Safety Agent issues alert (e.g., High Wave), Coordinator prioritizes safety over fisheries recommendation.

***

## 19. Data Sources and Dataset Categories

### 19.1 Primary Data Sources

1. **ISRO/MOSDAC**: Oceansat-2 OCM chlorophyll, SST [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **INCOIS**: PFZ advisories, Ocean State Forecast (wave, wind), High Wave Alerts, marine hazards [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
3. **NASA**: MODIS SST, chlorophyll, SSH [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
4. **NOAA**: AVHRR SST, marine heatwave monitoring [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
5. **Copernicus Marine Service**: Global ocean reanalysis (SST, chlorophyll, SSH, currents, SSS, productivity) [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
6. **GEBCO**: Bathymetry, land/sea mask 

### 19.2 Dataset Categories

- **Observation**: Satellite/measured data (SST, chlorophyll, SSH, wind, waves)
- **Model**: Derived/modelled data (currents, MLD, productivity, SSS)
- **Forecast**: Predicted future state (OSF wave/wind, PFZ drift)
- **Climatology**: Long-term baseline (30-year SST climatology for MHW) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- **Advisories**: PFZ, High Wave Alert, marine hazard warnings [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 20. Scientific Domains Covered

1. **Physical Oceanography**: SST, SSS, SSH, currents, wind, waves, MLD, bathymetry [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **Biological Oceanography**: Chlorophyll-a, primary productivity, phytoplankton, fronts, upwelling, MHW, ecosystem anomalies [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
3. **Fisheries Science**: PFZ, fish habitat indicators, catch probability, species distribution [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
4. **Marine Safety**: Wave height, wind, hazards, high wave alerts, fishing bans [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
5. **Geospatial Science**: Coordinates, resolution, geographic consistency, data coverage [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 21. Major Marine Parameters

| Parameter | Representation | Unit | Indicates | Cannot Prove | Spatial/Temporal Considerations | ORCA Use |
|-----------|---------------|------|-----------|--------------|-------------------------------|----------|
| **SST** | Sea surface temperature | °C | Thermal structure, fronts, MHW  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | Fish abundance, subsurface conditions  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | 1–4 km resolution, daily to weekly; diurnal warming, cloud gaps  [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1) | Front detection, MHW, PFZ (with chlorophyll)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Chlorophyll-a** | Phytoplankton pigment concentration | mg/m³ | Phytoplankton biomass, productivity  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | Fish abundance, species composition  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | 1 km (OCM) to 4 km (MODIS); cloud/sun glint contamination; coastal algorithm uncertainty  [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full) | PFZ (with SST), front detection, bloom monitoring  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **SSH** | Sea surface height anomaly | m/cm | Currents, eddies, upwelling  [swot.jpl.nasa](https://swot.jpl.nasa.gov/system/documents/files/2244_2244_D-75724_SWOT_Cal_Val_Plan_Initial_20180129u.pdf) | Biological productivity, fish distribution  | 1/12° to 1/4° (~9–25 km); 10–35 day repeat cycle  | Eddy detection, current boundaries, upwelling signatures  |
| **Currents** | Water velocity (speed + direction) | m/s or cm/s | Transport pathways, PFZ drift, nutrient advection  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | Fish location at specific time, subsurface currents  | 1/12° to 1/4° resolution; 5–7 day forecast horizon  | PFZ drift prediction, transport pathways  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Wind** | Surface wind velocity (10 m) | m/s or km/h | Wave generation, upwelling forcing, PFZ drift  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | Subsurface conditions, fish behavior  | 10–25 km resolution; 5–7 day forecast  | PFZ drift, high wave alerts, upwelling identification  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Wave Height (Hs)** | Significant wave height | m | Sea state severity, navigation safety  | Individual wave height, coastal inundation  | 10–25 km resolution; 5–7 day forecast; validated against buoys/altimeters  | High Wave Alert (INCOIS thresholds), safety advisories  |
| **MLD** | Mixed layer depth | m | Nutrient supply potential, stratification, MHW vertical structure  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) | Exact nutrient concentration, fish distribution  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) | Model-derived: 1/12° to 1/4°; seasonal to interannual variability  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) | Ecosystem productivity interpretation, MHW vertical structure  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) |
| **Bathymetry** | Ocean depth | m | Fishing ground depth, habitat type, upwelling potential  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | Fish presence, current patterns  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | GEBCO 15 arc-sec (~450 m); static (no temporal change)  | Filter PFZ by depth, identify shelf breaks/seamounts  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |

***

## 22. AI/ML Concepts Used

1. **Multi-Agent Systems**: Specialized agents for marine subdomains (Ocean, Ecosystem, Fisheries, Safety, Geospatial, RAG, Verification, Coordinator).
2. **Retrieval-Augmented Generation (RAG)**: Scientific source attribution, literature retrieval, evidence synthesis. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
3. **Knowledge Graphs**: Structured representation of marine parameters, relationships, and scientific rules (SCIENTIFIC_RULES.md).
4. **LLM Reasoning**: Natural language generation for explainable outputs, evidence chain articulation.
5. **Confidence Calibration**: Assign confidence levels (High/Medium/Low/Insufficient) based on data quality, evidence level, parameter agreement. [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
6. **Uncertainty Propagation**: Propagate measurement, algorithmic, and interpretive uncertainty through inference chain. [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
7. **Geospatial AI**: Coordinate validation, resolution awareness, geographic consistency checks. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
8. **Temporal Reasoning**: Data freshness, forecast validity, feature drift handling. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Note**: ORCA does not claim to invent these AI/ML concepts; it applies them to marine decision intelligence with scientific constraints.

***

## 23. RAG / Knowledge Architecture

### 23.1 Knowledge Base

- **SCIENTIFIC_RULES.md**: Authoritative scientific rules, parameter definitions, inference constraints, confidence policy, red flags.
- **PROJECT_CONTEXT.md**: This document (project identity, vision, architecture, agent responsibilities, data sources).
- **ARCHITECTURE_RULES.md**: Technical architecture, component interactions, deployment guidelines.
- **CODING_RULES.md**: Coding standards, best practices, testing requirements.
- **WORKFLOW.md**: Development workflow, git practices, CI/CD pipeline.

### 23.2 RAG Agent Workflow

1. **Query**: Agent receives query (e.g., "PFZ methodology", "MHW definition").
2. **Retrieve**: Search knowledge base (SCIENTIFIC_RULES.md, authoritative references) for relevant documents.
3. **Extract**: Extract key information (definitions, methodologies, thresholds, citations).
4. **Attribute**: Format citations (source, year, DOI/URL) per SCIENTIFIC_RULES.md Section 13.2.
5. **Return**: Provide source attribution to requesting agent.

### 23.3 Knowledge Graph Structure

- **Nodes**: Marine parameters (SST, chlorophyll, SSH, etc.), scientific features (fronts, eddies, MHW, PFZ), agents (Ocean, Ecosystem, etc.), data sources (ISRO, INCOIS, NASA, etc.).
- **Edges**: Relationships (e.g., "SST + chlorophyll → PFZ", "SST > 90th percentile for ≥5 days → MHW", "PFZ → higher catch probability").
- **Constraints**: Scientific rules (SCIENTIFIC_RULES.md) govern valid relationships (e.g., "Chlorophyll alone cannot predict fish abundance").

***

## 24. Geospatial Capabilities

1. **Coordinate Validation**: WGS84 (EPSG:4326) lat/lon; reject land coordinates, flag out-of-coverage areas. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **Resolution Awareness**: Respect native data resolution (1 km chlorophyll, 4 km SST, 1/12° SSH); do not infer sub-grid features. [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)
3. **Geographic Consistency**: Use region-appropriate products (INCOIS for Indian Ocean, Copernicus for global); flag coastal contamination. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
4. **Data Coverage Check**: Validate data availability (cloud gaps, sun glint, polar night); flag missing data .
5. **Spatial Interpolation**: Aggregate/interpolate datasets to common resolution when combining (e.g., SST + chlorophyll for PFZ). [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 25. Reasoning and Decision-Intelligence Flow

**Structured Flow**:

1. **Observed Data**: Satellite/measured data (SST, chlorophyll, SSH, wind, waves) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **Model Data**: Derived/modelled data (currents, MLD, productivity, SSS) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf)
3. **Forecast Data**: Predicted future state (OSF wave/wind forecast, PFZ drift) 
4. **Derived Indicators**: Scientific features (fronts, eddies, MHW, PFZ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
5. **AI Inference**: Probabilistic interpretation (habitat suitability, catch probability, safety risk) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
6. **Recommendation**: Actionable guidance (target PFZ, exercise caution, monitor updates) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example**:

- **Observed Data**: SST = 28°C, chlorophyll = 2 mg/m³ at 12°N, 78°E (INCOIS, 31 Aug 2026) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Derived Indicator**: SST gradient + chlorophyll gradient indicate ocean front [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- **Scientific Interpretation**: Fronts are associated with enhanced productivity and fish aggregation [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- **AI Inference**: PFZ delineated at front location; higher probability of pelagic fish presence [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Recommendation**: Target PFZ zone; use wind vectors to estimate drift; PFZ reduces search time but does not guarantee catch [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 26. Evidence and Source Attribution

**Every scientific claim must cite**:
- **Source**: Agency, paper, product (e.g., "INCOIS PFZ", "Hobday et al. 2016")
- **Year/Version**: Publication year or product version
- **DOI/URL**: Where available

**Example**:
- "Marine heatwaves are defined as SST > 90th percentile for ≥5 days  (Hobday et al. 2016, DOI: 10.1038/nclimate2935)" [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- "PFZ advisories use SST from NOAA-AVHRR and chlorophyll from Oceansat-2 OCM  (INCOIS, 2026)" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Evidence Hierarchy** (SCIENTIFIC_RULES.md Section 13.1):
- **Level 1**: Peer-reviewed meta-analysis / operational validation (e.g., INCOIS PFZ validation ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Level 2**: Single peer-reviewed study / government technical report (e.g., INCOIS technical reports ) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- **Level 3**: Consensus scientific definition (e.g., Hobday et al. 2016 MHW definition ) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- **Level 4**: Expert judgment / preliminary research (flag as preliminary)
- **Level 5**: Anecdotal / unverified (do not use as scientific evidence)

***

## 27. Confidence and Uncertainty

### 27.1 Confidence Levels (SCIENTIFIC_RULES.md Section 20.1)

| Confidence | Criteria | ORCA Action |
|------------|----------|-------------|
| **High** | Level 1–2 evidence; all parameters agree; data quality good; fresh (<24 hours); spatial consistency good | Strong recommendation (e.g., "PFZ likely to improve catch efficiency"  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)) |
| **Medium** | Level 2–3 evidence; most parameters agree; data quality acceptable; fresh (24–48 hours); minor spatial issues | Advisory with caveats (e.g., "PFZ may improve catch; confidence reduced due to cloud gaps"  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)) |
| **Low** | Level 3–4 evidence; parameters disagree; data quality reduced; stale (>48 hours); spatial issues (coastal contamination) | Informational only (e.g., "SST suggests front; chlorophyll unavailable; confidence low"  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)) |
| **Insufficient Evidence** | Level 4–5 evidence; critical data missing; conflicting sources; unvalidated inference | Do not infer; state "Insufficient authoritative evidence – do not infer"  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |

**DO NOT assign arbitrary percentages** (e.g., "70% confidence") unless implementation has validated methodology. [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

### 27.2 Uncertainty Types (SCIENTIFIC_RULES.md Section 12.1)

- **Measurement Uncertainty**: Sensor noise, calibration error (e.g., SST ±0.5°C) [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)
- **Algorithm Uncertainty**: Retrieval algorithm error (e.g., chlorophyll in coastal waters ±30%) [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
- **Representativeness Uncertainty**: Satellite footprint vs. in-situ point [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)
- **Temporal Uncertainty**: Latency, compositing period [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)
- **Interpretive Uncertainty**: Scientific inference from data (e.g., PFZ → fish probability) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**ORCA Must**:
- Propagate uncertainty through inference chain
- Communicate key uncertainties to user (e.g., "Chlorophyll uncertainty: ±30% in coastal waters" ) [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
- Reduce confidence when uncertainty compounds

***

## 28. Safety Constraints

1. **No Guaranteed Safety**: ORCA must not claim guaranteed fishing or navigation safety .
2. **Official Source Attribution**: Safety outputs must cite source (INCOIS, IMD, NOAA), timestamp, forecast/observation status, uncertainty .
3. **Conservative Handling**: Use INCOIS High Wave Alert thresholds (Watch 2.5–3.0 m, Alert >3.0 m); advise caution, not prohibition .
4. **Suspend PFZ During Hazards**: During marine fishing ban or adverse sea state (cyclones, high waves, tsunamis), PFZ service is suspended. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
5. **Prioritize Official Warnings**: ORCA must not override or contradict official hazard warnings (INCOIS, IMD, NOAA). [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Safety Output Format**:
- **Source**: "INCOIS Ocean State Forecast"
- **Timestamp**: "Issued 31 Aug 2026, valid 31 Aug – 5 Sep 2026"
- **Forecast/Observation Status**: "5-day forecast, daily update"
- **Uncertainty**: "Wave height forecast uncertainty: ±0.5 m"
- **Disclaimer**: "ORCA does not guarantee fishing or navigation safety; consult official advisories and local conditions"

***

## 29. Expected User Experience

1. **Input**: User provides location (lat/lon) and query (e.g., "Where should I fish?", "Is it safe?").
2. **Processing**: ORCA agents process data, validate scientifically, synthesize evidence.
3. **Output**: Explainable recommendation with:
   - **Evidence Chain**: Observation → Indicator → Interpretation → Inference → Recommendation
   - **Confidence Level**: High/Medium/Low/Insufficient
   - **Source Attribution**: Citations (ISRO, INCOIS, NASA, NOAA, Copernicus, peer-reviewed literature)
   - **Uncertainty Bounds**: Key uncertainties (e.g., "Chlorophyll uncertainty: ±30% in coastal waters")
   - **Safety Alerts**: High Wave Alert, fishing ban notifications (if applicable)
   - **Actionable Guidance**: "Target PFZ at 12°N, 78°E; use wind vectors to estimate drift; exercise caution due to high waves"

**Example Output**:
```
PFZ Recommendation:
- Location: 12°N, 78°E
- Rationale: SST gradient + chlorophyll gradient indicate ocean front  [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/AVHRR_PATHFINDER_L3_SST_MONTHLY_DAYTIME_V5); fronts associated with enhanced productivity and fish aggregation  [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/AVHRR_PATHFINDER_L3_SST_MONTHLY_DAYTIME_V5)
- Evidence: INCOIS PFZ methodology (SST + chlorophyll integration)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory); validation studies show reduced search time for pelagic species  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Confidence: Medium (chlorophyll cloud gaps reduce data quality)
- Uncertainty: Chlorophyll uncertainty: ±30% in coastal waters [41]; PFZ may shift 10–20 km/day with wind  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Safety: High Wave Alert: Hs > 3.0 m (INCOIS OSF, issued 31 Aug 2026, valid 31 Aug – 5 Sep 2026; uncertainty ±0.5 m)  [coralreefwatch.noaa](https://coralreefwatch.noaa.gov/product/marine_heatwave/); small vessels should exercise caution
- Recommendation: Target PFZ zone; use wind vectors to estimate drift; PFZ reduces search time but does not guarantee catch  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory); monitor safety updates
```

***

## 30. Prototype Demonstration Scenario

**Scenario**: Fisherman queries ORCA for fishing location and safety status off Kerala coast.

**Input**:
- Location: 12°N, 78°E (off Kerala coast)
- Query: "Where should I fish today? Is it safe?"

**ORCA Processing**:
1. **Geospatial Agent**: Validates coordinates (12°N, 78°E) are within Indian Ocean; checks data coverage (OCM, AVHRR available).
2. **Ocean Agent**: Retrieves SST (28°C, AVHRR), SSH (0.1 m anomaly, Copernicus), wind (5 m/s NE, INCOIS OSF), waves (Hs = 3.2 m, INCOIS OSF).
3. **Ecosystem Agent**: Retrieves chlorophyll (2 mg/m³, OCM), detects SST + chlorophyll gradient (front), checks MHW (no MHW detected).
4. **Fisheries Agent**: Integrates SST + chlorophyll for PFZ (INCOIS methodology), validates against bathymetry (50 m depth, suitable for pelagic), estimates drift (10 km east with wind).
5. **Safety Agent**: Checks wave height (Hs = 3.2 m > 3.0 m → High Wave Alert), checks fishing ban (no ban).
6. **RAG Agent**: Attributes sources (INCOIS PFZ, Hobday MHW, INCOIS OSF ). [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
7. **Verification Agent**: Validates consistency (SST + chlorophyll agree on front), timestamp (fresh: 31 Aug 2026), quality flags (good, no sun glint/clouds).
8. **Coordinator**: Synthesizes outputs, assigns confidence (Medium: chlorophyll cloud gaps), generates evidence chain, produces recommendation.

**Output**:
```
PFZ Recommendation:
- Location: 12°N, 78°E (may shift 10 km east with wind)
- Rationale: SST gradient + chlorophyll gradient indicate ocean front  [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/AVHRR_PATHFINDER_L3_SST_MONTHLY_DAYTIME_V5); fronts associated with enhanced productivity and fish aggregation  [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/AVHRR_PATHFINDER_L3_SST_MONTHLY_DAYTIME_V5)
- Evidence: INCOIS PFZ methodology (SST + chlorophyll integration)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory); validation studies show reduced search time for pelagic species  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Confidence: Medium (chlorophyll cloud gaps reduce data quality)
- Uncertainty: Chlorophyll uncertainty: ±30% in coastal waters [41]; PFZ may shift 10–20 km/day with wind  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Safety: High Wave Alert: Hs > 3.0 m (INCOIS OSF, issued 31 Aug 2026, valid 31 Aug – 5 Sep 2026; uncertainty ±0.5 m)  [coralreefwatch.noaa](https://coralreefwatch.noaa.gov/product/marine_heatwave/); small vessels should exercise caution
- Recommendation: Target PFZ zone; use wind vectors to estimate drift; PFZ reduces search time but does not guarantee catch  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory); monitor safety updates
```

***

## 31. Success Criteria

1. **Scientific Validity**: All inferences adhere to SCIENTIFIC_RULES.md; no prohibited claims (e.g., "PFZ guarantees catch").
2. **Explainability**: Outputs include evidence chain, confidence levels, source attribution, uncertainty bounds.
3. **Safety Compliance**: Safety alerts use official sources (INCOIS, IMD, NOAA); no guaranteed safety claims.
4. **Multi-Agent Collaboration**: Agents collaborate through structured reasoning flow; Coordinator synthesizes traceable outputs.
5. **Prototype Demonstration**: MVP demonstrates PFZ recommendation with safety alerts and scientific rationale for Indian Ocean region.
6. **User Trust**: Outputs are interpretable by end users (fishermen, coastal communities); source attribution builds credibility.

***

## 32. Known Limitations

1. **Species-Specific Predictions**: MVP does not predict specific species abundance without validated models.
2. **Subsurface Oceanography**: ORCA MVP uses surface data only; subsurface inference is out of scope.
3. **Real-Time Data Ingestion**: MVP uses near-real-time or retrospective data; real-time streaming is future scope.
4. **Coastal Algorithm Uncertainty**: Chlorophyll algorithms have substantial uncertainties in optically complex coastal waters. [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
5. **Data Gaps**: Cloud contamination, sun glint, polar night create data gaps; ORCA must flag missing data.
6. **PFZ Validity**: PFZ is valid for 24–48 hours; features shift with wind/currents. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
7. **Confidence Calibration**: MVP uses qualitative confidence (High/Medium/Low/Insufficient); quantitative probabilities require validated methodology. [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

***

## 33. Future Scope

1. **Species-Specific Models**: Integrate validated species distribution models for targeted predictions.
2. **Subsurface Data Integration**: Incorporate Argo floats, model reanalysis for subsurface temperature, salinity, oxygen.
3. **Real-Time Data Ingestion**: Implement streaming data pipelines for real-time satellite/model data.
4. **Mobile App Deployment**: Develop mobile app for fishermen (offline support, regional languages).
5. **User Personalization**: User accounts, historical queries, personalized recommendations.
6. **Multi-Language Support**: Regional languages (Malayalam, Tamil, Hindi, etc.) for broader accessibility.
7. **Historical Trend Analysis**: Long-term ecosystem trends, climate change impacts.
8. **Commercial Fleet Integration**: Features for industrial fishing fleets (route optimization, catch forecasting).
9. **Quantitative Confidence Calibration**: Implement validated methodology for probabilistic confidence (e.g., cross-validation, Bayesian calibration).
10. **Expanded Geographic Coverage**: Beyond Indian Ocean (global coverage using Copernicus, NASA, NOAA).

***

## 34. Important Terminology

- **PFZ (Potential Fishing Zone)**: Areas with oceanographic features (fronts, eddies, upwelling) favorable for pelagic fish aggregation; derived from SST + chlorophyll integration (INCOIS methodology). [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **MHW (Marine Heatwave)**: Prolonged discrete anomalously warm water event; defined as SST > 90th percentile for ≥5 days (Hobday et al. 2016). [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- **OSF (Ocean State Forecast)**: INCOIS forecast of wave height, wind, swell for 5–7 days .
- **High Wave Alert**: INCOIS safety alert; Watch (Hs 2.5–3.0 m), Alert (Hs > 3.0 m) .
- **SST (Sea Surface Temperature)**: Temperature of ocean surface layer (skin or bulk); indicates thermal structure, fronts, MHW. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Chlorophyll-a**: Concentration of chlorophyll pigment in phytoplankton; proxy for phytoplankton biomass. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **SSH (Sea Surface Height)**: Height of sea surface relative to reference ellipsoid; indicates currents, eddies, upwelling. [swot.jpl.nasa](https://swot.jpl.nasa.gov/system/documents/files/2244_2244_D-75724_SWOT_Cal_Val_Plan_Initial_20180129u.pdf)
- **MLD (Mixed Layer Depth)**: Depth of surface ocean layer with uniform temperature/salinity; indicates nutrient supply potential. [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf)
- **Front**: Boundary between water masses with different properties (SST, chlorophyll); indicates enhanced productivity. [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- **Upwelling**: Vertical transport of cold, nutrient-rich subsurface water to surface; indicates enhanced productivity. [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- **Evidence Chain**: Structured reasoning flow: Observation → Derived Indicator → Scientific Interpretation → AI Inference → Recommendation.
- **Confidence Level**: Qualitative measure (High/Medium/Low/Insufficient) of inference reliability based on data quality, evidence level, parameter agreement. [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)

***

## 35. Authoritative References

1. **ISRO/MOSDAC**: Oceansat-2 OCM chlorophyll, SST. URL: https://www.mosdac.gov.in [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **INCOIS**: PFZ advisories, Ocean State Forecast, High Wave Alerts. URL: https://incois.gov.in [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
3. **NASA**: MODIS SST, chlorophyll, SSH. URL: https://earthdata.nasa.gov [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
4. **NOAA**: AVHRR SST, marine heatwave monitoring. URL: https://www.noaa.gov [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
5. **Copernicus Marine Service**: Global ocean reanalysis (SST, chlorophyll, SSH, currents, SSS, productivity). URL: https://marine.copernicus.eu [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
6. **GEBCO**: Bathymetry, land/sea mask. URL: https://www.gebco.net 
7. **Hobday et al. 2016**: "A hierarchical approach to defining marine heatwaves". DOI: 10.1038/nclimate2935 (verify) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
8. **Hobday et al. 2018**: "Longer and more frequent marine heatwaves over the past century". DOI: 10.1038/s41467-018-03732-9 (verify) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf)
9. **INCOIS Technical Reports**: "Integrated Potential Fishing Zone Forecasts", "Methodology for PFZ generation". URL: https://incois.gov.in/documents/ResearchPapers/ [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
10. **PFZ Validation Studies**: "The Validation of Potential Fishing Zone Advisories", "Potential fishing zone (PFZ) advisories-Are they beneficial to the coastal fisherfolk?" [ijarsct.co](https://ijarsct.co.in/Paper10524.pdf)
11. **Ocean Color Quality**: "Copernicus GlobColour processor", "A Review and Assessment of Copernicus Water Quality..." [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)

***

## AI AGENT INSTRUCTION

**Any AI coding agent working on ORCA must read and follow this document together with**:

- **ARCHITECTURE_RULES.md**: Technical architecture, component interactions, deployment guidelines.
- **CODING_RULES.md**: Coding standards, best practices, testing requirements.
- **SCIENTIFIC_RULES.md**: Scientific rules, parameter definitions, inference constraints, confidence policy, red flags.
- **WORKFLOW.md**: Development workflow, git practices, CI/CD pipeline.

**Do not proceed with implementation without understanding**:
- Project vision, objectives, and scope (Sections 1–14)
- Core agents and their responsibilities (Sections 16–18)
- Data sources and marine parameters (Sections 19–21)
- Reasoning flow, evidence attribution, confidence, and safety constraints (Sections 25–28)
- Known limitations and future scope (Sections 32–33)

**If something is uncertain or not defined**, explicitly mark it as:  
`TBD – Requires Team Decision`

**Do not silently invent features, datasets, scientific claims, APIs, or technologies** that are not supported by the provided project documentation.

**ORCA is an evidence-grounded collaborative marine reasoning platform that integrates heterogeneous marine information through specialized agents to produce explainable decision intelligence.**

***

**END OF PROJECT_CONTEXT.md**