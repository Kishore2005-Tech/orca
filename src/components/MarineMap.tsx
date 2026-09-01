import React, { useState } from 'react';
import { Layers, Eye, EyeOff, Navigation, ZoomIn, ZoomOut, Compass, MapPin, Waves, Anchor, Info, AlertTriangle, ShieldCheck } from 'lucide-react';
import { MarineZone, OrcaResponse, RoutePlan } from '../types/orca.ts';

interface MarineMapProps {
  data: OrcaResponse;
  selectedZone: MarineZone | null;
  onSelectZone: (zone: MarineZone) => void;
}

export const MarineMap: React.FC<MarineMapProps> = ({ data, selectedZone, onSelectZone }) => {
  const [showSstLayer, setShowSstLayer] = useState(true);
  const [showChlaLayer, setShowChlaLayer] = useState(true);
  const [showWaveLayer, setShowWaveLayer] = useState(true);
  const [showRouteLayer, setShowRouteLayer] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(1);

  const { parsedIntent, candidateZones, routePlan } = data;
  const origin = parsedIntent?.location || { name: 'Chennai', latitude: 13.0827, longitude: 80.2707 };
  const originLat = typeof origin?.latitude === 'number' ? origin.latitude : 13.0827;
  const originLon = typeof origin?.longitude === 'number' ? origin.longitude : 80.2707;
  const originName = origin?.name || 'Chennai';
  const activeZone = selectedZone || (candidateZones && candidateZones[0]) || null;

  return (
    <div className="relative flex flex-col rounded-2xl border border-sky-200/90 bg-white/90 overflow-hidden shadow-xl shadow-sky-950/5 font-sans backdrop-blur-xl">
      {/* Map Control Bar */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-sky-200/80 bg-sky-50/90 px-5 py-3 z-20 text-xs">
        <div className="flex items-center gap-3">
          <Compass className="h-4 w-4 text-sky-700" />
          <span className="font-mono font-bold uppercase tracking-wider text-[#082F49]">
            {originName} SECTOR // 01
          </span>
          <span className="rounded-full border border-sky-300 bg-white px-2.5 py-0.5 text-[9px] font-mono text-sky-800 font-bold shadow-xs">
            {originLat.toFixed(2)}°N, {originLon.toFixed(2)}°E
          </span>
        </div>

        {/* Layer Toggles */}
        <div className="flex flex-wrap items-center gap-1.5">
          <button
            onClick={() => setShowSstLayer(!showSstLayer)}
            className={`flex items-center gap-1 rounded-full px-3 py-1 text-[10px] font-mono font-bold tracking-wider uppercase transition-all shadow-xs ${
              showSstLayer
                ? 'bg-rose-500 text-white border border-rose-600'
                : 'bg-white text-sky-900/60 border border-sky-200 hover:text-sky-900'
            }`}
          >
            <span>SST</span>
          </button>

          <button
            onClick={() => setShowChlaLayer(!showChlaLayer)}
            className={`flex items-center gap-1 rounded-full px-3 py-1 text-[10px] font-mono font-bold tracking-wider uppercase transition-all shadow-xs ${
              showChlaLayer
                ? 'bg-emerald-600 text-white border border-emerald-700'
                : 'bg-white text-sky-900/60 border border-sky-200 hover:text-sky-900'
            }`}
          >
            <span>CHL-A</span>
          </button>

          <button
            onClick={() => setShowWaveLayer(!showWaveLayer)}
            className={`flex items-center gap-1 rounded-full px-3 py-1 text-[10px] font-mono font-bold tracking-wider uppercase transition-all shadow-xs ${
              showWaveLayer
                ? 'bg-cyan-600 text-white border border-cyan-700'
                : 'bg-white text-sky-900/60 border border-sky-200 hover:text-sky-900'
            }`}
          >
            <span>SWELL</span>
          </button>

          <button
            onClick={() => setShowRouteLayer(!showRouteLayer)}
            className={`flex items-center gap-1 rounded-full px-3 py-1 text-[10px] font-mono font-bold tracking-wider uppercase transition-all shadow-xs ${
              showRouteLayer
                ? 'bg-[#082F49] text-white border border-[#082F49]'
                : 'bg-white text-sky-900/60 border border-sky-200 hover:text-sky-900'
            }`}
          >
            <span>ROUTE</span>
          </button>

          {/* Zoom controls */}
          <div className="flex items-center rounded-full border border-sky-300 bg-white p-0.5 ml-2 shadow-xs">
            <button
              onClick={() => setZoomLevel(Math.min(1.5, zoomLevel + 0.15))}
              className="p-1 text-sky-700 hover:text-[#082F49]"
              title="Zoom In"
            >
              <ZoomIn className="h-3 w-3" />
            </button>
            <button
              onClick={() => setZoomLevel(Math.max(0.7, zoomLevel - 0.15))}
              className="p-1 text-sky-700 hover:text-[#082F49]"
              title="Zoom Out"
            >
              <ZoomOut className="h-3 w-3" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Interactive SVG Vector Stage */}
      <div className="relative h-[480px] w-full overflow-hidden bg-[#0c2a44] select-none">
        <svg
          viewBox="0 0 800 480"
          className="h-full w-full transition-transform duration-300"
          style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'center center' }}
        >
          <defs>
            {/* Gradients for SST & Ocean */}
            <radialGradient id="sstHeatmap1" cx="60%" cy="40%" r="50%">
              <stop offset="0%" stopColor="#f43f5e" stopOpacity="0.45" />
              <stop offset="60%" stopColor="#fb923c" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#0284c7" stopOpacity="0" />
            </radialGradient>

            <radialGradient id="chlaBloom" cx="65%" cy="35%" r="40%">
              <stop offset="0%" stopColor="#10b981" stopOpacity="0.45" />
              <stop offset="50%" stopColor="#14b8a6" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#0f172a" stopOpacity="0" />
            </radialGradient>

            <linearGradient id="routeGradient" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#ffffff" />
              <stop offset="100%" stopColor="#38bdf8" />
            </linearGradient>

            <linearGradient id="returnGradient" x1="100%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor="#34d399" />
            </linearGradient>

            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#164e63" strokeWidth="0.75" strokeDasharray="2 2" />
            </pattern>
          </defs>

          {/* Background Navigational Grid */}
          <rect width="800" height="480" fill="#082338" />
          <rect width="800" height="480" fill="url(#grid)" />

          {/* Coastal Landmass Silhouette */}
          <path
            d="M 0 0 L 140 0 C 135 120, 160 220, 170 300 C 180 370, 150 440, 130 480 L 0 480 Z"
            fill="#061826"
            stroke="#0e3b5e"
            strokeWidth="2"
          />

          {/* 50m and 100m Bathymetric Contour Lines */}
          <path
            d="M 190 0 C 210 140, 240 260, 270 380 C 290 430, 260 480, 240 480"
            fill="none"
            stroke="#155e75"
            strokeWidth="1.2"
            strokeDasharray="4 4"
            opacity="0.8"
          />
          <text x="235" y="460" fill="#38bdf8" fontSize="9" fontFamily="JetBrains Mono" opacity="0.9">50m Bathymetry</text>

          <path
            d="M 280 0 C 310 130, 360 250, 420 370 C 450 430, 430 480, 410 480"
            fill="none"
            stroke="#0e7490"
            strokeWidth="1.2"
            strokeDasharray="6 4"
            opacity="0.7"
          />
          <text x="390" y="460" fill="#22d3ee" fontSize="9" fontFamily="JetBrains Mono" opacity="0.9">100m Shelf Break</text>

          {/* SST Heatmap Layer */}
          {showSstLayer && (
            <ellipse cx="500" cy="180" rx="220" ry="140" fill="url(#sstHeatmap1)" />
          )}

          {/* Chlorophyll-a Layer */}
          {showChlaLayer && (
            <ellipse cx="480" cy="170" rx="170" ry="110" fill="url(#chlaBloom)" />
          )}

          {/* Wave Swell Vectors Layer */}
          {showWaveLayer && (
            <g opacity="0.6" stroke="#bae6fd" strokeWidth="1.5">
              {[
                { x: 340, y: 110, angle: 65 },
                { x: 420, y: 130, angle: 70 },
                { x: 500, y: 150, angle: 65 },
                { x: 380, y: 220, angle: 75 },
                { x: 480, y: 240, angle: 70 },
                { x: 580, y: 210, angle: 60 },
                { x: 320, y: 320, angle: 80 },
                { x: 440, y: 340, angle: 75 },
                { x: 540, y: 310, angle: 70 }
              ].map((arrow, i) => (
                <g key={i} transform={`translate(${arrow.x}, ${arrow.y}) rotate(${arrow.angle})`}>
                  <line x1="-12" y1="0" x2="12" y2="0" />
                  <polyline points="6,-4 12,0 6,4" fill="none" />
                </g>
              ))}
            </g>
          )}

          {/* Outbound Route Line */}
          {showRouteLayer && routePlan && (
            <>
              {/* Outbound polyline */}
              <path
                d="M 175 290 Q 320 250, 490 170"
                fill="none"
                stroke="url(#routeGradient)"
                strokeWidth="3.5"
                strokeDasharray="none"
              />

              {/* Return polyline with dogleg */}
              <path
                d="M 490 170 C 440 230, 310 320, 175 290"
                fill="none"
                stroke="url(#returnGradient)"
                strokeWidth="2.5"
                strokeDasharray="6 4"
                opacity="0.9"
              />

              {/* Waypoints */}
              <circle cx="175" cy="290" r="5" fill="#ffffff" stroke="#082F49" strokeWidth="2" />
              <circle cx="320" cy="245" r="4" fill="#38bdf8" stroke="#ffffff" strokeWidth="1.5" />
              <circle cx="410" cy="205" r="4" fill="#38bdf8" stroke="#ffffff" strokeWidth="1.5" />
              <circle cx="490" cy="170" r="7" fill="#10b981" stroke="#ffffff" strokeWidth="2.5" />
            </>
          )}

          {/* Candidate Zones Markers */}
          {candidateZones.map((zone, idx) => {
            const zx = 490 + (idx === 1 ? -60 : idx === 2 ? 80 : 0);
            const zy = 170 + (idx === 1 ? 90 : idx === 2 ? 100 : 0);
            const isSelected = activeZone?.id === zone.id;

            return (
              <g
                key={zone.id}
                onClick={() => onSelectZone(zone)}
                className="cursor-pointer group"
                transform={`translate(${zx}, ${zy})`}
              >
                {/* Outer Pulse Ring if Selected */}
                {isSelected && (
                  <circle r="22" fill="none" stroke="#ffffff" strokeWidth="2" opacity="0.9" className="animate-ping" />
                )}

                {/* PFZ Polygon Boundary */}
                <circle
                  r="16"
                  fill={zone.suitabilityScore >= 80 ? '#065f46' : '#1e293b'}
                  fillOpacity="0.85"
                  stroke={zone.suitabilityScore >= 80 ? '#34d399' : '#ffffff'}
                  strokeWidth={isSelected ? 3 : 1.5}
                />

                {/* Score Marker */}
                <text
                  textAnchor="middle"
                  dy="4"
                  fill="#ffffff"
                  fontSize="10"
                  fontFamily="JetBrains Mono"
                  fontWeight="bold"
                >
                  {zone.suitabilityScore}
                </text>

                {/* Zone Label Card */}
                <g transform="translate(20, -10)">
                  <rect
                    width="140"
                    height="32"
                    rx="6"
                    fill="#082F49"
                    fillOpacity="0.95"
                    stroke={isSelected ? '#38bdf8' : '#0369a1'}
                    strokeWidth={isSelected ? "1.5" : "1"}
                  />
                  <text x="8" y="14" fill="#ffffff" fontSize="10" fontFamily="Space Grotesk" fontWeight="bold">
                    {zone.name.split(' ')[0]} ({zone.code.split('-').pop()})
                  </text>
                  <text x="8" y="25" fill="#7dd3fc" fontSize="8" fontFamily="JetBrains Mono">
                    {zone.distanceNm} NM • {zone.sstCelsius}°C • Hs {zone.waveHeightM}m
                  </text>
                </g>
              </g>
            );
          })}

          {/* User GPS Origin Port */}
          <g transform="translate(175, 290)">
            <circle r="8" fill="#ffffff" stroke="#082F49" strokeWidth="2.5" />
            <g transform="translate(-50, -25)">
              <rect width="100" height="20" rx="4" fill="#082F49" fillOpacity="0.95" stroke="#38bdf8" strokeWidth="1" />
              <text x="50" y="13" textAnchor="middle" fill="#ffffff" fontSize="9" fontFamily="JetBrains Mono" fontWeight="bold">
                {originName.split(' ')[0]} PORT
              </text>
            </g>
          </g>
        </svg>

        {/* On-Map Legend Overlay */}
        <div className="pointer-events-none absolute bottom-4 left-4 rounded-xl border border-sky-200/80 bg-white/90 p-3 text-[10px] text-sky-950 backdrop-blur-md font-mono shadow-lg">
          <div className="font-bold text-[#082F49] mb-2 uppercase tracking-widest text-[9px]">MAP LEGEND //</div>
          <div className="space-y-1.5 font-semibold">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
              <span>HIGH SUITABILITY (≥80)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-slate-400" />
              <span>MODERATE SUITABILITY</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-1 w-4 bg-sky-500 rounded" />
              <span>OUTBOUND TRACK</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-1 w-4 bg-amber-500 rounded" />
              <span>SAFE RETURN CORRIDOR</span>
            </div>
          </div>
        </div>

        {/* Selected Zone Inspector Floating Drawer */}
        {activeZone && (
          <div className="absolute top-4 right-4 w-72 rounded-2xl border border-sky-200/90 bg-white/95 p-4 text-xs text-sky-950 shadow-2xl backdrop-blur-md font-mono">
            <div className="flex items-center justify-between mb-3 border-b border-sky-200 pb-2">
              <span className="font-bold text-[#082F49] font-display uppercase tracking-tight">{activeZone.name}</span>
              <span className="rounded-full border border-sky-300 bg-sky-100 px-2 py-0.5 text-[9px] font-bold text-sky-950">
                SCORE {activeZone.suitabilityScore}
              </span>
            </div>

            <div className="space-y-2 text-[11px] text-sky-950">
              <div className="flex justify-between">
                <span className="text-sky-700 font-medium">DISTANCE:</span>
                <span className="font-bold text-[#082F49]">{activeZone.distanceNm} NM ({activeZone.bearingDeg}°)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sky-700 font-medium">SST:</span>
                <span className="font-bold text-rose-600">{activeZone.sstCelsius}°C (FRONT: {activeZone.thermalGradientCPerKm}°C/km)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sky-700 font-medium">CHL-A:</span>
                <span className="font-bold text-emerald-700">{activeZone.chlorophyllMgM3} mg/m³</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sky-700 font-medium">SWELL (Hs):</span>
                <span className="font-bold text-sky-700">{activeZone.waveHeightM}m ({activeZone.windSpeedKnots} kts)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sky-700 font-medium">STATUS:</span>
                <span className={`font-bold ${activeZone.safetyStatus === 'SAFE' ? 'text-emerald-700' : 'text-amber-700'}`}>
                  {activeZone.safetyStatus}
                </span>
              </div>
            </div>

            <p className="mt-3 text-[10px] text-sky-800 border-t border-sky-100 pt-2 leading-relaxed font-sans font-medium">
              {activeZone.summary}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

