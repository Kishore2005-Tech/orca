# DOMAIN_KNOWLEDGE.md

# ORCA — Marine Ecosystems Reasoning with Collaborative Agents

**Project:** SIH26176 – ORCA
**Organization:** ISRO
**Category:** Software
**Domain:** Marine Ecosystems + Earth Observation + AI + Agentic AI + Decision Intelligence

---

## 1. Purpose

This document defines the core marine-science knowledge required by developers, data engineers, AI agents, researchers, and domain experts working on ORCA.

ORCA integrates heterogeneous marine datasets—including satellite Earth Observation, oceanographic observations, meteorological information, fisheries information, bathymetry, and derived ecological indicators—to support evidence-grounded reasoning about marine environments.

The purpose of this document is **not** to provide simplistic rules such as:

> "High chlorophyll = more fish."

Instead, ORCA should reason through scientifically defensible relationships:

> Physical conditions → influence nutrient transport and habitat conditions → influence biological productivity → potentially affect prey availability → may contribute to habitat suitability for particular species.

Even these relationships are **context-dependent**. ORCA must distinguish between:

* **Observed measurements**
* **Derived scientific indicators**
* **Established scientific relationships**
* **Statistical relationships**
* **Operational heuristics**
* **Model predictions**
* **Assumptions**
* **Uncertainty**

---

# 2. Core Scientific Principle

Marine ecosystems are **dynamic, spatially heterogeneous, temporally variable, and nonlinear systems**.

No single parameter is sufficient to describe marine ecosystem conditions.

For example:

```text
SST
 │
 ├── influences thermal habitat
 │
 ├── interacts with stratification
 │
 └── can affect biological processes
          │
          ▼
      Phytoplankton
          │
          ▼
      Zooplankton
          │
          ▼
       Fish prey
          │
          ▼
   Fish distribution
```

This is a conceptual relationship, not a deterministic prediction.

ORCA should therefore avoid statements such as:

> "Chlorophyll is high, therefore fish are definitely present."

A scientifically safer interpretation is:

> "Elevated chlorophyll-a indicates increased phytoplankton biomass or concentration and may, depending on species, season, physical conditions, and ecosystem structure, be associated with areas of enhanced biological productivity."

---

# 3. Scientific Evidence Hierarchy

ORCA agents should prioritize evidence in approximately this order:

1. **Direct observations**
2. **Validated scientific products**
3. **Derived indicators**
4. **Validated predictive models**
5. **Published scientific relationships**
6. **Statistical correlations**
7. **Operational heuristics**
8. **Unverified assumptions**

Every generated recommendation should ideally identify which category it relies upon.

---

# A. PHYSICAL OCEANOGRAPHY

Physical oceanography describes the physical state and movement of seawater.

---

## A.1 Sea Surface Temperature — SST

### Definition

Sea Surface Temperature (SST) is the temperature of seawater near the ocean surface.

Satellite SST products generally represent the temperature of the skin or near-surface layer depending on the sensor and retrieval methodology.

### Unit

* °C
* Sometimes Kelvin (K)

Conversion:

```text
K = °C + 273.15
```

### Typical Interpretation

SST provides information about:

* thermal structure of the surface ocean
* water masses
* temperature gradients
* fronts
* seasonal variability
* marine heat conditions
* potential habitat conditions for temperature-sensitive organisms

Large spatial SST gradients can indicate ocean fronts.

### Why ORCA Needs It

SST is important for:

* fish habitat analysis
* Potential Fishing Zone (PFZ) reasoning
* marine heat-wave detection
* ocean-front detection
* understanding seasonal ocean conditions
* interpreting biological observations
* assessing environmental conditions around a fishing location

### Potential Data Sources

* ISRO / MOSDAC satellite products
* Oceansat-derived products where applicable
* INCOIS
* Copernicus Marine Service
* NOAA
* NASA ocean-observation products
* in-situ buoy and ship observations

### Limitations

* Cloud cover can obscure infrared SST measurements.
* Different sensors may measure slightly different physical layers.
* Satellite retrievals may have uncertainty.
* SST does not represent the entire water column.
* Surface temperature can differ substantially from subsurface temperature.
* Resolution varies between datasets.

### Common Misconception

**Misconception:** SST represents the temperature of the entire ocean.

**Reality:** SST primarily describes near-surface conditions.

### Scientific Relationship vs Heuristic

**Scientific relationship:**

SST is an important descriptor of thermal habitat and water-mass structure.

**Heuristic:**

A particular SST range is suitable for a particular fish species.

The second statement requires species-specific ecological evidence and should not be universally assumed.

---

# A.2 Sea Surface Salinity — SSS

### Definition

Sea Surface Salinity (SSS) describes the concentration of dissolved salts in seawater near the ocean surface.

### Unit

Commonly:

* PSU (Practical Salinity Units)
* Often represented as a dimensionless practical salinity value

Modern salinity products may use different conventions depending on the product.

### Typical Interpretation

SSS helps identify:

* freshwater influence
* river discharge
* evaporation and precipitation effects
* water masses
* ocean circulation patterns
* mixing
* salinity fronts

### Why ORCA Needs It

SSS can help ORCA:

* characterize water masses
* identify salinity gradients
* interpret coastal environmental conditions
* combine with SST to identify water-mass boundaries
* improve habitat and ecosystem interpretation

### Potential Data Sources

* SMAP satellite salinity products
* SMOS
* Copernicus Marine Service
* Argo floats
* oceanographic buoys
* research cruises

### Limitations

* Satellite salinity resolution can be relatively coarse.
* Coastal retrievals may be difficult.
* Rainfall and freshwater discharge can create rapidly changing surface conditions.
* SSS only describes the surface layer.

### Common Misconception

**Misconception:** Higher salinity always means healthier or more productive ocean water.

**Reality:** Salinity is a physical property. Its ecological significance depends on organisms, location, depth, and other environmental conditions.

### Scientific Relationship vs Heuristic

**Scientific relationship:**

Salinity differences contribute to density differences and therefore can influence ocean stratification and circulation.

**Heuristic:**

"High salinity means good fishing."

This is unsupported without additional ecological evidence.

---

# A.3 Sea Surface Height — SSH

### Definition

Sea Surface Height (SSH) describes the height of the ocean surface relative to a reference level, generally derived from satellite altimetry and ocean models.

### Unit

* metres (m)
* centimetres (cm)

### Typical Interpretation

SSH anomalies can indicate:

* large-scale circulation
* oceanic structures
* geostrophic current patterns
* eddies
* sea-level variability

### Why ORCA Needs It

SSH is particularly useful for:

* identifying mesoscale eddies
* estimating geostrophic currents
* understanding ocean circulation
* combining physical circulation with biological indicators
* detecting dynamically important ocean features

### Potential Data Sources

* Copernicus Marine Service
* satellite altimetry missions
* ISRO ocean products where available
* NOAA
* CMEMS-derived ocean circulation products

### Limitations

* SSH is not a direct measurement of ocean current.
* Coastal areas can be challenging for altimetry.
* Spatial resolution is limited compared with some satellite imagery.
* Interpretation often requires anomaly fields or derived gradients.

### Common Misconception

**Misconception:** High SSH directly means high fish abundance.

**Reality:** SSH is a physical oceanographic variable. Any ecological relationship is indirect and context-dependent.

### Scientific Relationship vs Heuristic

**Scientific relationship:**

SSH gradients can be used to estimate geostrophic current structure.

**Heuristic:**

