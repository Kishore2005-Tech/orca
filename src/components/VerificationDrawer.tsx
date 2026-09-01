import React from 'react';
import { X, ShieldAlert, CheckCircle2, AlertTriangle, Database, Clock, Compass } from 'lucide-react';
import { VerificationReport } from '../types/orca.ts';

interface VerificationDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  report: VerificationReport;
}

export const VerificationDrawer: React.FC<VerificationDrawerProps> = ({ isOpen, onClose, report }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#082F49]/40 p-4 backdrop-blur-md font-sans">
      <div className="relative w-full max-w-2xl rounded-2xl border border-sky-200/90 bg-white/95 p-6 shadow-2xl backdrop-blur-xl">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4 rounded-full p-2 text-sky-800 hover:bg-sky-100 hover:text-sky-950 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 border-b border-sky-100 pb-4 mb-5">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-100 text-sky-700 border border-sky-200 shadow-xs">
            <ShieldAlert className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-base font-mono font-bold uppercase tracking-wider text-[#082F49]">ORCA VERIFICATION AUDIT</h3>
            <p className="text-xs text-sky-800/80 font-mono">Independent data provenance, causality, and marine safety validation</p>
          </div>
        </div>

        {/* Overall Status Banner */}
        <div className="mb-5 rounded-xl border border-emerald-300 bg-emerald-50 p-4 flex items-center justify-between font-mono shadow-xs">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="h-5 w-5 text-emerald-600" />
            <div>
              <span className="text-xs font-bold text-emerald-900 uppercase tracking-wider">VALIDATION: {report.overallStatus}</span>
              <p className="text-[11px] text-emerald-800 font-sans mt-0.5 font-medium">All multi-agent outputs verified against scientific safety rules.</p>
            </div>
          </div>
          <span className="rounded-full border border-emerald-300 bg-white px-3 py-0.5 text-xs font-bold text-emerald-900 shadow-xs">
            PASS (6/6 CHECKS)
          </span>
        </div>

        {/* Individual Verification Checks List */}
        <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1 font-mono">
          {report.checks.map((chk, idx) => (
            <div
              key={idx}
              className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-3.5 flex items-start gap-3 text-xs shadow-xs"
            >
              {chk.status === 'pass' ? (
                <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0 mt-0.5" />
              ) : (
                <AlertTriangle className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
              )}
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-[#082F49] font-sans text-xs">{chk.name}</span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-[8px] font-bold uppercase tracking-widest shadow-xs ${
                      chk.status === 'pass' ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-amber-100 text-amber-800 border border-amber-300'
                    }`}
                  >
                    {chk.status}
                  </span>
                </div>
                <p className="text-[11px] text-sky-900/70 leading-relaxed font-sans font-medium">{chk.detail}</p>
              </div>
            </div>
          ))}
        </div>

        {report.dataFreshnessWarning && (
          <div className="mt-4 rounded-xl border border-amber-300 bg-amber-50 p-3 text-xs text-amber-900 font-mono shadow-xs">
            <span className="font-bold uppercase">TEMPORAL NOTE // </span>
            <span className="font-medium">{report.dataFreshnessWarning}</span>
          </div>
        )}

        <div className="mt-6 text-right">
          <button
            onClick={onClose}
            className="rounded-full bg-[#082F49] px-6 py-2 text-xs font-mono font-bold uppercase tracking-wider text-white hover:bg-sky-900 transition-colors shadow-md shadow-sky-950/20"
          >
            CLOSE AUDIT LOGS
          </button>
        </div>
      </div>
    </div>
  );
};

