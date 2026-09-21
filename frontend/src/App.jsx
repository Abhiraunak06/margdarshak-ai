import React, { useState, useEffect, useRef } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import StreamSelector from './components/StreamSelector';
import ExamSelector from './components/ExamSelector';
import PredictorForm from './components/PredictorForm';
import CollegeResultCard from './components/CollegeResultCard';
import CutoffDetailsModal from './components/CutoffDetailsModal';
import CutoffTrendsModal from './components/CutoffTrendsModal';
import ComparisonDrawer from './components/ComparisonDrawer';
import CareerExplorer from './components/CareerExplorer';
import PersonalizedRoadmap from './components/PersonalizedRoadmap';
import CollegeDirectory from './components/CollegeDirectory';
import AdminDashboard from './components/AdminDashboard';
import StickySearchBar from './components/StickySearchBar';
import MedicalPredictor from './components/MedicalPredictor';
import CommerceSection from './components/CommerceSection';
import ArtsSection from './components/ArtsSection';
import ErrorBoundary from './components/ErrorBoundary';
import MargdarshakChatbot from './components/MargdarshakChatbot';
import GlassOrb from './components/GlassOrb';
import { fetchExams, fetchExamMeta, searchCutoffs } from './services/api';
import { 
  Sparkles, 
  ArrowRight, 
  Compass, 
  GraduationCap, 
  Briefcase, 
  Layers, 
  AlertCircle,
  CheckCircle2, 
  ChevronLeft,
  ChevronRight,
  Filter,
  Mic,
  Search,
  Settings
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('predictor'); // predictor, colleges, careers, roadmap, admin
  const [selectedStream, setSelectedStream] = useState('PCM');
  const [exams, setExams] = useState([]);
  const [selectedExam, setSelectedExam] = useState(null);
  const [examMeta, setExamMeta] = useState(null);
  const [loadingExams, setLoadingExams] = useState(true);

  // Margdarshak Chatbot state
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);
  const [heroPrompt, setHeroPrompt] = useState('');

  // Search state
  const [searchResults, setSearchResults] = useState(null);
  const [searchParams, setSearchParams] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  // Modals & Drawers
  const [selectedCutoffItem, setSelectedCutoffItem] = useState(null);
  const [selectedTrendItem, setSelectedTrendItem] = useState(null);
  const [isCompareOpen, setIsCompareOpen] = useState(false);
  const [prefilledCareer, setPrefilledCareer] = useState(null);

  // Bookmarks / Saved colleges
  const [savedColleges, setSavedColleges] = useState(() => {
    try {
      const stored = localStorage.getItem('careerpath_saved_colleges');
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  const predictorRef = useRef(null);

  const handleNavigateStreamFromChatbot = (streamName, suggestedTab) => {
    const normalized = (streamName || '').toUpperCase();
    if (normalized.includes('PCM') || normalized.includes('ENG')) {
      setSelectedStream('PCM');
      setActiveTab('predictor');
    } else if (normalized.includes('PCB') || normalized.includes('MED')) {
      setSelectedStream('PCB');
      setActiveTab('predictor');
    } else if (normalized.includes('COMMERCE')) {
      setSelectedStream('COMMERCE');
      setActiveTab('predictor');
    } else if (normalized.includes('ART')) {
      setSelectedStream('ARTS');
      setActiveTab('predictor');
    } else {
      setActiveTab(suggestedTab || 'predictor');
    }

    setTimeout(() => {
      predictorRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 150);
  };
  const examsRef = useRef(null);
  const currentSearchIdRef = useRef(null);

  // Save to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('careerpath_saved_colleges', JSON.stringify(savedColleges));
    } catch (e) {
      console.error(e);
    }
  }, [savedColleges]);

  // Load Exams on initial load and handle URL query params
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const streamParam = urlParams.get('stream');
    if (streamParam && ['PCM', 'PCB', 'COMMERCE', 'ARTS'].includes(streamParam.toUpperCase())) {
      setSelectedStream(streamParam.toUpperCase());
    }

    const examParam = urlParams.get('exam');
    const counsellingParam = urlParams.get('counselling');
    const rankParam = urlParams.get('rank');
    const categoryParam = urlParams.get('category');
    const quotaParam = urlParams.get('quota');
    const branchParam = urlParams.get('branch');
    const homeStateParam = urlParams.get('home_state');

    fetchExams('PCM')
      .then((data) => {
        setExams(data);
        if (data.length > 0) {
          const matchedExam = examParam ? data.find(e => e.code === examParam) : null;
          const defaultExam = matchedExam || data.find(e => e.code === 'JEE_MAIN') || data[0];
          setSelectedExam(defaultExam);
          
          fetchExamMeta(defaultExam.code, 2024).then((meta) => {
            setExamMeta(meta);
            const defaultCategory = categoryParam || (meta.categories?.includes('OPEN') ? 'OPEN' : (meta.categories?.[0] || 'OPEN'));
            const defaultRank = rankParam ? Number(rankParam) : (defaultExam.code === 'BITSAT' ? 280 : 4000);
            const defaultCounselling = counsellingParam || meta.default_counselling || meta.admission_systems?.[0]?.code;
            const initialParams = {
              exam_code: defaultExam.code,
              counselling: defaultCounselling,
              rank: defaultRank,
              category: defaultCategory,
              quota: quotaParam || 'All',
              branch: branchParam || undefined,
              home_state: homeStateParam || undefined,
              mode: branchParam ? 'B' : 'A',
              page: Number(urlParams.get('page')) || 1
            };
            handlePredictSubmit(initialParams);
          }).catch(console.error);
        }
        setLoadingExams(false);
      })
      .catch((err) => {
        console.error(err);
        setLoadingExams(false);
      });
  }, []);

  const handleSelectExam = (exam) => {
    setSelectedExam(exam);
    fetchExamMeta(exam.code, 2024)
      .then((meta) => {
        setExamMeta(meta);
        const defaultCategory = meta.categories?.includes('OPEN') ? 'OPEN' : (meta.categories?.[0] || 'OPEN');
        const defaultRank = exam.code === 'BITSAT' ? 280 : 4000;
        const defaultCounselling = meta.default_counselling || meta.admission_systems?.[0]?.code;
        handlePredictSubmit({
          exam_code: exam.code,
          counselling: defaultCounselling,
          rank: defaultRank,
          category: defaultCategory,
          quota: 'All',
          mode: 'A',
          page: 1
        });
      })
      .catch(console.error);
  };

  const handleStreamSelect = (newStream) => {
    setSelectedStream(newStream);
    try {
      const url = new URL(window.location.href);
      url.searchParams.set('stream', newStream);
      window.history.pushState({}, '', url.toString());
    } catch (e) {
      console.warn('Could not update stream in URL', e);
    }
  };

  const updateUrlParams = (params) => {
    try {
      const url = new URL(window.location.href);
      if (selectedStream) url.searchParams.set('stream', selectedStream);
      if (params.exam_code) url.searchParams.set('exam', params.exam_code);
      if (params.counselling) url.searchParams.set('counselling', params.counselling);
      if (params.rank) url.searchParams.set('rank', params.rank);
      if (params.category) url.searchParams.set('category', params.category);
      if (params.quota) url.searchParams.set('quota', params.quota);
      if (params.branch) url.searchParams.set('branch', params.branch); else url.searchParams.delete('branch');
      if (params.home_state) url.searchParams.set('home_state', params.home_state); else url.searchParams.delete('home_state');
      if (params.page) url.searchParams.set('page', params.page);
      window.history.pushState({}, '', url.toString());
    } catch (e) {
      console.warn('Could not update URL parameters', e);
    }
  };

  const handlePredictSubmit = async (params) => {
    const searchId = "srch_" + Date.now() + "_" + Math.random().toString(36).substring(2, 7);
    currentSearchIdRef.current = searchId;
    setSearchLoading(true);
    setSearchParams(params);
    setCurrentPage(params.page || 1);
    updateUrlParams(params);

    try {
      const data = await searchCutoffs({ ...params, search_id: searchId });
      // Protect against stale responses from fast sequential queries
      if (data.search_id && data.search_id !== currentSearchIdRef.current) {
        return;
      }
      setSearchResults(data);
      // Smooth scroll to results
      setTimeout(() => {
        const el = document.getElementById('results-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      alert(err.message || 'Error searching cutoffs');
    } finally {
      setSearchLoading(false);
    }
  };

  const handlePageChange = (newPage) => {
    if (!searchParams) return;
    const updated = { ...searchParams, page: newPage };
    handlePredictSubmit(updated);
  };

  const toggleSaveCollege = (college) => {
    const exists = savedColleges.some(c => c.id === college.id);
    if (exists) {
      setSavedColleges(savedColleges.filter(c => c.id !== college.id));
    } else {
      setSavedColleges([...savedColleges, college]);
    }
  };

  const handleRemoveSaved = (collegeId) => {
    setSavedColleges(savedColleges.filter(c => c.id !== collegeId));
  };

  const handleClearAllSaved = () => {
    setSavedColleges([]);
  };

  const navigateToCareerRoadmap = (career) => {
    setPrefilledCareer(career);
    setActiveTab('roadmap');
  };

  return (
    <div className="min-h-screen flex flex-col bg-iridescent-mesh selection:bg-pink-500 selection:text-white">
      
      {/* Top Navigation */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        savedCount={savedColleges.length}
        onOpenCompare={() => setIsCompareOpen(true)}
        onOpenChatbot={() => setIsChatbotOpen(true)}
      />

      {/* Dynamic Content Views */}
      <main className="flex-grow">
        <ErrorBoundary>
        
        {/* VIEW 1: PREDICTOR / HOME */}
        {activeTab === 'predictor' && (
          <div>
            {/* Sticky Search Control Bar (Sticky on scroll for instant route/rank switching in PCM) */}
            {selectedStream === 'PCM' && (
              <StickySearchBar 
                exams={exams}
                selectedExam={selectedExam}
                onSelectExam={handleSelectExam}
                examMeta={examMeta}
                searchParams={searchParams}
                onSearch={handlePredictSubmit}
                loading={searchLoading}
                totalColleges={searchResults?.pagination?.total_colleges_count}
                totalBranches={searchResults?.pagination?.total_count}
              />
            )}
            
            {/* Hero Section — Classy Iridescent Aesthetic */}
            <div className="relative pt-12 pb-16 sm:pb-20 px-4 sm:px-6 lg:px-8">
              <div className="max-w-5xl mx-auto">
                
                {/* Headline matching user's classy reference layout */}
                <div className="text-center max-w-4xl mx-auto space-y-3">
                  <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full text-xs font-black tracking-wider uppercase bg-white/80 text-purple-800 border border-white/80 shadow-xs backdrop-blur-md">
                    <Sparkles className="w-3.5 h-3.5 text-pink-500 animate-pulse" />
                    <span>Margdarshak AI • Empirical Career Guidance</span>
                  </div>

                  <h1 className="text-3xl sm:text-5xl lg:text-6xl font-light tracking-tight text-slate-700 leading-tight">
                    <span className="text-pink-500 font-medium">AI Powers</span>{' '}
                    <strong className="font-black text-slate-900">Career Discovery</strong>{' '}
                    <span className="text-slate-400 font-light">And</span>{' '}
                    <br className="hidden sm:inline" />
                    <strong className="font-black text-slate-900">Dream College Prediction</strong>
                  </h1>

                  <p className="text-xs sm:text-sm text-slate-500 max-w-2xl mx-auto font-medium leading-relaxed">
                    15-question Random Forest psychometric assessment, 56,000+ authentic JoSAA/NEET cutoffs, and tailored stream roadmaps.
                  </p>
                </div>

                {/* Centerpiece: 3D Iridescent Glowing Glass Orb with Reflection */}
                <div className="py-6 sm:py-9 flex justify-center">
                  <GlassOrb size={200} onClick={() => setIsChatbotOpen(true)} />
                </div>

                {/* Quick Action Chips above Prompt Bar */}
                <div className="flex flex-wrap items-center justify-center gap-2 max-w-3xl mx-auto mb-3">
                  <button
                    onClick={() => setIsChatbotOpen(true)}
                    className="px-3 py-1.5 rounded-full text-xs font-bold bg-white/70 hover:bg-white border border-white/90 text-slate-700 shadow-xs transition-all flex items-center space-x-1.5 hover:border-purple-300 hover:shadow-sm"
                  >
                    <Sparkles className="w-3.5 h-3.5 text-pink-500" />
                    <span>15-Q Career ML Recommender</span>
                  </button>

                  <button
                    onClick={() => {
                      setSelectedStream('PCM');
                    }}
                    className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all flex items-center space-x-1.5 shadow-xs ${
                      selectedStream === 'PCM'
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-white/70 hover:bg-white border-white/90 text-slate-700 hover:border-blue-300'
                    }`}
                  >
                    <Compass className="w-3.5 h-3.5 text-blue-500" />
                    <span>Engineering & JEE</span>
                  </button>

                  <button
                    onClick={() => {
                      setSelectedStream('PCB');
                    }}
                    className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all flex items-center space-x-1.5 shadow-xs ${
                      selectedStream === 'PCB'
                        ? 'bg-emerald-600 text-white border-emerald-600'
                        : 'bg-white/70 hover:bg-white border-white/90 text-slate-700 hover:border-emerald-300'
                    }`}
                  >
                    <GraduationCap className="w-3.5 h-3.5 text-emerald-500" />
                    <span>Medical & NEET</span>
                  </button>

                  <button
                    onClick={() => {
                      setSelectedStream('COMMERCE');
                    }}
                    className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all flex items-center space-x-1.5 shadow-xs ${
                      selectedStream === 'COMMERCE'
                        ? 'bg-amber-600 text-white border-amber-600'
                        : 'bg-white/70 hover:bg-white border-white/90 text-slate-700 hover:border-amber-300'
                    }`}
                  >
                    <Briefcase className="w-3.5 h-3.5 text-amber-500" />
                    <span>Commerce & CA</span>
                  </button>

                  <button
                    onClick={() => {
                      setSelectedStream('ARTS');
                    }}
                    className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all flex items-center space-x-1.5 shadow-xs ${
                      selectedStream === 'ARTS'
                        ? 'bg-rose-600 text-white border-rose-600'
                        : 'bg-white/70 hover:bg-white border-white/90 text-slate-700 hover:border-rose-300'
                    }`}
                  >
                    <Layers className="w-3.5 h-3.5 text-rose-500" />
                    <span>Law & Arts</span>
                  </button>
                </div>

                {/* Floating Frosted Prompt Bar (Directly from reference design) */}
                <div className="max-w-2xl mx-auto">
                  <div className="chromatic-border">
                    <div className="bg-white/80 backdrop-blur-xl rounded-[1.15rem] p-3 shadow-glass">
                      <form
                        onSubmit={(e) => {
                          e.preventDefault();
                          setIsChatbotOpen(true);
                        }}
                        className="space-y-2.5"
                      >
                        <input
                          type="text"
                          value={heroPrompt}
                          onChange={(e) => setHeroPrompt(e.target.value)}
                          placeholder="Career Recommendation Chatbot"
                          className="w-full px-2 py-1.5 bg-transparent text-sm text-slate-800 placeholder-slate-400 font-medium focus:outline-none"
                        />
                        <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                          <div className="flex items-center space-x-1.5">
                            <button
                              type="button"
                              onClick={() => setIsChatbotOpen(true)}
                              className="px-2.5 py-1 rounded-xl bg-slate-100/90 hover:bg-purple-50 text-[11px] font-extrabold text-slate-700 hover:text-purple-700 flex items-center space-x-1 transition-colors"
                            >
                              <Sparkles className="w-3 h-3 text-purple-600" />
                              <span>15-Q Assessment</span>
                            </button>
                            <button
                              type="button"
                              onClick={() => {
                                predictorRef.current?.scrollIntoView({ behavior: 'smooth' });
                              }}
                              className="px-2.5 py-1 rounded-xl bg-slate-100/90 hover:bg-blue-50 text-[11px] font-extrabold text-slate-700 hover:text-blue-700 flex items-center space-x-1 transition-colors"
                            >
                              <Compass className="w-3 h-3 text-blue-600" />
                              <span>Predict Cutoffs</span>
                            </button>
                          </div>

                          <div className="flex items-center space-x-1.5">
                            <button
                              type="button"
                              onClick={() => setIsChatbotOpen(true)}
                              className="text-slate-400 hover:text-slate-700 p-1.5 transition-colors"
                              title="Voice AI"
                            >
                              <Mic className="w-4 h-4 text-purple-600" />
                            </button>
                            <button
                              type="submit"
                              className="px-4 py-1.5 rounded-xl bg-gradient-to-r from-pink-500 via-purple-600 to-indigo-600 hover:from-pink-600 hover:to-indigo-700 text-white text-xs font-black flex items-center space-x-1.5 shadow-md shadow-pink-500/20 active:scale-95 transition-all"
                            >
                              <span>Send</span>
                              <ArrowRight className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>

                {/* Core Trust Statistics — Frosted Glass Cards */}
                <div className="mt-9 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-3xl mx-auto">
                  <div className="p-3.5 rounded-2xl bg-white/60 backdrop-blur-md border border-white/80 shadow-xs text-center hover:bg-white/80 transition-colors">
                    <span className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">150+</span>
                    <span className="block text-[11px] text-slate-500 font-semibold mt-0.5">Premier Institutes</span>
                  </div>
                  <div className="p-3.5 rounded-2xl bg-white/60 backdrop-blur-md border border-white/80 shadow-xs text-center hover:bg-white/80 transition-colors">
                    <span className="text-xl sm:text-2xl font-black text-purple-600 tracking-tight">56,000+</span>
                    <span className="block text-[11px] text-slate-500 font-semibold mt-0.5">Authentic Cutoffs</span>
                  </div>
                  <div className="p-3.5 rounded-2xl bg-white/60 backdrop-blur-md border border-white/80 shadow-xs text-center hover:bg-white/80 transition-colors">
                    <span className="text-xl sm:text-2xl font-black text-emerald-600 tracking-tight">100%</span>
                    <span className="block text-[11px] text-slate-500 font-semibold mt-0.5">Official Records</span>
                  </div>
                  <div className="p-3.5 rounded-2xl bg-white/60 backdrop-blur-md border border-white/80 shadow-xs text-center hover:bg-white/80 transition-colors">
                    <span className="text-xl sm:text-2xl font-black text-pink-600 tracking-tight">4 Streams</span>
                    <span className="block text-[11px] text-slate-500 font-semibold mt-0.5">PCM • PCB • Comm • Arts</span>
                  </div>
                </div>

              </div>
            </div>

            {/* Step-by-Step Selection Flow */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12" ref={predictorRef}>
              
              {/* Step 1: Academic Stream */}
              <StreamSelector 
                selectedStream={selectedStream} 
                onSelectStream={handleStreamSelect} 
              />

              {/* STREAM VIEW 1: PCM (ENGINEERING) */}
              {selectedStream === 'PCM' && (
                <div className="space-y-10 animate-fadeIn">
                  
                  {/* Step 2: Entrance Examination */}
                  <div ref={examsRef}>
                    <ExamSelector 
                      exams={exams} 
                      selectedExam={selectedExam} 
                      onSelectExam={handleSelectExam} 
                      loading={loadingExams}
                    />
                  </div>

                  {/* Step 3: Dynamic Predictor Form */}
                  {selectedExam && examMeta && (
                    <PredictorForm 
                      selectedExam={selectedExam}
                      examMeta={examMeta}
                      onSubmit={handlePredictSubmit}
                      loading={searchLoading}
                    />
                  )}

                  {/* Active Loading State */}
                  {searchLoading && (
                    <div className="my-8 p-8 rounded-3xl bg-blue-50/90 border border-blue-200 text-center animate-pulse">
                      <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent mb-3"></div>
                      <h3 className="text-base font-black text-blue-900">
                        Loading {selectedExam?.name} {searchParams?.counselling ? `/ ${searchParams.counselling}` : ''} results...
                      </h3>
                      <p className="text-xs text-blue-700 mt-1 font-medium">
                        Querying strictly verified participating institutes under the selected admission system.
                      </p>
                    </div>
                  )}

                  {/* Search Results Display */}
                  {searchResults && (
                    <div id="results-section" className="pt-8 border-t border-slate-200 animate-fadeIn">
                      
                      {/* Results Top Header */}
                      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm mb-8">
                        <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-4">
                          <div>
                            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">
                              Search Intelligence
                            </span>
                            <h2 className="text-2xl sm:text-3xl font-black text-slate-900 mt-1">
                              {searchResults.pagination.total_colleges_count !== undefined
                                ? `${searchResults.pagination.total_colleges_count} Colleges Found`
                                : 'Matching Colleges Found'}
                            </h2>
                            <p className="text-sm font-semibold text-slate-600 mt-0.5">
                              {searchResults.pagination.total_count.toLocaleString()} eligible branch cutoffs matched your rank
                            </p>
                          </div>

                          <div className="p-3 rounded-2xl bg-amber-50 border border-amber-200 text-xs text-amber-900 max-w-md flex items-start space-x-2">
                            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                            <span>
                              <strong>{searchResults.search_parameters.disclaimer}</strong> Future cutoffs vary according to seat matrix and applicant choices.
                            </span>
                          </div>
                        </div>

                        {/* Applied Parameters Summary Pills */}
                        <div className="flex flex-wrap items-center gap-2 text-xs">
                          <span className="font-bold text-slate-500">Your Search:</span>
                          <span className="px-3 py-1 rounded-lg bg-blue-50 text-blue-800 font-bold">
                            Exam: {searchResults.search_parameters.exam_name}
                          </span>
                          <span className="px-3 py-1 rounded-lg bg-slate-100 text-slate-800 font-bold">
                            Rank: {searchResults.search_parameters.rank.toLocaleString()}
                          </span>
                          <span className="px-3 py-1 rounded-lg bg-slate-100 text-slate-800 font-bold">
                            Category: {searchResults.search_parameters.category}
                          </span>
                          <span className="px-3 py-1 rounded-lg bg-slate-100 text-slate-800 font-bold">
                            Quota: {searchResults.search_parameters.quota}
                          </span>
                          {searchResults.search_parameters.home_state && (
                            <span className="px-3 py-1 rounded-lg bg-indigo-50 text-indigo-800 font-bold">
                              Home State: {searchResults.search_parameters.home_state}
                            </span>
                          )}
                          <span className="px-3 py-1 rounded-lg bg-slate-100 text-slate-800 font-bold">
                            Round: {searchResults.search_parameters.round}
                          </span>
                          <span className="px-3 py-1 rounded-lg bg-emerald-50 text-emerald-800 font-bold">
                            Strategy: {searchResults.search_parameters.strategy}
                          </span>
                        </div>
                      </div>

                      {/* Results Grid */}
                      {searchResults.results.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                          {searchResults.results.map((item) => (
                            <CollegeResultCard 
                              key={item.cutoff_id}
                              item={item}
                              onViewCutoff={setSelectedCutoffItem}
                              onViewTrends={setSelectedTrendItem}
                              isSaved={savedColleges.some(c => c.id === item.college.id)}
                              onToggleSave={toggleSaveCollege}
                            />
                          ))}
                        </div>
                      ) : (
                        <div className="py-16 text-center bg-white rounded-3xl border border-slate-200">
                          <Compass className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                          <h3 className="text-lg font-bold text-slate-800">No Programs Found Within This Range</h3>
                          <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
                            Try expanding your rank strategy buffer to 'Reach / Ambitious', or select 'All Branches' to view all eligible programs.
                          </p>
                        </div>
                      )}

                      {/* Pagination Controls */}
                      {searchResults.pagination.total_pages > 1 && (
                        <div className="flex flex-col sm:flex-row items-center justify-between bg-white p-4 rounded-2xl border border-slate-200 gap-3 text-xs font-bold text-slate-600">
                          <div>
                            Page {searchResults.pagination.page} of {searchResults.pagination.total_pages} ({searchResults.pagination.total_colleges_count || 0} colleges • {searchResults.pagination.total_count.toLocaleString()} branches)
                          </div>
                          <div className="flex space-x-2">
                            <button
                              disabled={searchResults.pagination.page <= 1}
                              onClick={() => handlePageChange(searchResults.pagination.page - 1)}
                              className="px-3.5 py-2 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 disabled:opacity-40 flex items-center space-x-1"
                            >
                              <ChevronLeft className="w-4 h-4" />
                              <span>Previous</span>
                            </button>
                            <button
                              disabled={searchResults.pagination.page >= searchResults.pagination.total_pages}
                              onClick={() => handlePageChange(searchResults.pagination.page + 1)}
                              className="px-3.5 py-2 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 disabled:opacity-40 flex items-center space-x-1"
                            >
                              <span>Next</span>
                              <ChevronRight className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      )}

                    </div>
                  )}

                </div>
              )}

              {/* STREAM VIEW 2: PCB (MEDICAL & HEALTHCARE) */}
              {selectedStream === 'PCB' && (
                <MedicalPredictor 
                  onSaveCollege={toggleSaveCollege}
                  isSavedMap={savedColleges.reduce((acc, c) => ({ ...acc, [c.id]: true }), {})}
                />
              )}

              {/* STREAM VIEW 3: COMMERCE & MANAGEMENT */}
              {selectedStream === 'COMMERCE' && (
                <CommerceSection 
                  onSaveCollege={toggleSaveCollege}
                  isSavedMap={savedColleges.reduce((acc, c) => ({ ...acc, [c.id]: true }), {})}
                />
              )}

              {/* STREAM VIEW 4: ARTS & HUMANITIES */}
              {selectedStream === 'ARTS' && (
                <ArtsSection 
                  onSaveCollege={toggleSaveCollege}
                  isSavedMap={savedColleges.reduce((acc, c) => ({ ...acc, [c.id]: true }), {})}
                />
              )}

            </div>

          </div>
        )}

        {/* VIEW 2: COLLEGES DIRECTORY */}
        {activeTab === 'colleges' && (
          <CollegeDirectory 
            onSaveCollege={toggleSaveCollege}
            isSavedMap={savedColleges.reduce((acc, c) => ({ ...acc, [c.id]: true }), {})}
          />
        )}

        {/* VIEW 3: CAREER EXPLORER */}
        {activeTab === 'careers' && (
          <CareerExplorer 
            onSelectCareerForRoadmap={navigateToCareerRoadmap}
          />
        )}

        {/* VIEW 4: PERSONALIZED ROADMAP */}
        {activeTab === 'roadmap' && (
          <PersonalizedRoadmap 
            initialCareer={prefilledCareer}
          />
        )}

        {/* VIEW 5: DATA ADMIN & QUALITY */}
        {activeTab === 'admin' && (
          <AdminDashboard />
        )}

        </ErrorBoundary>
      </main>

      {/* Cutoff Details Traceability Modal */}
      {selectedCutoffItem && (
        <CutoffDetailsModal 
          item={selectedCutoffItem} 
          onClose={() => setSelectedCutoffItem(null)} 
        />
      )}

      {/* Cutoff Trends Modal */}
      {selectedTrendItem && (
        <CutoffTrendsModal 
          item={selectedTrendItem} 
          onClose={() => setSelectedTrendItem(null)} 
        />
      )}

      {/* College Comparison Drawer */}
      <ComparisonDrawer 
        isOpen={isCompareOpen}
        onClose={() => setIsCompareOpen(false)}
        savedColleges={savedColleges}
        onRemove={handleRemoveSaved}
        onClearAll={handleClearAllSaved}
      />

      {/* Footer */}
      <Footer />

      {/* Margdarshak AI Floating Launcher Button (when modal is closed) */}
      {!isChatbotOpen && (
        <button
          onClick={() => setIsChatbotOpen(true)}
          className="fixed bottom-6 right-6 z-40 flex items-center space-x-2.5 px-4 py-3 bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-700 hover:to-indigo-700 text-white font-extrabold text-sm rounded-full shadow-2xl shadow-blue-600/40 hover:scale-105 transition-all cursor-pointer border border-white/20"
          title="Ask Margdarshak AI - Your Career Navigator"
        >
          <div className="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center">
            <Sparkles className="w-3.5 h-3.5 text-amber-300 animate-spin" style={{ animationDuration: '4s' }} />
          </div>
          <span>Ask Margdarshak</span>
        </button>
      )}

      {/* Margdarshak AI Career Chatbot */}
      <MargdarshakChatbot 
        isOpen={isChatbotOpen}
        onClose={() => setIsChatbotOpen(false)}
        onNavigateStream={handleNavigateStreamFromChatbot}
        initialQuery={heroPrompt}
        onClearInitialQuery={() => setHeroPrompt('')}
      />

    </div>
  );
}
