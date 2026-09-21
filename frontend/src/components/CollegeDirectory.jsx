import React, { useState, useEffect } from 'react';
import { 
  Building2, 
  MapPin, 
  Search, 
  ExternalLink, 
  TrendingUp, 
  Filter, 
  GraduationCap, 
  ChevronLeft, 
  ChevronRight,
  Info
} from 'lucide-react';
import { fetchColleges, fetchCollegeDetails } from '../services/api';

export default function CollegeDirectory({ onSaveCollege, isSavedMap }) {
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('All');
  const [stateFilter, setStateFilter] = useState('All');
  const [selectedCollegeModal, setSelectedCollegeModal] = useState(null);
  const [modalLoading, setModalLoading] = useState(false);

  const loadColleges = () => {
    setLoading(true);
    fetchColleges({
      q: searchQuery,
      type: typeFilter,
      state: stateFilter,
      page,
      limit: 15
    })
      .then(res => {
        setColleges(res.colleges);
        setTotal(res.total);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    loadColleges();
  }, [page, typeFilter, stateFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    loadColleges();
  };

  const openCollegeModal = async (colId) => {
    setModalLoading(true);
    try {
      const details = await fetchCollegeDetails(colId);
      setSelectedCollegeModal(details);
    } catch (e) {
      alert('Failed to load college details.');
    } finally {
      setModalLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-8">
        <span className="text-xs font-bold uppercase tracking-widest text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
          Institutional Directory
        </span>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 mt-2 tracking-tight">
          Premier Engineering Colleges & Official Disclosures
        </h1>
        <p className="text-slate-600 text-sm mt-2">
          Explore IITs, NITs, IIITs, and premier state universities across India with verified official websites and NIRF placement disclosures.
        </p>
      </div>

      {/* Search & Filters */}
      <div className="bg-white p-4 sm:p-6 rounded-2xl border border-slate-200 shadow-sm mb-8">
        <form onSubmit={handleSearchSubmit} className="grid grid-cols-1 sm:grid-cols-12 gap-4">
          
          <div className="sm:col-span-6 relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search college name, short code, or city..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900"
            />
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          </div>

          <div className="sm:col-span-3">
            <select
              value={typeFilter}
              onChange={(e) => { setTypeFilter(e.target.value); setPage(1); }}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-700 bg-white"
            >
              <option value="All">All College Types</option>
              <option value="IIT">IITs Only</option>
              <option value="NIT">NITs Only</option>
              <option value="IIIT">IIITs Only</option>
              <option value="GFTI">GFTIs Only</option>
              <option value="State-Govt">State Government</option>
            </select>
          </div>

          <div className="sm:col-span-3">
            <button
              type="submit"
              className="w-full py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs transition-colors shadow-sm"
            >
              Apply Filter
            </button>
          </div>

        </form>
      </div>

      {/* Results List */}
      {loading ? (
        <div className="py-24 flex justify-center items-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-sm text-slate-600 font-semibold">Loading Colleges...</span>
        </div>
      ) : colleges.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {colleges.map((c) => (
            <div 
              key={c.id} 
              className="bg-white rounded-2xl border border-slate-200 p-5 hover:border-blue-400 hover:shadow-lg transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="px-2.5 py-0.5 rounded text-[10px] font-extrabold uppercase bg-blue-100 text-blue-800">
                    {c.type}
                  </span>
                  {c.nirf_rank && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-900 border border-amber-200">
                      NIRF #{c.nirf_rank}
                    </span>
                  )}
                </div>

                <h3 className="text-base font-bold text-slate-900 leading-snug">
                  {c.name}
                </h3>

                <p className="text-xs text-slate-500 mt-1 flex items-center space-x-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  <span>{c.city ? `${c.city}, ` : ''}{c.state}</span>
                  {c.established_year && <span>• Est. {c.established_year}</span>}
                </p>

                {c.placement && (
                  <div className="mt-4 p-3 rounded-xl bg-emerald-50/40 border border-emerald-100">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-500">NIRF Median CTC:</span>
                      <span className="font-black text-emerald-800">
                        {c.placement.median_package_lpa ? `₹${c.placement.median_package_lpa} LPA` : 'N/A'}
                      </span>
                    </div>
                    {c.placement.placement_percentage && (
                      <div className="flex items-center justify-between text-xs mt-1">
                        <span className="font-semibold text-slate-500">Placement %:</span>
                        <span className="font-black text-emerald-800">
                          {c.placement.placement_percentage}%
                        </span>
                      </div>
                    )}
                  </div>
                )}
              </div>

              <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs font-bold">
                <button
                  onClick={() => openCollegeModal(c.id)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  View Profile & Cutoffs →
                </button>

                {c.official_website && (
                  <a
                    href={c.official_website}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center space-x-1 text-slate-600 hover:text-slate-900"
                    title="Visit Official Website"
                  >
                    <span>Website</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="py-16 text-center text-slate-500">
          No colleges matching the specified filter criteria.
        </div>
      )}

      {/* Pagination */}
      {total > 15 && (
        <div className="flex items-center justify-between border-t border-slate-200 pt-4 text-xs font-bold text-slate-600">
          <span>Showing {((page - 1) * 15) + 1} to {Math.min(page * 15, total)} of {total} institutions</span>
          <div className="flex space-x-2">
            <button
              disabled={page <= 1}
              onClick={() => setPage(p => Math.max(1, p - 1))}
              className="px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-40"
            >
              Previous
            </button>
            <button
              disabled={page * 15 >= total}
              onClick={() => setPage(p => p + 1)}
              className="px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>
      )}

      {/* College Profile Modal */}
      {selectedCollegeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
          <div className="bg-white rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border border-slate-200 shadow-2xl p-6 sm:p-8 relative">
            <div className="flex items-start justify-between pb-4 border-b border-slate-100 mb-6">
              <div>
                <span className="text-[11px] font-extrabold uppercase bg-blue-100 text-blue-800 px-2.5 py-0.5 rounded">
                  {selectedCollegeModal.type}
                </span>
                <h2 className="text-2xl font-black text-slate-900 mt-1">
                  {selectedCollegeModal.name}
                </h2>
                <p className="text-xs text-slate-500 mt-0.5 flex items-center space-x-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  <span>{selectedCollegeModal.city ? `${selectedCollegeModal.city}, ` : ''}{selectedCollegeModal.state}</span>
                </p>
              </div>
              <button
                onClick={() => setSelectedCollegeModal(null)}
                className="text-slate-400 hover:text-slate-600 p-2 text-xl font-bold"
              >
                ✕
              </button>
            </div>

            {/* Placement Info */}
            {selectedCollegeModal.placement && (
              <div className="p-4 rounded-2xl bg-emerald-50/50 border border-emerald-200 mb-6">
                <h4 className="text-xs font-bold text-emerald-900 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                  <TrendingUp className="w-4 h-4 text-emerald-600" />
                  <span>Official NIRF Placement Disclosure</span>
                </h4>
                <div className="grid grid-cols-3 gap-3 text-center text-xs">
                  <div className="bg-white p-2.5 rounded-xl border border-emerald-100">
                    <span className="text-[10px] text-slate-500 block">Median Package</span>
                    <span className="text-base font-black text-emerald-800">
                      ₹{selectedCollegeModal.placement.median_package_lpa} LPA
                    </span>
                  </div>
                  <div className="bg-white p-2.5 rounded-xl border border-emerald-100">
                    <span className="text-[10px] text-slate-500 block">Placement Rate</span>
                    <span className="text-base font-black text-emerald-800">
                      {selectedCollegeModal.placement.placement_percentage}%
                    </span>
                  </div>
                  <div className="bg-white p-2.5 rounded-xl border border-emerald-100">
                    <span className="text-[10px] text-slate-500 block">Highest Package</span>
                    <span className="text-base font-black text-emerald-800">
                      ₹{selectedCollegeModal.placement.highest_package_lpa} LPA
                    </span>
                  </div>
                </div>
                <p className="text-[10px] text-slate-500 mt-2 italic">
                  {selectedCollegeModal.placement.label}
                </p>
              </div>
            )}

            {/* Offered Branches */}
            <div className="mb-6">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
                Offered Branches & Programs ({selectedCollegeModal.branches_count})
              </h4>
              <div className="max-h-48 overflow-y-auto space-y-1.5 pr-2">
                {selectedCollegeModal.branches?.map((b) => (
                  <div key={b.id} className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 text-xs flex items-center justify-between">
                    <span className="font-bold text-slate-800">{b.canonical_name}</span>
                    <span className="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded">{b.degree}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Sample Round 5 Cutoffs */}
            {selectedCollegeModal.sample_cutoffs?.length > 0 && (
              <div className="mb-6">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
                  Sample Published Round 5 Cutoffs (OPEN / HS / OS)
                </h4>
                <div className="overflow-x-auto rounded-xl border border-slate-200 text-xs">
                  <table className="w-full text-left">
                    <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 font-bold text-[11px]">
                      <tr>
                        <th className="p-2.5">Branch</th>
                        <th className="p-2.5">Quota</th>
                        <th className="p-2.5">Category</th>
                        <th className="p-2.5">Closing Rank</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {selectedCollegeModal.sample_cutoffs.slice(0, 8).map((sc, i) => (
                        <tr key={i}>
                          <td className="p-2.5 font-medium text-slate-900">{sc.branch}</td>
                          <td className="p-2.5">{sc.quota}</td>
                          <td className="p-2.5 font-semibold">{sc.category}</td>
                          <td className="p-2.5 font-mono font-bold text-blue-700">{sc.closing_rank.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            <div className="flex justify-end space-x-3 pt-3 border-t border-slate-100">
              <button
                onClick={() => setSelectedCollegeModal(null)}
                className="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-700 font-bold text-xs hover:bg-slate-50"
              >
                Close
              </button>
              {selectedCollegeModal.official_website && (
                <a
                  href={selectedCollegeModal.official_website}
                  target="_blank"
                  rel="noreferrer"
                  className="px-5 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-xs hover:bg-blue-700 flex items-center space-x-1.5 shadow-sm"
                >
                  <span>Visit Official Website</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
