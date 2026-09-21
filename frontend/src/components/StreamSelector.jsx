import React from 'react';
import { Cpu, Dna, TrendingUp, Palette, CheckCircle2 } from 'lucide-react';

const STREAMS = [
  {
    id: 'PCM',
    title: 'PCM',
    subtitle: 'Physics • Chemistry • Mathematics',
    description: 'Engineering, Computer Science, AI/ML, Electronics, Core & BITSAT/State CETs.',
    icon: Cpu,
    color: 'from-blue-600 via-indigo-600 to-purple-600',
    accentBorder: 'border-blue-500',
    badge: 'Engineering & Tech (JEE/WBJEE/BITSAT)',
    active: true,
    exams: 'JEE Main, JEE Advanced, WBJEE, COMEDK, BITSAT'
  },
  {
    id: 'PCB',
    title: 'PCB',
    subtitle: 'Physics • Chemistry • Biology',
    description: 'Medicine (MBBS), Dental (BDS), AYUSH, Veterinary, Pharmacy, Biotechnology.',
    icon: Dna,
    color: 'from-emerald-500 via-teal-600 to-cyan-600',
    accentBorder: 'border-emerald-500',
    badge: 'Medical & Healthcare (NEET-UG)',
    active: true,
    exams: 'NEET-UG (MBBS/BDS), AYUSH, Pharmacy'
  },
  {
    id: 'COMMERCE',
    title: 'Commerce',
    subtitle: 'Business • Finance • Economics',
    description: 'Chartered Accountancy (CA), CS, CMA, Investment Banking, CUET & IIM IPMAT.',
    icon: TrendingUp,
    color: 'from-amber-500 via-orange-500 to-rose-500',
    accentBorder: 'border-amber-500',
    badge: 'CA/CS/CMA & Finance (CUET/IPMAT)',
    active: true,
    exams: 'CA Foundation, CSEET, CMA, CUET-UG, IPMAT'
  },
  {
    id: 'ARTS',
    title: 'Arts / Humanities',
    subtitle: 'Law • Governance • Creative Media',
    description: 'Civil Services (UPSC), Law (CLAT/NLUs), Psychology, Journalism & Policy.',
    icon: Palette,
    color: 'from-pink-500 via-rose-500 to-purple-600',
    accentBorder: 'border-rose-500',
    badge: 'Law & Civil Services (CLAT/UPSC)',
    active: true,
    exams: 'UPSC CSE, CLAT (NLUs), CUET-UG, UGC-NET'
  }
];

export default function StreamSelector({ selectedStream, onSelectStream }) {
  return (
    <div className="mb-12">
      <div className="text-center max-w-2xl mx-auto mb-8">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-black tracking-wider uppercase bg-white/80 border border-slate-200/80 text-purple-700 shadow-xs backdrop-blur-md">
          <span>✨ Curated Stream Ecosystems</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-slate-900 mt-2 tracking-tight">
          Select Your Academic Stream
        </h2>
        <p className="text-slate-600 text-xs sm:text-sm mt-1.5 font-medium">
          Choose your Class 11-12 curriculum to load verified cutoff models, syllabus roadmaps, and career matrices.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {STREAMS.map((st) => {
          const Icon = st.icon;
          const isSelected = selectedStream === st.id;

          return (
            <div
              key={st.id}
              onClick={() => {
                if (st.active) onSelectStream(st.id);
              }}
              className={`relative rounded-3xl p-5 sm:p-6 transition-all duration-300 cursor-pointer backdrop-blur-md ${
                isSelected
                  ? `bg-white/90 ${st.accentBorder} border-2 shadow-glass-hover ring-4 ring-purple-500/10 scale-[1.02]`
                  : 'bg-white/60 hover:bg-white/90 border border-white/80 hover:border-slate-300/80 shadow-glass hover:shadow-glass-hover hover:-translate-y-0.5'
              }`}
            >
              {isSelected && (
                <div className="absolute top-4 right-4">
                  <div className="w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center shadow-sm">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  </div>
                </div>
              )}

              <div className={`w-12 h-12 rounded-2xl bg-gradient-to-tr ${st.color} text-white flex items-center justify-center mb-4 shadow-md shadow-purple-500/15`}>
                <Icon className="w-6 h-6" />
              </div>

              <div className="flex items-center space-x-2 mb-1">
                <h3 className="text-lg font-black text-slate-900 tracking-tight">{st.title}</h3>
                <span className="text-[11px] text-slate-500 font-medium truncate">({st.subtitle.split('•')[0]}...)</span>
              </div>

              <p className="text-xs text-slate-600 mb-4 line-clamp-2 leading-relaxed">
                {st.description}
              </p>

              <div className="pt-3 border-t border-slate-100/80">
                <span
                  className="inline-block text-[10px] font-extrabold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-800 border border-slate-200/60"
                >
                  {st.badge}
                </span>
                <p className="text-[10px] text-slate-400 mt-1.5 font-medium truncate">
                  {st.exams}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