A specific SSH anomaly automatically identifies a PFZ.

That requires empirical validation.

---

# A.4 Ocean Currents

### Definition

Ocean currents are organized movements of seawater.

They can occur because of:

* wind forcing
* pressure gradients
* density differences
* Earth's rotation
* tides
* topography
* interactions between ocean and atmosphere

### Unit

* m/s
* knots in marine operations

### Typical Interpretation

Currents describe:

* direction of water movement
* transport
* circulation
* water-mass movement
* dispersal of organisms and nutrients

### Why ORCA Needs It

Currents help ORCA understand:

* movement of water masses
* transport of biological material
* potential dispersal pathways
* relationship between physical and biological observations
* operational marine conditions

### Potential Data Sources

* Copernicus Marine Service
* HYCOM
* NOAA
* INCOIS
* satellite-derived geostrophic currents
* drifters
* ADCP observations
* ocean models

### Limitations

* Surface currents may differ from currents at depth.
* Model currents are estimates, not necessarily observations.
* Coastal currents can be highly complex.
* Wind-driven surface currents can vary rapidly.

### Common Misconception

**Misconception:** Current direction at the surface describes the entire water column.

**Reality:** Current velocity and direction vary with depth.

---

# A.5 Wind

### Definition

Wind is the movement of air relative to the Earth's surface.

For marine applications, wind speed and direction are important atmospheric forcing variables.

### Unit

Wind speed:

* m/s
* knots
* km/h

Wind direction:

* degrees
* compass direction

### Typical Interpretation

Wind affects:

* wave generation
* surface ocean circulation
* evaporation
* mixing
* coastal upwelling
* marine operational conditions

### Why ORCA Needs It

Wind information supports:

* marine safety
* wave forecasting
* upwelling interpretation
* cyclone detection
* fishing-condition assessment
* surface circulation reasoning

### Potential Data Sources

* IMD
* ISRO satellite products
* scatterometer missions
* ECMWF
* Copernicus
* NOAA

### Limitations

* Wind can change rapidly.
* Forecast uncertainty increases with forecast horizon.
* Satellite observations are snapshots rather than continuous measurements.
* Local coastal effects may not be captured by coarse models.

### Common Misconception

**Misconception:** Strong wind always means strong ocean current.

**Reality:** Wind can drive surface circulation, but current response depends on duration, direction, stratification, coastline, Coriolis effects, and other factors.

---

# A.6 Wave Height

### Definition

Wave height describes the vertical distance between wave crest and trough.

Operational wave products commonly report significant wave height (Hs), representing the average height of the highest one-third of waves in a wave field.

### Unit

* metres (m)

### Typical Interpretation

Higher wave height generally indicates rougher sea conditions.

### Why ORCA Needs It

Wave height is important for:

* marine safety
* fishing operation planning
* vessel risk assessment
* cyclone impact assessment
* coastal hazard analysis

### Potential Data Sources

* INCOIS
* Copernicus Marine Service
* NOAA
* ECMWF
* satellite altimetry
* buoy observations

### Limitations

* Significant wave height does not describe every individual wave.
* Wave period and direction also matter.
* Local vessel response depends on vessel characteristics.
* Forecasts contain uncertainty.

### Common Misconception

**Misconception:** A wave-height value alone completely determines whether a vessel can safely operate.

**Reality:** Safety depends on vessel characteristics, wave height, period, direction, wind, currents, weather, operator capability, and official advisories.

---

# A.7 Mixed Layer Depth — MLD

### Definition

Mixed Layer Depth (MLD) is an estimate of the depth over which ocean properties such as temperature, salinity, or density are relatively uniform because of mixing.

Different scientific products use different definitions and thresholds.

### Unit

* metres (m)

### Typical Interpretation

Deep mixed layers can indicate stronger vertical mixing.

Shallow mixed layers can indicate stronger near-surface stratification.

### Why ORCA Needs It

MLD can help interpret:

* nutrient availability
* vertical mixing
* stratification
* phytoplankton conditions
* seasonal ocean dynamics

### Potential Data Sources

* Argo floats
* Copernicus Marine Service
* ocean models
* research cruises
* reanalysis products

### Limitations

* MLD depends on the definition used.
* Different algorithms can produce different depths.
* It is difficult to directly observe everywhere.
* Model-derived MLD is subject to model uncertainty.

### Common Misconception

**Misconception:** Deep MLD always means high biological productivity.

**Reality:** Deep mixing can transport nutrients upward, but biological productivity also depends on light, nutrient composition, temperature, grazing, and other factors.

---

# A.8 Bathymetry

### Definition

Bathymetry describes the depth and shape of the seafloor.

### Unit

* metres (m)

Depth may be represented relative to sea level or another vertical reference.

### Typical Interpretation

Bathymetry reveals:

* continental shelves
* slopes
* trenches
* seamounts
* underwater ridges
* channels
* coastal depth structure

### Why ORCA Needs It

Bathymetry can support:

* habitat analysis
* fishing-ground characterization
* species habitat modeling
* coastal hazard analysis
* spatial masking
* interpretation of currents and oceanographic features

### Potential Data Sources

* GEBCO
* NOAA bathymetric datasets
* EMODnet where applicable
* national hydrographic datasets
* multibeam surveys
* satellite-derived bathymetry in suitable shallow-water conditions

### Limitations

* Global bathymetry can have relatively coarse resolution.
* Coastal areas may have data gaps.
* Vertical accuracy varies.
* Some datasets combine direct measurements with interpolation.

### Common Misconception

**Misconception:** Bathymetry is only useful for navigation.

**Reality:** Seafloor structure can influence circulation, sediment transport, habitat distribution, and fisheries ecology.

---

# A.9 Upwelling

### Definition

Upwelling is the upward movement of deeper water toward the surface.

Upwelled water can contain nutrients that were regenerated or accumulated at depth.

### Unit

Upwelling itself may be represented using:

* vertical velocity (m/s)
* transport
* temperature anomalies
* nutrient observations
* indirect indices

### Typical Interpretation

Upwelling can produce:

* cooler surface waters
* nutrient enrichment
* enhanced phytoplankton productivity under suitable light conditions

### Why ORCA Needs It

Upwelling is relevant to:

* fisheries
* productivity analysis
* chlorophyll interpretation
* ecosystem dynamics
* PFZ analysis

### Potential Data Sources

* SST satellite products
* wind/scatterometer data
* ocean models
* chlorophyll-a products
* oceanographic observations

### Limitations

Upwelling cannot be reliably identified from one parameter in every situation.

For example:

```text
Cool SST
+
favourable wind
+
coastal geometry
+
appropriate circulation
```

provides stronger evidence than SST alone.

### Common Misconception

**Misconception:** Every cold SST patch represents upwelling.

**Reality:** Cold water can result from several processes.

---

# A.10 Ocean Fronts

### Definition

An ocean front is a region with a strong horizontal gradient in properties such as:

* temperature
* salinity
* density
* chlorophyll concentration

### Unit

Front intensity may be represented as a gradient:

* °C/km
* PSU/km
* density gradient
* chlorophyll gradient

### Typical Interpretation

Fronts can represent boundaries between different water masses and regions of strong physical gradients.

Some fronts can be associated with enhanced biological activity or aggregation of organisms, but this is not universal.

### Why ORCA Needs It

Front detection can support:

* ecosystem analysis
* habitat suitability modeling
* PFZ analysis
* identifying water-mass boundaries

### Potential Data Sources

* SST
* SSS
* SSH
* chlorophyll-a
* ocean models

