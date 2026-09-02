# DATA_SOURCE_CATALOG.md

# ORCA Data Source Catalog

**Project:** SIH26176 – ORCA  
**Full Name:** Marine Ecosystems Reasoning with Collaborative Agents  
**Purpose:** Catalog of real, authoritative, currently accessible or officially documented datasets/services suitable for an ORCA prototype focused on Indian coastal waters, the Bay of Bengal, and the Arabian Sea.

**Catalog status:** Prototype planning reference, not an implementation guarantee.  
**Last reviewed:** August 30, 2026.

---

## Scope and usage rules

ORCA should prefer authoritative operational providers such as INCOIS, ISRO/MOSDAC, NASA, NOAA, Copernicus Marine, GEBCO, and IMD where access is available.

A source being listed here does **not** mean ORCA can claim real-time coverage, numerical accuracy, or API availability without testing access, latency, licensing, and data quality during implementation.

### Status labels

- **REAL-TIME:** Observation or operational feed intended to represent current conditions with low latency.
- **NEAR-REAL-TIME:** Data is processed and released after operational latency, usually hours to days.
- **HISTORICAL:** Archive, reanalysis, climatology, or delayed-mode dataset.
- **STATIC:** Dataset changes infrequently, such as bathymetry or coastline geometry.
- **FORECAST:** Model-generated future conditions. Forecasts must never be presented as observations.

---

## Recommended prototype dataset set

For a practical SIH prototype, ORCA should begin with a controlled combination of the following sources:

| Requirement | Recommended primary source | Backup / complementary source | ORCA agent |
|---|---|---|---|
| SST | Copernicus Marine global SST or NASA OB.DAAC | ISRO EOS-06/MOSDAC where accessible | Ocean Agent, Ecosystem Agent |
| Chlorophyll-a | NASA Ocean Color / OB.DAAC | ISRO EOS-06 OCM-3 / MOSDAC | Ecosystem Agent, Fisheries Agent |
| Ocean currents | Copernicus Marine Global Ocean Physics | Open-Meteo Marine for prototype point forecasts | Ocean Agent, Geospatial Agent |
| Wave height | Copernicus Marine wave products or Open-Meteo Marine | INCOIS operational forecast after access validation | Safety Agent |
| Wind | Copernicus Marine / weather forecast provider | MOSDAC scatterometer products where accessible | Safety Agent, Ocean Agent |
| Tides | Open-Meteo Marine for indicative global model output | INCOIS coastal forecast after access validation | Safety Agent, Geospatial Agent |
| Bathymetry | GEBCO 2026 Grid | Indian nautical/hydrographic data only when authorized | Geospatial Agent |
| PFZ | INCOIS PFZ advisories | Demo-layer archive/manual ingestion if permitted | Fisheries Agent |
| Marine heat waves | Derived from SST anomaly baseline | Copernicus Marine bulletin and SST forecast context | Ecosystem Agent |
| Weather | Open-Meteo Weather API for prototype | IMD / INCOIS warnings after access validation | Safety Agent |
| Fisheries | INCOIS PFZ and authorized landing/catch records | FAO FishStatJ for historical aggregate context | Fisheries Agent |
| Satellite imagery | NASA Ocean Color imagery and EOS-06 OCM-3 products | NASA Worldview / MOSDAC browse products | Ecosystem Agent, Map UI |

---

# 1. Sea Surface Temperature

## 1.1 Copernicus Marine Global SST Products

| Field | Details |
|---|---|
| **Dataset name** | Copernicus Marine global sea-surface temperature products, including Level-4 satellite observation and global analysis/forecast SST products |
| **Provider** | Copernicus Marine Service, implemented by Mercator Ocean International for the European Union |
| **Status** | **NEAR-REAL-TIME**, **HISTORICAL**, and **FORECAST**, depending on selected product |
| **Official URL** | https://data.marine.copernicus.eu/ |
| **Download/API** | Copernicus Marine Data Store; Copernicus Marine Toolbox supports product discovery, metadata access, subsetting, and download. Registration may be required for download functionality. |
| **Format** | Primarily NetCDF; programmatic workflows supported through Copernicus Marine Toolbox and Python-compatible tools |
| **Spatial resolution** | Product-dependent. Global SST products commonly include approximately 0.05 degree to 0.25 degree grids; exact resolution must be confirmed from selected product metadata |
| **Temporal resolution** | Product-dependent; daily analyses, hourly to daily forecast products, and historical reanalysis products are available |
| **Coverage** | Global ocean, including Bay of Bengal, Arabian Sea, and Indian Ocean |
| **Update frequency** | Product-dependent; operational forecast products are updated regularly, while reanalysis products are updated less frequently |
| **Variables** | Sea surface temperature, SST uncertainty or error estimates where provided, quality-control metadata, analysis/forecast fields depending on product |
| **Units** | Usually degrees Celsius or Kelvin; confirm from NetCDF metadata before use |
| **License** | Copernicus Marine terms of use and attribution requirements apply; confirm the selected product licence before redistribution |
| **Quality flags** | Product-dependent. Use quality-control variables, uncertainty fields, observation flags, and metadata supplied with each product |
| **Historical availability** | Yes; historical SST and reanalysis products are available |
| **Real-time availability** | Operational products are generally near-real-time rather than instantaneous real-time |
| **Prototype suitability** | **High.** Strong primary SST source for an Indian Ocean prototype because it supports historical, current, and forecast reasoning |
| **Agent using it** | Ocean Agent, Ecosystem Agent, Fisheries Agent, Verification Agent |
| **Implementation note** | Use one explicitly selected product ID and document its update latency, resolution, valid time, and uncertainty field in the prototype |

Copernicus Marine combines satellite observations, in-situ observations, and numerical models to provide ocean-state information and makes data available through the Marine Data Store. Its Toolbox supports metadata exploration, subsetting, and download workflows. [16][21][24]

---

## 1.2 NASA OB.DAAC Ocean Color and SST Products

