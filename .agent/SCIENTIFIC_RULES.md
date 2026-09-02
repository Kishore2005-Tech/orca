# SCIENTIFIC_RULES.md

## ORCA Marine Ecosystems Reasoning with Collaborative Agents  
**Scientific Validation and Inference Governance Document**

***

## 1. Scientific Principles

### 1.1 Foundational Marine Science Framework

ORCA operates within established marine science principles derived from physical oceanography, biological oceanography, and fisheries science. All AI-generated inferences must align with peer-reviewed scientific understanding and authoritative government/intergovernmental data sources.

**Core Principles:**

- **Observational Hierarchy**: Satellite observations → Derived indicators → Scientific interpretation → AI inference → User recommendation [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Multi-Parameter Integration**: No single ocean parameter deterministically predicts ecosystem state or fish abundance [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Temporal Dynamics**: Ocean features are dynamic; spatial locations shift with wind, currents, and temporal evolution [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Uncertainty Propagation**: All derived products carry measurement uncertainty, algorithmic uncertainty, and interpretive uncertainty [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)

### 1.2 Authoritative Source Hierarchy

ORCA must prioritize evidence from (in order):

1. **ISRO** (Indian Space Research Organisation) – Indian satellite data, Oceansat series [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **MOSDAC** (Meteorological & Oceanographic Satellite Data Archival Centre) – Indian ocean color and SST products [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
3. **INCOIS** (Indian National Centre for Ocean Information Services) – PFZ advisories, Ocean State Forecasts, marine hazard warnings [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
4. **Government of India Scientific Organizations** – MoES, NIO, CMFRI, NIOT
5. **NASA** – MODIS, VIIRS, JPL physical oceanography products [earthdata.nasa](https://www.earthdata.nasa.gov/s3fs-public/2025-12/uqtalk_franz.pdf)
6. **NOAA** – AVHRR, marine heatwave definitions, ocean monitoring [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
7. **Copernicus Marine Service** – Global ocean reanalysis, SST, chlorophyll, SSH products [marine.copernicus](https://marine.copernicus.eu/sites/default/files/media/pdf/2024-05/cmems-service-catalogue-2024-04.pdf)
8. **Peer-Reviewed Scientific Literature** – Hobday et al. 2016 (marine heatwaves), oceanography journals [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

**Prohibited Sources**: Random blogs, unverified social media, non-peer-reviewed opinion pieces, commercial fishing forums without scientific backing.

***

## 2. Marine Data Classification

### 2.1 Data Type Categories

| Data Type | Definition | ORCA Handling |
|-----------|------------|---------------|
| **Observation** | Direct satellite or in-situ measurement (e.g., SST from AVHRR, chlorophyll from OCM) | Use only with quality flags, timestamp, spatial resolution metadata  [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf) |
| **Derived Indicator** | Algorithmically processed product (e.g., PFZ from SST+chlorophyll, MHW from SST anomaly) | Must cite algorithm source, validity domain, uncertainty  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Forecast** | Model-predicted future state (e.g., INCOIS Ocean State Forecast, wave height 5-day forecast) | Must label as forecast, include valid period, model source, skill metrics if available  [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp) |
| **Interpretation** | Scientific inference from data (e.g., "upwelling zone", "ocean front") | Must distinguish from observation, cite scientific basis, include confidence level  [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf) |
| **Recommendation** | Actionable guidance to user (e.g., "PFZ location", "high wave alert") | Must be traceable to observation→indicator→interpretation chain, include safety caveats  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |

### 2.2 Data Provenance Requirements

Every data point used by ORCA must include:

- **Source**: Which agency/satellite/product (e.g., "INCOIS PFZ from Oceansat-2 OCM + NOAA AVHRR") [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Timestamp**: Acquisition time and validity period [incois.gov](https://incois.gov.in/MarineFisheries/TextDataHome?mfid=1&request_locale=en)
- **Spatial Resolution**: Grid size or footprint (e.g., 1 km chlorophyll, 4 km SST) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
- **Quality Flags**: Data quality indicators (e.g., sun glint, cloud contamination, algorithm failure) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- **Processing Level**: L2 (swath), L3 (gridded), L4 (analyzed) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)

**Insufficient authoritative evidence – do not infer** if provenance metadata is missing.

***

## 3. Physical Oceanography Rules

### 3.1 Sea Surface Temperature (SST)

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Temperature of the ocean surface layer (skin temperature ~10 μm depth for infrared, bulk temperature ~1 m for microwave)  [earthdata.nasa](https://www.earthdata.nasa.gov/s3fs-public/2025-12/uqtalk_franz.pdf) |
| **Typical unit** | Degrees Celsius (°C)  [incois.gov](https://incois.gov.in/geoportal/MFASPFZ/index.html) |
| **What it can legitimately indicate** | Thermal structure, ocean fronts, upwelling zones, marine heatwave conditions, water mass boundaries  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **What it cannot prove** | Fish abundance, chlorophyll concentration, subsurface conditions, salinity, dissolved oxygen  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Spatial/temporal considerations** | Satellite SST: 1–4 km resolution, daily to weekly composites; diurnal warming affects daytime IR SST; cloud contamination gaps  [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf) |
| **How ORCA may use it** | Identify thermal fronts, detect marine heatwaves (SST > 90th percentile for ≥5 days)  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891), contribute to PFZ as one parameter  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory), never alone predict fish catch  [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf) |

**Scientific Constraint**: SST alone must NOT deterministically predict fish abundance or PFZ validity. PFZ requires SST + chlorophyll integration. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 3.2 Sea Surface Salinity (SSS)

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Salt concentration at ocean surface (practical salinity units)  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |
| **Typical unit** | PSU (Practical Salinity Units) or dimensionless  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |
| **What it can legitimately indicate** | Freshwater input (river discharge, rainfall), evaporation zones, water mass mixing, estuarine fronts  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |
| **What it cannot prove** | Biological productivity, fish distribution, subsurface salinity structure  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |
| **Spatial/temporal considerations** | Satellite SSS: ~50–100 km resolution, weekly composites; coastal contamination, rain interference  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |
| **How ORCA may use it** | Identify river plumes, estuarine fronts, water mass boundaries; contribute to ecosystem interpretation when combined with SST and chlorophyll  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |

**Insufficient authoritative evidence – do not infer** direct relationships between SSS and fish catch without peer-reviewed validation for specific species/region.

### 3.3 Sea Surface Height (SSH) / Altimetry

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Height of sea surface relative to reference ellipsoid/geoid; includes geostrophic currents, eddies, tides  [science](https://www.science.gov/topicpages/o/ocean+color+parameters) |
| **Typical unit** | Meters (m) or centimeters (cm) anomaly  [science](https://www.science.gov/topicpages/o/ocean+color+parameters) |
| **What it can legitimately indicate** | Ocean currents (geostrophic), mesoscale eddies, upwelling/downwelling signatures, large-scale circulation  [science](https://www.science.gov/topicpages/o/ocean+color+parameters) |
| **What it cannot prove** | Biological productivity, fish aggregation, wind-driven currents, coastal processes (altimetry degraded near coast)  [science](https://www.science.gov/topicpages/o/ocean+color+parameters) |
| **Spatial/temporal considerations** | Along-track altimetry: ~7 km resolution, repeat cycle 10–35 days; gridded products: 1/4° to 1/12°, daily to weekly  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |
| **How ORCA may use it** | Identify eddies, current boundaries, upwelling signatures; integrate with SST and chlorophyll for ecosystem interpretation  [science](https://www.science.gov/topicpages/o/ocean+color+parameters) |

**Scientific Constraint**: SSH anomalies alone cannot predict biological state; must be combined with ocean color and SST. [science](https://www.science.gov/topicpages/o/ocean+color+parameters)

### 3.4 Ocean Currents

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Water movement (velocity vector: speed + direction); surface currents from altimetry + wind, or model reanalysis  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |
| **Typical unit** | Meters per second (m/s) or centimeters per second (cm/s); direction in degrees from north  [journals.ametsoc](https://journals.ametsoc.org/view/journals/atot/32/11/jtech-d-15-0047_1.pdf) |
| **What it can legitimately indicate** | Transport pathways, larval dispersal, nutrient advection, frontogenesis, PFZ shift prediction  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **What it cannot prove** | Fish location at specific time, subsurface currents, coastal currents (model resolution limits)  [journals.ametsoc](https://journals.ametsoc.org/view/journals/atot/32/11/jtech-d-15-0047_1.pdf) |
| **Spatial/temporal considerations** | Model resolution: 1/12° to 1/4°; forecast horizon: 5–7 days with decreasing skill  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |
| **How ORCA may use it** | Predict PFZ drift using wind + current vectors  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory), identify transport pathways for ecosystem connectivity  [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf) |

### 3.5 Wind (Surface)

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Surface wind velocity (speed + direction) at 10 m above sea level  [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp) |
| **Typical unit** | Meters per second (m/s) or kilometers per hour (km/h); direction in degrees  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf) |
| **What it can legitimately indicate** | Wave generation, upwelling forcing (alongshore wind), PFZ shift prediction, storm conditions  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **What it cannot prove** | Subsurface conditions, fish behavior, wave height without wave model  [journals.ametsoc](https://journals.ametsoc.org/view/journals/atot/32/11/jtech-d-15-0047_1.pdf) |
| **Spatial/temporal considerations** | Forecast horizon: 5–7 days; resolution: 10–25 km for models; satellite wind: scatterometer, 25–50 km  [journals.ametsoc](https://journals.ametsoc.org/view/journals/atot/32/11/jtech-d-15-0047_1.pdf) |
| **How ORCA may use it** | Predict PFZ drift (INCOIS incorporates wind for feature shift guidance)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory), generate high wave alerts (INCOIS High Wave Alert: Hs > 2.5 m watch, > 3.0 m alert)  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf), identify upwelling-favorable wind conditions  [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf) |

### 3.6 Wave Height (Significant Wave Height, Hs)

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Average height of highest 1/3 of waves; statistical measure of sea state  [journals.ametsoc](https://journals.ametsoc.org/view/journals/atot/32/11/jtech-d-15-0047_1.pdf) |
| **Typical unit** | Meters (m)  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf) |
| **What it can legitimately indicate** | Sea state severity, navigation safety, fishing operational safety, swell propagation  [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp) |
| **What it cannot prove** | Individual wave height, breaking waves, coastal inundation without coastal model  [journals.ametsoc](https://journals.ametsoc.org/view/journals/atot/32/11/jtech-d-15-0047_1.pdf) |
| **Spatial/temporal considerations** | Forecast horizon: 5–7 days; resolution: 10–25 km; validated against buoys and altimeters  [journals.ametsoc](https://journals.ametsoc.org/view/journals/atot/32/11/jtech-d-15-0047_1.pdf) |
| **How ORCA may use it** | Generate safety alerts (INCOIS High Wave Alert thresholds)  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf), advise on fishing operational safety (never guarantee safety)  [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp) |

**Safety Constraint**: ORCA must NOT claim guaranteed fishing safety or navigation safety. Safety outputs must identify source, timestamp, forecast/observation status, and relevant uncertainty. [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

### 3.7 Mixed Layer Depth (MLD)

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Depth of surface ocean layer with nearly uniform temperature/salinity (actively mixed by wind and buoyancy fluxes)  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) |
| **Typical unit** | Meters (m)  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) |
| **What it can legitimately indicate** | Nutrient supply potential, upper ocean stratification, marine heatwave vertical structure, primary production capacity  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) |
| **What it cannot prove** | Exact nutrient concentration, chlorophyll profile, fish distribution  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) |
| **Spatial/temporal considerations** | Model-derived: 1/12° to 1/4° resolution; in-situ: sparse; seasonal to interannual variability  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) |
| **How ORCA may use it** | Contribute to ecosystem productivity interpretation (shallow MLD + high light = potential productivity); interpret marine heatwave vertical structure  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf) |

**Insufficient authoritative evidence – do not infer** direct MLD–fish catch relationships without peer-reviewed validation.

### 3.8 Bathymetry

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Ocean depth relative to sea level; seafloor topography  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Typical unit** | Meters (m)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzWebGis) |
| **What it can legitimately indicate** | Fishing ground depth, habitat type (continental shelf, slope, abyssal), upwelling potential (shelf breaks)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **What it cannot prove** | Fish presence, current patterns, biological productivity  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Spatial/temporal considerations** | Resolution varies: GEBCO 15 arc-sec (~450 m), regional surveys finer; static (no temporal change except sedimentation/erosion)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzWebGis) |
| **How ORCA may use it** | Filter PFZ by depth ranges relevant to target species  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory), identify shelf breaks and seamounts as potential fishing grounds  [incois.gov](https://incois.gov.in/MarineFisheries/PfzWebGis) |

***

## 4. Biological Oceanography Rules

### 4.1 Chlorophyll-a (Chl-a)

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Concentration of chlorophyll-a pigment in phytoplankton; proxy for phytoplankton biomass  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Typical unit** | Milligrams per cubic meter (mg/m³)  [incois.gov](https://incois.gov.in/geoportal/MFASPFZ/index.html) |
| **What it can legitimately indicate** | Phytoplankton biomass, primary productivity potential, biologically productive zones, ocean fronts (chlorophyll gradients)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **What it cannot prove** | Fish abundance, zooplankton distribution, subsurface chlorophyll, species composition, water quality without additional parameters  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Spatial/temporal considerations** | Satellite ocean color: 1 km (OCM) to 4 km (MODIS); daily to weekly composites; cloud contamination, sun glint, atmospheric correction errors, coastal algorithm uncertainty  [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf) |
| **How ORCA may use it** | Identify productive zones, ocean fronts, upwelling signatures  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory); contribute to PFZ as one parameter (SST + Chl-a integration)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory); never alone predict fish catch  [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf) |

**Critical Scientific Distinction**:  
**DO NOT ALLOW**: "High chlorophyll = high fish abundance."  
**Scientifically defensible reasoning**: "Chlorophyll-a can act as a proxy for phytoplankton biomass/productivity and may contribute to habitat interpretation when considered together with other relevant variables (SST, fronts, bathymetry)". [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Data Quality Note**: Chlorophyll algorithms have substantial uncertainties in optically complex coastal waters; bias correction may be required. Quality flags must be checked (sun glint, clouds, atmospheric correction failure). [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)

### 4.2 Primary Productivity

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Rate of carbon fixation by phytoplankton (photosynthesis); typically modeled from chlorophyll, SST, light  [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production) |
| **Typical unit** | Milligrams carbon per square meter per day (mg C/m²/day)  [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production) |
| **What it can legitimately indicate** | Ecosystem energy base, potential fish habitat quality, biogeochemical cycling  [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production) |
| **What it cannot prove** | Fish catch, trophic transfer efficiency, species-specific habitat suitability  [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production) |
| **Spatial/temporal considerations** | Model-derived: 1/12° to 1/4° resolution; daily to monthly; algorithm uncertainty from chlorophyll, light, temperature parameterization  [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production) |
| **How ORCA may use it** | Contribute to ecosystem productivity interpretation; identify high-productivity zones as potential fish habitat (with caveats)  [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production) |

**Insufficient authoritative evidence – do not infer** direct primary productivity–fish catch relationships without peer-reviewed validation for specific species/region.

### 4.3 Phytoplankton

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Microscopic photosynthetic organisms; base of marine food web  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Typical unit** | Biomass (mg Chl-a/m³), abundance (cells/L), or carbon (mg C/m³)  [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production) |
| **What it can legitimately indicate** | Food web base, primary production, habitat quality for zooplankton and planktivorous fish  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **What it cannot prove** | Fish abundance, species composition, trophic transfer efficiency, harmful algal blooms without additional data  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **Spatial/temporal considerations** | Satellite chlorophyll: surface only; no species discrimination; blooms can be ephemeral (days to weeks)  [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production) |
| **How ORCA may use it** | Identify bloom conditions, productive zones; contribute to PFZ and ecosystem interpretation  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |

**Scientific Constraint**: Phytoplankton biomass (chlorophyll) is a necessary but not sufficient condition for fish aggregation; fish distribution depends on temperature, oxygen, predation, fishing pressure, and other factors. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 4.4 Marine Heat Waves (MHW)

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Prolonged discrete anomalously warm water event  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891) |
| **Typical unit** | SST anomaly (°C) above 90th percentile threshold; duration (days); intensity (°C above threshold)  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891) |
| **What it can legitimately indicate** | Ecosystem stress, species range shifts, coral bleaching risk, fishery impacts, anomalous thermal conditions  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891) |
| **What it cannot prove** | Specific species mortality, fish catch reduction, ecosystem collapse without additional ecological data  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891) |
| **Spatial/temporal considerations** | Definition: SST > 90th percentile for ≥5 consecutive days (Hobday et al. 2016)  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891); gaps <2–3 days collated into single event  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf); baseline period: 30-year climatology (e.g., 1983–2012)  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/69979/noaa_69979_DS1.pdf) |
| **How ORCA may use it** | Detect MHW events using Hobday et al. 2016 criteria  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891); warn of ecosystem stress conditions; never claim specific ecological impacts without peer-reviewed evidence  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891) |

**Scientific Definition (Hobday et al. 2016)**:  
A marine heatwave is "a prolonged discrete anomalously warm water event that can be described by its duration, intensity, rate of evolution, and spatial extent". [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
**Quantitative**: SST exceeds 90th percentile of seasonally varying threshold for at least 5 consecutive days. [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

**Categories** (Hobday et al. 2018):  
- **Moderate**: SST ≥ 90th percentile  
- **Strong**: SST ≥ 92.5th percentile  
- **Severe/Extreme**: SST ≥ 95th percentile [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf)

### 4.5 Ocean Fronts

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Boundaries between water masses with different properties (temperature, salinity, chlorophyll)  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf) |
| **Typical unit** | Gradient magnitude (°C/km, mg/m³/km); location (lat/lon)  [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf) |
| **What it can legitimately indicate** | Nutrient convergence, enhanced productivity, fish aggregation zones, water mass boundaries  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf) |
| **What it cannot prove** | Fish presence at specific time, species composition, front persistence without temporal data  [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf) |
| **Spatial/temporal considerations** | Detected from SST and chlorophyll gradients; resolution: 1–4 km; fronts can shift daily with wind and currents  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| **How ORCA may use it** | Identify fronts from SST and chlorophyll breaks  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf); contribute to PFZ (fronts are key PFZ features)  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf); advise on probable shifts using wind data  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |

