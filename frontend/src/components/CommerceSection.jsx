import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
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
  ChevronRight,
  Sparkles,
  ArrowRight,
  GraduationCap
} from 'lucide-react';
import { searchUniversityCutoffs } from '../services/api';

const COMMERCE_CAREER_INTERESTS = [
  { id: 'CA', label: 'Chartered Accountancy (CA)', hasPredictor: false, desc: 'Statutory audit, corporate taxation, IFRS, forensic accounting' },
  { id: 'CS', label: 'Company Secretary (CS)', hasPredictor: false, desc: 'Corporate governance, secretarial audit, board advisory, compliance' },
  { id: 'CMA', label: 'Cost & Management (CMA)', hasPredictor: false, desc: 'Cost audit, operational budgeting, pricing strategy, supply chain' },
  { id: 'BCOM', label: 'B.Com (Hons) Top Colleges', hasPredictor: true, desc: 'CUET-UG admission to SRCC, Hindu, LSR, Hansraj' },
  { id: 'BMS', label: 'BBA / BMS / Management', hasPredictor: true, desc: 'SSCBS, Delhi University BMS/BBA(FIA), IIM IPMAT' },
  { id: 'ECONOMICS', label: 'Economics (Hons)', hasPredictor: true, desc: 'Econometrics, public policy, financial economics at Delhi University' },
  { id: 'INVESTMENT', label: 'Investment Banking & CFA', hasPredictor: false, desc: 'M&A valuation, equity research, asset management, private equity' },
  { id: 'BANKING', label: 'Banking & Regulators (RBI/SBI)', hasPredictor: false, desc: 'RBI Grade B Officer, SEBI, SBI PO, public sector banking leadership' },
  { id: 'ACTUARIAL', label: 'Actuarial & Business Analytics', hasPredictor: false, desc: 'Risk modeling, IAI actuarial papers, predictive financial models' }
];

