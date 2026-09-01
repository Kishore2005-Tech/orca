import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar.tsx';
import { LandingPage } from './components/LandingPage.tsx';
import { AuthModal, PRESET_USERS } from './components/AuthModal.tsx';
import { QueryBar } from './components/QueryBar.tsx';
import { AgentActivityPipeline } from './components/AgentActivityPipeline.tsx';
import { DecisionBanner } from './components/DecisionBanner.tsx';
import { MarineMap } from './components/MarineMap.tsx';
import { EvidenceTable } from './components/EvidenceTable.tsx';
import { ReasoningGraphView } from './components/ReasoningGraphView.tsx';
import { ChartsView } from './components/ChartsView.tsx';
import { RoutePlannerCard } from './components/RoutePlannerCard.tsx';
import { VerificationDrawer } from './components/VerificationDrawer.tsx';
import { ScientificCorpusModal } from './components/ScientificCorpusModal.tsx';
import { OceanCanvasBackground } from './components/OceanCanvasBackground.tsx';
import oceanHeroBg from './assets/images/ocean_hero_bg_1788170791119.jpg';
import { MarineZone, OrcaResponse, UserMode, UserProfile } from './types/orca.ts';

export default function App() {
  const [inWorkspace, setInWorkspace] = useState(false);
  const [activeTab, setActiveTab] = useState<'workspace' | 'map' | 'reasoning' | 'evidence' | 'knowledge'>('workspace');
  const [userMode, setUserMode] = useState<UserMode>('scientist');
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(PRESET_USERS[0]);
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isVerificationOpen, setIsVerificationOpen] = useState(false);
  const [isKnowledgeOpen, setIsKnowledgeOpen] = useState(false);

  const [selectedRegion, setSelectedRegion] = useState('chennai');
  const [timeContext, setTimeContext] = useState('Tomorrow Morning (04:30 - 11:30 IST)');
  const [currentQuery, setCurrentQuery] = useState(
    'Where is the most promising and safer fishing area near Chennai tomorrow morning and give me a route?'
  );

  const [isLoading, setIsLoading] = useState(false);
  const [orcaData, setOrcaData] = useState<OrcaResponse | null>(null);
  const [selectedZone, setSelectedZone] = useState<MarineZone | null>(null);

  // Execute ORCA Reasoning Pipeline
  const executeQuery = async (queryText: string, regionOverride?: string, timeOverride?: string) => {
    setIsLoading(true);
    setCurrentQuery(queryText);
    const reg = regionOverride || selectedRegion;
    const tim = timeOverride || timeContext;

    try {
      const response = await fetch('/api/orca/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: queryText,
          userMode,
          location: { name: reg },
          timeContext: tim
        })
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data: OrcaResponse = await response.json();
      setOrcaData(data);
      if (data.candidateZones && data.candidateZones.length > 0) {
        setSelectedZone(data.candidateZones[0]);
      }
    } catch (err) {
      console.error('Failed to query ORCA API:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Initial load execution
  useEffect(() => {
    executeQuery(currentQuery);
  }, []);

  // Handler to launch from landing page
  const handleLaunchScenario = (scenarioQuery: string) => {
    setInWorkspace(true);
    executeQuery(scenarioQuery);
  };

  if (!inWorkspace) {
    return (
      <LandingPage
        onEnterWorkspace={() => setInWorkspace(true)}
        onSelectScenario={handleLaunchScenario}
      />
    );
  }

  return (
    <div className="relative min-h-screen bg-[#EBF7FD] text-[#0A2540] font-sans selection:bg-sky-500 selection:text-white overflow-hidden">
      {/* 1. Generated Live Ocean Imagery Texture Layer */}
      <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden opacity-30 mix-blend-multiply">
        <img
          src={oceanHeroBg}
          alt="Ocean Imagery Texture"
          referrerPolicy="no-referrer"
          className="h-full w-full object-cover object-center scale-105"
        />
      </div>

      {/* 2. Interactive Moving Ocean Swells & Current Particles Canvas */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <OceanCanvasBackground intensity={0.8} />
      </div>

      {/* 3. Bathymetry Dot Grid Overlay */}
      <div className="pointer-events-none fixed inset-0 z-0 ocean-dot-grid opacity-35" />

      {/* 4. Ambient Oceanic Refraction Glows */}
      <div className="pointer-events-none fixed -top-40 left-1/2 h-[550px] w-[70rem] -translate-x-1/2 rounded-full bg-sky-300/30 blur-[140px]" />
      <div className="pointer-events-none fixed bottom-0 right-0 h-[450px] w-[450px] rounded-full bg-cyan-200/35 blur-[130px]" />

      {/* Top Navbar */}
      <div className="relative z-30">
        <Navbar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          userMode={userMode}
          setUserMode={setUserMode}
          currentUser={currentUser}
          onOpenAuth={() => setIsAuthOpen(true)}
          onLogout={() => setCurrentUser(null)}
          selectedRegion={selectedRegion}
          onSelectRegion={reg => {
            setSelectedRegion(reg);
            executeQuery(currentQuery, reg);
          }}
        />
      </div>

      {/* Main Workspace Body */}
      <main className="relative z-10 mx-auto max-w-7xl px-4 py-8 sm:px-6 space-y-6">
        {/* Natural Language Query Bar */}
        <QueryBar
          currentQuery={currentQuery}
          onExecuteQuery={q => executeQuery(q)}
          isLoading={isLoading}
          selectedRegion={selectedRegion}
          onSelectRegion={reg => {
            setSelectedRegion(reg);
            executeQuery(currentQuery, reg);
          }}
          timeContext={timeContext}
          setTimeContext={t => {
            setTimeContext(t);
            executeQuery(currentQuery, selectedRegion, t);
          }}
        />

        {orcaData && (
          <>
            {/* Dynamic Multi-Agent Execution Status */}
            <AgentActivityPipeline
              activeAgents={orcaData.activeAgents}
              agentResults={orcaData.agentResults}
              isLoading={isLoading}
            />

            {/* ONE-LINE DECISION BANNER (First Priority) */}
            <DecisionBanner
              data={orcaData}
              userMode={userMode}
              onOpenVerification={() => setIsVerificationOpen(true)}
              onOpenKnowledge={() => setIsKnowledgeOpen(true)}
            />

            {/* TAB VIEW CONTENT */}
            {activeTab === 'workspace' && (
              <div className="space-y-6">
                {/* 2-Column Responsive Layout: Map on Left / Supporting Charts on Right */}
                <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
                  <div className="lg:col-span-7">
                    <MarineMap
                      data={orcaData}
                      selectedZone={selectedZone}
                      onSelectZone={z => setSelectedZone(z)}
                    />
                  </div>

                  <div className="lg:col-span-5 space-y-5">
                    {/* Scientific Explanation Summary */}
                    <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-6 shadow-xl shadow-sky-950/5 backdrop-blur-xl font-sans">
                      <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-sky-800 mb-3 flex items-center gap-2">
                        <span className="h-2 w-2 rounded-full bg-sky-600 animate-pulse" />
                        SCIENTIFIC REASONING SYNTHESIS //
                      </h4>
                      <p className="text-xs text-[#0F294A] leading-relaxed font-medium">
                        {orcaData.scientificExplanation}
                      </p>
                    </div>

                    {/* Route Planning Card if applicable */}
                    {orcaData.routePlan && (
                      <RoutePlannerCard routePlan={orcaData.routePlan} />
                    )}
                  </div>
                </div>

                {/* Scientific Oceanographic & SWAN Forecast Charts */}
                <ChartsView chartsData={orcaData.chartsData} />

                {/* Traceable Evidence Grounding Table */}
                <EvidenceTable evidence={orcaData.evidence} />
              </div>
            )}

            {activeTab === 'map' && (
              <div className="space-y-6">
                <MarineMap
                  data={orcaData}
                  selectedZone={selectedZone}
                  onSelectZone={z => setSelectedZone(z)}
                />
                {orcaData.routePlan && <RoutePlannerCard routePlan={orcaData.routePlan} />}
              </div>
            )}

            {activeTab === 'reasoning' && (
              <div className="space-y-6">
                <ReasoningGraphView
                  nodes={orcaData.reasoningGraph.nodes}
                  edges={orcaData.reasoningGraph.edges}
                />
                <ChartsView chartsData={orcaData.chartsData} />
              </div>
            )}

            {activeTab === 'evidence' && (
              <div className="space-y-6">
                <EvidenceTable evidence={orcaData.evidence} />
                <div className="rounded-2xl border border-sky-200/90 bg-white/85 p-6 shadow-xl shadow-sky-950/5 backdrop-blur-xl font-sans">
                  <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-sky-800 mb-4 flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-sky-600" />
                    EARTH OBSERVATION DATA LINEAGE //
                  </h4>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4 font-mono text-xs">
                    {orcaData.sources.map((s, idx) => (
                      <div key={idx} className="rounded-xl border border-sky-200/80 bg-sky-50/80 p-4 shadow-sm">
                        <span className="font-bold text-[#082F49] font-sans text-xs block mb-1">{s.name}</span>
                        <div className="text-[11px] text-sky-700 font-mono font-bold mb-1">{s.sensor}</div>
                        <div className="text-[10px] text-sky-900/70">{s.agency}</div>
                        <div className="text-[9px] text-sky-800/60 mt-2 border-t border-sky-200/60 pt-1">CALIBRATED: {s.lastCalibrated}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'knowledge' && (
              <div className="space-y-6">
                <ReasoningGraphView
                  nodes={orcaData.reasoningGraph.nodes}
                  edges={orcaData.reasoningGraph.edges}
                />
              </div>
            )}
          </>
        )}
      </main>

      {/* Auth Portal Modal */}
      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        onLogin={u => setCurrentUser(u)}
      />

      {/* Verification Audit Drawer */}
      {orcaData && (
        <VerificationDrawer
          isOpen={isVerificationOpen}
          onClose={() => setIsVerificationOpen(false)}
          report={orcaData.verification}
        />
      )}

      {/* Scientific Literature Modal */}
      <ScientificCorpusModal
        isOpen={isKnowledgeOpen || activeTab === 'knowledge'}
        onClose={() => {
          setIsKnowledgeOpen(false);
          if (activeTab === 'knowledge') setActiveTab('workspace');
        }}
      />
    </div>
  );
}
