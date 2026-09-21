import React from 'react';
import { 
  Compass, 
  GraduationCap, 
  Briefcase, 
  BookmarkCheck, 
  ShieldCheck, 
  Sparkles,
  Download,
  Bot
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, savedCount = 0, onOpenCompare, onOpenChatbot }) {
  return (
    <header className="sticky top-0 z-40 bg-white/70 backdrop-blur-xl border-b border-white/80 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo: Margdarshak */}
          <div 
            onClick={() => setActiveTab('predictor')}
            className="flex items-center space-x-3 cursor-pointer group select-none"
          >
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-pink-500 via-purple-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-purple-500/20 group-hover:scale-105 transition-transform">
              <span className="font-black text-lg tracking-wider">M</span>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-extrabold tracking-tight text-slate-900 font-sans">Margdarshak</span>
                <span className="text-[10px] font-black px-2 py-0.5 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 text-white shadow-xs">
                  AI
                </span>
              </div>
              <p className="text-[10px] text-slate-500 font-medium hidden sm:block">AI Career Intelligence & Stream Discovery</p>
            </div>
          </div>

          {/* Navigation Items */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-100/70 p-1 rounded-2xl border border-slate-200/60 backdrop-blur-sm">
            <button
              onClick={() => setActiveTab('predictor')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'predictor' 
                  ? 'bg-white text-slate-900 shadow-xs' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <Compass className="w-3.5 h-3.5 text-blue-600" />
              <span>Predictor</span>
            </button>

            <button
              onClick={() => setActiveTab('colleges')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'colleges' 
                  ? 'bg-white text-slate-900 shadow-xs' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <GraduationCap className="w-3.5 h-3.5 text-purple-600" />
              <span>Colleges</span>
            </button>

            <button
              onClick={() => setActiveTab('careers')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'careers' 
                  ? 'bg-white text-slate-900 shadow-xs' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <Briefcase className="w-3.5 h-3.5 text-emerald-600" />
              <span>Career Explorer</span>
            </button>

            <button
              onClick={() => setActiveTab('roadmap')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'roadmap' 
                  ? 'bg-white text-slate-900 shadow-xs' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>Roadmaps</span>
            </button>

            <button
              onClick={() => setActiveTab('admin')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'admin' 
                  ? 'bg-white text-slate-900 shadow-xs' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />
              <span>Data Admin</span>
            </button>
          </nav>

          {/* Right Actions */}
          <div className="flex items-center space-x-2 sm:space-x-2.5">
            {/* Margdarshak AI Chatbot Pill */}
            <button
              onClick={onOpenChatbot}
              className="flex items-center space-x-1.5 px-3.5 py-2 rounded-2xl bg-gradient-to-r from-pink-500 via-purple-600 to-indigo-600 hover:from-pink-600 hover:to-indigo-700 text-white text-xs font-extrabold shadow-md shadow-purple-500/20 transition-all transform active:scale-95"
              title="Open Margdarshak AI 15-Question Recommender"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-200 animate-spin-slow" />
              <span>Margdarshak AI</span>
            </button>

            {/* Saved Colleges */}
            <button
              onClick={onOpenCompare}
              className="relative flex items-center space-x-1 px-3 py-2 rounded-2xl border border-slate-200/80 bg-white/80 hover:bg-white text-xs font-bold text-slate-700 transition-all shadow-xs"
              title="View Bookmarked Colleges & Compare"
            >
              <BookmarkCheck className="w-3.5 h-3.5 text-blue-600" />
              <span className="hidden sm:inline">Saved</span>
              {savedCount > 0 && (
                <span className="ml-1 px-1.5 py-0.2 text-[10px] font-black rounded-full bg-blue-600 text-white">
                  {savedCount}
                </span>
              )}
            </button>

            {/* Download Project Source */}
            <a
              href="http://127.0.0.1:8000/api/download/project"
              download="margdarshak-platform.zip"
              className="hidden lg:flex items-center space-x-1.5 px-3 py-2 rounded-2xl bg-slate-900 hover:bg-slate-800 text-xs font-bold text-white transition-all shadow-xs"
              title="Download Complete Project Source Archive (.ZIP)"
            >
              <Download className="w-3.5 h-3.5 text-slate-300" />
              <span>Source ZIP</span>
            </a>
          </div>
        </div>

        {/* Mobile Sub-Navigation */}
        <div className="flex md:hidden overflow-x-auto py-2 border-t border-slate-100 space-x-1.5 text-xs font-bold no-scrollbar">
          <button
            onClick={() => setActiveTab('predictor')}
            className={`px-3 py-1.5 rounded-full whitespace-nowrap ${
              activeTab === 'predictor' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'
            }`}
          >
            Predictor
          </button>
          <button
            onClick={() => setActiveTab('colleges')}
            className={`px-3 py-1.5 rounded-full whitespace-nowrap ${
              activeTab === 'colleges' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'
            }`}
          >
            Colleges
          </button>
          <button
            onClick={() => setActiveTab('careers')}
            className={`px-3 py-1.5 rounded-full whitespace-nowrap ${
              activeTab === 'careers' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'
            }`}
          >
            Careers
          </button>
          <button
            onClick={() => setActiveTab('roadmap')}
            className={`px-3 py-1.5 rounded-full whitespace-nowrap ${
              activeTab === 'roadmap' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'
            }`}
          >
            Roadmaps
          </button>
          <button
            onClick={() => setActiveTab('admin')}
            className={`px-3 py-1.5 rounded-full whitespace-nowrap ${
              activeTab === 'admin' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'
            }`}
          >
            Data Admin
          </button>
        </div>
      </div>
    </header>
  );
}