| Field | Details |
|---|---|
| **Dataset name** | NASA Ocean Biology Distributed Active Archive Center ocean-color and sea-surface-temperature products |
| **Provider** | NASA Goddard Space Flight Center, Ocean Biology Processing Group and Ocean Biology DAAC |
| **Status** | **NEAR-REAL-TIME** and **HISTORICAL**, depending on sensor and processing level |
| **Official URL** | https://www.earthdata.nasa.gov/centers/ob-daac |
| **Download/API** | NASA Earthdata and Ocean Color Web; users generally need NASA Earthdata authentication for many downloads |
| **Format** | NetCDF, HDF, mapped imagery, Level-2/Level-3/Level-4 products depending on mission |
| **Spatial resolution** | Sensor and product dependent; MODIS, VIIRS, Sentinel-3 OLCI, GOCI, and other missions have different native and mapped resolutions |
| **Temporal resolution** | Daily, multi-day, monthly, and mission-specific composites |
| **Coverage** | Global ocean, including Indian coastal waters |
| **Update frequency** | Depends on mission, processing level, and product generation pipeline |
| **Variables** | SST, chlorophyll-a, remote-sensing reflectance, particulate and phytoplankton optical properties, absorption/scattering products, quality flags |
| **Units** | SST generally degrees Celsius; chlorophyll-a generally mg/m³; verify product metadata |
| **License** | NASA Earth science data are generally openly available, subject to Earthdata access terms, attribution, and product-specific documentation |
| **Quality flags** | Yes. Use sensor/product quality flags, cloud masking, land masking, glint flags, atmospheric-correction flags, and uncertainty variables where available |
| **Historical availability** | Yes; multi-mission archives provide long historical records |
| **Real-time availability** | Near-real-time availability varies by sensor and processing stream |
| **Prototype suitability** | **High.** Best authoritative complementary source for SST and chlorophyll-a, especially for historical baseline analysis |
| **Agent using it** | Ocean Agent, Ecosystem Agent, Knowledge/RAG Agent, Verification Agent |
| **Implementation note** | Use Level-3 mapped products for rapid prototype integration; use Level-2 only when detailed pixel-level analysis is necessary |

NASA’s OB.DAAC archives and distributes ocean-color observations from satellite, airborne, shipborne, autonomous in-situ, and model-derived sources. [34]

---

## 1.3 NOAA Optimum Interpolation SST

| Field | Details |
|---|---|
| **Dataset name** | NOAA Optimum Interpolation Sea Surface Temperature, version 2.1 |
| **Provider** | NOAA, with data commonly distributed through NOAA Physical Sciences Laboratory and associated NOAA services |
| **Status** | **NEAR-REAL-TIME** and **HISTORICAL** |
| **Official URL** | https://psl.noaa.gov/ |
| **Download/API** | Official distribution methods vary by hosting service; verify current NOAA dataset landing page and access method before implementation |
| **Format** | Commonly NetCDF |
| **Spatial resolution** | Approximately 0.25 degree for the OISST v2.1 gridded product |
| **Temporal resolution** | Daily |
| **Coverage** | Global ocean |
| **Update frequency** | Daily operational update cycle |
| **Variables** | Analysed SST, SST anomaly, error estimates, sea-ice concentration depending on product version |
| **Units** | Degrees Celsius |
| **License** | NOAA public data policy generally supports open access; cite the dataset and verify product-specific terms |
| **Quality flags** | Product includes analysis and error-related variables; consult dataset documentation |
| **Historical availability** | Yes; long historical record |
| **Real-time availability** | Operationally updated daily; treat as near-real-time |
| **Prototype suitability** | **High** for historical anomaly detection and marine heat-wave baseline calculations |
| **Agent using it** | Ocean Agent, Ecosystem Agent, Verification Agent |
| **Implementation note** | Suitable for a robust SST anomaly baseline, but not a replacement for higher-resolution local satellite products |

NOAA OISST v2.1 is used alongside other SST products in Copernicus Marine heat-wave monitoring workflows. [102]

---

# 2. Chlorophyll-a and Ocean Color

## 2.1 NASA Ocean Color Chlorophyll-a Products

| Field | Details |
|---|---|
| **Dataset name** | NASA Ocean Color chlorophyll-a products from MODIS, VIIRS, Sentinel-3 OLCI, SeaHawk-HawkEye, GOCI, and other supported missions |
| **Provider** | NASA OB.DAAC / Ocean Biology Processing Group |
| **Status** | **NEAR-REAL-TIME** and **HISTORICAL** |
| **Official URL** | https://oceancolor.gsfc.nasa.gov/ |
| **Download/API** | NASA Earthdata / Ocean Color Web data access; authentication may be required |
| **Format** | NetCDF, HDF, imagery and gridded composite products |
| **Spatial resolution** | Sensor-dependent; commonly hundreds of metres to several kilometres for mapped products |
| **Temporal resolution** | Daily, 8-day, monthly, and sensor-specific composite windows |
| **Coverage** | Global ocean |
| **Update frequency** | Mission and processing-stream dependent |
| **Variables** | Chlorophyll-a concentration, remote-sensing reflectance, phytoplankton absorption, particulate backscattering, ocean-colour quality flags |
| **Units** | Chlorophyll-a usually mg/m³ |
| **License** | NASA Earthdata/open science access conditions; attribution required |
| **Quality flags** | Yes. Cloud, land, glint, atmospheric correction, algorithm failure, and other flags are supplied depending on product |
| **Historical availability** | Yes; multi-decadal archive across multiple satellite missions |
| **Real-time availability** | Near-real-time product availability varies by sensor |
| **Prototype suitability** | **High.** Essential ecosystem productivity indicator for ORCA prototype |
| **Agent using it** | Ecosystem Agent, Fisheries Agent, Verification Agent |
| **Implementation note** | Do not treat chlorophyll-a as a direct measure of fish abundance. Use it as one ecological indicator alongside SST, fronts, PFZ, currents, seasonality, and safety constraints |

NASA states that ocean-color data support research on phytoplankton, harmful algal blooms, ocean health, and carbon-cycle processes. [40]

---

## 2.2 ISRO EOS-06 / Oceansat-3 OCM-3 Products