### Limitations

* Detection depends strongly on spatial resolution.
* A detected gradient does not necessarily represent a biologically productive front.
* Cloud contamination can affect optical and infrared products.

### Common Misconception

**Misconception:** Every ocean front is a fishing zone.

**Reality:** A front is a physical or biogeochemical boundary; fisheries relevance is species- and context-dependent.

---

# A.11 Eddies

### Definition

An eddy is a rotating mesoscale ocean feature that can transport and redistribute heat, nutrients, organisms, and other properties.

Eddies may be broadly categorized as:

* cyclonic
* anticyclonic

### Unit

Common descriptors include:

* radius: km
* rotational velocity: m/s
* SSH anomaly: m
* vorticity: s⁻¹

### Typical Interpretation

Eddies can influence:

* vertical transport
* nutrient distribution
* biological productivity
* water-mass movement
* marine habitat structure

The direction and magnitude of these effects depend on the type and physical environment of the eddy.

### Why ORCA Needs It

Eddies can improve:

* ocean-feature detection
* habitat analysis
* biological interpretation
* current analysis
* multi-variable reasoning

### Potential Data Sources

* satellite altimetry
* SSH products
* Copernicus Marine Service
* ocean circulation models
* satellite SST/chlorophyll

### Limitations

* Eddy detection algorithms can disagree.
* Small eddies may not be resolved.
* SSH-derived eddies describe surface/upper-ocean dynamics rather than the complete 3D structure.

### Common Misconception

**Misconception:** Cyclonic eddy always means high fish abundance.

**Reality:** Cyclonic and anticyclonic eddies can have different physical and biological effects, but fish abundance cannot be inferred deterministically from eddy polarity alone.

---

# B. MARINE BIOLOGY

---

# B.1 Chlorophyll-a

### Definition

Chlorophyll-a is a photosynthetic pigment found in phytoplankton and other photosynthetic organisms.

Ocean-colour satellites use optical measurements to estimate chlorophyll-a concentration.

### Unit

Commonly:

* mg/m³

### Typical Interpretation

Satellite chlorophyll-a is commonly used as a proxy for phytoplankton biomass or concentration.

Higher values often indicate greater phytoplankton concentration, but interpretation depends on water type and algorithm performance.

### Why ORCA Needs It

Chlorophyll-a is central to:

* primary productivity analysis
* ecosystem monitoring
* PFZ reasoning
* bloom detection
* habitat analysis

### Potential Data Sources

* ISRO ocean-colour missions
* Oceansat
* Copernicus Marine Service
* NASA Ocean Color
* NOAA

### Limitations

* It is an indirect measurement.
* Coastal waters are optically complex.
* Atmospheric correction can introduce uncertainty.
* High chlorophyll does not necessarily mean high fish abundance.
* Cloud cover can create missing observations.

### Common Misconception

**Misconception:** Chlorophyll-a measures fish population.

**Reality:** It is primarily an indicator associated with phytoplankton biomass.

### Scientific Relationship vs Heuristic

**Scientific relationship:**

Phytoplankton use chlorophyll-a in photosynthesis.

**Heuristic:**

High chlorophyll = immediate high fish catch.

This is an oversimplification.

---

# B.2 Phytoplankton

### Definition

Phytoplankton are microscopic organisms capable of photosynthesis that live in aquatic environments.

They form a major component of marine primary producers.

### Unit

Phytoplankton abundance may be measured as:

* cells/L
* biomass
* carbon concentration
* chlorophyll-a concentration

### Typical Interpretation

Phytoplankton form the base of many marine food webs.

### Why ORCA Needs It

Phytoplankton information supports:

* productivity analysis
* ecosystem modeling
* food-web reasoning
* bloom detection
* fisheries habitat interpretation

### Potential Data Sources

* ocean-colour satellites
* microscopy observations
* flow cytometry
* research cruises
* biogeochemical models

### Limitations

Satellite imagery generally cannot identify all phytoplankton species directly.

### Common Misconception

**Misconception:** All phytoplankton are beneficial.

**Reality:** Some phytoplankton can form harmful algal blooms or produce toxins.

---

# B.3 Zooplankton

### Definition

Zooplankton are drifting aquatic organisms that consume phytoplankton, other plankton, or organic material.

They include organisms ranging from microscopic forms to larger gelatinous organisms.

### Unit

Possible measurements include:

* individuals/m³
* biomass
* carbon concentration

### Typical Interpretation

Zooplankton represent an important trophic link between primary producers and higher trophic levels.

### Why ORCA Needs It

Zooplankton can help explain:

```text
Phytoplankton
      ↓
Zooplankton
      ↓
Small pelagic organisms
      ↓
Larger fish
```

This is a simplified food-web representation.

### Potential Data Sources

* plankton surveys
* research cruises
* oceanographic institutions
* ecological models

### Limitations

Zooplankton distributions are highly variable and difficult to infer from satellite data alone.

### Common Misconception

**Misconception:** More phytoplankton always means more zooplankton immediately.

**Reality:** Biological responses involve time lags, grazing, species composition, temperature, and other factors.

---

# B.4 Primary Productivity

### Definition

Primary productivity is the rate at which primary producers convert inorganic carbon into organic matter, primarily through photosynthesis.

### Unit

Commonly:

* mg C/m²/day
* g C/m²/day

### Typical Interpretation

Higher productivity indicates greater rates of organic carbon production under the specified measurement/model definition.

### Why ORCA Needs It

It helps ORCA understand:

* ecosystem productivity
* carbon cycling
* potential food-web support
* seasonal biological dynamics

### Potential Data Sources

* satellite ocean-colour products
* biogeochemical models
* oceanographic observations

### Limitations

Satellite-derived productivity is usually model-based and depends on:

* chlorophyll
* light
* temperature
* photosynthetic parameters
* algorithm assumptions

### Common Misconception

**Misconception:** Primary productivity directly measures fish production.

**Reality:** Fish production depends on food-web transfer efficiency and many ecological processes.

---

# B.5 Fish Habitat

### Definition

Fish habitat refers to the environmental conditions and physical/biological features that support the presence, survival, growth, reproduction, or movement of a particular fish species or assemblage.

### Unit

There is no single unit.

Habitat models may output:

* probability
* suitability score
* classification
* density
* presence/absence

### Typical Interpretation

A habitat-suitability map estimates where environmental conditions are more or less consistent with a species' observed ecological preferences.

### Why ORCA Needs It

Habitat modeling supports:

* PFZ reasoning
* fishing planning
* ecological monitoring
* species distribution analysis
* decision support

### Potential Data Sources

* fisheries surveys
* catch data
* tagging data
* environmental observations
* satellite products
* oceanographic models

### Limitations

Habitat suitability is species-specific.

A model trained for one species should not automatically be applied to another.

### Common Misconception

**Misconception:** Suitable habitat guarantees fish presence.

**Reality:** Habitat suitability indicates environmental compatibility, not certainty of fish presence or catch.

---

# B.6 Trophic Levels

### Definition

A trophic level describes an organism's position within a food chain.

Simplified structure:

```text
Level 1 → Primary producers
Level 2 → Primary consumers
Level 3 → Secondary consumers
Level 4+ → Higher predators
```

Real marine food webs are more complex.

### Unit

Trophic level is dimensionless.

### Typical Interpretation

Higher trophic levels generally depend indirectly on energy captured by lower trophic levels.

### Why ORCA Needs It

Trophic-level reasoning helps connect:

