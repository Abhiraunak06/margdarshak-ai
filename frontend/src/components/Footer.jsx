import React from 'react';
import { ShieldCheck, ExternalLink, Database, AlertCircle } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-400 text-sm border-t border-slate-800 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          {/* Col 1: About & Purpose */}
          <div className="space-y-3 md:col-span-2">
            <div className="flex items-center space-x-2 text-white font-extrabold text-lg">
              <div className="w-7 h-7 rounded-xl bg-gradient-to-tr from-pink-500 to-purple-600 flex items-center justify-center text-white text-xs font-black shadow-xs">
                M
              </div>
              <span>Margdarshak — AI Career & University Intelligence</span>
            </div>
            <p className="text-slate-400 leading-relaxed text-xs">
              A high-precision, data-driven career guidance and college prediction platform built exclusively for Indian students. 
              Powered by machine learning models and authoritative counselling datasets across National (JoSAA/CSAB, NEET-UG, CUET-UG) and State levels.
            </p>
            <div className="p-3 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-amber-300/90 flex items-start space-x-2">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-amber-400" />
              <span>
                <strong>Official Disclaimer:</strong> College prediction results are calculated strictly from historical published opening and closing rank archives. Cutoffs vary each counselling year based on applicant volume, seat matrix adjustments, and student choices. Not a guarantee of admission.
              </span>
            </div>
          </div>

          {/* Col 2: Authoritative Data Sources */}
          <div>
            <h4 className="text-white font-semibold text-xs tracking-wider uppercase mb-3 flex items-center space-x-1.5">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>Verified Data Sources</span>
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <a 
                  href="https://josaa.admissions.nic.in" 
                  target="_blank" 
                  rel="noreferrer"
                  className="hover:text-white transition-colors flex items-center space-x-1"
                >
                  <span>JoSAA / NIC Official Portal</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://csab.nic.in" 
                  target="_blank" 
                  rel="noreferrer"
                  className="hover:text-white transition-colors flex items-center space-x-1"
                >
                  <span>CSAB Special Rounds</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://www.nirfindia.org" 
                  target="_blank" 
                  rel="noreferrer"
                  className="hover:text-white transition-colors flex items-center space-x-1"
                >
                  <span>NIRF Ministry of Education</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://wbjeeb.nic.in" 
                  target="_blank" 
                  rel="noreferrer"
                  className="hover:text-white transition-colors flex items-center space-x-1"
                >
                  <span>WBJEEB West Bengal</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
            </ul>
          </div>

          {/* Col 3: Principles & Integrity */}
          <div>
            <h4 className="text-white font-semibold text-xs tracking-wider uppercase mb-3">
              Data Integrity Policy
            </h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              <li className="flex items-center space-x-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span>Zero fabricated/sample cutoffs</span>
              </li>
              <li className="flex items-center space-x-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span>Explicit missing data disclosures</span>
              </li>
              <li className="flex items-center space-x-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span>Verified official college websites only</span>
              </li>
              <li className="flex items-center space-x-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span>Transparent college vs branch placements</span>
              </li>
            </ul>
          </div>

        </div>

        <div className="pt-8 border-t border-slate-800 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-500">
          <p>© {new Date().getFullYear()} CareerPath AI. Built for Indian Students & Aspirants.</p>
          <p className="mt-2 sm:mt-0">All trademarks and examination names are the property of their respective official governing bodies.</p>
        </div>
      </div>
    </footer>
  );
}
