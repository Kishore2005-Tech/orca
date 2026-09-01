import React from 'react';
import { CheckCircle2, AlertCircle, Clock, Waves, Fish, ShieldCheck, MapPin, BookOpen, ShieldAlert, Cpu } from 'lucide-react';
import { AgentResult, AgentType } from '../types/orca.ts';

interface AgentActivityPipelineProps {
  activeAgents: AgentType[];
  agentResults: Partial<Record<AgentType, AgentResult>>;
  isLoading: boolean;
}

export const AgentActivityPipeline: React.FC<AgentActivityPipelineProps> = ({
  activeAgents,
  agentResults,
  isLoading
}) => {
  const agentMeta: Record<AgentType, { name: string; icon: any; desc: string }> = {
    ocean: {
      name: 'OCEAN',
      icon: Waves,
      desc: 'Physical SST & front gradients'
    },
    ecosystem: {
      name: 'ECOSYSTEM',
      icon: Waves,
      desc: 'Chlorophyll-a & productivity'
    },
    fisheries: {
      name: 'FISHERIES',
      icon: Fish,
      desc: 'Candidate PFZ scoring'
    },
    safety: {
      name: 'SAFETY',
      icon: ShieldCheck,
      desc: 'SWAN wave height & swell risk'
    },
    geospatial: {
      name: 'GEOSPATIAL',
      icon: MapPin,
      desc: 'Waypoints & distance calculation'
    },
    knowledge: {
      name: 'CORPUS RAG',
      icon: BookOpen,
      desc: 'Scientific literature validation'
    },
    verification: {
      name: 'VERIFICATION',
      icon: ShieldAlert,
      desc: 'Provenance & unit sanity audit'
    },
    coordinator: {
      name: 'COORDINATOR',
      icon: Cpu,
      desc: 'DAG synthesis & consensus'
    }
  };

  return (
    <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-4 font-sans shadow-lg shadow-sky-950/5 backdrop-blur-xl">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div className="flex items-center gap-2">
          <span className="flex h-2 w-2 rounded-full bg-cyan-600 animate-ping" />
          <span className="text-[10px] font-mono font-bold uppercase tracking-[0.25em] text-[#082F49]">
            MULTI-AGENT DAG EXECUTION
          </span>
        </div>
        <span className="text-[10px] font-mono uppercase tracking-wider text-sky-800/70 font-bold">
          {activeAgents.length} AGENTS ACTIVE IN PIPELINE
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-8">
        {activeAgents.map(ag => {
          const meta = agentMeta[ag] || { name: ag.toUpperCase(), icon: Cpu, desc: '' };
          const Icon = meta.icon;
          const res = agentResults[ag];

          return (
            <div
              key={ag}
              className={`flex flex-col justify-between rounded-xl border p-3 transition-all ${
                res
                  ? 'border-sky-300 bg-sky-50/90 text-sky-950 shadow-sm'
                  : 'border-sky-100 bg-white/60 text-sky-900/40'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <Icon className="h-3.5 w-3.5 text-sky-700" />
                {isLoading ? (
                  <Clock className="h-3 w-3 animate-spin text-sky-500" />
                ) : res?.status === 'success' ? (
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                ) : res?.status === 'warning' ? (
                  <AlertCircle className="h-3.5 w-3.5 text-amber-600" />
                ) : (
                  <span className="h-1.5 w-1.5 rounded-full bg-sky-300" />
                )}
              </div>

              <div>
                <div className="text-[10px] font-mono font-bold tracking-wider uppercase leading-tight truncate text-[#082F49]">
                  {meta.name}
                </div>
                <div className="text-[9px] font-mono text-sky-800/70 mt-1 truncate font-bold">
                  {res ? `${res.executionTimeMs}MS` : 'QUEUED'}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