* primary productivity
* plankton
* prey availability
* fish communities
* predators

### Potential Data Sources

* ecological literature
* stomach-content studies
* stable-isotope studies
* fisheries research
* ecosystem models

### Limitations

Many marine organisms occupy multiple trophic positions.

### Common Misconception

**Misconception:** Every species has one fixed trophic level.

**Reality:** Trophic position can vary with life stage, diet, location, season, and ecosystem.

---

# B.7 Food Webs

### Definition

A food web represents feeding relationships among organisms in an ecosystem.

Unlike a simple food chain, a food web contains multiple interconnected feeding pathways.

### Unit

No physical unit.

Network analysis may use:

* nodes
* edges
* interaction strengths

### Typical Interpretation

Marine ecosystems contain interconnected relationships between:

* phytoplankton
* zooplankton
* fish
* seabirds
* marine mammals
* decomposers
* detrital pathways

### Why ORCA Needs It

Food-web reasoning prevents oversimplified statements about ecosystem productivity.

### Potential Data Sources

* ecological surveys
* scientific literature
* ecosystem models
* trophic databases

### Limitations

Food webs are incomplete representations of highly complex ecosystems.

### Common Misconception

**Misconception:** Food webs are static.

**Reality:** Feeding relationships can change with season, location, life stage, and environmental conditions.

---

# C. FISHERIES

---

# C.1 Potential Fishing Zone — PFZ

### Definition

A Potential Fishing Zone (PFZ) is an area identified as potentially favorable for fishing based on environmental and oceanographic indicators.

PFZ advisories commonly use combinations of remotely sensed and oceanographic features.

### Unit

PFZ itself is spatial rather than a physical unit.

A PFZ may be represented as:

* point coordinates
* polygons
* lines
* raster suitability maps

### Typical Interpretation

A PFZ indicates an area with environmental characteristics associated with potentially favorable fishing conditions.

It does **not** guarantee fish presence or catch.

### Why ORCA Needs It

PFZ is one of ORCA's important decision-support applications.

Example:

```text
SST
+
Chlorophyll-a
+
Ocean fronts
+
Currents
+
Bathymetry
+
Historical fisheries evidence
        ↓
Habitat / PFZ reasoning
        ↓
Potential fishing area
```

### Potential Data Sources

* INCOIS
* ISRO / MOSDAC
* Oceansat
* fisheries agencies
* oceanographic observations
* historical catch datasets

### Limitations

PFZ predictions depend on:

* species
* season
* environmental conditions
* model/algorithm
* data quality
* fishing effort
* vessel capability
* observation gaps

### Common Misconception

**Misconception:** PFZ means "fish are definitely there."

**Reality:** PFZ means conditions are potentially favorable according to a defined methodology.

### Critical ORCA Rule

ORCA must never transform:

> "Potential Fishing Zone"

into:

> "Guaranteed Fish Zone."

---

# C.2 Habitat Suitability

### Definition

Habitat suitability represents how compatible environmental conditions are with the known ecological requirements or observed distribution of a species.

### Unit

Usually:

* 0–1 probability/suitability
* 0–100 score
* categorical classes

The exact meaning depends on the model.

### Typical Interpretation

Higher suitability means the environmental conditions resemble those associated with the target species or fishery dataset.

### Why ORCA Needs It

It can support:

* species-specific fishing decisions
* ecological forecasting
* spatial planning
* conservation
* PFZ refinement

### Potential Data Sources

* catch datasets
* fish survey datasets
* environmental variables
* species distribution models
* tagging data

### Limitations

A suitability model can suffer from:

* sampling bias
* spatial bias
* missing environmental variables
* model overfitting
* extrapolation beyond training data

### Common Misconception

**Misconception:** Suitability = abundance.

**Reality:** Suitability describes environmental compatibility, not necessarily population density.

---

# C.3 Fishing Effort

### Definition

Fishing effort measures the amount of fishing activity applied over a given area and time.

Examples:

* vessel-hours
* fishing days
* number of trips
* distance traveled while fishing

### Unit

Depends on definition:

* hours
* vessel-days
* trips
* km
* gear-specific effort units

### Typical Interpretation

Fishing effort indicates how intensely an area is being fished.

### Why ORCA Needs It

Effort data helps distinguish:

```text
Low catch + low effort
```

from:

```text
Low catch + high effort
```

These situations can have very different interpretations.

### Potential Data Sources

* vessel tracking systems
* VMS
* AIS where applicable
* fisheries logbooks
* observer programs
* fisheries surveys

### Limitations

AIS does not necessarily represent all fishing vessels or fishing activity.

Fishing behavior may be missing or misclassified.

### Common Misconception

**Misconception:** More vessel activity means more fish.

**Reality:** More fishing activity can also mean greater fishing pressure or concentration of fishing effort.

---

# C.4 Catch Data

### Definition

Catch data records the amount and characteristics of fish captured by fishing operations.

### Unit

Commonly:

* kg
* tonnes
* number of individuals

It may also contain:

* species
* location
* date
* gear type
* vessel
* effort

### Typical Interpretation

Catch data provides observations of fishing outcomes, but catch is influenced by both fish availability and fishing effort.

### Why ORCA Needs It

Catch data can be used to:

* train habitat models
* validate PFZ predictions
* identify historical fishing patterns
* evaluate model performance

### Potential Data Sources

* fisheries departments
* research institutions
* logbooks
* landing centers
* observer programs
* vessel monitoring systems

### Limitations

Catch data can contain:

* reporting errors
* sampling bias
* missing locations
* effort bias
* species misidentification

### Common Misconception

**Misconception:** Catch location directly represents fish distribution.

**Reality:** Catch is the result of fish availability **and** fishing behavior, gear, effort, vessel capability, regulations, and environmental conditions.

---

# D. MARINE HAZARDS

---

# D.1 Marine Heat Waves — MHW

### Definition

A Marine Heat Wave (MHW) is a prolonged period of unusually warm ocean temperatures relative to a defined historical baseline.

A commonly used framework identifies events when temperatures exceed a seasonally varying threshold for a specified minimum duration.

### Unit

* °C anomaly
* duration: days

### Typical Interpretation

MHWs represent anomalously warm ocean conditions.

They can affect:

* species distributions
* coral ecosystems
* productivity
* fisheries
* ecosystem structure

### Why ORCA Needs It

ORCA can use MHW detection for:

* ecosystem monitoring
* anomaly detection
* fisheries interpretation
* climate-related marine analysis

### Potential Data Sources

* satellite SST
* NOAA
* Copernicus Marine Service
* climate reanalysis products

### Limitations

Definition depends on:

* baseline period
* percentile threshold
* temporal resolution
* spatial resolution

### Common Misconception

**Misconception:** Any warm day is a marine heat wave.

**Reality:** MHWs are defined relative to climatology and duration criteria.

---

# D.2 Cyclones

### Definition

A tropical cyclone is a rotating low-pressure weather system that develops over sufficiently warm tropical or subtropical waters under suitable atmospheric conditions.

### Unit

Important parameters include:

* wind speed: m/s or knots
* central pressure: hPa
* radius: km
* track coordinates

### Typical Interpretation

Cyclones can produce:

* extreme winds
* high waves
* heavy rainfall
* storm surge
* coastal flooding
* ocean mixing

### Why ORCA Needs It

Cyclone information is critical for:

* marine safety
* fishing advisories
* vessel routing
* hazard alerts
* post-event ecosystem analysis

### Potential Data Sources

