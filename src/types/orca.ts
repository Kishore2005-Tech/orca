export type DataClassification = 
  | 'OBSERVED_DATA'
  | 'MODEL_DATA'
  | 'FORECAST_DATA'
  | 'DERIVED_INDICATOR'
  | 'AI_INFERENCE'
  | 'RECOMMENDATION';

export type AgentType = 
  | 'ocean'
  | 'ecosystem'
  | 'fisheries'
  | 'safety'
  | 'geospatial'
  | 'knowledge'
  | 'verification'
  | 'coordinator';

export type UserMode = 'fisher' | 'scientist' | 'operations';

export interface MarineLocation {
  name: string;
  latitude: number;
  longitude: number;
  regionName: string;
  eezZone: string;
  depthMeters: number;
}

export interface EvidenceItem {
  id: string;
  parameter: string;
  value: string | number;
  unit: string;
  timestamp: string;
  location: {
    name: string;
    latitude: number;
    longitude: number;
  };
  source: string;
  sourceAuthority: string;
  dataType: DataClassification;
  freshness: 'CURRENT' | 'STALE' | 'FORECAST' | 'SIMULATED';
  confidenceScore: number;
  sensorInfo?: string;
}

export interface AgentResult {
  agent: AgentType;
  status: 'success' | 'warning' | 'skipped' | 'error';
  executionTimeMs: number;
  query: string;
  location: {
    name: string;
    latitude: number;
    longitude: number;
  };
  time: string;
  findings: string[];
  observations: Record<string, string | number | boolean | null | Record<string, any>>;
  dataSources: string[];
  dataType: DataClassification;
  confidence: number;
  limitations: string[];
  warnings: string[];
}

export interface MarineZone {
  id: string;
  code: string;
  name: string;
  latitude: number;
  longitude: number;
  distanceNm: number;
  bearingDeg: number;
  suitabilityScore: number; // 0 - 100
  sstCelsius: number;
  chlorophyllMgM3: number;
  waveHeightM: number;
  windSpeedKnots: number;
  safetyStatus: 'SAFE' | 'CAUTION' | 'HAZARDOUS';
  pfzConfidence: 'HIGH' | 'MEDIUM' | 'LOW';
  depthMeters: number;
  thermalGradientCPerKm: number;
  summary: string;
}

export interface RouteWaypoint {
  name: string;
  latitude: number;
  longitude: number;
  distanceFromStartNm: number;
  legDistanceNm: number;
  waveHeightM: number;
  windSpeedKnots: number;
  safetyFlag: 'NORMAL' | 'CAUTION' | 'WARNING';
}

export interface RoutePlan {
  origin: {
    name: string;
    latitude: number;
    longitude: number;
  };
  destination: MarineZone;
  outboundWaypoints: RouteWaypoint[];
  returnWaypoints: RouteWaypoint[];
  totalDistanceNm: number;
  outboundDistanceNm: number;
  returnDistanceNm: number;
  estimatedOutboundHours: number;
  estimatedReturnHours: number;
  recommendedDepartureTime: string;
  mustReturnBefore: string;
  safetySummary: string;
  navigationDisclaimer: string;
}

export interface ReasoningGraphNode {
  id: string;
  label: string;
  category: 'raw_data' | 'pattern' | 'ecosystem' | 'fisheries' | 'safety' | 'verification' | 'decision';
  status: 'observed' | 'derived' | 'forecast' | 'verified' | 'decision';
  agent?: AgentType;
  value?: string;
  detail?: string;
  confidence?: number;
}

export interface ReasoningGraphEdge {
  from: string;
  to: string;
  label?: string;
  relationType?: 'supports' | 'constrains' | 'validates' | 'resolves';
}

export interface ConflictReport {
  detected: boolean;
  description?: string;
  conflictingAgents: AgentType[];
  resolutionStrategy?: string;
  outcome?: string;
}

export interface VerificationCheck {
  name: string;
  status: 'pass' | 'warning' | 'fail';
  detail: string;
}

export interface VerificationReport {
  passed: boolean;
  overallStatus: 'VERIFIED' | 'CAUTION_QUALIFIED' | 'REJECTED';
  checks: VerificationCheck[];
  dataFreshnessWarning?: string;
  confidenceAdjustmentReason?: string;
}

export interface ParsedQueryIntent {
  rawQuery: string;
  action: string;
  primaryDomain: 'oceanography' | 'ecosystem' | 'fisheries' | 'safety' | 'geospatial' | 'what_if_scenario';
  location: {
    name: string;
    latitude: number;
    longitude: number;
  };
  timeContext: string;
  requestedParameters: string[];
  requiresRoute: boolean;
  isWhatIfScenario: boolean;
  whatIfDelta?: string;
}

export interface OrcaResponse {
  id: string;
  timestamp: string;
  query: string;
  parsedIntent: ParsedQueryIntent;
  oneLineRecommendation: string;
  keyStatus: {
    fishingSuitability: 'High' | 'Medium' | 'Low' | 'Inconclusive';
    marineSafety: 'Safe' | 'Caution' | 'High Risk' | 'Unknown';
    confidenceLevel: 'High' | 'Medium' | 'Low';
    confidenceScore: number;
  };
  activeAgents: AgentType[];
  agentResults: Partial<Record<AgentType, AgentResult>>;
  evidence: EvidenceItem[];
  candidateZones: MarineZone[];
  recommendedZoneId?: string;
  routePlan?: RoutePlan;
  reasoningGraph: {
    nodes: ReasoningGraphNode[];
    edges: ReasoningGraphEdge[];
  };
  conflictReport: ConflictReport;
  verification: VerificationReport;
  chartsData: {
    sstTimeline: Array<{ time: string; observed: number; baseline: number }>;
    chlorophyllProfile: Array<{ zone: string; chla: number; threshold: number }>;
    safetyForecast: Array<{ hour: string; waveHeight: number; windSpeed: number; waveThreshold: number }>;
  };
  scientificExplanation: string;
  sources: Array<{
    name: string;
    sensor: string;
    agency: string;
    updateFrequency: string;
    lastCalibrated: string;
  }>;
  limitations: string[];
  userMode: UserMode;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: 'Researcher / Oceanographer' | 'Commercial Fisher' | 'Maritime Operations Officer';
  organization: string;
  defaultRegion: string;
  avatarUrl?: string;
}