| Field | Details |
|---|---|
| **Dataset name** | EOS-06 / Oceansat-3 Ocean Colour Monitor-3 data products |
| **Provider** | Indian Space Research Organisation; access and archive services may be provided through MOSDAC, NRSC/Bhuvan, or other official ISRO channels |
| **Status** | **NEAR-REAL-TIME** and **HISTORICAL** subject to product availability |
| **Official URL** | https://www.isro.gov.in/ |
| **Download/API** | Use official ISRO, MOSDAC, Bhuvan, or Bhoonidhi access portals; verify account requirements and product-level availability before implementation |
| **Format** | Product-dependent; commonly scientific geospatial formats such as HDF, NetCDF, GeoTIFF, or browse imagery |
| **Spatial resolution** | Product dependent; verify exact OCM-3 processing-level documentation before use |
| **Temporal resolution** | Oceansat-3 mission documentation indicates repeated global observations for ocean-colour monitoring; confirm specific product cadence and usable cloud-free coverage |
| **Coverage** | Global ocean with high relevance for Indian EEZ and surrounding seas |
| **Update frequency** | Operational processing and dissemination dependent |
| **Variables** | Ocean-colour reflectance and derived products such as chlorophyll-a; product availability must be verified |
| **Units** | Product-dependent; chlorophyll-a generally mg/m³ where supplied |
| **License** | ISRO/MOSDAC terms and data policy apply |
| **Quality flags** | Product dependent; inspect quality layers and metadata before scientific use |
| **Historical availability** | EOS-06 data available from the mission period onward; earlier continuity may come from Oceansat-2 and other sensors |
| **Real-time availability** | Near-real-time status must be confirmed for each distribution service |
| **Prototype suitability** | **High after access validation.** Indigenous and geographically relevant source for Indian waters |
| **Agent using it** | Ecosystem Agent, Fisheries Agent, Ocean Agent, Verification Agent |
| **Implementation note** | Treat MOSDAC/ISRO availability as a validation item. Build a fallback using NASA or Copernicus chlorophyll products so the prototype remains demonstrable if a service is unavailable |

EOS-06/Oceansat-3 supports ocean-colour and surface-wind observation and continues India’s Oceansat mission series. [43]

---

# 3. Ocean Currents

## 3.1 Copernicus Marine Global Ocean Physics Analysis and Forecast

| Field | Details |
|---|---|
| **Dataset name** | Copernicus Marine Global Ocean Physics Analysis and Forecast products |
| **Provider** | Copernicus Marine Service / Mercator Ocean International |
| **Status** | **FORECAST**, **NEAR-REAL-TIME**, and **HISTORICAL** through analysis and reanalysis product families |
| **Official URL** | https://data.marine.copernicus.eu/ |
| **Download/API** | Copernicus Marine Data Store and Copernicus Marine Toolbox |
| **Format** | NetCDF; remote subsetting and programmatic access supported |
| **Spatial resolution** | Product-dependent; global physics products commonly provide fine global grids, often around 1/12 degree for selected reanalysis/forecast systems |
| **Temporal resolution** | Product-dependent; daily or sub-daily fields may be available |
| **Coverage** | Global ocean, including Bay of Bengal and Arabian Sea |
| **Update frequency** | Forecast and analysis products are updated operationally; verify selected product metadata |
| **Variables** | Zonal current velocity, meridional current velocity, temperature, salinity, sea-surface height, mixed-layer depth, and related model variables depending on product |
| **Units** | Current components commonly m/s; temperature degrees Celsius; sea level metres |
| **License** | Copernicus Marine terms, attribution, and access requirements apply |
| **Quality flags** | Model products include metadata and may include error estimates or quality indicators; consult product documentation |
| **Historical availability** | Yes, through reanalysis products such as GLORYS families |
| **Real-time availability** | Operational analysis/forecast products are near-real-time, not direct in-situ real-time observations |
| **Prototype suitability** | **High.** Strong source for currents, SST context, MLD, SSH, and forecast-aware reasoning |
| **Agent using it** | Ocean Agent, Safety Agent, Geospatial Agent, Verification Agent |
| **Implementation note** | Ensure ORCA clearly labels current fields as model analysis or forecast rather than measured current observations |

Copernicus Marine distributes ocean products derived from satellite and in-situ observations as well as numerical models. [21][24]

---

## 3.2 OSCAR Ocean Surface Current Analyses

| Field | Details |
|---|---|
| **Dataset name** | OSCAR — Ocean Surface Current Analyses Real-time |
| **Provider** | NASA Earthdata; originally developed with NASA-supported processing and satellite altimeter/scatterometer inputs |
| **Status** | **NEAR-REAL-TIME** and **HISTORICAL**, subject to product stream availability |
| **Official URL** | https://www.earthdata.nasa.gov/data/projects/oscar |
| **Download/API** | NASA Earthdata access; confirm current download endpoints and authentication requirements |
| **Format** | Commonly NetCDF and gridded scientific data products |
| **Spatial resolution** | Product/version dependent; verify metadata |
| **Temporal resolution** | Product/version dependent |
| **Coverage** | Global or broad ocean regions; original emphasis included tropical Pacific applications |
| **Update frequency** | Operational product dependent |
| **Variables** | Surface current velocity and direction or zonal/meridional components |
| **Units** | Commonly m/s |
| **License** | NASA data-access terms and attribution requirements |
| **Quality flags** | Consult dataset metadata and product documentation |
| **Historical availability** | Yes |
| **Real-time availability** | Operational/near-real-time according to active product availability |
| **Prototype suitability** | **Moderate.** Useful as a complementary surface-current source; Copernicus is generally more suitable for integrated Indian Ocean physics fields |
| **Agent using it** | Ocean Agent, Verification Agent |
| **Implementation note** | Compare OSCAR current direction/magnitude with Copernicus model current fields only after aligning time, depth, spatial grid, and datum assumptions |

OSCAR provides ocean surface velocity fields derived from satellite altimeter and vector-wind information. [86]

---

# 4. Wave Height and Marine Safety

## 4.1 Open-Meteo Marine Weather API

| Field | Details |
|---|---|
| **Dataset name** | Open-Meteo Marine Weather API |
| **Provider** | Open-Meteo, aggregating global marine model outputs including MeteoFrance, ECMWF, NCEP GFS, and DWD model sources |
| **Status** | **FORECAST**, **NEAR-REAL-TIME**, and limited **HISTORICAL** availability depending on underlying model |
| **Official URL** | https://open-meteo.com/en/docs/marine-weather-api |
| **Download/API** | Public HTTPS API endpoint documented as `/v1/marine`; no API key is required for standard non-commercial use according to the provider documentation |
| **Format** | JSON; CSV and XLSX are supported for selected response workflows |
| **Spatial resolution** | Source-model dependent: documented ranges include about 0.05 degree to 0.25 degree, approximately 5 km to 25 km, for different models |
| **Temporal resolution** | Hourly marine conditions and forecasts |
| **Coverage** | Global ocean |
| **Update frequency** | Source-model dependent; documented updates range from every 6 to 24 hours |
| **Variables** | Wave height, wave direction, wave period, wind-wave height/direction/period, swell height/direction/period, ocean-current velocity/direction, sea-surface temperature, sea-level height |
| **Units** | Wave height metres; period seconds; directions degrees; current velocity configurable; SST degrees Celsius; sea-level height metres |
| **License** | Check Open-Meteo terms, source attribution requirements, and commercial usage provisions |
| **Quality flags** | Does not replace native model quality-control documentation; identify underlying selected model and communicate model uncertainty |
| **Historical availability** | ERA5-Ocean is documented as available from 1940 to present with a delay; individual forecast models have shorter history |
| **Real-time availability** | Forecast-based output; not direct real-time buoy observation |
| **Prototype suitability** | **High for rapid prototype integration.** Provides simple coordinate-based JSON responses for wave and basic ocean safety signals |
| **Agent using it** | Safety Agent, Ocean Agent, Geospatial Agent |
| **Implementation note** | For safety decisions, combine wave height with wind, weather warnings, route distance, vessel assumptions, and authoritative local advisories. Never call it a navigational safety guarantee |

