# DATA_DICTIONARY.md

# ORCA Data Dictionary

**Project:** SIH26176 – ORCA
**Full Name:** Marine Ecosystems Reasoning with Collaborative Agents
**Derived from:** `DATA_SOURCE_CATALOG.md` (last reviewed August 30, 2026) and `DOMAIN_KNOWLEDGE.md`
**Purpose:** Define every data field ORCA's prototype needs, at the level of detail required for schema design, ingestion validation, and agent consumption.
**Status:** Category B (Proposed Design) unless otherwise noted. Fields marked "Requires validation" fall under Category C per the ORCA master context document and must be confirmed against live source access before implementation.

---

## 0. Scope and Method

This dictionary covers only fields tied to a dataset or derived product that appears in the **Recommended prototype dataset set** table of `DATA_SOURCE_CATALOG.md`, plus the provenance/quality-metadata envelope that the catalog's Section 12 ("Data Quality and Verification Policy") mandates for every ingestion record.

**Deliberately excluded** (present in `DOMAIN_KNOWLEDGE.md` as scientific concepts but absent from the catalog's prototype dataset table, and therefore not given dedicated fields here):

- Sea Surface Salinity (SSS) — no SSS-specific source is listed in the catalog's Tier 1/2 prototype set.
- Sea Surface Height (SSH) as a standalone altimetry field — SSH appears only as an incidental Copernicus physics variable, not as a tracked catalog row; `sea_level_height` (Section 6, sourced from Open-Meteo) is the only sea-level field the catalog scopes for the prototype.
- Mixed Layer Depth (MLD), ocean fronts, eddies — mentioned in `DOMAIN_KNOWLEDGE.md` as reasoning concepts, but no catalog source is designated for them.
- EEZ boundary geometry — no EEZ dataset appears in the catalog.
- Fishing effort / VMS / AIS — mentioned conceptually in `DOMAIN_KNOWLEDGE.md` but not present in the catalog's dataset list.
- Species-specific habitat fields — explicitly deferred by `DOMAIN_KNOWLEDGE.md` Section 8 as requiring species-level evidence not yet sourced.

If any of these are needed later, they require a corresponding entry to be added to `DATA_SOURCE_CATALOG.md` first, per the master context document's rule against inventing datasets.

**Database stack assumed** (per ORCA proposed technology stack): PostgreSQL + PostGIS (geometry) + TimescaleDB (time-series hypertables) + pgvector (not used by structured fields below).

---

## 1. Query / Geospatial Context Fields

These are not sourced from an external dataset; they originate from the user query and from derived geospatial computation, per `DATA_SOURCE_CATALOG.md` Section 15 ("Geospatial Agent: GEBCO depth context + distance calculation").

### 1.1 `query_latitude`

| Attribute | Value |
|---|---|
| Field name | `query_latitude` |
| Description | Latitude of the user's query location or point of interest |
| Data type | Float (double precision) |
| Unit | Decimal degrees |
| Valid range | -90.0 to 90.0 (practically ~5.0 to 25.0 for Indian coastal/Bay of Bengal/Arabian Sea scope) |
| Nullable | No |
| Source dataset | User input / device geolocation (not a catalog dataset) |
| Spatial reference | WGS84 (EPSG:4326) |
| Temporal reference | Not applicable |
| Quality flag | Not applicable |
| Freshness requirement | Real-time (per query) |
| Validation rule | Must be within -90..90; combined with `query_longitude` must fall within or near Indian EEZ / Bay of Bengal / Arabian Sea prototype bounding box |
| Agent consuming it | Geospatial Agent, ORCA Coordinator |
| Database representation | Encoded jointly with longitude as `PostGIS GEOMETRY(Point, 4326)` column `query_location` |
| Example value | `13.0500` |

### 1.2 `query_longitude`

| Attribute | Value |
|---|---|
| Field name | `query_longitude` |
| Description | Longitude of the user's query location or point of interest |
| Data type | Float (double precision) |
| Unit | Decimal degrees |
| Valid range | -180.0 to 180.0 (practically ~68.0 to 92.0 for Indian coastal scope) |
| Nullable | No |
| Source dataset | User input / device geolocation (not a catalog dataset) |
| Spatial reference | WGS84 (EPSG:4326) |
| Temporal reference | Not applicable |
| Quality flag | Not applicable |
| Freshness requirement | Real-time (per query) |
| Validation rule | Must be within -180..180; combined with latitude must fall within prototype bounding box |
| Agent consuming it | Geospatial Agent, ORCA Coordinator |
| Database representation | Encoded jointly with latitude in `query_location` (see above) |
| Example value | `80.2700` |

### 1.3 `query_timestamp`

| Attribute | Value |
|---|---|
| Field name | `query_timestamp` |
| Description | Time for which the user is requesting marine conditions or a recommendation (may be current time or a near-future time for forecast queries) |
| Data type | Timestamp with time zone |
| Unit | ISO-8601 |
| Valid range | Not earlier than the earliest available historical baseline; not later than the maximum forecast horizon of the shortest-horizon source in use |
| Nullable | No |
| Source dataset | User input (not a catalog dataset) |
| Spatial reference | Not applicable |
| Temporal reference | ISO-8601, UTC internally; localized to IST for display |
| Quality flag | Not applicable |
| Freshness requirement | Real-time (per query) |
| Validation rule | Reject timestamps beyond the maximum forecast horizon available from Section 6/9's data sources; flag (not reject) past timestamps beyond available historical baseline coverage |
| Agent consuming it | ORCA Coordinator, all domain agents |
| Database representation | `TIMESTAMPTZ` column on the query/session table |
| Example value | `2026-08-31T06:00:00+05:30` |

### 1.4 `distance_to_coast_km`

| Attribute | Value |
|---|---|
| Field name | `distance_to_coast_km` |
| Description | Derived straight-line distance from the query location to the nearest coastline, computed from bathymetry/coastline geometry |
| Data type | Float |
| Unit | Kilometres |
| Valid range | ≥ 0 |
| Nullable | Yes (null if coastline geometry unavailable for the region) |
| Source dataset | Derived from GEBCO 2026 Grid (Section 7.1) coastline extraction |
| Spatial reference | WGS84 (EPSG:4326); computed geodesically |
| Temporal reference | Static (recomputed only if underlying bathymetry version changes) |
| Quality flag | Inherits GEBCO Type Identifier Grid caveat (interpolated/modelled areas) |
| Freshness requirement | Static — recompute only on GEBCO grid version update (annual) |
| Validation rule | Must be ≥ 0; flag as low-confidence if source point falls in a GEBCO interpolated (non-measured) area |
| Agent consuming it | Geospatial Agent, Safety Agent |
| Database representation | `NUMERIC(8,2)` column, derived/cached, not stored per-observation |
| Example value | `12.40` |

---

## 2. Physical Oceanography

### 2.1 `sea_surface_temperature`

| Attribute | Value |
|---|---|
| Field name | `sea_surface_temperature` |
| Description | Temperature of seawater at or near the ocean surface (skin or near-surface layer depending on sensor/product) |
| Data type | Float |
| Unit | °C |
| Valid range | -2.0 to 36.0 (physically realistic range for Indian Ocean / Bay of Bengal / Arabian Sea) |
| Nullable | Yes (null on cloud-obscured or missing-observation cells; do not substitute 0) |
| Source dataset | Copernicus Marine global SST products (1.1) — primary; NASA OB.DAAC SST (1.2) and NOAA OISST v2.1 (1.3) as backup/historical baseline |
| Spatial reference | WGS84 (EPSG:4326); source grid ~0.05°–0.25° (Copernicus) or ~0.25° (NOAA OISST) |
| Temporal reference | Product-dependent: daily analysis, forecast horizon per selected Copernicus product, or daily for OISST |
| Quality flag | Source-reported quality-control/uncertainty variable, or `null` if unavailable — never treated as valid by default |
| Freshness requirement | Near-real-time; flag as stale if `retrieved_at` − `valid_time_end` exceeds the source product's documented update latency |
| Validation rule | Reject values outside -2.0–36.0°C; reject if `data_class` metadata is missing; must never be displayed without accompanying `data_class` (observation/analysis/forecast) |
| Agent consuming it | Ocean Agent, Ecosystem Agent, Fisheries Agent, Verification Agent |
| Database representation | TimescaleDB hypertable `sst_observations` (`geom GEOMETRY(Point,4326)`, `sst_c NUMERIC(5,2)`, `valid_time TIMESTAMPTZ`) |
| Example value | `28.60` |

### 2.2 `ocean_current_u`

| Attribute | Value |
|---|---|
| Field name | `ocean_current_u` |
| Description | Zonal (east–west) component of ocean current velocity |
| Data type | Float |
| Unit | m/s |
| Valid range | -3.0 to 3.0 (typical operational range; extreme mesoscale features may exceed) |
| Nullable | Yes |
| Source dataset | Copernicus Marine Global Ocean Physics Analysis and Forecast (3.1) — primary; OSCAR (3.2) as complementary surface-current source |
| Spatial reference | WGS84 (EPSG:4326); ~1/12° grid for selected Copernicus product |
| Temporal reference | Product-dependent; daily or sub-daily, spans analysis/forecast horizon |
| Quality flag | Source model metadata/error estimate where provided, else `null` |
| Freshness requirement | Near-real-time; must carry explicit `data_class` = analysis or forecast, never labeled as direct observation |
| Validation rule | Reject values outside -3.0–3.0 m/s without a documented mesoscale-event override; must be paired with `ocean_current_v` and never interpreted alone |
| Agent consuming it | Ocean Agent, Safety Agent, Geospatial Agent, Verification Agent |
| Database representation | TimescaleDB hypertable `ocean_current_observations` (`u_ms NUMERIC(5,3)`, `v_ms NUMERIC(5,3)`, `geom`, `valid_time`) |
| Example value | `0.340` |

### 2.3 `ocean_current_v`

| Attribute | Value |
|---|---|
| Field name | `ocean_current_v` |
| Description | Meridional (north–south) component of ocean current velocity |
| Data type | Float |
| Unit | m/s |
| Valid range | -3.0 to 3.0 |
| Nullable | Yes |
| Source dataset | Copernicus Marine Global Ocean Physics Analysis and Forecast (3.1); OSCAR (3.2) as complementary source |
| Spatial reference | WGS84 (EPSG:4326); ~1/12° grid |
| Temporal reference | Product-dependent; daily or sub-daily |
| Quality flag | Source model metadata/error estimate where provided, else `null` |
| Freshness requirement | Near-real-time; same data-class labeling requirement as `ocean_current_u` |
| Validation rule | Reject values outside -3.0–3.0 m/s without documented override; always paired with `ocean_current_u` |
| Agent consuming it | Ocean Agent, Safety Agent, Geospatial Agent, Verification Agent |
| Database representation | Same row as `ocean_current_u` in `ocean_current_observations` |
| Example value | `-0.120` |

### 2.4 `sea_level_height`

| Attribute | Value |
|---|---|
| Field name | `sea_level_height` |
| Description | Tide-influenced sea-surface height relative to global mean sea level, from global marine model output (not a coastal-navigation-grade tide table) |
| Data type | Float |
| Unit | Metres |
| Valid range | -3.0 to 3.0 (indicative; provider does not certify coastal accuracy) |
| Nullable | Yes |
| Source dataset | Open-Meteo Marine API sea-level-height field (6.1). Note: NOAA Tides and Currents (6.2) is explicitly excluded from this field's sourcing — catalog marks it unsuitable for Indian coastal locations |
| Spatial reference | WGS84 (EPSG:4326); source model ~0.08° |
| Temporal reference | Hourly, forecast-based |
| Quality flag | None (model output); must be labeled `data_class = forecast/model` |
| Freshness requirement | Hourly; source model updates daily per documentation |
| Validation rule | Must always be displayed with the catalog's explicit caveat that this field is not suitable for coastal navigation decisions |
| Agent consuming it | Safety Agent, Geospatial Agent |
| Database representation | TimescaleDB hypertable `sea_level_observations` (`sea_level_m NUMERIC(5,3)`, `geom`, `valid_time`) |
| Example value | `0.42` |

### 2.5 `bathymetric_depth`

| Attribute | Value |
|---|---|
| Field name | `bathymetric_depth` |
| Description | Seafloor depth/elevation at a given location |
| Data type | Float |
| Unit | Metres (negative = below sea level, per GEBCO convention) |
| Valid range | -11000 to 9000 (global ocean/land elevation extremes) |
| Nullable | No (GEBCO provides global coverage) |
| Source dataset | GEBCO 2026 Grid (7.1) |
| Spatial reference | WGS84 (EPSG:4326); 15 arc-second grid |
| Temporal reference | Static; annual versioned release |
| Quality flag | GEBCO Type Identifier Grid (indicates measured vs. interpolated/modelled source cell) |
| Freshness requirement | Static — refresh only on annual GEBCO release |
| Validation rule | Must retain the Type Identifier Grid value alongside depth; must never be used as a navigational-clearance or legal safety value (explicit catalog restriction) |
| Agent consuming it | Geospatial Agent, Safety Agent, Ocean Agent |
| Database representation | Raster table or `NUMERIC(7,1)` column keyed by `geom GEOMETRY(Point,4326)` in a static reference table `bathymetry_grid` |
| Example value | `-45.0` |

---

## 3. Waves and Wind (Safety)

### 3.1 `significant_wave_height`

| Attribute | Value |
|---|---|
| Field name | `significant_wave_height` |
| Description | Average height of the highest one-third of waves in the local wave field (Hs) |
| Data type | Float |
| Unit | Metres |
| Valid range | 0.0 to 20.0 |
| Nullable | Yes |
| Source dataset | Open-Meteo Marine Weather API (4.1) — primary for prototype; INCOIS operational ocean forecast (4.2) after access validation |
| Spatial reference | WGS84 (EPSG:4326); source model ~0.05°–0.25° |
| Temporal reference | Hourly forecast |
| Quality flag | None (model output); label `data_class = forecast` |
| Freshness requirement | Hourly; source model updates every 6–24 hours depending on underlying model |
| Validation rule | Reject negative values; values > 20.0 m require flagging for manual review rather than silent acceptance |
| Agent consuming it | Safety Agent |
| Database representation | TimescaleDB hypertable `wave_observations` (`hs_m NUMERIC(4,2)`, `period_s`, `direction_deg`, `geom`, `valid_time`) |
| Example value | `1.80` |

### 3.2 `wave_period`

| Attribute | Value |
|---|---|
| Field name | `wave_period` |
| Description | Period of the dominant/significant wave, required alongside height for meaningful safety assessment per `DOMAIN_KNOWLEDGE.md` (wave height alone is explicitly flagged as an insufficient safety indicator) |
| Data type | Float |
| Unit | Seconds |
| Valid range | 0.0 to 25.0 |
| Nullable | Yes |
| Source dataset | Open-Meteo Marine Weather API (4.1) |
| Spatial reference | WGS84 (EPSG:4326) |
| Temporal reference | Hourly forecast |
| Quality flag | None (model output); label `data_class = forecast` |
| Freshness requirement | Hourly |
| Validation rule | Reject values outside 0–25 s; must not be dropped even when `significant_wave_height` is low — Safety Agent requires both jointly |
| Agent consuming it | Safety Agent |
| Database representation | Same row as `significant_wave_height` (`period_s NUMERIC(4,1)`) |
| Example value | `6.50` |

### 3.3 `wave_direction`

| Attribute | Value |
|---|---|
| Field name | `wave_direction` |
| Description | Direction from which the dominant wave is traveling |
| Data type | Float |
| Unit | Degrees (compass, 0–360, direction-from convention) |
| Valid range | 0.0 to 360.0 |
| Nullable | Yes |
| Source dataset | Open-Meteo Marine Weather API (4.1) |
| Spatial reference | WGS84 (EPSG:4326) |
| Temporal reference | Hourly forecast |
| Quality flag | None (model output); label `data_class = forecast` |
| Freshness requirement | Hourly |
| Validation rule | Must be within 0–360; wrap-around at 360→0 must be handled explicitly in code, not truncated |
| Agent consuming it | Safety Agent |
| Database representation | Same row as `significant_wave_height` (`direction_deg NUMERIC(5,1)`) |
| Example value | `142.0` |

### 3.4 `wind_speed`

| Attribute | Value |
|---|---|
| Field name | `wind_speed` |
| Description | Near-surface wind speed |
| Data type | Float |
| Unit | m/s (canonical internal unit; source may report knots/km/h and must be normalized on ingestion) |
| Valid range | 0.0 to 60.0 |
| Nullable | Yes |
| Source dataset | ISRO EOS-06 scatterometer wind products (5.1) after access validation; Open-Meteo Weather Forecast API (5.2) as prototype-ready fallback |
| Spatial reference | WGS84 (EPSG:4326) |
| Temporal reference | Hourly (Open-Meteo) or ~12-hour repeat (EOS-06, pending validation) |
| Quality flag | Scatterometer ambiguity-removal/quality flag (EOS-06) or `null` (Open-Meteo model output) |
| Freshness requirement | Hourly for Open-Meteo; near-real-time pending validation for EOS-06 |
| Validation rule | Reject negative values; must record which source (`5.1` or `5.2`) produced the value, since accuracy/latency characteristics differ materially |
| Agent consuming it | Safety Agent, Ocean Agent |
| Database representation | TimescaleDB hypertable `wind_observations` (`speed_ms NUMERIC(5,2)`, `direction_deg`, `geom`, `valid_time`, `source_id`) |
| Example value | `7.20` |

### 3.5 `wind_direction`

| Attribute | Value |
|---|---|
| Field name | `wind_direction` |
| Description | Direction from which the wind is blowing |
| Data type | Float |
| Unit | Degrees (compass, 0–360) |
| Valid range | 0.0 to 360.0 |
| Nullable | Yes |
| Source dataset | ISRO EOS-06 scatterometer wind products (5.1); Open-Meteo Weather Forecast API (5.2) |
| Spatial reference | WGS84 (EPSG:4326) |
| Temporal reference | Same as `wind_speed` |
| Quality flag | Same as `wind_speed` |
| Freshness requirement | Same as `wind_speed` |
| Validation rule | Must be within 0–360 with explicit wrap-around handling |
| Agent consuming it | Safety Agent, Ocean Agent |
| Database representation | Same row as `wind_speed` (`direction_deg NUMERIC(5,1)`) |
| Example value | `210.0` |

---

## 4. Weather (General Atmospheric)

### 4.1 `precipitation`

| Attribute | Value |
|---|---|
| Field name | `precipitation` |
| Description | Forecast or observed precipitation amount, used as a contextual safety/hazard signal |
| Data type | Float |
| Unit | mm |
| Valid range | 0.0 to 500.0 (per reporting interval) |
| Nullable | Yes |
| Source dataset | Open-Meteo Weather Forecast and Historical APIs (10.1) — supplementary source only; IMD/INCOIS official warnings (10.2) take override priority when available |
| Spatial reference | WGS84 (EPSG:4326); model-dependent grid |
| Temporal reference | Hourly or daily |
| Quality flag | None (model output); label `data_class = forecast` |
| Freshness requirement | Hourly |
| Validation rule | Reject negative values; must never override an active IMD/INCOIS official warning |
| Agent consuming it | Safety Agent |
| Database representation | TimescaleDB hypertable `weather_observations` (`precipitation_mm NUMERIC(6,1)`, `weather_code`, `geom`, `valid_time`) |
| Example value | `4.20` |

### 4.2 `weather_condition_code`

| Attribute | Value |
|---|---|
| Field name | `weather_condition_code` |
| Description | Categorical weather condition code (e.g., clear, cloudy, thunderstorm) from the source model |
| Data type | Integer (source-defined code) |
| Unit | Not applicable |
| Valid range | Per Open-Meteo's documented weather-code enumeration |
| Nullable | Yes |
| Source dataset | Open-Meteo Weather Forecast and Historical APIs (10.1) |
| Spatial reference | WGS84 (EPSG:4326) |
| Temporal reference | Hourly or daily |
| Quality flag | None (model output); label `data_class = forecast` |
| Freshness requirement | Hourly |
| Validation rule | Must map only to Open-Meteo's documented code table; unmapped codes are stored raw and flagged, never guessed |
| Agent consuming it | Safety Agent |
| Database representation | Same row as `precipitation` (`weather_code SMALLINT`) |
| Example value | `61` (slight rain, per Open-Meteo's WMO code table) |

### 4.3 `official_marine_warning`

| Attribute | Value |
|---|---|
| Field name | `official_marine_warning` |
| Description | Presence and category of an official IMD/INCOIS marine hazard warning (cyclone, storm, sea-state danger) for the query region |
| Data type | Text/enum (`none`, `advisory`, `warning`, `severe_warning` — exact taxonomy requires validation against official product documentation) |
| Unit | Not applicable |
| Valid range | Enumerated categories only |
| Nullable | No — must default to `none` only when a check against the source has actually run, never as a silent absence |
| Source dataset | IMD and INCOIS marine warnings (10.2) — **Requires validation**: official machine-readable access mechanism (portal, CAP feed, bulletin) is not yet confirmed |
| Spatial reference | Warning-polygon or named-region dependent (source format TBD) |
| Temporal reference | Event-driven; carries its own validity period, issue time, revision number |
| Quality flag | Source agency, revision number, issue time |
| Freshness requirement | Real-time to near-real-time; treat any check older than the source's stated bulletin cycle as stale and re-fetch before answering a safety query |
| Validation rule | Per catalog Section 10.2 policy: **must override** a favorable PFZ/ecosystem signal whenever present; ORCA Coordinator must not present a fishing recommendation without checking this field first |
| Agent consuming it | Safety Agent, Verification Agent, ORCA Coordinator |
| Database representation | `warnings` table (`region GEOMETRY` or `region_code TEXT`, `category TEXT`, `issued_at TIMESTAMPTZ`, `valid_until TIMESTAMPTZ`, `revision INT`) |
| Example value | `advisory` |

---

## 5. Ecosystem

### 5.1 `chlorophyll_a_concentration`

| Attribute | Value |
|---|---|
| Field name | `chlorophyll_a_concentration` |
| Description | Satellite-derived estimate of chlorophyll-a concentration, used as a proxy for phytoplankton biomass — never as a direct measure of fish abundance (explicit `DOMAIN_KNOWLEDGE.md` guardrail) |
| Data type | Float |
| Unit | mg/m³ |
| Valid range | 0.01 to 100.0 (typical open-ocean-to-coastal range; coastal waters can be optically complex and less reliable) |
| Nullable | Yes (cloud cover and atmospheric-correction failure are common) |
| Source dataset | NASA Ocean Color chlorophyll-a products (2.1) — primary; ISRO EOS-06/Oceansat-3 OCM-3 (2.2) as geographically relevant complementary source pending access validation |
| Spatial reference | WGS84 (EPSG:4326); sensor-dependent, commonly hundreds of metres to a few km |
| Temporal reference | Daily, 8-day, or monthly composite depending on selected product |
| Quality flag | Source cloud/land/glint/atmospheric-correction/algorithm-failure flags — must be retained, not discarded |
| Freshness requirement | Near-real-time (daily composite preferred); reject use of a composite older than its stated compositing window without labeling it as such |
| Validation rule | Reject non-positive values; any recommendation using this field must explicitly avoid the phrase "high chlorophyll means fish" per Guardrail 1 in `DOMAIN_KNOWLEDGE.md` |
| Agent consuming it | Ecosystem Agent, Fisheries Agent, Verification Agent |
| Database representation | TimescaleDB hypertable `chlorophyll_observations` (`chl_a_mgm3 NUMERIC(6,3)`, `geom`, `valid_time`, `quality_flag`) |
| Example value | `0.850` |

### 5.2 `sst_anomaly`

| Attribute | Value |
|---|---|
| Field name | `sst_anomaly` |
| Description | Difference between observed SST and the climatological baseline for the same location and time of year; the base signal for marine heat-wave detection |
| Data type | Float |
| Unit | °C |
| Valid range | -10.0 to 10.0 |
| Nullable | Yes (depends on `sea_surface_temperature` and baseline availability) |
| Source dataset | Derived internally from `sea_surface_temperature` (Section 2.1), per the ORCA-derived marine heat-wave indicator (9.1); NOAA OISST v2.1 (1.3) recommended for the historical baseline |
| Spatial reference | Inherits the spatial reference of the selected SST source |
| Temporal reference | Inherits the temporal cadence of the selected SST source, commonly daily |
| Quality flag | Inherits source SST quality flags plus ORCA-added flags for missing data, cloud gaps, interpolation, and baseline coverage |
| Freshness requirement | Recomputed whenever the underlying SST source updates |
| Validation rule | Must document the exact climatological baseline period used; must never be labeled an "observed event" if it derives from a forecast SST value |
| Agent consuming it | Ecosystem Agent, Verification Agent |
| Database representation | TimescaleDB hypertable `sst_anomaly_derived` (`anomaly_c NUMERIC(5,2)`, `baseline_period TEXT`, `geom`, `valid_time`) |
| Example value | `1.80` |

### 5.3 `mhw_event_category`

| Attribute | Value |
|---|---|
| Field name | `mhw_event_category` |
| Description | Marine heat-wave intensity category (e.g., moderate, strong, severe, extreme) assigned by the adopted MHW detection methodology |
| Data type | Text/enum |
| Unit | Not applicable |
| Valid range | Categories defined by the specific published MHW methodology ORCA adopts (methodology selection is a Category C / requires-validation item) |
| Nullable | Yes (only populated when `sst_anomaly` exceeds the methodology's threshold for the minimum qualifying duration) |
| Source dataset | Derived internally (9.1), cross-referenced against Copernicus Marine heat-wave bulletin (9.2) for validation, not as a live API-ready feed |
| Spatial reference | Inherits `sst_anomaly` spatial reference |
| Temporal reference | Event-based; spans the qualifying duration, not a single timestamp |
| Quality flag | Data completeness and confidence flags per the 9.1 derived-product schema |
| Freshness requirement | Recomputed whenever underlying SST/anomaly data updates |
| Validation rule | Must not be populated unless the adopted methodology's minimum-duration threshold is met; must always be labeled as ORCA-derived, not sourced directly from an external MHW feed |
| Agent consuming it | Ecosystem Agent, Verification Agent |
| Database representation | Column on `sst_anomaly_derived` (`mhw_category TEXT NULL`, `event_duration_days SMALLINT NULL`) |
| Example value | `moderate` |

---

## 6. Fisheries

### 6.1 `pfz_geometry`

| Attribute | Value |
|---|---|
| Field name | `pfz_geometry` |
| Description | Spatial location/extent of an advised Potential Fishing Zone |
| Data type | Geometry (point, line, or polygon depending on advisory format) |
| Unit | Decimal degrees (WGS84) |
| Valid range | Must fall within Indian EEZ / advisory coverage region |
| Nullable | No, when a PFZ record exists |
| Source dataset | INCOIS Potential Fishing Zone Advisory (8.1) — **Requires validation**: machine-readable format and official API access not yet confirmed |
| Spatial reference | WGS84 (EPSG:4326); advisory/product-dependent precision |
| Temporal reference | Tied to `pfz_issued_at` / `pfz_valid_until` below |
| Quality flag | Advisory validity period, issue time, product version, cloud/data-availability notes |
| Freshness requirement | Daily operational advisory cadence (to be confirmed with INCOIS) |
| Validation rule | Must never be converted into a guarantee of catch — must always carry `pfz_prospect_category` and be subordinate to `official_marine_warning` when the two conflict |
| Agent consuming it | Fisheries Agent, Geospatial Agent, Verification Agent |
| Database representation | `pfz_advisories` table (`geom GEOMETRY(Geometry,4326)`, `prospect_category TEXT`, `issued_at TIMESTAMPTZ`, `valid_until TIMESTAMPTZ`, `source_version TEXT`) |
| Example value | `POINT(80.35 13.10)` |

### 6.2 `pfz_prospect_category`

| Attribute | Value |
|---|---|
| Field name | `pfz_prospect_category` |
| Description | Advisory's fishing-prospect classification for the associated `pfz_geometry` |
| Data type | Text/enum |
| Unit | Not applicable |
| Valid range | Per INCOIS's official advisory taxonomy (**requires validation**) |
| Nullable | No, when a PFZ record exists |
| Source dataset | INCOIS Potential Fishing Zone Advisory (8.1) |
| Spatial reference | Tied to `pfz_geometry` |
| Temporal reference | Tied to `pfz_issued_at` / `pfz_valid_until` |
| Quality flag | Same as `pfz_geometry` |
| Freshness requirement | Same as `pfz_geometry` |
| Validation rule | Must be displayed alongside the fixed disclaimer distinguishing "potential" from "guaranteed" fishing zone, per the catalog's Critical ORCA Rule |
| Agent consuming it | Fisheries Agent, ORCA Coordinator |
| Database representation | Column on `pfz_advisories` (`prospect_category TEXT`) |
| Example value | `favourable` |

### 6.3 `pfz_issued_at` / `pfz_valid_until`

| Attribute | Value |
|---|---|
| Field name | `pfz_issued_at`, `pfz_valid_until` |
| Description | Issue timestamp and validity-expiry timestamp of the PFZ advisory |
| Data type | Timestamp with time zone (both fields) |
| Unit | ISO-8601 |
| Valid range | `pfz_valid_until` must be later than `pfz_issued_at` |
| Nullable | No, when a PFZ record exists |
| Source dataset | INCOIS Potential Fishing Zone Advisory (8.1) |
| Spatial reference | Not applicable |
| Temporal reference | IST/UTC per source publication convention (to be confirmed) |
| Quality flag | Advisory issue time and revision metadata |
| Freshness requirement | Must be re-checked against current time before every use; an expired advisory must not be presented as current |
| Validation rule | Reject or flag any PFZ record where `query_timestamp` falls outside `[pfz_issued_at, pfz_valid_until]` |
| Agent consuming it | Fisheries Agent, Verification Agent, ORCA Coordinator |
| Database representation | Columns on `pfz_advisories` (`issued_at TIMESTAMPTZ`, `valid_until TIMESTAMPTZ`) |
| Example value | `2026-08-30T05:30:00+05:30` / `2026-08-31T05:30:00+05:30` |

### 6.4 `historical_catch_tonnes`

| Attribute | Value |
|---|---|
| Field name | `historical_catch_tonnes` |
| Description | Annual aggregate capture-production figure for context in Scientist/Government-mode analytics — not used for daily fishing-route recommendations |
| Data type | Float |
| Unit | Tonnes |
| Valid range | ≥ 0 |
| Nullable | Yes |
| Source dataset | FAO FishStatJ global fisheries statistics (8.2) — Tier 3 (research/context), not part of the live decision-support pipeline |
| Spatial reference | Country / FAO fishing-area / reporting-unit level — not fine-scale coordinates |
| Temporal reference | Annual |
| Quality flag | FAO reporting-status metadata (estimated vs. reported values, aggregation notes) |
| Freshness requirement | Annual release cycle; not required to be fresher than the latest published FAO release |
| Validation rule | Must never be combined with daily `pfz_geometry`/`pfz_prospect_category` data without explicitly labeling the difference in temporal and spatial scale |
| Agent consuming it | Fisheries Agent (Government/Scientist mode only), Knowledge/RAG Agent |
| Database representation | `fisheries_statistics_annual` table (`reporting_area TEXT`, `year SMALLINT`, `catch_tonnes NUMERIC(12,2)`, `is_estimated BOOLEAN`) |
| Example value | `412500.00` |

---

## 7. Satellite Imagery (Map UI)

### 7.1 `satellite_imagery_layer_ref`

| Attribute | Value |
|---|---|
| Field name | `satellite_imagery_layer_ref` |
| Description | Reference (tile URL / layer identifier) to a rendered satellite imagery layer for map visualization — a visual aid, not an analysis-grade data source |
| Data type | Text (URL/URI) |
| Unit | Not applicable |
| Valid range | Must resolve to a documented NASA Worldview or MOSDAC browse endpoint |
| Nullable | Yes |
| Source dataset | NASA Worldview / Earthdata browse products (11.1) — primary; MOSDAC browse products (11.2) as India-relevant complementary source, subject to service-health validation |
| Spatial reference | Web-Mercator tile grid (EPSG:3857) typical for browse imagery, or source-native projection — to be confirmed per endpoint |
| Temporal reference | Daily for most eligible layers; mission/layer dependent |
| Quality flag | None applicable to rendered imagery; underlying scientific products (used for actual analysis) carry their own flags separately |
| Freshness requirement | Daily; MOSDAC layers require an active health check per catalog's explicit staleness-notice requirement |
| Validation rule | Must never be used to derive quantitative SST/chlorophyll values — imagery is for display only, per catalog's explicit implementation note |
| Agent consuming it | Ecosystem Agent (context only), Map UI |
| Database representation | `imagery_layers` table (`layer_id TEXT`, `tile_url TEXT`, `source TEXT`, `layer_date DATE`, `status TEXT`) |
| Example value | `https://worldview.earthdata.nasa.gov/.../MODIS_Terra_CorrectedReflectance_TrueColor/.../2026-08-30` |

---

## 8. Provenance / Data-Quality Envelope

Per `DATA_SOURCE_CATALOG.md` Section 12, every ingested record — regardless of parameter — must carry this metadata envelope. These are not optional per-parameter extras; they are structural fields on every observation/derived-product row.

### 8.1 `source_provider`

| Attribute | Value |
|---|---|
| Field name | `source_provider` |
| Description | Name of the organization/service that produced the underlying data |
| Data type | Text |
| Unit | Not applicable |
| Valid range | One of the catalog's documented providers (Copernicus Marine, NASA OB.DAAC, NOAA, ISRO/MOSDAC, INCOIS, Open-Meteo, GEBCO, FAO, IMD) |
| Nullable | No |
| Source dataset | Set at ingestion time from the catalog entry used |
| Spatial reference | Not applicable |
| Temporal reference | Not applicable |
| Quality flag | Not applicable |
| Freshness requirement | Not applicable (static per record) |
| Validation rule | Must match a provider name present in `DATA_SOURCE_CATALOG.md`; unrecognized providers are rejected at ingestion |
| Agent consuming it | Verification Agent, all domain agents (for citation) |
| Database representation | `TEXT` column on every observation/derived-product table |
| Example value | `Copernicus Marine Service` |

### 8.2 `dataset_id`

| Attribute | Value |
|---|---|
| Field name | `dataset_id` |
| Description | Exact selected product/dataset identifier used for this record (not a generic provider name) |
| Data type | Text |
| Unit | Not applicable |
| Valid range | Must correspond to a specific product ID documented at implementation time |
| Nullable | No |
| Source dataset | Set at ingestion time |
| Spatial reference | Not applicable |
| Temporal reference | Not applicable |
| Quality flag | Not applicable |
| Freshness requirement | Not applicable |
| Validation rule | Must be specific enough to reproduce the exact query against the source (per catalog's reproducibility requirement) |
| Agent consuming it | Verification Agent |
| Database representation | `TEXT` column on every observation/derived-product table |
| Example value | `cmems_obs-sst_glo_phy_nrt_l4_P1D-m` |

### 8.3 `retrieved_at`

| Attribute | Value |
|---|---|
| Field name | `retrieved_at` |
| Description | Timestamp at which ORCA fetched/ingested this record |
| Data type | Timestamp with time zone |
| Unit | ISO-8601 |
| Valid range | Not in the future |
| Nullable | No |
| Source dataset | Set by ingestion pipeline |
| Spatial reference | Not applicable |
| Temporal reference | UTC |
| Quality flag | Not applicable |
| Freshness requirement | Not applicable (this field defines freshness for other fields) |
| Validation rule | Used to compute `staleness_status` against each source's documented update latency |
| Agent consuming it | Verification Agent |
| Database representation | `TIMESTAMPTZ` column on every observation/derived-product table |
| Example value | `2026-08-30T14:05:00Z` |

### 8.4 `valid_time_start` / `valid_time_end`

| Attribute | Value |
|---|---|
| Field name | `valid_time_start`, `valid_time_end` |
| Description | The time window for which the value is asserted to be valid (a single instant has `valid_time_start = valid_time_end`) |
| Data type | Timestamp with time zone (both fields) |
| Unit | ISO-8601 |
| Valid range | `valid_time_end` ≥ `valid_time_start` |
| Nullable | No |
| Source dataset | Set from source product metadata at ingestion |
| Spatial reference | Not applicable |
| Temporal reference | UTC |
| Quality flag | Not applicable |
| Freshness requirement | Not applicable |
| Validation rule | Data outside its validity window at query time must be rejected or clearly flagged (per catalog's mandatory verification rules) |
| Agent consuming it | Verification Agent, ORCA Coordinator |
| Database representation | `TIMESTAMPTZ` columns on every observation/derived-product table |
| Example value | `2026-08-30T00:00:00Z` / `2026-08-30T23:59:59Z` |

### 8.5 `data_class`

| Attribute | Value |
|---|---|
| Field name | `data_class` |
| Description | Classifies whether the value is an observation, analysis, forecast, reanalysis, or ORCA-derived product |
| Data type | Text/enum |
| Unit | Not applicable |
| Valid range | `observation`, `analysis`, `forecast`, `reanalysis`, `derived` |
| Nullable | No |
| Source dataset | Set from source product metadata / derivation logic at ingestion |
| Spatial reference | Not applicable |
| Temporal reference | Not applicable |
| Quality flag | Not applicable |
| Freshness requirement | Not applicable |
| Validation rule | Must never mix classes in a single displayed comparison without labeling each; forecast values must never be displayed as though observed (catalog's mandatory rule) |
| Agent consuming it | Verification Agent, ORCA Coordinator, all domain agents |
| Database representation | `TEXT` column (or `SMALLINT` enum reference) on every observation/derived-product table |
| Example value | `forecast` |

### 8.6 `quality_flag`

| Attribute | Value |
|---|---|
| Field name | `quality_flag` |
| Description | Source-reported quality/control indicator for the record, if the source provides one |
| Data type | Text |
| Unit | Not applicable |
| Valid range | Source-specific (varies per provider/product) |
| Nullable | Yes — but a missing flag must be treated as an uncertainty signal, never as proof of validity (explicit catalog rule) |
| Source dataset | Set from source product metadata at ingestion |
| Spatial reference | Not applicable |
| Temporal reference | Not applicable |
| Quality flag | Self-referential — this is the flag |
| Freshness requirement | Not applicable |
| Validation rule | A `null` value here must lower downstream confidence scoring, not be silently ignored |
| Agent consuming it | Verification Agent |
| Database representation | `TEXT NULL` column on every observation/derived-product table |
| Example value | `good` |

### 8.7 `uncertainty`

| Attribute | Value |
|---|---|
| Field name | `uncertainty` |
| Description | Source-reported uncertainty/error estimate for the value, if provided |
| Data type | Float |
| Unit | Same unit as the parent field |
| Valid range | ≥ 0 |
| Nullable | Yes |
| Source dataset | Set from source product metadata at ingestion |
| Spatial reference | Not applicable |
| Temporal reference | Not applicable |
| Quality flag | Not applicable |
| Freshness requirement | Not applicable |
| Validation rule | Must not be fabricated when absent from the source — store `null`, never a guessed value (per master document's "never invent performance metrics" rule) |
| Agent consuming it | Verification Agent |
| Database representation | `NUMERIC NULL` column on every observation/derived-product table |
| Example value | `0.40` |

### 8.8 `staleness_status`

| Attribute | Value |
|---|---|
| Field name | `staleness_status` |
| Description | Computed status describing whether the record is current relative to its source's expected update cadence |
| Data type | Text/enum |
| Unit | Not applicable |
| Valid range | `fresh`, `delayed`, `stale`, `unavailable` |
| Nullable | No |
| Source dataset | Computed by the ingestion pipeline from `retrieved_at`, `valid_time_end`, and the source's documented update frequency |
| Spatial reference | Not applicable |
| Temporal reference | Not applicable |
| Quality flag | Not applicable |
| Freshness requirement | Self-referential — this field is the freshness indicator |
| Validation rule | `stale` or `unavailable` records must trigger an explicit warning in any user-facing response that relies on them, per catalog Section 12 (MOSDAC staleness example) |
| Agent consuming it | Verification Agent, ORCA Coordinator, Map UI (source-status badge) |
| Database representation | `TEXT` column, recomputed on read or via a scheduled job |
| Example value | `fresh` |

---

## 9. Items Requiring Validation Before Implementation

Consistent with Category C of the ORCA master context document, the following are known gaps rather than invented facts:

- **INCOIS PFZ machine-readable access** (`pfz_geometry`, `pfz_prospect_category`, `pfz_issued_at`, `pfz_valid_until`) — official API/format not yet confirmed.
- **IMD/INCOIS official warning feed format** (`official_marine_warning`) — access mechanism (portal, CAP feed, bulletin) not yet confirmed.
- **ISRO EOS-06/MOSDAC product-level access** (`wind_speed`/`wind_direction` primary source, `chlorophyll_a_concentration` complementary source) — registration requirements and current service health not yet confirmed; MOSDAC has displayed notices that some services are not updating.
- **MHW detection methodology** (`mhw_event_category`) — specific published threshold/percentile methodology to be selected and documented before implementation.
- **Satellite imagery tile access terms** (`satellite_imagery_layer_ref`) — exact endpoint/authentication requirements for NASA Worldview and MOSDAC browse products to be confirmed.

No numeric accuracy, latency, or coverage claim in this dictionary should be treated as tested until validated against live source access.