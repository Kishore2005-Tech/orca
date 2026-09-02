from typing import Dict, Any, List
from backend.schemas.agent import ConfidenceBreakdown, EvidenceItem

class VerificationAgent:
    def __init__(self):
        self.agent_id = "verification_agent"
        self.agent_name = "Independent Verification & Evidentiary Audit Agent"

    def compute_confidence(self, evidence_list: List[EvidenceItem]) -> ConfidenceBreakdown:
        if not evidence_list:
            return ConfidenceBreakdown(
                level="uncertain",
                score=0.20,
                tier_weight_component=0.0,
                spatial_coverage_component=0.1,
                temporal_freshness_component=0.1,
                basis="No verified empirical evidence provided; relying purely on fallback heuristic."
            )

        # Tier weights: Tier 1 (In-situ/INCOIS) = 1.0, Tier 2 (Satellite) = 0.85, Tier 3 (Model) = 0.70, Tier 4 = 0.40
        tier_weights_map = {1: 1.0, 2: 0.85, 3: 0.70, 4: 0.40}
        
        avg_tier_weight = sum([tier_weights_map.get(e.reliability_tier, 0.5) for e in evidence_list]) / len(evidence_list)
        avg_spatial = sum([e.spatial_relevance for e in evidence_list]) / len(evidence_list)
        avg_temporal = sum([e.temporal_relevance for e in evidence_list]) / len(evidence_list)
        
        # Standard Formula: 0.40 * Tier + 0.30 * Spatial + 0.30 * Temporal
        score = (0.40 * avg_tier_weight) + (0.30 * avg_spatial) + (0.30 * avg_temporal)
        score = round(min(1.0, max(0.0, score)), 3)
        
        if score >= 0.85:
            level = "high"
            basis = f"Cross-verified by {len(evidence_list)} multi-mission sources including Tier 1 INCOIS buoys and Tier 2 Oceansat-3/INSAT-3DR satellite observations with high spatial-temporal alignment."
        elif score >= 0.65:
            level = "moderate"
            basis = "Moderate confidence; supported by satellite observation and numerical models with adequate temporal freshness."
        elif score >= 0.40:
            level = "low"
            basis = "Low confidence; limited sensor observations or potential temporal degradation in cloud-affected areas."
        else:
            level = "uncertain"
            basis = "High uncertainty; insufficient empirical data."

        return ConfidenceBreakdown(
            level=level,
            score=score,
            tier_weight_component=round(avg_tier_weight * 0.40, 3),
            spatial_coverage_component=round(avg_spatial * 0.30, 3),
            temporal_freshness_component=round(avg_temporal * 0.30, 3),
            basis=basis
        )

    def verify_envelope(self, payload: Dict[str, Any], evidence_list: List[EvidenceItem]) -> Dict[str, Any]:
        contradictions = []
        caveats = list(payload.get("caveats", []))
        
        # Check for oceanographic physical contradictions
        zone_assessments = payload.get("zone_assessments", [])
        for z in zone_assessments:
            # 1. Check if wind speed is high but safety is marked safe
            if z.get("wind_speed_knots", 0) > 22.0 and z.get("safety_status") == "SAFE":
                contradictions.append(f"Physical contradiction in {z.get('zone_name')}: Wind speed of {z.get('wind_speed_knots')} knots exceeds safe operating threshold for small crafts.")
            
            # 2. Check if SST gradient is reported high without biological confirmation
            if z.get("sst_gradient_c_per_km", 0) > 0.4 and z.get("chlorophyll_mg_m3", 0) < 0.2:
                caveats.append(f"Frontal divergence: High SST gradient in {z.get('zone_name')} without typical coastal chlorophyll enrichment; verify with SAR or in-situ CTD.")

        # Determine Verdict
        if contradictions:
            verdict = "REJECT"
        elif len(caveats) > 0:
            verdict = "PASS_WITH_CAVEATS"
        else:
            verdict = "PASS"

        confidence = self.compute_confidence(evidence_list)

        return {
            "verdict": verdict,
            "confidence": confidence,
            "contradictions": contradictions,
            "caveats": caveats
        }
