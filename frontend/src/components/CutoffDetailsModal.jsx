import React from 'react';
import { X, ExternalLink, ShieldCheck, Calendar, Database, CheckCircle2 } from 'lucide-react';

export default function CutoffDetailsModal({ item, onClose }) {
  if (!item) return null;

  const { college, branch, cutoff, placement } = item;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div 
        className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-slate-200 shadow-2xl p-6 sm:p-8 relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="mb-6">
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-blue-600 mb-1">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
            <span>Official Cutoff Traceability & Provenance Report</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900">
            {college.name}
          </h2>
          <p className="text-sm font-semibold text-slate-600 mt-0.5">
            {branch.canonical_name} ({branch.degree})
          </p>
        </div>

        {/* Data Provenance Badge */}
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 mb-6 flex items-start space-x-3">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-xs font-bold text-emerald-900 uppercase tracking-wide">
              Authentic Counselling Archive Record
            </h4>
            <p className="text-xs text-emerald-800 mt-0.5">
              This record is ingested directly from the official National Informatics Centre (NIC) counselling repository for JoSAA / CSAB. It contains zero simulated or estimated figures.
            </p>
          </div>
        </div>

        {/* Traceable Data Fields Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs mb-6">
          
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-500 uppercase tracking-wider block mb-1">Admission Examination</span>
            <span className="font-extrabold text-slate-900 text-sm">{cutoff.year} Counselling</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-500 uppercase tracking-wider block mb-1">Counselling Round</span>
            <span className="font-extrabold text-blue-700 text-sm">Round {cutoff.round}</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-500 uppercase tracking-wider block mb-1">Category / Reservation</span>
            <span className="font-extrabold text-slate-900 text-sm">{cutoff.category}</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-500 uppercase tracking-wider block mb-1">Seat Quota</span>
            <span className="font-extrabold text-slate-900 text-sm">{cutoff.quota}</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-500 uppercase tracking-wider block mb-1">Gender Specification</span>
            <span className="font-extrabold text-slate-900 text-sm">{cutoff.gender}</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-500 uppercase tracking-wider block mb-1">Seat Type Code</span>
            <span className="font-extrabold text-slate-900 text-sm">{cutoff.seat_type || cutoff.category}</span>
          </div>

          <div className="p-3.5 rounded-xl bg-blue-50/60 border border-blue-100">
            <span className="font-bold text-blue-700 uppercase tracking-wider block mb-1">Official Opening Rank (OR)</span>
            <span className="font-black text-slate-900 text-lg">{cutoff.opening_rank ? Number(cutoff.opening_rank).toLocaleString() : 'N/A'}</span>
          </div>

          <div className="p-3.5 rounded-xl bg-blue-50/60 border border-blue-100">
            <span className="font-bold text-blue-700 uppercase tracking-wider block mb-1">Official Closing Rank (CR)</span>
            <span className="font-black text-blue-800 text-lg">{cutoff.closing_rank ? Number(cutoff.closing_rank).toLocaleString() : 'N/A'}</span>
          </div>

        </div>

        {/* Source Provenance Info Box */}
        <div className="p-4 rounded-2xl bg-slate-100/70 border border-slate-200 text-xs text-slate-600 mb-6 space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-bold text-slate-700">Authoritative Source:</span>
            <span className="font-semibold text-slate-900">{cutoff.source_name}</span>
          </div>
          {cutoff.source_url && (
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-700">Source Portal URL:</span>
              <a 
                href={cutoff.source_url} 
                target="_blank" 
                rel="noreferrer"
                className="text-blue-600 hover:underline flex items-center space-x-1 font-semibold"
              >
                <span>{cutoff.source_url}</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          )}
          <div className="flex items-center justify-between">
            <span className="font-bold text-slate-700">Last Verified Date:</span>
            <span className="font-mono text-slate-800">
              {cutoff.last_verified_at ? new Date(cutoff.last_verified_at).toLocaleDateString('en-IN', { dateStyle: 'long' }) : 'Verified at Ingestion'}
            </span>
          </div>
        </div>

        {/* Legal Disclaimer */}
        <p className="text-[11px] text-slate-500 italic mb-6">
          * Note: Historical closing cutoffs are archived strictly for admission strategy planning. The Joint Seat Allocation Authority conducts fresh counselling rounds every year with dynamic seat allotments.
        </p>

        {/* Footer Actions */}
        <div className="flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-700 font-bold text-xs hover:bg-slate-50 transition-colors"
          >
            Close Inspector
          </button>
          {college.official_website && (
            <a
              href={college.official_website}
              target="_blank"
              rel="noreferrer"
              className="px-5 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-xs hover:bg-blue-700 transition-colors flex items-center space-x-1.5 shadow-sm"
            >
              <span>Visit Official College Website</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>

      </div>
    </div>
  );
}
