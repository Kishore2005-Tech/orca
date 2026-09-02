# IMPLEMENTATION_PLAN.md

## ORCA – Marine Ecosystems Reasoning with Collaborative Agents  
**SIH26176 | ISRO | Implementation Plan for Antigravity/OpenCode**

***

## 1. Overview

This implementation plan breaks ORCA development into **18 dependency-aware phases**, prioritizing the **60–70% SIH prototype** (MVP) over production-scale infrastructure. Each phase contains tasks with clear dependencies, file/module assignments, acceptance criteria, tests, and Definition of Done (DoD).

**Implementation Principles**:
- **Dependency-Aware**: Later phases depend on earlier phases (e.g., agents depend on data ingestion).
- **MVP-First**: Prioritize prototype functionality (local filesystem, single-node) over production (cloud, distributed).
- **Test-Driven**: Every task includes tests; DoD requires passing tests.
- **Iterative**: Each phase builds on previous phases; refactoring allowed.

**Timeline Estimate**:
- **Phases 1–12 (Core Backend)**: 60% of effort
- **Phases 13–15 (API/Frontend)**: 25% of effort
- **Phases 16–18 (Testing/Evaluation/Polish)**: 15% of effort

***

## 2. Phase 1: Repository Foundation

**Goal**: Establish repository structure, development environment, and CI/CD basics.

### Task 1.1: Initialize Repository

- **Task ID**: `P1T1`
- **Description**: Create GitHub repository with standard structure (README, LICENSE, .gitignore, directories).
- **Dependencies**: None.
- **Files/Modules**:
  - `README.md`
  - `LICENSE` (MIT or Apache 2.0)
  - `.gitignore` (Python, Node, data files)
  - `docs/`, `src/`, `tests/`, `data/`, `scripts/` directories
- **Acceptance Criteria**:
  - Repository is public on GitHub.
  - README includes project overview, SIH code, team info.
  - Directory structure matches PROJECT_CONTEXT.md.
- **Tests**: None (manual check).
- **Definition of Done**:
  - Repository created and accessible.
  - README reviewed and approved by team.

### Task 1.2: Development Environment Setup

- **Task ID**: `P1T2`
- **Description**: Set up Python virtual environment, dependencies, and pre-commit hooks.
- **Dependencies**: `P1T1`.
- **Files/Modules**:
  - `requirements.txt` (Python dependencies: xarray, pandas, geopandas, netcdf4, requests, pytest)
  - `environment.yml` (Conda environment for reproducibility)
  - `.pre-commit-config.yaml` (black, flake8, isort)
  - `scripts/setup.sh` (automated setup script)
- **Acceptance Criteria**:
  - `pip install -r requirements.txt` succeeds.
  - Pre-commit hooks run on `git commit`.
- **Tests**:
  - `scripts/setup.sh` runs without errors.
  - Pre-commit hooks pass on sample commit.
- **Definition of Done**:
  - New developers can set up environment in < 15 minutes.
  - Pre-commit hooks configured and tested.

### Task 1.3: CI/CD Pipeline (Basic)

- **Task ID**: `P1T3`
- **Description**: Set up GitHub Actions for linting, testing, and deployment (prototype).
- **Dependencies**: `P1T1`, `P1T2`.
- **Files/Modules**:
  - `.github/workflows/ci.yml` (lint + test on PR)
  - `.github/workflows/deploy.yml` (deploy to prototype server on main merge)
- **Acceptance Criteria**:
  - CI runs on every PR (lint + test).
  - Deploy workflow deploys to prototype server (e.g., Heroku, Render).
- **Tests**:
  - CI workflow passes on sample PR.
  - Deploy workflow succeeds on main merge.
- **Definition of Done**:
  - CI/CD pipeline is functional.
  - Team can deploy prototype with `git push`.

***

## 3. Phase 2: Database

**Goal**: Set up lightweight database for metadata, caching, and audit trail (prototype: SQLite; production-ready: PostgreSQL + PostGIS).

### Task 2.1: Database Schema Design

- **Task ID**: `P2T1`
- **Description**: Design database schema for metadata, data provenance, and audit trail.
- **Dependencies**: `P1T1` (PROJECT_CONTEXT.md, DATA_PIPELINE.md).
- **Files/Modules**:
  - `docs/database_schema.md` (ER diagram, table definitions)
  - `scripts/create_tables.sql` (SQL schema)
- **Acceptance Criteria**:
  - Schema includes tables: `datasets`, `metadata`, `audit_log`, `cache`.
  - Schema aligns with DATA_PIPELINE.md Section 10.2.
- **Tests**: None (manual review).
- **Definition of Done**:
  - Schema reviewed and approved by team.
  - SQL script creates tables without errors.

### Task 2.2: Database Setup (SQLite for MVP)

- **Task ID**: `P2T2`
- **Description**: Set up SQLite database for MVP (lightweight, no server required).
- **Dependencies**: `P2T1`.
- **Files/Modules**:
  - `src/database/db.py` (database connection, initialization)
  - `src/database/models.py` (SQLAlchemy models for tables)
  - `data/orca.db` (SQLite database file)
- **Acceptance Criteria**:
  - Database initializes on first run.
  - Models match schema from `P2T1`.
- **Tests**:
  - `tests/test_database.py` (test table creation, insert, query).
- **Definition of Done**:
  - Database is functional.
  - Tests pass.

### Task 2.3: Metadata Storage

