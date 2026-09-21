import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  Send, 
  Compass, 
  CheckCircle2, 
  BookOpen, 
  Award, 
  AlertCircle,
  Lightbulb,
  ArrowRight,
  GraduationCap
} from 'lucide-react';
import { generatePersonalizedRoadmap } from '../services/api';

const STREAM_CONFIGS = {
  PCM: {
    exams: ['JEE Main', 'JEE Advanced', 'WBJEE', 'BITSAT', 'COMEDK'],
    defaultBranch: 'Computer Science and Engineering',
    interests: [
      'Software Development',
      'Artificial Intelligence & ML',
      'VLSI & Semiconductor Design',
      'Robotics & Autonomous Systems',
      'Core Engineering & EV',
      'Cybersecurity',
      'Scientific Research & Higher Studies',
      'Tech Entrepreneurship'
    ],
    defaultGoal: 'Product Software Engineer / Systems Architect'
  },
  PCB: {
    exams: ['NEET-UG', 'State Medical Counselling', 'AIIMS Nursing'],
    defaultBranch: 'MBBS (Bachelor of Medicine & Surgery)',
    interests: [
      'Clinical Medicine & Surgery',
      'Dental Surgery & Orthodontics',
      'Pharmacology & Drug Discovery',
      'Cardiology & Critical Care',
      'Clinical Psychology & Psychiatry',
      'Genomics & Biotechnology Research'
    ],
    defaultGoal: 'Specialist Physician / Post-Graduate MD/MS'
  },
  COMMERCE: {
    exams: ['CUET-UG', 'IPMAT', 'CA Foundation', 'CSEET'],
    defaultBranch: 'B.Com (Hons) / BMS / Finance',
    interests: [
      'Chartered Accountancy & Statutory Audit',
      'Investment Banking, M&A & CFA',
      'Company Secretary & Corporate Governance',
      'Cost & Management Accounting (CMA)',
      'Fintech & Business Analytics',
      'Central Banking (RBI Grade B / SBI PO)'
    ],
    defaultGoal: 'Chartered Accountant / Investment Banking Associate'
  },
  ARTS: {
    exams: ['CLAT (NLUs)', 'UPSC Civil Services', 'CUET-UG', 'UGC-NET'],
    defaultBranch: 'B.A. LL.B. (Hons) / B.A. Economics / Political Science',
    interests: [
      'Corporate Law & Commercial Litigation',
      'Civil Services & Public Administration (IAS/IPS)',
      'Clinical Psychology & Mental Health',
      'Public Policy, NITI Aayog & Economics',
      'Investigative Journalism & Digital Media',
      'University Academia & Research (UGC-NET)'
    ],
    defaultGoal: 'Tier-1 Law Firm Associate / Civil Servant'
  }
};

