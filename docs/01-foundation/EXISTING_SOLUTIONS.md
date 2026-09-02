# Existing Solutions Analysis – SIH26176 ORCA

**Document Purpose:** Comprehensive analysis of existing marine information systems, data sources, AI/ML research, and multi-agent scientific systems relevant to ORCA. This document identifies technological and functional gaps that ORCA aims to address.

**Last Updated:** August 30, 2026

**Research Methodology:** Primary sources from official organizational websites, peer-reviewed research papers (2024–2026), and authoritative marine data portals.

---

## Table of Contents

1. [Indian Marine Information Systems](#1-indian-marine-information-systems)
   - 1.1 INCOIS PFZ Advisory
   - 1.2 INCOIS SAMUDRA
   - 1.3 INCOIS WebGIS
   - 1.4 ISRO EOS-06/Oceansat-3
   - 1.5 MOSDAC
2. [International Marine Data Systems](#2-international-marine-data-systems)
   - 2.1 NASA Ocean Color
   - 2.2 NOAA IOOS
   - 2.3 Copernicus Marine Service
3. [Marine Ecosystem Models](#3-marine-ecosystem-models)
4. [Marine AI and LLM Research](#4-marine-ai-and-llm-research)
5. [Marine Knowledge Graph Research](#5-marine-knowledge-graph-research)
6. [Multi-Agent Scientific Systems](#6-multi-agent-scientific-systems)
7. [Comparative Analysis and ORCA Relevance](#7-comparative-analysis-and-orca-relevance)
8. [References](#8-references)

---

## 1. Indian Marine Information Systems

### 1.1 INCOIS PFZ Advisory

| Attribute | Details |
|-----------|---------|
| **Name** | Potential Fishing Zone (PFZ) Advisory |
| **Organization** | Indian National Centre for Ocean Information Services (INCOIS), Ministry of Earth Sciences, Government of India |
| **Purpose** | Provide daily fishing advisories to identify oceanic areas with high probability of fish aggregation across the Indian Exclusive Economic Zone (EEZ) [cite:3][cite:8][cite:12] |
| **Data** | Satellite-derived Sea Surface Temperature (SST), Chlorophyll-a concentration, oceanographic variables, numerical ocean models, fisheries science data [cite:3][cite:4][cite:8] |
| **Technology** | Advanced machine learning algorithms for Hilsa availability prediction, satellite data processing, numerical ocean models, integration with 586 fish-landing centres [cite:2][cite:3] |
| **Users** | Marine fishermen, fisheries departments, coastal communities [cite:3][cite:8][cite:13] |
| **Outputs** | Daily PFZ advisories with coordinates (latitude/longitude), depth, direction, distance from coastal landmarks, three-day outlook, five-level fishing prospect categorization (very low, low, medium, high, very high) [cite:2][cite:3][cite:8] |
| **Strengths** | • Authoritative government service with operational deployment since 2000s [cite:3]<br>• Scientifically validated using satellite observations and ocean models [cite:3][cite:8]<br>• Demonstrated economic impact: reduced search time, higher catch rates [cite:8]<br>• Integration with Vessel Communication and Support System (VCSS) and Nabhmitra app for last-mile delivery [cite:13]<br>• Multilingual dissemination capabilities [cite:4] |
| **Limitations** | • Single-parameter focus (primarily SST + chlorophyll for PFZ) [cite:3][cite:8]<br>• Limited cross-domain reasoning (does not integrate safety, weather, ecosystem anomalies simultaneously) [cite:3]<br>• Static advisory format without interactive natural-language querying [cite:3]<br>• No explicit uncertainty quantification or confidence scoring [cite:3]<br>• Human interpretation required for integrating multiple advisories (PFZ + weather + warnings) [cite:4] |
| **ORCA Relevance** | **HIGH** – PFZ is a critical input for ORCA's Fisheries Agent. ORCA proposes to integrate PFZ with ecosystem, safety, ocean, and geospatial reasoning rather than replacing PFZ. ORCA's innovation is cross-domain reasoning layer over PFZ and other data sources [cite:3][cite:8]. |
| **Official URL** | https://www.incois.gov.in/incois/adv_pfz.aspx |
| **Research Papers** | • Frontiers in Marine Science (2026): "Development and deployment of a pilot multilingual citizen..." [cite:3]<br>• The Hindu (2026): "INCOIS advisory helps fishermen net Hilsa bonanza off Bengal coast" [cite:2] |

---

### 1.2 INCOIS SAMUDRA

| Attribute | Details |
|-----------|---------|
| **Name** | SAMUDRA (context-dependent: refers to multiple systems) |
| **Organization** | Context 1: INCOIS (marine information); Context 2: Ministry of Shipping (e-Samudra maritime governance) [cite:1][cite:5][cite:14] |
| **Purpose** | **Note:** Research reveals two distinct systems:<br>1. **INCOIS SAMUDRA**: Marine information and advisory services (specific details require direct INCOIS verification)<br>2. **e-Samudra**: Cloud-native maritime governance platform unifying 60+ maritime services under Directorate General of Shipping [cite:1][cite:5][cite:14] |
| **Data** | **e-Samudra**: Ship registration, certification, seafarer services, charter permissions, port services, regulatory compliance data [cite:1][cite:5][cite:14]<br>**INCOIS SAMUDRA**: Marine/oceanographic data (specifics require verification) |
| **Technology** | **e-Samudra**: Cloud-native architecture, geospatial mapping, predictive analytics, AI-powered dashboards, digital workflows, online payments, real-time tracking [cite:1][cite:5][cite:14]<br>**INCOIS SAMUDRA**: Not publicly documented in detail |
| **Users** | **e-Samudra**: Shipping industry, vessel operators, seafarers, port authorities, maritime regulators [cite:1][cite:5][cite:14]<br>**INCOIS SAMUDRA**: Marine stakeholders (specifics require verification) |
| **Outputs** | **e-Samudra**: Digital certificates, regulatory approvals, compliance tracking, real-time application status [cite:1][cite:5][cite:14]<br>**INCOIS SAMUDRA**: Marine advisories (specifics require verification) |
| **Strengths** | **e-Samudra**:<br>• Unified digital window for 72+ maritime services [cite:15]<br>• Paperless workflows with real-time tracking [cite:14][cite:15]<br>• AI-powered dashboards for decision support [cite:5]<br>• Integration with global sustainability compliance [cite:5] |
| **Limitations** | **e-Samudra**: Focuses on regulatory/administrative services, not marine ecosystem reasoning or fishing decision support [cite:1][cite:5][cite:14]<br>**INCOIS SAMUDRA**: Limited public documentation on technical architecture and reasoning capabilities |
| **ORCA Relevance** | **MODERATE** – e-Samudra addresses maritime governance, not marine ecosystem decision intelligence. ORCA targets different use case (ecosystem reasoning vs. regulatory compliance). INCOIS SAMUDRA may overlap with marine advisory domain but lacks documented cross-domain reasoning capabilities. |
| **Official URL** | **e-Samudra**: https://esamudra.gov.in/ (Ministry of Shipping)<br>**INCOIS**: https://www.incois.gov.in/ |
| **Research Papers** | • The Week (2026): "Shipping ministry launches flagship e-Samudra platform" [cite:5]<br>• BusinessWorld (2026): "The Sea Has No Signboards, ISRO Built One" [cite:4] |

**Important Note:** The name "SAMUDRA" appears in multiple contexts. ORCA team should verify with INCOIS which specific system corresponds to INCOIS SAMUDRA referenced in the problem statement.

---

### 1.3 INCOIS WebGIS

| Attribute | Details |
|-----------|---------|
| **Name** | INCOIS WebGIS (Marine Geospatial Portal) |
| **Organization** | Indian National Centre for Ocean Information Services (INCOIS) |
| **Purpose** | Provide geospatial visualization and access to marine/oceanographic data products through web-based GIS interface |
| **Data** | Marine geospatial datasets including bathymetry, EEZ boundaries, oceanographic parameters, PFZ maps, hazard zones |
| **Technology** | Web GIS frameworks, OGC-compliant services (WMS, WFS), geospatial databases |
| **Users** | Marine scientists, researchers, government agencies, fisheries departments |
| **Outputs** | Interactive marine maps, geospatial data layers, downloadable GIS datasets, thematic maps |
| **Strengths** | • Authoritative geospatial data from INCOIS<br>• OGC-compliant interoperability<br>• Integration with other INCOIS products (PFZ, advisories)<br>• Free access to marine geospatial information |
| **Limitations** | • Primarily visualization and data access portal<br>• Limited AI/ML-based reasoning capabilities<br>• No natural-language query interface<br>• Static layer-based visualization without cross-domain inference |
| **ORCA Relevance** | **HIGH** – INCOIS WebGIS provides geospatial context that ORCA's Geospatial Agent can leverage. ORCA proposes to add reasoning layer over geospatial data rather than replacing WebGIS. |
| **Official URL** | https://www.incois.gov.in/ (WebGIS section) |
| **Research Papers** | Not specifically documented in peer-reviewed literature |

---

### 1.4 ISRO EOS-06/Oceansat-3

| Attribute | Details |
|-----------|---------|
| **Name** | EOS-06 / Oceansat-3 |
| **Organization** | Indian Space Research Organisation (ISRO) |
| **Purpose** | Earth observation satellite for ocean colour monitoring, sea-surface temperature measurement, and wind vector data collection to support operational oceanography and fisheries [cite:4][cite:39][cite:43] |
| **Data** | Ocean Colour Monitor (OCM-3) with 13 bands in VNIR region (400–1100 nm), Ku-Band pencil beam scatterometer for ocean surface wind vectors, global ocean coverage with 2-day repeat for ocean colour, 12-hour repeat for wind [cite:4][cite:43] |
| **Technology** | PSLV-C54 launch (November 26, 2022), Sun-synchronous polar orbit, Ocean Colour Monitor instrument, scatterometer for wind measurement [cite:4][cite:39][cite:43] |
| **Users** | INCOIS (for PFZ advisories), MOSDAC (data archival), researchers, operational oceanography services, fisheries [cite:4][cite:31][cite:43] |
| **Outputs** | Ocean colour products (chlorophyll-a, phytoplankton), sea-surface temperature, wind vectors, Level-3 gridded products (daily, 8-day, monthly at ~4 km resolution) [cite:4][cite:31][cite:43] |
| **Strengths** | • Indigenous Indian satellite with operational deployment [cite:4][cite:39]<br>• Improved temporal resolution (2-day ocean colour, 12-hour wind) [cite:43]<br>• Data continuity from Oceansat-2 with enhanced capabilities [cite:43]<br>• Free data access through Bhoonidhi and Bhuvan portals [cite:43]<br>• Directly supports PFZ advisory generation [cite:4] |
| **Limitations** | • Satellite provides raw/processed observations, not decision intelligence [cite:4][cite:43]<br>• Requires downstream processing (INCOIS, MOSDAC) for operational products [cite:4][cite:31]<br>• Cloud cover can affect optical ocean colour measurements [cite:43]<br>• Data interpretation requires domain expertise |
| **ORCA Relevance** | **CRITICAL** – EOS-06 is a primary data source for ORCA. SST and chlorophyll from OCM-3 are fundamental inputs for Ocean Agent, Ecosystem Agent, and Fisheries Agent. ORCA relies on EOS-06 data continuity for operational reasoning [cite:4][cite:43]. |
| **Official URL** | https://www.isro.gov.in/EOS-06.html<br>https://bhoonidhi.nrsc.gov.in/ (data access)<br>https://bhuvan.nrsc.gov.in/ (visualization) |
| **Research Papers** | • IOCCG (2026): "August 2026 News" – Oceansat-3 mission overview [cite:43]<br>• BusinessWorld (2026): "The Sea Has No Signboards, ISRO Built One" [cite:4] |

---

### 1.5 MOSDAC

| Attribute | Details |
|-----------|---------|
| **Name** | Meteorological and Oceanographic Satellite Data Archival Centre (MOSDAC) |
| **Organization** | Indian Space Research Organisation (ISRO) |
| **Purpose** | Archive and disseminate meteorological and oceanographic satellite data products from ISRO missions for citizens and government departments [cite:31][cite:32] |
| **Data** | Browse products (JPG, GIF, PNG), web services (OGC-compliant protocols), satellite data products (HDF, netCDF, GeoTIFF), ocean colour, SST, wind, atmospheric parameters [cite:31][cite:32] |
| **Technology** | Data archival systems, OGC-compliant web services (WMS, WFS, WCS), Bhuvan portal integration, HDF/netCDF/GeoTIFF data formats [cite:31][cite:32] |
| **Users** | Citizens, researchers, government departments, operational agencies [cite:31][cite:32] |
| **Outputs** | Freely accessible browse products, downloadable satellite data products, web services for programmatic access, integration with Bhuvan geoportal [cite:31][cite:32] |
| **Strengths** | • Official ISRO data archive with authoritative products [cite:31][cite:32]<br>• OGC-compliant interoperability for GIS integration [cite:31]<br>• Multiple data formats (HDF, netCDF, GeoTIFF) for diverse use cases [cite:31]<br>• Free access for most data [cite:32]<br>• Integration with Bhuvan for visualization [cite:31][cite:32] |
| **Limitations** | • Primarily data archival and distribution, not decision support [cite:31][cite:32]<br>• Some services reported as temporarily unavailable (as of August 2026) [cite:45]<br>• Requires user expertise to interpret raw satellite products<br>• No AI/ML-based reasoning or natural-language interface |
| **ORCA Relevance** | **HIGH** – MOSDAC is a key data source for ORCA, providing access to EOS-06 and other ISRO oceanographic products. ORCA can leverage MOSDAC's OGC-compliant services for automated data retrieval [cite:31][cite:32]. |
| **Official URL** | https://mosdac.gov.in/ |
| **Research Papers** | • ISRO (2026): "Meteorological & Oceanographic Satellite Data Archival Centre" [cite:31][cite:32] |

---

## 2. International Marine Data Systems

### 2.1 NASA Ocean Color

| Attribute | Details |
|-----------|---------|
| **Name** | NASA Ocean Biology DAAC / Ocean Color Data |
| **Organization** | NASA Goddard Space Flight Center (GSFC), Ocean Biology Processing Group (OBPG), Ocean Biology Distributed Active Archive Center (OB.DAAC) [cite:33][cite:34][cite:41] |
| **Purpose** | Acquire, archive, and publicly distribute ocean color and sea surface temperature data from multiple satellite missions for scientific research and operational applications [cite:33][cite:34][cite:41] |
| **Data** | MODIS (Terra/Aqua), VIIRS (Suomi NPP, JPSS), OLCI (Sentinel-3), SeaHawk-HawkEye, GOCI, ocean color products (chlorophyll-a, phytoplankton absorption, particulate backscattering), SST, inherent optical properties (IOPs) [cite:33][cite:34][cite:35][cite:37][cite:40][cite:41] |
| **Technology** | OBPG data processing pipeline, SeaDAS Toolbox for data analysis, Ocean Color Level 3/4 Browser, Earthdata platform, HDF/netCDF data formats, API access [cite:33][cite:34][cite:41][cite:42][cite:44] |
| **Users** | Marine scientists, researchers, operational oceanography services, climate researchers, educators [cite:33][cite:34][cite:40] |
| **Outputs** | Level-2/3/4 ocean color products, global composites at various spatial/temporal scales, absorption/scattering coefficients, GIOP model outputs, in situ validation datasets [cite:33][cite:34][cite:36][cite:40] |
| **Strengths** | • Multi-mission data archive with global coverage [cite:34][cite:41]<br>• Long-term data continuity (decades of observations) [cite:34][cite:40]<br>• High-quality processing algorithms (OBPG) [cite:41]<br>• Free and open data access [cite:33][cite:34]<br>• Comprehensive validation datasets [cite:36]<br>• Advanced tools (SeaDAS, Level 3/4 Browser) [cite:33][cite:44] |
| **Limitations** | • Global focus may not provide highest resolution for regional Indian waters<br>• Data latency (processing time from observation to availability)<br>• Requires technical expertise to process and interpret<br>• No integrated decision support or reasoning layer |
| **ORCA Relevance** | **MODERATE-HIGH** – NASA Ocean Color provides complementary global data that can validate or augment ISRO/EOS-06 products for ORCA. Useful for historical comparison and global context. ORCA should prioritize ISRO data for Indian waters but can leverage NASA for validation and research [cite:33][cite:34][cite:41]. |
| **Official URL** | https://www.earthdata.nasa.gov/centers/ob-daac<br>https://www.earthdata.nasa.gov/centers/obpg<br>https://oceancolor.gsfc.nasa.gov/ |
| **Research Papers** | • Earth System Science Data (2026): "A compilation of global bio-optical in situ data for ocean-colour satellite applications – version four" [cite:36]<br>• NASA Ocean Biology DAAC documentation [cite:33][cite:34][cite:41] |

---

### 2.2 NOAA IOOS

| Attribute | Details |
|-----------|---------|
| **Name** | Integrated Ocean Observing System (IOOS) |
| **Organization** | National Oceanic and Atmospheric Administration (NOAA), National Ocean Service, U.S. Department of Commerce [cite:22][cite:62] |
| **Purpose** | Integrated network of people and technology gathering ocean observing data and developing tracking and predictive tools to benefit economy, environment, and public safety [cite:22][cite:62] |
| **Data** | Currents, temperature, salinity, wave height, wind, water quality, harmful algal blooms, marine hazards, in situ sensors, satellite data, numerical models (e.g., West Florida Coastal Ocean Model - WFCOM) [cite:22][cite:62] |
| **Technology** | Environmental Sensor Map, IOOS Model Viewer, data integration platforms, real-time sensor networks, API access, geospatial visualization [cite:22][cite:62] |
| **Users** | Coastal communities, mariners, emergency managers, researchers, coastal zone managers, marine industries [cite:62] |
| **Outputs** | Real-time observations, forecasts, model outputs, interactive maps, data portals, mobile apps, alerts and warnings [cite:22][cite:62] |
| **Strengths** | • Comprehensive observing network with in situ + satellite + models [cite:62]<br>• Real-time data delivery [cite:22][cite:62]<br>• Regional associations covering U.S. coastal waters [cite:62]<br>• Integration of multiple data sources [cite:22][cite:62]<br>• Operational focus on public safety and economic benefit [cite:62] |
| **Limitations** | • U.S.-focused (not directly applicable to Indian waters)<br>• Primarily data delivery and visualization, limited AI reasoning<br>• No natural-language query interface<br>• Does not perform cross-domain decision reasoning |
| **ORCA Relevance** | **MODERATE** – IOOS demonstrates best practices for integrated ocean observing and data delivery. ORCA can learn from IOOS architecture but focuses on Indian waters with ISRO/INCOIS data. IOOS Model Viewer concept is similar to ORCA's proposed marine intelligence map but ORCA adds reasoning layer [cite:22][cite:62]. |
| **Official URL** | https://ioos.noaa.gov/ |
| **Research Papers** | • NOAA IOOS documentation and newsletters [cite:22][cite:62] |

---

### 2.3 Copernicus Marine Service

| Attribute | Details |
|-----------|---------|
| **Name** | Copernicus Marine Service (CMEMS) |
| **Organization** | Mercator Ocean International, European Union Copernicus Programme |
| **Purpose** | Provide free and open data and services tracking ocean state indicators, supporting marine environment protection, energy resources, climate awareness, and decision-making [cite:16][cite:24][cite:61] |
| **Data** | Global and regional ocean physical and biogeochemical data: temperature, salinity, sea level, currents, sea ice, marine ecosystem variables from satellite observations, in situ measurements, numerical model reanalysis and forecasts [cite:16][cite:24][cite:27][cite:61] |
| **Technology** | Copernicus Marine Toolbox (Python API, CLI), MyOcean Pro Viewer (advanced visualization), OGC-compliant WMTS, Catalogue Service for Web (CSW), STAC API, netCDF-4 data format, xarray integration [cite:16][cite:17][cite:18][cite:19][cite:20][cite:21][cite:25][cite:26][cite:27] |
| **Users** | Scientists, policymakers, innovators, marine industries, climate researchers, operational oceanography services [cite:20][cite:24][cite:74] |
| **Outputs** | Daily analyses and forecasts, historical reanalysis, interactive visualizations, downloadable datasets (original files or subsets), API access for programmatic retrieval [cite:16][cite:19][cite:20][cite:21][cite:23][cite:26] |
| **Strengths** | • Comprehensive global and regional ocean products [cite:24][cite:61]<br>• Free and open data access [cite:16][cite:24]<br>• Advanced Toolbox API for programmatic access [cite:16][cite:17][cite:19]<br>• MyOcean Pro Viewer for interactive analysis [cite:20][cite:21][cite:23]<br>• High-quality numerical models and reanalysis (GLORYS12, GLO12) [cite:18][cite:74]<br>• AI integration (GLONET AI-driven forecasting system) [cite:74]<br>• OGC-compliant interoperability [cite:27] |
| **Limitations** | • Global/European focus, not optimized for Indian coastal waters<br>• Primarily data delivery and visualization, not decision intelligence<br>• Requires domain expertise to interpret model outputs<br>• No natural-language reasoning or cross-domain inference |
| **ORCA Relevance** | **MODERATE-HIGH** – Copernicus Marine demonstrates state-of-the-art ocean data delivery and API design. ORCA can learn from Copernicus Toolbox API architecture for data retrieval. GLONET AI forecasting shows hybrid physics-AI approach relevant to ORCA's reasoning layer. However, ORCA focuses on Indian waters with ISRO/INCOIS data and adds decision reasoning not present in Copernicus [cite:16][cite:24][cite:61][cite:74]. |
| **Official URL** | https://data.marine.copernicus.eu/ |
| **Research Papers** | • Mercator Ocean International (2025): GLONET AI-driven global forecasting system [cite:74]<br>• Copernicus Marine Toolbox documentation [cite:16][cite:17][cite:18][cite:19] |

---

## 3. Marine Ecosystem Models

### Overview

Marine ecosystem models simulate biological, chemical, and physical processes in ocean environments. These models are critical for understanding ecosystem dynamics, predicting changes, and supporting management decisions.

### Key Models and Approaches

| Model/Approach | Organization/Source | Purpose | Technology | ORCA Relevance |
|----------------|---------------------|---------|------------|----------------|
| **Numerical Ocean Models (NEMO, ROMS, HYCOM)** | Various (Met Office, NOAA, academic) | Physical ocean forecasting (currents, SST, SSH, salinity) | Physics-based numerical models, data assimilation [cite:66][cite:67] | **HIGH** – ORCA can integrate model outputs as inputs for Ocean Agent and Safety Agent |
| **GLONET (AI-driven)** | Mercator Ocean International | Global 10-day ocean forecasts (temperature, salinity, SSH, currents) | AI/ML trained on GLORYS12 reanalysis, generates forecasts in seconds [cite:74] | **HIGH** – Demonstrates AI forecasting feasibility; ORCA can leverage similar approaches for regional Indian waters |
| **FuXi-ONS** | Academic (arXiv 2026) | Machine-learning ensemble forecasting for global ocean (5-day, 10-day) | Data-driven ensemble prediction, physically structured perturbations, atmospheric encoding [cite:68] | **MODERATE-HIGH** – Shows ML ensemble forecasting advances; relevant for ORCA uncertainty estimation |
| **OceanLight** | Academic (arXiv 2026) | Efficient global ocean forecasting | Geometry-adaptive unstructured mesh tokenization, graph neural networks (GNN), 62% GPU memory reduction [cite:71] | **MODERATE** – Advanced ML architecture for ocean forecasting; ORCA can explore GNN for spatial reasoning |
| **SeaCast** | Academic (Nature 2025) | Mediterranean Sea forecasting | Graph-based deep learning, autoregressive ML model [cite:64] | **MODERATE** – Regional ML forecasting approach; relevant for ORCA's Bay of Bengal/Arabian Sea focus |
| **Hybrid Physics-AI Models** | Various (arXiv 2025, 2026) | Combine physics-based models with ML parameterizations | Physics-informed neural networks, spectral nudging, ML parameterizations in climate models [cite:67][cite:69][cite:73] | **HIGH** – ORCA should integrate physics-based constraints with AI reasoning for scientific validity |
| **Marine Heatwave Prediction Models** | Academic (Springer 2025) | MHW detection and forecasting (up to 10–30 days) | Deep learning (EOF-EMD-Informer), physics-guided DL, VQ-VAE for probabilistic forecasting [cite:65] | **HIGH** – Directly relevant for ORCA's Ecosystem Agent to detect marine heat waves and ecosystem anomalies |
| **MSSTN (Multiscale Spatiotemporal Network)** | Academic (Nature 2025) | Marine environment prediction | Graph Convolutional Networks + Temporal Transformer for spatiotemporal feature fusion [cite:63] | **MODERATE-HIGH** – GCN + Transformer architecture relevant for ORCA's spatiotemporal reasoning |

### Key Insights from Marine Ecosystem Modeling Research

1. **Hybrid Physics-AI is State-of-the-Art**: Pure ML models are being combined with physics-based models to improve accuracy while maintaining physical consistency [cite:67][cite:69][cite:73][cite:74].

2. **Ensemble Forecasting is Critical**: Probabilistic forecasts (e.g., FuXi-ONS) provide uncertainty estimates essential for decision-making [cite:68].

3. **Regional Focus Improves Accuracy**: Regional models (e.g., SeaCast for Mediterranean) outperform global models for specific areas [cite:64], supporting ORCA's focus on Indian coastal waters.

4. **Graph Neural Networks are Emerging**: GNNs are being applied to ocean forecasting (OceanLight, SeaCast) due to their ability to handle irregular spatial structures [cite:64][cite:71].

5. **Explainable AI is Gaining Importance**: Physics-guided and interpretable ML approaches are preferred for scientific applications [cite:65][cite:73].

### ORCA Integration Strategy

- **Ocean Agent**: Integrate outputs from numerical models (NEMO, HYCOM) and AI models (GLONET, FuXi-ONS) for physical parameters.
- **Ecosystem Agent**: Use marine heatwave prediction models and ecosystem anomaly detection from research [cite:65].
- **Uncertainty Estimation**: Leverage ensemble forecasting approaches (FuXi-ONS) for confidence scoring [cite:68].
- **Spatiotemporal Reasoning**: Explore GCN + Transformer architectures (MSSTN, OceanLight) for spatial reasoning [cite:63][cite:71].

---

## 4. Marine AI and LLM Research

### 4.1 LLM Applications in Maritime Domain

| System/Paper | Organization | Purpose | Technology | Key Findings | ORCA Relevance |
|--------------|--------------|---------|------------|--------------|----------------|
| **Llamarine** | Academic (2026) | Open-source LLM for maritime navigation | Domain-specific LLM fine-tuned for maritime context | Outperforms general-purpose LLMs for maritime tasks [cite:59] | **HIGH** – Demonstrates value of domain-specific LLMs; ORCA should consider marine-finetuned models |
| **Ship Navigation LLM** | Academic (2025) | Autonomous collision avoidance decision-making | LLM with hierarchical reasoning (cognition → analysis → decision), scene-instruction mapping | F1-score 0.92 for direction action, 0.82 for speed action, trajectory errors <10m [cite:48] | **HIGH** – Hierarchical reasoning framework directly relevant to ORCA's Coordinator agent |
| **COLREG Compliance LLM** | Academic (arXiv 2026) | Situational understanding and COLREG compliance | LLMs evaluated on 50 real-world navigation scenarios | Maritime navigation remains difficult without fine-tuning, even for large models [cite:52] | **MODERATE-HIGH** – Highlights need for domain fine-tuning and retrieval augmentation (RAG) |
| **Small LLMs on Edge Devices** | Academic (Sensors 2026) | Maritime navigation support on edge devices | Small Language Models (SLMs) with RAG using Sailing Directions | RAG significantly improves response quality for constrained SLMs [cite:55] | **MODERATE** – Supports ORCA's RAG Agent design for knowledge retrieval |
| **Agentic RAG for Maritime AIoT** | Academic (PMC 2026) | Natural language access to maritime sensor data | Agentic RAG framework integrating LLMs with IoT sensors | Enables conversational access to sensor data streams [cite:47] | **HIGH** – Directly relevant to ORCA's RAG Agent and multi-agent architecture |
| **DePTH-GPT** | China (UN Decade of Ocean Science) | Deep-sea research cognitive system | Multimodal AI integrating video, maps, simulations, sediment samples, bioacoustics | Demonstrates multimodal AI for ocean exploration [cite:29] | **MODERATE** – Multimodal integration approach relevant for ORCA's heterogeneous data fusion |

### 4.2 Marine AI Reasoning and Decision Support

| System/Paper | Organization | Purpose | Technology | Key Findings | ORCA Relevance |
|--------------|--------------|---------|------------|--------------|----------------|
| **Compass** | Academic (arXiv 2026) | Marine lead data extraction from scientific papers | Expert-guided LLM agent with Knowledge Tree, task decomposition | 92% accuracy in data extraction, 3,751 new records from 230,000 papers [cite:70] | **CRITICAL** – Expert-guided agent framework with Knowledge Tree is directly analogous to ORCA's Coordinator + specialized agents. Demonstrates scientific validity through expert co-design [cite:70]. |
| **Sensorium Arc** | Academic (arXiv 2025) | Interactive eco-art system personifying ocean | Modular multi-agent system, RAG-enhanced LLM, natural spoken conversation | Blends scientific insight with ecological poetics, mediates affective access to marine data [cite:51] | **HIGH** – Multi-agent RAG architecture for ocean data exploration; demonstrates conversational AI for marine data [cite:51] |
| **MARINE (Multi-Agent Recursive IN-context Enhancement)** | Academic (arXiv 2025) | Improve LLM reasoning through iterative refinement | Multi-agent framework with persistent reference trajectory, minimal batch optimization | 80B model with MARINE matches 1000B standalone agents [cite:50] | **MODERATE-HIGH** – Multi-agent reasoning enhancement technique; ORCA can explore iterative refinement for Coordinator |
| **AI for Atmosphere-Ocean Sciences** | Academic (PMC 2026) | Review of AI advancements in Earth science | Survey of AI/ML applications in oceanography, climate science | EarthLink agents form forecast-to-action framework; AI investigates drivers, evaluates impacts, proposes strategies [cite:49] | **HIGH** – EarthLink concept similar to ORCA: AI not just predicts but reasons about drivers and proposes actions [cite:49] |
| **OceanPile** | Academic (Hugging Face 2026) | Large-scale multimodal ocean corpus for foundation models | OceanCorpus (sonar, imagery, text), OceanInstruction (knowledge graph-guided), OceanBenchmark | Provides training data and benchmark for marine AI [cite:56] | **MODERATE** – Supports ORCA's RAG Agent with domain-specific corpus and knowledge graph |
| **MaRAG** | Academic (ScienceDirect 2026) | Multi-agent framework with knowledge graph + RAG | Knowledge graph construction + retrieval-augmented generation | Supports intelligent decision-making in marine domain [cite:53] | **HIGH** – Directly relevant to ORCA's Knowledge/RAG Agent + knowledge graph integration |
| **LLM + Multi-Agent Deep RL** | Academic (J-Stage 2026) | Autonomous coordination in marine environments | Integration of LLMs with Multi-Agent Deep Reinforcement Learning (MADRL) | Enhances autonomous coordination capabilities [cite:54] | **MODERATE** – LLM + RL integration could enhance ORCA's agent coordination |

### Key Insights from Marine AI Research

1. **Domain-Specific Fine-Tuning is Essential**: General-purpose LLMs underperform in maritime tasks without domain adaptation [cite:48][cite:52][cite:59].

2. **Expert-Guided Agents Ensure Scientific Validity**: Compass demonstrates that expert co-design (Knowledge Tree) prevents hallucinations and ensures scientific rigor [cite:70].

3. **Multi-Agent Architectures are Emerging**: Sensorium Arc, MaRAG, and Compass all use multi-agent frameworks for marine applications [cite:51][cite:53][cite:70].

4. **RAG is Critical for Scientific Accuracy**: Retrieval augmentation from authoritative sources reduces hallucinations and improves response quality [cite:47][cite:55][cite:70].

5. **Knowledge Graphs Enhance Reasoning**: OceanPile, MaRAG, and Compass all integrate knowledge graphs for structured domain knowledge [cite:53][cite:56][cite:70].

6. **Hybrid Physics-AI is Preferred**: Pure data-driven approaches are being combined with physics-based constraints for scientific validity [cite:49][cite:67][cite:73].

### ORCA Integration Strategy

- **Coordinator Agent**: Implement hierarchical reasoning framework from ship navigation LLM (cognition → analysis → decision) [cite:48].
- **Knowledge/RAG Agent**: Use expert-guided approach from Compass with Knowledge Tree co-designed with marine scientists [cite:70].
- **Specialized Agents**: Follow multi-agent architecture from Sensorium Arc and MaRAG [cite:51][cite:53].
- **Domain Fine-Tuning**: Consider marine-specific LLM (similar to Llamarine) or fine-tune open-source LLM on marine corpus (OceanPile) [cite:56][cite:59].
- **Uncertainty Estimation**: Leverage ensemble approaches and probabilistic forecasting from FuXi-ONS and marine heatwave models [cite:65][cite:68].

---

## 5. Marine Knowledge Graph Research

### 5.1 Ocean Knowledge Graphs

| Knowledge Graph | Organization | Purpose | Technology | Key Features | ORCA Relevance |
|-----------------|--------------|---------|------------|--------------|----------------|
| **OKG (Ocean Knowledge Graph)** | Academic (IEEE TKDE 2026) | Global SST prediction aligned with observation data | Graph embedding network, LLM alignment with OKG | First systematic OKG for SST prediction, captures sea region characteristics and correlations [cite:46] | **CRITICAL** – Demonstrates OKG-LLM alignment for SST prediction; ORCA can leverage similar approach for multi-parameter reasoning [cite:46] |
| **OSO (Observatories of the Seas Ontology)** | EMSO ERIC (2026) | Improve interoperability of marine observatories | FAIR knowledge graph, semantic technologies | Structures infrastructures, sites, platforms, organisations, activities; machine-actionable data integration [cite:58] | **HIGH** – Provides ontology for marine observatory data; ORCA can use OSO for knowledge representation [cite:58] |
| **Ocean Concept Knowledge Graph** | Academic (OceanPile 2026) | Guide instruction dataset synthesis for marine AI | Hierarchical knowledge graph for ocean science | Supports OceanInstruction dataset creation, enables structured reasoning [cite:56] | **HIGH** – Hierarchical structure supports ORCA's multi-level reasoning (parameter → ecosystem → decision) [cite:56] |

### 5.2 Knowledge Graph Applications in Marine AI

| Application | Paper/System | Key Contribution | ORCA Relevance |
|-------------|--------------|------------------|----------------|
| **OKG-LLM Alignment** | IEEE TKDE 2026 [cite:46] | Aligns ocean knowledge graph with observation data via LLMs for global SST prediction | **CRITICAL** – Directly relevant to ORCA's Knowledge/RAG Agent. OKG-LLM demonstrates how knowledge graphs can ground LLM reasoning in scientific observations [cite:46]. |
| **MaRAG** | ScienceDirect 2026 [cite:53] | Multi-agent framework integrating knowledge graph construction with RAG | **HIGH** – Combines knowledge graph + multi-agent + RAG, similar to ORCA's proposed architecture [cite:53]. |
| **Compass Knowledge Tree** | arXiv 2026 [cite:70] | Expert-guided Knowledge Tree co-designed with marine scientists for data extraction | **CRITICAL** – Demonstrates expert co-design ensures scientific validity; ORCA should adopt similar approach for Coordinator agent reasoning rules [cite:70]. |
| **OceanPile** | Hugging Face 2026 [cite:56] | Large-scale multimodal ocean corpus with knowledge graph-guided instruction dataset | **MODERATE-HIGH** – Provides training data and benchmark for marine AI; ORCA can leverage OceanPile for RAG corpus [cite:56]. |

### Key Insights from Marine Knowledge Graph Research

1. **Knowledge Graphs Ground LLM Reasoning**: OKG-LLM shows that aligning LLMs with structured ocean knowledge improves prediction accuracy and scientific validity [cite:46].

2. **Expert Co-Design is Critical**: Compass's Knowledge Tree was co-designed with marine scientists to ensure scientific correctness [cite:70].

3. **Hierarchical Structure Supports Multi-Level Reasoning**: Ocean Concept Knowledge Graph's hierarchical structure enables reasoning from parameters to ecosystems to decisions [cite:56].

4. **FAIR Principles Enable Interoperability**: OSO follows FAIR (Findable, Accessible, Interoperable, Reusable) principles for marine data integration [cite:58].

### ORCA Integration Strategy

- **Knowledge/RAG Agent**: Build on OKG-LLM approach, aligning LLM with ocean knowledge graph for multi-parameter reasoning [cite:46].
- **Coordinator Agent**: Use Compass-style Knowledge Tree co-designed with marine scientists for reasoning rules [cite:70].
- **Ontology**: Adopt OSO ontology for marine observatory data representation [cite:58].
- **RAG Corpus**: Leverage OceanPile for domain-specific training and retrieval [cite:56].

---

## 6. Multi-Agent Scientific Systems

### 6.1 Multi-Agent Systems in Ocean/Climate Science

| System | Organization | Purpose | Architecture | Key Features | ORCA Relevance |
|--------|--------------|---------|--------------|--------------|----------------|
| **Sensorium Arc** | Academic (arXiv 2025) | Interactive eco-art system for ocean data exploration | Modular multi-agent system, RAG-enhanced LLM | Natural spoken conversation, personifies ocean, blends science with poetics [cite:51] | **HIGH** – Demonstrates multi-agent RAG for ocean data; ORCA can learn from modular agent design [cite:51] |
| **Compass** | Academic (arXiv 2026) | Marine lead data extraction from scientific papers | Expert-guided LLM agent with Knowledge Tree | Task decomposition, verifiable steps, 92% accuracy [cite:70] | **CRITICAL** – Expert-guided agent framework is directly analogous to ORCA; demonstrates scientific validity through expert co-design [cite:70] |
| **MaRAG** | Academic (ScienceDirect 2026) | Intelligent decision support in marine domain | Multi-agent framework + knowledge graph + RAG | Integrates knowledge graph construction with retrieval-augmented generation [cite:53] | **HIGH** – Combines multi-agent + knowledge graph + RAG, similar to ORCA's architecture [cite:53] |
| **EarthLink** | Academic (PMC 2026) | Forecast-to-action framework for Earth science | AI agents investigating drivers, evaluating impacts, proposing strategies | AI not just predicts but reasons about underlying causes and proposes actions [cite:49] | **HIGH** – Similar to ORCA's vision: AI reasoning beyond prediction to decision support [cite:49] |
| **MARINE** | Academic (arXiv 2025) | Improve LLM reasoning through iterative refinement | Multi-agent recursive in-context enhancement | Persistent reference trajectory, minimal batch optimization [cite:50] | **MODERATE-HIGH** – Multi-agent reasoning enhancement; ORCA can explore iterative refinement [cite:50] |

### 6.2 Multi-Agent Systems in Other Scientific Domains

| System | Domain | Purpose | Architecture | Key Features | ORCA Relevance |
|--------|--------|---------|--------------|--------------|----------------|
| **Agentic RAG for Industrial Anomaly Detection** | Industrial IoT | Anomaly detection in industrial systems | Agentic RAG framework | Multi-agent coordination for anomaly detection [cite:47] | **MODERATE** – Agentic RAG pattern applicable to ORCA's anomaly detection (marine heat waves, ecosystem anomalies) |
| **Lighthouse Bot** | Maritime | Evaluate LLMs for maritime data analysis | Platform for LLM evaluation | Benchmarking framework for maritime LLMs [cite:47] | **MODERATE** – Provides evaluation methodology for ORCA's marine LLM components |

### Key Insights from Multi-Agent Scientific Systems

1. **Expert Guidance Ensures Scientific Validity**: Compass demonstrates that expert-guided agents with Knowledge Trees prevent hallucinations and ensure scientific correctness [cite:70].

2. **Modular Multi-Agent Architecture is Effective**: Sensorium Arc and MaRAG use modular multi-agent designs for complex scientific tasks [cite:51][cite:53].

3. **RAG + Knowledge Graph is Powerful Combination**: MaRAG and Compass both integrate RAG with knowledge graphs for structured reasoning [cite:53][cite:70].

4. **Task Decomposition Improves Accuracy**: Compass decomposes complex tasks into verifiable steps, achieving 92% accuracy [cite:70].

5. **Human-in-the-Loop is Critical**: Expert validation and co-design are essential for scientific applications [cite:70].

### ORCA Integration Strategy

- **Coordinator Agent**: Implement Compass-style expert-guided task decomposition with Knowledge Tree [cite:70].
- **Specialized Agents**: Follow modular multi-agent design from Sensorium Arc and MaRAG [cite:51][cite:53].
- **Verification Agent**: Implement multi-layer validation from Compass (AI → expert review) [cite:70].
- **RAG + Knowledge Graph**: Integrate RAG with ocean knowledge graph (OKG-LLM, MaRAG approach) [cite:46][cite:53].

---

## 7. Comparative Analysis and ORCA Relevance

### 7.1 Existing Systems vs. ORCA

| Dimension | Existing Systems | ORCA Proposed Innovation |
|-----------|-----------------|--------------------------|
| **Data Integration** | Single-source or limited multi-source (e.g., PFZ: SST + chlorophyll) [cite:3][cite:8] | Heterogeneous data fusion across ocean, ecosystem, fisheries, safety, geospatial, knowledge domains |
| **Reasoning** | Static rules or single-parameter models [cite:3][cite:8] | Cross-domain collaborative reasoning with specialized agents |
| **Conflict Resolution** | Not addressed (single system output) [cite:3][cite:8] | Explicit conflict detection and resolution between agent outputs |
| **Uncertainty** | Implicit or absent [cite:3][cite:8] | Explicit confidence/uncertainty estimation with evidence attribution |
| **Explainability** | Limited (static advisory format) [cite:3][cite:8] | Explainable decision graph showing reasoning pathway |
| **User Interface** | Map-based visualization or static advisory [cite:3][cite:8][cite:20][cite:21] | Natural-language query + interactive map + reasoning visualization |
| **Temporal Reasoning** | Current + forecast (limited historical comparison) [cite:3][cite:8] | Historical → current → forecast reasoning with anomaly detection |
| **Knowledge Integration** | Separate from data (manual literature review) [cite:3][cite:8] | Integrated RAG + knowledge graph for scientific context |
| **Multi-Agent Architecture** | Single system or no agents [cite:3][cite:8][cite:20][cite:21] | Specialized agents (Ocean, Ecosystem, Fisheries, Safety, Geospatial, Knowledge, Verification) with Coordinator |
| **Decision Intelligence** | Information delivery (human interpretation required) [cite:3][cite:4][cite:8] | Evidence-grounded decision recommendations with reasoning |

### 7.2 Technological and Functional Gaps

Based on comprehensive research, the following gaps exist in current marine information systems:

#### Gap 1: Cross-Domain Reasoning Layer

**Current State**: Existing systems (INCOIS PFZ, Copernicus Marine, NOAA IOOS) provide data and forecasts but require human experts to integrate multiple sources for decision-making [cite:3][cite:8][cite:24][cite:62].

**ORCA Innovation**: Collaborative reasoning layer that automatically integrates heterogeneous data across domains (ocean + ecosystem + fisheries + safety + geospatial) and produces evidence-grounded recommendations [cite:49][cite:70].

**Evidence**: Compass demonstrates expert-guided LLM agents can extract and integrate scientific data with 92% accuracy [cite:70]. EarthLink shows AI can reason about drivers and propose actions, not just predict [cite:49].

#### Gap 2: Agent Conflict Resolution

**Current State**: Single-system outputs (e.g., PFZ advisory) do not address conflicts between different data sources or models [cite:3][cite:8].

**ORCA Innovation**: Explicit conflict detection and resolution between specialized agents (e.g., Fisheries Agent says "favorable" but Safety Agent says "high risk") with evidence-based arbitration.

**Evidence**: Multi-agent systems in other domains (Sensorium Arc, MaRAG) demonstrate agent coordination is feasible [cite:51][cite:53].

#### Gap 3: Uncertainty Quantification with Evidence Attribution

**Current State**: Existing advisories (PFZ) do not provide explicit confidence scores or uncertainty ranges [cite:3][cite:8].

**ORCA Innovation**: Confidence/uncertainty estimation with explicit evidence attribution (data source, parameter, timestamp, value, reasoning).

**Evidence**: FuXi-ONS demonstrates ensemble forecasting for probabilistic ocean prediction [cite:68]. Marine heatwave models show probabilistic forecasting is feasible [cite:65].

#### Gap 4: Explainable Decision Graph

**Current State**: Static advisory formats (PFZ maps, text bulletins) do not show reasoning pathway [cite:3][cite:8].

**ORCA Innovation**: Visual decision graph showing how parameters (SST, chlorophyll, currents, waves, wind) contribute to final recommendation.

**Evidence**: Compass demonstrates task decomposition into verifiable steps with expert validation [cite:70].

#### Gap 5: Natural-Language Query with Scientific Grounding

**Current State**: Users must navigate multiple portals (INCOIS, MOSDAC, WebGIS) and interpret technical visualizations [cite:3][cite:8][cite:31][cite:32].

**ORCA Innovation**: Natural-language query interface ("Which area near Chennai has better fishing potential tomorrow morning?") with scientifically grounded responses.

**Evidence**: Sensorium Arc demonstrates conversational AI for ocean data exploration [cite:51]. Llamarine shows domain-specific LLMs outperform general LLMs for maritime tasks [cite:59].

#### Gap 6: Integrated Knowledge Retrieval

**Current State**: Scientific literature, government documents, and marine guidelines are separate from operational data systems [cite:3][cite:8].

**ORCA Innovation**: RAG Agent integrates scientific papers, government documents, and marine guidelines with operational data for context-aware reasoning.

**Evidence**: Compass extracts 3,751 new records from 230,000 papers using expert-guided LLM agents [cite:70]. OceanPile provides multimodal corpus for marine AI [cite:56].

### 7.3 ORCA Differentiation Summary

**ORCA is NOT simply:**
- Another marine data portal (Copernicus Marine, MOSDAC already exist) [cite:24][cite:31][cite:61]
- Another PFZ advisory system (INCOIS PFZ already operational) [cite:3][cite:8]
- Another marine map (INCOIS WebGIS, Copernicus MyOcean Viewer exist) [cite:20][cite:21]
- Another LLM chatbot (Llamarine, Sensorium Arc exist) [cite:51][cite:59]

**ORCA IS proposing:**
- **Collaborative reasoning layer** integrating heterogeneous data across domains [cite:49][cite:70]
- **Multi-agent architecture** with specialized agents for ocean, ecosystem, fisheries, safety, geospatial, knowledge [cite:51][cite:53][cite:70]
- **Conflict resolution** between agents with evidence-based arbitration
- **Uncertainty quantification** with confidence scores and evidence attribution [cite:65][cite:68]
- **Explainable decision graphs** showing reasoning pathway [cite:70]
- **Natural-language interface** with scientific grounding [cite:51][cite:59]
- **Integrated knowledge retrieval** from scientific literature and operational data [cite:56][cite:70]

**Key Innovation**: The integration of these components into a single evidence-grounded reasoning workflow, not the individual technologies themselves.

---

## 8. References

### Primary Sources

1. INCOIS PFZ Advisory – https://www.incois.gov.in/incois/adv_pfz.aspx [cite:2][cite:3][cite:8][cite:12][cite:13]
2. ISRO EOS-06/Oceansat-3 – https://www.isro.gov.in/EOS-06.html [cite:4][cite:39][cite:43]
3. MOSDAC – https://mosdac.gov.in/ [cite:31][cite:32][cite:45]
4. NASA Ocean Color – https://www.earthdata.nasa.gov/centers/ob-daac [cite:33][cite:34][cite:36][cite:40][cite:41][cite:42][cite:44]
5. NOAA IOOS – https://ioos.noaa.gov/ [cite:22][cite:62]
6. Copernicus Marine Service – https://data.marine.copernicus.eu/ [cite:16][cite:17][cite:18][cite:19][cite:20][cite:21][cite:23][cite:24][cite:25][cite:26][cite:27][cite:61][cite:74]
7. e-Samudra – https://esamudra.gov.in/ [cite:1][cite:5][cite:14][cite:15]

### Research Papers (2024–2026)

8. OKG-LLM: Aligning Ocean Knowledge Graph With Observation Data via LLMs – IEEE TKDE 2026 [cite:46]
9. Compass: Navigating Global Marine Lead Data Integration through Expert-Guided LLM Agent – arXiv 2026 [cite:70]
10. Sensorium Arc: AI Agent System for Oceanic Data Exploration – arXiv 2025 [cite:51]
11. MaRAG: Multi-agent framework with knowledge graph + RAG – ScienceDirect 2026 [cite:53]
12. FuXi-ONS: Machine-learning ensemble forecasting for global ocean – arXiv 2026 [cite:68]
13. OceanLight: Efficient global ocean forecasting via geometry-adaptive unstructured mesh – arXiv 2026 [cite:71]
14. Marine heatwave prediction with hybrid physics-AI – Springer 2025 [cite:65]
15. MSSTN: Multiscale spatiotemporal network for marine environment prediction – Nature 2025 [cite:63]
16. SeaCast: Graph-based deep learning for Mediterranean forecasting – Nature 2025 [cite:64]
17. Hybrid physics-AI coupled ocean models – arXiv 2025 [cite:67]
18. Hybrid ensemble forecasting with spectral nudging – arXiv 2026 [cite:69]
19. Llamarine: Open-source maritime industry-specific LLM – 2026 [cite:59]
20. Ship navigation LLM with hierarchical reasoning – 2025 [cite:48]
21. COLREG compliance LLM evaluation – arXiv 2026 [cite:52]
22. Small LLMs on edge devices for maritime applications – Sensors 2026 [cite:55]
23. Agentic RAG for Maritime AIoT – PMC 2026 [cite:47]
24. MARINE: Multi-Agent Recursive IN-context Enhancement – arXiv 2025 [cite:50]
25. AI for atmosphere-ocean sciences review – PMC 2026 [cite:49]
26. OceanPile: Large-scale multimodal ocean corpus – Hugging Face 2026 [cite:56]
27. OSO: Observatories of the Seas Ontology – EMSO 2026 [cite:58]
28. GLONET: AI-driven global ocean forecasting – Mercator Ocean 2025 [cite:74]

### News and Reports

29. The Hindu (2026): INCOIS advisory helps fishermen net Hilsa bonanza [cite:2]
30. BusinessWorld (2026): The Sea Has No Signboards, ISRO Built One [cite:4]
31. Frontiers in Marine Science (2026): Development and deployment of pilot multilingual citizen [cite:3]
32. The Week (2026): Shipping ministry launches flagship e-Samudra platform [cite:5]
33. IOCCG (2026): August 2026 News – Oceansat-3 mission overview [cite:43]

---

## Document Notes

**Citation Format**: [cite:X] refers to the numbered search result from the research phase.

**Research Limitations**:
- INCOIS WebGIS specific technical details not fully documented in publicly available sources.
- INCOIS SAMUDRA requires clarification (multiple systems use similar names).
- Some research papers are preprints (arXiv) and not yet peer-reviewed.

**Recommended Next Steps**:
1. Direct consultation with INCOIS for SAMUDRA and WebGIS technical specifications.
2. Validation of data API availability for ISRO/INCOIS products.
3. Expert review of proposed reasoning rules with marine scientists.
4. Prototype development with focused Bay of Bengal/Arabian Sea use case.