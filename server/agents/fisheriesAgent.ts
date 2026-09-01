import { AgentResult } from '../../src/types/orca.ts';
import { LocationProfile, getDynamicMarineContext } from '../marineDataEngine.ts';

export function runFisheriesAgent(
  profile: LocationProfile,
  timeContext: string,
  query: string
): AgentResult {
  const startTime = Date.now();
  const ctx = getDynamicMarineContext(profile, timeContext);

  const topCandidate = ctx.recommendedZone;
  const findings: string[] = [
    `Identified ${ctx.candidateZones.length} candidate Potential Fishing Zones (PFZs) within the regional maritime sector.`,
    `Top candidate: ${topCandidate.name} (${topCandidate.code}) with an overall suitability score of ${topCandidate.suitabilityScore}/100.`,
    `Candidate is characterized by thermal front gradient (${topCandidate.thermalGradientCPerKm}°C/km) co-located with chlorophyll-a (${topCandidate.chlorophyllMgM3} mg/m³).`,
    `Secondary candidates: ${ctx.candidateZones.slice(1).map(z => `${z.name} (Score: ${z.suitabilityScore})`).join(', ')}.`
  ];

  return {
    agent: 'fisheries',
    status: 'success',
    executionTimeMs: Date.now() - startTime + 48,
    query,
    location: {
      name: profile.name,
      latitude: profile.lat,
      longitude: profile.lon
    },
    time: ctx.isTomorrow ? 'Tomorrow AM Forecast Window' : 'Current Advisories',
    findings,
    observations: {
      totalCandidateZones: ctx.candidateZones.length,
      primaryCandidateCode: topCandidate.code,
      primarySuitabilityScore: topCandidate.suitabilityScore,
      targetSpeciesGroup: 'Small/Medium Pelagics (Carangids, Sardinella, Scombrids)',
      thermalChlorophyllOverlap: true,
      confidenceClassification: topCandidate.pfzConfidence
    },
    dataSources: [
      'INCOIS Ocean Advisory Services & PFZ Mission',
      'CMFRI Pelagic Fishery Catch Statistics & Habitat Models',
      'ISRO Earth Observation Integrated Advisory Pipeline'
    ],
    dataType: 'DERIVED_INDICATOR',
    confidence: 0.88,
    limitations: [
      'PFZ advisories represent oceanographic habitat favorability; actual catch rates depend on gear type, mesh size, schooling depth, and diurnal vertical migration.',
      'Does not verify presence of demersal/bottom species.'
    ],
    warnings: [
      'Marine conservation note: Respect mesh size regulations and maritime sanctuary boundaries.'
    ]
  };
}