- **Task ID**: `P2T3`
- **Description**: Implement metadata storage (source, timestamp, resolution, quality flags).
- **Dependencies**: `P2T2`.
- **Files/Modules**:
  - `src/database/metadata.py` (metadata CRUD operations)
  - `src/database/schemas.py` (Pydantic schemas for metadata validation)
- **Acceptance Criteria**:
  - Metadata can be stored and retrieved for datasets.
  - Metadata includes: source, timestamp, resolution, units, quality_flags, is_stale.
- **Tests**:
  - `tests/test_metadata.py` (test metadata CRUD, validation).
- **Definition of Done**:
  - Metadata storage is functional.
  - Tests pass.

***

## 4. Phase 3: Data Ingestion

**Goal**: Implement data ingestion from authoritative sources (ISRO, INCOIS, NASA, NOAA, Copernicus).

### Task 3.1: API Ingestion Framework

- **Task ID**: `P3T1`
- **Description**: Build generic API ingestion framework (REST, OPeNDAP, FTP).
- **Dependencies**: `P1T2`, `P2T2`.
- **Files/Modules**:
  - `src/ingestion/api_ingest.py` (API ingestion logic)
  - `src/ingestion/ftp_ingest.py` (FTP ingestion logic)
  - `src/ingestion/config.py` (source configurations: URLs, auth, parameters)
- **Acceptance Criteria**:
  - Framework supports MOSDAC OPeNDAP, INCOIS REST API, NASA FTP.
  - Retry logic with exponential backoff (max 5 retries).
  - Logging for all ingestion attempts.
- **Tests**:
  - `tests/test_api_ingest.py` (test API ingestion, retry logic, error handling).
- **Definition of Done**:
  - Framework ingests data from at least 2 sources (e.g., MOSDAC, INCOIS).
  - Tests pass.

### Task 3.2: File Ingestion

- **Task ID**: `P3T2`
- **Description**: Implement file ingestion (NetCDF, HDF5, CSV, GeoJSON).
- **Dependencies**: `P3T1`.
- **Files/Modules**:
  - `src/ingestion/file_ingest.py` (file ingestion logic)
  - `src/ingestion/validators.py` (file structure validation)
- **Acceptance Criteria**:
  - Supports NetCDF, HDF5, CSV, GeoJSON.
  - Validates file structure (required variables/columns).
  - Copies files to `staging/` directory.
- **Tests**:
  - `tests/test_file_ingest.py` (test file ingestion, validation).
- **Definition of Done**:
  - File ingestion is functional for all supported formats.
  - Tests pass.

### Task 3.3: Caching

- **Task ID**: `P3T3`
- **Description**: Implement file-based caching (TTL: 24 hours for dynamic data, 30 days for static).
- **Dependencies**: `P3T1`, `P3T2`.
- **Files/Modules**:
  - `src/ingestion/cache.py` (cache management: key generation, TTL, invalidation)
  - `data/cache/` (cache directory)
- **Acceptance Criteria**:
  - Cache key = hash(source, product, time_range, bbox).
  - Cache invalidation after TTL.
  - Cache hit rate logged.
- **Tests**:
  - `tests/test_cache.py` (test cache hit/miss, TTL, invalidation).
- **Definition of Done**:
  - Caching is functional.
  - Tests pass.

***

## 5. Phase 4: Marine Data Tools

**Goal**: Build tools for parsing, validation, quality control, normalization, spatial/temporal alignment.

### Task 4.1: Raster Data Parsing

- **Task ID**: `P4T1`
- **Description**: Implement raster data parsing (NetCDF, HDF5, GeoTIFF) using xarray.
- **Dependencies**: `P3T2`.
- **Files/Modules**:
  - `src/parsing/raster_parser.py` (raster parsing logic)
  - `src/parsing/scale_offset.py` (apply scale factors, offsets)
- **Acceptance Criteria**:
  - Parses NetCDF, HDF5, GeoTIFF.
  - Applies scale/offset, masks fill values.
  - Extracts metadata (units, standard_name, calendar).
- **Tests**:
  - `tests/test_raster_parser.py` (test parsing, scale/offset, fill value masking).
- **Definition of Done**:
  - Raster parsing is functional.
  - Tests pass.

### Task 4.2: Tabular Data Parsing

- **Task ID**: `P4T2`
- **Description**: Implement tabular data parsing (CSV, JSON, GeoJSON) using pandas/geopandas.
- **Dependencies**: `P3T2`.
- **Files/Modules**:
  - `src/parsing/tabular_parser.py` (tabular parsing logic)
  - `src/parsing/timestamp_parser.py` (timestamp parsing, UTC conversion)
- **Acceptance Criteria**:
  - Parses CSV, JSON, GeoJSON.
  - Converts timestamps to UTC.
  - Validates required columns.
- **Tests**:
  - `tests/test_tabular_parser.py` (test parsing, timestamp conversion, column validation).
- **Definition of Done**:
  - Tabular parsing is functional.
  - Tests pass.

### Task 4.3: Validation

- **Task ID**: `P4T3`
- **Description**: Implement structural, semantic, and provenance validation.
- **Dependencies**: `P4T1`, `P4T2`.
- **Files/Modules**:
  - `src/validation/structural.py` (required variables, dimensions, attributes)
  - `src/validation/semantic.py` (coordinate ranges, physical bounds, temporal consistency)
  - `src/validation/provenance.py` (source, timestamp, version, DOI)