The Open-Meteo Marine API documents hourly global wave forecasts, source-model resolution, update schedules, ocean-current variables, SST, and sea-level-height fields. [122]

---

## 4.2 INCOIS Operational Ocean Forecast Products

| Field | Details |
|---|---|
| **Dataset name** | INCOIS operational ocean forecast products |
| **Provider** | Indian National Centre for Ocean Information Services |
| **Status** | Expected **FORECAST** and **NEAR-REAL-TIME**; exact publicly accessible service status requires validation |
| **Official URL** | https://www.incois.gov.in/ |
| **Download/API** | Public portal/API availability, authentication, permitted usage, and endpoint documentation must be verified directly with INCOIS before implementation |
| **Format** | Not confirmed in this catalog; potentially map services, files, dashboards, or authenticated APIs depending on product |
| **Spatial resolution** | Product-dependent; third-party reporting mentions SST around 0.05 degree and waves around 0.5 degree, but ORCA must verify official documentation before using these figures |
| **Temporal resolution** | Product-dependent |
| **Coverage** | Indian EEZ and surrounding waters, depending on selected forecast product |
| **Update frequency** | Product-dependent |
| **Variables** | Potentially wave height, tides, SST, salinity, currents, and operational marine forecast parameters |
| **Units** | Product-dependent |
| **License** | INCOIS terms and authorization requirements apply |
| **Quality flags** | Verify product-specific flags and uncertainty information |
| **Historical availability** | May exist for selected model/archive products; requires validation |
| **Real-time availability** | Operational but must be validated per service |
| **Prototype suitability** | **High after official access validation.** Strong local relevance for Indian waters |
| **Agent using it** | Ocean Agent, Safety Agent, Fisheries Agent, Verification Agent |
| **Implementation note** | Do not hard-code a presumed INCOIS API. Use a documented endpoint only after obtaining official access or written confirmation |

Public descriptions indicate that INCOIS produces operational outputs including temperature, salinity, currents, chlorophyll, wave, and tidal information, but implementation must verify official access details. [82][115]

---

# 5. Wind

## 5.1 ISRO EOS-06 Scatterometer Wind Products

| Field | Details |
|---|---|
| **Dataset name** | EOS-06/Oceansat-3 Ku-band scatterometer wind-vector products |
| **Provider** | ISRO; distribution expected through official ISRO/MOSDAC/NRSC services |
| **Status** | **NEAR-REAL-TIME** and **HISTORICAL**, subject to access validation |
| **Official URL** | https://www.isro.gov.in/ |
| **Download/API** | Verify official portal product access, registration, terms, and formats before implementation |
| **Format** | Product-dependent scientific geospatial formats |
| **Spatial resolution** | Instrument and processing-level dependent; verify product metadata |
| **Temporal resolution** | Oceansat-3 documentation indicates approximately 12-hour repeat capability for wind observations; actual product latency must be validated |
| **Coverage** | Broad ocean coverage including Indian Ocean |
| **Update frequency** | Operational processing dependent |
| **Variables** | Surface wind vector, wind speed, wind direction, quality information |
| **Units** | Commonly m/s and degrees; verify product metadata |
| **License** | ISRO/MOSDAC terms apply |
| **Quality flags** | Scatterometer wind products generally require ambiguity removal and quality-control flags; use official quality layers |
| **Historical availability** | Available from EOS-06 mission period onward; continuity may exist from earlier missions |
| **Real-time availability** | Near-real-time only after dissemination; not instantaneous |
| **Prototype suitability** | **Moderate to high after access validation.** Strong Indian Ocean relevance |
| **Agent using it** | Safety Agent, Ocean Agent, Verification Agent |
| **Implementation note** | Use weather-model wind as a fallback for live demonstrations if ISRO product access is unavailable |

EOS-06 carries a Ku-band scatterometer intended to provide ocean-surface wind-vector data. [43]

---

## 5.2 Open-Meteo Weather Forecast API

| Field | Details |
|---|---|
| **Dataset name** | Open-Meteo Weather Forecast API |
| **Provider** | Open-Meteo, using meteorological forecast model providers |
| **Status** | **FORECAST** and limited **HISTORICAL** access through related archive services |
| **Official URL** | https://open-meteo.com/ |
| **Download/API** | Official API documentation available from Open-Meteo; request coordinates and weather variables |
| **Format** | JSON, with selected CSV/XLSX support |
| **Spatial resolution** | Model dependent |
| **Temporal resolution** | Hourly and daily |
| **Coverage** | Global |
| **Update frequency** | Model dependent |
| **Variables** | Wind speed, wind direction, gusts, precipitation, pressure, temperature, cloud cover, weather code, visibility, and other weather variables depending on endpoint |
| **Units** | Metric units configurable; wind commonly km/h, m/s, knots, or mph depending on request |
| **License** | Check Open-Meteo terms and upstream source attribution requirements |
| **Quality flags** | Forecast-model metadata rather than observation quality flags |
| **Historical availability** | Related historical API supports archive data; validate exact variables and model coverage |
| **Real-time availability** | Forecast output, not direct real-time observation |
| **Prototype suitability** | **High** as a development-friendly supplementary weather source |
| **Agent using it** | Safety Agent |
| **Implementation note** | Local Indian Marine Department or INCOIS warnings should override generic model interpretation where officially available |

---

# 6. Tides and Sea Level

## 6.1 Open-Meteo Marine Tide and Sea-Level Fields

