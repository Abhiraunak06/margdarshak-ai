import React from 'react';
import { 
  Building2, 
  MapPin, 
  ExternalLink, 
  TrendingUp, 
  Bookmark, 
  BookmarkCheck, 
  Eye, 
  LineChart, 
  CheckCircle, 
  HelpCircle, 
  ShieldCheck,
  Info
} from 'lucide-react';

export default function CollegeResultCard({ 
  item, 
  onViewCutoff, 
  onViewTrends, 
  isSaved, 
  onToggleSave 
}) {
  const { college = {}, branch = {}, cutoff = {}, placement = null, strategy = {} } = item || {};

  // Strategy badge styling
  const strategyStyles = {
    safe: 'bg-emerald-100 text-emerald-800 border-emerald-300',
    conservative: 'bg-emerald-100 text-emerald-800 border-emerald-300',
    match: 'bg-blue-100 text-blue-800 border-blue-300',
    ambitious: 'bg-amber-100 text-amber-900 border-amber-300'
  };

  const collegeTypeBadges = {
    IIT: 'bg-indigo-700 text-white',
    NIT: 'bg-blue-700 text-white',
    IIIT: 'bg-sky-600 text-white',
    GFTI: 'bg-teal-700 text-white',
    'State-Govt': 'bg-emerald-700 text-white',
    Private: 'bg-purple-700 text-white'
  };

  const formatRank = (val) => {
    if (val === null || val === undefined) return 'N/A';
    const num = Number(val);
    return isNaN(num) ? String(val) : num.toLocaleString();
  };

  const badgeClass = strategyStyles[strategy?.badge] || 'bg-blue-50 text-blue-800 border-blue-200';

  return (
    <div className="bg-white rounded-2xl border border-slate-200 hover:border-blue-400 hover:shadow-lg transition-all p-5 sm:p-6 relative flex flex-col justify-between group">
      
      {/* Top Meta Bar */}
      <div>
        <div className="flex items-start justify-between gap-3 mb-2">
          
          <div className="flex flex-wrap items-center gap-1.5">
            <span className={`px-2.5 py-0.5 rounded-md text-[11px] font-extrabold uppercase tracking-wide ${collegeTypeBadges[college.type] || 'bg-slate-700 text-white'}`}>
              {college.type || 'College'}
            </span>

            {college.nirf_rank && (
              <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-amber-50 text-amber-800 border border-amber-200">
                NIRF #{college.nirf_rank}
              </span>
            )}

            <span className={`px-2 py-0.5 rounded-md text-[11px] font-bold border ${badgeClass}`}>
              {strategy?.label || 'Eligible'}
            </span>
          </div>

          {/* Bookmark Button */}
          <button
            onClick={() => onToggleSave && onToggleSave(college)}
            className={`p-2 rounded-xl transition-all ${
              isSaved
                ? 'bg-blue-50 text-blue-600 border border-blue-200'
                : 'bg-slate-50 text-slate-400 hover:text-slate-600 border border-slate-100'
            }`}
            title={isSaved ? "Saved for Comparison" : "Save / Bookmark"}
          >
            {isSaved ? (
              <BookmarkCheck className="w-5 h-5 fill-blue-600 text-blue-600" />
            ) : (
              <Bookmark className="w-5 h-5" />
            )}
          </button>
        </div>

        {/* College Name & Location */}
        <h3 className="text-lg sm:text-xl font-bold text-slate-900 leading-snug group-hover:text-blue-600 transition-colors">
          {college.name}
        </h3>

        <div className="flex items-center space-x-2 text-xs text-slate-500 mt-1 mb-4">
          <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <span>{college.city ? `${college.city}, ` : ''}{college.state}</span>
          {college.established_year && (
            <>
              <span>•</span>
              <span>Est. {college.established_year}</span>
            </>
          )}
        </div>

        {/* Branch Title & Discipline */}
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100 mb-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
              {branch.degree || 'Degree'} ({branch.duration_years || 4} Years)
            </span>
            <span className="text-[11px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
              {branch.discipline || 'Engineering'}
            </span>
          </div>
          <p className="text-base font-bold text-slate-900 mt-0.5">
            {branch.canonical_name}
          </p>
        </div>

        {/* Cutoff Rank Metrics Box */}
        <div className="grid grid-cols-2 gap-3 p-3.5 rounded-xl bg-blue-50/40 border border-blue-100 mb-4">
          <div>
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
              Opening Rank (OR)
            </span>
            <span className="text-lg font-black text-slate-800">
              {formatRank(cutoff.opening_rank)}
            </span>
          </div>
          <div>
            <span className="text-[11px] font-bold text-blue-700 uppercase tracking-wider block">
              Closing Rank (CR)
            </span>
            <span className="text-lg font-black text-blue-700">
              {formatRank(cutoff.closing_rank)}
            </span>
          </div>
          <div className="col-span-2 pt-2 border-t border-blue-100 flex flex-wrap items-center justify-between text-[11px] text-slate-600 gap-y-1">
            <span><strong>Round:</strong> {cutoff.round || 1} ({cutoff.year || 2024})</span>
            <span><strong>Category:</strong> {cutoff.category || 'OPEN'}</span>
            <span><strong>Quota:</strong> {cutoff.quota || 'All'}</span>
            <span><strong>Type:</strong> {cutoff.rank_type === 'CATEGORY_RANK' ? 'Category Rank' : cutoff.rank_type === 'MERIT_RANK' ? 'Merit Rank' : 'CRL AIR'}</span>
          </div>
        </div>

        {/* Placement Statistics Box */}
        {placement ? (
          <div className="p-3.5 rounded-xl bg-emerald-50/40 border border-emerald-100 mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-emerald-900 flex items-center space-x-1">
                <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
                <span>Verified Placement Statistics</span>
              </span>
              <span className="text-[10px] font-semibold text-slate-500">
                {placement.source_name}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-center">
              <div className="bg-white p-2 rounded-lg border border-emerald-100">
                <span className="text-[10px] text-slate-500 font-semibold block">Median CTC</span>
                <span className="text-sm font-black text-emerald-800">
                  {placement.median_package_lpa ? `₹${placement.median_package_lpa} LPA` : 'N/A'}
                </span>
              </div>
              <div className="bg-white p-2 rounded-lg border border-emerald-100">
                <span className="text-[10px] text-slate-500 font-semibold block">Average CTC</span>
                <span className="text-sm font-black text-emerald-800">
                  {placement.average_package_lpa ? `₹${placement.average_package_lpa} LPA` : 'N/A'}
                </span>
              </div>
              <div className="bg-white p-2 rounded-lg border border-emerald-100">
                <span className="text-[10px] text-slate-500 font-semibold block">Placed %</span>
                <span className="text-sm font-black text-emerald-800">
                  {placement.placement_percentage ? `${placement.placement_percentage}%` : 'N/A'}
                </span>
              </div>
            </div>

            {placement.label && (
              <p className="text-[10px] text-slate-500 mt-2 italic flex items-center space-x-1">
                <Info className="w-3 h-3 text-slate-400 shrink-0" />
                <span>{placement.label}</span>
              </p>
            )}
          </div>
        ) : (
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-500 mb-4 italic">
            Institutional placement disclosure unavailable from official NIRF database for this college.
          </div>
        )}
      </div>

      {/* Action Footer Buttons */}
      <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs font-bold">
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => onViewCutoff && onViewCutoff(item)}
            className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors flex items-center space-x-1"
          >
            <Eye className="w-3.5 h-3.5 text-slate-500" />
            <span>Traceability</span>
          </button>

          <button
            onClick={() => onViewTrends && onViewTrends(item)}
            className="px-3 py-1.5 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 transition-colors flex items-center space-x-1"
          >
            <LineChart className="w-3.5 h-3.5 text-blue-600" />
            <span>Cutoff Trend</span>
          </button>
        </div>

        {college.official_website && (
          <a
            href={college.official_website}
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white transition-colors flex items-center space-x-1 shadow-sm"
          >
            <span>Official Website</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        )}

      </div>

    </div>
  );
}