- **Acceptance Criteria**:
  - Structural validation catches missing variables/attributes.
  - Semantic validation catches out-of-bounds values (e.g., SST > 35°C).
  - Provenance validation logs source, timestamp, version.
- **Tests**:
  - `tests/test_validation.py` (test structural, semantic, provenance validation).
- **Definition of Done**:
  - Validation is functional.
  - Tests pass.

### Task 4.4: Quality Control

- **Task ID**: `P4T4`
- **Description**: Implement quality flags, missing value handling, outlier detection, stale data checks.
- **Dependencies**: `P4T3`.
- **Files/Modules**:
  - `src/quality/flags.py` (quality flag handling: cloud, sun glint, algorithm failure)
  - `src/quality/missing.py` (missing value detection, interpolation)
  - `src/quality/outliers.py` (outlier detection: physical bounds, statistical, spatial)
  - `src/quality/stale.py` (staleness checks per DATA_PIPELINE.md Section 6.4)
- **Acceptance Criteria**:
  - Quality flags mask low-quality pixels (quality level < 3).
  - Missing values are logged and interpolated (if < 10% gap).
  - Outliers are flagged and clipped to physical bounds.
  - Stale data is flagged (SST > 48 hours old).
- **Tests**:
  - `tests/test_quality.py` (test quality flags, missing values, outliers, stale data).
- **Definition of Done**:
  - Quality control is functional.
  - Tests pass.

### Task 4.5: Normalization

- **Task ID**: `P4T5`
- **Description**: Implement unit, coordinate, and timestamp normalization.
- **Dependencies**: `P4T4`.
- **Files/Modules**:
  - `src/normalization/units.py` (unit conversion: K→°C, km/h→m/s, etc.)
  - `src/normalization/coordinates.py` (coordinate normalization: WGS84, longitude range)
  - `src/normalization/timestamps.py` (timestamp normalization: UTC, ISO 8601)
- **Acceptance Criteria**:
  - All units converted to standard (°C, mg/m³, m, m/s).
  - All coordinates in WGS84 (EPSG:4326), longitude in [-180, 180].
  - All timestamps in UTC, ISO 8601 format.
- **Tests**:
  - `tests/test_normalization.py` (test unit, coordinate, timestamp conversion).
- **Definition of Done**:
  - Normalization is functional.
  - Tests pass.

### Task 4.6: Spatial Alignment

- **Task ID**: `P4T6`
- **Description**: Implement grid standardization, coastal masking, resolution consistency.
- **Dependencies**: `P4T5`.
- **Files/Modules**:
  - `src/alignment/spatial.py` (spatial alignment: resampling, coastal masking)
  - `src/alignment/grid.py` (target grid: 0.01°, Indian Ocean domain)
  - `src/alignment/mask.py` (land/sea mask from GEBCO)
- **Acceptance Criteria**:
  - All data resampled to target grid (0.01°).
  - Land pixels masked (set to NaN).
  - Resolution mismatch logged and aggregated to coarsest.
- **Tests**:
  - `tests/test_spatial_alignment.py` (test resampling, masking, resolution handling).
- **Definition of Done**:
  - Spatial alignment is functional.
  - Tests pass.

### Task 4.7: Temporal Alignment

- **Task ID**: `P4T7`
- **Description**: Implement time standardization, temporal interpolation, forecast validity.
- **Dependencies**: `P4T6`.
- **Files/Modules**:
  - `src/alignment/temporal.py` (temporal alignment: rounding, interpolation)
  - `src/alignment/forecast.py` (forecast validity checks: OSF 5–7 days, PFZ 24–48 hours)
- **Acceptance Criteria**:
  - All timestamps rounded to common frequency (hourly/daily).
  - Temporal interpolation for gaps < 3 days.
  - Forecast data truncated to valid window.
- **Tests**:
  - `tests/test_temporal_alignment.py` (test rounding, interpolation, forecast validity).
- **Definition of Done**:
  - Temporal alignment is functional.
  - Tests pass.

***

## 6. Phase 5: Ocean Agent

**Goal**: Implement Ocean Agent for physical ocean parameters (SST, SSS, SSH, currents, wind, waves, MLD, bathymetry).

### Task 5.1: Ocean Agent Core

- **Task ID**: `P5T1`
- **Description**: Implement Ocean Agent core logic (data retrieval, processing, output).
- **Dependencies**: `P4T7` (all data pipeline stages).
- **Files/Modules**:
  - `src/agents/ocean_agent.py` (Ocean Agent class)
  - `src/agents/tools/ocean_tools.py` (tools: get_sst, get_ssh, get_wind, get_waves, etc.)
- **Acceptance Criteria**:
  - Retrieves SST, SSH, wind, waves from processed data.
  - Computes SST gradient, detects fronts.
  - Outputs physical ocean indicators (e.g., "SST gradient = 2°C/10 km indicates front").
- **Tests**:
  - `tests/test_ocean_agent.py` (test data retrieval, gradient computation, front detection).
- **Definition of Done**:
  - Ocean Agent is functional.
  - Tests pass.

### Task 5.2: Ocean Agent Validation

- **Task ID**: `P5T2`
- **Description**: Integrate Ocean Agent with Verification Agent for scientific consistency.
- **Dependencies**: `P5T1`, `P11T1` (Verification Agent).
- **Files/Modules**:
  - `src/agents/ocean_agent.py` (add verification step)