| Field | Details |
|---|---|
| **Dataset name** | Open-Meteo Marine API sea-level-height and tide-influenced current fields |
| **Provider** | Open-Meteo using global marine models |
| **Status** | **FORECAST** and limited **HISTORICAL** depending on source model |
| **Official URL** | https://open-meteo.com/en/docs/marine-weather-api |
| **Download/API** | Coordinate-based HTTPS JSON API |
| **Format** | JSON; selected CSV/XLSX output options |
| **Spatial resolution** | Documented source models include approximately 0.08 degree global current/tide fields; verify selected source model |
| **Temporal resolution** | Hourly |
| **Coverage** | Global |
| **Update frequency** | Source model dependent; documentation lists daily update for MeteoFrance SMOC currents/tides |
| **Variables** | Sea-level height relative to global mean sea level, ocean current velocity, ocean-current direction |
| **Units** | Sea-level height metres; current velocity configurable; direction degrees |
| **License** | Open-Meteo terms and attribution requirements |
| **Quality flags** | No local tide-station quality flag substitute; treat as model output |
| **Historical availability** | Underlying sources vary; ERA5-Ocean archive is documented from 1940 to present with latency |
| **Real-time availability** | Forecast/model estimate; not a local verified tide-table substitute |
| **Prototype suitability** | **Moderate.** Useful for indicative sea-level context and demonstrations, not for coastal navigation decisions |
| **Agent using it** | Safety Agent, Geospatial Agent |
| **Implementation note** | The provider explicitly notes coastal accuracy limitations and says the sea-level field is not suitable for coastal navigation |

Open-Meteo documents sea-level height as a global-mean-sea-level-referenced model field and warns that it is not suitable for coastal navigation. [122]

---

## 6.2 NOAA Tides and Currents

| Field | Details |
|---|---|
| **Dataset name** | NOAA Tides and Currents predictions and water-level observations |
| **Provider** | NOAA National Ocean Service |
| **Status** | **REAL-TIME**, **FORECAST**, and **HISTORICAL** for U.S. stations |
| **Official URL** | https://tidesandcurrents.noaa.gov/ |
| **Download/API** | NOAA provides web services and station-based prediction/observation downloads |
| **Format** | JSON/XML/text and web-service responses depending on endpoint |
| **Spatial resolution** | Station-point observations and station-based predictions |
| **Temporal resolution** | Station and product dependent; predictions can be retrieved over limited time ranges |
| **Coverage** | Primarily U.S. coasts, territories, and associated waters |
| **Update frequency** | Real-time station observations and regularly updated prediction services |
| **Variables** | Tide predictions, water level, currents at supported stations, meteorological observations at some stations |
| **Units** | Metres, feet, knots, and station/product-specific units |
| **License** | NOAA open-data policies; cite source and station metadata |
| **Quality flags** | Station/product quality-control information and datum references are critical |
| **Historical availability** | Yes |
| **Real-time availability** | Yes, for supported NOAA stations |
| **Prototype suitability** | **Low for Indian coastal tide operations** because the network is U.S.-focused; useful only for software/API development examples |
| **Agent using it** | Safety Agent, Data Integration Test Suite |
| **Implementation note** | Do not use NOAA tide predictions as a source for Chennai, Tamil Nadu, or other Indian coast locations |

NOAA’s tide-prediction service provides measured and predicted tide information and exposes download and web-service options for supported stations. [87]

---

# 7. Bathymetry

## 7.1 GEBCO 2026 Grid

| Field | Details |
|---|---|
| **Dataset name** | GEBCO_2026 Grid |
| **Provider** | General Bathymetric Chart of the Oceans Bathymetric Compilation Group |
| **Status** | **STATIC**, updated annually |
| **Official URL** | https://www.gebco.net/data_and_products/gridded_bathymetry_data/ |
| **Download/API** | Global download, tiled download, user-defined geographic-area download, and OPeNDAP access |
| **Format** | NetCDF, GeoTIFF, Esri ASCII raster |
| **Spatial resolution** | 15 arc-seconds |
| **Temporal resolution** | Not applicable; annual versioned release |
| **Coverage** | Global ocean and land terrain, including Indian Ocean and Indian coastal waters |
| **Update frequency** | Generally annual releases |
| **Variables** | Elevation/bathymetry in metres; Type Identifier Grid indicating source-data type |
| **Units** | Metres |
| **License** | Public domain; use is free of charge subject to terms of use and attribution |
| **Quality flags** | Type Identifier Grid provides source-type information. Users must understand that the grid includes heterogeneous underlying data quality and may include interpolation/modelled areas |
| **Historical availability** | Versioned annual grids are available |
| **Real-time availability** | Not applicable |
| **Prototype suitability** | **High.** Strong authoritative base layer for distance, depth context, shallow-water warnings, and map visualization |
| **Agent using it** | Geospatial Agent, Safety Agent, Ocean Agent |
| **Implementation note** | Use bathymetry for broad spatial context; do not use GEBCO as an official navigational chart or for vessel route clearance decisions |

GEBCO_2026 provides global terrain elevation/bathymetry at 15 arc-second intervals, offers NetCDF/GeoTIFF/ASCII downloads and OPeNDAP access, and is placed in the public domain. [108]

---

# 8. Potential Fishing Zones and Fisheries

## 8.1 INCOIS Potential Fishing Zone Advisories

| Field | Details |
|---|---|
| **Dataset name** | Potential Fishing Zone Advisory |
| **Provider** | Indian National Centre for Ocean Information Services |
| **Status** | **NEAR-REAL-TIME** operational advisory and short-range outlook |
| **Official URL** | https://www.incois.gov.in/ |
| **Download/API** | Verify official PFZ portal, permitted dissemination channels, data format, and API access directly with INCOIS before implementation |
| **Format** | Advisory products may include maps, textual coordinates, mobile-app dissemination, and other official formats; exact machine-readable access requires validation |
| **Spatial resolution** | Advisory/product dependent |
| **Temporal resolution** | Operational daily advisory and short-range advisory outlook; verify specific coastal product schedule |
| **Coverage** | Indian EEZ and selected coastal regions, subject to advisory service coverage |
| **Update frequency** | Operational advisory schedule; verify current official timetable |
| **Variables** | PFZ location/coordinates, fishing-prospect category, SST/chlorophyll-based indicators, direction/distance information and advisory metadata depending on product |
| **Units** | Coordinates in latitude/longitude; distance and depth units may vary by advisory |
| **License** | INCOIS terms, attribution, and dissemination restrictions apply |
| **Quality flags** | Advisory validity period, issue time, product version, cloud/data availability, and source metadata should be retained |
| **Historical availability** | Historical advisory archives may exist but availability must be confirmed |
| **Real-time availability** | Operational advisory; treat as near-real-time due to generation and dissemination latency |
| **Prototype suitability** | **High after formal access validation.** It is ORCA’s most relevant fisheries evidence layer |
| **Agent using it** | Fisheries Agent, Geospatial Agent, Verification Agent |
| **Implementation note** | PFZ is an advisory indicator, not a guarantee of catch. ORCA must not convert PFZ into a guaranteed fishing recommendation and must allow safety conditions to override fishing potential |

