import React from 'react';
import { Award, BookOpen, MapPin, Building2, CheckCircle2, Sparkles } from 'lucide-react';

export default function ExamSelector({ exams = [], selectedExam, onSelectExam, loading }) {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-sm text-slate-600 font-medium">Loading Examination Database...</span>
      </div>
    );
  }

  // Partition by level
  const nationalExams = exams.filter(e => e.level === 'National');
  const stateExams = exams.filter(e => e.level === 'State');
  const otherExams = exams.filter(e => e.level !== 'National' && e.level !== 'State');

  const formatCutoffsCount = (num) => {
    if (!num) return 'Authentic';
    return Number(num).toLocaleString();
  };

  return (
    <div className="mb-10">
      <div className="text-center max-w-2xl mx-auto mb-6">
        <span className="text-xs font-bold uppercase tracking-widest text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">
          Step 2 of 3
        </span>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">
          Select Engineering Entrance Examination
        </h2>
        <p className="text-slate-600 text-sm mt-1">
          Dynamic examination registry. Form fields, seat quotas, and counseling datasets adapt automatically.
        </p>
      </div>

      {/* 1. National Examinations */}
      <div className="mb-6">
        <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
          <Award className="w-4 h-4 text-blue-600" />
          <span>National Level Examinations (JoSAA / CSAB)</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {nationalExams.map((exam) => {
            const isSelected = selectedExam?.code === exam.code;
            return (
              <div
                key={exam.code}
                onClick={() => onSelectExam(exam)}
                className={`p-5 rounded-2xl border-2 transition-all cursor-pointer relative bg-white ${
                  isSelected
                    ? 'border-blue-600 shadow-md shadow-blue-500/10 ring-2 ring-blue-500/20'
                    : 'border-slate-200 hover:border-blue-300 hover:shadow-sm'
                }`}
              >
                {isSelected && (
                  <div className="absolute top-4 right-4 text-blue-600">
                    <CheckCircle2 className="w-5 h-5 fill-blue-600 text-white" />
                  </div>
                )}
                <div className="flex items-center space-x-2 mb-2">
                  <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-800 text-xs font-bold">
                    {exam.code === 'JEE_MAIN' ? 'NITs / IIITs / GFTIs' : 'IITs Only'}
                  </span>
                  <span className="text-xs text-slate-500 font-medium">Rank Based</span>
                </div>
                <h3 className="text-lg font-bold text-slate-900">{exam.name}</h3>
                <p className="text-xs text-slate-500 mt-1 line-clamp-2">
                  {exam.description}
                </p>
                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-600">
                  <span className="font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                    {formatCutoffsCount(exam.total_cutoffs)} Authentic Cutoffs
                  </span>
                  <span className="text-slate-400">Rounds 1 - 5</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 2. State Examinations */}
      {stateExams.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
            <MapPin className="w-4 h-4 text-indigo-600" />
            <span>State Level Counselling & Examinations</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {stateExams.map((exam) => {
              const isSelected = selectedExam?.code === exam.code;
              const stateBadge = exam.code === 'WBJEE' ? 'West Bengal State' : 'Karnataka State';
              const authorityBadge = exam.code === 'WBJEE' ? 'WBJEEB Official Data' : 'COMEDK Official Data';
              return (
                <div
                  key={exam.code}
                  onClick={() => onSelectExam(exam)}
                  className={`p-5 rounded-2xl border-2 transition-all cursor-pointer relative bg-white ${
                    isSelected
                      ? 'border-blue-600 shadow-md shadow-blue-500/10 ring-2 ring-blue-500/20'
                      : 'border-slate-200 hover:border-blue-300 hover:shadow-sm'
                  }`}
                >
                  {isSelected && (
                    <div className="absolute top-4 right-4 text-blue-600">
                      <CheckCircle2 className="w-5 h-5 fill-blue-600 text-white" />
                    </div>
                  )}
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="px-2 py-0.5 rounded bg-indigo-100 text-indigo-800 text-xs font-bold">
                      {stateBadge}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">Rank Based</span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900">{exam.name}</h3>
                  <p className="text-xs text-slate-500 mt-1 line-clamp-2">
                    {exam.description}
                  </p>
                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-600">
                    <span className="font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                      {authorityBadge}
                    </span>
                    <span className="text-slate-400">{formatCutoffsCount(exam.total_cutoffs)} Cutoffs</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 3. University / Deemed Examinations (BITSAT & VITEEE) */}
      {otherExams.length > 0 && (
        <div>
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
            <Building2 className="w-4 h-4 text-purple-600" />
            <span>Premier Institute / University Examinations</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {otherExams.map((exam) => {
              const isSelected = selectedExam?.code === exam.code;
              const isScore = exam.scoring_type === 'Score' || exam.code === 'BITSAT';
              return (
                <div
                  key={exam.code}
                  onClick={() => onSelectExam(exam)}
                  className={`p-5 rounded-2xl border-2 transition-all cursor-pointer relative bg-white ${
                    isSelected
                      ? 'border-blue-600 shadow-md shadow-blue-500/10 ring-2 ring-blue-500/20'
                      : 'border-slate-200 hover:border-blue-300 hover:shadow-sm'
                  }`}
                >
                  {isSelected && (
                    <div className="absolute top-4 right-4 text-blue-600">
                      <CheckCircle2 className="w-5 h-5 fill-blue-600 text-white" />
                    </div>
                  )}
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="px-2 py-0.5 rounded bg-purple-100 text-purple-800 text-xs font-bold">
                      {exam.code === 'BITSAT' ? 'BITS Pilani / Goa / Hyd' : 'VIT Campuses'}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">
                      {isScore ? 'Score Based (/390)' : 'Rank Based'}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900">{exam.name}</h3>
                  <p className="text-xs text-slate-500 mt-1 line-clamp-2">
                    {exam.description}
                  </p>
                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-600">
                    <span className="font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                      {isScore ? 'Score Cutoffs' : 'Rank Cutoffs'}
                    </span>
                    <span className="text-slate-400">{formatCutoffsCount(exam.total_cutoffs)} Cutoffs</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

    </div>
  );
}