- **Acceptance Criteria**:
  - Ocean Agent outputs are validated by Verification Agent.
  - Inconsistent outputs are flagged and corrected.
- **Tests**:
  - `tests/test_ocean_agent_validation.py` (test verification integration).
- **Definition of Done**:
  - Ocean Agent validation is functional.
  - Tests pass.

***

## 7. Phase 6: Ecosystem Agent

**Goal**: Implement Ecosystem Agent for biological oceanography (chlorophyll-a, primary productivity, phytoplankton, MHW, fronts, upwelling, ecosystem anomalies).

### Task 6.1: Ecosystem Agent Core

- **Task ID**: `P6T1`
- **Description**: Implement Ecosystem Agent core logic (chlorophyll processing, MHW detection, front/upwelling identification).
- **Dependencies**: `P4T7`, `P5T1` (Ocean Agent SST).
- **Files/Modules**:
  - `src/agents/ecosystem_agent.py` (Ecosystem Agent class)
  - `src/agents/tools/ecosystem_tools.py` (tools: get_chlorophyll, get_mhw, get_fronts, get_upwelling)
- **Acceptance Criteria**:
  - Retrieves chlorophyll from processed data.
  - Detects MHW (Hobday criteria: SST > 90th percentile for ≥5 days).
  - Identifies fronts (SST + chlorophyll gradients), upwelling (cold SST + high chlorophyll).
  - Outputs ecosystem indicators (e.g., "Chlorophyll = 2 mg/m³ indicates elevated biomass").
- **Tests**:
  - `tests/test_ecosystem_agent.py` (test chlorophyll processing, MHW detection, front/upwelling identification).
- **Definition of Done**:
  - Ecosystem Agent is functional.
  - Tests pass.

### Task 6.2: Ecosystem Agent Validation

- **Task ID**: `P6T2`
- **Description**: Integrate Ecosystem Agent with Verification Agent for scientific consistency.
- **Dependencies**: `P6T1`, `P11T1`.
- **Files/Modules**:
  - `src/agents/ecosystem_agent.py` (add verification step)
- **Acceptance Criteria**:
  - Ecosystem Agent outputs are validated by Verification Agent.
  - Inconsistent outputs (e.g., MHW without SST anomaly) are flagged.
- **Tests**:
  - `tests/test_ecosystem_agent_validation.py` (test verification integration).
- **Definition of Done**:
  - Ecosystem Agent validation is functional.
  - Tests pass.

***

## 8. Phase 7: Fisheries Agent

**Goal**: Implement Fisheries Agent for PFZ, fish habitat indicators, catch probability.

### Task 7.1: Fisheries Agent Core

- **Task ID**: `P7T1`
- **Description**: Implement Fisheries Agent core logic (PFZ generation, habitat suitability, drift estimation).
- **Dependencies**: `P5T1` (Ocean Agent), `P6T1` (Ecosystem Agent).
- **Files/Modules**:
  - `src/agents/fisheries_agent.py` (Fisheries Agent class)
  - `src/agents/tools/fisheries_tools.py` (tools: get_pfz, get_habitat_suitability, get_pfz_drift)
- **Acceptance Criteria**:
  - Generates PFZ from SST + chlorophyll (INCOIS methodology).
  - Validates PFZ against bathymetry (depth range for pelagic species).
  - Estimates PFZ drift using wind/currents.
  - Outputs PFZ coordinates, habitat indicators (e.g., "PFZ at 12°N, 78°E; may reduce search time").
- **Tests**:
  - `tests/test_fisheries_agent.py` (test PFZ generation, bathymetry validation, drift estimation).
- **Definition of Done**:
  - Fisheries Agent is functional.
  - Tests pass.

### Task 7.2: Fisheries Agent Validation

- **Task ID**: `P7T2`
- **Description**: Integrate Fisheries Agent with Verification Agent for scientific consistency.
- **Dependencies**: `P7T1`, `P11T1`.
- **Files/Modules**:
  - `src/agents/fisheries_agent.py` (add verification step)
- **Acceptance Criteria**:
  - Fisheries Agent outputs are validated (e.g., PFZ requires SST + chlorophyll, not chlorophyll alone).
  - Prohibited claims (e.g., "PFZ guarantees catch") are flagged.
- **Tests**:
  - `tests/test_fisheries_agent_validation.py` (test verification integration, prohibited claim detection).
- **Definition of Done**:
  - Fisheries Agent validation is functional.
  - Tests pass.

***

## 9. Phase 8: Safety Agent

**Goal**: Implement Safety Agent for wave height, wind, hazards, High Wave Alerts.

### Task 8.1: Safety Agent Core

- **Task ID**: `P8T1`
- **Description**: Implement Safety Agent core logic (wave height thresholds, hazard warnings, fishing ban checks).
- **Dependencies**: `P5T1` (Ocean Agent waves/wind).
- **Files/Modules**:
  - `src/agents/safety_agent.py` (Safety Agent class)
  - `src/agents/tools/safety_tools.py` (tools: get_wave_risk, get_hazard_alert, check_fishing_ban)
- **Acceptance Criteria**:
  - Retrieves wave height from INCOIS OSF.
  - Applies High Wave Alert thresholds (Watch 2.5–3.0 m, Alert >3.0 m).
  - Checks for marine hazards (cyclones, tsunamis) and fishing bans.
  - Outputs safety alerts (e.g., "High Wave Alert: Hs > 3.0 m; small vessels should exercise caution").