INCOIS PFZ advisories use satellite-derived ocean information to support fisheries guidance and are disseminated to fishing communities through operational channels. [2][3][8]

---

## 8.2 FAO FishStatJ and Global Fisheries Statistics

| Field | Details |
|---|---|
| **Dataset name** | FAO FishStatJ global fisheries and aquaculture statistics |
| **Provider** | Food and Agriculture Organization of the United Nations |
| **Status** | **HISTORICAL** |
| **Official URL** | https://www.fao.org/fishery/en/statistics/software/fishstatj |
| **Download/API** | Official FishStatJ software and downloadable statistical tables; verify current datasets and access terms |
| **Format** | Statistical tables, CSV-compatible exports, database/software distribution formats |
| **Spatial resolution** | Country, FAO fishing area, species, fleet, commodity, and reporting-unit dependent; not fine-scale fishing-zone data |
| **Temporal resolution** | Usually annual |
| **Coverage** | Global |
| **Update frequency** | Statistical release cycle, typically annual or periodic |
| **Variables** | Capture production, aquaculture production, fleet indicators, commodities, species/group statistics, trade and related fisheries statistics |
| **Units** | Tonnes, values, counts, and other statistical units depending on table |
| **License** | FAO data policy and attribution requirements apply |
| **Quality flags** | Use metadata on reporting status, estimated values, species aggregation, and country reporting limitations |
| **Historical availability** | Yes; multi-year historical records |
| **Real-time availability** | No |
| **Prototype suitability** | **Moderate.** Useful for scientist/government context and historical fisheries analytics, not daily fishing-route recommendations |
| **Agent using it** | Fisheries Agent, Knowledge/RAG Agent, Government Mode Analytics |
| **Implementation note** | Do not combine annual FAO landing totals with daily PFZ predictions without clearly distinguishing their scale and purpose |

---

## 8.3 Kaggle Datasets

| Field | Details |
|---|---|
| **Dataset name** | Kaggle-hosted marine, fisheries, satellite, or oceanographic datasets |
| **Provider** | Individual dataset publishers through Kaggle |
| **Status** | Varies; often **HISTORICAL** |
| **Official URL** | https://www.kaggle.com/datasets |
| **Download/API** | Kaggle API and website download, subject to dataset-specific licence and Kaggle terms |
| **Format** | CSV, Parquet, images, GeoTIFF, NetCDF, notebooks, and other community-provided formats |
| **Spatial resolution** | Dataset dependent |
| **Temporal resolution** | Dataset dependent |
| **Coverage** | Dataset dependent |
| **Update frequency** | Dataset dependent; often irregular |
| **Variables** | Dataset dependent |
| **Units** | Dataset dependent |
| **License** | Must be checked dataset by dataset |
| **Quality flags** | Often absent or inconsistently documented |
| **Historical availability** | Often yes |
| **Real-time availability** | Usually no |
| **Prototype suitability** | **Low to moderate.** Appropriate only for exploratory ML experiments, UI mock data, or reproducible academic baselines after provenance review |
| **Agent using it** | Offline ML Experiment Pipeline only |
| **Implementation note** | Kaggle must not be the primary source for operational safety, PFZ, SST, chlorophyll, or government-facing marine decisions. Prefer the original authoritative producer whenever possible |

---

# 9. Marine Heat Waves

## 9.1 Derived Marine Heat-Wave Detection from SST

| Field | Details |
|---|---|
| **Dataset name** | ORCA-derived marine heat-wave indicator generated from authoritative SST time series |
| **Provider** | ORCA derived product; source SST should come from NOAA, Copernicus Marine, NASA, or validated ISRO products |
| **Status** | **HISTORICAL**, **NEAR-REAL-TIME**, and **FORECAST** depending on input SST data |
| **Official URL** | Not applicable; ORCA derived analysis |
| **Download/API** | Derived internally from selected source datasets |
| **Format** | NetCDF/GeoTIFF/Parquet for raster/time-series processing; GeoJSON for map polygons; JSON for API response |
| **Spatial resolution** | Inherits selected SST source resolution |
| **Temporal resolution** | Inherits selected SST source cadence, commonly daily |
| **Coverage** | Defined by selected SST source; global or Indian Ocean focus |
| **Update frequency** | Recomputed when source SST updates |
| **Variables** | SST anomaly, climatological percentile threshold, event duration, intensity, category, data completeness, confidence |
| **Units** | SST anomaly in degrees Celsius; duration in days; intensity in degrees Celsius above threshold |
| **License** | Inherits obligations of source SST data; ORCA must cite upstream provider |
| **Quality flags** | Source SST quality flags plus ORCA flags for missing data, cloud-related gaps, interpolation, baseline coverage, and forecast status |
| **Historical availability** | Yes, if SST baseline period is available |
| **Real-time availability** | Near-real-time only when source SST supports it |
| **Prototype suitability** | **High.** More feasible than searching for a separate universal MHW raster feed; transparent derivation is scientifically clearer |
| **Agent using it** | Ecosystem Agent, Verification Agent |
| **Implementation note** | Adopt a published marine heat-wave methodology and clearly label outputs as derived indicators. Do not describe a model forecast as an observed event |

Copernicus Marine publishes marine heat-wave monitoring and ten-day forecast bulletins using global ocean analysis/forecast and observation-based SST products. [102][104]

---

## 9.2 Copernicus Marine Heat-Wave Bulletin

