import React, { useState, useEffect } from 'react';
import { 
  Stethoscope, 
  Search, 
  Award, 
  MapPin, 
  ExternalLink, 
  Building2, 
  FileText, 
  AlertCircle, 
  CheckCircle2, 
  Dna, 
  BookOpen, 
  DollarSign, 
  Clock, 
  ShieldCheck,
  Activity,
  Sparkles
} from 'lucide-react';
import { searchNeetCutoffs } from '../services/api';

const PCB_CAREER_INTERESTS = [
  { id: 'Medicine', label: 'Medicine (MBBS)', hasPredictor: true, desc: 'Primary physician, surgery, specialized medical practice' },
  { id: 'Dentistry', label: 'Dentistry (BDS)', hasPredictor: true, desc: 'Oral surgery, orthodontics, cosmetic dentistry' },
  { id: 'Pharmacy', label: 'Pharmacy (B.Pharm)', hasPredictor: false, desc: 'Drug discovery, clinical trials, pharmacology' },
  { id: 'Nursing', label: 'Nursing (B.Sc Nursing)', hasPredictor: false, desc: 'Critical intensive care, clinical patient management' },
  { id: 'Physiotherapy', label: 'Physiotherapy (BPT)', hasPredictor: false, desc: 'Neuro-rehabilitation, sports injuries, musculoskeletal' },
  { id: 'Biotechnology', label: 'Biotechnology & Genomics', hasPredictor: false, desc: 'CRISPR, molecular genetics, bioprocessing' },
  { id: 'Veterinary', label: 'Veterinary (BVSc & AH)', hasPredictor: false, desc: 'Animal health, clinical veterinary surgery, zoonoses' },
  { id: 'AYUSH', label: 'AYUSH (BAMS / BHMS)', hasPredictor: false, desc: 'Ayurvedic & Homeopathic clinical medicine' },
  { id: 'Allied Health', label: 'Allied Health Sciences', hasPredictor: false, desc: 'Radiology technology, medical lab diagnostics' },
  { id: 'Research', label: 'Clinical Research & Academia', hasPredictor: false, desc: 'ICMR fellowships, life sciences research, PhD' }
];

