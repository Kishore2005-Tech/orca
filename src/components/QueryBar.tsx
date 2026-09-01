import React, { useState } from 'react';
import { Search, Compass, MapPin, Clock, Sparkles, RefreshCw, Send, Sliders } from 'lucide-react';

interface QueryBarProps {
  currentQuery: string;
  onExecuteQuery: (query: string, regionOverride?: string, timeOverride?: string) => void;
  isLoading: boolean;
  selectedRegion: string;
  onSelectRegion: (reg: string) => void;
  timeContext: string;
  setTimeContext: (time: string) => void;
}

export const QueryBar: React.FC<QueryBarProps> = ({
  currentQuery,
  onExecuteQuery,
  isLoading,
  selectedRegion,
  onSelectRegion,
  timeContext,
  setTimeContext
}) => {
  const [inputVal, setInputVal] = useState(currentQuery);

  const quickScenarios = [
    {
      label: 'SST Chennai',
      query: 'What is the SST near Chennai?'
    },
    {
      label: 'Ecosystem Productivity',
      query: 'Why does this region have potentially favorable ecosystem conditions?'
    },
    {
      label: 'Fishing & Route Chennai',
      query: 'Where is the most promising and safer fishing area near Chennai tomorrow morning and give me a route?'
    },
    {
      label: 'Sea State & Safety',
      query: 'Is it safe to go fishing tomorrow morning?'
    },
    {
      label: 'Kochi Malabar Upwelling',
      query: 'Where should I fish tomorrow morning near Kochi and what is the sea state?'
    },
    {
      label: 'Temporal Comparison',
      query: "Compare today's ocean conditions with yesterday."
    },
    {
      label: 'Climate +1.5°C SST',
      query: 'What happens if SST increases by 1.5°C?'
    }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim() || isLoading) return;
    onExecuteQuery(inputVal.trim());
  };

  const handleChipClick = (q: string) => {
    setInputVal(q);
    onExecuteQuery(q);
  };

  return (
    <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-5 shadow-xl shadow-sky-950/5 backdrop-blur-xl font-sans">
      {/* Region & Time Context Selectors */}
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Region Picker */}
          <div className="flex items-center gap-2 rounded-full border border-sky-300/80 bg-sky-50/90 px-3.5 py-1.5 text-sky-950 shadow-sm">
            <MapPin className="h-3.5 w-3.5 text-sky-600" />
            <span className="text-[10px] text-sky-800/70 uppercase font-mono tracking-wider font-bold">SECTOR:</span>
            <select
              value={selectedRegion}
              onChange={e => onSelectRegion(e.target.value)}
              className="bg-transparent text-xs font-mono font-bold text-sky-950 focus:outline-none cursor-pointer uppercase"
            >
              <option value="chennai" className="bg-white text-sky-950">Chennai BoB</option>
              <option value="kochi" className="bg-white text-sky-950">Kochi Arabian Sea</option>
              <option value="visakhapatnam" className="bg-white text-sky-950">Visakhapatnam BoB</option>
              <option value="veraval" className="bg-white text-sky-950">Veraval Gujarat</option>
              <option value="port_blair" className="bg-white text-sky-950">Port Blair Andaman</option>
            </select>
          </div>

          {/* Temporal Window */}
          <div className="flex items-center gap-2 rounded-full border border-sky-300/80 bg-sky-50/90 px-3.5 py-1.5 text-sky-950 shadow-sm">
            <Clock className="h-3.5 w-3.5 text-amber-600" />
            <span className="text-[10px] text-sky-800/70 uppercase font-mono tracking-wider font-bold">WINDOW:</span>
            <select
              value={timeContext}
              onChange={e => setTimeContext(e.target.value)}
              className="bg-transparent text-xs font-mono font-bold text-sky-950 focus:outline-none cursor-pointer uppercase"
            >
              <option value="Current In-Situ Window" className="bg-white text-sky-950">Live In-Situ</option>
              <option value="Tomorrow Morning (04:30 - 11:30 IST)" className="bg-white text-sky-950">Tomorrow Morning (04:30 - 11:30 IST)</option>
              <option value="Tomorrow Afternoon/Evening (13:00 - 18:00 IST)" className="bg-white text-sky-950">Tomorrow Afternoon</option>
              <option value="Historical Reference (Yesterday)" className="bg-white text-sky-950">Historical Reference</option>
            </select>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-sky-300/80 bg-sky-100/80 px-3 py-1 text-[10px] font-mono font-bold tracking-widest uppercase text-sky-900 shadow-sm">
            <div className="h-1.5 w-1.5 rounded-full bg-cyan-600 animate-ping" />
            <span>DAG REASONING LIVE</span>
          </span>
        </div>
      </div>

      {/* Main Search Input Form */}
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <div className="pointer-events-none absolute left-4 flex items-center text-sky-600">
          <Search className="h-4 w-4" />
        </div>

        <input
          type="text"
          value={inputVal}
          onChange={e => setInputVal(e.target.value)}
          placeholder="Ask ORCA (e.g., 'Where is the most promising and safer fishing area near Chennai tomorrow morning and give me a route?')"
          className="w-full rounded-full border border-sky-300/90 bg-white/95 py-3.5 pl-12 pr-32 text-sm text-sky-950 placeholder-sky-900/40 focus:border-sky-500 focus:ring-2 focus:ring-sky-200 focus:outline-none transition-all font-medium shadow-inner"
        />

        <button
          type="submit"
          disabled={isLoading || !inputVal.trim()}
          className="absolute right-2 flex items-center gap-2 rounded-full bg-[#082F49] px-5 py-2 text-xs font-mono font-black uppercase tracking-wider text-white hover:bg-sky-900 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-md shadow-sky-950/20"
        >
          {isLoading ? (
            <>
              <RefreshCw className="h-3.5 w-3.5 animate-spin text-white" />
              <span>REASONING</span>
            </>
          ) : (
            <>
              <span>REASON</span>
              <Send className="h-3 w-3 text-cyan-300" />
            </>
          )}
        </button>
      </form>

      {/* Quick Scenario Chips */}
      <div className="mt-4 flex items-center gap-2 overflow-x-auto pb-1 text-xs scrollbar-none">
        <span className="text-[9px] uppercase font-mono tracking-[0.25em] text-sky-900/60 font-bold whitespace-nowrap mr-1">
          SCENARIOS //
        </span>
        {quickScenarios.map((sc, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleChipClick(sc.query)}
            className="whitespace-nowrap rounded-full border border-sky-200/90 bg-sky-50/80 px-3 py-1 text-[10px] font-mono font-bold tracking-wider text-sky-900 hover:border-sky-400 hover:bg-[#082F49] hover:text-white transition-all uppercase shadow-sm"
          >
            {sc.label}
          </button>
        ))}
      </div>
    </div>
  );
};

