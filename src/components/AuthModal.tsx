import React, { useState } from 'react';
import { X, ShieldCheck, UserCheck, Anchor, Waves, Lock, ArrowRight, Check } from 'lucide-react';
import { UserProfile } from '../types/orca.ts';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLogin: (user: UserProfile) => void;
}

export const PRESET_USERS: UserProfile[] = [
  {
    id: 'user-sci-1',
    name: 'Dr. Ananya Sharma',
    email: 'ananya.sharma@isro.gov.in',
    role: 'Researcher / Oceanographer',
    organization: 'ISRO Space Applications Centre (SAC)',
    defaultRegion: 'Chennai Coast (Coromandel)'
  },
  {
    id: 'user-fish-1',
    name: 'Murugan Velayudham',
    email: 'murugan.v@artisanal-fisher.org',
    role: 'Commercial Fisher',
    organization: 'Tamil Nadu Mechanized Fishermen Federation',
    defaultRegion: 'Chennai Coast (Coromandel)'
  },
  {
    id: 'user-ops-1',
    name: 'Cmdr. Rajesh Nambiar',
    email: 'ops.commander@coastguard.gov.in',
    role: 'Maritime Operations Officer',
    organization: 'Indian Coast Guard Eastern Seaboard',
    defaultRegion: 'Bay of Bengal Maritime Sector'
  }
];

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, onLogin }) => {
  const [emailInput, setEmailInput] = useState('');
  const [nameInput, setNameInput] = useState('');

  if (!isOpen) return null;

  const handleCustomLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!emailInput) return;
    const user: UserProfile = {
      id: `user-custom-${Date.now()}`,
      name: nameInput || emailInput.split('@')[0],
      email: emailInput,
      role: 'Researcher / Oceanographer',
      organization: 'Maritime Research Affiliate',
      defaultRegion: 'Chennai Coast'
    };
    onLogin(user);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#082F49]/40 p-4 backdrop-blur-md font-sans">
      <div className="relative w-full max-w-md rounded-2xl border border-sky-200/90 bg-white/95 p-6 shadow-2xl backdrop-blur-xl">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4 rounded-full p-2 text-sky-800 hover:bg-sky-100 hover:text-sky-950 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Modal Header */}
        <div className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-sky-100 text-sky-700 border border-sky-200 shadow-xs">
            <Lock className="h-5 w-5" />
          </div>
          <h3 className="text-lg font-mono font-bold uppercase tracking-wider text-[#082F49]">ORCA ACCESS PORTAL</h3>
          <p className="mt-1 text-xs text-sky-800/80 font-mono">
            Authenticate to access live Earth observation pipelines and multi-agent consensus
          </p>
        </div>

        {/* Quick Instant Role Selector */}
        <div className="mb-6">
          <label className="mb-2 block text-[10px] font-mono font-bold uppercase tracking-wider text-sky-800/70">
            SELECT PRESET PROFILE //
          </label>
          <div className="space-y-2">
            {PRESET_USERS.map(u => (
              <button
                key={u.id}
                onClick={() => {
                  onLogin(u);
                  onClose();
                }}
                className="flex w-full items-center justify-between rounded-xl border border-sky-200/80 bg-sky-50/70 p-3 text-left transition-all hover:border-sky-400 hover:bg-white shadow-xs"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-sky-700 border border-sky-200 shadow-xs">
                    {u.role.includes('Researcher') ? (
                      <Waves className="h-4 w-4" />
                    ) : u.role.includes('Fisher') ? (
                      <Anchor className="h-4 w-4" />
                    ) : (
                      <ShieldCheck className="h-4 w-4" />
                    )}
                  </div>
                  <div>
                    <div className="text-xs font-bold text-[#082F49] font-sans">{u.name}</div>
                    <div className="text-[10px] text-sky-700/80 font-mono font-medium">{u.role}</div>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-sky-500" />
              </button>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div className="relative mb-6 text-center">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-sky-100" />
          </div>
          <span className="relative bg-white px-3 text-[9px] font-mono font-bold text-sky-800/70 uppercase tracking-widest">
            OR SIGN IN WITH EMAIL
          </span>
        </div>

        {/* Custom Auth Form */}
        <form onSubmit={handleCustomLogin} className="space-y-3 font-mono">
          <div>
            <input
              type="text"
              placeholder="Your Full Name"
              value={nameInput}
              onChange={e => setNameInput(e.target.value)}
              className="w-full rounded-xl border border-sky-200 bg-sky-50/50 px-4 py-2.5 text-xs text-[#082F49] placeholder-sky-800/40 focus:border-sky-500 focus:bg-white focus:outline-none shadow-xs"
            />
          </div>
          <div>
            <input
              type="email"
              placeholder="Work Email (e.g., user@domain.gov.in)"
              value={emailInput}
              onChange={e => setEmailInput(e.target.value)}
              className="w-full rounded-xl border border-sky-200 bg-sky-50/50 px-4 py-2.5 text-xs text-[#082F49] placeholder-sky-800/40 focus:border-sky-500 focus:bg-white focus:outline-none shadow-xs"
              required
            />
          </div>
          <button
            type="submit"
            className="flex w-full items-center justify-center gap-2 rounded-full bg-[#082F49] py-2.5 text-xs font-mono font-bold uppercase tracking-wider text-white hover:bg-sky-900 transition-all shadow-md shadow-sky-950/20"
          >
            <span>AUTHENTICATE SESSION</span>
            <UserCheck className="h-4 w-4" />
          </button>
        </form>

        <p className="mt-4 text-center text-[9px] text-sky-800/60 font-mono font-semibold uppercase tracking-wider">
          PROTECTED BY ORCA ENTERPRISE & PROVENANCE PROTOCOLS
        </p>
      </div>
    </div>
  );
};

