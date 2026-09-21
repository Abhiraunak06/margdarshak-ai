import React, { useState, useEffect } from 'react';
import { 
  Search, 
  SlidersHorizontal, 
  Filter, 
  Sparkles, 
  Layers, 
  CheckSquare, 
  Info,
  ShieldCheck,
  ChevronDown
} from 'lucide-react';

const COMMON_BRANCH_PILLS = [
  "Computer Science and Engineering",
  "Information Technology",
  "Electronics & Communication",
  "Electrical Engineering",
  "Mechanical Engineering",
  "Civil Engineering",
  "Chemical Engineering",
  "Artificial Intelligence",
  "Data Science",
  "Mathematics & Computing",
  "Aerospace Engineering"
];

export default function PredictorForm({ 
  selectedExam, 
  examMeta, 
  onSubmit, 
  loading 
}) {
  const [counselling, setCounselling] = useState(examMeta?.default_counselling || 'JOSAA');
  const [rank, setRank] = useState(4000);
  const [category, setCategory] = useState('OPEN');
  const [quota, setQuota] = useState('All');
  const [homeState, setHomeState] = useState('');
  const [gender, setGender] = useState('Gender-Neutral');
  const [round, setRound] = useState('Any');
  const [mode, setMode] = useState('A'); // A, B, C
  const [selectedBranch, setSelectedBranch] = useState('Computer Science and Engineering');
  const [compareBranches, setCompareBranches] = useState(['Computer Science and Engineering', 'Electronics & Communication']);
  const [strategy, setStrategy] = useState('all'); // all, conservative, match, ambitious
  const [collegeType, setCollegeType] = useState('All');
  const [selectedState, setSelectedState] = useState('All');
  const [sortBy, setSortBy] = useState('closing_rank_asc');

  // Update defaults when exam metadata changes
  useEffect(() => {
    if (examMeta?.default_counselling) {
      setCounselling(examMeta.default_counselling);
    }
    if (examMeta?.categories?.length) {
      if (!examMeta.categories.includes(category)) {
        setCategory(examMeta.categories.includes('OPEN') ? 'OPEN' : examMeta.categories[0]);
      }
    }
    if (examMeta?.quotas?.length) {
      if (quota !== 'All' && !examMeta.quotas.includes(quota)) {
        setQuota('All');
      }
    }
    if (examMeta?.rounds?.length) {
      if (round !== 'Any' && !examMeta.rounds.includes(Number(round))) {
        setRound('Any');
      }
    }
    if (examMeta?.has_home_state_quota && examMeta?.states?.length) {
      if (!homeState || !examMeta.states.includes(homeState)) {
        setHomeState(examMeta.states[0]);
      }
    }
  }, [examMeta]);

  const handleSubmit = (e) => {
    e.preventDefault();
    let branchParam = '';
    if (mode === 'B') {
      branchParam = selectedBranch;
    } else if (mode === 'C') {
      branchParam = compareBranches.join(',');
    }

    onSubmit({
      exam_code: selectedExam.code,
      counselling: counselling || examMeta?.default_counselling || undefined,
      year: examMeta?.year || 2024,
      rank: Number(rank),
      category,
      quota,
      home_state: (selectedExam.has_home_state_quota && quota !== 'All') ? homeState : undefined,
      gender,
      round,
      mode,
      branch: branchParam,
      strategy,
      college_type: collegeType,
      state: selectedState,
      sort_by: sortBy,
      page: 1,
      limit: 25
    });
  };

  const toggleCompareBranch = (branchName) => {
    if (compareBranches.includes(branchName)) {
      if (compareBranches.length > 1) {
        setCompareBranches(compareBranches.filter(b => b !== branchName));
      }
    } else {
      if (compareBranches.length < 5) {
        setCompareBranches([...compareBranches, branchName]);
      }
    }
  };

  const getRankLabel = () => {
    if (selectedExam.code === 'JEE_MAIN' || selectedExam.code === 'JEE_ADV') {
      if (category === 'OPEN' || category === 'OPEN (PwD)') {
        return 'Overall CRL Rank (AIR) *';
      }
      return `Category Rank (${category}) *`;
    }
    if (selectedExam.code === 'WBJEE') return 'WBJEE Merit Rank (GMR) *';
    if (selectedExam.code === 'COMEDK') return 'COMEDK General Merit Rank *';
    if (selectedExam.code === 'VITEEE') return 'VITEEE Equated Rank *';
    return 'Your Exam Rank *';
  };

  const getRankSubtext = () => {
    if (selectedExam.code === 'JEE_MAIN' || selectedExam.code === 'JEE_ADV') {
      if (category === 'OPEN' || category === 'OPEN (PwD)') {
        return 'Enter Common Rank List (CRL) AIR';
      }
      return `JoSAA cutoffs use Category Rank for ${category}`;
    }
    if (selectedExam.code === 'WBJEE') return 'Enter General Merit Rank (GMR) from scorecard';
    if (selectedExam.code === 'COMEDK') return 'Enter GM Rank from official scorecard';
    return 'Enter rank as per your scorecard';
  };

  const getQuickPills = () => {
    if (selectedExam.code === 'WBJEE') return [1500, 8000, 25000, 40000];
    if (selectedExam.code === 'COMEDK') return [50, 500, 2500, 8000];
    if (selectedExam.code === 'VITEEE') return [1500, 5000, 15000, 35000];
    return [1500, 4000, 10000, 25000];
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200 shadow-xl shadow-slate-200/50 p-6 sm:p-8 mb-12">
      
      {/* Header with Search Mode Selector */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-slate-100 gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-800 uppercase tracking-wide">
              {selectedExam.code.replace('_', ' ')}
            </span>
            <span className="text-xs text-slate-500 font-medium">
              Data Year: {examMeta?.year || 2024} (Rounds 1 - 5)
            </span>
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 mt-1">
            Predict Matching Colleges & Branches
          </h2>
          {examMeta?.rank_guidance && (
            <p className="text-xs text-slate-600 mt-1 font-medium bg-blue-50/70 border border-blue-100 px-3 py-1.5 rounded-lg inline-block">
              ℹ️ <strong>Guidance:</strong> {examMeta.rank_guidance}
            </p>
          )}
        </div>

        {/* 3 Search Modes Switcher */}
        <div className="bg-slate-100 p-1 rounded-xl flex space-x-1 self-start md:self-auto text-xs font-bold">
          <button
            type="button"
            onClick={() => setMode('A')}
            className={`px-3 py-2 rounded-lg transition-all ${
              mode === 'A' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Mode A: All Branches
          </button>
          <button
            type="button"
            onClick={() => setMode('B')}
            className={`px-3 py-2 rounded-lg transition-all ${
              mode === 'B' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Mode B: Specific Branch
          </button>
          <button
            type="button"
            onClick={() => setMode('C')}
            className={`px-3 py-2 rounded-lg transition-all ${
              mode === 'C' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Mode C: Branch Compare
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Admission / Counselling System Route Switcher (e.g., JoSAA vs CSAB) */}
        {examMeta?.admission_systems?.length > 1 && (
          <div className="bg-amber-50/70 border border-amber-200 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-amber-800 flex items-center space-x-1">
                <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
                <span>Admission / Counselling Authority Route:</span>
              </span>
              <p className="text-xs text-amber-900 mt-0.5">
                Restricts predicted colleges strictly to verified participating institutions for that counselling system.
              </p>
            </div>
            <div className="flex space-x-2">
              {examMeta.admission_systems.map((sys) => (
                <button
                  key={sys.code}
                  type="button"
                  onClick={() => setCounselling(sys.code)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition-all ${
                    counselling === sys.code
                      ? 'bg-amber-800 text-white shadow-md shadow-amber-900/20'
                      : 'bg-white text-amber-900 border border-amber-200 hover:bg-amber-100'
                  }`}
                >
                  {sys.code} ({sys.participating_institutes_count} Institutes)
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Core Inputs Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          
          {/* 1. Student Rank */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
                {getRankLabel()}
              </label>
              {rank && !isNaN(Number(rank)) && (
                <span className="text-[11px] font-bold text-blue-600">
                  {Number(rank).toLocaleString()}
                </span>
              )}
            </div>
            <div className="relative">
              <input
                type="number"
                min="1"
                max="1000000"
                required
                value={rank}
                onChange={(e) => setRank(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-blue-600 font-semibold text-slate-900 text-base shadow-sm"
                placeholder="e.g. 4000"
              />
              <span className="absolute right-3 top-2.5 text-xs font-semibold text-slate-400">
                {selectedExam.code === 'WBJEE' ? 'GMR' : selectedExam.code === 'COMEDK' ? 'GM' : 'RANK'}
              </span>
            </div>
            {/* Quick rank helper pills */}
            <div className="flex space-x-1.5 mt-1.5 text-[11px] text-slate-500">
              <span>Quick:</span>
              {getQuickPills().map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setRank(r)}
                  className="hover:text-blue-600 underline"
                >
                  {r.toLocaleString()}
                </button>
              ))}
            </div>
            <p className="text-[11px] text-slate-500 mt-1">{getRankSubtext()}</p>
          </div>

          {/* 2. Category (Dynamic from DB) */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Category (Seat Allocation) *
            </label>
            <div className="relative">
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-blue-600 font-semibold text-slate-900 text-sm shadow-sm bg-white appearance-none pr-8"
              >
                {examMeta?.categories?.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Official counselling seat category</p>
          </div>

          {/* 3. Gender */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Gender Pool
            </label>
            <div className="relative">
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-blue-600 font-semibold text-slate-900 text-sm shadow-sm bg-white appearance-none pr-8"
              >
                <option value="Gender-Neutral">Gender-Neutral (All candidates)</option>
                <option value="Female-only">Female-only (Supernumerary)</option>
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Includes supernumerary female quota</p>
          </div>

          {/* 4. Counselling Round */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Counselling Round
            </label>
            <div className="relative">
              <select
                value={round}
                onChange={(e) => setRound(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-blue-600 font-semibold text-slate-900 text-sm shadow-sm bg-white appearance-none pr-8"
              >
                <option value="Any">Any Round (Best Match)</option>
                {examMeta?.rounds?.map((r) => (
                  <option key={r} value={r}>
                    Round {r}
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Independent round records preserved</p>
          </div>

        </div>

        {/* Quota & Home State Row (Only when applicable) */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 pt-2">
          
          {/* Quota */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Quota Filter
            </label>
            <div className="relative">
              <select
                value={quota}
                onChange={(e) => setQuota(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-blue-600 font-semibold text-slate-900 text-sm shadow-sm bg-white appearance-none pr-8"
              >
                <option value="All">All Eligible Quotas (AI + HS + OS)</option>
                <option value="AI">All India (AI)</option>
                {selectedExam.has_home_state_quota && (
                  <>
                    <option value="HS">Home State (HS)</option>
                    <option value="OS">Other State (OS)</option>
                  </>
                )}
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
            </div>
          </div>

          {/* Home State (Conditional) */}
          {selectedExam.has_home_state_quota ? (
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                Your Home State *
              </label>
              <div className="relative">
                <select
                  value={homeState}
                  onChange={(e) => setHomeState(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-blue-600 font-semibold text-slate-900 text-sm shadow-sm bg-white appearance-none pr-8"
                >
                  <option value="">-- Select Your 12th State --</option>
                  {examMeta?.states?.map((st) => (
                    <option key={st} value={st}>
                      {st}
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
              </div>
              <p className="text-[11px] text-slate-500 mt-1">Determines 50% NIT Home State eligibility</p>
            </div>
          ) : (
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
                Home State Quota
              </label>
              <div className="px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-400 text-xs font-medium">
                Not applicable for {selectedExam.name} (100% All India Quota)
              </div>
            </div>
          )}

          {/* Safety Buffer Strategy Filter */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              Admission Strategy Buffer
            </label>
            <div className="relative">
              <select
                value={strategy}
                onChange={(e) => setStrategy(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-blue-600 font-semibold text-slate-900 text-sm shadow-sm bg-white appearance-none pr-8"
              >
                <option value="all">All Ranges (Eligible + Reach Programs)</option>
                <option value="all_eligible">All Eligible Programs (Rank ≤ Closing Cutoff)</option>
                <option value="range_match">Opening & Closing Range Match (OR ≤ Rank ≤ CR)</option>
                <option value="conservative">Safer Range (Closing ≥ 1.15x Rank)</option>
                <option value="ambitious">Reach / Ambitious (Aspirational)</option>
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
            </div>
          </div>

          {/* College Type Filter */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
              College Type
            </label>
            <div className="relative">
              <select
                value={collegeType}
                onChange={(e) => setCollegeType(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-blue-600 font-semibold text-slate-900 text-sm shadow-sm bg-white appearance-none pr-8"
              >
                <option value="All">All Types</option>
                {examMeta?.college_types?.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
            </div>
          </div>

        </div>

        {/* Mode B: Specific Branch Selector */}
        {mode === 'B' && (
          <div className="p-4 rounded-2xl bg-blue-50/70 border border-blue-200">
            <label className="block text-xs font-bold uppercase tracking-wider text-blue-900 mb-2">
              Select Desired Branch Program
            </label>
            <input
              type="text"
              value={selectedBranch}
              onChange={(e) => setSelectedBranch(e.target.value)}
              placeholder="e.g. Computer Science, Mechanical, AI, Electrical..."
              className="w-full px-4 py-2 rounded-xl border border-blue-300 focus:ring-2 focus:ring-blue-600 text-sm font-semibold text-slate-900 bg-white mb-2"
            />
            <div className="flex flex-wrap gap-1.5">
              {COMMON_BRANCH_PILLS.map((b) => (
                <button
                  key={b}
                  type="button"
                  onClick={() => setSelectedBranch(b)}
                  className={`text-xs px-2.5 py-1 rounded-full border transition-all ${
                    selectedBranch === b
                      ? 'bg-blue-600 text-white border-blue-600 font-bold'
                      : 'bg-white text-slate-700 border-slate-200 hover:border-blue-400'
                  }`}
                >
                  {b}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Mode C: Branch Comparison Multi-Select */}
        {mode === 'C' && (
          <div className="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-200">
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-bold uppercase tracking-wider text-indigo-900">
                Choose Branches to Compare (Select 2 to 5)
              </label>
              <span className="text-xs font-bold text-indigo-700">
                {compareBranches.length} selected
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {COMMON_BRANCH_PILLS.map((b) => {
                const active = compareBranches.includes(b);
                return (
                  <button
                    key={b}
                    type="button"
                    onClick={() => toggleCompareBranch(b)}
                    className={`text-xs px-3 py-1.5 rounded-xl border font-semibold transition-all flex items-center space-x-1.5 ${
                      active
                        ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                        : 'bg-white text-slate-700 border-slate-200 hover:border-indigo-400'
                    }`}
                  >
                    <span>{b}</span>
                    {active && <span className="text-[10px] ml-1">✓</span>}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Sorting & Search Action Row */}
        <div className="flex flex-col sm:flex-row items-center justify-between pt-4 border-t border-slate-100 gap-4">
          <div className="flex items-center space-x-2 text-xs text-slate-600 w-full sm:w-auto">
            <SlidersHorizontal className="w-4 h-4 text-slate-400" />
            <span className="font-semibold">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-slate-50 text-xs font-bold text-slate-700"
            >
              <option value="closing_rank_asc">Closing Rank (Ascending)</option>
              <option value="closing_rank_desc">Closing Rank (Descending)</option>
              <option value="orank_asc">Opening Rank (Ascending)</option>
              <option value="college_name_asc">College Name (A - Z)</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full sm:w-auto px-8 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-sm shadow-lg shadow-blue-500/25 transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Predicting Eligible Colleges...</span>
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                <span>Find Eligible Colleges</span>
              </>
            )}
          </button>
        </div>

      </form>
    </div>
  );
}
