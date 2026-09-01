import React, { useState } from 'react';
import { Compass, Waves, ArrowRight, ShieldCheck, Cpu, Database, ChevronRight, Activity, Globe, CheckCircle2, Play, Sparkles, Wind, Eye } from 'lucide-react';
import { OceanCanvasBackground } from './OceanCanvasBackground';
import oceanHeroBg from '../assets/images/ocean_hero_bg_1788170791119.jpg';

interface LandingPageProps {
  onEnterWorkspace: () => void;
  onSelectScenario: (scenarioQuery: string) => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onEnterWorkspace, onSelectScenario }) => {
  const [waveIntensity, setWaveIntensity] = useState<number>(1);
  const [showSatelliteTexture, setShowSatelliteTexture] = useState<boolean>(true);

  const sampleScenarios = [
    {
      title: 'Fishing & Safety Mission',
      query: 'Where is the most promising and safer fishing area near Chennai tomorrow morning and give me a route?',
      badge: 'MULTI-AGENT PIPELINE',
      coord: '13.0827° N, 80.2707° E'
    },
    {
      title: 'Ecosystem Productivity Analysis',
      query: 'Why does this region have potentially favorable ecosystem conditions?',
      badge: 'OCEAN + ECOSYSTEM + CORPUS',
      coord: 'COROMANDEL SECTOR'
    },
    {
      title: 'Physical Oceanography State',
      query: 'What is the SST near Chennai?',
      badge: 'INSAT-3D TIR RADIOMETRY',
      coord: 'IN-SITU SAMUDRA'
    },
    {
      title: 'Arabian Sea Malabar Sector',
      query: 'Where should I fish tomorrow morning near Kochi and what is the sea state?',
      badge: 'UPWELLING THERMAL FRONTS',
      coord: '09.9312° N, 76.2673° E'
    }
  ];

  return (
    <div className="relative min-h-screen bg-[#EBF7FD] text-[#0A2540] overflow-hidden font-sans selection:bg-sky-500 selection:text-white">
      {/* 1. Generated Live Ocean Imagery Layer */}
      {showSatelliteTexture && (
        <div className="pointer-events-none absolute inset-0 z-0 overflow-hidden opacity-35 mix-blend-multiply transition-opacity duration-700">
          <img
            src={oceanHeroBg}
            alt="Live Ocean Surface Bathymetry"
            referrerPolicy="no-referrer"
            className="h-full w-full object-cover object-center scale-105 animate-pulse"
            style={{ animationDuration: '8s' }}
          />
        </div>
      )}

      {/* 2. Interactive Moving Ocean Swells & Current Particles Canvas */}
      <div className="pointer-events-none absolute inset-0 z-0">
        <OceanCanvasBackground intensity={waveIntensity} />
      </div>

      {/* 3. Ocean Bathymetry Dot Grid Overlay */}
      <div className="pointer-events-none absolute inset-0 z-0 ocean-dot-grid opacity-35" />

      {/* 4. Ambient Oceanic Light Refraction Glows */}
      <div className="pointer-events-none absolute -top-40 left-1/2 h-[550px] w-[70rem] -translate-x-1/2 rounded-full bg-sky-300/35 blur-[140px]" />
      <div className="pointer-events-none absolute bottom-0 right-0 h-[450px] w-[450px] rounded-full bg-cyan-200/40 blur-[130px]" />

      {/* Top Navigation Header */}
      <header className="relative z-10 mx-auto flex max-w-7xl items-center justify-between px-6 py-6 border-b border-sky-200/70 backdrop-blur-md bg-white/40">
        <div className="flex flex-col">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-tr from-sky-600 to-cyan-500 text-white shadow-md shadow-sky-500/30">
              <Waves className="h-4 w-4" />
            </div>
            <span className="font-display text-2xl font-black tracking-tighter uppercase text-[#082F49] leading-none">
              ORCA // 01
            </span>
            <div className="px-2.5 py-0.5 border border-sky-400/40 bg-sky-100/80 rounded-full text-[9px] font-mono tracking-[0.25em] uppercase text-sky-900 font-bold">
              ISRO SAC • INCOIS
            </div>
          </div>
          <span className="text-[10px] tracking-[0.35em] uppercase text-sky-800/70 mt-1 font-mono font-medium">
            Marine Ecosystems Reasoning with Collaborative Agents
          </span>
        </div>

        <nav className="flex items-center gap-4 sm:gap-6">
          {/* Live Swell Controller Chip */}
          <div className="hidden lg:flex items-center gap-2 rounded-full border border-sky-300/70 bg-white/70 px-3 py-1 text-[10px] font-mono font-bold text-sky-950 backdrop-blur-sm shadow-sm">
            <Wind className="h-3.5 w-3.5 text-sky-600" />
            <span>SWELL INTENSITY:</span>
            <button
              onClick={() => setWaveIntensity(prev => (prev === 1 ? 1.7 : prev === 1.7 ? 0.5 : 1))}
              className="rounded-full bg-sky-100 px-2 py-0.5 text-sky-800 hover:bg-sky-200 transition-colors uppercase tracking-wider text-[9px]"
            >
              {waveIntensity === 1 ? 'ACTIVE (1.0x)' : waveIntensity === 1.7 ? 'SURGE (1.7x)' : 'CALM (0.5x)'}
            </button>
            <button
              onClick={() => setShowSatelliteTexture(!showSatelliteTexture)}
              className="ml-1 rounded-full p-1 text-sky-700 hover:bg-sky-100 transition-colors"
              title="Toggle satellite texture backdrop"
            >
              <Eye className="h-3.5 w-3.5" />
            </button>
          </div>

          <div className="hidden sm:flex items-center gap-6 text-[11px] font-mono font-bold tracking-[0.2em] uppercase text-sky-900/80">
            <span className="hover:text-sky-950 transition-colors cursor-pointer" onClick={onEnterWorkspace}>SYSTEMS</span>
            <span className="hover:text-sky-950 transition-colors cursor-pointer" onClick={onEnterWorkspace}>SWAN SPECTRA</span>
            <span className="hover:text-sky-950 transition-colors cursor-pointer" onClick={onEnterWorkspace}>CONSENSUS</span>
          </div>

          <button
            onClick={onEnterWorkspace}
            className="flex items-center gap-2.5 px-6 py-2.5 rounded-full bg-gradient-to-r from-sky-600 to-cyan-600 hover:from-sky-700 hover:to-cyan-700 text-white text-xs font-bold font-mono tracking-[0.15em] uppercase transition-all shadow-lg shadow-sky-600/25"
          >
            <span>Launch v2.6</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 mx-auto max-w-7xl px-6 pt-14 pb-24">
        {/* Category Tracker Rule */}
        <div className="flex items-center gap-4 mb-4">
          <div className="h-[2px] w-20 bg-sky-600" />
          <span className="text-[11px] uppercase tracking-[0.45em] font-mono font-bold text-sky-800">
            Earth Observation Intelligence // Live Ocean Simulation
          </span>
        </div>

        {/* Monumental Bold Display Headline */}
        <h1 className="font-display text-5xl sm:text-7xl md:text-8xl lg:text-9xl font-black tracking-tighter uppercase leading-[0.88] text-[#072448]">
          UNDERSTAND<br />
          <span className="text-stroke-navy text-sky-950/20">THE OCEAN.</span>
        </h1>

        <div className="mt-10 grid grid-cols-1 md:grid-cols-12 gap-8 items-start border-t border-sky-300/50 pt-8">
          <div className="md:col-span-5 space-y-6">
            <p className="text-base sm:text-lg leading-relaxed text-[#0F294A] font-medium">
              A high-density reasoning platform fusing INSAT-3D thermal radiometry, Oceansat-3 bio-optical metrics, and INCOIS SWAN wave spectra through collaborative AI agents to deliver explainable, safety-verified marine decisions.
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-2">
              <button
                onClick={onEnterWorkspace}
                className="flex items-center justify-center gap-3 px-8 py-4 bg-[#082F49] hover:bg-[#0C4A6E] text-white rounded-full text-xs font-black font-mono tracking-[0.2em] uppercase transition-all shadow-xl shadow-sky-900/20"
              >
                <span>ENTER WORKSPACE</span>
                <ArrowRight className="h-4 w-4" />
              </button>

              <button
                onClick={() => onSelectScenario('Where is the most promising and safer fishing area near Chennai tomorrow morning and give me a route?')}
                className="flex items-center justify-center gap-2 px-6 py-4 border border-sky-400 bg-white/70 hover:bg-white text-sky-950 rounded-full text-xs font-bold font-mono tracking-[0.15em] uppercase transition-all backdrop-blur-md shadow-sm"
              >
                <Play className="h-3.5 w-3.5 text-sky-600 fill-sky-600" />
                <span>TRACE REASONING</span>
              </button>
            </div>
          </div>

          <div className="hidden md:block md:col-span-1 border-l border-sky-300/60 h-full" />

          {/* High-density Telemetry Cards with Frosted Light Glass */}
          <div className="md:col-span-6 grid grid-cols-2 gap-5">
            <div className="flex flex-col justify-between p-6 rounded-2xl bg-white/80 border border-sky-200/80 shadow-lg shadow-sky-900/5 backdrop-blur-xl">
              <span className="text-[10px] uppercase font-mono tracking-[0.3em] font-bold text-sky-700 mb-2">PRIMARY COORDINATE</span>
              <span className="text-xl sm:text-2xl font-mono font-bold text-[#082F49]">13.0827° N, 80.2707° E</span>
              <span className="text-[11px] font-bold text-sky-600 font-mono mt-2 flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-sky-500 animate-ping" />
                BAY OF BENGAL SECTOR
              </span>
            </div>

            <div className="flex flex-col justify-between p-6 rounded-2xl bg-white/80 border border-sky-200/80 shadow-lg shadow-sky-900/5 backdrop-blur-xl">
              <span className="text-[10px] uppercase font-mono tracking-[0.3em] font-bold text-sky-700 mb-2">INSPECTION MODEL</span>
              <span className="text-xl sm:text-2xl font-mono font-bold text-[#082F49]">MULTI-AGENT-08</span>
              <span className="text-[11px] font-bold text-emerald-600 font-mono mt-2">DETERMINISTIC CONSENSUS</span>
            </div>

            <div className="col-span-2 p-5 rounded-2xl bg-white/85 border border-sky-200/90 shadow-lg shadow-sky-900/5 backdrop-blur-xl flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-emerald-500 ring-4 ring-emerald-200 animate-pulse" />
                <div>
                  <div className="text-xs font-bold uppercase font-mono tracking-wider text-[#082F49]">Live In-Situ Ocean Telemetry Active</div>
                  <div className="text-[10px] text-sky-800/80 font-mono">INSAT-3D • Oceansat-3 • SWAN Wave Spectra • SAMUDRA</div>
                </div>
              </div>
              <span className="px-3 py-1 border border-emerald-300 bg-emerald-50 rounded-full text-[10px] font-mono font-bold tracking-widest uppercase text-emerald-800">
                AUDIT PASS 6/6
              </span>
            </div>
          </div>
        </div>

        {/* Live Interactive Scenarios Grid */}
        <div className="mt-16 border-t border-sky-300/60 pt-10">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono font-bold tracking-[0.25em] uppercase text-sky-900">
                02 // DYNAMIC INTERACTION SCENARIOS
              </span>
            </div>
            <span className="text-[10px] font-mono tracking-[0.2em] uppercase font-bold text-sky-700/80">
              REAL-TIME SATELLITE COMPILATION PIPELINE
            </span>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {sampleScenarios.map((sc, idx) => (
              <div
                key={idx}
                onClick={() => onSelectScenario(sc.query)}
                className="group cursor-pointer rounded-2xl border border-sky-200/80 bg-white/80 p-6 shadow-md shadow-sky-900/5 backdrop-blur-xl transition-all hover:border-sky-400 hover:bg-white hover:shadow-xl hover:shadow-sky-900/10 hover:-translate-y-0.5"
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-mono font-bold tracking-[0.2em] text-sky-600 uppercase">
                    QUERY-0{idx + 1}
                  </span>
                  <span className="px-3 py-0.5 border border-sky-300 bg-sky-50 rounded-full text-[9px] font-mono font-bold tracking-[0.15em] uppercase text-sky-800">
                    {sc.badge}
                  </span>
                </div>
                <h3 className="text-sm font-bold text-[#082F49] group-hover:text-sky-600 transition-colors mb-2">
                  {sc.title}
                </h3>
                <p className="text-xs text-sky-900/75 leading-relaxed line-clamp-2">
                  "{sc.query}"
                </p>
                <div className="mt-4 flex items-center justify-between border-t border-sky-100 pt-3 text-[10px] font-mono font-medium text-sky-700">
                  <span>{sc.coord}</span>
                  <div className="flex items-center gap-1 font-bold text-sky-900 group-hover:translate-x-1 transition-transform">
                    <span>EXECUTE PIPELINE</span>
                    <ChevronRight className="h-3.5 w-3.5 text-sky-600" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Key Architectural Pillars */}
        <div className="mt-16 grid grid-cols-1 gap-5 sm:grid-cols-3">
          <div className="rounded-2xl border border-sky-200/80 bg-white/80 p-6 shadow-md shadow-sky-900/5 backdrop-blur-xl">
            <div className="text-[10px] font-mono tracking-[0.3em] uppercase font-bold text-sky-600 mb-3">PILLAR // 01</div>
            <h4 className="text-base font-black uppercase font-display tracking-tight text-[#082F49] mb-2">
              Multi-Sensor Grounding
            </h4>
            <p className="text-xs text-sky-900/75 leading-relaxed">
              Ingests INSAT-3D thermal radiometry, Oceansat-3 chlorophyll observations, INCOIS SWAN wave spectra, and SAMUDRA in-situ ocean buoys.
            </p>
          </div>

          <div className="rounded-2xl border border-sky-200/80 bg-white/80 p-6 shadow-md shadow-sky-900/5 backdrop-blur-xl">
            <div className="text-[10px] font-mono tracking-[0.3em] uppercase font-bold text-sky-600 mb-3">PILLAR // 02</div>
            <h4 className="text-base font-black uppercase font-display tracking-tight text-[#082F49] mb-2">
              Dynamic Multi-Agent DAG
            </h4>
            <p className="text-xs text-sky-900/75 leading-relaxed">
              Specialized Ocean, Ecosystem, Fisheries, Safety, and Geospatial agents collaborate dynamically based on user intent and spatial context.
            </p>
          </div>

          <div className="rounded-2xl border border-sky-200/80 bg-white/80 p-6 shadow-md shadow-sky-900/5 backdrop-blur-xl">
            <div className="text-[10px] font-mono tracking-[0.3em] uppercase font-bold text-sky-600 mb-3">PILLAR // 03</div>
            <h4 className="text-base font-black uppercase font-display tracking-tight text-[#082F49] mb-2">
              Provenance & Safety Guard
            </h4>
            <p className="text-xs text-sky-900/75 leading-relaxed">
              Every inference is audited by an independent Verification Agent for provenance, timestamp sanity, scientific causality, and maritime risk.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-sky-300/70 bg-[#0C3259] text-white py-10 px-6">
        <div className="mx-auto max-w-7xl flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-8">
            <div className="flex flex-col">
              <span className="text-[9px] font-mono uppercase tracking-[0.3em] text-sky-300/80 mb-1">SYSTEM STATUS</span>
              <span className="text-xs font-mono font-bold uppercase text-white">OPERATIONAL BUILD 2026.4</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[9px] font-mono uppercase tracking-[0.3em] text-sky-300/80 mb-1">DATA INTEGRITY</span>
              <span className="text-xs font-mono font-bold uppercase text-emerald-300">100% SATELLITE GROUNDED</span>
            </div>
          </div>

          <div className="flex items-center gap-4 text-[10px] font-mono tracking-widest text-sky-200/70 uppercase">
            <span>INSAT-3D</span>
            <span>/</span>
            <span>OCEANSAT-3</span>
            <span>/</span>
            <span>INCOIS SWAN</span>
            <span>/</span>
            <span>NIOT SAMUDRA</span>
          </div>
        </div>
      </footer>
    </div>
  );
};


