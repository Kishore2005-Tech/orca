import React from 'react';
import { Compass, ShieldCheck, Waves, Cpu, Database, BookOpen, User, LogOut, Activity, Anchor, MapPin } from 'lucide-react';
import { UserMode, UserProfile } from '../types/orca.ts';

interface NavbarProps {
  activeTab: 'workspace' | 'map' | 'reasoning' | 'evidence' | 'knowledge';
  setActiveTab: (tab: 'workspace' | 'map' | 'reasoning' | 'evidence' | 'knowledge') => void;
  userMode: UserMode;
  setUserMode: (mode: UserMode) => void;
  currentUser: UserProfile | null;
  onOpenAuth: () => void;
  onLogout: () => void;
  selectedRegion: string;
  onSelectRegion: (reg: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  userMode,
  setUserMode,
  currentUser,
  onOpenAuth,
  onLogout,
  selectedRegion,
  onSelectRegion
}) => {
  return (
    <header className="sticky top-0 z-40 border-b border-sky-200/80 bg-white/75 backdrop-blur-md font-sans shadow-sm shadow-sky-900/5">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        {/* Brand & Identity */}
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-sky-600 via-cyan-600 to-sky-700 text-white shadow-md shadow-sky-600/25">
            <Waves className="h-5 w-5 text-white animate-pulse" />
          </div>
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="font-display text-lg font-black tracking-tight text-[#082F49] uppercase">
                ORCA
              </span>
              <span className="px-2 py-0.5 border border-sky-300/80 rounded-full text-[9px] font-mono font-bold tracking-[0.2em] uppercase bg-sky-50 text-sky-800">
                ISRO EO-CORE
              </span>
            </div>
            <span className="text-[9px] uppercase tracking-[0.22em] font-mono text-sky-800/70 hidden sm:block">
              Marine Ecosystems Reasoning Platform
            </span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden items-center gap-1 rounded-full border border-sky-200/90 bg-white/90 p-1 md:flex shadow-inner">
          <button
            onClick={() => setActiveTab('workspace')}
            className={`flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[11px] font-mono font-bold tracking-wider uppercase transition-all ${
              activeTab === 'workspace'
                ? 'bg-[#082F49] text-white shadow-md shadow-sky-950/20'
                : 'text-sky-900/70 hover:text-sky-950 hover:bg-sky-50'
            }`}
          >
            <Activity className="h-3 w-3" />
            <span>Workspace</span>
          </button>

          <button
            onClick={() => setActiveTab('map')}
            className={`flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[11px] font-mono font-bold tracking-wider uppercase transition-all ${
              activeTab === 'map'
                ? 'bg-[#082F49] text-white shadow-md shadow-sky-950/20'
                : 'text-sky-900/70 hover:text-sky-950 hover:bg-sky-50'
            }`}
          >
            <Waves className="h-3 w-3" />
            <span>Marine Map</span>
          </button>

          <button
            onClick={() => setActiveTab('reasoning')}
            className={`flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[11px] font-mono font-bold tracking-wider uppercase transition-all ${
              activeTab === 'reasoning'
                ? 'bg-[#082F49] text-white shadow-md shadow-sky-950/20'
                : 'text-sky-900/70 hover:text-sky-950 hover:bg-sky-50'
            }`}
          >
            <Cpu className="h-3 w-3" />
            <span>Reasoning Graph</span>
          </button>

          <button
            onClick={() => setActiveTab('evidence')}
            className={`flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[11px] font-mono font-bold tracking-wider uppercase transition-all ${
              activeTab === 'evidence'
                ? 'bg-[#082F49] text-white shadow-md shadow-sky-950/20'
                : 'text-sky-900/70 hover:text-sky-950 hover:bg-sky-50'
            }`}
          >
            <Database className="h-3 w-3" />
            <span>Evidence</span>
          </button>

          <button
            onClick={() => setActiveTab('knowledge')}
            className={`flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[11px] font-mono font-bold tracking-wider uppercase transition-all ${
              activeTab === 'knowledge'
                ? 'bg-[#082F49] text-white shadow-md shadow-sky-950/20'
                : 'text-sky-900/70 hover:text-sky-950 hover:bg-sky-50'
            }`}
          >
            <BookOpen className="h-3 w-3" />
            <span>Corpus</span>
          </button>
        </nav>

        {/* User Mode & Authentication */}
        <div className="flex items-center gap-2.5">
          {/* User Mode Switcher */}
          <div className="flex items-center rounded-full border border-sky-200/90 bg-white/90 p-1 text-[10px] font-mono shadow-sm">
            <button
              onClick={() => setUserMode('fisher')}
              className={`flex items-center gap-1 rounded-full px-2.5 py-1 transition-all ${
                userMode === 'fisher' ? 'bg-amber-100 text-amber-900 font-bold border border-amber-300' : 'text-sky-800/70 hover:text-sky-950'
              }`}
              title="Fisher Mode: Actionable Decisions, Safety & Return Route"
            >
              <Anchor className="h-3 w-3" />
              <span className="hidden lg:inline uppercase">Fisher</span>
            </button>
            <button
              onClick={() => setUserMode('scientist')}
              className={`flex items-center gap-1 rounded-full px-2.5 py-1 transition-all ${
                userMode === 'scientist' ? 'bg-sky-100 text-sky-900 font-bold border border-sky-300' : 'text-sky-800/70 hover:text-sky-950'
              }`}
              title="Scientist Mode: Sensor Data, Thermal Fronts & Lineage"
            >
              <Activity className="h-3 w-3" />
              <span className="hidden lg:inline uppercase">Scientist</span>
            </button>
            <button
              onClick={() => setUserMode('operations')}
              className={`flex items-center gap-1 rounded-full px-2.5 py-1 transition-all ${
                userMode === 'operations' ? 'bg-emerald-100 text-emerald-900 font-bold border border-emerald-300' : 'text-sky-800/70 hover:text-sky-950'
              }`}
              title="Maritime Ops Mode: Safety Thresholds & Sector Alerts"
            >
              <ShieldCheck className="h-3 w-3" />
              <span className="hidden lg:inline uppercase">Ops</span>
            </button>
          </div>

          {/* User Profile / Auth Gate */}
          {currentUser ? (
            <div className="flex items-center gap-2 rounded-full border border-sky-200/90 bg-white/90 px-3 py-1 text-xs shadow-sm">
              <div className="flex h-5 w-5 items-center justify-center rounded-full bg-[#082F49] text-white font-mono font-bold text-[10px]">
                {currentUser.name.charAt(0)}
              </div>
              <div className="hidden sm:block text-left font-mono">
                <span className="font-bold text-[#082F49] text-xs">{currentUser.name.split(' ')[0]}</span>
              </div>
              <button
                onClick={onLogout}
                className="ml-1 text-sky-700/60 hover:text-rose-600 transition-colors"
                title="Sign Out"
              >
                <LogOut className="h-3 w-3" />
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenAuth}
              className="flex items-center gap-1.5 rounded-full border border-sky-300 bg-[#082F49] px-3.5 py-1.5 text-xs font-mono font-bold uppercase tracking-wider text-white hover:bg-sky-900 transition-all shadow-sm"
            >
              <User className="h-3 w-3" />
              <span>Sign In</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

