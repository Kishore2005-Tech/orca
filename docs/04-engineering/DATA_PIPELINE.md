# DATA_PIPELINE.md

## ORCA – Marine Ecosystems Reasoning with Collaborative Agents  
**SIH26176 | ISRO | Data Pipeline Specification**

***

## 1. Overview

This document specifies the ORCA data pipeline architecture, from source ingestion to agent-ready feature generation. The pipeline handles heterogeneous marine data (satellite, model, forecast, in-situ) with rigorous quality control, spatial/temporal alignment, and scientific validation per SCIENTIFIC_RULES.md.

**Pipeline Stages**:
1. Data Source
2. Ingestion
3. Parsing
4. Validation
5. Quality Control
6. Normalization
7. Spatial Alignment
8. Temporal Alignment
9. Storage
10. Feature Generation
11. Agent Tools

**Design Principles**:
- **Authoritative Sources Only**: ISRO, MOSDAC, INCOIS, NASA, NOAA, Copernicus, peer-reviewed products [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
- **Quality-First**: Quality flags, uncertainty bounds, provenance metadata at every stage
- **Reproducible**: Logging, caching, versioned datasets for audit trail
- **Scalable**: Prototype (single-node, file-based) → Production (distributed, cloud-native)

***

## 2. Data Sources

### 2.1 Supported Data Sources

| Source | Data Type | Format | Access Method | Latency | Coverage |
|--------|-----------|--------|---------------|---------|----------|
| **ISRO/MOSDAC** | OCM chlorophyll, SST | NetCDF, HDF5, GeoTIFF | API (MOSDAC OPeNDAP), FTP | 1–3 days | Indian Ocean |
| **INCOIS** | PFZ advisories, OSF (wave, wind), High Wave Alert | GeoJSON, NetCDF, CSV | API (INCOIS WebGIS), FTP | Daily (OSF), Thrice weekly (PFZ) | Indian Ocean |
| **NASA (PO.DAAC)** | MODIS SST, chlorophyll, SSH | NetCDF, HDF5 | API (Earthdata Search), FTP | 1–4 days (L4 SST) | Global |
| **NOAA** | AVHRR SST, MHW monitoring | NetCDF, HDF5 | API (NOAA CoastWatch), FTP | 1–2 days | Global |
| **Copernicus Marine** | SST, chlorophyll, SSH, currents, SSS, productivity | NetCDF, Zarr | API (CMEMS MyOcean), FTP | 1–7 days (product-dependent) | Global |
| **GEBCO** | Bathymetry, land/sea mask | NetCDF, GeoTIFF | FTP, direct download | Static | Global |
| **In-Situ (Argo, Buoys)** | SST, SSS, subsurface profiles | NetCDF, CSV | API (Argo GDAC, NCEI) | 1–7 days | Sparse, global |

**TBD – Requires Team Decision**:
- Priority sources for MVP (recommend: INCOIS PFZ + OSF, MOSDAC OCM, NASA MODIS SST)
- Authentication requirements (CMEMS requires registration; Earthdata requires login)
- Rate limits and quota management for API access

### 2.2 Data Categories

1. **Observation**: Satellite/measured data (SST, chlorophyll, SSH, wind, waves) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **Model**: Derived/modelled data (currents, MLD, productivity, SSS) [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
3. **Forecast**: Predicted future state (OSF wave/wind forecast, PFZ drift) 
4. **Climatology**: Long-term baseline (30-year SST climatology for MHW) 
5. **Advisories**: PFZ, High Wave Alert, marine hazard warnings [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

***

## 3. Ingestion

### 3.1 API Ingestion

**Supported Protocols**:
- **OPeNDAP** (MOSDAC, NASA, NOAA): Direct subset extraction via URL
- **REST API** (INCOIS, CMEMS): JSON/GeoJSON responses
- **FTP/SFTP** (GEBCO, NASA PODAAC): Bulk file download
- **OData** (CMEMS): Structured query interface

**Ingestion Workflow**:
1. **Authenticate**: Use API keys/tokens (stored in environment variables, not code)
2. **Query**: Construct URL with parameters (bbox, time range, variables)
3. **Download**: Stream data to temporary storage (avoid memory overload)
4. **Retry**: Exponential backoff (1s, 2s, 4s, 8s, max 5 retries) for transient failures
5. **Log**: Record source, timestamp, URL, status code, file size, checksum

**Example (MOSDAC OPeNDAP)**:
```python
url = "https://mosdac.opendap.org/ocm_chl.nc?bbox=10,75,15,80&time=2026-08-31"
response = requests.get(url, auth=(API_KEY, ""), stream=True)
with open("temp/ocm_chl_20260831.nc", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

**Error Handling**:
- **4xx (Client Error)**: Log error, skip source, notify user (e.g., "MOSDAC API returned 404: data not available")
- **5xx (Server Error)**: Retry with exponential backoff; if all retries fail, mark source as unavailable
- **Timeout**: Set timeout (30s for API, 300s for large file downloads); retry on timeout

### 3.2 File Ingestion

**Supported Formats**:
- **Raster**: NetCDF, HDF5, GeoTIFF, GRIB (for model/forecast data)
- **Tabular**: CSV, JSON, GeoJSON (for advisories, in-situ data)
- **Vector**: Shapefile, GeoJSON (for PFZ boundaries, bathymetry contours)

**Ingestion Workflow**:
1. **Detect Format**: Use file extension + magic bytes (e.g., `netcdf4` library for NetCDF)
2. **Validate Structure**: Check required variables/attributes (e.g., NetCDF must have `lat`, `lon`, `time`, `chl_a`)
3. **Extract Metadata**: Source, timestamp, resolution, units, quality flags
4. **Copy to Staging**: Move to `staging/` directory for processing

**Example (NetCDF Validation)**:
```python
import xarray as xr

ds = xr.open_dataset("staging/ocm_chl.nc")
required_vars = ["lat", "lon", "time", "chl_a"]
assert all(v in ds.variables for v in required_vars), "Missing required variables"
```

**TBD – Requires Team Decision**:
- Maximum file size for MVP (recommend: 1 GB per file; larger files require chunked processing)
- Supported compression formats (gzip, bzip2, xz for tabular data)

***

## 4. Parsing

### 4.1 Raster Data Parsing

**Tools**: `xarray`, `netcdf4`, `rasterio`, `h5py`

**Parsing Steps**:
1. **Load Dataset**: Open NetCDF/HDF5 with `xarray.open_dataset()`
2. **Extract Variables**: Select required variables (e.g., `sst`, `chl_a`, `ssh`)
3. **Read Attributes**: Extract units, scale factors, fill values, quality flags
4. **Apply Scale/Offset**: Convert packed integers to physical values (e.g., `sst = sst_scaled * 0.01 + 273.15`)
5. **Mask Fill Values**: Replace `_FillValue` or `missing_value` with `NaN`

**Example**:
```python
ds = xr.open_dataset("staging/modis_sst.nc")
sst = ds["sst"] * ds["sst"].scale_factor + ds["sst"].add_offset
sst = sst.where(sst != ds["sst"]._FillValue)
```

### 4.2 Tabular Data Parsing

**Tools**: `pandas`, `geopandas`

**Parsing Steps**:
1. **Load CSV/JSON**: Use `pd.read_csv()` or `pd.read_json()`
2. **Parse Timestamps**: Convert string timestamps to `datetime64[ns]` (UTC)
3. **Validate Columns**: Check required columns (e.g., `latitude`, `longitude`, `time`, `value`)
4. **Convert Units**: Standardize units (e.g., km/h → m/s for wind)
5. **Handle Missing Values**: Mark as `NaN`; log missing value percentage

**Example (INCOIS PFZ CSV)**:
```python
pfz = pd.read_csv("staging/incois_pfz.csv")
pfz["time"] = pd.to_datetime(pfz["time"], utc=True)
assert all(col in pfz.columns for col in ["lat", "lon", "time", "pfz_flag"])
```

### 4.3 Geospatial Data Parsing

**Tools**: `geopandas`, `rasterio`, `pyproj`

**Parsing Steps**:
1. **Load Vector Data**: Use `gpd.read_file()` for Shapefile/GeoJSON
2. **Reproject to WGS84**: Convert to EPSG:4326 (if not already)
3. **Validate Geometry**: Check for invalid geometries (self-intersections, NaN coordinates)
4. **Extract Attributes**: Parse metadata (e.g., PFZ validity period, source)

**Example**:
```python
import geopandas as gpd

pfz_gdf = gpd.read_file("staging/incois_pfz.geojson")
pfz_gdf = pfz_gdf.to_crs("EPSG:4326")
assert pfz_gdf.geometry.is_valid.all(), "Invalid geometries detected"
```

***

## 5. Validation

### 5.1 Structural Validation

**Checks**:
- **Required Variables**: Ensure all expected variables are present (e.g., `lat`, `lon`, `time`, `sst`)
- **Dimension Consistency**: Verify dimensions match (e.g., `lat` length = 1000, `lon` length = 2000)
- **Attribute Presence**: Check for required attributes (e.g., `units`, `standard_name`, `calendar`)
- **Data Type**: Validate variable types (e.g., `sst` is float32, `time` is datetime64)

**Example**:
```python
def validate_structure(ds, required_vars):
    missing = [v for v in required_vars if v not in ds.variables]
    if missing:
        raise ValueError(f"Missing required variables: {missing}")
```

### 5.2 Semantic Validation

**Checks**:
- **Coordinate Ranges**: Latitude [-90, 90], Longitude [-180, 180] or[0][360]
- **Physical Bounds**: SST [-2, 35]°C, chlorophyll  mg/m³, SSH [-2, 2] m[0][50]
- **Temporal Consistency**: Timestamps are monotonic, within expected range (e.g., not year 1970)
- **Unit Consistency**: Units match expected (e.g., SST in °C or K, not °F)

**Example**:
```python
assert ds["lat"].min() >= -90 and ds["lat"].max() <= 90, "Latitude out of bounds"
assert ds["sst"].min() >= -2 and ds["sst"].max() <= 35, "SST out of physical bounds"
```

### 5.3 Provenance Validation

**Checks**:
- **Source Attribution**: Verify source metadata (e.g., `source="INCOIS"`, `product="PFZ"`)
- **Timestamp**: Ensure acquisition time is present and valid
- **Version**: Check product version (e.g., `version="4.1"` for MUR SST)
- **DOI/URL**: Validate citation information (if available)

**Logging**:
- Record source, timestamp, version, DOI for audit trail
- Flag missing provenance metadata (e.g., "WARNING: No source attribute found in SST file")

***

## 6. Quality Control

### 6.1 Quality Flags

**Flag Types**:
- **Cloud Contamination**: Satellite pixels obscured by clouds (flag = 1)
- **Sun Glint**: Reflectance artifacts from sun angle (flag = 2)
- **Atmospheric Correction Failure**: Algorithm failed to retrieve value (flag = 3)
- **Land/Ice Contamination**: Pixel partially over land/ice (flag = 4)
- **Algorithm Failure**: Retrieval algorithm error (flag = 5)
- **Quality Level**: 0–4 (4 = best, 0 = worst) 

**Handling**:
- **Mask Low Quality**: Exclude pixels with quality level < 3 (for operational use)
- **Flag to User**: Report quality issues (e.g., "Chlorophyll data quality reduced due to sun glint")
- **Log Flag Distribution**: Record percentage of pixels with each flag type

**Example (MODIS Chlorophyll)**:
```python
chl = ds["chl_a"]
quality = ds["quality_level"]
chl_masked = chl.where(quality >= 3)  # Exclude low-quality pixels
```

### 6.2 Missing Values

**Detection**:
- **Fill Values**: Check for `_FillValue`, `missing_value`, `NaN`
- **Percentage**: Calculate missing value percentage per variable
- **Spatial Pattern**: Identify spatial clusters of missing data (e.g., cloud gaps)

**Handling**:
- **Mark as NaN**: Replace fill values with `NaN` for consistent handling
- **Log Missing Rate**: Record missing percentage (e.g., "Chlorophyll: 15% missing due to clouds")
- **Interpolation (Optional)**: For small gaps (<10%), use spatial interpolation (e.g., nearest-neighbor, kriging)
- **Flag Large Gaps**: If missing > 30%, mark dataset as "incomplete" and reduce confidence

**TBD – Requires Team Decision**:
- Interpolation method for small gaps (recommend: nearest-neighbor for MVP)
- Threshold for "large gaps" (recommend: 30% missing → reduce confidence)

### 6.3 Outliers

**Detection**:
- **Physical Bounds**: Values outside expected range (e.g., SST > 35°C in open ocean)
- **Statistical Outliers**: Values > 3σ from mean (per region/season)
- **Spatial Outliers**: Pixels significantly different from neighbors (e.g., SST gradient > 5°C/km)

**Handling**:
- **Flag Outliers**: Mark outliers with special flag (e.g., `outlier_flag = 1`)
- **Clip to Bounds**: For physical bounds violations, clip to valid range (e.g., SST = 35°C if > 35°C)
- **Investigate**: Log outliers for manual review (e.g., "WARNING: SST = 40°C at 12°N, 78°E; possible artifact")

**Example**:
```python
sst_outliers = (sst > 35) | (sst < -2)
sst_clipped = sst.clip(-2, 35)
```

### 6.4 Stale Data

**Freshness Thresholds** (per SCIENTIFIC_RULES.md Section 11.1):

| Data Type | Maximum Age | Action if Stale |
|-----------|-------------|-----------------|
| SST (dynamic features) | 48 hours | Flag as "stale"; reduce confidence |
| Chlorophyll | 48 hours | Flag as "stale"; reduce confidence |
| PFZ Advisory | Valid period (24–48 hours)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | Do not use beyond validity |
| OSF Forecast | Within forecast window (5–7 days)  | Use only within window |
| Bathymetry | No expiration (static)  | No action needed |
| Climatology | 30-year period  | No action needed |

**Handling**:
- **Check Timestamp**: Compare acquisition time to current time
- **Flag Stale**: Mark dataset with `is_stale = True` if beyond threshold
- **Reduce Confidence**: Downgrade confidence level (e.g., High → Medium) if stale
- **Notify User**: Report staleness (e.g., "SST data is 5 days old; front location may have shifted")

**Example**:
```python
from datetime import timedelta

max_age = timedelta(hours=48)
is_stale = (current_time - acquisition_time) > max_age
```

***

## 7. Normalization

### 7.1 Unit Normalization

**Standard Units**:
- **SST**: Degrees Celsius (°C)
- **Chlorophyll-a**: Milligrams per cubic meter (mg/m³)
- **SSH**: Meters (m)
- **Currents**: Meters per second (m/s)
- **Wind**: Meters per second (m/s)
- **Wave Height**: Meters (m)
- **MLD**: Meters (m)
- **Bathymetry**: Meters (m)
- **Salinity (SSS)**: Practical Salinity Units (PSU)

**Conversion**:
- **Temperature**: Kelvin → °C (`T_c = T_k - 273.15`)
- **Speed**: km/h → m/s (`v_ms = v_kmh / 3.6`)
- **Depth**: Kilometers → meters (`d_m = d_km * 1000`)

**Example**:
```python
sst_c = sst_k - 273.15  # Convert Kelvin to Celsius
wind_ms = wind_kmh / 3.6  # Convert km/h to m/s
```

### 7.2 Coordinate Normalization

**Standard CRS**: WGS84 (EPSG:4326)

**Conversion**:
- **Latitude**: Ensure range [-90, 90]
- **Longitude**: Convert  → [-180, 180] if needed (`lon = lon - 360 if lon > 180 else lon`)[0][360]
- **Reprojection**: Use `pyproj` or `rasterio` to reproject to EPSG:4326

**Example**:
```python
def normalize_longitude(lon):
    return lon - 360 if lon > 180 else lon

lon_normalized = normalize_longitude(ds["lon"])
```

### 7.3 Timestamp Normalization

**Standard Timezone**: UTC

**Conversion**:
- **Parse Timezone**: Convert all timestamps to UTC (e.g., IST → UTC: `utc_time = ist_time - 5.5 hours`)
- **Standard Format**: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`)
- **Handle Time Calendars**: For model data with non-standard calendars (e.g., `noleap`, `360_day`), convert to standard Gregorian

**Example**:
```python
import pytz

ist = pytz.timezone("Asia/Kolkata")
utc = pytz.utc

ist_time = ist.localize(datetime(2026, 8, 31, 15, 30))
utc_time = ist_time.astimezone(utc)
```

***

## 8. Spatial Alignment

### 8.1 Grid Standardization

**Target Grid**:
- **Resolution**: 0.01° (~1 km) for MVP (balance between detail and performance)
- **Extent**: Indian Ocean domain (lat:, lon: ) for MVP; global for production[0][30][60][100]
- **Projection**: WGS84 (EPSG:4326)

**Resampling**:
- **Nearest-Neighbor**: For categorical data (e.g., quality flags, PFZ binary mask)
- **Bilinear**: For continuous data (e.g., SST, chlorophyll, SSH)
- **Conservative**: For fluxes (e.g., wind stress, heat flux)

**Example (xarray)**:
```python
target_lat = np.arange(0, 30, 0.01)
target_lon = np.arange(60, 100, 0.01)

sst_resampled = ds["sst"].interp(lat=target_lat, lon=target_lon, method="linear")
```

### 8.2 Coastal Masking

**Land/Sea Mask**:
- **Source**: GEBCO 15 arc-sec bathymetry 
- **Threshold**: Depth > 0 m = ocean; Depth ≤ 0 m = land
- **Application**: Mask land pixels in all datasets (set to `NaN`)

**Example**:
```python
bathymetry = xr.open_dataset("gebco_2023.nc")["elevation"]
land_mask = bathymetry <= 0

sst_masked = sst.where(~land_mask)
```

### 8.3 Resolution Consistency

**Rule**: Do not infer sub-grid features (e.g., claim 100 m precision from 4 km data) 

**Handling**:
- **Flag Native Resolution**: Record native resolution for each dataset (e.g., `sst_resolution = 4 km`)
- **Aggregate to Coarsest**: When combining datasets, aggregate to coarsest resolution (e.g., 4 km SST + 1 km chlorophyll → 4 km grid)
- **Warn User**: Report resolution mismatch (e.g., "SST resolution: 4 km; chlorophyll resolution: 1 km; output resolution: 4 km")

***

## 9. Temporal Alignment

### 9.1 Time Standardization

**Standard Timezone**: UTC

**Steps**:
1. **Convert to UTC**: All timestamps to UTC (see Section 7.3)
2. **Round to Common Frequency**: Round to nearest hour/day (e.g., 14:32 → 14:00 for hourly, 2026-08-31 → 2026-09-01 for daily)
3. **Align Datasets**: Interpolate/extrapolate to common time grid (e.g., daily SST + 3-hourly wind → daily grid)

**Example**:
```python
# Round to nearest day
ds["time"] = ds["time"].dt.round("D")

# Resample to daily mean
sst_daily = sst.resample(time="1D").mean()
```

### 9.2 Temporal Interpolation

**Methods**:
- **Nearest-Neighbor**: For categorical data (e.g., PFZ binary mask)
- **Linear**: For continuous data (e.g., SST, SSH)
- **Forward-Fill**: For forecasts (e.g., OSF wave height forecast)

**Constraints**:
- **Maximum Gap**: Do not interpolate gaps > 3 days (flag as "data gap")
- **Extrapolation**: Do not extrapolate beyond forecast window (e.g., OSF 5-day forecast → do not use day 6+)

**Example**:
```python
# Linear interpolation for SST gaps < 3 days
sst_interpolated = sst.interpolate_na(dim="time", method="linear", max_gap=3)
```

### 9.3 Forecast Validity

**Forecast Windows**:
- **OSF (INCOIS)**: 5–7 days, 3-hourly intervals 
- **PFZ Drift**: 24–48 hours (features shift with wind/currents) [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)

**Handling**:
- **Check Validity Period**: Compare current time to forecast valid period
- **Truncate**: Exclude forecast points beyond valid window
- **Flag Expiring**: Warn user if forecast expires soon (e.g., "PFZ advisory expires in 12 hours")

***

## 10. Storage

### 10.1 Storage Architecture

**Prototype (MVP)**:
- **Format**: NetCDF (for raster), Parquet (for tabular), GeoJSON (for vector)
- **Location**: Local filesystem (`data/processed/`)
- **Organization**:
  ```
  data/
  ├── raw/           # Original downloaded files
  ├── staging/       # Parsed, validated files
  ├── processed/     # Normalized, aligned datasets
  ├── features/      # Agent-ready features
  └── cache/         # Cached intermediate results
  ```

**Production**:
- **Format**: Zarr (for raster), Parquet (for tabular), PostGIS (for vector)
- **Location**: Cloud storage (AWS S3, Google Cloud Storage)
- **Organization**:
  ```
  s3://orca-data/
  ├── raw/
  ├── staging/
  ├── processed/
  ├── features/
  └── cache/
  ```

**TBD – Requires Team Decision**:
- Cloud provider for production (recommend: AWS S3 for MVP compatibility)
- Database for metadata (recommend: PostgreSQL + PostGIS for geospatial queries)

### 10.2 Metadata Storage

**Metadata Schema**:
```json
{
  "source": "INCOIS",
  "product": "PFZ",
  "timestamp": "2026-08-31T00:00:00Z",
  "resolution": "0.01°",
  "units": "binary (0/1)",
  "quality_flags": {
    "cloud": 0.05,
    "sun_glint": 0.02,
    "missing": 0.08
  },
  "is_stale": false,
  "valid_until": "2026-09-01T00:00:00Z",
  "doi": "TBD",
  "url": "https://incois.gov.in/MarineFisheries/PfzAdvisory"
}
```

**Storage**:
- **Sidecar Files**: Store metadata as JSON alongside data files (e.g., `sst.nc` + `sst.json`)
- **Database**: For production, store metadata in PostgreSQL for queryable access

### 10.3 Caching

**Cache Strategy**:
- **Key**: Hash of (source, product, time_range, bbox)
- **TTL**: 24 hours for dynamic data (SST, chlorophyll), 30 days for static data (bathymetry, climatology)
- **Invalidation**: Clear cache if source data is updated (check timestamp/version)

**Example**:
```python
import hashlib

cache_key = hashlib.md5(f"INCOIS:PFZ:2026-08-31:10,75,15,80".encode()).hexdigest()
cache_path = f"cache/{cache_key}.nc"

if os.path.exists(cache_path) and not is_expired(cache_path, ttl=24*3600):
    ds = xr.open_dataset(cache_path)
else:
    ds = ingest_and_process(...)
    ds.to_netcdf(cache_path)
```

***

## 11. Feature Generation

### 11.1 Derived Features

**Features for Agents**:

| Feature | Description | Input Data | Output Type |
|---------|-------------|------------|-------------|
| **SST Gradient** | SST spatial gradient (°C/km) | SST | Raster (float) |
| **Chlorophyll Gradient** | Chlorophyll spatial gradient (mg/m³/km) | Chlorophyll | Raster (float) |
| **Front Mask** | Binary mask for ocean fronts (SST + chlorophyll gradients)  | SST, chlorophyll | Raster (binary) |
| **MHW Mask** | Binary mask for marine heatwaves (SST > 90th percentile for ≥5 days)  | SST, climatology | Raster (binary) |
| **PFZ Mask** | Binary mask for Potential Fishing Zones (INCOIS methodology)  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | SST, chlorophyll, bathymetry | Raster (binary) |
| **Upwelling Index** | Indicator for upwelling (cold SST + high chlorophyll)  | SST, chlorophyll | Raster (float) |
| **Eddy Detection** | SSH anomaly + gradient for eddy identification  | SSH | Raster (binary) |
| **Habitat Suitability** | Combined index (SST, chlorophyll, bathymetry, fronts) | SST, chlorophyll, bathymetry, fronts | Raster (float) |
| **Wave Risk** | Categorized wave height (Low: <2.5 m, Watch: 2.5–3.0 m, Alert: >3.0 m)  | Wave height | Raster (categorical) |
| **PFZ Drift** | Predicted PFZ shift (km/day) using wind/currents  [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory) | PFZ, wind, currents | Vector (displacement) |

**Example (SST Gradient)**:
```python
import numpy as np

def compute_gradient(field, dx=1.0):
    """Compute spatial gradient (per km)"""
    grad_y, grad_x = np.gradient(field, dx)
    gradient = np.sqrt(grad_x**2 + grad_y**2)
    return gradient

sst_gradient = compute_gradient(sst, dx=1.0)  # dx = 1 km
```

### 11.2 Feature Storage

**Format**:
- **Raster Features**: NetCDF/Zarr (with coordinates, time, attributes)
- **Vector Features**: GeoJSON/PostGIS (for PFZ boundaries, drift vectors)

**Naming Convention**:
- `{source}_{product}_{feature}_{resolution}_{timestamp}.{ext}`
- Example: `incois_pfz_front_mask_0.01deg_20260831.nc`

**Metadata**:
- Include feature description, input data, algorithm, uncertainty bounds

***

## 12. Agent Tools

### 12.1 Tool Interface

**Agent Tool API**:
```python
def get_feature(feature_name: str, bbox: Tuple[float, float, float, float], time_range: Tuple[datetime, datetime]) -> xr.Dataset:
    """
    Retrieve feature for agents.

    Parameters:
    - feature_name: e.g., "sst", "chl_gradient", "pfz_mask"
    - bbox: (lat_min, lon_min, lat_max, lon_max)
    - time_range: (start_time, end_time)

    Returns:
    - xr.Dataset with feature data, coordinates, metadata
    """
```

**Example Usage (Ocean Agent)**:
```python
sst = get_feature("sst", bbox=(10, 75, 15, 80), time_range=(datetime(2026, 8, 31), datetime(2026, 8, 31)))
sst_gradient = get_feature("sst_gradient", bbox=(10, 75, 15, 80), time_range=(datetime(2026, 8, 31), datetime(2026, 8, 31)))
```

### 12.2 Available Tools

| Tool | Description | Input | Output |
|------|-------------|-------|--------|
| `get_sst` | Retrieve SST data | bbox, time_range | xr.Dataset (sst, lat, lon, time) |
| `get_chlorophyll` | Retrieve chlorophyll data | bbox, time_range | xr.Dataset (chl_a, lat, lon, time) |
| `get_ssh` | Retrieve SSH data | bbox, time_range | xr.Dataset (ssh, lat, lon, time) |
| `get_wind` | Retrieve wind data | bbox, time_range | xr.Dataset (wind_speed, wind_dir, lat, lon, time) |
| `get_waves` | Retrieve wave height data | bbox, time_range | xr.Dataset (hs, lat, lon, time) |
| `get_pfz` | Retrieve PFZ mask | bbox, time_range | xr.Dataset (pfz_mask, lat, lon, time) |
| `get_fronts` | Retrieve front mask | bbox, time_range | xr.Dataset (front_mask, lat, lon, time) |
| `get_mhw` | Retrieve MHW mask | bbox, time_range | xr.Dataset (mhw_mask, lat, lon, time) |
| `get_bathymetry` | Retrieve bathymetry | bbox | xr.Dataset (depth, lat, lon) |
| `get_currents` | Retrieve current data | bbox, time_range | xr.Dataset (u, v, lat, lon, time) |
| `get_wave_risk` | Retrieve categorized wave risk | bbox, time_range | xr.Dataset (wave_risk, lat, lon, time) |
| `get_pfz_drift` | Retrieve PFZ drift vector | bbox, time_range | gpd.GeoDataFrame (drift_vector, geometry) |

### 12.3 Tool Implementation

**Example (`get_sst`)**:
```python
def get_sst(bbox, time_range):
    """Retrieve SST data from processed storage."""
    lat_min, lon_min, lat_max, lon_max = bbox
    start_time, end_time = time_range

    # Query processed SST files
    files = find_files("processed", "sst", bbox, time_range)

    if not files:
        raise ValueError("No SST data available for specified bbox/time")

    # Load and concatenate
    datasets = [xr.open_dataset(f) for f in files]
    ds = xr.concat(datasets, dim="time")

    # Subset to bbox
    ds = ds.sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))

    return ds
```

***

## 13. Prototype vs Production Pipeline

### 13.1 Prototype (MVP)

**Characteristics**:
- **Scale**: Single-node, local filesystem
- **Data Volume**: < 100 GB total
- **Ingestion**: Manual or cron-based (no real-time streaming)
- **Processing**: Sequential (no parallelization)
- **Storage**: NetCDF/Parquet on local disk
- **Caching**: Simple file-based cache (`cache/` directory)
- **Logging**: File-based logs (`logs/pipeline.log`)
- **Monitoring**: Manual inspection (no automated alerts)

**Tools**:
- **Ingestion**: `requests`, `ftplib`
- **Parsing**: `xarray`, `pandas`, `geopandas`
- **Processing**: `numpy`, `scipy`
- **Storage**: `netcdf4`, `pyarrow`
- **Logging**: `logging` module

**Limitations**:
- Not scalable to large datasets (> 100 GB)
- No fault tolerance (single point of failure)
- Manual intervention required for errors
- Limited concurrency (sequential processing)

### 13.2 Production

**Characteristics**:
- **Scale**: Distributed, cloud-native (AWS/GCP)
- **Data Volume**: > 1 TB total
- **Ingestion**: Event-driven (S3 triggers, message queues)
- **Processing**: Parallel (Dask, Spark, Kubernetes)
- **Storage**: Zarr (object storage), PostGIS (database)
- **Caching**: Redis/Memcached for metadata, S3 for data
- **Logging**: Centralized logging (ELK stack, CloudWatch)
- **Monitoring**: Automated alerts (Prometheus, Grafana)

**Tools**:
- **Ingestion**: AWS Lambda, Apache Kafka, Airflow
- **Parsing**: Dask, Spark (for large datasets)
- **Processing**: Dask, Xarray-Distributed
- **Storage**: AWS S3, Google Cloud Storage, PostgreSQL + PostGIS
- **Caching**: Redis, Memcached
- **Logging**: ELK stack (Elasticsearch, Logstash, Kibana), CloudWatch
- **Monitoring**: Prometheus, Grafana, PagerDuty

**Scalability**:
- **Horizontal Scaling**: Add more nodes for parallel processing
- **Data Partitioning**: Partition by time, region for efficient querying
- **Load Balancing**: Distribute ingestion/processing across nodes

**TBD – Requires Team Decision**:
- Production cloud provider (recommend: AWS for MVP compatibility)
- Orchestration framework (recommend: Airflow for workflow, Kubernetes for deployment)
- Monitoring/alerting thresholds (e.g., ingestion failure rate > 5% → alert)

***

## 14. Error Handling and Logging

### 14.1 Error Handling

**Error Types**:
- **Ingestion Errors**: API failures, FTP connection errors, file corruption
- **Parsing Errors**: Missing variables, invalid formats, type mismatches
- **Validation Errors**: Out-of-bounds values, missing metadata, timestamp issues
- **Processing Errors**: Memory overflow, numerical errors, algorithm failures

**Handling Strategy**:
- **Retry**: For transient errors (API timeouts, network failures), retry with exponential backoff
- **Skip**: For non-critical errors (single file corruption), skip and log warning
- **Fail**: For critical errors (missing required variables, invalid coordinates), fail pipeline and alert
- **Fallback**: Use alternative source if primary source fails (e.g., NASA MODIS → NOAA AVHRR for SST)

**Example**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=60))
def ingest_api(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content
```

### 14.2 Logging

**Log Levels**:
- **DEBUG**: Detailed processing steps (e.g., "Loaded SST file: modis_sst.nc")
- **INFO**: High-level progress (e.g., "Ingested 10 files from MOSDAC")
- **WARNING**: Non-critical issues (e.g., "Chlorophyll: 15% missing due to clouds")
- **ERROR**: Critical failures (e.g., "SST validation failed: missing 'lat' variable")
- **CRITICAL**: Pipeline-breaking errors (e.g., "All SST sources unavailable")

**Log Format**:
```
{timestamp} | {level} | {source} | {message} | {metadata}
```

**Example**:
```
2026-08-31T10:00:00Z | INFO | MOSDAC | Ingested OCM chlorophyll file | {"file": "ocm_chl.nc", "size": "50 MB"}
2026-08-31T10:01:00Z | WARNING | MOSDAC | Chlorophyll: 15% missing due to clouds | {"missing_pct": 0.15}
2026-08-31T10:02:00Z | ERROR | MOSDAC | SST validation failed: missing 'lat' variable | {"file": "modis_sst.nc"}
```

**Storage**:
- **Prototype**: File-based logs (`logs/pipeline.log`)
- **Production**: Centralized logging (ELK stack, CloudWatch)

***

## 15. Security and Compliance

### 15.1 Authentication

**API Keys/Tokens**:
- **Storage**: Environment variables (`.env` file, not committed to git)
- **Rotation**: Rotate keys every 90 days (automated via secrets manager)
- **Access Control**: Restrict API key permissions (read-only for data sources)

**Example**:
```python
import os

API_KEY = os.getenv("MOSDAC_API_KEY")
if not API_KEY:
    raise ValueError("MOSDAC_API_KEY not set in environment")
```

### 15.2 Data Privacy

**Sensitive Data**:
- **User Queries**: Log anonymized queries (no PII)
- **API Credentials**: Never log API keys/tokens
- **Proprietary Data**: Respect data licenses (e.g., CMEMS terms of use)

**Compliance**:
- **GDPR**: Anonymize user data, provide data deletion mechanism
- **Data Licenses**: Adhere to source-specific licenses (e.g., NASA data is public domain; CMEMS requires attribution)

### 15.3 Audit Trail

**Requirements**:
- **Data Provenance**: Log source, timestamp, version for all datasets
- **Processing History**: Log all transformations (normalization, alignment, feature generation)
- **Access Logs**: Log who accessed what data and when (for production)

**Implementation**:
- **Metadata Files**: Store provenance metadata alongside data (Section 10.2)
- **Database**: For production, store audit trail in PostgreSQL for queryable access

***

## 16. Performance Optimization

### 16.1 Chunking

**Strategy**:
- **Raster Data**: Process in chunks (e.g., 1000x1000 pixels) to avoid memory overflow
- **Tabular Data**: Use `pandas.read_csv(chunksize=10000)` for large files
- **Parallel Processing**: Use `dask` or `multiprocessing` for parallel chunk processing

**Example**:
```python
import dask.array as da

sst_dask = da.from_netcdf("sst.nc", chunks=(1000, 1000))
sst_gradient = da.map_blocks(compute_gradient, sst_dask, dtype=float)
```

### 16.2 Indexing

**Spatial Indexing**:
- **Raster**: Use `xarray` with `lat`/`lon` coordinates for fast subsetting
- **Vector**: Use `geopandas` with spatial index (`sindex`) for fast spatial queries

**Temporal Indexing**:
- **Time Series**: Use `xarray` with `time` coordinate for fast temporal subsetting
- **Database**: For production, use PostgreSQL with time-series indexes (e.g., BRIN for time)

### 16.3 Caching

**Cache Layers**:
- **L1 (Memory)**: Cache frequently accessed data in RAM (e.g., Redis for metadata)
- **L2 (Disk)**: Cache processed data on local disk (`cache/` directory)
- **L3 (Object Storage)**: Cache in S3/GCS for production (avoid reprocessing)

**Cache Invalidation**:
- **Time-Based**: Clear cache after TTL (24 hours for dynamic data, 30 days for static)
- **Version-Based**: Clear cache if source data version changes (check metadata)

***

## 17. Testing and Validation

### 17.1 Unit Tests

**Test Cases**:
- **Ingestion**: Verify API/file ingestion returns expected data
- **Parsing**: Verify parsed data matches expected structure
- **Validation**: Verify validation catches out-of-bounds values
- **Normalization**: Verify unit/coordinate/timestamp conversion is correct
- **Feature Generation**: Verify derived features (e.g., SST gradient) are computed correctly

**Example (pytest)**:
```python
def test_sst_gradient():
    sst = np.array([[1, 2], [3, 4]], dtype=float)
    gradient = compute_gradient(sst, dx=1.0)
    assert np.allclose(gradient, np.sqrt(2))  # Expected gradient
```

### 17.2 Integration Tests

**Test Cases**:
- **End-to-End Pipeline**: Ingest → Parse → Validate → Process → Store → Feature Generation
- **Multi-Source Integration**: Combine SST (NASA) + chlorophyll (MOSDAC) → PFZ
- **Error Handling**: Verify pipeline handles API failures, missing data, invalid files

**Example**:
```python
def test_end_to_end_pipeline():
    bbox = (10, 75, 15, 80)
    time_range = (datetime(2026, 8, 31), datetime(2026, 8, 31))

    sst = get_sst(bbox, time_range)
    chl = get_chlorophyll(bbox, time_range)
    pfz = generate_pfz(sst, chl)

    assert pfz is not None
    assert pfz.min() >= 0 and pfz.max() <= 1
```

### 17.3 Data Validation

**Automated Checks**:
- **Daily Validation**: Run validation scripts on newly ingested data
- **Anomaly Detection**: Flag sudden changes in data statistics (e.g., SST mean shifts by > 5°C)
- **Cross-Source Validation**: Compare SST from NASA vs. NOAA; flag discrepancies > 1°C

**Example**:
```python
def validate_sst_consistency(sst_nasa, sst_noaa):
    diff = np.abs(sst_nasa - sst_noaa)
    if diff.mean() > 1.0:
        raise ValueError(f"SST discrepancy: NASA vs NOAA mean diff = {diff.mean()}°C")
```

***

## 18. Monitoring and Alerting

### 18.1 Metrics

**Key Metrics**:
- **Ingestion Rate**: Files ingested per hour
- **Processing Time**: Time to process each dataset
- **Error Rate**: Percentage of failed ingestions/processing steps
- **Data Freshness**: Age of latest available data (e.g., "SST: 24 hours old")
- **Cache Hit Rate**: Percentage of requests served from cache

**Example (Prometheus)**:
```python
from prometheus_client import Counter, Histogram

ingestion_counter = Counter("orca_ingestion_total", "Total ingested files", ["source"])
processing_time = Histogram("orca_processing_seconds", "Processing time", ["step"])
```

### 18.2 Alerts

**Alert Conditions**:
- **Ingestion Failure**: > 5% of ingestions fail in 1 hour
- **Stale Data**: SST/chlorophyll > 48 hours old
- **Processing Error**: Critical error in feature generation
- **Data Anomaly**: SST mean shifts by > 5°C in 1 day

**Alert Channels**:
- **Prototype**: Email/Slack notification
- **Production**: PagerDuty, Opsgenie for 24/7 alerting

***

## 19. Future Enhancements

1. **Real-Time Streaming**: Ingest streaming data (e.g., satellite direct broadcast, buoy networks)
2. **Machine Learning Features**: Generate ML-ready features (e.g., lagged SST, rolling statistics)
3. **Data Fusion**: Combine multi-sensor data (e.g., SST from AVHRR + MODIS + VIIRS)
4. **Automated Quality Control**: ML-based anomaly detection for data quality
5. **Edge Computing**: Deploy pipeline on edge devices (e.g., coastal servers for low-latency access)

***

## 20. References

1. **ISRO/MOSDAC**: Oceansat-2 OCM data. URL: https://www.mosdac.gov.in [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
2. **INCOIS**: PFZ advisories, OSF. URL: https://incois.gov.in [incois.gov](https://incois.gov.in/MarineFisheries/PfzAdvisory)
3. **NASA (PO.DAAC)**: MODIS SST, chlorophyll. URL: https://podaac.jpl.nasa.gov [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)
4. **NOAA**: AVHRR SST, MHW. URL: https://www.noaa.gov [podaac.jpl.nasa](https://podaac.jpl.nasa.gov/dataset/AVHRR_PATHFINDER_L3_SST_MONTHLY_DAYTIME_V5)
5. **Copernicus Marine**: Global ocean reanalysis. URL: https://marine.copernicus.eu [sincem.unibo](https://www.sincem.unibo.it/images/articoli/10.1080_1755876X.2016.1273446.pdf)
6. **GEBCO**: Bathymetry. URL: https://www.gebco.net 

***

**END OF DATA_PIPELINE.md**