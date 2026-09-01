import React from 'react';
import { Navigation, Clock, ShieldCheck, AlertTriangle, Compass, MapPin, ArrowRight, Anchor } from 'lucide-react';
import { RoutePlan } from '../types/orca.ts';

interface RoutePlannerCardProps {
  routePlan?: RoutePlan;
}

export const RoutePlannerCard: React.FC<RoutePlannerCardProps> = ({ routePlan }) => {
  if (!routePlan) return null;

  return (
    <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-6 shadow-xl shadow-sky-950/5 font-sans backdrop-blur-xl">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-sky-100 pb-4 mb-5">
        <div className="flex items-center gap-2">
          <Navigation className="h-4 w-4 text-sky-700" />
          <h3 className="text-sm font-mono font-bold uppercase tracking-wider text-[#082F49]">
            DYNAMIC TRANSIT CORRIDOR
          </h3>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="text-sky-800/70 font-mono text-[10px] uppercase tracking-wider font-bold">ROUND-TRIP:</span>
          <span className="rounded-full border border-sky-300 bg-sky-50 px-3 py-0.5 font-bold text-[#082F49] font-mono text-xs shadow-xs">
            {routePlan.totalDistanceNm} NM
          </span>
        </div>
      </div>

      {/* Primary Metrics Grid */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 mb-5 font-mono text-xs">
        <div className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-3.5 shadow-xs">
          <span className="text-[9px] text-sky-800/70 uppercase font-bold tracking-widest block mb-1">OUTBOUND</span>
          <span className="text-base font-bold text-[#082F49] block">{routePlan.outboundDistanceNm} NM</span>
          <span className="text-[10px] text-sky-700/80 block mt-1 font-semibold">~{routePlan.estimatedOutboundHours} HRS @ 11.5 KTS</span>
        </div>

        <div className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-3.5 shadow-xs">
          <span className="text-[9px] text-sky-800/70 uppercase font-bold tracking-widest block mb-1">RETURN CORRIDOR</span>
          <span className="text-base font-bold text-[#082F49] block">{routePlan.returnDistanceNm} NM</span>
          <span className="text-[10px] text-sky-700/80 block mt-1 font-semibold">~{routePlan.estimatedReturnHours} HRS (SAFE TRACK)</span>
        </div>

        <div className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-3.5 shadow-xs">
          <span className="text-[9px] text-sky-800/70 uppercase font-bold tracking-widest block mb-1">DEPARTURE</span>
          <span className="text-base font-bold text-emerald-700 block">{routePlan.recommendedDepartureTime.split(' ')[0]}</span>
          <span className="text-[10px] text-sky-700/80 block mt-1 font-semibold">CALM WINDOW</span>
        </div>

        <div className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-3.5 shadow-xs">
          <span className="text-[9px] text-sky-800/70 uppercase font-bold tracking-widest block mb-1">CUTOFF DEADLINE</span>
          <span className="text-base font-bold text-amber-700 block">{routePlan.mustReturnBefore}</span>
          <span className="text-[10px] text-amber-700/80 block mt-1 font-semibold">PRE-SWELL SAFETY</span>
        </div>
      </div>

      {/* Waypoints Breakdown */}
      <div className="mb-5">
        <h4 className="text-[10px] font-mono font-bold uppercase tracking-[0.25em] text-sky-800/70 font-bold mb-3">
          NAVIGATIONAL WAYPOINT DIRECTORY //
        </h4>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 font-mono">
          {/* Outbound List */}
          <div className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-4 shadow-xs">
            <span className="text-[10px] font-bold text-[#082F49] uppercase tracking-wider block mb-3 border-b border-sky-200/60 pb-1.5">
              OUTBOUND VECTORS
            </span>
            <div className="space-y-2 text-[11px]">
              {routePlan.outboundWaypoints.map((wp, i) => (
                <div key={i} className="flex items-center justify-between border-b border-sky-200/40 pb-1.5 text-sky-950">
                  <div className="flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-cyan-600" />
                    <span className="font-bold text-[#082F49]">{wp.name}</span>
                  </div>
                  <span className="text-sky-800/80 text-[10px] font-semibold">
                    +{wp.distanceFromStartNm} NM • Hs {wp.waveHeightM}m
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Return List */}
          <div className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-4 shadow-xs">
            <span className="text-[10px] font-bold text-amber-800 uppercase tracking-wider block mb-3 border-b border-sky-200/60 pb-1.5">
              RETURN TRANSIT CORRIDOR
            </span>
            <div className="space-y-2 text-[11px]">
              {routePlan.returnWaypoints.map((wp, i) => (
                <div key={i} className="flex items-center justify-between border-b border-sky-200/40 pb-1.5 text-sky-950">
                  <div className="flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-amber-500" />
                    <span className="font-bold text-[#082F49]">{wp.name}</span>
                  </div>
                  <span className="text-sky-800/80 text-[10px] font-semibold">
                    +{wp.distanceFromStartNm} NM • Hs {wp.waveHeightM}m
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Safety Disclaimer */}
      <div className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-3 text-[11px] text-sky-800/80 flex items-start gap-2.5 font-mono shadow-xs">
        <ShieldCheck className="h-4 w-4 text-sky-700 shrink-0 mt-0.5" />
        <p className="leading-relaxed font-sans font-medium">{routePlan.navigationDisclaimer}</p>
      </div>
    </div>
  );
};

