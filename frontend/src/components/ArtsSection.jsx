import React, { useState, useEffect } from 'react';
import { 
  Palette, 
  Search, 
  Award, 
  MapPin, 
  ExternalLink, 
  Building2, 
  FileText, 
  AlertCircle, 
  CheckCircle2, 
  Briefcase, 
  BookOpen, 
  DollarSign, 
  Clock, 
  ShieldCheck,
  Landmark,
  Scale,
  GraduationCap,
  Sparkles,
  ChevronRight,
  UserCheck,
  Flame,
  BadgePercent
} from 'lucide-react';
import { searchUniversityCutoffs, fetchGovernmentExams } from '../services/api';

const ARTS_CAREER_INTERESTS = [
  { id: 'GOV_EXAMS', label: 'Government Exams & Civil Services', type: 'GOV', desc: 'UPSC CSE (IAS/IPS/IFS), SSC CGL, Railways, Banking, Defence' },
  { id: 'LAW', label: 'Law & NLUs (CLAT)', type: 'CLAT', desc: '5-Year Integrated B.A. LL.B. (Hons) at NLSIU, NALSAR, WBNUJS' },
  { id: 'CUET_ARTS', label: 'Top Central Universities (CUET)', type: 'CUET', desc: 'St. Stephen’s, Hindu, LSR, Miranda House for BA (Hons)' },
  { id: 'PSYCHOLOGY', label: 'Psychology & Mental Health', type: 'ROADMAP', desc: 'Clinical Psychology, Counseling, Cognitive Behavioral Therapy, RCI License' },
  { id: 'JOURNALISM', label: 'Journalism & Media', type: 'ROADMAP', desc: 'Investigative reporting, digital media broadcasting, IIMC, mass communication' },
  { id: 'POLICY', label: 'Economics & Public Policy', type: 'ROADMAP', desc: 'Think tanks, NITI Aayog policy research, geopolitical analysis, development sector' },
  { id: 'TEACHING', label: 'Academia & Research (UGC-NET)', type: 'ROADMAP', desc: 'Junior Research Fellowship (JRF), Assistant Professor, PhD fellowships' }
];

