'use client';
import { useState } from 'react';
import { submitQuery, QueryResponse } from '@/lib/api';

export default function Dashboard() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAskOrca = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await submitQuery(query);
      setResponse(res);
    } catch (err: any) {
      setError(err.message || 'Error connecting to ORCA backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-900 text-slate-200 font-sans">
      {/* Sidebar: Ask ORCA */}
      <div className="w-[450px] bg-slate-800 border-r border-slate-700 flex flex-col">
        <div className="p-6 border-b border-slate-700">
          <h2 className="text-2xl font-semibold text-emerald-400">ORCA Intelligence</h2>
          <p className="text-sm text-slate-400 mt-1">Agentic Marine Reasoning</p>
        </div>
        
        <div className="flex-grow p-6 overflow-y-auto">
          {error && (
            <div className="p-4 bg-red-900/50 border border-red-500 rounded-md text-red-200 mb-6 shadow-sm">
              {error}
            </div>
          )}

          {response && (
            <div className="space-y-6">
              <div className="bg-slate-700/50 p-5 rounded-lg border border-emerald-500/30 shadow-lg shadow-emerald-500/10">
                <h3 className="text-emerald-400 font-medium mb-3 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  Recommendation
                </h3>
                <p className="text-slate-200 leading-relaxed text-sm">{response.final_answer}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-700/30 p-4 rounded-lg border border-slate-600">
                  <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Verification</span>
                  <div className="flex items-center gap-2 mt-2">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${response.verification_verdict === 'pass' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-red-500/20 text-red-400 border border-red-500/30'}`}>
                      {response.verification_verdict.toUpperCase()}
                    </span>
                  </div>
                </div>
                
                <div className="bg-slate-700/30 p-4 rounded-lg border border-slate-600">
                  <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Confidence</span>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="px-2 py-1 rounded text-xs font-medium bg-blue-500/20 text-blue-400 border border-blue-500/30">
                      {response.final_confidence.level.toUpperCase()} ({(response.final_confidence.score * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-700/30 p-4 rounded-lg border border-slate-600">
                <span className="text-xs text-slate-400 uppercase tracking-wider block mb-3">Contributing Agents</span>
                <div className="flex flex-wrap gap-2">
                  {response.contributing_agents.map(agent => (
                    <span key={agent} className="px-3 py-1 bg-slate-800 border border-slate-600 rounded-full text-xs text-slate-300 shadow-sm">
                      {agent.replace('_agent', '')}
                    </span>
                  ))}
                </div>
              </div>

              {response.caveats.length > 0 && (
                <div className="bg-orange-900/20 p-4 rounded-lg border border-orange-500/30">
                  <span className="text-xs text-orange-400 uppercase tracking-wider block mb-2">Caveats</span>
                  <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">
                    {response.caveats.map((c, i) => <li key={i}>{c}</li>)}
                  </ul>
                </div>
              )}
            </div>
          )}
          
          {!response && !loading && (
            <div className="h-full flex items-center justify-center text-slate-500 text-center px-6 text-sm">
              Enter a query below to start collaborative marine reasoning.
            </div>
          )}
          
          {loading && (
            <div className="h-full flex flex-col items-center justify-center text-emerald-400 space-y-4">
              <div className="w-8 h-8 border-4 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin"></div>
              <span className="animate-pulse text-sm">ORCA is reasoning...</span>
            </div>
          )}
        </div>

        <div className="p-6 bg-slate-800 border-t border-slate-700">
          <textarea 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => { if(e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleAskOrca(); } }}
            className="w-full bg-slate-900 border border-slate-600 rounded-lg p-4 text-slate-200 text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-none shadow-inner"
            rows={3}
            placeholder="E.g., Is it safe to fish in the Bay of Bengal today?"
            disabled={loading}
          />
          <button 
            onClick={handleAskOrca}
            disabled={loading || !query.trim()}
            className="w-full mt-4 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold py-3 px-4 rounded-lg transition-colors shadow-lg shadow-emerald-900/50 flex justify-center items-center gap-2"
          >
            {loading ? 'Processing...' : 'Analyze'}
          </button>
        </div>
      </div>

      {/* Main Content: Map & Dashboard */}
      <div className="flex-1 flex flex-col">
        {/* Top Stats Bar */}
        <div className="h-20 bg-slate-900 border-b border-slate-700 flex items-center px-8 gap-8 shadow-sm">
          <div className="flex flex-col">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-semibold mb-1">Demo Data Source</span>
            <span className="text-base font-medium text-slate-200">INCOIS / Copernicus</span>
          </div>
          <div className="w-px h-8 bg-slate-700 mx-2"></div>
          <div className="flex flex-col">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-semibold mb-1">SST (Mock)</span>
            <span className="text-base font-medium text-emerald-400">28.5 °C</span>
          </div>
          <div className="w-px h-8 bg-slate-700 mx-2"></div>
          <div className="flex flex-col">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-semibold mb-1">Marine Hazard</span>
            <span className="text-base font-medium text-emerald-400">Clear</span>
          </div>
        </div>
        
        {/* Map Area */}
        <div className="flex-1 bg-slate-800 relative p-6">
          <div className="w-full h-full flex flex-col items-center justify-center bg-slate-900/50 border-2 border-dashed border-slate-700 rounded-2xl text-slate-500 shadow-inner">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mb-4 opacity-50"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" x2="9" y1="3" y2="18"/><line x1="15" x2="15" y1="6" y2="21"/></svg>
            <span className="text-lg font-medium">Interactive MapLibre Viewer</span>
            <span className="text-sm mt-2 opacity-70">(Placeholder for MVP)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
