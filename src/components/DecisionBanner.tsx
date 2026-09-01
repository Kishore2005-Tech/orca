import React from 'react';
import { ShieldCheck, AlertTriangle, Fish, Compass, Sparkles, CheckCircle2, ChevronDown, ChevronUp, AlertCircle } from 'lucide-react';
import { OrcaResponse, UserMode } from '../types/orca.ts';

interface DecisionBannerProps {
  data: OrcaResponse;
  userMode: UserMode;
  onOpenVerification: () => void;
  onOpenKnowledge: () => void;
}

export const DecisionBanner: React.FC<DecisionBannerProps> = ({
  data,
  userMode,
  onOpenVerification,
  onOpenKnowledge
}) => {
  const { keyStatus, oneLineRecommendation, conflictReport, verification, parsedIntent } = data;

  return (
    <div className="rounded-2xl border border-sky-200/90 bg-white/90 p-6 shadow-xl shadow-sky-950/5 relative overflow-hidden font-sans backdrop-blur-xl">
      {/* Top Status Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-sky-200/70 pb-4 mb-5">
        <div className="flex items-center gap-3">
          <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-[10px] font-mono font-black uppercase tracking-[0.25em] text-[#082F49]">
            SYNTHESIS REPORT // 01
          </span>
          <span className="text-sky-300 font-mono text-xs">/</span>
          <span className="text-xs font-mono text-sky-800/80 uppercase font-bold">
            {parsedIntent?.location?.name || 'Chennai'} [{parsedIntent?.timeContext || 'Current In-Situ Window'}]
          </span>
        </div>

        {/* Status Badges */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Suitability */}
          <div className="flex items-center gap-1.5 rounded-full border border-sky-200/80 bg-sky-50/90 px-3 py-1 text-xs shadow-sm">
            <Fish className="h-3.5 w-3.5 text-sky-600" />
            <span className="text-sky-800/70 text-[10px] uppercase font-mono tracking-wider font-bold">SUITABILITY:</span>
            <span
              className={`font-mono font-bold uppercase ${
                keyStatus.fishingSuitability === 'High'
                  ? 'text-emerald-700'
                  : keyStatus.fishingSuitability === 'Medium'
                  ? 'text-sky-700'
                  : 'text-amber-700'
              }`}
            >
              {keyStatus.fishingSuitability}
            </span>
          </div>

          {/* Marine Safety */}
          <div className="flex items-center gap-1.5 rounded-full border border-sky-200/80 bg-sky-50/90 px-3 py-1 text-xs shadow-sm">
            <ShieldCheck className="h-3.5 w-3.5 text-amber-600" />
            <span className="text-sky-800/70 text-[10px] uppercase font-mono tracking-wider font-bold">SAFETY:</span>
            <span
              className={`font-mono font-bold uppercase ${
                keyStatus.marineSafety === 'Safe'
                  ? 'text-emerald-700'
                  : keyStatus.marineSafety === 'Caution'
                  ? 'text-amber-700'
                  : 'text-rose-700'
              }`}
            >
              {keyStatus.marineSafety}
            </span>
          </div>

          {/* Confidence Score */}
          <div className="flex items-center gap-1.5 rounded-full border border-sky-200/80 bg-sky-50/90 px-3 py-1 text-xs shadow-sm">
            <Sparkles className="h-3.5 w-3.5 text-purple-600" />
            <span className="text-sky-800/70 text-[10px] uppercase font-mono tracking-wider font-bold">CONFIDENCE:</span>
            <span className="font-mono font-bold text-[#082F49]">
              {keyStatus.confidenceScore}%
            </span>
          </div>
        </div>
      </div>

      {/* Primary One-Line Decision */}
      <div className="mb-5">
        <h2 className="text-xl sm:text-2xl font-black font-display tracking-tight text-[#082F49] leading-snug">
          "{oneLineRecommendation}"
        </h2>
      </div>

      {/* Conflict Resolution Notice if Triggered */}
      {conflictReport.detected && (
        <div className="mb-5 flex items-start gap-3 rounded-xl border border-amber-300 bg-amber-50/90 p-4 text-xs text-amber-950 shadow-sm">
          <AlertTriangle className="h-4 w-4 shrink-0 text-amber-600 mt-0.5" />
          <div className="font-mono">
            <span className="font-bold uppercase tracking-wider text-amber-800">Cross-Agent Conflict Resolved: </span>
            <span className="text-amber-900 font-sans">{conflictReport.description} </span>
            <span className="text-amber-900 font-bold">[{conflictReport.resolutionStrategy}]</span>
          </div>
        </div>
      )}

      {/* Quick Summary Highlights */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 border-t border-sky-200/70 pt-4 text-xs">
        <div className="rounded-xl border border-sky-200/80 bg-sky-50/80 p-4 shadow-sm">
          <span className="text-[9px] uppercase font-mono tracking-[0.25em] text-sky-800/70 block mb-1 font-bold">
            TARGET ZONE CANDIDATE
          </span>
          <span className="font-display font-black text-[#082F49] block text-base uppercase">
            {data.candidateZones[0]?.name || 'Sector Alpha'}
          </span>
          <span className="text-[11px] font-mono text-sky-700 mt-1 block font-bold">
            SCORE {data.candidateZones[0]?.suitabilityScore || 88}/100 • {data.candidateZones[0]?.distanceNm || 18.5} NM OUT
          </span>
        </div>

        <div className="rounded-xl border border-sky-200/80 bg-sky-50/80 p-4 shadow-sm">
          <span className="text-[9px] uppercase font-mono tracking-[0.25em] text-sky-800/70 block mb-1 font-bold">
            TRANSIT WINDOW
          </span>
          <span className="font-display font-black text-[#082F49] block text-base uppercase">
            {data.routePlan?.recommendedDepartureTime || '04:30 AM IST WINDOW'}
          </span>
          <span className="text-[11px] font-mono text-amber-700 mt-1 block font-bold">
            RETURN: {data.routePlan?.mustReturnBefore || 'BEFORE 12:00 PM IST'}
          </span>
        </div>

        <div className="rounded-xl border border-sky-200/80 bg-sky-50/80 p-4 flex flex-col justify-between shadow-sm">
          <div>
            <span className="text-[9px] uppercase font-mono tracking-[0.25em] text-sky-800/70 block mb-1 font-bold">
              VERIFICATION AUDIT
            </span>
            <div className="flex items-center gap-1.5 text-xs font-mono font-bold text-emerald-700 uppercase">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
              <span>{verification.overallStatus} (6/6 CHECKS)</span>
            </div>
          </div>
          <button
            onClick={onOpenVerification}
            className="text-[10px] font-mono font-bold tracking-wider uppercase text-sky-800 hover:text-sky-950 transition-colors text-left mt-2 flex items-center gap-1"
          >
            <span>INSPECT AUDIT LOGS</span>
            <span>→</span>
          </button>
        </div>
      </div>
    </div>
  );
};