**Scientific Definition**: "Fronts are the boundaries between two water masses with different properties. They can be easily detected as breaks in the ocean colour (chlorophyll concentration) or SST of water masses on an image". [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf)

### 4.6 Upwelling

| Aspect | Scientific Specification |
|--------|-------------------------|
| **What it represents** | Vertical transport of cold, nutrient-rich subsurface water to surface; driven by wind (coastal) or divergence (equatorial)  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf) |
| **Typical unit** | Vertical velocity (m/day, often modeled); identified by cold SST, high chlorophyll signatures  [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf) |
| **What it can legitimately indicate** | Enhanced productivity, fish habitat potential, cold SST anomalies, nutrient supply  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf) |
| **What it cannot prove** | Fish catch, upwelling strength without in-situ data, subsurface nutrient concentration  [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf) |
| **Spatial/temporal considerations** | Identified from SST (cold) and chlorophyll (high); seasonal to interannual variability; coastal upwelling favored by alongshore wind  [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf) |
| **How ORCA may use it** | Identify upwelling signatures from SST + chlorophyll patterns  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf); contribute to PFZ and ecosystem productivity interpretation  [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf) |

***

## 5. Ecosystem Rules

### 5.1 Ecosystem Anomalies

**Definition**: Deviations from long-term mean or climatological state in ecosystem parameters (chlorophyll, SST, productivity, etc.). [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production)