* IMD
* JTWC
* NOAA
* ECMWF
* satellite observations

### Limitations

Forecast tracks and intensity contain uncertainty.

### Common Misconception

**Misconception:** A cyclone track gives an exact future path.

**Reality:** Forecast tracks are probabilistic and uncertain.

---

# D.3 High Waves

### Definition

High waves describe wave conditions that exceed a relevant operational or climatological threshold.

### Unit

* significant wave height: metres
* wave period: seconds

### Typical Interpretation

High waves can indicate hazardous marine conditions.

### Why ORCA Needs It

Important for:

* fishing safety
* vessel operations
* cyclone response
* marine warnings

### Potential Data Sources

* INCOIS
* Copernicus Marine Service
* NOAA
* ECMWF
* wave buoys
* satellite altimetry

### Limitations

Risk depends on:

* wave height
* period
* direction
* wind
* vessel type
* vessel size
* local bathymetry

### Common Misconception

**Misconception:** One wave-height threshold is safe for every vessel.

**Reality:** Operational safety thresholds are vessel- and context-dependent.

---

# D.4 Strong Winds

### Definition

Strong winds are winds exceeding a defined operational or climatological threshold.

### Unit

* m/s
* knots
* km/h

### Typical Interpretation

Strong winds can increase:

* wave generation
* vessel instability
* spray
* operational difficulty

### Why ORCA Needs It

Strong wind information is important for marine safety and hazard reasoning.

### Potential Data Sources

* IMD
* scatterometers
* ECMWF
* NOAA
* satellite observations

### Limitations

Thresholds must be explicitly defined.

### Common Misconception

**Misconception:** "Strong wind" has one universal numerical definition.

**Reality:** Thresholds depend on application and warning system.

---

# D.5 Harmful Algal Blooms — HABs

### Definition

A Harmful Algal Bloom is an unusually high concentration of certain algae or phytoplankton that can produce ecological or toxic effects.

Not all algal blooms are harmful.

### Unit

Depending on the monitoring method:

* cells/L
* chlorophyll-a
* toxin concentration

### Typical Interpretation

HABs can cause:

* oxygen depletion in some circumstances
* toxin production
* fish mortality
* shellfish contamination
* ecosystem disruption

### Why ORCA Needs It

ORCA can support:

* bloom monitoring
* anomaly detection
* marine ecosystem alerts
* fisheries risk assessment

### Potential Data Sources

* ocean-colour satellites
* in-situ sampling
* microscopy
* toxin measurements
* fisheries/oceanographic agencies

### Limitations

Satellite chlorophyll alone generally cannot reliably determine:

* species
* toxicity
* exact biological cause

### Common Misconception

**Misconception:** High chlorophyll automatically means harmful algal bloom.

**Reality:** High chlorophyll may represent a productive but non-harmful phytoplankton population.

---

# E. GEOSPATIAL CONCEPTS

---

# E.1 Latitude and Longitude

### Definition

Latitude and longitude provide geographic coordinates.

Latitude measures angular position north or south of the Equator.

Longitude measures angular position east or west of the Prime Meridian.

### Unit

* degrees (°)
* decimal degrees
* degrees/minutes/seconds

### Typical Interpretation

Example:

```text
13.05° N, 80.27° E
```

represents a geographic position.

### Why ORCA Needs It

All spatial observations must be associated with geographic coordinates to:

* locate ocean conditions
* query nearby datasets
* intersect spatial layers
* generate maps
* provide location-specific recommendations

### Potential Data Sources

Almost every marine geospatial dataset.

### Limitations

Coordinate reference systems and datums must be handled correctly.

### Common Misconception

**Misconception:** Latitude/longitude always use the same distance scale.

**Reality:** One degree of longitude represents different physical distances depending on latitude.

---

# E.2 Raster

### Definition

A raster represents geographic information as a grid of cells/pixels.

Example:

```text
+----+----+----+
| 25 | 26 | 27 |
+----+----+----+
| 24 | 25 | 26 |
+----+----+----+
| 23 | 24 | 25 |
+----+----+----+
```

Each cell contains a value.

### Unit

Depends on the variable.

Examples:

* SST: °C
* chlorophyll: mg/m³
* bathymetry: m

### Typical Interpretation

Each pixel represents an area on Earth's surface.

### Why ORCA Needs It

Satellite and model products are commonly raster data.

ORCA needs raster processing for:

* spatial queries
* feature extraction
* anomaly detection
* map generation
* habitat modeling

### Potential Data Sources

* satellite products
* ocean models
* digital elevation/bathymetry datasets

### Limitations

Raster resolution determines how much spatial detail can be represented.

---

# E.3 Vector

### Definition

Vector data represents geographic features using:

* points
* lines
* polygons

### Unit

Depends on the geometry and attribute.

Examples:

* vessel position → point
* cyclone track → line
* EEZ → polygon
* PFZ → polygon/line/point

### Why ORCA Needs It

Vector data is useful for:

* administrative boundaries
* EEZs
* vessel tracks
* cyclone tracks
* fishing zones
* sampling locations

### Potential Data Sources

* government GIS datasets
* maritime boundaries
* fisheries agencies
* vessel tracking systems

### Limitations

Vector data may contain:

* topology errors
* invalid geometries
* coordinate-system mismatches
* outdated boundaries

---

# E.4 Spatial Resolution

### Definition

Spatial resolution describes the geographic size represented by a pixel or observation.

Example:

```text
1 km resolution
```

means each raster cell represents approximately a 1 km × 1 km area, subject to the dataset's exact grid definition.

### Unit

* metres
* kilometres
* arc-seconds
* degrees

### Typical Interpretation

Higher spatial resolution generally means smaller grid cells and potentially more spatial detail.

### Why ORCA Needs It

Datasets may have very different resolutions.

Example:

```text
SST → 1 km
Ocean model → several km
Bathymetry → hundreds of metres
Vessel position → point observation
```

ORCA must account for these differences before combining datasets.

### Limitations

Higher resolution does not automatically mean higher accuracy.

### Common Misconception

**Misconception:** Smaller pixels always mean better scientific information.

**Reality:** Resolution and accuracy are different properties.

---

# E.5 Temporal Resolution

### Definition

Temporal resolution describes how frequently observations are available.

Examples:

* hourly
* daily
* weekly
* monthly

### Unit

* seconds
* hours
* days
* months

### Typical Interpretation

Higher temporal resolution provides more frequent observations.

### Why ORCA Needs It

Marine systems change rapidly.

A cyclone forecast updated hourly and a monthly climatology should not be treated as equivalent evidence.

### Limitations

High-frequency data may still have:

* missing observations
* sensor errors
* forecast uncertainty

### Common Misconception

**Misconception:** The most recent dataset is always the most accurate.

**Reality:** Recency and accuracy are separate properties.

---

# E.6 Exclusive Economic Zone — EEZ

### Definition

An Exclusive Economic Zone (EEZ) is a maritime zone defined under international law in which a coastal state has specific sovereign rights regarding natural-resource exploration, exploitation, conservation, and management.

It generally extends up to 200 nautical miles from the territorial sea baseline, subject to relevant maritime boundaries and international law.

### Unit

* nautical miles
* km² for area

### Why ORCA Needs It

EEZ boundaries help ORCA:

* constrain spatial analysis
* identify jurisdiction
* contextualize fisheries information
* avoid inappropriate cross-border recommendations

### Potential Data Sources

* official maritime boundary datasets
* Marine Regions
* national government sources
* authoritative GIS repositories