| Field | Details |
|---|---|
| **Dataset name** | Copernicus Marine heat-wave bulletin and associated SST/forecast context |
| **Provider** | Mercator Ocean International / Copernicus Marine Service |
| **Status** | **NEAR-REAL-TIME** and **FORECAST** |
| **Official URL** | https://www.mercator-ocean.eu/ |
| **Download/API** | Bulletin content is web-accessible; underlying global physics/SST products are available through Copernicus Marine Data Store subject to access requirements |
| **Format** | Bulletin pages/reports plus underlying NetCDF marine products |
| **Spatial resolution** | Underlying product dependent |
| **Temporal resolution** | Weekly bulletin and ten-day forecast context |
| **Coverage** | Global; some graphics and categories may emphasize European waters |
| **Update frequency** | Weekly bulletin cycle |
| **Variables** | Marine heat-wave presence, extent, intensity category, duration context, SST forecast/analysis |
| **Units** | Temperature anomaly/intensity context; verify source product metadata |
| **License** | Copernicus/Mercator Ocean terms and attribution requirements |
| **Quality flags** | Underlying product quality and model uncertainty apply |
| **Historical availability** | Bulletin archive availability must be checked |
| **Real-time availability** | Near-real-time monitoring and forecast product |
| **Prototype suitability** | **Moderate.** Useful for validation, dashboard context, and reference; derive local MHW indicators directly from SST for a focused Indian prototype |
| **Agent using it** | Ecosystem Agent, Knowledge/RAG Agent |
| **Implementation note** | Do not assume the bulletin provides an API-ready Indian coastal MHW layer |

Copernicus Marine states that its marine heat-wave bulletins use observation-based SST maps and global model analyses/forecasts to produce ten-day heat-wave forecasts. [104]

---

# 10. Weather and Marine Warnings

## 10.1 Open-Meteo Weather Forecast and Historical APIs

| Field | Details |
|---|---|
| **Dataset name** | Open-Meteo Weather Forecast API and Historical Weather API |
| **Provider** | Open-Meteo, using meteorological forecast and reanalysis sources |
| **Status** | **FORECAST** and **HISTORICAL** |
| **Official URL** | https://open-meteo.com/ |
| **Download/API** | HTTPS APIs with coordinate/time/variable parameters |
| **Format** | JSON; selected CSV/XLSX support |
| **Spatial resolution** | Model dependent; historical documentation indicates 0.1 or 0.25 degree data, with newer post-2017 weather models at approximately 9 km for selected variables |
| **Temporal resolution** | Hourly and daily |
| **Coverage** | Global |
| **Update frequency** | Forecast model and archive source dependent |
| **Variables** | Wind speed, wind direction, gusts, precipitation, temperature, cloud cover, pressure, humidity, weather code, visibility, and other available atmospheric variables |
| **Units** | Variable dependent; API supports unit configuration |
| **License** | Verify Open-Meteo terms and upstream attribution obligations |
| **Quality flags** | Model/reanalysis metadata, not direct sensor observation quality flags |
| **Historical availability** | Historical API documentation indicates coverage dating to 1940 for some data streams |
| **Real-time availability** | Forecast data reflect model runs; do not present as direct observation |
| **Prototype suitability** | **High for prototype safety context.** Use as a supplementary source, not as an authoritative official warning service |
| **Agent using it** | Safety Agent, Verification Agent |
| **Implementation note** | For a production system, integrate official Indian meteorological and ocean warning sources after formal validation |

Open-Meteo documents historical weather coverage extending to 1940 for selected products and provides model-driven coordinate-based weather data. [93]

---

## 10.2 IMD and INCOIS Marine Warnings

| Field | Details |
|---|---|
| **Dataset name** | Indian Meteorological Department and INCOIS marine weather/cyclone/warning products |
| **Provider** | IMD and INCOIS |
| **Status** | Potentially **REAL-TIME**, **NEAR-REAL-TIME**, and **FORECAST**, depending on alert service |
| **Official URL** | https://mausam.imd.gov.in/ and https://www.incois.gov.in/ |
| **Download/API** | Official access mechanism must be verified before integration; may involve portals, bulletins, CAP feeds, maps, or restricted services |
| **Format** | Product dependent |
| **Spatial resolution** | Product dependent |
| **Temporal resolution** | Product dependent |
| **Coverage** | India, Bay of Bengal, Arabian Sea, and adjacent operational warning regions |
| **Update frequency** | Event and forecast dependent |
| **Variables** | Cyclone alerts, marine weather warnings, wind, rainfall, sea state, wave, and other hazard information depending on product |
| **Units** | Product dependent |
| **License** | Government service terms and attribution requirements apply |
| **Quality flags** | Validity period, warning category, issue time, revision number, source agency |
| **Historical availability** | Bulletin archives may exist; validate access |
| **Real-time availability** | Potentially yes for warnings; verify official product status |
| **Prototype suitability** | **High after validation.** Official warnings should have override priority in ORCA’s safety rules |
| **Agent using it** | Safety Agent, Verification Agent, ORCA Coordinator |
| **Implementation note** | Safety policy should state: official cyclone, storm, or marine-danger warnings override favorable PFZ or ecosystem signals |

---

# 11. Satellite Imagery

## 11.1 NASA Worldview and Earthdata Browse Products

| Field | Details |
|---|---|
| **Dataset name** | NASA Worldview imagery and Earthdata browse products |
| **Provider** | NASA Earthdata |
| **Status** | **NEAR-REAL-TIME** and **HISTORICAL** |
| **Official URL** | https://worldview.earthdata.nasa.gov/ |
| **Download/API** | Web visualization and mission/product-specific Earthdata download services; verify tile/API access terms for implementation |
| **Format** | Web imagery tiles, rendered image products, and source scientific data files depending on mission |
| **Spatial resolution** | Sensor-dependent |
| **Temporal resolution** | Mission dependent; many imagery layers update daily |
| **Coverage** | Global |
| **Update frequency** | Mission and layer dependent |
| **Variables** | True colour, false colour, ocean colour, clouds, SST and other satellite-derived visual layers depending on selected product |
| **Units** | Imagery values/product-dependent |
| **License** | NASA Earthdata terms and attribution requirements |
| **Quality flags** | Scientific source products include flags; visual imagery alone should not be treated as analysis-grade data |
| **Historical availability** | Yes, depending on layer |
| **Real-time availability** | Near-real-time for eligible layers |
| **Prototype suitability** | **High for visualization; moderate for direct analysis.** Useful as map evidence and UI layer |
| **Agent using it** | Ecosystem Agent, Ocean Agent, Map UI |
| **Implementation note** | Do not infer quantitative chlorophyll/SST values from rendered PNG/JPEG imagery; use underlying scientific datasets for reasoning |

---

## 11.2 MOSDAC Browse and Satellite Products

