import React, { useState, useEffect } from 'react';
import { 
  Search, 
  SlidersHorizontal, 
  ChevronDown, 
  Sparkles, 
  X, 
  Layers,
  ArrowRight
} from 'lucide-react';

export default function StickySearchBar({
  exams,
  selectedExam,
  onSelectExam,
  examMeta,
  searchParams,
  onSearch,
  loading,
  totalColleges,
  totalBranches
}) {
  const [examCode, setExamCode] = useState(selectedExam?.code || 'JEE_MAIN');
  const [counselling, setCounselling] = useState(searchParams?.counselling || 'JOSAA');
  const [rank, setRank] = useState(searchParams?.rank || 4000);
  const [category, setCategory] = useState(searchParams?.category || 'OPEN');
  const [quota, setQuota] = useState(searchParams?.quota || 'All');
  const [branch, setBranch] = useState(searchParams?.branch || '');
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  // Sync state when props change
  useEffect(() => {
    if (selectedExam) {
      setExamCode(selectedExam.code);
    }
  }, [selectedExam]);

  useEffect(() => {
    if (examMeta) {
      if (examMeta.default_counselling) {
        setCounselling(examMeta.default_counselling);
      } else if (examMeta.admission_systems?.length) {
        setCounselling(examMeta.admission_systems[0].code);
      }
      if (examMeta.categories?.length) {
        setCategory(prev => {
          if (examMeta.categories.includes(prev)) return prev;
          return examMeta.categories.includes('OPEN') ? 'OPEN' : examMeta.categories[0];
        });
      }
      setQuota('All');
    }
  }, [examMeta]);

  useEffect(() => {
    if (searchParams) {
      if (searchParams.rank) setRank(searchParams.rank);
      if (searchParams.category) setCategory(searchParams.category);
      if (searchParams.quota) setQuota(searchParams.quota);
      if (searchParams.counselling) setCounselling(searchParams.counselling);
      if (searchParams.branch !== undefined) setBranch(searchParams.branch);
    }
  }, [searchParams]);

  const handleExamChange = (newCode) => {
    setExamCode(newCode);
    const matched = exams.find(e => e.code === newCode);
    if (matched) {
      onSelectExam(matched);
    }
  };

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    onSearch({
      exam_code: examCode,
      counselling: counselling || undefined,
      rank: Number(rank) || 4000,
      category,
      quota,
      branch: branch || undefined,
      mode: branch ? 'B' : 'A',
      page: 1
    });
    setMobileDrawerOpen(false);
  };

  const formatRank = (val) => {
    const num = Number(val);
    return isNaN(num) ? val : num.toLocaleString();
  };

  return (
    <>
      {/* Sticky Top Bar for Desktop */}
      <div className="sticky top-0 z-40 bg-slate-900/95 backdrop-blur-md border-b border-slate-800 text-white shadow-xl transition-all hidden md:block">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5">
          <form onSubmit={handleSubmit} className="flex items-center justify-between gap-3 text-xs">
            
            {/* 1. Exam Switcher */}
            <div className="flex items-center space-x-2 shrink-0">
              <span className="font-bold text-slate-400 uppercase tracking-wider text-[11px]">Exam:</span>
              <div className="relative">
                <select
                  value={examCode}
                  onChange={(e) => handleExamChange(e.target.value)}
                  className="bg-slate-800 text-white font-bold rounded-lg px-2.5 py-1.5 border border-slate-700 focus:ring-2 focus:ring-blue-500 appearance-none pr-7 text-xs"
                >
                  {exams.map(e => (
                    <option key={e.code} value={e.code}>
                      {e.name}
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2 top-2 pointer-events-none" />
              </div>
            </div>

            {/* 2. Counselling Route (JoSAA vs CSAB vs State) */}
            {examMeta?.admission_systems?.length > 1 && (
              <div className="flex items-center space-x-2 shrink-0">
                <span className="font-bold text-slate-400 uppercase tracking-wider text-[11px]">Route:</span>
                <div className="relative">
                  <select
                    value={counselling}
                    onChange={(e) => setCounselling(e.target.value)}
                    className="bg-slate-800 text-amber-400 font-bold rounded-lg px-2.5 py-1.5 border border-slate-700 focus:ring-2 focus:ring-blue-500 appearance-none pr-7 text-xs"
                  >
                    {examMeta.admission_systems.map(sys => (
                      <option key={sys.code} value={sys.code}>
                        {sys.code} ({sys.participating_institutes_count} Inst)
                      </option>
                    ))}
                  </select>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2 top-2 pointer-events-none" />
                </div>
              </div>
            )}

            {/* 3. Rank Input */}
            <div className="flex items-center space-x-2 shrink-0">
              <span className="font-bold text-slate-400 uppercase tracking-wider text-[11px]">Rank:</span>
              <input
                type="number"
                min="1"
                required
                value={rank}
                onChange={(e) => setRank(e.target.value)}
                className="bg-slate-800 text-white font-black w-24 px-2.5 py-1.5 rounded-lg border border-slate-700 focus:ring-2 focus:ring-blue-500 text-xs"
                placeholder="Rank"
              />
            </div>

            {/* 4. Category */}
            {examMeta?.categories?.length > 0 && (
              <div className="flex items-center space-x-2 shrink-0">
                <span className="font-bold text-slate-400 uppercase tracking-wider text-[11px]">Cat:</span>
                <div className="relative">
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="bg-slate-800 text-white font-bold rounded-lg px-2.5 py-1.5 border border-slate-700 focus:ring-2 focus:ring-blue-500 appearance-none pr-7 text-xs"
                  >
                    {examMeta.categories.map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2 top-2 pointer-events-none" />
                </div>
              </div>
            )}

            {/* 5. Branch (Quick text filter or All) */}
            <div className="flex items-center space-x-2 flex-1 max-w-[200px]">
              <span className="font-bold text-slate-400 uppercase tracking-wider text-[11px]">Branch:</span>
              <input
                type="text"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                placeholder="All Branches"
                className="bg-slate-800 text-white font-medium w-full px-2.5 py-1.5 rounded-lg border border-slate-700 focus:ring-2 focus:ring-blue-500 text-xs"
              />
            </div>

            {/* 6. Action Button & Results Badge */}
            <div className="flex items-center space-x-3 shrink-0">
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold flex items-center space-x-1.5 transition-all shadow-md shadow-blue-600/30 text-xs disabled:opacity-50"
              >
                {loading ? (
                  <span>Searching...</span>
                ) : (
                  <>
                    <Search className="w-3.5 h-3.5" />
                    <span>Update</span>
                  </>
                )}
              </button>

              {totalColleges !== undefined && (
                <div className="hidden lg:flex items-center space-x-1 text-[11px] text-emerald-400 font-bold bg-emerald-950/60 px-2.5 py-1 rounded-lg border border-emerald-800/60">
                  <span>{totalColleges} Colleges</span>
                  <span>•</span>
                  <span>{totalBranches} Cutoffs</span>
                </div>
              )}
            </div>

          </form>
        </div>
      </div>

      {/* Floating Mobile Sticky Bar & Drawer Trigger */}
      <div className="fixed bottom-4 left-4 right-4 z-40 md:hidden">
        <div className="bg-slate-900/95 backdrop-blur-md text-white border border-slate-800 rounded-2xl p-3 shadow-2xl flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded bg-blue-600 font-black text-[10px] uppercase">
                {selectedExam?.code}
              </span>
              <span className="text-xs font-bold text-slate-300">
                Rank {formatRank(rank)}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-0.5">
              {totalColleges || 0} colleges • {totalBranches || 0} options
            </p>
          </div>

          <button
            onClick={() => setMobileDrawerOpen(true)}
            className="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center space-x-1.5 shadow-md shadow-blue-600/40"
          >
            <SlidersHorizontal className="w-4 h-4" />
            <span>Modify Search</span>
          </button>
        </div>
      </div>

      {/* Mobile Search Modal Drawer */}
      {mobileDrawerOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4">
          <div className="bg-white text-slate-900 w-full max-w-lg rounded-t-3xl sm:rounded-3xl p-6 shadow-2xl max-h-[90vh] overflow-y-auto animate-slideUp">
            
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <SlidersHorizontal className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-black text-slate-900">Modify Search Parameters</h3>
              </div>
              <button 
                onClick={() => setMobileDrawerOpen(false)}
                className="p-2 rounded-full hover:bg-slate-100 text-slate-500"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Exam */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Examination
                </label>
                <select
                  value={examCode}
                  onChange={(e) => handleExamChange(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-300 font-bold text-sm bg-white"
                >
                  {exams.map(e => (
                    <option key={e.code} value={e.code}>{e.name}</option>
                  ))}
                </select>
              </div>

              {/* Counselling Route */}
              {examMeta?.admission_systems?.length > 1 && (
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Counselling / Admission Route
                  </label>
                  <select
                    value={counselling}
                    onChange={(e) => setCounselling(e.target.value)}
                    className="w-full px-3 py-2.5 rounded-xl border border-slate-300 font-bold text-sm bg-white"
                  >
                    {examMeta.admission_systems.map(sys => (
                      <option key={sys.code} value={sys.code}>
                        {sys.name} ({sys.participating_institutes_count} Institutes)
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {/* Rank */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Your Scorecard Rank
                </label>
                <input
                  type="number"
                  min="1"
                  required
                  value={rank}
                  onChange={(e) => setRank(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-300 font-black text-base text-slate-900"
                  placeholder="e.g. 40000"
                />
              </div>

              {/* Category */}
              {examMeta?.categories?.length > 0 && (
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Category
                  </label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full px-3 py-2.5 rounded-xl border border-slate-300 font-bold text-sm bg-white"
                  >
                    {examMeta.categories.map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>
              )}

              {/* Branch */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                  Branch Filter (Optional)
                </label>
                <input
                  type="text"
                  value={branch}
                  onChange={(e) => setBranch(e.target.value)}
                  placeholder="Leave empty for All Branches"
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-300 font-medium text-sm text-slate-900"
                />
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm flex items-center justify-center space-x-2 shadow-lg shadow-blue-600/30 disabled:opacity-50"
              >
                {loading ? (
                  <span>Searching...</span>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>Apply & View Results</span>
                  </>
                )}
              </button>
            </form>

          </div>
        </div>
      )}
    </>
  );
}
