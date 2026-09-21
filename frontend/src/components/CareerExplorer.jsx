import React, { useState, useEffect } from 'react';
import { 
  Briefcase, 
  Sparkles, 
  TrendingUp, 
  Code2, 
  Cpu, 
  Compass, 
  ChevronRight, 
  CheckCircle2, 
  BookOpen,
  ArrowRight,
  GraduationCap,
  Layers,
  Award
} from 'lucide-react';
import { fetchCareerPaths } from '../services/api';

const STREAM_TABS = [
  { id: 'ALL', label: 'All Streams (24 Careers)' },
  { id: 'PCM', label: 'PCM (Engineering & Tech)' },
  { id: 'PCB', label: 'PCB (Medical & Healthcare)' },
  { id: 'COMMERCE', label: 'Commerce & Finance' },
  { id: 'ARTS', label: 'Arts & Public Policy' }
];

export default function CareerExplorer({ onSelectCareerForRoadmap }) {
  const [careers, setCareers] = useState([]);
  const [selectedStream, setSelectedStream] = useState('ALL');
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedDomain, setSelectedDomain] = useState('All');

  useEffect(() => {
    fetchCareerPaths()
      .then(data => {
        setCareers(data);
        if (data.length > 0) setSelectedCareer(data[0]);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  // Filter by stream first
  const streamFiltered = selectedStream === 'ALL'
    ? careers
    : careers.filter(c => c.stream === selectedStream);

  const domains = ['All', ...new Set(streamFiltered.map(c => c.domain))];

  // Then filter by domain
  const finalCareers = selectedDomain === 'All'
    ? streamFiltered
    : streamFiltered.filter(c => c.domain === selectedDomain);

  // If selected career is no longer in finalCareers, select the first available
  useEffect(() => {
    if (finalCareers.length > 0 && !finalCareers.some(c => c.slug === selectedCareer?.slug)) {
      setSelectedCareer(finalCareers[0]);
    }
  }, [selectedStream, selectedDomain, finalCareers]);

  if (loading) {
    return (
      <div className="py-24 flex justify-center items-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-sm text-slate-600 font-semibold">Loading Cross-Stream Career Knowledge Base...</span>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <span className="text-xs font-bold uppercase tracking-widest text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full">
          Cross-Stream Career Engine
        </span>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 mt-2 tracking-tight">
          Explore High-Growth Careers Across All 4 Streams
        </h1>
        <p className="text-slate-600 text-sm mt-2">
          Understand industry job roles, required technical skills, relevant entrance examinations, degrees, and multi-year milestone roadmaps before locking choices.
        </p>
      </div>

      {/* Stream Tabs Selector */}
      <div className="flex flex-wrap items-center justify-center gap-2 mb-6">
        {STREAM_TABS.map((tab) => {
          const isSelected = selectedStream === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => {
                setSelectedStream(tab.id);
                setSelectedDomain('All');
              }}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                isSelected
                  ? 'bg-slate-900 text-white shadow-md shadow-slate-900/20 ring-2 ring-slate-900/20'
                  : 'bg-white text-slate-700 border border-slate-200 hover:border-slate-400'
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Domain Filter Pills */}
      {domains.length > 2 && (
        <div className="flex flex-wrap items-center justify-center gap-2 mb-8">
          {domains.map((dom) => (
            <button
              key={dom}
              onClick={() => setSelectedDomain(dom)}
              className={`px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                selectedDomain === dom
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {dom}
            </button>
          ))}
        </div>
      )}

      {/* Main Grid: Left List + Right Career Detail */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Career Cards */}
        <div className="lg:col-span-5 space-y-3">
          {finalCareers.map((c) => {
            const isSelected = selectedCareer?.slug === c.slug;
            return (
              <div
                key={c.slug}
                onClick={() => setSelectedCareer(c)}
                className={`p-5 rounded-2xl border-2 transition-all cursor-pointer bg-white ${
                  isSelected
                    ? 'border-blue-600 shadow-md ring-2 ring-blue-500/10'
                    : 'border-slate-200 hover:border-blue-300 hover:shadow-sm'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center space-x-1.5">
                    <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded ${
                      c.stream === 'PCM' ? 'bg-blue-100 text-blue-800' :
                      c.stream === 'PCB' ? 'bg-emerald-100 text-emerald-800' :
                      c.stream === 'COMMERCE' ? 'bg-amber-100 text-amber-800' :
                      'bg-rose-100 text-rose-800'
                    }`}>
                      {c.stream}
                    </span>
                    <span className="text-[11px] font-bold text-slate-500">
                      {c.domain}
                    </span>
                  </div>
                  <span className="text-xs font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                    Avg ₹{c.average_starting_salary_lpa} LPA
                  </span>
                </div>
                <h3 className="text-base font-extrabold text-slate-900 mt-1">
                  {c.title}
                </h3>
                <p className="text-xs text-slate-500 line-clamp-2 mt-1">
                  {c.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* Right Column: Selected Career Deep Dive */}
        {selectedCareer && (
          <div className="lg:col-span-7 bg-white rounded-3xl border border-slate-200 shadow-xl shadow-slate-200/50 p-6 sm:p-8 space-y-6">
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-full uppercase tracking-wider">
                    {selectedCareer.domain}
                  </span>
                  <span className="text-xs font-bold text-slate-500">
                    Stream: {selectedCareer.stream}
                  </span>
                </div>
                <h2 className="text-2xl font-black text-slate-900 mt-1">
                  {selectedCareer.title}
                </h2>
              </div>
              <button
                onClick={() => onSelectCareerForRoadmap(selectedCareer)}
                className="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs flex items-center space-x-1.5 shadow-md shadow-blue-500/20 transition-all self-start sm:self-auto"
              >
                <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                <span>Personalize Roadmap</span>
              </button>
            </div>

            <p className="text-sm text-slate-700 leading-relaxed font-normal">
              {selectedCareer.description}
            </p>

            {/* Metrics Row */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              <div className="p-3 rounded-xl bg-emerald-50/50 border border-emerald-100 text-center">
                <span className="text-[10px] font-bold text-slate-500 uppercase block">Starting CTC</span>
                <span className="text-lg font-black text-emerald-800">₹{selectedCareer.average_starting_salary_lpa} LPA</span>
              </div>
              <div className="p-3 rounded-xl bg-blue-50/50 border border-blue-100 text-center">
                <span className="text-[10px] font-bold text-slate-500 uppercase block">Growth Outlook</span>
                <span className="text-lg font-black text-blue-800">{selectedCareer.growth_outlook}</span>
              </div>
              <div className="p-3 rounded-xl bg-purple-50/50 border border-purple-100 text-center col-span-2 sm:col-span-1">
                <span className="text-[10px] font-bold text-slate-500 uppercase block">Stream</span>
                <span className="text-xs font-bold text-purple-800">{selectedCareer.stream}</span>
              </div>
            </div>

            {/* Recommended Degrees */}
            {selectedCareer.recommended_degrees?.length > 0 && (
              <div>
                <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-700 mb-2 flex items-center space-x-1.5">
                  <GraduationCap className="w-4 h-4 text-emerald-600" />
                  <span>Recommended Degree Programs</span>
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {selectedCareer.recommended_degrees.map((deg, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-50 text-emerald-800 border border-emerald-200"
                    >
                      {deg}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Entrance Examinations */}
            {selectedCareer.entrance_exams?.length > 0 && (
              <div>
                <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-700 mb-2 flex items-center space-x-1.5">
                  <Award className="w-4 h-4 text-purple-600" />
                  <span>Key Entrance & Eligibility Examinations</span>
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {selectedCareer.entrance_exams.map((ex, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-50 text-purple-800 border border-purple-200"
                    >
                      {ex}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Technical Skills Required */}
            <div>
              <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-700 mb-2.5 flex items-center space-x-1.5">
                <Code2 className="w-4 h-4 text-blue-600" />
                <span>Industry Technical & Professional Competencies</span>
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {selectedCareer.required_skills?.map((skill, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-200"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Milestone Roadmap Steps */}
            <div>
              <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-700 mb-3 flex items-center space-x-1.5">
                <Compass className="w-4 h-4 text-amber-600" />
                <span>Multi-Year Professional Roadmap</span>
              </h4>
              <div className="space-y-3">
                {selectedCareer.roadmap_steps?.map((step, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="px-2 py-0.5 rounded text-[10px] font-black uppercase bg-blue-600 text-white">
                        {step.year || `Phase ${idx + 1}`}
                      </span>
                      <span className="text-xs font-bold text-slate-900">
                        {step.goal}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                      {step.actions}
                    </p>
                  </div>
                ))}
              </div>
            </div>

          </div>
        )}

      </div>

    </div>
  );
}
