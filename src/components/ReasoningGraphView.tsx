import React from 'react';
import { Cpu, ArrowRight, ShieldCheck, CheckCircle2, Waves, Fish, Activity, Sparkles } from 'lucide-react';
import { ReasoningGraphEdge, ReasoningGraphNode } from '../types/orca.ts';

interface ReasoningGraphViewProps {
  nodes: ReasoningGraphNode[];
  edges: ReasoningGraphEdge[];
}

export const ReasoningGraphView: React.FC<ReasoningGraphViewProps> = ({ nodes, edges }) => {
  return (
    <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-6 shadow-xl shadow-sky-950/5 font-sans backdrop-blur-xl">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-sky-100 pb-4 mb-6">
        <div>
          <h3 className="text-sm font-mono font-bold uppercase tracking-wider text-[#082F49] flex items-center gap-2">
            <Cpu className="h-4 w-4 text-sky-700" />
            <span>COLLABORATIVE REASONING GRAPH (DAG)</span>
          </h3>
          <p className="text-xs text-sky-800/80 mt-1 font-mono">
            Deterministic causality chain from raw satellite telemetry to safety-verified recommendation.
          </p>
        </div>
        <span className="rounded-full border border-sky-300 bg-sky-50 px-3 py-1 text-[10px] font-mono font-bold uppercase tracking-wider text-sky-900 shadow-xs">
          CONSENSUS ENGINE // VERIFIED
        </span>
      </div>

      {/* Visual Step-by-Step Chain */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4 font-mono">
        {nodes.map((node, idx) => (
          <div
            key={node.id}
            className="relative flex flex-col justify-between rounded-xl border border-sky-200/80 bg-sky-50/70 p-4 transition-all hover:border-sky-400 hover:bg-white shadow-xs"
          >
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[9px] uppercase font-bold tracking-[0.2em] text-sky-800/70">
                  STEP 0{idx + 1} // {node.category.toUpperCase().replace('_', ' ')}
                </span>
                <span className="rounded-full border border-sky-300 bg-white px-2 py-0.5 text-[8px] font-bold uppercase tracking-widest text-sky-900 shadow-xs">
                  {node.status}
                </span>
              </div>

              <div className="text-xs font-bold text-[#082F49] font-sans mb-1">{node.label}</div>
              {node.value && (
                <div className="text-sm font-mono font-bold text-sky-700 mb-1.5">{node.value}</div>
              )}
              {node.detail && (
                <p className="text-[11px] text-sky-900/70 leading-relaxed font-sans font-medium">{node.detail}</p>
              )}
            </div>

            {node.agent && (
              <div className="mt-4 border-t border-sky-200/60 pt-2.5 text-[9px] text-sky-800/80 font-mono font-bold flex items-center justify-between">
                <span>AGENT: {node.agent.toUpperCase()}</span>
                <CheckCircle2 className="h-3 w-3 text-emerald-600" />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Logical Relationship Edges */}
      <div className="mt-8 border-t border-sky-100 pt-5">
        <h4 className="text-[10px] font-mono font-bold uppercase tracking-[0.25em] text-sky-800/70 font-bold mb-3">
          VALIDATED INFERENCE EDGES //
        </h4>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3 text-xs font-mono">
          {edges.map((edge, i) => (
            <div
              key={i}
              className="flex items-center justify-between rounded-lg border border-sky-200/80 bg-sky-50/70 px-3 py-2 text-sky-950 shadow-xs"
            >
              <span className="text-[10px] font-bold text-[#082F49]">{edge.from.replace('node-', '').toUpperCase()}</span>
              <div className="flex items-center gap-1.5 text-[9px] font-bold text-sky-700 px-2">
                <span>{edge.label.toUpperCase()}</span>
                <ArrowRight className="h-3 w-3 text-sky-500" />
              </div>
              <span className="text-[10px] font-bold text-emerald-700">{edge.to.replace('node-', '').toUpperCase()}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

