from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class EvidenceItem(BaseModel):
    source_id: str
    source_name: str
    reliability_tier: int = Field(ge=1, le=4, description="1: Verified In-situ/INCOIS, 2: Satellite Earth Observation, 3: Numerical Model, 4: Unverified/Heuristic")
    data_type: str
    sensor: Optional[str] = None
    retrieved_at: str
    raw_value: Any
    spatial_relevance: float = Field(ge=0.0, le=1.0)
    temporal_relevance: float = Field(ge=0.0, le=1.0)
    provenance_url: Optional[str] = None

class ReasoningStep(BaseModel):
    agent_id: str
    agent_name: str
    step_number: int
    action: str
    thought: str
    output_summary: str
    duration_ms: int

class ConfidenceBreakdown(BaseModel):
    level: str  # high, moderate, low, uncertain
    score: float = Field(ge=0.0, le=1.0)
    tier_weight_component: float
    spatial_coverage_component: float
    temporal_freshness_component: float
    basis: str

class ZoneAssessment(BaseModel):
    zone_name: str
    latitude: float
    longitude: float
    distance_km: float
    distance_nm: float
    depth_m: float
    sst_celsius: float
    chlorophyll_mg_m3: float
    sst_gradient_c_per_km: float
    wave_height_m: float
    wind_speed_knots: float
    current_speed_m_s: float
    current_direction_deg: float
    pfz_overlap: bool
    potential_score: int = Field(ge=0, le=100)
    catch_suitability: str
    recommended_target_species: List[str]
    safety_status: str  # SAFE, CAUTION, DANGER
    craft_advisory: str

class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: Any

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONGeometry
    properties: Dict[str, Any]

class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]

class StandardResponseEnvelope(BaseModel):
    request_id: str
    query: str
    timestamp: str
    intent: str
    final_answer: str
    contributing_agents: List[str]
    verification_verdict: str  # PASS, PASS_WITH_CAVEATS, REJECT
    final_confidence: ConfidenceBreakdown
    reasoning_trace: List[ReasoningStep]
    zone_assessments: Optional[List[ZoneAssessment]] = None
    geojson_layers: Optional[GeoJSONFeatureCollection] = None
    citations: List[str]
    caveats: List[str]
    unresolved_conflicts: List[str]
    safety_summary: Optional[Dict[str, Any]] = None
    fishery_summary: Optional[Dict[str, Any]] = None