- **Tests**:
  - `tests/test_safety_agent.py` (test wave height thresholds, hazard checks, fishing ban).
- **Definition of Done**:
  - Safety Agent is functional.
  - Tests pass.

### Task 8.2: Safety Agent Validation

- **Task ID**: `P8T2`
- **Description**: Integrate Safety Agent with Verification Agent for scientific consistency.
- **Dependencies**: `P8T1`, `P11T1`.
- **Files/Modules**:
  - `src/agents/safety_agent.py` (add verification step)
- **Acceptance Criteria**:
  - Safety Agent outputs use official sources (INCOIS, IMD, NOAA).
  - Deterministic safety claims (e.g., "Safe to fish") are flagged.
- **Tests**:
  - `tests/test_safety_agent_validation.py` (test verification integration, safety claim validation).
- **Definition of Done**:
  - Safety Agent validation is functional.
  - Tests pass.

***

## 10. Phase 9: Geospatial Agent

**Goal**: Implement Geospatial Agent for coordinate validation, resolution awareness, geographic consistency.

### Task 9.1: Geospatial Agent Core

- **Task ID**: `P9T1`
- **Description**: Implement Geospatial Agent core logic (coordinate validation, resolution checks, coverage validation).
- **Dependencies**: `P4T7` (spatial/temporal alignment).
- **Files/Modules**:
  - `src/agents/geospatial_agent.py` (Geospatial Agent class)
  - `src/agents/tools/geospatial_tools.py` (tools: validate_coordinates, check_resolution, check_coverage)
- **Acceptance Criteria**:
  - Validates WGS84 coordinates (lat/lon ranges).
  - Checks ocean domain (not land).
  - Respects native resolution (no sub-grid inference).
  - Flags coastal contamination, data gaps.
- **Tests**:
  - `tests/test_geospatial_agent.py` (test coordinate validation, resolution checks, coverage).
- **Definition of Done**:
  - Geospatial Agent is functional.
  - Tests pass.

***

## 11. Phase 10: RAG/Evidence Agent

**Goal**: Implement RAG Agent for scientific source attribution, literature retrieval.

### Task 10.1: RAG Agent Core

- **Task ID**: `P10T1`
- **Description**: Implement RAG Agent core logic (source retrieval, citation generation).
- **Dependencies**: `P2T3` (metadata storage), `P4T3` (provenance validation).
- **Files/Modules**:
  - `src/agents/rag_agent.py` (RAG Agent class)
  - `src/agents/tools/rag_tools.py` (tools: retrieve_source, generate_citation)
  - `data/knowledge_base/` (SCIENTIFIC_RULES.md, authoritative references)
- **Acceptance Criteria**:
  - Retrieves sources from knowledge base (SCIENTIFIC_RULES.md, references).
  - Generates citations (source, year, DOI/URL).
  - Flags unverified sources (blogs, social media).
- **Tests**:
  - `tests/test_rag_agent.py` (test source retrieval, citation generation, source validation).
- **Definition of Done**:
  - RAG Agent is functional.
  - Tests pass.

***

## 12. Phase 11: Verification

**Goal**: Implement Verification Agent for scientific consistency, source provenance, timestamp, unsupported inference detection.

### Task 11.1: Verification Agent Core

- **Task ID**: `P11T1`
- **Description**: Implement Verification Agent core logic (consistency checks, provenance validation, timestamp checks, hallucination detection).
- **Dependencies**: `P5T1`–`P10T1` (all other agents).
- **Files/Modules**:
  - `src/agents/verification_agent.py` (Verification Agent class)
  - `src/agents/tools/verification_tools.py` (tools: check_consistency, validate_provenance, check_timestamp, detect_hallucination)
- **Acceptance Criteria**:
  - Checks scientific consistency (e.g., SST + chlorophyll agree on front).
  - Validates source provenance (ISRO, INCOIS, NASA, etc.).
  - Checks timestamps (freshness, forecast validity).
  - Detects unsupported inferences (hallucinations).
- **Tests**:
  - `tests/test_verification_agent.py` (test consistency, provenance, timestamp, hallucination detection).
- **Definition of Done**:
  - Verification Agent is functional.
  - Tests pass.

***

## 13. Phase 12: Coordinator

**Goal**: Implement Coordinator for multi-agent synthesis, evidence combination, traceable output generation.

### Task 12.1: Coordinator Core

- **Task ID**: `P12T1`
- **Description**: Implement Coordinator core logic (agent orchestration, evidence synthesis, confidence assignment, output generation).
- **Dependencies**: `P5T1`–`P11T1` (all agents).
- **Files/Modules**:
  - `src/agents/coordinator.py` (Coordinator class)
  - `src/agents/tools/coordinator_tools.py` (tools: synthesize_evidence, assign_confidence, generate_output)
- **Acceptance Criteria**:
  - Orchestrates all agents (Ocean, Ecosystem, Fisheries, Safety, Geospatial, RAG, Verification).
  - Synthesizes evidence into traceable output (Observation → Indicator → Interpretation → Inference → Recommendation).
  - Assigns confidence levels (High/Medium/Low/Insufficient) per SCIENTIFIC_RULES.md Section 20.
  - Generates explainable output with evidence chain, citations, uncertainty.
