import React from 'react';
import { X, Trash2, ExternalLink, Scale, Check, Minus } from 'lucide-react';

export default function ComparisonDrawer({ 
  isOpen, 
  onClose, 
  savedColleges, 
  onRemove, 
  onClearAll 
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div 
        className="bg-white rounded-3xl max-w-5xl w-full max-h-[90vh] overflow-y-auto border border-slate-200 shadow-2xl p-6 sm:p-8 relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-4 mb-6 border-b border-slate-100">
          <div className="flex items-center space-x-2">
            <div className="p-2 rounded-xl bg-blue-50 text-blue-600">
              <Scale className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl sm:text-2xl font-black text-slate-900">
                Compare Saved Colleges
              </h2>
              <p className="text-xs text-slate-500 font-medium">
                Side-by-side comparison of institutional rank, location, NIRF verified placement stats, and official portals.
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            {savedColleges.length > 0 && (
              <button
                onClick={onClearAll}
                className="px-3 py-1.5 rounded-lg text-xs font-bold text-rose-600 hover:bg-rose-50 border border-rose-200 transition-colors flex items-center space-x-1"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Clear All</span>
              </button>
            )}
            <button
              onClick={onClose}
              className="p-2 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {savedColleges.length === 0 ? (
          <div className="py-16 text-center text-slate-500">
            <Scale className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-700">No Colleges Saved Yet</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
              Click the bookmark icon on any college result card to add colleges to this comparison matrix.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse min-w-[650px]">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="py-3 px-4 w-40 font-bold text-slate-400 uppercase tracking-wider bg-slate-50">
                    Feature / Metric
                  </th>
                  {savedColleges.map((col) => (
                    <th key={col.id} className="py-3 px-4 font-bold text-slate-900 bg-blue-50/30 border-l border-slate-100 min-w-[200px]">
                      <div className="flex items-start justify-between">
                        <span className="text-sm font-black text-slate-900 line-clamp-2">
                          {col.short_name || col.name}
                        </span>
                        <button
                          onClick={() => onRemove(col.id)}
                          className="text-slate-400 hover:text-rose-600 p-1"
                          title="Remove"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                      <span className="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-extrabold bg-blue-100 text-blue-800 uppercase">
                        {col.type}
                      </span>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                
                {/* Location */}
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-600 bg-slate-50">Location</td>
                  {savedColleges.map((col) => (
                    <td key={col.id} className="py-3 px-4 font-medium border-l border-slate-100">
                      {col.city ? `${col.city}, ` : ''}{col.state}
                    </td>
                  ))}
                </tr>

                {/* Established Year */}
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-600 bg-slate-50">Established</td>
                  {savedColleges.map((col) => (
                    <td key={col.id} className="py-3 px-4 font-medium border-l border-slate-100">
                      {col.established_year ? `Est. ${col.established_year}` : 'N/A'}
                    </td>
                  ))}
                </tr>

                {/* NIRF Rank */}
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-600 bg-slate-50">NIRF Engineering Rank</td>
                  {savedColleges.map((col) => (
                    <td key={col.id} className="py-3 px-4 font-black text-amber-700 border-l border-slate-100 text-sm">
                      {col.nirf_rank ? `#${col.nirf_rank}` : 'Unranked'}
                    </td>
                  ))}
                </tr>

                {/* Median Package */}
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-600 bg-slate-50">Median CTC (LPA)</td>
                  {savedColleges.map((col) => {
                    const lpa = col.placement?.median_package_lpa;
                    return (
                      <td key={col.id} className="py-3 px-4 font-black text-emerald-800 text-sm border-l border-slate-100">
                        {lpa ? `₹${lpa} LPA` : 'Unavailable'}
                      </td>
                    );
                  })}
                </tr>

                {/* Average Package */}
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-600 bg-slate-50">Average CTC (LPA)</td>
                  {savedColleges.map((col) => {
                    const lpa = col.placement?.average_package_lpa;
                    return (
                      <td key={col.id} className="py-3 px-4 font-bold text-slate-800 border-l border-slate-100">
                        {lpa ? `₹${lpa} LPA` : 'Unavailable'}
                      </td>
                    );
                  })}
                </tr>

                {/* Placement Rate */}
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-600 bg-slate-50">Placement Rate</td>
                  {savedColleges.map((col) => {
                    const pct = col.placement?.placement_percentage;
                    return (
                      <td key={col.id} className="py-3 px-4 font-bold text-slate-800 border-l border-slate-100">
                        {pct ? `${pct}%` : 'Unavailable'}
                      </td>
                    );
                  })}
                </tr>

                {/* Official Website */}
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-600 bg-slate-50">Official Website</td>
                  {savedColleges.map((col) => (
                    <td key={col.id} className="py-3 px-4 border-l border-slate-100">
                      {col.official_website ? (
                        <a
                          href={col.official_website}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 hover:underline font-bold flex items-center space-x-1"
                        >
                          <span>Visit Website</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      ) : (
                        <span className="text-slate-400">Unavailable</span>
                      )}
                    </td>
                  ))}
                </tr>

              </tbody>
            </table>
          </div>
        )}

        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-slate-900 text-white font-bold text-xs hover:bg-slate-800 transition-colors"
          >
            Done
          </button>
        </div>

      </div>
    </div>
  );
}