**ORCA Handling**:
- Must compare against appropriate baseline (e.g., 30-year climatology for MHW, seasonal mean for chlorophyll ) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- Must specify anomaly type (positive/negative), magnitude, duration, spatial extent
- Must NOT claim ecosystem collapse, species extinction, or fishery failure without peer-reviewed evidence [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

**Insufficient authoritative evidence – do not infer** causal links between anomalies and specific ecological outcomes without validation.

### 5.2 Fish Habitat Indicators

**Scientifically Valid Indicators** (when combined):
- SST within species-specific thermal range [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Chlorophyll-a as proxy for productivity [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Ocean fronts (SST/chlorophyll gradients) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- Bathymetry (depth range for species) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Upwelling signatures (cold SST, high chlorophyll) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- SSH anomalies (eddies, currents) [science](https://www.science.gov/topicpages/o/ocean+color+parameters)

**Scientific Constraints**:
- No single indicator deterministically predicts fish presence [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- PFZ is a **probabilistic** indicator, not a guarantee [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Validation studies show PFZ advisories are "more beneficial" and reduce search time, but do not guarantee catch [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**ORCA Must State**: "PFZ indicates areas with higher probability of fish aggregation based on satellite oceanography; actual catch depends on fishing gear, timing, species behavior, and other factors". [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 6. Fisheries-Related Rules

### 6.1 Potential Fishing Zone (PFZ)

**Scientific Basis** (INCOIS):
- PFZ advisories are generated using SST (NOAA-AVHRR, MetOp) and chlorophyll (Oceansat-2 OCM, MODIS Aqua) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Methodology: Integration of chlorophyll and SST images (Dwivedi & co-workers) to identify fronts, eddies, rings, upwelling areas [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- Operational since 1990s (MARSIS programme); validated by feedback from fishermen and research projects [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**What PFZ Represents**:
- **Observation**: SST and chlorophyll satellite data [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Derived Indicator**: PFZ map/coordinates from SST+chlorophyll integration [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Scientific Interpretation**: Areas with oceanographic features favorable for pelagic fish aggregation (fronts, eddies, upwelling) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- **AI Inference**: Higher probability of fish presence compared to non-PFZ areas [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Recommendation**: Fishermen may target PFZ locations to reduce search time and fuel cost [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**What PFZ Cannot Prove**:
- Guaranteed fish catch [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Species composition [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)
- Fish abundance (only relative probability) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Persistence beyond advisory validity (PFZ shifts with wind/currents) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Spatial/Temporal Considerations**:
- Generated thrice weekly (INCOIS) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- Valid for 24–48 hours; features shift with wind and currents [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Resolution: 1 km chlorophyll, 4 km SST; PFZ line/curve delineated from composite [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
- Wind speed/direction provided to guide fishermen on probable shifts [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Validation Evidence**:
- "PFZ advisories were found more beneficial to artisanal, motorised and small mechanised sector fishermen engaged in pelagic fishing activities such as ring seining, gill netting etc., thereby reducing the searching time which in turn result in the saving of valuable fuel oil and also human effort" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- "Catch in the PFZ area is substantially higher when compared to the other areas" (feedback from validation projects) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- PFZ advisories are "good indicators of the availability/abundance of pelagic fishes such as sardines, mackerel, anchovies, tunas and carangids" [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)

**ORCA Must State**:
- PFZ is based on SST + chlorophyll integration [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- PFZ indicates higher probability, not certainty [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- PFZ validity is limited (24–48 hours); features shift [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Actual catch depends on gear, timing, species, fishing skill, and other factors [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 6.2 PFZ Scientific Limitations

**DO NOT ALLOW**:
- "PFZ guarantees fish catch" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- "High chlorophyll + optimal SST = high fish abundance" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- "PFZ is valid for >48 hours without update" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- "PFZ applies to all fish species equally" [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)

**Scientifically Defensible**:
- "PFZ identifies areas with oceanographic features (fronts, eddies, upwelling) associated with higher probability of pelagic fish aggregation" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- "Validation studies show PFZ advisories reduce search time and improve catch efficiency for pelagic species" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- "PFZ should be used with wind information to account for feature drift" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 7. Weather and Safety Rules

### 7.1 Ocean State Forecast (OSF)

**Source**: INCOIS Ocean State Forecast [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

**Parameters**:
- Significant wave height (Hs)
- Ocean surface wind (speed, direction)
- Swell (remotely generated waves) [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

**Forecast Horizon**: 5–7 days, 3-hourly intervals, daily updates [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

**Validation**: Routinely validated against coastal and open-ocean buoys, altimeters [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)

**ORCA Handling**:
- Must label as forecast, include valid period, update time [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)
- Must NOT claim guaranteed safety; must include uncertainty [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- Must cite INCOIS as source for Indian Ocean region [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

### 7.2 High Wave Alert (INCOIS)

**Thresholds**: [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- **Watch**: Hs between 2.5 and 3.0 m
- **Alert**: Hs > 3.0 m

**Cause**: Disturbed conditions from local winds or high swells [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)

**ORCA Handling**:
- Must use INCOIS thresholds for Indian Ocean [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- Must NOT claim "safe" or "unsafe" deterministically; must state probabilistic risk [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- Must include source (INCOIS), timestamp, forecast validity [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

**Safety Constraint**: ORCA must not claim guaranteed fishing safety or navigation safety. Safety outputs must identify:
- Source (e.g., "INCOIS Ocean State Forecast")
- Timestamp (e.g., "Issued 31 Aug 2026, valid 31 Aug – 5 Sep 2026")
- Forecast/observation status (e.g., "5-day forecast, daily update")
- Relevant uncertainty (e.g., "Wave height forecast uncertainty: ±0.5 m") [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

### 7.3 Marine Hazards (Cyclones, Tsunamis, etc.)

**ORCA Handling**:
- Must rely on official warnings (INCOIS, IMD, NOAA) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must NOT generate independent hazard predictions without authoritative source
- During marine fishing ban or adverse sea state (cyclones, high waves, tsunamis), PFZ service is suspended [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Insufficient authoritative evidence – do not infer** hazard conditions without official warning.

***

## 8. Geospatial Rules

### 8.1 Coordinate Systems

**Requirements**:
- All spatial data must use WGS84 (EPSG:4326) latitude/longitude [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Latitude range: -90 to +90; Longitude range: -180 to +180 (or 0–360E)
- Must validate coordinates are within ocean domain (not on land) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**ORCA Must**:
- Reject coordinates on land for marine queries
- Flag coordinates outside data coverage (e.g., polar gaps, coastal land contamination)
- Use consistent coordinate precision (e.g., 4 decimal places ≈ 10 m resolution)

### 8.2 Spatial Resolution Consistency

**Requirements**:
- Must respect native resolution of each dataset:
  - SST: 1–4 km [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
  - Chlorophyll: 1 km (OCM) to 4 km (MODIS) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
  - SSH: 1/12° to 1/4° (~9–25 km) [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
  - Wind/Wave: 10–25 km (model) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- Must NOT infer sub-grid features (e.g., claim 100 m precision from 4 km data)
- Must aggregate/interpolate consistently when combining datasets

**Insufficient authoritative evidence – do not infer** features smaller than data resolution.

### 8.3 Geographic Consistency

**Requirements**:
- Must use region-appropriate data products (e.g., INCOIS for Indian Ocean, Copernicus for global/European waters) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must respect coastal boundaries (ocean color algorithms degraded in optically complex coastal waters) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
- Must flag data gaps (clouds, sun glint, polar night) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)

**ORCA Must**:
- Check data coverage before inference
- Flag coastal contamination risk (e.g., "Chlorophyll data may be unreliable within 10 km of coast due to optically complex waters" ) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
- Use appropriate regional climatology (e.g., 30-year baseline for MHW must be region-specific) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

***

## 9. Temporal Reasoning Rules

### 9.1 Timestamp Requirements

**Every data point must include**:
- Acquisition time (for observations)
- Validity period (for forecasts)
- Timezone (UTC or local)
- Latency (e.g., "L4 SST: 1-day latency" ) [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)

**ORCA Must**:
- Reject data without timestamp
- Flag stale data (e.g., SST > 48 hours old for dynamic features)
- Distinguish observation vs. forecast clearly

### 9.2 Temporal Resolution

**Typical Resolutions**:
- SST: Daily to weekly composites [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
- Chlorophyll: Daily to weekly (cloud-dependent) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
- PFZ: Thrice weekly (INCOIS) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- OSF: 3-hourly, 5–7 day forecast [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)
- MHW: Daily detection, monthly climatology [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

**ORCA Must**:
- Respect temporal resolution (e.g., do not claim daily chlorophyll if only weekly composite available)
- Interpolate temporally only with appropriate methods (e.g., linear for SST, not for episodic blooms)
- Flag temporal gaps (e.g., "No chlorophyll data for 25–28 Aug due to cloud cover")

### 9.3 Temporal Dynamics

**Scientific Constraints**:
- Ocean features evolve: fronts shift, eddies propagate, blooms develop/decay [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- PFZ validity: 24–48 hours; features shift with wind/currents [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- MHW: Minimum 5 days duration; gaps <2–3 days collated [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

**ORCA Must**:
- Advise users on feature drift (e.g., "PFZ may shift 10–20 km/day with wind; use wind vectors to estimate drift" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- NOT use stale data for dynamic features (e.g., do not use 7-day-old SST for front detection)
- Distinguish persistent features (bathymetry, climatology) from ephemeral (fronts, blooms, MHW)

***

## 10. Data Quality Rules

### 10.1 Quality Flags

**Satellite Data Quality Flags** (must check): [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Cloud contamination
- Sun glint
- Atmospheric correction failure
- Algorithm failure (e.g., chlorophyll retrieval failure in turbid water)
- Land/ice contamination
- Quality level (0–4, where 4 is best) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)

**ORCA Must**:
- Reject data with quality flag < threshold (e.g., quality level < 3 for operational use)
- Flag low-quality data to user (e.g., "Chlorophyll data quality reduced due to sun glint")
- Use quality flags to weight confidence (see Scientific Confidence Policy)

### 10.2 Validation Status

**Requirements**:
- Must use validated products (e.g., INCOIS PFZ, Copernicus L4 SST, NOAA MHW) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must cite validation studies where available (e.g., "PFZ validated by CMFRI and fisherman feedback" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must flag experimental/research products (e.g., "NOAA MHW forecast: experimental, research use only" ) [psl.noaa](https://psl.noaa.gov/marine-heatwaves/)

**Insufficient authoritative evidence – do not infer** from unvalidated or experimental products without disclaimer.

### 10.3 Uncertainty Quantification

**Types of Uncertainty**:
- **Measurement uncertainty**: Sensor noise, calibration error [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- **Algorithm uncertainty**: Retrieval algorithm error (e.g., chlorophyll in coastal waters) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
- **Representativeness uncertainty**: Satellite footprint vs. in-situ point [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- **Temporal uncertainty**: Latency, compositing period [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- **Interpretive uncertainty**: Scientific inference from data (e.g., PFZ → fish probability) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**ORCA Must**:
- Propagate uncertainty through inference chain (observation → indicator → interpretation → recommendation)
- Communicate uncertainty to user (e.g., "Chlorophyll uncertainty: ±30% in coastal waters" ) [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
- Reduce confidence when uncertainty is high (see Scientific Confidence Policy)

***

## 11. Data Freshness Rules

### 11.1 Freshness Thresholds

| Data Type | Maximum Age for Operational Use | Rationale |
|-----------|--------------------------------|-----------|
| SST (dynamic features: fronts, MHW) | 24–48 hours | SST evolves rapidly; fronts shift daily  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| Chlorophyll (blooms, fronts) | 24–48 hours | Blooms develop/decay rapidly; cloud gaps  [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf) |
| PFZ Advisory | Valid period (24–48 hours)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | Features shift with wind/currents  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |
| Ocean State Forecast | Within forecast window (5–7 days)  [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp) | Skill decreases with forecast lead time  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf) |
| Bathymetry | No expiration (static)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzWebGis) | Seafloor does not change on human timescales |
| Climatology (MHW baseline) | 30-year period (e.g., 1983–2012)  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891) | Long-term baseline for anomaly detection |

**ORCA Must**:
- Reject data older than freshness threshold for dynamic features
- Flag stale data to user (e.g., "SST data is 5 days old; front location may have shifted")
- Prioritize latest available data (e.g., prefer 1-day latency L4 SST over 4-day latency) [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)

### 11.2 Latency Awareness

**Typical Latencies**:
- L2 SST (swath): Near-real-time (hours) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- L4 SST (analyzed): 1-day (near-real-time) to 4-day (retrospective) [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)
- Chlorophyll (L2/L3): 1–3 days (cloud-dependent) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
- PFZ: Thrice weekly (INCOIS) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- OSF: Daily update, 5–7 day forecast [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

**ORCA Must**:
- Account for latency in temporal reasoning (e.g., "4-day latency SST represents conditions 4 days ago")
- Prefer lower-latency products for operational use
- Communicate latency to user (e.g., "SST data latency: 1 day; represents 30 Aug 2026 conditions")

***

## 12. Uncertainty Rules

### 12.1 Uncertainty Propagation

**Inference Chain**:
1. **Observation** (e.g., SST from AVHRR): Measurement uncertainty (e.g., ±0.5°C) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
2. **Derived Indicator** (e.g., MHW): Algorithm uncertainty (e.g., 90th percentile threshold uncertainty) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
3. **Scientific Interpretation** (e.g., "ecosystem stress"): Interpretive uncertainty (e.g., species-specific response variability) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
4. **AI Inference** (e.g., "reduced fish catch probability"): Model uncertainty (e.g., AI confidence calibration)
5. **Recommendation** (e.g., "avoid fishing in MHW zone"): Decision uncertainty (e.g., socioeconomic factors)

**ORCA Must**:
- Propagate uncertainty at each step (e.g., SST uncertainty → MHW detection uncertainty → ecosystem impact uncertainty)
- Reduce confidence when uncertainty compounds (see Scientific Confidence Policy)
- Communicate key uncertainties to user (e.g., "MHW detection uncertainty: ±1 day in start/end date" ) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

### 12.2 Confidence Calibration

**AI-Generated Confidence**:
- Must NOT be presented as scientific probability unless mathematically/calibrationally justified [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- Must be based on validated methodology (e.g., cross-validation, bootstrap, Bayesian calibration)
- Must distinguish AI confidence (model certainty) from scientific probability (empirical frequency)

**Insufficient authoritative evidence – do not infer** scientific probabilities from AI confidence scores without validation.

***

## 13. Evidence Rules

### 13.1 Evidence Hierarchy

| Evidence Level | Description | ORCA Use |
|----------------|-------------|----------|
| **Level 1**: Peer-reviewed meta-analysis / operational validation | Multiple peer-reviewed studies, operational validation (e.g., INCOIS PFZ validation  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)) | Strong basis for inference |
| **Level 2**: Single peer-reviewed study / government technical report | One peer-reviewed paper, government technical report (e.g., INCOIS technical reports  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)) | Moderate basis; flag as single-study |
| **Level 3**: Consensus scientific definition | Community consensus (e.g., Hobday et al. 2016 MHW definition  [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)) | Strong basis for definitions |
| **Level 4**: Expert judgment / preliminary research | Expert opinion, preprints, conference abstracts | Weak basis; flag as preliminary |
| **Level 5**: Anecdotal / unverified | Fisherman feedback without validation, blogs, social media | Do not use as scientific evidence |

**ORCA Must**:
- Cite evidence level for each inference (e.g., "PFZ validation: Level 1 ") [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Prefer Level 1–3 evidence for operational inferences
- Flag Level 4–5 evidence as preliminary or anecdotal

### 13.2 Citation Requirements

**Every scientific claim must cite**:
- Source (agency, paper, product)
- Year (for papers) or version (for products)
- DOI or URL (where available)

**Example**:
- "Marine heatwaves are defined as SST > 90th percentile for ≥5 days  (Hobday et al. 2016, DOI: 10.1038/nclimate2935)" [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- "PFZ advisories use SST from NOAA-AVHRR and chlorophyll from Oceansat-2 OCM  (INCOIS, 2026)" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Insufficient authoritative evidence – do not infer** without citation.

***

## 14. AI Inference Rules

### 14.1 Inference Boundaries

**Allowed Inferences**:
- Identify oceanographic features from data (e.g., "SST gradient indicates front" ) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- Combine multiple parameters for habitat interpretation (e.g., "SST + chlorophyll + bathymetry suggest productive zone" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Apply validated empirical relationships (e.g., "PFZ associated with higher catch probability for pelagic species" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Detect anomalies relative to climatology (e.g., "SST > 90th percentile indicates MHW" ) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

**Prohibited Inferences**:
- Deterministic fish catch prediction from single parameter (e.g., "High chlorophyll = high catch") [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Causal claims without peer-reviewed evidence (e.g., "MHW causes fishery collapse" without validation) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- Extrapolation beyond data domain (e.g., infer subsurface conditions from surface data) [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
- Species-specific predictions without species-level validation (e.g., "PFZ guarantees sardine catch" without species-specific PFZ validation) [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)

### 14.2 Inference Transparency

**ORCA Must**:
- Distinguish observation, indicator, interpretation, inference, recommendation (see Section 1.1)
- State assumptions (e.g., "Assuming wind-driven drift, PFZ may shift 10 km east" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Flag speculative inferences (e.g., "Preliminary evidence suggests...; requires validation")
- Provide alternative explanations (e.g., "High chlorophyll may indicate bloom OR sediment resuspension; additional data needed" ) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)

***

## 15. Recommendation Rules

### 15.1 Recommendation Hierarchy

**Recommendation Types**:
1. **Informational**: "SST is 28°C at location X" (direct data)
2. **Interpretive**: "SST gradient indicates ocean front" (scientific interpretation)
3. **Advisory**: "PFZ located at 12°N, 78°E; may reduce search time" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
4. **Safety**: "High Wave Alert: Hs > 3.0 m; exercise caution" [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
5. **Actionable**: "Target PFZ zone with ring seine; use wind vectors to estimate drift" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**ORCA Must**:
- Match recommendation type to evidence level (e.g., Level 1 evidence → actionable recommendation; Level 4 → informational only)
- Include caveats (e.g., "PFZ reduces search time but does not guarantee catch" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Provide alternatives (e.g., "If PFZ inaccessible, consider nearby frontal zones")

### 15.2 Recommendation Constraints

**Prohibited Recommendations**:
- "Guaranteed catch at PFZ" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- "Safe to fish" or "Unsafe to fish" (deterministic safety) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- "Species X will be present" without species-specific validation [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)
- "Ignore PFZ; use traditional knowledge only" (disregarding scientific evidence)

**Scientifically Defensible Recommendations**:
- "PFZ may improve catch efficiency for pelagic species; validation studies show reduced search time " [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- "High Wave Alert (Hs > 3.0 m); small vessels should exercise caution " [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- "MHW detected; ecosystem stress possible; monitor local fishery advisories " [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

***

## 16. Safety-Critical Rules

### 16.1 Safety Disclaimer Requirements

**Every safety-related output must include**:
- **Source**: "INCOIS Ocean State Forecast" [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)
- **Timestamp**: "Issued 31 Aug 2026, valid 31 Aug – 5 Sep 2026" [incois.gov](https://incois.gov.in/MarineFisheries/TextDataHome?mfid=1&request_locale=en)
- **Forecast/Observation Status**: "5-day forecast, daily update" [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)
- **Uncertainty**: "Wave height forecast uncertainty: ±0.5 m" [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- **Disclaimer**: "ORCA does not guarantee fishing or navigation safety; consult official advisories and local conditions"

### 16.2 Safety Thresholds

**INCOIS High Wave Alert**: [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- **Watch**: Hs 2.5–3.0 m
- **Alert**: Hs > 3.0 m

**ORCA Must**:
- Use INCOIS thresholds for Indian Ocean [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- NOT override official warnings (e.g., if INCOIS issues cyclone warning, suspend PFZ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Advise caution, not prohibition (e.g., "High Wave Alert; small vessels should exercise caution" NOT "Do not fish")

**Marine Fishing Ban**:
- During government-imposed marine fishing ban, PFZ service is suspended [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- ORCA must NOT generate PFZ during ban periods

### 16.3 Hazard Communication

**ORCA Must**:
- Prioritize official hazard warnings (INCOIS, IMD, NOAA) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Use clear, conservative language (e.g., "High risk" NOT "Certain disaster")
- Provide actionable guidance (e.g., "Seek shelter; monitor updates" NOT "You will die")

**Prohibited**:
- "Guaranteed safety" or "No risk" claims
- Independent hazard predictions without authoritative source
- Minimizing official warnings (e.g., "Ignore cyclone warning; conditions are fine")

***

## 17. Scientific Anti-Hallucination Rules

### 17.1 Prohibited Statements

**ORCA Must NEVER state without sufficient evidence**:

1. **"High chlorophyll guarantees high fish catch"** [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **"PFZ is 100% accurate"** [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
3. **"SST alone predicts fish abundance"** [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
4. **"Marine heatwave will cause fishery collapse"** (without peer-reviewed evidence for specific region/species) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
5. **"This eddy will persist for 2 weeks"** (without model forecast validation) [science](https://www.science.gov/topicpages/o/ocean+color+parameters)
6. **"Salinity is 35 PSU at location X"** (without SSS data) [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
7. **"Subsurface temperature is 20°C at 50 m depth"** (from surface SST only) [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
8. **"Fish species X is present"** (without species-specific observation or validated model) [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)
9. **"Wave height is exactly 2.5 m"** (without uncertainty; should be "2.5 m ± 0.5 m") [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
10. **"Safe to fish"** or **"Unsafe to fish"** (deterministic safety claims) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)

### 17.2 Evidence Verification

**ORCA Must**:
- Cross-check claims against multiple sources (e.g., SST from AVHRR + MODIS) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Verify temporal consistency (e.g., SST trend over time) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- Validate spatial consistency (e.g., SST gradient matches front location) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- Flag inconsistencies (e.g., "SST and chlorophyll patterns disagree; confidence reduced")

**Insufficient authoritative evidence – do not infer** if sources conflict or data is missing.

***

## 18. Agent-Specific Scientific Constraints

### 18.1 Ocean Agent (Physical Oceanography)

**Scope**: SST, SSS, SSH, currents, wind, waves, MLD, bathymetry [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Constraints**:
- Must use validated physical oceanography products (INCOIS, Copernicus, NASA, NOAA) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must NOT infer biological state from physical parameters alone (e.g., "High SST = low fish" without ecological validation) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must propagate physical uncertainty (e.g., SST ±0.5°C, wave height ±0.5 m) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Must respect spatial/temporal resolution (e.g., 4 km SST, daily composites) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)

**Example Valid Inference**: "SST gradient of 2°C over 10 km indicates ocean front; front may shift 10 km/day with wind " [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Invalid Inference**: "SST of 28°C guarantees high fish catch" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 18.2 Ecosystem Agent (Biological Oceanography)

**Scope**: Chlorophyll-a, primary productivity, phytoplankton, MHW, ocean fronts, upwelling, ecosystem anomalies [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Constraints**:
- Must use validated ocean color products (INCOIS, Copernicus, NASA) with quality flags [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Must NOT claim chlorophyll alone predicts fish abundance [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must apply Hobday et al. 2016 MHW definition (SST > 90th percentile for ≥5 days) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- Must flag coastal algorithm uncertainty (chlorophyll in turbid waters) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
- Must distinguish observation (chlorophyll) from interpretation (productivity, ecosystem stress) [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production)

**Example Valid Inference**: "Chlorophyll-a = 2 mg/m³ indicates elevated phytoplankton biomass; combined with SST front, suggests productive zone " [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Invalid Inference**: "Chlorophyll = 2 mg/m³ means high fish catch" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 18.3 Fisheries Agent (Fisheries Science)

**Scope**: PFZ, fish habitat indicators, catch probability, species distribution [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Constraints**:
- Must use INCOIS PFZ methodology (SST + chlorophyll integration) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must NOT claim PFZ guarantees catch [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must cite validation evidence (e.g., "PFZ reduces search time for pelagic species" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must account for PFZ drift (wind/currents) and validity period (24–48 hours) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must distinguish pelagic vs. demersal species (PFZ validated primarily for pelagic) [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)

**Example Valid Inference**: "PFZ at 12°N, 78°E; validation studies show reduced search time for pelagic species; use wind vectors to estimate drift " [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Invalid Inference**: "PFZ guarantees 500 kg catch of sardines" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 18.4 Safety Agent (Marine Safety)

**Scope**: Wave height, wind, marine hazards, high wave alerts, fishing bans [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Constraints**:
- Must use INCOIS Ocean State Forecast and High Wave Alert thresholds [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)
- Must NOT claim guaranteed safety [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
- Must include source, timestamp, forecast status, uncertainty in all safety outputs [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)
- Must suspend PFZ during marine fishing ban or adverse sea state (cyclones, high waves, tsunamis) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must prioritize official warnings (INCOIS, IMD, NOAA) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Valid Output**: "High Wave Alert: Hs > 3.0 m (INCOIS OSF, issued 31 Aug 2026, valid 31 Aug – 5 Sep 2026; uncertainty ±0.5 m). Small vessels should exercise caution. ORCA does not guarantee fishing safety." [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)

**Example Invalid Output**: "Safe to fish; wave height is 2.0 m" (deterministic safety claim) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)

### 18.5 Geospatial Agent (Spatial Analysis)

**Scope**: Coordinates, spatial resolution, geographic consistency, data coverage [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Constraints**:
- Must use WGS84 coordinates; validate ocean domain (not land) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must respect native spatial resolution (e.g., 1 km chlorophyll, 4 km SST) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
- Must flag coastal contamination (ocean color algorithms degraded in turbid waters) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
- Must check data coverage (cloud gaps, polar night, land contamination) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Must use region-appropriate products (INCOIS for Indian Ocean, Copernicus for global) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Valid Inference**: "Coordinates 12°N, 78°E are within Indian Ocean; chlorophyll data available at 1 km resolution; quality flag: good (no sun glint, clouds)" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Invalid Inference**: "Coordinates 12°N, 78°E have chlorophyll = 2 mg/m³ at 100 m resolution" (exceeds native resolution) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)

### 18.6 RAG Agent (Retrieval-Augmented Generation)

**Scope**: Scientific source attribution, literature retrieval, evidence synthesis [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Constraints**:
- Must cite authoritative sources (ISRO, MOSDAC, INCOIS, NASA, NOAA, Copernicus, peer-reviewed literature) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must NOT use random blogs or unverified sources [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must provide full citation (source, year, DOI/URL) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- Must flag preliminary or conflicting evidence [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
- Must distinguish observation, indicator, interpretation, inference, recommendation [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Valid Output**: "Marine heatwaves are defined as SST > 90th percentile for ≥5 days  (Hobday et al. 2016, DOI: 10.1038/nclimate2935)" [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

**Example Invalid Output**: "Marine heatwaves are very hot ocean periods" (no citation, vague) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

### 18.7 Verification Agent (Scientific Validation)

**Scope**: Scientific consistency, source provenance, timestamp, unsupported inference detection [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Constraints**:
- Must check scientific consistency (e.g., SST + chlorophyll + SSH agree on front location) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- Must verify source provenance (e.g., INCOIS PFZ from SST + chlorophyll) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must validate timestamps (e.g., SST not older than 48 hours for dynamic features) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must flag unsupported inferences (e.g., "chlorophyll alone predicts catch" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must enforce evidence hierarchy (Level 1–5; Section 13.1)

**Example Valid Check**: "PFZ inference validated: SST + chlorophyll integration per INCOIS methodology; timestamp: 31 Aug 2026 (fresh); quality flags: good" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Invalid Check**: "PFZ inference: chlorophyll alone used (invalid; requires SST + chlorophyll) " [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 18.8 Coordinator (Multi-Agent Synthesis)

**Scope**: Combine evidence from Ocean, Ecosystem, Fisheries, Safety, Geospatial, RAG, Verification agents [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Constraints**:
- Must combine evidence rather than invent scientific relationships [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must resolve conflicts (e.g., SST vs. chlorophyll disagreement → reduce confidence) [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)
- Must propagate uncertainty across agents (e.g., Ocean Agent SST uncertainty → Fisheries Agent PFZ uncertainty) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
- Must NOT collapse observation → indicator → interpretation → inference → recommendation into one statement [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Must produce traceable, cited output (every claim linked to source) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Valid Synthesis**:  
"Observation: SST = 28°C, chlorophyll = 2 mg/m³ at 12°N, 78°E (INCOIS, 31 Aug 2026). [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
Derived Indicator: SST gradient + chlorophyll gradient indicate ocean front. [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
Scientific Interpretation: Fronts are associated with enhanced productivity and fish aggregation. [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
AI Inference: PFZ delineated at front location; higher probability of pelagic fish presence. [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
Recommendation: Target PFZ zone; use wind vectors to estimate drift; PFZ reduces search time but does not guarantee catch." [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Example Invalid Synthesis**:  
"High chlorophyll and warm SST mean high fish catch at 12°N, 78°E" (collapses inference chain; deterministic claim) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 19. Scientific Validation Requirements

### 19.1 Pre-Deployment Validation

**ORCA Must**:
- Validate all scientific inferences against peer-reviewed literature or operational validation studies [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Test on historical data with known outcomes (e.g., PFZ validation against catch data) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Document validation methodology and results (e.g., "PFZ accuracy: 70% hit rate for pelagic species" ) [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)
- Flag unvalidated inferences as experimental or preliminary

### 19.2 Continuous Monitoring

**ORCA Must**:
- Monitor scientific literature for updates (e.g., new MHW definitions, PFZ methodology improvements) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- Update rules when authoritative sources revise products (e.g., new chlorophyll algorithm, SST reprocessing) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Track user feedback and validation studies (e.g., fisherman catch reports, research validations) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Deprecate rules when evidence is contradicted or superseded

### 19.3 Audit Trail

**ORCA Must**:
- Log all data sources, timestamps, quality flags for each inference [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Log all scientific rules applied (e.g., "MHW detection: Hobday et al. 2016" ) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
- Log all confidence levels and uncertainty estimates [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Enable post-hoc audit (e.g., "Why did ORCA recommend PFZ at location X on date Y?")

***

## 20. Scientific Confidence Policy

### 20.1 Confidence Levels

**ORCA Must Assign Confidence Based on**:
- Data quality (quality flags, resolution, latency) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Evidence level (Level 1–5; Section 13.1) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Parameter agreement (e.g., SST + chlorophyll + SSH agree on front) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- Temporal freshness (e.g., SST < 24 hours old vs. > 48 hours) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Spatial consistency (e.g., no land contamination, coastal algorithm validity) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)

**Confidence Levels**:

| Confidence | Criteria | ORCA Action |
|------------|----------|-------------|
| **High** | Level 1–2 evidence; all parameters agree; data quality good; fresh (<24 hours); spatial consistency good | Strong recommendation (e.g., "PFZ likely to improve catch efficiency"  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)) |
| **Medium** | Level 2–3 evidence; most parameters agree; data quality acceptable; fresh (24–48 hours); minor spatial issues | Advisory with caveats (e.g., "PFZ may improve catch; confidence reduced due to cloud gaps"  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)) |
| **Low** | Level 3–4 evidence; parameters disagree; data quality reduced; stale (>48 hours); spatial issues (coastal contamination) | Informational only (e.g., "SST suggests front; chlorophyll unavailable; confidence low"  [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)) |
| **Insufficient Evidence** | Level 4–5 evidence; critical data missing; conflicting sources; unvalidated inference | Do not infer; state "Insufficient authoritative evidence – do not infer"  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) |

**DO NOT assign arbitrary percentages** (e.g., "70% confidence") unless implementation has validated methodology (e.g., cross-validation, bootstrap, Bayesian calibration). [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

### 20.2 Confidence Modifiers

**Increase Confidence**:
- Multiple independent sources agree (e.g., SST from AVHRR + MODIS) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Validation studies support inference (e.g., PFZ validation ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- High-quality data (quality flag = 4, low uncertainty) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Fresh data (<24 hours for dynamic features) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Decrease Confidence**:
- Parameters disagree (e.g., SST indicates front, chlorophyll does not) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
- Low-quality data (quality flag < 3, high uncertainty) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
- Stale data (>48 hours for dynamic features) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Coastal contamination (ocean color algorithms degraded) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
- Conflicting sources (e.g., INCOIS vs. Copernicus SST disagree) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Set to Insufficient Evidence**:
- Critical data missing (e.g., no chlorophyll for PFZ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Unvalidated inference (e.g., new parameter combination without peer-reviewed support) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Conflicting authoritative sources (e.g., INCOIS vs. NOAA MHW detection disagree) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

### 20.3 Confidence Communication

**ORCA Must**:
- Communicate confidence level to user (e.g., "High confidence: PFZ validated by multiple studies" ) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- Explain confidence rationale (e.g., "Confidence reduced due to cloud gaps in chlorophyll data" ) [acrs-aars](https://acrs-aars.org/proceeding/ACRS2020/ifomqo.pdf)
- Adjust recommendation strength based on confidence (e.g., High → actionable; Low → informational)
- Never present AI confidence as scientific probability without validation [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

***

## 21. Scientific Red Flags

**ORCA Must NEVER Make These Statements Without Sufficient Evidence**:

### 21.1 Fisheries Red Flags

1. ❌ "PFZ guarantees fish catch" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. ❌ "High chlorophyll = high fish abundance" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
3. ❌ "SST alone predicts fish location" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
4. ❌ "PFZ is 100% accurate" [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
5. ❌ "Species X will definitely be present at PFZ" (without species-specific validation) [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)
6. ❌ "Ignore PFZ; traditional knowledge is always better" (disregarding scientific evidence) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 21.2 Safety Red Flags

7. ❌ "Safe to fish" or **"No risk"** [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
8. ❌ "Unsafe to fish; do not go to sea" (deterministic prohibition without official warning) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
9. ❌ "Wave height is exactly 2.5 m" (without uncertainty) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
10. ❌ "Cyclone will not affect your area" (without official forecast) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
11. ❌ "Tsunami warning is false alarm" (contradicting official warning) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

### 21.3 Oceanography Red Flags

12. ❌ "Subsurface temperature is 20°C at 50 m depth" (from surface SST only) [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
13. ❌ "Salinity is 35 PSU" (without SSS data) [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
14. ❌ "This eddy will persist for 2 weeks" (without model forecast validation) [science](https://www.science.gov/topicpages/o/ocean+color+parameters)
15. ❌ "Chlorophyll algorithm is 100% accurate in coastal waters" (ignoring algorithm uncertainty) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
16. ❌ "SST data is real-time" (when latency is 1–4 days) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)

### 21.4 Ecosystem Red Flags

17. ❌ "Marine heatwave will cause fishery collapse" (without peer-reviewed evidence for specific region/species) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
18. ❌ "Phytoplankton bloom means fish will aggregate here" (without multi-parameter validation) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
19. ❌ "Ecosystem anomaly detected; biodiversity will decrease" (without ecological validation) [marine.copernicus](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/chlorophyll-and-primary-production)
20. ❌ "Upwelling guarantees high productivity and fish catch" (without validation) [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)

### 21.5 General Red Flags

21. ❌ "Scientific probability: 85%" (without validated calibration methodology) [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
22. ❌ "This inference is based on Level 5 evidence" (presenting anecdotal evidence as scientific) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
23. ❌ "No uncertainty" (all measurements have uncertainty) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
24. ❌ "Data is perfect" (all data has quality flags, errors, gaps) [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)
25. ❌ "ORCA is always correct" (AI can hallucinate; must validate) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 22. Authoritative References

### 22.1 Primary Sources (Government/Intergovernmental)

1. **ISRO/MOSDAC** (Indian Space Research Organisation / Meteorological & Oceanographic Satellite Data Archival Centre)
   - Oceansat-2 OCM chlorophyll data [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
   - URL: https://www.mosdac.gov.in

2. **INCOIS** (Indian National Centre for Ocean Information Services)
   - PFZ advisories [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
   - Ocean State Forecast (OSF) [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)
   - High Wave Alert [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP43.pdf)
   - URL: https://incois.gov.in

3. **NASA** (National Aeronautics and Space Administration)
   - MODIS SST and chlorophyll [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
   - JPL Physical Oceanography DAAC (PO.DAAC) [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)
   - URL: https://earthdata.nasa.gov

4. **NOAA** (National Oceanic and Atmospheric Administration)
   - AVHRR SST [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
   - Marine Heatwave definitions and monitoring [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
   - URL: https://www.noaa.gov

5. **Copernicus Marine Service** (European Union)
   - Global ocean reanalysis (SST, chlorophyll, SSH, currents, SSS) [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
   - URL: https://marine.copernicus.eu

### 22.2 Peer-Reviewed Literature

6. **Hobday et al. 2016**: "A hierarchical approach to defining marine heatwaves" [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
   - DOI: 10.1038/nclimate2935 (or similar; verify exact DOI)
   - Definition: MHW = SST > 90th percentile for ≥5 days [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)

7. **Hobday et al. 2018**: "Longer and more frequent marine heatwaves over the past century" [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf)
   - DOI: 10.1038/s41467-018-03732-9 (verify)
   - MHW categories: moderate, strong, severe/extreme [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/59277/noaa_59277_DS1.pdf)

8. **INCOIS Technical Reports**:
   - "Integrated Potential Fishing Zone Forecasts" [services.incois.gov](https://services.incois.gov.in/documents/ResearchPapers/RP77.pdf)
   - "Methodology for PFZ generation" [io50.incois.gov](https://io50.incois.gov.in/documents/TechnicalReports/INCOIS-ASG-PFZ-TR-08-2007.pdf)
   - URL: https://incois.gov.in/documents/ResearchPapers/

9. **PFZ Validation Studies**:
   - "The Validation of Potential Fishing Zone Advisories" [ijarsct.co](https://ijarsct.co.in/Paper10524.pdf)
   - "Potential fishing zone (PFZ) advisories-Are they beneficial to the coastal fisherfolk?" [eprints.cmfri.org](https://eprints.cmfri.org.in/10269/1/Preetha_G_Nair_Biological_Forum.pdf)
   - "Mobile advisory information to reduce coastal risks and to enhance..." [niscpr.res](https://www.niscpr.res.in/jinfo/IJMS/IJMS-Forthcoming-Articles/BKP-IJMS-PR-Oct%202014/MS%202149%20Edited.pdf)

10. **Ocean Color Quality**:
    - "Copernicus GlobColour processor" [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)
    - "A Review and Assessment of Copernicus Water Quality..." [frontiersin](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2026.1913182/full)

### 22.3 Data Products

11. **SST Products**:
    - AVHRR Pathfinder L3 SST (NOAA) [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/AVHRR_PATHFINDER_L3_SST_MONTHLY_DAYTIME_V5)
    - MUR L4 SST (JPL) [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)
    - Copernicus SST L4 [documentation.marine.copernicus](https://documentation.marine.copernicus.eu/PUM/CMEMS-SST-PUM-010-007-032.pdf)

12. **Chlorophyll Products**:
    - Oceansat-2 OCM (ISRO/MOSDAC) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
    - MODIS Aqua (NASA) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
    - Copernicus GlobColour [os.copernicus](https://os.copernicus.org/articles/15/819/2019/os-15-819-2019.pdf)

13. **SSH/Altimetry**:
    - Copernicus SSH L4 [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
    - SWOT (NASA/CNES) [swot.jpl.nasa](https://swot.jpl.nasa.gov/system/documents/files/2244_2244_D-75724_SWOT_Cal_Val_Plan_Initial_20180129u.pdf)

14. **Ocean State Forecast**:
    - INCOIS OSF (wave height, wind, swell) [iioe-2.incois.gov](https://iioe-2.incois.gov.in/oceanservices/osfforecast.jsp)

15. **Marine Heatwave Products**:
    - NOAA PSL MHW monitoring and forecast [repository.library.noaa](https://repository.library.noaa.gov/view/noaa/63891)
    - URL: https://psl.noaa.gov/marine-heatwaves/

***

## 23. Document Maintenance

**Version**: 1.0  
**Date**: 31 August 2026  
**Maintained By**: ORCA Scientific Validation Team  
**Review Cycle**: Annual (or when authoritative sources update products)

**Change Log**:
- v1.0 (31 Aug 2026): Initial release based on ISRO, MOSDAC, INCOIS, NASA, NOAA, Copernicus, and peer-reviewed literature [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Contact**: For scientific queries, contact ORCA Scientific Validation Team with specific rule citations (e.g., "Section 4.1: Chlorophyll-a interpretation").

***

**END OF SCIENTIFIC_RULES.md**