### Limitations

Maritime boundaries can involve:

* neighboring-state agreements
* disputed areas
* complex baselines
* legal updates

### Common Misconception

**Misconception:** Every ocean point 200 nautical miles from a coast automatically belongs to that country's EEZ.

**Reality:** EEZ delimitation can be affected by neighboring states, geography, treaties, and international law.

---

# E.7 Spatial Interpolation

### Definition

Spatial interpolation estimates values at locations where observations are unavailable using surrounding observations.

Methods include:

* nearest neighbor
* inverse distance weighting (IDW)
* kriging
* spline interpolation

### Unit

Same as the interpolated variable.

### Typical Interpretation

Interpolation creates an estimated continuous surface from discrete observations.

### Why ORCA Needs It

Marine observations are often sparse.

Interpolation can help:

* fill spatial gaps
* create analysis grids
* integrate observations

### Limitations

Interpolation can introduce artificial patterns.

The result depends on:

* sampling density
* method
* spatial correlation
* boundaries
* assumptions

### Common Misconception

**Misconception:** Interpolated values are measurements.

**Reality:** Interpolated values are estimates.

---

# F. AI CONCEPTS

---

# F.1 Retrieval-Augmented Generation — RAG

### Definition

Retrieval-Augmented Generation (RAG) is an AI architecture in which a language model retrieves relevant external information before generating an answer.

### Unit

Not applicable.

### Typical Interpretation

For ORCA:

```text
User Question
      ↓
Intent Detection
      ↓
Retrieve relevant data/evidence
      ↓
Scientific reasoning
      ↓
LLM generation
      ↓
Evidence-grounded response
```

### Why ORCA Needs It

RAG helps prevent an LLM from relying only on internal knowledge when answering questions about:

* datasets
* scientific definitions
* advisories
* historical observations
* methodology
* metadata

### Potential Data Sources

* scientific documents
* dataset metadata
* research papers
* official advisories
* oceanographic reports
* internal knowledge bases

### Limitations

RAG does not automatically guarantee correctness.

Problems include:

* poor retrieval
* stale documents
* incorrect chunking
* conflicting sources
* insufficient evidence

### Common Misconception

**Misconception:** RAG eliminates hallucinations.

**Reality:** RAG can reduce unsupported generation but does not guarantee factual correctness.

---

# F.2 Multi-Agent Systems

### Definition

A multi-agent system consists of multiple specialized AI agents that cooperate to perform a task.

ORCA may use agents such as:

```text
                    ORCA
                     │
          ┌──────────┼──────────┐
          │          │          │
     Ocean Agent  Biology    Fisheries
          │          │          │
          └──────────┼──────────┘
                     │
                Hazard Agent
                     │
                GIS Agent
                     │
              Reasoning Agent
                     │
             Decision Agent
```

### Typical Interpretation

Each agent can specialize in a domain or task.

### Why ORCA Needs It

Marine ecosystem reasoning is multidisciplinary.

Agents can specialize in:

* physical oceanography
* marine biology
* fisheries
* hazards
* geospatial processing
* evidence retrieval
* uncertainty analysis

### Limitations

Multi-agent systems introduce:

* coordination errors
* inconsistent outputs
* duplicated reasoning
* latency
* higher computational cost

### Common Misconception

**Misconception:** More agents automatically produce better answers.

**Reality:** Agent specialization only helps when tasks are appropriately decomposed and outputs are coordinated.

---

# F.3 Evidence Grounding

### Definition

Evidence grounding means connecting an AI-generated claim to observable data, authoritative sources, calculations, or other verifiable evidence.

### Unit

Not applicable.

### Typical Interpretation

A grounded answer should be traceable.

Example:

```text
Claim
 ↓
Dataset
 ↓
Timestamp
 ↓
Spatial region
 ↓
Measurement
 ↓
Reasoning
```

### Why ORCA Needs It

ORCA is a decision-intelligence system rather than a generic chatbot.

Users need to know:

* where information came from
* when it was observed
* what dataset was used
* whether it was measured or predicted
* what uncertainty exists

### Limitations

Grounding is only as reliable as the underlying evidence.

### Common Misconception

**Misconception:** Adding a citation automatically makes an answer scientifically valid.

**Reality:** The cited source must actually support the claim.

---

# F.4 Knowledge Graphs

### Definition

A knowledge graph represents entities and relationships as a graph.

Example:

```text
SST
 │
 ├── measured_by → satellite
 │
 ├── varies_with → season
 │
 └── associated_with → thermal habitat

Chlorophyll-a
 │
 ├── associated_with → phytoplankton
 │
 └── used_as → productivity indicator
```

### Unit

Not applicable.

### Why ORCA Needs It

Knowledge graphs can help represent:

* scientific concepts
* dataset relationships
* spatial relationships
* temporal relationships
* entity relationships
* provenance

### Potential Data Sources

* scientific ontologies
* official metadata
* domain literature
* ORCA-curated relationships

### Limitations

Knowledge graphs may contain:

* incomplete relationships
* outdated information
* incorrectly encoded assumptions

### Common Misconception

**Misconception:** A knowledge graph contains the complete truth about a domain.

**Reality:** It is a structured representation of selected knowledge.

---

# F.5 Uncertainty

### Definition

Uncertainty describes the lack of complete knowledge about the true value, state, or outcome.

Sources include:

* measurement error
* model uncertainty
* sampling limitations
* forecast uncertainty
* spatial gaps
* temporal gaps

### Unit

Depends on the variable.

Examples:

```text
SST = 28.2 ± 0.4 °C
```

or:

```text
Forecast probability = 70%
```

### Typical Interpretation

Uncertainty should be explicitly represented rather than hidden.

### Why ORCA Needs It

Marine decisions often involve incomplete information.

ORCA should communicate uncertainty in:

* forecasts
* habitat predictions
* anomaly detection
* satellite retrievals
* interpolated values

### Common Misconception

**Misconception:** Uncertainty means the data is useless.

**Reality:** Quantified uncertainty is an essential component of scientific decision-making.

---

# F.6 Confidence

### Definition

Confidence represents how strongly a system supports a conclusion based on available evidence.

Confidence is not necessarily the same as statistical probability.

### Unit

Possible representations:

* 0–1 score
* percentage
* low / medium / high

The definition must be explicitly documented.

### Typical Interpretation

A high-confidence recommendation should generally have:

* strong evidence
* good data quality
* sufficient coverage
* agreement between relevant sources
* validated reasoning

### Why ORCA Needs It

ORCA should distinguish:

```text
High confidence
```

from:

```text
Weakly supported inference
```

### Limitations

An arbitrary AI confidence score can be misleading if it is not calibrated.

### Common Misconception

**Misconception:** LLM confidence equals scientific probability.

**Reality:** They are fundamentally different concepts unless a calibrated probabilistic model explicitly defines the relationship.

---

# F.7 Anomaly Detection

### Definition

Anomaly detection identifies observations that differ substantially from an expected baseline.

Example:

```text
Observed SST = 31°C
Historical expected SST = 28°C
```

The difference may indicate an anomaly.

### Unit

Depends on the parameter:

* °C
* mg/m³
* m
* standardized score
* percentile

### Typical Interpretation

An anomaly means:

> "This observation differs from the defined baseline."

It does not automatically mean:

> "This observation is dangerous."

### Why ORCA Needs It

Anomaly detection can identify:

* marine heat waves
* unusual chlorophyll events
* unusual SSH patterns
* abnormal environmental conditions
* potential HAB-related anomalies