- **Tests**:
  - `tests/test_coordinator.py` (test agent orchestration, evidence synthesis, confidence assignment, output generation).
- **Definition of Done**:
  - Coordinator is functional.
  - Tests pass.

### Task 12.2: Coordinator Integration

- **Task ID**: `P12T2`
- **Description**: Integrate Coordinator with all agents for end-to-end reasoning.
- **Dependencies**: `P12T1`, `P5T1`–`P11T1`.
- **Files/Modules**:
  - `src/agents/coordinator.py` (add agent integration)
- **Acceptance Criteria**:
  - End-to-end reasoning flow works (query → agents → Coordinator → output).
  - Conflicts are resolved (e.g., SST vs. chlorophyll disagreement → confidence downgrade).
- **Tests**:
  - `tests/test_coordinator_integration.py` (test end-to-end reasoning, conflict resolution).
- **Definition of Done**:
  - Coordinator integration is functional.
  - Tests pass.

***

## 14. Phase 13: API

**Goal**: Implement REST API for ORCA queries, data access, and agent tools.

### Task 13.1: API Core

- **Task ID**: `P13T1`
- **Description**: Implement REST API using FastAPI (query endpoint, data access, agent tools).
- **Dependencies**: `P12T2` (Coordinator integration).
- **Files/Modules**:
  - `src/api/main.py` (FastAPI app)
  - `src/api/routes.py` (API routes: /query, /data/{parameter}, /tools/{tool})
  - `src/api/schemas.py` (Pydantic schemas for request/response)
- **Acceptance Criteria**:
  - `/query` endpoint accepts location (lat/lon) and query, returns ORCA output.
  - `/data/{parameter}` endpoint returns data (SST, chlorophyll, etc.) for bbox/time.
  - `/tools/{tool}` endpoint exposes agent tools (get_sst, get_pfz, etc.).
  - API includes authentication (API key) and rate limiting.
- **Tests**:
  - `tests/test_api.py` (test endpoints, authentication, rate limiting).
- **Definition of Done**:
  - API is functional.
  - Tests pass.

### Task 13.2: API Documentation

- **Task ID**: `P13T2`
- **Description**: Generate API documentation using FastAPI Swagger/OpenAPI.
- **Dependencies**: `P13T1`.
- **Files/Modules**:
  - `docs/api.md` (API documentation, examples)
  - `/docs` (FastAPI auto-generated Swagger UI)
- **Acceptance Criteria**:
  - Swagger UI is accessible at `/docs`.
  - API documentation includes examples, schemas, error codes.
- **Tests**: None (manual check).
- **Definition of Done**:
  - API documentation is complete.
  - Swagger UI is accessible.

***

## 15. Phase 14: Frontend/Map

**Goal**: Implement web-based frontend with interactive map for ORCA queries and visualization.

### Task 14.1: Frontend Core

- **Task ID**: `P14T1`
- **Description**: Implement frontend using React + Leaflet (map, query form, results display).
- **Dependencies**: `P13T1` (API).
- **Files/Modules**:
  - `frontend/src/App.jsx` (React app)
  - `frontend/src/components/Map.jsx` (Leaflet map)
  - `frontend/src/components/QueryForm.jsx` (query form: lat/lon, query text)
  - `frontend/src/components/Results.jsx` (results display: PFZ, safety alerts, evidence chain)
- **Acceptance Criteria**:
  - Interactive map displays location, PFZ, fronts, MHW.
  - Query form accepts lat/lon and query text.
  - Results display shows ORCA output (PFZ, safety alerts, evidence chain, citations).
- **Tests**:
  - `frontend/tests/test_app.jsx` (test map, query form, results display).
- **Definition of Done**:
  - Frontend is functional.
  - Tests pass.

### Task 14.2: Frontend Deployment

- **Task ID**: `P14T2`
- **Description**: Deploy frontend to prototype server (Netlify, Vercel, or same server as API).
- **Dependencies**: `P14T1`.
- **Files/Modules**:
  - `frontend/package.json` (build scripts)
  - `scripts/deploy_frontend.sh` (deployment script)
- **Acceptance Criteria**:
  - Frontend is deployed and accessible via URL.
  - Frontend connects to API (no CORS errors).
- **Tests**: None (manual check).
- **Definition of Done**:
  - Frontend is deployed.
  - Team can access frontend via URL.

***

## 16. Phase 15: Reasoning Visualization

**Goal**: Implement visualization for evidence chain, confidence levels, agent contributions.

### Task 15.1: Evidence Chain Visualization

- **Task ID**: `P15T1`
- **Description**: Implement evidence chain visualization (Observation → Indicator → Interpretation → Inference → Recommendation).
- **Dependencies**: `P14T1` (Frontend), `P12T1` (Coordinator).
- **Files/Modules**:
  - `frontend/src/components/EvidenceChain.jsx` (evidence chain visualization)
  - `frontend/src/components/ConfidenceGauge.jsx` (confidence level gauge)
  - `frontend/src/components/AgentContributions.jsx` (agent contribution breakdown)
- **Acceptance Criteria**:
  - Evidence chain is displayed as flowchart (5 stages).
  - Confidence level is displayed as gauge (High/Medium/Low/Insufficient).
  - Agent contributions are displayed (which agents contributed to output).
- **Tests**:
  - `frontend/tests/test_evidence_chain.jsx` (test visualization components).
- **Definition of Done**:
  - Evidence chain visualization is functional.
  - Tests pass.