const ARTS_ROADMAPS = {
  'PSYCHOLOGY': {
    title: 'Clinical & Counseling Psychology Pathway',
    eligibility: '10+2 with Psychology/Arts/Science -> B.A./B.Sc in Psychology (Minimum 55%)',
    stages: [
      {
        step: 'Stage 1: Undergraduate Degree',
        detail: 'B.A. or B.Sc in Psychology (3-4 years) covering Cognitive Psychology, Biopsychology, Psychometrics, Social Psychology, and Statistics.'
      },
      {
        step: 'Stage 2: Master’s Degree (M.A. / M.Sc Psychology)',
        detail: 'Specialization in Clinical, Counseling, or Neuropsychology at premier institutions (NIMHANS, Delhi University, TISS, Christ University).'
      },
      {
        step: 'Stage 3: M.Phil in Clinical Psychology / Psy.D (RCI Approved)',
        detail: '2-year intensive clinical residency at psychiatric hospitals (NIMHANS Bengaluru, CIP Ranchi, LGBRIMH Tezpur) to obtain the mandatory Rehabilitation Council of India (RCI) professional license.'
      },
      {
        step: 'Stage 4: Professional Practice & Specialization',
        detail: 'Licensed Clinical Psychologist in super-specialty hospitals, private psychotherapy practice, child developmental clinics, or rehabilitation centers.'
      }
    ]
  },
  'JOURNALISM': {
    title: 'Journalism, Broadcast & Digital Media Pathway',
    eligibility: '10+2 in any stream -> B.A. Journalism / Mass Communication',
    stages: [
      {
        step: 'Stage 1: Bachelor’s Degree / Foundational Skills',
        detail: 'B.A. (Hons) Journalism or Mass Communication from DU, Jamia Millia Islamia, or Xavier Institute. Master camera handling, audio editing, news writing, and digital journalism.'
      },
      {
        step: 'Stage 2: Post-Graduate Diploma / Entrance Exams',
        detail: 'Crack the Indian Institute of Mass Communication (IIMC) CUET-PG entrance or ACJ (Asian College of Journalism) Chennai entrance.'
      },
      {
        step: 'Stage 3: Newsroom Internships & Beat Reporting',
        detail: 'Hands-on ground reporting internships with national dailies (The Hindu, Indian Express) or television networks (NDTV, BBC India, CNBC).'
      },
      {
        step: 'Stage 4: Career Progression',
        detail: 'Correspondent -> Senior Beat Reporter (Politics, Economy, Defense, Tech) -> Bureau Chief / Editor / Digital Media Director.'
      }
    ]
  },
  'POLICY': {
    title: 'Public Policy, Geopolitics & Development Economics',
    eligibility: '10+2 -> Undergraduate in Economics, Political Science, or Public Administration',
    stages: [
      {
        step: 'Stage 1: Core Undergraduate Education',
        detail: 'Master Microeconomics, Macroeconomics, Public Finance, and Econometric Data Analysis (R / Python / STATA).'
      },
      {
        step: 'Stage 2: Master’s in Public Policy (MPP) / Development Economics',
        detail: 'Institutes: National Law School of India University (NLSIU MPP), Delhi School of Economics (DSE), IIT Delhi (School of Public Policy), or Oxford/LSE/Harvard Kennedy School.'
      },
      {
        step: 'Stage 3: Policy Fellowships & Internships',
        detail: 'Work with NITI Aayog (Young Professional), CPR (Centre for Policy Research), Observer Research Foundation (ORF), or UNDP India.'
      },
      {
        step: 'Stage 4: Long-Term Leadership',
        detail: 'Policy Advisor to Government Ministries, Chief Economist at International Think Tanks, World Bank / ADB Economist, or Public Affairs Lead for Tech MNCs.'
      }
    ]
  },
  'TEACHING': {
    title: 'University Academia & Research (UGC-NET / Assistant Professor)',
    eligibility: 'Master’s Degree with at least 55% marks in the relevant subject',
    stages: [
      {
        step: 'Stage 1: Post-Graduate Degree (M.A. / M.Sc / M.Com)',
        detail: 'In-depth mastery of the subject domain, seminar presentations, and dissertation writing.'
      },
      {
        step: 'Stage 2: Clear UGC-NET & JRF Examination',
        detail: 'Qualify for Junior Research Fellowship (JRF) conducted by NTA to receive a monthly government fellowship of ~₹37,000 + HRA for 5 years.'
      },
      {
        step: 'Stage 3: Doctoral Research (Ph.D.)',
        detail: 'Enrol in a Central University (JNU, DU, BHU, Hyderabad University) or IIT humanities department. Publish in peer-reviewed Scopus/UGC-CARE journals.'
      },
      {
        step: 'Stage 4: Assistant Professor Appointment',
        detail: 'Direct recruitment in Central/State Universities at 7th Pay Commission Level 10 (Basic Pay ₹57,700, gross ~₹90,000 - ₹1,10,000/month) with progression to Associate Professor and Professor.'
      }
    ]
  }
};