const PCB_ROADMAPS = {
  'Pharmacy': {
    degree: 'B.Pharm (4 Years) -> M.Pharm / Pharm.D',
    entrance: 'State CETs (WBJEE Pharmacy, MHT CET, KCET) / CUET-UG / Merit',
    stages: [
      { step: '12th PCB', detail: 'Minimum 50% aggregate in Physics, Chemistry, Biology/Mathematics.' },
      { step: 'Entrance / Admission', detail: 'Appear in State Pharmacy CETs or Central University CUET.' },
      { step: 'Degree Program', detail: '4-year B.Pharm covering Medicinal Chemistry, Pharmacology, Pharmaceutics, and Drug Formulations.' },
      { step: 'Industrial Internship', detail: 'Mandatory 150-hour industrial training at GMP/USFDA approved manufacturing facilities.' },
      { step: 'Higher Studies & GPAT', detail: 'Qualify GPAT (Graduate Pharmacy Aptitude Test) for M.Pharm at NIPER or pursue MS abroad.' },
      { step: 'Career Roles', detail: 'Formulation Scientist, Regulatory Affairs Associate, Clinical Research Coordinator, Quality Control Analyst.' }
    ]
  },
  'Veterinary': {
    degree: 'B.V.Sc & A.H. (5.5 Years including 1 Year Internship)',
    entrance: 'NEET-UG (15% All-India Veterinary Council Quota) & State Veterinary Entrances',
    stages: [
      { step: '12th PCB', detail: 'Physics, Chemistry, Biology with minimum 50% marks.' },
      { step: 'Entrance Exam', detail: 'NEET-UG score used by VCI for 15% All India Quota seats in Government Veterinary Colleges.' },
      { step: 'Degree Program', detail: 'Veterinary Gross Anatomy, Animal Genetics, Surgery, Animal Pathology, Pharmacology, and Livestock Nutrition.' },
      { step: 'Clinical Internship', detail: '6-month clinical veterinary teaching hospital posting + 6-month farm & zoo clinical rotations.' },
      { step: 'Licensing', detail: 'Registration with State Veterinary Council / Veterinary Council of India (VCI).' },
      { step: 'Career Roles', detail: 'Veterinary Surgeon, Livestock Development Officer, Wildlife Veterinarian, Animal Nutritionist.' }
    ]
  },
  'Physiotherapy': {
    degree: 'Bachelor of Physiotherapy - BPT (4.5 Years)',
    entrance: 'State Entrances / University Aptitude / NEET in select states',
    stages: [
      { step: '12th PCB', detail: 'Class 12 with Physics, Chemistry, Biology and English.' },
      { step: 'Degree Coursework', detail: 'Anatomy, Exercise Therapy, Biomechanics, Electrotherapy, Neuro-physiotherapy, Cardio-respiratory therapy.' },
      { step: 'Rotary Internship', detail: '6-month full-time rotating clinical hospital internship across Orthopedics, Neurology, ICU, and Sports medicine.' },
      { step: 'Specialization (MPT)', detail: 'Master of Physiotherapy (MPT) in Sports Rehabilitation, Orthopedics, or Neurology.' },
      { step: 'Career Roles', detail: 'Sports Team Physiotherapist (BCCI/IPL/ISL), Hospital Neuro-rehab Specialist, Ergonomics Consultant.' }
    ]
  },
  'Nursing': {
    degree: 'B.Sc Nursing (4 Years)',
    entrance: 'NEET-UG (for Military Nursing, AIIMS, JIPMER) & State Nursing Entrances',
    stages: [
      { step: '12th PCB', detail: 'Physics, Chemistry, Biology with minimum 45% aggregate.' },
      { step: 'Entrance Examination', detail: 'AIIMS B.Sc Nursing Entrance / NEET-UG / State Nursing Council Tests.' },
      { step: 'Degree & Clinical Training', detail: 'Anatomy, Medical-Surgical Nursing, Pharmacology, Obstetric Nursing, and Pediatric Patient Care.' },
      { step: 'Hospital Postings', detail: 'Hands-on clinical rotations in Emergency, ICU, Operation Theatres, and Community Health.' },
      { step: 'Council Registration', detail: 'Register as Registered Nurse & Registered Midwife (RN/RM) with State Nursing Council.' },
      { step: 'Career Roles', detail: 'Critical Care Nursing Officer, Nurse Practitioner, Military Nursing Services (MNS), Hospital Admin.' }
    ]
  },
  'Biotechnology': {
    degree: 'B.Tech / B.Sc Biotechnology (3-4 Years)',
    entrance: 'JEE Main / State CETs / CUET-UG / University Entrance',
    stages: [
      { step: '12th PCB / PCMB', detail: 'Strong foundation in Biology, Chemistry, and Mathematics.' },
      { step: 'Undergraduate Program', detail: 'Recombinant DNA technology, Molecular Genetics, Fermentation Bioprocess, and Python Bioinformatics.' },
      { step: 'Research Fellowships', detail: 'Apply for IASc-INSA-NASI Summer Research Fellowships at IISc, NCBS, or IITs.' },
      { step: 'Higher Studies (M.Tech/MS/PhD)', detail: 'GATE Biotechnology / CSIR-NET JRF / GRE for international doctoral programs.' },
      { step: 'Career Roles', detail: 'Genomic Data Analyst, Bioprocess Engineer, CRISPR Research Scientist, Bioinformatics Consultant.' }
    ]
  }
};