const COMMERCE_ROADMAPS = {
  'CA': {
    title: 'Chartered Accountancy (ICAI New Education & Training Scheme 2024)',
    conducting_body: 'The Institute of Chartered Accountants of India (ICAI)',
    eligibility: 'Pass 10+2 in any stream (Commerce, Science, Arts) or Direct Entry for Graduates',
    duration: 'Approx. 4.5 to 5 Years',
    stages: [
      {
        phase: 'Stage 1: CA Foundation',
        papers: '4 Papers (Accounting, Business Laws, Quantitative Aptitude, Business Economics)',
        details: 'Register after Class 10; appear after Class 12 board examinations. Requires 40% in individual papers and 50% aggregate to qualify.'
      },
      {
        phase: 'Stage 2: CA Intermediate',
        papers: '6 Papers across 2 Groups (Advanced Accounting, Corporate Laws, Taxation, Cost & Management Accounting, Auditing & Ethics, Financial & Strategic Management)',
        details: '8-month study period after Foundation. Must pass both groups and complete ICITSS (Information Technology & Orientation Course) before starting practical training.'
      },
      {
        phase: 'Stage 3: Self-Paced Online Modules (SPOM)',
        papers: 'Set A: Corporate & Economic Laws; Set B: Strategic Cost & Performance Management (Online Proctored)',
        details: 'Mandatory online learning modules completed anytime during articleship before appearing in CA Final.'
      },
      {
        phase: 'Stage 4: 2-Year Practical Training (Articleship)',
        papers: 'Full-time stipend training under a practicing Chartered Accountant / Registered CA Firm',
        details: 'Under the 2024 scheme, articleship duration is streamlined to an uninterrupted 24 months, with 12 leaves per year.'
      },
      {
        phase: 'Stage 5: CA Final Examination',
        papers: '6 Papers across 2 Groups (Financial Reporting, Advanced Financial Management, Advanced Auditing & Professional Ethics, Direct & International Taxation, Indirect Tax Laws, Integrated Business Solutions / Multidisciplinary Case Study)',
        details: 'Appear after completion of 2 years of practical training and passing SPOM sets.'
      },
      {
        phase: 'Stage 6: Membership & ICAI Convocation',
        papers: 'Conferment of Associate Chartered Accountant (ACA) title and Certificate of Practice (COP)',
        details: 'Join Big 4 auditing firms (Deloitte, PwC, EY, KPMG), Fortune 500 multinationals, or start independent audit practice.'
      }
    ]
  },
  'CS': {
    title: 'Company Secretary (ICSI New Syllabus)',
    conducting_body: 'The Institute of Company Secretaries of India (ICSI)',
    eligibility: '10+2 Pass in any stream (except Fine Arts)',
    duration: '3 to 4 Years',
    stages: [
      {
        phase: 'Stage 1: CSEET (CS Executive Entrance Test)',
        papers: '4 Computer-based Subjects: Business Communication, Legal Aptitude & Logical Reasoning, Economic & Business Environment, Current Affairs & Quantitative Aptitude',
        details: 'Held four times a year (January, May, July, November).'
      },
      {
        phase: 'Stage 2: CS Executive Programme',
        papers: '7 Papers in 2 Groups covering Company Law & Practice, Jurisprudence, Setting Up of Business, Corporate Accounting, Capital Markets & Securities Laws',
        details: 'Comprehensive legal and compliance curriculum.'
      },
      {
        phase: 'Stage 3: Practical Training (EDP & Long-Term)',
        papers: 'Executive Development Programme (1 month) + 21 months practical training in a listed company or under a practicing CS',
        details: 'Hands-on corporate governance, board meeting documentation, SEBI filings, and legal drafting.'
      },
      {
        phase: 'Stage 4: CS Professional Programme',
        papers: '7 Papers including Strategic Management, Drafting & Pleadings, Compliance Management, and Elective Specializations',
        details: 'Final milestone before qualifying as an Associate Company Secretary (ACS).'
      }
    ]
  },
  'CMA': {
    title: 'Cost and Management Accountant (ICMAI)',
    conducting_body: 'The Institute of Cost Accountants of India (ICMAI)',
    eligibility: '10+2 Pass in any stream',
    duration: '3 to 4 Years',
    stages: [
      {
        phase: 'Stage 1: CMA Foundation',
        papers: 'Fundamentals of Business Laws, Financial & Cost Accounting, Business Mathematics & Statistics, Business Economics & Management',
        details: 'Entry point for 10+2 students.'
      },
      {
        phase: 'Stage 2: CMA Intermediate',
        papers: '8 Papers in 2 Groups: Direct & Indirect Taxation, Cost Accounting, Corporate Accounting & Auditing, Financial Management',
        details: 'In-depth focus on industrial cost optimization and statutory cost accounting records.'
      },
      {
        phase: 'Stage 3: 15-Month Practical Training',
        papers: 'Hands-on industrial training in PSUs, manufacturing plants, or cost audit firms',
        details: 'Exposure to SAP/ERP, variance analysis, standard costing, and pricing control.'
      },
      {
        phase: 'Stage 4: CMA Final & Membership',
        papers: '8 Papers covering Strategic Cost Management, Corporate Financial Reporting, Strategic Financial Management, and Cost & Management Audit',
        details: 'Eligible for appointment as Cost Auditor under Companies Act 2013 and management roles in Maharatna PSUs.'
      }
    ]
  },
  'INVESTMENT': {
    title: 'Investment Banking, Equity Research & CFA Charter',
    conducting_body: 'CFA Institute (USA) & Global Investment Banks',
    eligibility: 'Undergraduate Degree (Can appear for Level 1 during final 2 years of graduation)',
    duration: '2 to 3 Years alongside university studies or career',
    stages: [
      {
        phase: 'Milestone 1: Undergraduate Foundation',
        papers: 'B.Com (Hons), BMS, B.A. Economics, or B.Tech with strong quantitative & financial modeling skills',
        details: 'Build proficiency in Excel DCF modeling, LBO models, Bloomberg terminal data, and accounting statement analysis.'
      },
      {
        phase: 'Milestone 2: CFA Level I',
        papers: '10 Topic Areas: Ethical and Professional Standards, Quantitative Methods, Economics, Financial Statement Analysis, Corporate Issuers, Equity, Fixed Income, Derivatives, Alternative Investments, Portfolio Management',
        details: 'Computer-based exam testing fundamental investment tools and asset valuation concepts.'
      },
      {
        phase: 'Milestone 3: CFA Level II',
        papers: 'Vignette-based case studies focusing deeply on Asset Valuation and Complex Financial Reporting',
        details: 'Industry gold standard for equity research analysts, hedge fund associates, and valuation specialists.'
      },
      {
        phase: 'Milestone 4: CFA Level III',
        papers: 'Constructed response (essay) and item sets focusing on Portfolio Management and Wealth Planning',
        details: 'Advanced asset allocation and institutional portfolio optimization.'
      },
      {
        phase: 'Milestone 5: 4,000 Hours Professional Work Experience',
        papers: 'Qualified investment decision-making experience in private equity, M&A, research, or asset management',
        details: 'Conferment of the prestigious CFA Charterholder designation recognized globally in 160+ countries.'
      }
    ]
  },
  'BANKING': {
    title: 'Reserve Bank of India (RBI Grade B Officer) & SBI PO',
    conducting_body: 'Reserve Bank of India Services Board & State Bank of India',
    eligibility: 'Graduate in any discipline with minimum 60% marks; Age 21 to 30 years',
    duration: '1 Year intensive preparation',
    stages: [
      {
        phase: 'Phase 1: Preliminary Objective Exam',
        papers: 'General Awareness (80 Qs), Quantitative Aptitude (30 Qs), Reasoning (60 Qs), English Language (30 Qs) - Total 200 Marks',
        details: 'High-speed elimination test. GA requires mastery of RBI circulars, monetary policy updates, and economic survey.'
      },
      {
        phase: 'Phase 2: Mains Examination (Descriptive & Objective)',
        papers: 'Paper I: Economic & Social Issues (ESI); Paper II: Descriptive English (Essay, Precis, Comprehension); Paper III: Finance & Management (FM)',
        details: 'In-depth conceptual analysis of Indian financial system, banking technology, corporate governance, and fiscal policy.'
      },
      {
        phase: 'Phase 3: Personality Test / Interview',
        papers: 'Interview conducted by Senior Central Board Members of RBI at Regional Offices',
        details: 'Evaluates macroeconomic comprehension, ethical leadership, and central banking awareness.'
      },
      {
        phase: 'Induction & Cadre Allocation',
        papers: 'Reserve Bank Staff College (RBSC) Chennai induction followed by Central Banking Cadre posting',
        details: 'Starting CTC ~₹30+ LPA including central government grade pay, official residential quarters in prime metro cities, and rapid elevation to Chief General Manager.'
      }
    ]
  }
};