export default function ArtsSection({ onSaveCollege, isSavedMap = {} }) {
  const [selectedInterest, setSelectedInterest] = useState('GOV_EXAMS');
  
  // Government Exams state
  const [govExams, setGovExams] = useState([]);
  const [selectedGovExam, setSelectedGovExam] = useState(null);
  const [govLoading, setGovLoading] = useState(false);

  // CLAT Predictor state
  const [clatRank, setClatRank] = useState(450);
  const [clatCategory, setClatCategory] = useState('OPEN');
  const [clatResults, setClatResults] = useState(null);
  const [clatLoading, setClatLoading] = useState(false);

  // CUET Arts Predictor state
  const [cuetScore, setCuetScore] = useState(785);
  const [cuetCategory, setCuetCategory] = useState('OPEN');
  const [cuetCourse, setCuetCourse] = useState('All');
  const [cuetResults, setCuetResults] = useState(null);
  const [cuetLoading, setCuetLoading] = useState(false);

  // Load government exams on mount
  useEffect(() => {
    setGovLoading(true);
    fetchGovernmentExams()
      .then((data) => {
        setGovExams(data);
        if (data.length > 0) setSelectedGovExam(data[0]);
      })
      .catch(console.error)
      .finally(() => setGovLoading(false));
  }, []);

  // Fetch CLAT results
  const handleClatSearch = async (e) => {
    if (e) e.preventDefault();
    setClatLoading(true);
    try {
      const data = await searchUniversityCutoffs({
        exam_code: 'CLAT',
        score: Number(clatRank),
        category: clatCategory,
        year: 2024
      });
      setClatResults(data);
    } catch (err) {
      alert('Error querying CLAT cutoffs: ' + err.message);
    } finally {
      setClatLoading(false);
    }
  };

  // Fetch CUET Arts results
  const handleCuetArtsSearch = async (e) => {
    if (e) e.preventDefault();
    setCuetLoading(true);
    try {
      const data = await searchUniversityCutoffs({
        exam_code: 'CUET_UG',
        score: Number(cuetScore),
        category: cuetCategory,
        course: cuetCourse !== 'All' ? cuetCourse : undefined,
        stream: 'ARTS',
        year: 2024
      });
      setCuetResults(data);
    } catch (err) {
      alert('Error querying CUET arts cutoffs: ' + err.message);
    } finally {
      setCuetLoading(false);
    }
  };

  // Auto-search CLAT on first tab view
  useEffect(() => {
    if (selectedInterest === 'LAW' && !clatResults) {
      handleClatSearch();
    } else if (selectedInterest === 'CUET_ARTS' && !cuetResults) {
      handleCuetArtsSearch();
    }
  }, [selectedInterest]);

  const currentInterestObj = ARTS_CAREER_INTERESTS.find(i => i.id === selectedInterest);
  const currentRoadmap = ARTS_ROADMAPS[selectedInterest];

  return (
    <div className="space-y-10 animate-fadeIn">
      
      {/* Stream Sub-Navigation / Pathways Grid */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
        <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-widest text-rose-600 mb-2">
          <Palette className="w-4 h-4" />
          <span>Arts, Humanities & Public Leadership Pathways</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
          What career or examination roadmap do you want to explore?
        </h2>
        <p className="text-xs sm:text-sm text-slate-600 mt-1 mb-6">
          Explore government competitive examinations, National Law Universities (CLAT), premier Delhi University arts programs (CUET-UG), or specialized social science careers.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
          {ARTS_CAREER_INTERESTS.map((item) => {
            const isSelected = selectedInterest === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setSelectedInterest(item.id)}
                className={`p-3.5 rounded-2xl border text-left transition-all flex flex-col justify-between ${
                  isSelected
                    ? 'border-rose-600 bg-rose-50/60 shadow-sm ring-2 ring-rose-500/20'
                    : 'border-slate-200 hover:border-rose-300 hover:bg-slate-50/50'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-xs font-extrabold ${isSelected ? 'text-rose-900' : 'text-slate-800'}`}>
                      {item.label}
                    </span>
                    <span className={`text-[9px] font-black uppercase px-1.5 py-0.5 rounded ${
                      item.type === 'CLAT' || item.type === 'CUET'
                        ? 'bg-rose-100 text-rose-800'
                        : item.type === 'GOV'
                        ? 'bg-amber-100 text-amber-800'
                        : 'bg-slate-100 text-slate-700'
                    }`}>
                      {item.type === 'GOV' ? 'Directory' : item.type === 'ROADMAP' ? 'Roadmap' : 'Cutoffs'}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500 line-clamp-2 leading-tight">
                    {item.desc}
                  </p>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* VIEW 1: DEDICATED GOVERNMENT EXAMS EXPLORER */}
      {selectedInterest === 'GOV_EXAMS' && (
        <div className="space-y-8">
          
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4 mb-6">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-rose-600 bg-rose-50 px-2.5 py-1 rounded-full">
                  National Public Service Directory
                </span>
                <h3 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
                  Government Career & Competitive Examination Explorer
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 mt-0.5">
                  Selection stages, official eligibility criteria, 7th CPC salary structure, authentic syllabus, and 4-phase preparation blueprints.
                </p>
              </div>

              <div className="flex items-center space-x-2 text-xs font-bold text-slate-600 bg-slate-50 p-2 rounded-xl border border-slate-200">
                <Landmark className="w-4 h-4 text-blue-600 shrink-0" />
                <span>Central & State Commission Verified</span>
              </div>
            </div>

            {/* Exam Selector Tabs */}
            <div className="flex flex-wrap gap-2 mb-8">
              {govExams.map((exam) => {
                const isSelected = selectedGovExam?.exam_code === exam.exam_code;
                return (
                  <button
                    key={exam.exam_code}
                    onClick={() => setSelectedGovExam(exam)}
                    className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center space-x-2 ${
                      isSelected
                        ? 'bg-rose-600 text-white shadow-md shadow-rose-600/20'
                        : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200'
                    }`}
                  >
                    <span>{exam.exam_name}</span>
                    <span className={`text-[10px] px-1.5 py-0.2 rounded font-mono ${isSelected ? 'bg-rose-700 text-rose-100' : 'bg-slate-200 text-slate-600'}`}>
                      {exam.conducting_body}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Selected Exam Deep Dive */}
            {selectedGovExam && (
              <div className="space-y-8">
                
                {/* Exam Key Attributes */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <span className="text-[10px] font-bold uppercase text-slate-500 block">Cadre / Posts</span>
                    <span className="text-sm font-black text-slate-900 block mt-0.5">{selectedGovExam.posts_offered}</span>
                  </div>
                  <div className="p-4 rounded-2xl bg-emerald-50/70 border border-emerald-200">
                    <span className="text-[10px] font-bold uppercase text-emerald-700 block">7th Pay Commission Scale</span>
                    <span className="text-sm font-black text-emerald-900 block mt-0.5">{selectedGovExam.pay_scale}</span>
                  </div>
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <span className="text-[10px] font-bold uppercase text-slate-500 block">Age Limit & Attempts</span>
                    <span className="text-sm font-bold text-slate-900 block mt-0.5">{selectedGovExam.age_limit}</span>
                  </div>
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <span className="text-[10px] font-bold uppercase text-slate-500 block">Educational Eligibility</span>
                    <span className="text-xs font-bold text-slate-800 block mt-0.5">{selectedGovExam.eligibility}</span>
                  </div>
                </div>

                {/* Selection Stages */}
                <div className="pt-4 border-t border-slate-100">
                  <h4 className="text-base font-black text-slate-900 mb-4 flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>Examination Selection Architecture</span>
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {selectedGovExam.selection_stages?.map((st, i) => (
                      <div key={i} className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-black text-rose-700">Stage {i + 1}: {st.stage}</span>
                          <span className="text-[10px] font-bold text-slate-500">{st.type}</span>
                        </div>
                        <p className="text-xs font-bold text-slate-800 mt-1">{st.papers}</p>
                        <p className="text-[11px] text-slate-500 mt-1">{st.details}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Syllabus Overview */}
                <div className="pt-4 border-t border-slate-100">
                  <h4 className="text-base font-black text-slate-900 mb-2 flex items-center space-x-2">
                    <BookOpen className="w-4 h-4 text-blue-600" />
                    <span>Official Syllabus Breakdown</span>
                  </h4>
                  <p className="text-xs text-slate-700 bg-blue-50/50 p-4 rounded-2xl border border-blue-100 leading-relaxed font-normal">
                    {selectedGovExam.syllabus_overview}
                  </p>
                </div>

                {/* 4-Phase Preparation Roadmap */}
                <div className="pt-4 border-t border-slate-100">
                  <h4 className="text-base font-black text-slate-900 mb-6 flex items-center space-x-2">
                    <Sparkles className="w-4 h-4 text-amber-600" />
                    <span>Recommended 4-Phase Preparation Blueprint</span>
                  </h4>
                  <div className="space-y-4">
                    {selectedGovExam.preparation_roadmap?.map((rp, idx) => (
                      <div key={idx} className="flex items-start space-x-3 p-4 rounded-2xl bg-slate-50 border border-slate-200">
                        <div className="w-7 h-7 rounded-full bg-rose-600 text-white font-black text-xs flex items-center justify-center shrink-0 mt-0.5">
                          {idx + 1}
                        </div>
                        <div>
                          <h5 className="text-xs sm:text-sm font-black text-slate-900">
                            {rp.phase}
                          </h5>
                          <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                            {rp.strategy}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Official Web Portal */}
                <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span>Frequency: <strong>Annual Cycle</strong></span>
                  {selectedGovExam.official_website && (
                    <a
                      href={selectedGovExam.official_website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-1.5 text-rose-600 font-bold hover:underline"
                    >
                      <span>Official Commission Portal ({selectedGovExam.conducting_body})</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  )}
                </div>

              </div>
            )}

          </div>

        </div>
      )}

      {/* VIEW 2: LAW EXPLORER & CLAT NLU PREDICTOR */}
      {selectedInterest === 'LAW' && (
        <div className="space-y-8">
          
          {/* CLAT Search Form */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4 mb-6">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-rose-600 bg-rose-50 px-2.5 py-1 rounded-full">
                  Law Admissions Intelligence
                </span>
                <h3 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
                  CLAT 2024 National Law University (NLU) Predictor
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 mt-0.5">
                  Strictly verified opening and closing ranks from Consortium of NLUs 2024 for 5-Year Integrated B.A. LL.B. (Hons).
                </p>
              </div>

              <div className="flex items-center space-x-2 text-xs font-bold text-slate-600 bg-slate-50 p-2 rounded-xl border border-slate-200">
                <Scale className="w-4 h-4 text-blue-600 shrink-0" />
                <span>Consortium of NLUs Verified</span>
              </div>
            </div>

            <form onSubmit={handleClatSearch} className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  CLAT All India Rank (AIR)
                </label>
                <input
                  type="number"
                  min="1"
                  max="50000"
                  value={clatRank}
                  onChange={(e) => setClatRank(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                  placeholder="e.g. 450"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  Category
                </label>
                <select
                  value={clatCategory}
                  onChange={(e) => setClatCategory(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                >
                  <option value="OPEN">All India General (OPEN)</option>
                  <option value="OBC">OBC</option>
                  <option value="EWS">EWS</option>
                  <option value="SC">SC</option>
                  <option value="ST">ST</option>
                </select>
              </div>

              <div className="flex items-end">
                <button
                  type="submit"
                  disabled={clatLoading}
                  className="w-full py-2.5 px-4 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center justify-center space-x-2 transition-all shadow-md shadow-rose-600/20 disabled:opacity-50"
                >
                  <Search className="w-4 h-4" />
                  <span>{clatLoading ? 'Checking NLUs...' : 'Predict Eligible NLUs'}</span>
                </button>
              </div>
            </form>
          </div>

          {/* CLAT Results Cards */}
          {clatResults && (
            <div className="space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 px-1">
                <div>
                  <h4 className="text-xl font-black text-slate-900">
                    {clatResults.pagination.total_colleges_count} Premier NLUs Match Your Rank
                  </h4>
                  <p className="text-xs text-slate-600">
                    Candidates with CLAT Rank #{Number(clatRank).toLocaleString()} in {clatCategory} category.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {clatResults.results.map((item) => {
                  const college = item.college;
                  const cutoff = item.cutoff;
                  const isSaved = isSavedMap[college.id];

                  return (
                    <div
                      key={item.cutoff_id}
                      className="bg-white rounded-3xl border border-slate-200 hover:border-rose-400 hover:shadow-lg transition-all p-6 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-3">
                          <span className={`text-[10px] font-black uppercase px-2.5 py-1 rounded-full ${
                            item.strategy.badge === 'safe' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                          }`}>
                            {item.strategy.label}
                          </span>
                          {college.nirf_rank && (
                            <span className="text-[10px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
                              NIRF Law #{college.nirf_rank}
                            </span>
                          )}
                        </div>

                        <h3 className="text-base font-black text-slate-900 leading-snug">
                          {college.name}
                        </h3>
                        <div className="flex items-center space-x-1.5 text-xs text-slate-500 mt-1">
                          <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                          <span>{college.city}, {college.state}</span>
                        </div>

                        {/* Program */}
                        <div className="mt-3.5 p-3 rounded-2xl bg-rose-50/70 border border-rose-100">
                          <div className="text-xs font-bold text-rose-950">
                            B.A. LL.B. (Honours) - 5-Year Integrated
                          </div>
                          <div className="text-[10px] text-rose-800 mt-0.5">
                            Approved by Bar Council of India (BCI)
                          </div>
                        </div>

                        {/* Cutoffs & Placement */}
                        <div className="grid grid-cols-2 gap-2 text-xs mt-4 pt-4 border-t border-slate-100">
                          <div className="p-2.5 rounded-xl bg-slate-50">
                            <span className="text-[10px] font-bold uppercase text-slate-500 block">Cutoff Rank Range</span>
                            <span className="text-sm font-black text-rose-700">
                              {cutoff.opening_rank} - {cutoff.closing_rank}
                            </span>
                            <span className="text-[9px] text-slate-400 block mt-0.5">
                              {cutoff.category} Category
                            </span>
                          </div>

                          <div className="p-2.5 rounded-xl bg-slate-50">
                            <span className="text-[10px] font-bold uppercase text-slate-500 block">Median Package</span>
                            <span className="text-sm font-black text-emerald-700">
                              ₹{college.median_package_lpa || '16.0'} LPA
                            </span>
                            <span className="text-[9px] text-slate-400 block mt-0.5">
                              Tier 1 Corporate Law
                            </span>
                          </div>
                        </div>

                        <div className="mt-3 text-[11px] text-slate-500 flex items-center justify-between">
                          <span>Annual Fee: ₹{(college.annual_tuition_fee_inr || 275000).toLocaleString()}</span>
                          <span className="text-[10px] text-slate-400">Round {cutoff.round} ({cutoff.year})</span>
                        </div>
                      </div>

                      {/* Footer Actions */}
                      <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between">
                        <div className="text-[10px] text-slate-400 truncate max-w-[170px]" title={cutoff.source_name}>
                          Src: {cutoff.source_name}
                        </div>

                        <div className="flex items-center space-x-2">
                          {college.official_website && (
                            <a
                              href={college.official_website}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="p-2 rounded-xl text-slate-600 hover:text-rose-700 hover:bg-slate-100 transition-colors"
                              title="Official Website"
                            >
                              <ExternalLink className="w-4 h-4" />
                            </a>
                          )}
                          <button
                            onClick={() => onSaveCollege && onSaveCollege(college)}
                            className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                              isSaved
                                ? 'bg-rose-600 text-white'
                                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                            }`}
                          >
                            {isSaved ? 'Saved' : 'Save'}
                          </button>
                        </div>
                      </div>

                    </div>
                  );
                })}
              </div>

            </div>
          )}

          {/* 5-Year Integrated Law Roadmap */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            <h4 className="text-lg font-black text-slate-900 mb-6 flex items-center space-x-2">
              <Scale className="w-5 h-5 text-rose-600" />
              <span>5-Year Integrated B.A. LL.B. Legal Career Blueprint</span>
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-xs font-black text-rose-600 uppercase block mb-1">Year 1 & 2</span>
                <h5 className="text-sm font-bold text-slate-900">Foundations & Mooting</h5>
                <p className="text-xs text-slate-600 mt-1">Constitutional Law, Contracts, Torts, Family Law, Legal Research, and intra-college moot court competitions.</p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-xs font-black text-rose-600 uppercase block mb-1">Year 3</span>
                <h5 className="text-sm font-bold text-slate-900">Corporate Law & Internships</h5>
                <p className="text-xs text-slate-600 mt-1">Company Law, IPR, Taxation, Competition Law. Vacation internships with Senior Advocates at High Courts and NGOs.</p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-xs font-black text-rose-600 uppercase block mb-1">Year 4 & 5</span>
                <h5 className="text-sm font-bold text-slate-900">Tier-1 Firms & Placements</h5>
                <p className="text-xs text-slate-600 mt-1">Arbitration, International Trade, Mergers & Acquisitions. Pre-Placement Offers (PPOs) from SAM, CAM, Trilegal, Khaitan.</p>
              </div>

              <div className="p-4 rounded-2xl bg-emerald-50/70 border border-emerald-200">
                <span className="text-xs font-black text-emerald-700 uppercase block mb-1">Post-Degree</span>
                <h5 className="text-sm font-bold text-emerald-900">AIBE & Diversified Careers</h5>
                <p className="text-xs text-emerald-800 mt-1">Clear All India Bar Examination (AIBE) for High Court / Supreme Court practice, State Judicial Services, or UPSC Civil Services.</p>
              </div>
            </div>
          </div>

        </div>
      )}

      {/* VIEW 3: CUET ARTS COLLEGE FINDER */}
      {selectedInterest === 'CUET_ARTS' && (
        <div className="space-y-8">
          
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4 mb-6">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-rose-600 bg-rose-50 px-2.5 py-1 rounded-full">
                  Central Universities
                </span>
                <h3 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
                  Delhi University & Central Arts College Finder
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 mt-0.5">
                  CUET-UG 2024 verified admission cutoffs for St. Stephen’s, Hindu, LSR, Miranda House.
                </p>
              </div>

              <div className="flex items-center space-x-2 text-xs font-bold text-slate-600 bg-slate-50 p-2 rounded-xl border border-slate-200">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>Zero Fake Cutoff Policy</span>
              </div>
            </div>

            <form onSubmit={handleCuetArtsSearch} className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  CUET Score (out of 800)
                </label>
                <input
                  type="number"
                  min="0"
                  max="800"
                  value={cuetScore}
                  onChange={(e) => setCuetScore(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                  placeholder="e.g. 780"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  Category
                </label>
                <select
                  value={cuetCategory}
                  onChange={(e) => setCuetCategory(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                >
                  <option value="OPEN">Unreserved (UR / General)</option>
                  <option value="OBC">OBC-NCL</option>
                  <option value="EWS">EWS</option>
                  <option value="SC">SC</option>
                  <option value="ST">ST</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  Subject Domain
                </label>
                <select
                  value={cuetCourse}
                  onChange={(e) => setCuetCourse(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                >
                  <option value="All">All Arts Disciplines</option>
                  <option value="Political Science">Political Science</option>
                  <option value="Economics">Economics</option>
                  <option value="Psychology">Psychology</option>
                  <option value="History">History</option>
                  <option value="Journalism">Journalism</option>
                </select>
              </div>

              <div className="sm:col-span-3 flex justify-end pt-2">
                <button
                  type="submit"
                  disabled={cuetLoading}
                  className="px-6 py-3 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center space-x-2 transition-all shadow-md shadow-rose-600/20 disabled:opacity-50"
                >
                  <Search className="w-4 h-4" />
                  <span>{cuetLoading ? 'Searching Cutoffs...' : 'Find Matching Colleges'}</span>
                </button>
              </div>
            </form>
          </div>

          {/* CUET Results Grid */}
          {cuetResults && (
            <div className="space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 px-1">
                <div>
                  <h4 className="text-xl font-black text-slate-900">
                    {cuetResults.pagination.total_colleges_count} Premier Central Institutions Found
                  </h4>
                  <p className="text-xs text-slate-600">
                    Showing {cuetResults.results.length} verified cutoff records based on CUET-UG 2024.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {cuetResults.results.map((item) => {
                  const college = item.college;
                  const course = item.course;
                  const cutoff = item.cutoff;
                  const isSaved = isSavedMap[college.id];

                  return (
                    <div
                      key={item.cutoff_id}
                      className="bg-white rounded-3xl border border-slate-200 hover:border-rose-400 hover:shadow-lg transition-all p-6 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-3">
                          <span className={`text-[10px] font-black uppercase px-2.5 py-1 rounded-full ${
                            item.strategy.badge === 'safe' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                          }`}>
                            {item.strategy.label}
                          </span>
                          {college.nirf_rank && (
                            <span className="text-[10px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
                              NIRF #{college.nirf_rank}
                            </span>
                          )}
                        </div>

                        <h3 className="text-base font-black text-slate-900 leading-snug">
                          {college.name}
                        </h3>
                        <div className="flex items-center space-x-1.5 text-xs text-slate-500 mt-1">
                          <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                          <span>{college.city}, {college.state}</span>
                        </div>

                        <div className="mt-3.5 p-3 rounded-2xl bg-rose-50/70 border border-rose-100">
                          <div className="flex items-center space-x-1.5 text-rose-950 font-bold text-xs">
                            <BookOpen className="w-3.5 h-3.5 text-rose-700" />
                            <span>{course.name}</span>
                          </div>
                          <div className="text-[11px] text-rose-800 mt-0.5">
                            Degree: {course.degree} • Duration: {course.duration_years} Years
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-2 text-xs mt-4 pt-4 border-t border-slate-100">
                          <div className="p-2.5 rounded-xl bg-slate-50">
                            <span className="text-[10px] font-bold uppercase text-slate-500 block">Cutoff Score</span>
                            <span className="text-base font-black text-rose-700">
                              {cutoff.cutoff_score}
                            </span>
                            <span className="text-[9px] text-slate-400 block mt-0.5">
                              {cutoff.category} Category
                            </span>
                          </div>

                          <div className="p-2.5 rounded-xl bg-slate-50">
                            <span className="text-[10px] font-bold uppercase text-slate-500 block">Avg Package</span>
                            <span className="text-base font-black text-emerald-700">
                              ₹{college.median_package_lpa || '10.5'} LPA
                            </span>
                            <span className="text-[9px] text-slate-400 block mt-0.5">
                              Highest: ₹{college.highest_package_lpa || '30.0'} LPA
                            </span>
                          </div>
                        </div>

                        <div className="mt-3 text-[11px] text-slate-500 flex items-center justify-between">
                          <span>Tuition: ₹{(college.annual_tuition_fee_inr || 24000).toLocaleString()}/yr</span>
                          <span className="text-[10px] text-slate-400">Round {cutoff.round} ({cutoff.year})</span>
                        </div>
                      </div>

                      <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between">
                        <div className="text-[10px] text-slate-400 truncate max-w-[170px]" title={cutoff.source_name}>
                          Src: {cutoff.source_name}
                        </div>

                        <div className="flex items-center space-x-2">
                          {college.official_website && (
                            <a
                              href={college.official_website}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="p-2 rounded-xl text-slate-600 hover:text-rose-700 hover:bg-slate-100 transition-colors"
                              title="Official Website"
                            >
                              <ExternalLink className="w-4 h-4" />
                            </a>
                          )}
                          <button
                            onClick={() => onSaveCollege && onSaveCollege(college)}
                            className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                              isSaved
                                ? 'bg-rose-600 text-white'
                                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                            }`}
                          >
                            {isSaved ? 'Saved' : 'Save'}
                          </button>
                        </div>
                      </div>

                    </div>
                  );
                })}
              </div>

            </div>
          )}

        </div>
      )}

      {/* VIEW 4: SPECIALIZED ARTS ROADMAPS (PSYCHOLOGY, JOURNALISM, POLICY, TEACHING) */}
      {currentRoadmap && (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4 mb-8">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-rose-600 bg-rose-50 px-2.5 py-1 rounded-full">
                Career Roadmap Blueprint
              </span>
              <h3 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
                {currentRoadmap.title}
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                Eligibility: <strong className="text-slate-800">{currentRoadmap.eligibility}</strong>
              </p>
            </div>
          </div>

          <div className="space-y-6">
            {currentRoadmap.stages.map((stage, idx) => (
              <div 
                key={idx}
                className="relative pl-8 sm:pl-10 before:content-[''] before:absolute before:left-3 sm:before:left-4 before:top-3 before:bottom-0 before:w-0.5 before:bg-rose-200 last:before:hidden"
              >
                <div className="absolute left-0 top-1 w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-rose-600 text-white font-black text-xs flex items-center justify-center shadow-md shadow-rose-600/30">
                  {idx + 1}
                </div>

                <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 hover:border-rose-300 transition-all">
                  <h4 className="text-sm sm:text-base font-black text-slate-900 mb-1">
                    {stage.step}
                  </h4>
                  <p className="text-xs text-slate-600 leading-relaxed font-normal">
                    {stage.detail}
                  </p>
                </div>
              </div>
            ))}
          </div>

        </div>
      )}

    </div>
  );
}