export default function PersonalizedRoadmap({ initialCareer }) {
  const [stream, setStream] = useState(initialCareer?.stream || 'PCM');
  const [exam, setExam] = useState(STREAM_CONFIGS[stream].exams[0]);
  const [rank, setRank] = useState(4000);
  const [branch, setBranch] = useState(STREAM_CONFIGS[stream].defaultBranch);
  const [interest, setInterest] = useState(initialCareer ? initialCareer.title : STREAM_CONFIGS[stream].interests[0]);
  const [careerGoal, setCareerGoal] = useState(STREAM_CONFIGS[stream].defaultGoal);
  const [loading, setLoading] = useState(false);
  const [roadmapResult, setRoadmapResult] = useState(null);

  // Sync defaults when stream changes
  const handleStreamChange = (newStream) => {
    setStream(newStream);
    const cfg = STREAM_CONFIGS[newStream];
    setExam(cfg.exams[0]);
    setBranch(cfg.defaultBranch);
    setInterest(cfg.interests[0]);
    setCareerGoal(cfg.defaultGoal);
    setRank(newStream === 'PCM' ? 4000 : newStream === 'PCB' ? 1500 : newStream === 'COMMERCE' ? 780 : 450);
  };

  useEffect(() => {
    if (initialCareer) {
      if (initialCareer.stream) handleStreamChange(initialCareer.stream);
      setInterest(initialCareer.title);
    }
  }, [initialCareer]);

  const handleGenerate = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    try {
      const data = await generatePersonalizedRoadmap({
        stream,
        exam,
        rank: Number(rank),
        branch,
        interest,
        career_goal: careerGoal
      });
      setRoadmapResult(data);
    } catch (err) {
      alert('Error generating personalized roadmap: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const currentCfg = STREAM_CONFIGS[stream];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-900 border border-amber-200 mb-3">
          <Sparkles className="w-4 h-4 text-amber-600" />
          <span>Multi-Stream Student Success Engine</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
          Generate Your Personalized Career Roadmap
        </h1>
        <p className="text-slate-600 text-sm mt-2">
          Tailored milestones aligning your academic stream, entrance exam rank/score, target course, and professional aspirations.
        </p>
      </div>

      {/* Stream Selector Bar */}
      <div className="flex flex-wrap items-center justify-center gap-2 mb-6">
        {Object.keys(STREAM_CONFIGS).map((st) => (
          <button
            key={st}
            onClick={() => handleStreamChange(st)}
            className={`px-5 py-2 rounded-xl text-xs font-black transition-all ${
              stream === st
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20 ring-2 ring-blue-500/30'
                : 'bg-white text-slate-700 border border-slate-200 hover:border-blue-400'
            }`}
          >
            {st === 'PCM' ? 'PCM (Engineering)' :
             st === 'PCB' ? 'PCB (Medical / Biology)' :
             st === 'COMMERCE' ? 'Commerce & Finance' :
             'Arts & Humanities'}
          </button>
        ))}
      </div>

      {/* Input Configuration Card */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-xl shadow-slate-200/50 p-6 sm:p-8 mb-10">
        <form onSubmit={handleGenerate} className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            
            {/* Exam */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                Entrance Exam
              </label>
              <select
                value={exam}
                onChange={(e) => setExam(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900 bg-white"
              >
                {currentCfg.exams.map((ex) => (
                  <option key={ex} value={ex}>{ex}</option>
                ))}
              </select>
            </div>

            {/* Rank / Score */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                {stream === 'COMMERCE' ? 'Score / Rank' : 'Exam Rank (AIR)'}
              </label>
              <input
                type="number"
                min="1"
                required
                value={rank}
                onChange={(e) => setRank(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900"
                placeholder={stream === 'COMMERCE' ? 'e.g. 780' : 'e.g. 4000'}
              />
            </div>

            {/* Branch / Course */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                Degree Program / Branch
              </label>
              <input
                type="text"
                required
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900"
                placeholder={currentCfg.defaultBranch}
              />
            </div>

            {/* Career Interest */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                Primary Career Interest
              </label>
              <select
                value={interest}
                onChange={(e) => setInterest(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900 bg-white"
              >
                {currentCfg.interests.map((int) => (
                  <option key={int} value={int}>{int}</option>
                ))}
              </select>
            </div>

            {/* Career Goal */}
            <div className="sm:col-span-2">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                Target Role / Industry Goal
              </label>
              <input
                type="text"
                required
                value={careerGoal}
                onChange={(e) => setCareerGoal(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900"
                placeholder="e.g. Senior Strategist / Technical Specialist"
              />
            </div>

          </div>

          <div className="pt-2 flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm flex items-center space-x-2 shadow-lg shadow-blue-500/25 transition-all disabled:opacity-50"
            >
              <Sparkles className="w-4 h-4 text-amber-300" />
              <span>{loading ? 'Synthesizing Roadmap...' : 'Generate Stream Roadmap'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Generated Roadmap Result */}
      {roadmapResult && (
        <div className="bg-white rounded-3xl border border-slate-200 shadow-xl shadow-slate-200/50 p-6 sm:p-10 space-y-8 animate-fadeIn">
          
          {/* Header & Rationale */}
          <div className="border-b border-slate-100 pb-6">
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">
                {roadmapResult.stream} Stream Strategy
              </span>
              <span className="text-xs font-bold text-slate-500">
                Generated: {new Date(roadmapResult.generated_at).toLocaleDateString()}
              </span>
            </div>

            <h2 className="text-2xl sm:text-3xl font-black text-slate-900 mt-1">
              Your Customized Milestone Roadmap
            </h2>

            <p className="mt-3 text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-2xl border border-slate-100 font-normal">
              {roadmapResult.personalized_rationale}
            </p>
          </div>

          {/* Phase-by-Phase Roadmap Timeline */}
          <div className="space-y-6">
            <h3 className="text-lg font-black text-slate-900 flex items-center space-x-2">
              <Compass className="w-5 h-5 text-blue-600" />
              <span>Execution Timeline & Core Milestones</span>
            </h3>

            <div className="space-y-6">
              {roadmapResult.phases?.map((phase, idx) => (
                <div 
                  key={idx}
                  className="relative pl-8 sm:pl-10 before:content-[''] before:absolute before:left-3 sm:before:left-4 before:top-3 before:bottom-0 before:w-0.5 before:bg-blue-100 last:before:hidden"
                >
                  <div className="absolute left-0 top-1 w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-blue-600 text-white font-black text-xs flex items-center justify-center shadow-md shadow-blue-500/30">
                    {idx + 1}
                  </div>

                  <div className="p-5 sm:p-6 rounded-2xl bg-slate-50/80 border border-slate-200/80 hover:border-blue-300 transition-all space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-200/60 pb-3">
                      <h4 className="text-base font-black text-slate-900">
                        {phase.phase}
                      </h4>
                      <span className="text-xs font-bold text-blue-700">
                        Focus: {phase.academic_focus}
                      </span>
                    </div>

                    {/* Core Skills */}
                    <div>
                      <span className="text-[11px] font-extrabold uppercase tracking-wider text-slate-500 block mb-1.5">
                        Key Competencies to Master:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {phase.core_skills?.map((sk, sidx) => (
                          <span key={sidx} className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-white text-slate-800 border border-slate-200 shadow-2xs">
                            {sk}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Milestone Projects & Deliverables */}
                    <div>
                      <span className="text-[11px] font-extrabold uppercase tracking-wider text-slate-500 block mb-1.5">
                        Mandatory Practical Deliverables:
                      </span>
                      <ul className="space-y-1 text-xs text-slate-700 list-disc list-inside">
                        {phase.milestone_projects?.map((proj, pidx) => (
                          <li key={pidx} className="font-medium">{proj}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Recommended Certification */}
                    {phase.certifications_recommendation && (
                      <div className="p-3 rounded-xl bg-amber-50/80 border border-amber-200 text-xs text-amber-900 flex items-start space-x-2">
                        <Award className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                        <div>
                          <strong>Key Benchmark / Licensure:</strong> {phase.certifications_recommendation}
                        </div>
                      </div>
                    )}

                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Strategic Recommendations */}
          {roadmapResult.strategic_recommendations?.length > 0 && (
            <div className="pt-4 border-t border-slate-100">
              <h3 className="text-base font-black text-slate-900 mb-3 flex items-center space-x-2">
                <Lightbulb className="w-5 h-5 text-amber-500" />
                <span>Expert Strategic Advice</span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {roadmapResult.strategic_recommendations.map((rec, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 flex items-start space-x-2 font-normal">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>
      )}

    </div>
  );
}