| Field | Details |
|---|---|
| **Dataset name** | MOSDAC meteorological and oceanographic satellite browse/data products |
| **Provider** | ISRO MOSDAC |
| **Status** | **NEAR-REAL-TIME**, **HISTORICAL**, and service-dependent |
| **Official URL** | https://mosdac.gov.in/ |
| **Download/API** | MOSDAC advertises browse products, data products, and web services. Actual service health, access requirements, and endpoint availability must be tested |
| **Format** | Browse imagery such as JPG/GIF/PNG; scientific products and web services may include HDF, NetCDF, GeoTIFF, and OGC-compatible services |
| **Spatial resolution** | Mission/product dependent |
| **Temporal resolution** | Mission/product dependent |
| **Coverage** | ISRO satellite coverage and associated meteorological/oceanographic products |
| **Update frequency** | Product and service dependent |
| **Variables** | Ocean colour, SST, wind, meteorological fields, and other ISRO satellite products depending on selected mission/product |
| **Units** | Product dependent |
| **License** | ISRO/MOSDAC terms and access rules apply |
| **Quality flags** | Product dependent; inspect associated metadata |
| **Historical availability** | Yes for archived products where provided |
| **Real-time availability** | Some services may be near-real-time, but current availability must be checked |
| **Prototype suitability** | **High after service validation.** Valuable for Indian-source imagery and data, but ORCA needs fallback sources because MOSDAC has displayed notices that some services are not currently updating |
| **Agent using it** | Ocean Agent, Ecosystem Agent, Map UI, Verification Agent |
| **Implementation note** | Implement health checks and a source-status badge. If MOSDAC is stale/unavailable, ORCA should identify it rather than silently showing old data |

MOSDAC officially describes meteorological and oceanographic data services and has displayed a notice that some information services are not currently updating. [31][45]

---

# 12. Data Quality and Verification Policy

Every ORCA ingestion record should include the following metadata:

```json
{
  "source_provider": "Copernicus Marine",
  "dataset_id": "exact-selected-product-id",
  "retrieved_at": "ISO-8601 timestamp",
  "valid_time_start": "ISO-8601 timestamp",
  "valid_time_end": "ISO-8601 timestamp",
  "data_class": "observation | analysis | forecast | reanalysis | derived",
  "spatial_resolution": "source-reported resolution",
  "units": "source-reported unit",
  "quality_flag": "source-reported value or null",
  "uncertainty": "source-reported uncertainty or null",
  "license_reference": "official terms URL",
  "processing_steps": ["subset", "reproject", "unit-normalization"],
  "staleness_status": "fresh | delayed | stale | unavailable"
}
```

## Mandatory verification rules

- Never mix observation, analysis, forecast, and reanalysis values without displaying their data class.
- Never show a forecast timestamp as though it were an observed measurement.
- Never derive a confidence percentage solely from an LLM response.
- Treat missing quality flags as an uncertainty signal, not as proof that data is valid.
- Reject or clearly flag data outside its validity window.
- Use source-specific units internally, then normalize only with logged conversion.
- Preserve original source timestamps and selected product identifiers.
- If two sources disagree materially, trigger the Verification Agent and show the conflict to the user.
- Official safety warnings must override a favorable fishing-potential result.
- Do not use bathymetry, tide models, or wave forecasts as navigational clearance or legal safety advice.

---

# 13. Prototype Priority Tiers

## Tier 1: Build first

- Copernicus Marine SST and global physics products
- NASA OB.DAAC chlorophyll-a and SST products
- Open-Meteo Marine API for wave, swell, basic currents, and SST point forecasts
- Open-Meteo Weather API for wind and precipitation
- GEBCO 2026 bathymetry
- A manually curated or officially authorized INCOIS PFZ evidence layer

## Tier 2: Integrate after access validation

- MOSDAC EOS-06/Oceansat-3 OCM-3 products
- INCOIS operational ocean forecast products
- INCOIS PFZ machine-readable services or advisory archive
- IMD/INCOIS official warning feeds
- Indian fisheries landing/catch datasets from authorized institutions

## Tier 3: Research and model development

- NOAA OISST historical anomaly baseline
- FAO FishStatJ historical fisheries context
- OceanDepths AI-ready global benchmark dataset
- Kaggle datasets only for non-operational experimentation after provenance review

---

# 14. Research Dataset: OceanDepths

| Field | Details |
|---|---|
| **Dataset name** | OceanDepths: A Global Dataset of Paired Subsurface and Surface Ocean Observations |
| **Provider** | ESA Phi-Lab research dataset |
| **Status** | **HISTORICAL** |
| **Official URL** | https://huggingface.co/datasets/ESA-philab/OceanDepths |
| **Download/API** | Hugging Face dataset access; confirm dataset licence and repository availability before use |
| **Format** | AI-ready gridded dataset; exact file structure should be verified from repository documentation |
| **Spatial resolution** | 0.1 degree by 0.1 degree |
| **Temporal resolution** | Weekly |
| **Coverage** | Global ocean |
| **Update frequency** | Research dataset release; not operationally updated |
| **Variables** | Satellite SST, sea-surface salinity, sea-surface height; EN4 subsurface temperature/salinity profiles; matched GLORYS12 reanalysis |
| **Units** | Variable dependent; verify repository metadata |
| **License** | Must be verified from official dataset repository |
| **Quality flags** | Source/product dependent; research dataset documentation must be reviewed |
| **Historical availability** | 2000–2024 |
| **Real-time availability** | No |
| **Prototype suitability** | **Moderate for offline ML experiments; low for live decision support** |
| **Agent using it** | Offline Model Training, Evaluation Pipeline |
| **Implementation note** | Useful for testing multivariate reconstruction or anomaly models, but not appropriate as the primary live ORCA data feed |

OceanDepths pairs satellite SST, SSS, and SSH products with subsurface observations and GLORYS12 context at 0.1 degree weekly resolution for 2000–2024. [103][111]

---

# 15. Source Selection Decision

For the SIH demonstration, ORCA should present a focused, scientifically defensible workflow:

```text
User location + requested time
        ↓
Geospatial Agent:
GEBCO depth context + distance calculation
        ↓
Ocean Agent:
Copernicus SST/current fields + forecast labels
        ↓
Ecosystem Agent:
NASA chlorophyll-a + SST anomaly / marine heat-wave indicator
        ↓
Fisheries Agent:
INCOIS PFZ advisory evidence when authorized
        ↓
Safety Agent:
Open-Meteo wave + wind forecast
+ official warning feed when available
        ↓
Verification Agent:
Timestamp, quality flag, spatial overlap,
forecast-vs-observation, source conflict checks
        ↓
ORCA Coordinator:
Evidence-grounded recommendation with uncertainty
```

The strongest prototype is not the one with the most datasets. It is the one that clearly demonstrates source attribution, validity-time checks, safe conflict handling, and explainable cross-domain reasoning.

---