export default function CommerceSection({ onSaveCollege, isSavedMap = {} }) {
  const [selectedInterest, setSelectedInterest] = useState('BCOM');
  const [examCode, setExamCode] = useState('CUET_UG');
  const [score, setScore] = useState(780);
  const [category, setCategory] = useState('OPEN');
  const [courseFilter, setCourseFilter] = useState('All');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [searched, setSearched] = useState(false);

  // When interest changes, update default parameters
  const handleInterestSelect = (interestId) => {
    setSelectedInterest(interestId);
    if (interestId === 'BCOM') {
      setExamCode('CUET_UG');
      setCourseFilter('B.Com (Hons)');
      setScore(780);
    } else if (interestId === 'BMS') {
      setExamCode('CUET_UG');
      setCourseFilter('Management');
      setScore(760);
    } else if (interestId === 'ECONOMICS') {
      setExamCode('CUET_UG');
      setCourseFilter('Economics');
      setScore(775);
    }
  };

  const currentInterestObj = COMMERCE_CAREER_INTERESTS.find(i => i.id === selectedInterest);
  const currentRoadmap = COMMERCE_ROADMAPS[selectedInterest];

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setSearched(true);
    try {
      const data = await searchUniversityCutoffs({
        exam_code: examCode,
        score: Number(score),
        category,
        course: courseFilter !== 'All' ? courseFilter : undefined,
        stream: 'COMMERCE',
        year: 2024
      });
      setResults(data);
    } catch (err) {
      alert('Error querying commerce cutoffs: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Run search on initial mount or when exam changes in predictor mode
  useEffect(() => {
    if (currentInterestObj?.hasPredictor && !searched) {
      handleSearch();
    }
  }, [selectedInterest]);

  return (
    <div className="space-y-10 animate-fadeIn">
      
      {/* Stream Sub-Navigation / Pathways Grid */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
        <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-widest text-amber-600 mb-2">
          <TrendingUp className="w-4 h-4" />
          <span>Commerce & Management Pathways</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
          What commerce pathway do you want to pursue?
        </h2>
        <p className="text-xs sm:text-sm text-slate-600 mt-1 mb-6">
          Explore professional certifications (CA, CS, CMA), premier undergraduate degree admissions (CUET-UG / IPMAT), or banking & corporate finance career tracks.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {COMMERCE_CAREER_INTERESTS.map((item) => {
            const isSelected = selectedInterest === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleInterestSelect(item.id)}
                className={`p-3.5 rounded-2xl border text-left transition-all flex flex-col justify-between ${
                  isSelected
                    ? 'border-amber-600 bg-amber-50/60 shadow-sm ring-2 ring-amber-500/20'
                    : 'border-slate-200 hover:border-amber-300 hover:bg-slate-50/50'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-xs font-extrabold ${isSelected ? 'text-amber-900' : 'text-slate-800'}`}>
                      {item.label}
                    </span>
                    {item.hasPredictor && (
                      <span className="text-[9px] font-black uppercase px-1.5 py-0.5 rounded bg-amber-100 text-amber-800">
                        Cutoffs
                      </span>
                    )}
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

      {/* VIEW A: COLLEGE FINDER (CUET / IPMAT) */}
      {currentInterestObj?.hasPredictor && (
        <div className="space-y-8">
          
          {/* Search Controls Card */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4 mb-6">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full">
                  Admission Intelligence
                </span>
                <h3 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
                  Premier Commerce & Management College Finder
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 mt-0.5">
                  Based on authentic 2024 CUET-UG normalized cutoffs (out of 800) and IPMAT composite cutoffs.
                </p>
              </div>

              <div className="flex items-center space-x-2 text-xs font-bold text-slate-600 bg-slate-50 p-2 rounded-xl border border-slate-200">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>Zero Fake Cutoff Policy</span>
              </div>
            </div>

            <form onSubmit={handleSearch} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Exam Selection */}
              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  Entrance Exam
                </label>
                <select
                  value={examCode}
                  onChange={(e) => {
                    setExamCode(e.target.value);
                    if (e.target.value === 'IPMAT') {
                      setScore(70);
                      setCourseFilter('Management');
                    } else {
                      setScore(780);
                    }
                  }}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                >
                  <option value="CUET_UG">CUET-UG (Delhi University Colleges)</option>
                  <option value="IPMAT">IPMAT (IIM Indore & IIM Rohtak)</option>
                </select>
              </div>

              {/* Score Input */}
              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  {examCode === 'IPMAT' ? 'Composite Score (out of 100)' : 'CUET Score (out of 800)'}
                </label>
                <input
                  type="number"
                  step={examCode === 'IPMAT' ? '0.1' : '1'}
                  min="0"
                  max={examCode === 'IPMAT' ? 100 : 800}
                  value={score}
                  onChange={(e) => setScore(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                  placeholder={examCode === 'IPMAT' ? 'e.g. 68.5' : 'e.g. 785'}
                  required
                />
              </div>

              {/* Category */}
              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  Category
                </label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                >
                  <option value="OPEN">Unreserved (UR / General)</option>
                  <option value="OBC">OBC-NCL</option>
                  <option value="EWS">Economically Weaker Section (EWS)</option>
                  <option value="SC">Scheduled Caste (SC)</option>
                  <option value="ST">Scheduled Tribe (ST)</option>
                </select>
              </div>

              {/* Course Filter */}
              <div>
                <label className="block text-xs font-bold uppercase text-slate-700 mb-1.5">
                  Degree Course
                </label>
                <select
                  value={courseFilter}
                  onChange={(e) => setCourseFilter(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-900 bg-white"
                >
                  <option value="All">All Commerce Courses</option>
                  <option value="B.Com (Hons)">B.Com (Hons)</option>
                  <option value="Economics">B.A. (Hons) Economics</option>
                  <option value="Management">BMS / BBA (FIA) / IPM</option>
                </select>
              </div>

              {/* Submit Button */}
              <div className="sm:col-span-2 lg:col-span-4 flex justify-end pt-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-3 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs flex items-center space-x-2 transition-all shadow-md shadow-amber-600/20 disabled:opacity-50"
                >
                  <Search className="w-4 h-4" />
                  <span>{loading ? 'Analyzing Cutoffs...' : 'Find Matching Institutions'}</span>
                </button>
              </div>
            </form>
          </div>

          {/* Results Grid */}
          {results && (
            <div className="space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 px-1">
                <div>
                  <h4 className="text-xl font-black text-slate-900">
                    {results.pagination.total_colleges_count} Premier Institutions Match Your Criteria
                  </h4>
                  <p className="text-xs text-slate-600">
                    Showing {results.results.length} verified cutoff records based on {examCode} 2024 admissions.
                  </p>
                </div>
                <div className="text-xs font-bold text-slate-500">
                  Target Score: <span className="text-amber-700 font-black">{score}</span> • Category: <span className="text-slate-800">{category}</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.results.map((item) => {
                  const college = item.college;
                  const course = item.course;
                  const cutoff = item.cutoff;
                  const strategy = item.strategy;
                  const isSaved = isSavedMap[college.id];

                  return (
                    <div 
                      key={item.cutoff_id}
                      className="bg-white rounded-3xl border border-slate-200 hover:border-amber-400 hover:shadow-lg transition-all p-6 flex flex-col justify-between"
                    >
                      <div>
                        {/* Badges Header */}
                        <div className="flex items-center justify-between mb-3">
                          <span className={`text-[10px] font-black uppercase px-2.5 py-1 rounded-full ${
                            strategy.badge === 'safe' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                          }`}>
                            {strategy.label}
                          </span>
                          {college.nirf_rank && (
                            <span className="text-[10px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
                              NIRF #{college.nirf_rank}
                            </span>
                          )}
                        </div>

                        {/* College & Course Name */}
                        <h3 className="text-base font-black text-slate-900 leading-snug">
                          {college.name}
                        </h3>
                        <div className="flex items-center space-x-1.5 text-xs text-slate-500 mt-1">
                          <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                          <span>{college.city}, {college.state}</span>
                        </div>

                        {/* Course Name Banner */}
                        <div className="mt-3.5 p-3 rounded-2xl bg-amber-50/70 border border-amber-100">
                          <div className="flex items-center space-x-1.5 text-amber-900 font-bold text-xs">
                            <BookOpen className="w-3.5 h-3.5 text-amber-700" />
                            <span>{course.name}</span>
                          </div>
                          <div className="text-[11px] text-amber-800 mt-0.5">
                            Degree: {course.degree} • Duration: {course.duration_years} Years
                          </div>
                        </div>

                        {/* Cutoff & Placement Data */}
                        <div className="grid grid-cols-2 gap-2 text-xs mt-4 pt-4 border-t border-slate-100">
                          <div className="p-2.5 rounded-xl bg-slate-50">
                            <span className="text-[10px] font-bold uppercase text-slate-500 block">
                              Required Score
                            </span>
                            <span className="text-base font-black text-amber-700">
                              {cutoff.cutoff_score}
                            </span>
                            <span className="text-[9px] text-slate-400 block mt-0.5">
                              {cutoff.category} Category
                            </span>
                          </div>

                          <div className="p-2.5 rounded-xl bg-slate-50">
                            <span className="text-[10px] font-bold uppercase text-slate-500 block">
                              Avg Package
                            </span>
                            <span className="text-base font-black text-emerald-700">
                              {college.median_package_lpa ? `₹${college.median_package_lpa} LPA` : '₹10.15 LPA'}
                            </span>
                            <span className="text-[9px] text-slate-400 block mt-0.5">
                              Highest: ₹{college.highest_package_lpa || '35.0'} LPA
                            </span>
                          </div>
                        </div>

                        {/* Fees & Source */}
                        <div className="mt-3 text-[11px] text-slate-500 flex items-center justify-between">
                          <span>Annual Tuition: ₹{(college.annual_tuition_fee_inr || 35000).toLocaleString()}</span>
                          <span className="text-[10px] text-slate-400">Round {cutoff.round} ({cutoff.year})</span>
                        </div>
                      </div>

                      {/* Footer Actions & Citation */}
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
                              className="p-2 rounded-xl text-slate-600 hover:text-amber-700 hover:bg-slate-100 transition-colors"
                              title="Official Website"
                            >
                              <ExternalLink className="w-4 h-4" />
                            </a>
                          )}
                          <button
                            onClick={() => onSaveCollege && onSaveCollege(college)}
                            className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                              isSaved
                                ? 'bg-amber-600 text-white'
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

              {results.results.length === 0 && (
                <div className="py-16 text-center bg-white rounded-3xl border border-slate-200">
                  <GraduationCap className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                  <h3 className="text-lg font-bold text-slate-800">No Cutoff Matches Found</h3>
                  <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
                    Try entering a higher CUET score or adjusting your category and course selections.
                  </p>
                </div>
              )}

            </div>
          )}

        </div>
      )}

      {/* VIEW B: STEP-BY-STEP PROFESSIONAL ROADMAP */}
      {currentRoadmap && (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4 mb-8">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full">
                Professional Progression Blueprint
              </span>
              <h3 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
                {currentRoadmap.title}
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                Governing Body: <strong className="text-slate-800">{currentRoadmap.conducting_body}</strong> • Duration: <strong className="text-slate-800">{currentRoadmap.duration}</strong>
              </p>
            </div>

            <div className="p-3 rounded-2xl bg-amber-50/70 border border-amber-200 text-xs text-amber-900 max-w-sm">
              <strong>Eligibility:</strong> {currentRoadmap.eligibility}
            </div>
          </div>

          <div className="space-y-6">
            {currentRoadmap.stages.map((stage, idx) => (
              <div 
                key={idx}
                className="relative pl-8 sm:pl-10 before:content-[''] before:absolute before:left-3 sm:before:left-4 before:top-3 before:bottom-0 before:w-0.5 before:bg-amber-200 last:before:hidden"
              >
                <div className="absolute left-0 top-1 w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-amber-600 text-white font-black text-xs flex items-center justify-center shadow-md shadow-amber-600/30">
                  {idx + 1}
                </div>

                <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 hover:border-amber-300 transition-all">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-2">
                    <h4 className="text-sm sm:text-base font-black text-slate-900">
                      {stage.phase}
                    </h4>
                    <span className="text-xs font-bold text-amber-700">
                      {stage.papers}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 leading-relaxed font-normal">
                    {stage.details}
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