### Task 15.2: Citation Visualization

- **Task ID**: `P15T2`
- **Description**: Implement citation visualization (clickable citations linking to sources).
- **Dependencies**: `P15T1`, `P10T1` (RAG Agent).
- **Files/Modules**:
  - `frontend/src/components/Citations.jsx` (citation list with links)
- **Acceptance Criteria**:
  - Citations are displayed as clickable links (DOI/URL).
  - Clicking citation opens source in new tab.
- **Tests**:
  - `frontend/tests/test_citations.jsx` (test citation links).
- **Definition of Done**:
  - Citation visualization is functional.
  - Tests pass.

***

## 17. Phase 16: Testing

**Goal**: Implement comprehensive testing (unit, integration, end-to-end).

### Task 16.1: Unit Tests

- **Task ID**: `P16T1`
- **Description**: Write unit tests for all modules (data pipeline, agents, API, frontend).
- **Dependencies**: `P4T7` (data pipeline), `P5T1`–`P12T1` (agents), `P13T1` (API), `P14T1` (frontend).
- **Files/Modules**:
  - `tests/test_*.py` (unit tests for all Python modules)
  - `frontend/tests/test_*.jsx` (unit tests for all React components)
- **Acceptance Criteria**:
  - All modules have unit tests.
  - Test coverage > 80% (measured by `pytest --cov`).
- **Tests**:
  - `pytest --cov` (coverage report).
- **Definition of Done**:
  - All modules have unit tests.
  - Coverage > 80%.

### Task 16.2: Integration Tests

- **Task ID**: `P16T2`
- **Description**: Write integration tests for agent interactions, API endpoints, frontend-backend integration.
- **Dependencies**: `P16T1`, `P12T2` (Coordinator integration), `P13T1` (API), `P14T1` (frontend).
- **Files/Modules**:
  - `tests/test_integration_*.py` (integration tests for agents, API)
  - `frontend/tests/test_integration_*.jsx` (integration tests for frontend-backend)
- **Acceptance Criteria**:
  - Agent interactions are tested (e.g., Ocean + Ecosystem → Fisheries).
  - API endpoints are tested (e.g., /query, /data/{parameter}).
  - Frontend-backend integration is tested (e.g., query form → API → results).
- **Tests**:
  - `pytest tests/test_integration_*.py` (integration tests).
- **Definition of Done**:
  - Integration tests are functional.
  - Tests pass.

### Task 16.3: End-to-End Tests

- **Task ID**: `P16T3`
- **Description**: Write end-to-end tests for full user workflows (query → results → visualization).
- **Dependencies**: `P16T2`, `P14T1` (frontend), `P13T1` (API), `P12T2` (Coordinator).
- **Files/Modules**:
  - `tests/test_e2e_*.py` (end-to-end tests using Selenium/Playwright)
- **Acceptance Criteria**:
  - Full user workflows are tested (e.g., "Query PFZ at 12°N, 78°E → view results → view evidence chain").
  - Tests run in CI/CD pipeline.
- **Tests**:
  - `pytest tests/test_e2e_*.py` (end-to-end tests).
- **Definition of Done**:
  - End-to-end tests are functional.
  - Tests pass in CI/CD.

***

## 18. Phase 17: Evaluation

**Goal**: Implement evaluation framework per EVALUATION_AND_TESTING.md.

### Task 17.1: Evaluation Framework

- **Task ID**: `P17T1`
- **Description**: Implement evaluation framework (metrics, test scenarios, ground truth comparison).
- **Dependencies**: `P16T3` (end-to-end tests), `P12T2` (Coordinator).
- **Files/Modules**:
  - `tests/evaluation/evaluate.py` (evaluation framework)
  - `tests/evaluation/metrics.py` (metrics: RMSE, MAE, hit rate, etc.)
  - `tests/evaluation/scenarios.py` (test scenarios from EVALUATION_AND_TESTING.md)
- **Acceptance Criteria**:
  - Evaluation framework computes all metrics from EVALUATION_AND_TESTING.md Section 7.
  - Test scenarios (S1–S12) are implemented.
  - Ground truth comparison is functional (vs. buoy, catch reports, MHW catalog).
- **Tests**:
  - `pytest tests/evaluation/test_evaluate.py` (test evaluation framework).
- **Definition of Done**:
  - Evaluation framework is functional.
  - Tests pass.

### Task 17.2: Evaluation Report

- **Task ID**: `P17T2`
- **Description**: Generate evaluation report (quantitative metrics, qualitative results, ablation tests).
- **Dependencies**: `P17T1`.
- **Files/Modules**:
  - `docs/evaluation_report.md` (evaluation report template)
  - `scripts/generate_report.py` (report generation script)
- **Acceptance Criteria**:
  - Report includes all metrics from EVALUATION_AND_TESTING.md Section 10.2 (template table).
  - Report includes qualitative results (expert review, user studies).
  - Report includes ablation test results (component importance).
- **Tests**: None (manual review).
- **Definition of Done**:
  - Evaluation report is generated.
  - Report is reviewed and approved by team.

***

## 19. Phase 18: Final Polish

**Goal**: Polish prototype for SIH submission (documentation, demo scenario, video).

### Task 18.1: Documentation