export default function MedicalPredictor({ onSaveCollege, isSavedMap = {} }) {
  const [selectedInterest, setSelectedInterest] = useState('Medicine');
  const [rank, setRank] = useState(1500);
  const [category, setCategory] = useState('OPEN');
  const [quota, setQuota] = useState('All');
  const [course, setCourse] = useState('MBBS');
  const [strategy, setStrategy] = useState('all');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (selectedInterest === 'Medicine' || selectedInterest === 'Dentistry') {
      handleSearch();
    }
  }, [selectedInterest]);

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!rank || rank <= 0) {
      alert('Please enter a valid NEET All India Rank (greater than 0).');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await searchNeetCutoffs({
        rank: Number(rank),
        category,
        quota,
        course,
        strategy,
        round: 1
      });
      setResults(data);
    } catch (err) {
      setError(err.message || 'Failed to search NEET cutoffs');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-10 animate-fadeIn">
      
      {/* Sub-Hero Header */}
      <div className="bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 rounded-3xl p-8 text-white shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
              <Stethoscope className="w-4 h-4" />
              <span>PCB Academic Track • Medical & Health Sciences Directory</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black tracking-tight">
              What are you interested in?
            </h1>
            <p className="text-sm text-emerald-200/90 max-w-2xl font-normal">
              Explore authentic NEET-UG MBBS/BDS cutoff ranks for AIIMS, Central Universities, and Government Medical Colleges, alongside structured career pathways for Pharmacy, Veterinary, Nursing, and Biotech.
            </p>
          </div>

          <div className="shrink-0 flex items-center gap-3">
            <div className="bg-white/10 backdrop-blur-md px-4 py-3 rounded-2xl border border-white/15 text-center">
              <span className="block text-2xl font-black text-emerald-400">100%</span>
              <span className="text-[11px] text-emerald-200 font-medium">MCC Verified</span>
            </div>
            <div className="bg-white/10 backdrop-blur-md px-4 py-3 rounded-2xl border border-white/15 text-center">
              <span className="block text-2xl font-black text-teal-300">AIQ</span>
              <span className="text-[11px] text-teal-200 font-medium">All India Quota</span>
            </div>
          </div>
        </div>

        {/* 10 Interest Options Pills */}
        <div className="mt-8 pt-6 border-t border-emerald-800/60">
          <span className="text-xs font-bold text-emerald-300 uppercase tracking-wider block mb-3">
            Select Your Area of Interest:
          </span>
          <div className="flex flex-wrap gap-2">
            {PCB_CAREER_INTERESTS.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  setSelectedInterest(item.id);
                  if (item.id === 'Dentistry') setCourse('BDS');
                  else if (item.id === 'Medicine') setCourse('MBBS');
                }}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center space-x-2 ${
                  selectedInterest === item.id
                    ? 'bg-emerald-400 text-slate-950 shadow-md shadow-emerald-400/20 scale-105'
                    : 'bg-emerald-950/60 text-emerald-200 hover:bg-emerald-800/60 border border-emerald-700/50'
                }`}
              >
                <span>{item.label}</span>
                {item.hasPredictor && (
                  <span className="px-1.5 py-0.5 text-[9px] rounded bg-emerald-900 text-emerald-200 font-mono">
                    Predictor
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* VIEW A: MEDICINE / DENTISTRY NEET PREDICTOR */}
      {(selectedInterest === 'Medicine' || selectedInterest === 'Dentistry') && (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
          
          <div className="flex items-center space-x-3 pb-6 border-b border-slate-100">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-black">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl sm:text-2xl font-black text-slate-900">
                NEET-UG Medical College Predictor (2024)
              </h2>
              <p className="text-xs text-slate-500 font-medium mt-0.5">
                Authentic Medical Counselling Committee (MCC) All India Quota (15%) Seat Allotments.
              </p>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSearch} className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            
            {/* NEET Rank Input */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                NEET All India Rank (AIR)
              </label>
              <input
                type="number"
                value={rank}
                onChange={(e) => setRank(e.target.value)}
                placeholder="e.g. 1500"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 font-bold text-sm text-slate-900"
                required
              />
            </div>

            {/* Course */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Course
              </label>
              <select
                value={course}
                onChange={(e) => setCourse(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 font-bold text-sm text-slate-900 bg-white"
              >
                <option value="MBBS">MBBS (Medicine & Surgery)</option>
                <option value="BDS">BDS (Dental Surgery)</option>
                <option value="All">All Medical Courses</option>
              </select>
            </div>

            {/* Category */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 font-bold text-sm text-slate-900 bg-white"
              >
                <option value="OPEN">OPEN / General</option>
                <option value="OBC">OBC-NCL</option>
                <option value="EWS">EWS</option>
                <option value="SC">SC</option>
                <option value="ST">ST</option>
              </select>
            </div>

            {/* Quota */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Quota
              </label>
              <select
                value={quota}
                onChange={(e) => setQuota(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-emerald-500 font-bold text-sm text-slate-900 bg-white"
              >
                <option value="All">All Quotas (AIQ, Deemed & State)</option>
                <option value="All India">All India Quota (AIQ 15%)</option>
                <option value="State Quota">State Quota (85%)</option>
              </select>
            </div>

            {/* Strategy & Search Button */}
            <div className="flex flex-col justify-end">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-sm shadow-md shadow-emerald-600/20 transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                {loading ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>Predict Colleges</span>
                  </>
                )}
              </button>
            </div>

          </form>

          {/* Results Display */}
          {results && (
            <div className="mt-8 pt-6 border-t border-slate-100">
              
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 gap-3">
                <div>
                  <h3 className="text-xl font-black text-slate-900">
                    {results.pagination.total_colleges_count} Medical & Dental Colleges Found
                  </h3>
                  <p className="text-xs text-slate-500 font-medium">
                    Showing {results.pagination.total_count} matching seat allotments for NEET AIR {Number(rank).toLocaleString()} ({category})
                  </p>
                </div>
                <div className="text-xs bg-emerald-50 text-emerald-800 px-3 py-1.5 rounded-xl border border-emerald-200 font-bold">
                  {results.search_parameters.disclaimer}
                </div>
              </div>

              {results.results.length === 0 ? (
                <div className="mt-6 p-8 rounded-2xl bg-amber-50/70 border border-amber-200 text-center space-y-3">
                  <AlertCircle className="w-8 h-8 text-amber-600 mx-auto" />
                  <h4 className="text-base font-bold text-amber-900">No Cutoffs Found for this Exact Query</h4>
                  <p className="text-xs text-amber-700 max-w-lg mx-auto leading-relaxed">
                    At NEET AIR {Number(rank).toLocaleString()} with Category <strong>{category}</strong> and Course <strong>{course}</strong>, government AIQ MBBS cutoffs typically fill up before 25,000 AIR. Try choosing <strong>"All Medical Courses"</strong> (to view Government BDS Dental colleges up to 58,000+ AIR) or ensure Quota is set to <strong>"All Quotas"</strong>.
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-4">
                {results.results.map((item) => (
                  <div 
                    key={item.cutoff_id}
                    className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm hover:shadow-md hover:border-emerald-300 transition-all flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200">
                          {item.college.type}
                        </span>
                        {item.college.nirf_medical_rank && (
                          <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                            NIRF Medical #{item.college.nirf_medical_rank}
                          </span>
                        )}
                      </div>

                      <h4 className="text-base font-extrabold text-slate-900 leading-snug">
                        {item.college.name}
                      </h4>
                      <p className="text-xs text-slate-500 flex items-center space-x-1 mt-1 font-medium">
                        <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span>{item.college.city}, {item.college.state}</span>
                      </p>

                      {/* Course badge */}
                      <div className="mt-3 p-2.5 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between text-xs">
                        <span className="font-bold text-slate-800">{item.course.name}</span>
                        <span className="text-slate-500 font-mono text-[11px]">{item.course.duration_years} Years</span>
                      </div>

                      {/* Cutoff Stats */}
                      <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                        <div className="p-2 rounded-lg bg-emerald-50/50 border border-emerald-100">
                          <span className="text-[10px] text-emerald-800 block font-semibold">Opening Rank</span>
                          <span className="font-mono font-bold text-emerald-900">{item.cutoff.opening_rank.toLocaleString()}</span>
                        </div>
                        <div className="p-2 rounded-lg bg-emerald-50/50 border border-emerald-100">
                          <span className="text-[10px] text-emerald-800 block font-semibold">Closing Rank</span>
                          <span className="font-mono font-bold text-emerald-900">{item.cutoff.closing_rank.toLocaleString()}</span>
                        </div>
                      </div>

                      {/* Fees & Stipend info */}
                      <div className="mt-3 space-y-1 text-xs text-slate-600 font-medium">
                        {item.college.annual_tuition_fee_inr !== null && (
                          <div className="flex justify-between">
                            <span>Annual Tuition Fee:</span>
                            <span className="font-bold text-slate-900">
                              {item.college.annual_tuition_fee_inr === 0 
                                ? 'Fully Subsidized' 
                                : `₹${item.college.annual_tuition_fee_inr.toLocaleString()}/yr`}
                            </span>
                          </div>
                        )}
                        {item.placement?.monthly_internship_stipend_inr && (
                          <div className="flex justify-between text-emerald-700">
                            <span>Internship Stipend:</span>
                            <span className="font-bold">₹{item.placement.monthly_internship_stipend_inr.toLocaleString()}/mo</span>
                          </div>
                        )}
                        {item.placement?.junior_resident_starting_salary_pm && (
                          <div className="flex justify-between text-indigo-700">
                            <span>Junior Resident Pay:</span>
                            <span className="font-bold">₹{item.placement.junior_resident_starting_salary_pm.toLocaleString()}/mo</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Footer buttons */}
                    <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] ${
                        item.strategy.badge === 'safe' 
                          ? 'bg-emerald-100 text-emerald-800' 
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {item.strategy.label}
                      </span>

                      {item.college.official_website && (
                        <a 
                          href={item.college.official_website} 
                          target="_blank" 
                          rel="noreferrer"
                          className="text-emerald-700 hover:text-emerald-900 flex items-center space-x-1"
                        >
                          <span>Official Portal</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

          </div>
        )}

        </div>
      )}

      {/* VIEW B: OTHER PCB PATHWAYS (Pharmacy, Veterinary, Physiotherapy, Nursing, Biotech) */}
      {selectedInterest !== 'Medicine' && selectedInterest !== 'Dentistry' && (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
          
          <div className="flex items-center space-x-3 pb-6 border-b border-slate-100">
            <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center font-black">
              <Dna className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl sm:text-2xl font-black text-slate-900">
                {selectedInterest} Career & Admission Roadmap
              </h2>
              <p className="text-xs text-slate-500 font-medium mt-0.5">
                Comprehensive step-by-step pathway from 12th PCB to clinical licensure, specialization, and practice.
              </p>
            </div>
          </div>

          {PCB_ROADMAPS[selectedInterest] ? (
            <div className="mt-6 space-y-6">
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                  <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-1">
                    Primary Degree Qualification
                  </span>
                  <span className="text-sm font-extrabold text-slate-900">
                    {PCB_ROADMAPS[selectedInterest].degree}
                  </span>
                </div>
                <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200">
                  <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wider block mb-1">
                    Applicable Entrance Examinations
                  </span>
                  <span className="text-sm font-extrabold text-emerald-900">
                    {PCB_ROADMAPS[selectedInterest].entrance}
                  </span>
                </div>
              </div>

              {/* Step by step stages */}
              <div className="pt-4">
                <h3 className="text-base font-black text-slate-900 mb-4">
                  Stage-by-Stage Professional Pathway:
                </h3>
                <div className="space-y-4">
                  {PCB_ROADMAPS[selectedInterest].stages.map((st, idx) => (
                    <div key={idx} className="flex items-start space-x-4 p-4 rounded-2xl bg-slate-50/70 border border-slate-100">
                      <div className="w-7 h-7 rounded-full bg-emerald-600 text-white flex items-center justify-center text-xs font-black shrink-0 mt-0.5">
                        {idx + 1}
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-slate-900">{st.step}</h4>
                        <p className="text-xs text-slate-600 mt-0.5 font-normal leading-relaxed">{st.detail}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          ) : (
            <div className="py-12 text-center text-slate-500 text-xs">
              Detailed curriculum roadmap available in global Career Explorer.
            </div>
          )}

        </div>
      )}

    </div>
  );
}