### Potential Data Sources

* satellite observations
* historical climatologies
* reanalysis
* model outputs
* sensor networks

### Limitations

Results depend strongly on:

* baseline period
* threshold
* spatial scale
* temporal scale
* data quality

### Common Misconception

**Misconception:** Every anomaly is an emergency.

**Reality:** An anomaly is simply a departure from an expected baseline.

---

# 4. Important Scientific Relationships for ORCA

ORCA should understand relationships between variables without treating them as deterministic rules.

---

## 4.1 SST ↔ Marine Habitat

### Established relationship

Temperature can influence physiological performance and distribution of marine organisms.

### ORCA interpretation

SST can be an important habitat variable.

### Do not infer

```text
Temperature X → fish definitely present
```

Species-specific evidence is required.

---

## 4.2 Wind ↔ Upwelling

### Established relationship

Wind stress can contribute to coastal upwelling under appropriate geographic and atmospheric conditions.

### ORCA interpretation

Wind direction and magnitude can be used alongside SST and other evidence to assess potential upwelling.

### Do not infer

```text
Strong wind → upwelling everywhere
```

---

## 4.3 Upwelling ↔ Nutrients

### Established relationship

Upwelling can transport deeper nutrient-rich water toward the surface.

### ORCA interpretation

Upwelling can contribute to enhanced nutrient availability.

### Do not infer

```text
Upwelling → immediate high chlorophyll
```

Light, residence time, phytoplankton community, grazing, and other factors matter.

---

## 4.4 Nutrients ↔ Phytoplankton

### Established relationship

Nutrients can limit phytoplankton growth in many marine environments.

### ORCA interpretation

Nutrient availability is one factor controlling primary productivity.

### Do not infer

```text
More nutrients → always more phytoplankton
```

Other limiting factors can dominate.

---

## 4.5 Chlorophyll-a ↔ Phytoplankton

### Established relationship

Chlorophyll-a is a major pigment used by phytoplankton and is widely used as an indicator of phytoplankton biomass/concentration.

### ORCA interpretation

Elevated chlorophyll can indicate elevated phytoplankton concentration.

### Do not infer

```text
High chlorophyll → high fish abundance
```

---

## 4.6 Phytoplankton ↔ Zooplankton

### Established relationship

Many zooplankton consume phytoplankton.

### ORCA interpretation

Phytoplankton availability can contribute to zooplankton food availability.

### Important qualification

The response can involve time lags and is affected by species composition, grazing, temperature, and other factors.

---

## 4.7 SSH ↔ Ocean Currents

### Established relationship

Horizontal gradients in sea-surface height can be used to estimate geostrophic flow under appropriate assumptions.

### ORCA interpretation

SSH is useful for deriving or interpreting large-scale and mesoscale circulation.

### Do not infer

```text
SSH value alone → direct current measurement
```

---

## 4.8 Fronts ↔ Biological Aggregation

### Scientific basis

Some physical and biological fronts can concentrate nutrients or organisms and may be associated with enhanced biological activity.

### ORCA interpretation

Fronts are useful candidate features for habitat analysis.

### Do not infer

```text
Detected front → guaranteed fish aggregation
```

---

## 4.9 Eddies ↔ Ecosystem Dynamics

### Scientific basis

Eddies can redistribute heat, nutrients, plankton, and other properties.

### ORCA interpretation

Eddy structure can provide useful context for biological observations.

### Do not infer

```text
Eddy type → universal biological outcome
```

---

# 5. Data Interpretation Rules

ORCA agents should follow these rules when reasoning over marine data.

---

## Rule 1 — Never confuse correlation with causation

Bad:

> "Chlorophyll increased, therefore fish increased."

Better:

> "Chlorophyll increased, indicating elevated phytoplankton concentration. This may provide evidence of enhanced primary productivity, but fish response depends on species, food-web dynamics, habitat conditions, and time lag."

---

## Rule 2 — Never treat a proxy as the underlying phenomenon

Examples:

```text
Chlorophyll-a ≠ fish abundance

SST ≠ complete ocean temperature profile

SSH ≠ direct current observation

Satellite classification ≠ direct species identification
```

---

## Rule 3 — Preserve spatial resolution

If:

```text
Dataset A = 1 km
Dataset B = 25 km
```

ORCA should not describe the combined result as having 1 km ecological accuracy merely because one layer has 1 km resolution.

---

## Rule 4 — Preserve temporal context

Every observation should ideally contain:

```text
timestamp
location
parameter
value
unit
source
quality
resolution
```

---

## Rule 5 — Distinguish observation from prediction

Examples:

```text
Observed SST
```

is different from:

```text
Forecast SST
```

Likewise:

```text
Observed catch
```

is different from:

```text
Predicted fish habitat
```

---

## Rule 6 — Never hide missing data

A missing observation is not equivalent to:

```text
0
```

and should not automatically be treated as normal conditions.

---

## Rule 7 — Avoid false precision

If the source uncertainty is large, ORCA should not produce unnecessarily precise conclusions.

Bad:

> "Fish abundance will be 17,483 individuals."

Better:

> "The available environmental indicators suggest relatively favorable habitat conditions, but fish abundance cannot be determined reliably from these variables alone."

---

# 6. Spatial Reasoning Rules

Marine observations should be interpreted in their geographic context.

ORCA should consider:

```text
Latitude
Longitude
Depth
Distance from coast
Bathymetry
EEZ
Oceanographic region
```

A parameter can have very different meaning in:

* open ocean
* continental shelf
* estuary
* coastal upwelling zone
* deep ocean
* coral reef environment

Therefore:

> **Same measurement ≠ same ecological meaning everywhere.**

---

# 7. Temporal Reasoning Rules

ORCA should consider:

```text
Current observation
Historical climatology
Season
Recent trend
Forecast
Event duration
Time since previous observation
```

For example:

```text
Current SST = 29°C
```

alone provides limited information.

But:

```text
Current SST = 29°C
Historical seasonal median = 27°C
Persistent for 8 days
```

provides evidence of a potentially meaningful anomaly.

---

# 8. Species-Specific Reasoning

Marine ecosystem reasoning should be species-aware whenever possible.

For example:

```text
Species
   ↓
Preferred temperature
Preferred salinity
Depth range
Prey
Spawning conditions
Seasonality
Migration
Bathymetry
Fishing gear
```

A generic:

> "good fishing condition"

is less scientifically meaningful than:

> "environmental conditions are consistent with the modeled habitat preferences of Species X."

---

# 9. PFZ Reasoning Framework

ORCA should treat PFZ generation as a **multi-variable decision problem**, not a single-variable threshold.

Conceptual pipeline:

```text
                    Marine Data
                        │
       ┌────────────────┼─────────────────┐
       │                │                 │
      SST          Chlorophyll-a       Currents
       │                │                 │
       ├────────────┬───┴───────┬─────────┤
       │            │           │
    Fronts       Upwelling    Eddies
       │            │           │
       └────────────┼───────────┘
                    │
             Habitat Features
                    │
          Species / Fishery Data
                    │
                    ▼
          Habitat Suitability
                    │
                    ▼
               PFZ Estimate
                    │
                    ▼
             Confidence + Evidence
```

This is a **conceptual architecture**, not a claim that every PFZ methodology must use every variable.

---

# 10. Marine Safety Reasoning

Marine safety should prioritize authoritative forecasts and warnings over AI-generated inference.

Conceptual hierarchy:

```text
Official warning / advisory
        ↓
Forecast products
        ↓
Current observations
        ↓
Historical climatology
        ↓
AI interpretation
```

ORCA should not override official safety warnings.

For questions such as:

> "Is it safe to venture into the sea tomorrow?"

ORCA should consider:

* official marine warnings
* cyclone information
* wind
* wave height
* wave period
* currents
* weather forecast
* forecast uncertainty
* vessel/fishing context

A simple threshold-based AI answer is insufficient for safety-critical decisions.

---

# 11. Data Quality Dimensions

Every ORCA dataset should ideally be characterized by:

| Dimension           | Meaning                                        |
| ------------------- | ---------------------------------------------- |
| Accuracy            | How close the measurement is to the true value |
| Precision           | Repeatability/measurement resolution           |
| Spatial resolution  | Geographic detail                              |
| Temporal resolution | Frequency of observations                      |
| Coverage            | Geographic availability                        |
| Completeness        | Percentage of expected observations available  |
| Latency             | Delay between observation and availability     |
| Uncertainty         | Quantified lack of certainty                   |
| Provenance          | Origin and processing history                  |
| Version             | Product/model version                          |
| Quality flag        | Dataset-specific quality assessment            |

---

# 12. Scientific Vocabulary Rules for AI Agents

Agents should prefer scientifically precise wording.

### Use

* "associated with"
* "consistent with"
* "suggests"
* "may indicate"
* "is a proxy for"
* "is correlated with"
* "under these conditions"
* "according to the available data"
* "model estimates"
* "observations indicate"

### Avoid unsupported language

* "proves"
* "guarantees"
* "definitely causes"
* "fish will be here"
* "safe for all vessels"
* "chlorophyll means fish"
* "one parameter determines ecosystem health"

unless the evidence genuinely supports such a statement.

---

# 13. Observation → Inference → Recommendation

ORCA should structure reasoning into three levels.

## Level 1 — Observation

What does the data directly show?

Example:

> "SST is 1.8°C above the seasonal climatological threshold."

## Level 2 — Scientific inference

What scientifically defensible interpretation follows?

> "This indicates an anomalously warm surface-water condition."

## Level 3 — Decision recommendation

What action or conclusion is appropriate?

> "The area may warrant marine heat-wave monitoring; ecological effects should be interpreted alongside species and biological observations."

The system must not skip directly from:

```text
Observation
```

to:

```text
Recommendation
```

without explaining the reasoning and uncertainty.

---

# 14. Heuristic vs Scientific Claim Matrix

| Statement                                                     | Classification                                |
| ------------------------------------------------------------- | --------------------------------------------- |
| SST describes near-surface ocean temperature                  | Scientific fact                               |
| Chlorophyll-a is associated with phytoplankton biomass        | Scientific relationship/proxy                 |
| Wind can drive coastal upwelling under suitable conditions    | Scientific relationship                       |
| SSH gradients can be used to estimate geostrophic currents    | Scientific relationship                       |
| High chlorophyll always means high fish abundance             | Unsupported claim                             |
| A detected front may be relevant to fish habitat              | Scientific possibility / contextual inference |
| Every front is a PFZ                                          | Unsupported heuristic                         |
| Habitat suitability means fish are guaranteed present         | Incorrect                                     |
| High wave height can increase marine operational risk         | Scientific/operational relationship           |
| Any warm SST event is a marine heat wave                      | Incorrect                                     |
| RAG guarantees factual answers                                | Incorrect                                     |
| More AI agents always improve results                         | Unsupported assumption                        |
| A high model score means biological certainty                 | Incorrect unless calibrated                   |
| Interpolation produces measured values                        | Incorrect                                     |
| Higher spatial resolution automatically means higher accuracy | Incorrect                                     |

---

# 15. ORCA Agent Knowledge Model

A marine-science-aware ORCA agent should internally represent information approximately as:

```text
Parameter
│
├── Value
├── Unit
├── Timestamp
├── Geographic extent
├── Spatial resolution
├── Temporal resolution
├── Source
├── Processing method
├── Quality flag
├── Uncertainty
├── Scientific interpretation
└── Limitations
```

For derived conclusions:

```text
Conclusion
│
├── Supporting observations
├── Scientific relationships
├── Model / algorithm
├── Assumptions
├── Uncertainty
├── Confidence
└── Provenance
```

---

# 16. Minimum Provenance Required for ORCA

For every important environmental value, ORCA should attempt to retain:

```text
source
dataset name
parameter
unit
timestamp
latitude
longitude
spatial resolution
temporal resolution
processing level
quality flag
model/version
```

This enables reproducibility and evidence-grounded explanations.

---

# 17. Key Marine Data Source Categories

Potential authoritative or widely used sources include:

### Indian Sources

* ISRO Earth Observation missions and MOSDAC
* INCOIS
* Indian Meteorological Department (IMD)
* Indian fisheries and oceanographic institutions
* National Hydrographic resources where accessible

### International Sources

* NOAA
* NASA
* Copernicus Marine Service
* ECMWF
* GEBCO
* Argo program
* global ocean-model/reanalysis systems

ORCA should prefer the most authoritative source available for the specific variable and geographic region.

---

# 18. Final Scientific Guardrails

The following principles are mandatory for ORCA's AI reasoning layer.

### Guardrail 1

**Do not equate environmental proxies with fish abundance.**

### Guardrail 2

**Do not treat correlations as causal relationships without evidence.**

### Guardrail 3

**Do not combine datasets without considering spatial and temporal resolution.**

### Guardrail 4

**Do not present predictions as observations.**

### Guardrail 5

**Do not present interpolated values as measurements.**

### Guardrail 6

**Do not present model confidence as statistical probability unless properly calibrated.**

### Guardrail 7

**Do not interpret anomalies without defining the baseline.**

### Guardrail 8

**Do not make species-specific claims without species-specific evidence.**

### Guardrail 9

**Do not treat PFZ as guaranteed fish presence or guaranteed catch.**

### Guardrail 10

**Do not issue safety-critical recommendations that contradict authoritative warnings.**

### Guardrail 11

**Every important AI conclusion should be traceable to evidence.**

### Guardrail 12

**When evidence is insufficient, ORCA should explicitly state that uncertainty rather than inventing a conclusion.**

---

# 19. ORCA Scientific Reasoning Philosophy

The central scientific philosophy of ORCA is:

```text
Observe
   ↓
Contextualize
   ↓
Cross-validate
   ↓
Reason
   ↓
Quantify uncertainty
   ↓
Explain evidence
   ↓
Recommend cautiously
```

ORCA should not behave as:

```text
Data
 ↓
LLM guess
 ↓
Confident answer
```

Instead, it should behave as:

```text
Heterogeneous Marine Data
        ↓
Data Quality + Provenance
        ↓
Spatial/Temporal Alignment
        ↓
Scientific Feature Extraction
        ↓
Domain-Specialized Agents
        ↓
Evidence Fusion
        ↓
Uncertainty Assessment
        ↓
Explainable Decision Intelligence
```

The goal is not simply to make ORCA **sound scientifically intelligent**.

The goal is to make its reasoning **traceable, evidence-grounded, scientifically defensible, and explicit about uncertainty**.

---

# 20. One-Line Mental Model

> **ORCA interprets the ocean as a coupled physical–biological–fisheries–hazard system rather than treating individual datasets as isolated facts.**

This principle should guide the architecture, agent design, data fusion, retrieval system, reasoning engine, UI explanations, and evaluation methodology of SIH26176 ORCA.