- **Task ID**: `P18T1`
- **Description**: Finalize all documentation (README, PROJECT_CONTEXT.md, SCIENTIFIC_RULES.md, DATA_PIPELINE.md, EVALUATION_AND_TESTING.md, IMPLEMENTATION_PLAN.md).
- **Dependencies**: All previous phases.
- **Files/Modules**:
  - `README.md` (updated with final overview, setup instructions)
  - `docs/` (all documentation files reviewed and finalized)
- **Acceptance Criteria**:
  - All documentation is complete, consistent, and up-to-date.
  - README includes SIH code, team info, setup instructions, demo link.
- **Tests**: None (manual review).
- **Definition of Done**:
  - All documentation is finalized.
  - Team reviews and approves documentation.

### Task 18.2: Demo Scenario

- **Task ID**: `P18T2`
- **Description**: Prepare demo scenario per PROJECT_CONTEXT.md Section 30 (Kerala coast PFZ query).
- **Dependencies**: `P14T1` (frontend), `P12T2` (Coordinator), `P17T1` (evaluation).
- **Files/Modules**:
  - `scripts/demo_scenario.py` (automated demo script)
  - `docs/demo_scenario.md` (demo scenario walkthrough)
- **Acceptance Criteria**:
  - Demo scenario runs end-to-end (query → results → evidence chain → citations).
  - Demo showcases key features (PFZ, safety alerts, evidence attribution, confidence).
- **Tests**:
  - `scripts/demo_scenario.py` runs without errors.
- **Definition of Done**:
  - Demo scenario is functional.
  - Team rehearses demo.

### Task 18.3: Submission Package

- **Task ID**: `P18T3`
- **Description**: Prepare SIH submission package (code, documentation, video, report).
- **Dependencies**: `P18T1`, `P18T2`.
- **Files/Modules**:
  - `submission/` (submission package directory)
  - `submission/report.pdf` (project report)
  - `submission/video.mp4` (demo video, 5–10 minutes)
  - `submission/code.zip` (code snapshot)
- **Acceptance Criteria**:
  - Submission package includes all required components (report, video, code).
  - Report follows SIH format (problem, solution, innovation, impact).
  - Video demonstrates demo scenario clearly.
- **Tests**: None (manual review).
- **Definition of Done**:
  - Submission package is complete.
  - Team reviews and approves submission.

***

## 20. Dependency Graph

```
Phase 1 (Repository) → Phase 2 (Database) → Phase 3 (Ingestion) → Phase 4 (Data Tools)
                                                      ↓
Phase 5 (Ocean Agent) ← Phase 4 ──────────────────────┘
Phase 6 (Ecosystem Agent) ← Phase 4, Phase 5
Phase 7 (Fisheries Agent) ← Phase 5, Phase 6
Phase 8 (Safety Agent) ← Phase 5
Phase 9 (Geospatial Agent) ← Phase 4
Phase 10 (RAG Agent) ← Phase 2, Phase 4
Phase 11 (Verification Agent) ← Phase 5–10
Phase 12 (Coordinator) ← Phase 5–11
Phase 13 (API) ← Phase 12
Phase 14 (Frontend) ← Phase 13
Phase 15 (Visualization) ← Phase 14, Phase 12
Phase 16 (Testing) ← Phase 4–15
Phase 17 (Evaluation) ← Phase 16, Phase 12
Phase 18 (Polish) ← Phase 1–17
```

***

## 21. MVP Prioritization (60–70% SIH Prototype)

**Core Features (MVP)**:
- **Phases 1–4**: Repository, database, data ingestion, data tools (foundational).
- **Phases 5–8**: Ocean, Ecosystem, Fisheries, Safety Agents (core reasoning).
- **Phases 9–12**: Geospatial, RAG, Verification, Coordinator (agent coordination).
- **Phase 13**: API (basic query endpoint).
- **Phase 14**: Frontend (basic map + query form).
- **Phase 16**: Testing (unit + integration tests).

**Deferred to Post-MVP**:
- **Phase 15**: Advanced visualization (evidence chain, confidence gauge) – basic text output is sufficient for MVP.
- **Phase 17**: Full evaluation framework – basic metric computation is sufficient for MVP.
- **Phase 18**: Final polish – focus on core functionality first.

**MVP Success Criteria**:
- ORCA can query PFZ + safety alerts for Indian Ocean location.
- Output includes evidence chain, citations, confidence level.
- API and frontend are functional.
- Tests pass (unit + integration).

***

## 22. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **Data Source Unavailability** | Use fallback sources (e.g., NASA MODIS if MOSDAC OCM unavailable); cache data aggressively. |
| **Agent Conflicts** | Verification Agent flags conflicts; Coordinator downgrades confidence. |
| **Hallucinations** | RAG Agent enforces source attribution; Verification Agent detects unsupported claims. |
| **Performance Issues** | Optimize data pipeline (chunking, caching); use lightweight SQLite for MVP. |
| **Timeline Slippage** | Prioritize MVP features (Phases 1–14); defer advanced visualization/evaluation (Phases 15, 17). |

***

## 23. References

1. **PROJECT_CONTEXT.md**: ORCA project identity, vision, architecture, agents.
2. **SCIENTIFIC_RULES.md**: Scientific rules, parameter definitions, inference constraints.
3. **DATA_PIPELINE.md**: Data ingestion, processing, storage, feature generation.
4. **EVALUATION_AND_TESTING.md**: Evaluation metrics, test scenarios, ground truth.

***

**END OF IMPLEMENTATION_PLAN.md**