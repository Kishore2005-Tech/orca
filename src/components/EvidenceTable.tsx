import React from 'react';
import { Database, Filter, ExternalLink, ShieldCheck, CheckCircle2, AlertCircle, Sparkles } from 'lucide-react';
import { DataClassification, EvidenceItem } from '../types/orca.ts';

interface EvidenceTableProps {
  evidence: EvidenceItem[];
}

export const EvidenceTable: React.FC<EvidenceTableProps> = ({ evidence }) => {
  const getBadgeStyle = (classification: DataClassification) => {
    switch (classification) {
      case 'OBSERVED_DATA':
        return 'border-emerald-300 bg-emerald-100 text-emerald-800';
      case 'MODEL_DATA':
        return 'border-sky-300 bg-sky-100 text-sky-800';
      case 'FORECAST_DATA':
        return 'border-cyan-300 bg-cyan-100 text-cyan-800';
      case 'DERIVED_INDICATOR':
        return 'border-purple-300 bg-purple-100 text-purple-800';
      case 'AI_INFERENCE':
        return 'border-sky-300 bg-sky-50 text-[#082F49]';
      case 'RECOMMENDATION':
        return 'border-rose-300 bg-rose-100 text-rose-800';
      default:
        return 'border-sky-200 bg-sky-50 text-sky-800';
    }
  };

  return (
    <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-6 shadow-xl shadow-sky-950/5 font-sans backdrop-blur-xl">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-sky-100 pb-4 mb-5">
        <div>
          <h3 className="text-sm font-mono font-bold uppercase tracking-wider text-[#082F49] flex items-center gap-2">
            <Database className="h-4 w-4 text-sky-700" />
            <span>GROUNDED EVIDENCE CORPUS</span>
          </h3>
          <p className="text-xs text-sky-800/80 mt-1 font-mono">
            Every decision parameter verified through provenance tracking and unit sanity assertions.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <span className="text-[10px] font-mono uppercase tracking-wider text-sky-800/70 font-bold">VERIFIED DATA POINTS:</span>
          <span className="rounded-full border border-sky-300 bg-sky-50 px-3 py-0.5 text-xs font-mono font-bold text-[#082F49] shadow-xs">
            {evidence.length}
          </span>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-sky-100 text-[10px] uppercase tracking-[0.2em] text-sky-800/70 font-bold">
              <th className="py-3 px-3">CLASSIFICATION</th>
              <th className="py-3 px-3">PARAMETER</th>
              <th className="py-3 px-3">OBSERVED VALUE</th>
              <th className="py-3 px-3">TIMESTAMP</th>
              <th className="py-3 px-3">SOURCE SENSOR</th>
              <th className="py-3 px-3">AUTHORITY</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-sky-100">
            {evidence.map(item => (
              <tr key={item.id} className="hover:bg-sky-50/50 transition-colors">
                <td className="py-3.5 px-3">
                  <span className={`inline-block rounded-full border px-2.5 py-0.5 text-[9px] font-bold tracking-wider uppercase shadow-xs ${getBadgeStyle(item.dataType)}`}>
                    {item.dataType}
                  </span>
                </td>
                <td className="py-3.5 px-3 font-bold text-[#082F49] font-sans text-xs">
                  {item.parameter}
                </td>
                <td className="py-3.5 px-3">
                  <span className="font-bold text-[#082F49] bg-sky-50 border border-sky-200 px-2 py-0.5 rounded shadow-xs">
                    {item.value} {item.unit}
                  </span>
                </td>
                <td className="py-3.5 px-3 text-sky-800/80 text-[11px] font-medium">
                  {item.timestamp}
                </td>
                <td className="py-3.5 px-3 text-sky-950">
                  <div className="font-bold text-[#082F49]">{item.source}</div>
                  {item.sensorInfo && (
                    <div className="text-[10px] text-sky-700/80 mt-0.5 font-medium">{item.sensorInfo}</div>
                  )}
                </td>
                <td className="py-3.5 px-3 text-sky-800 font-semibold">
                  {item.sourceAuthority}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

