import React from 'react';
import { Activity, Waves, TrendingUp, AlertTriangle, ShieldCheck } from 'lucide-react';
import { OrcaResponse } from '../types/orca.ts';

interface ChartsViewProps {
  chartsData: OrcaResponse['chartsData'];
}

export const ChartsView: React.FC<ChartsViewProps> = ({ chartsData }) => {
  const { sstTimeline, chlorophyllProfile, safetyForecast } = chartsData;

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-3 font-sans">
      {/* Chart 1: SST Diurnal Cycle */}
      <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-5 shadow-xl shadow-sky-950/5 backdrop-blur-xl">
        <div className="flex items-center justify-between border-b border-sky-100 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-rose-600" />
            <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-[#082F49]">SST (°C) DIURNAL</h4>
          </div>
          <span className="text-[9px] text-sky-800/70 font-mono tracking-widest uppercase font-bold">INSAT-3D TIR</span>
        </div>

        <div className="h-40 flex items-end justify-between gap-2 pt-4 pb-2 px-1">
          {sstTimeline.map((item, idx) => {
            const heightPct = Math.max(20, Math.min(100, (item.observed - 25) * 18));
            return (
              <div key={idx} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
                <span className="text-[10px] font-mono font-bold text-rose-700">{item.observed}°</span>
                <div
                  className="w-full rounded-t bg-rose-100 hover:bg-rose-200 border-t-2 border-rose-500 transition-all shadow-xs"
                  style={{ height: `${heightPct}%` }}
                />
                <span className="text-[9px] text-sky-900/60 font-mono font-semibold">{item.time}</span>
              </div>
            );
          })}
        </div>
        <div className="flex items-center justify-between text-[10px] font-mono text-sky-800/80 border-t border-sky-100 pt-3 mt-1 font-medium">
          <span>BASELINE: 28.4°C</span>
          <span className="text-rose-700 font-bold uppercase tracking-wider">FRONT ACTIVE</span>
        </div>
      </div>

      {/* Chart 2: Chlorophyll-a */}
      <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-5 shadow-xl shadow-sky-950/5 backdrop-blur-xl">
        <div className="flex items-center justify-between border-b border-sky-100 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <Activity className="h-4 w-4 text-emerald-600" />
            <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-[#082F49]">CHLOROPHYLL-A</h4>
          </div>
          <span className="text-[9px] text-sky-800/70 font-mono tracking-widest uppercase font-bold">OCEANSAT-3 OCM</span>
        </div>

        <div className="h-40 flex items-end justify-around gap-3 pt-4 pb-2 px-2">
          {chlorophyllProfile.map((item, idx) => {
            const heightPct = Math.max(25, Math.min(100, item.chla * 55));
            return (
              <div key={idx} className="flex-1 flex flex-col items-center gap-2 h-full justify-end max-w-[60px]">
                <span className="text-[10px] font-mono font-bold text-emerald-700">{item.chla}</span>
                <div
                  className="w-full rounded-t bg-emerald-100 hover:bg-emerald-200 border-t-2 border-emerald-600 transition-all shadow-xs"
                  style={{ height: `${heightPct}%` }}
                />
                <span className="text-[10px] text-[#082F49] font-mono font-bold uppercase truncate w-full text-center">
                  {item.zone.split(' ')[0]}
                </span>
              </div>
            );
          })}
        </div>
        <div className="flex items-center justify-between text-[10px] font-mono text-sky-800/80 border-t border-sky-100 pt-3 mt-1 font-medium">
          <span>THRESHOLD: 0.60 MG/M³</span>
          <span className="text-emerald-700 font-bold uppercase tracking-wider">BIOMASS HIGH</span>
        </div>
      </div>

      {/* Chart 3: SWAN Wave Height */}
      <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-5 shadow-xl shadow-sky-950/5 backdrop-blur-xl">
        <div className="flex items-center justify-between border-b border-sky-100 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <Waves className="h-4 w-4 text-sky-600" />
            <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-[#082F49]">WAVE (M) FORECAST</h4>
          </div>
          <span className="text-[9px] text-sky-800/70 font-mono tracking-widest uppercase font-bold">INCOIS SWAN</span>
        </div>

        <div className="h-40 flex items-end justify-between gap-2 pt-4 pb-2 px-1">
          {safetyForecast.map((item, idx) => {
            const waveHeightPct = Math.max(20, Math.min(100, item.waveHeight * 40));
            const isCaution = item.waveHeight >= 1.8;
            return (
              <div key={idx} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
                <span className={`text-[10px] font-mono font-bold ${isCaution ? 'text-amber-700' : 'text-sky-700'}`}>
                  {item.waveHeight}m
                </span>
                <div
                  className={`w-full rounded-t border-t-2 transition-all shadow-xs ${
                    isCaution
                      ? 'bg-amber-100 border-amber-500 hover:bg-amber-200'
                      : 'bg-sky-100 border-sky-500 hover:bg-sky-200'
                  }`}
                  style={{ height: `${waveHeightPct}%` }}
                />
                <span className="text-[9px] text-sky-900/60 font-mono font-semibold">{item.hour}</span>
              </div>
            );
          })}
        </div>
        <div className="flex items-center justify-between text-[10px] font-mono text-sky-800/80 border-t border-sky-100 pt-3 mt-1 font-medium">
          <span className="text-amber-700 font-bold">LIMIT: 2.0M</span>
          <span className="text-sky-900/80 font-bold">WINDOW: 04:00 - 11:30</span>
        </div>
      </div>
    </div>
  );
};

