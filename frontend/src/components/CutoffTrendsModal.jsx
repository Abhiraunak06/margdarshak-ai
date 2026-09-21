import React, { useState, useEffect } from 'react';
import { X, LineChart, TrendingUp, AlertCircle } from 'lucide-react';
import { fetchCutoffTrends } from '../services/api';

export default function CutoffTrendsModal({ item, onClose }) {
  if (!item) return null;

  const { college, branch, cutoff } = item;
  const [trendData, setTrendData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    fetchCutoffTrends(college.id, branch.id, cutoff.category, cutoff.quota)
      .then(res => {
        if (isMounted) {
          setTrendData(res.trends || []);
          setLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) setLoading(false);
      });
    return () => { isMounted = false; };
  }, [college.id, branch.id, cutoff.category, cutoff.quota]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div 
        className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-slate-200 shadow-2xl p-6 sm:p-8 relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="mb-6">
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-blue-600 mb-1">
            <LineChart className="w-4 h-4 text-blue-600" />
            <span>Historical Counselling Round Trend</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900">
            {college.name}
          </h2>
          <p className="text-sm font-semibold text-slate-600 mt-0.5">
            {branch.canonical_name} • Category: {cutoff.category} • Quota: {cutoff.quota}
          </p>
        </div>

        {loading ? (
          <div className="py-12 flex justify-center items-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-xs text-slate-600 font-semibold">Loading round cutoffs...</span>
          </div>
        ) : trendData.length > 0 ? (
          <div>
            {/* Visual Round Table */}
            <div className="overflow-x-auto rounded-2xl border border-slate-200 mb-6">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-slate-700 font-bold uppercase tracking-wider text-[11px]">
                    <th className="py-3 px-4">Counselling Stage</th>
                    <th className="py-3 px-4">Opening Rank</th>
                    <th className="py-3 px-4">Closing Rank</th>
                    <th className="py-3 px-4 text-right">Movement</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-slate-700">
                  {trendData.map((t, idx) => {
                    const prev = idx > 0 ? trendData[idx - 1] : null;
                    const diff = prev ? t.closing_rank - prev.closing_rank : 0;

                    return (
                      <tr key={idx} className="hover:bg-blue-50/40 transition-colors">
                        <td className="py-3 px-4 font-bold text-slate-900">
                          {t.round} ({t.year})
                        </td>
                        <td className="py-3 px-4 font-mono font-semibold text-slate-600">
                          {t.opening_rank.toLocaleString()}
                        </td>
                        <td className="py-3 px-4 font-mono font-bold text-blue-700">
                          {t.closing_rank.toLocaleString()}
                        </td>
                        <td className="py-3 px-4 text-right font-semibold">
                          {diff > 0 ? (
                            <span className="text-emerald-600">+{diff.toLocaleString()} (Relaxed)</span>
                          ) : diff < 0 ? (
                            <span className="text-rose-600">{diff.toLocaleString()}</span>
                          ) : (
                            <span className="text-slate-400">—</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            <div className="p-4 rounded-xl bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-start space-x-2">
              <AlertCircle className="w-4 h-4 shrink-0 text-blue-600 mt-0.5" />
              <span>
                <strong>How to interpret rounds:</strong> As counselling progresses from Round 1 through Round 5, closing ranks typically expand as candidates upgrade their seat preferences or withdraw.
              </span>
            </div>
          </div>
        ) : (
          <div className="py-8 text-center text-slate-500 text-xs">
            No additional round progressions recorded for this specific category and branch tuple.
          </div>
        )}

        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-slate-900 text-white font-bold text-xs hover:bg-slate-800 transition-colors"
          >
            Close Trends
          </button>
        </div>
      </div>
    </div>
  );
}
