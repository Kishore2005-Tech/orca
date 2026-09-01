import React from 'react';
import { X, BookOpen, ExternalLink, Award, FileText, CheckCircle2 } from 'lucide-react';

interface ScientificCorpusModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ScientificCorpusModal: React.FC<ScientificCorpusModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  const citations = [
    {
      title: 'Validation and Operational Methodology of Potential Fishing Zones (PFZ) Advisories in the Indian Seas',
      authors: 'Nayak, S., Solanki, H. U., Dwivedi, R. M., & Choudhury, S. B.',
      source: 'Current Science / INCOIS Special Scientific Publication',
      year: 2021,
      agency: 'INCOIS & ISRO Space Applications Centre',
      keyFinding:
        'Demonstrates that synchronous co-location of satellite thermal fronts (SST gradients >= 0.5°C/km) with chlorophyll-a color edges results in a 60–70% increase in pelagic catch-per-unit-effort (CPUE) for carangid and mackerel species.'
    },
    {
      title: 'Physical Mechanisms Driving Phytoplankton Blooms and Upwelling in the Southwest Bay of Bengal and Malabar Coast',
      authors: 'Vinayachandran, P. N., & Mathew, S.',
      source: 'Journal of Geophysical Research: Oceans',
      year: 2022,
      agency: 'Indian Institute of Science & National Institute of Oceanography',
      keyFinding:
        'Wind-driven coastal divergence stimulates subsurface nutrient pumping, leading to chlorophyll-a blooms within 48 to 72 hours. Plankton serves as a trophic foundation rather than a direct instantaneous fish locator.'
    },
    {
      title: 'High-Resolution SWAN Numerical Wave Modelling and Coastal Risk Verification along the Indian Peninsular Shelf',
      authors: 'Kumar, V. S., & Balakrishnan, N.',
      source: 'Ocean Engineering Review',
      year: 2023,
      agency: 'National Institute of Ocean Technology (NIOT)',
      keyFinding:
        'Diurnal coastal breeze amplification generates steep sea state steepness in afternoon hours. Morning transit corridors (04:30 - 11:30 IST) offer the safest operational window for artisanal craft.'
    }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#082F49]/40 p-4 backdrop-blur-md font-sans">
      <div className="relative w-full max-w-2xl rounded-2xl border border-sky-200/90 bg-white/95 p-6 shadow-2xl backdrop-blur-xl">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 rounded-full p-2 text-sky-800 hover:bg-sky-100 hover:text-sky-950 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        <div className="flex items-center gap-3 border-b border-sky-100 pb-4 mb-5">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-100 text-sky-700 border border-sky-200 shadow-xs">
            <BookOpen className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-base font-mono font-bold uppercase tracking-wider text-[#082F49]">ORCA SCIENTIFIC CORPUS RAG</h3>
            <p className="text-xs text-sky-800/80 font-mono">Peer-reviewed literature & INCOIS standard operational procedures</p>
          </div>
        </div>

        <div className="space-y-3.5 max-h-80 overflow-y-auto pr-1">
          {citations.map((c, i) => (
            <div key={i} className="rounded-xl border border-sky-200/80 bg-sky-50/70 p-4 text-xs font-mono shadow-xs">
              <div className="flex items-start justify-between gap-2 mb-2">
                <h4 className="font-bold text-[#082F49] font-sans text-xs">{c.title}</h4>
                <span className="rounded-full border border-sky-300 bg-white px-2.5 py-0.5 text-[9px] font-bold text-[#082F49] whitespace-nowrap shadow-xs">
                  {c.year}
                </span>
              </div>
              <div className="text-[11px] text-sky-800/80 mb-2.5 font-medium">
                <span>{c.authors} • </span>
                <span className="italic text-sky-950">{c.source}</span>
              </div>
              <div className="rounded-lg bg-white/90 p-3 text-[11px] text-sky-900 border border-sky-200 font-sans leading-relaxed shadow-xs">
                <span className="font-bold text-[#082F49] font-mono uppercase text-[10px] block mb-1">EMPIRICAL FINDING //</span>
                <span>{c.keyFinding}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 text-right">
          <button
            onClick={onClose}
            className="rounded-full bg-[#082F49] px-6 py-2 text-xs font-mono font-bold uppercase tracking-wider text-white hover:bg-sky-900 transition-colors shadow-md shadow-sky-950/20"
          >
            DISMISS
          </button>
        </div>
      </div>
    </div>
  );
};

