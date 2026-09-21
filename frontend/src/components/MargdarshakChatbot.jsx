import React, { useState, useEffect, useRef } from 'react';
import { 
  Sparkles, 
  MessageSquare, 
  X, 
  Minimize2, 
  Maximize2, 
  Send, 
  ArrowRight, 
  ArrowLeft,
  Compass, 
  RotateCcw, 
  CheckCircle2, 
  BrainCircuit, 
  Building2, 
  GraduationCap, 
  Award,
  ChevronRight,
  TrendingUp,
  FastForward,
  ExternalLink
} from 'lucide-react';
import { recommendCareer, fetchChatbotQuestions } from '../services/api';

const DEFAULT_KEY_FEATURES = [
  { id: 'q1', feature: 'biology_interest', prompt: 'Interest in Biology & Living Systems' },
  { id: 'q2', feature: 'medical_healthcare_interest', prompt: 'Interest in Medicine, Clinical Care & Health' },
  { id: 'q3', feature: 'chemistry_interest', prompt: 'Interest in Chemistry, Formulations & Drugs' },
  { id: 'q4', feature: 'computer_interest', prompt: 'Interest in Computers, Programming & Software' },
  { id: 'q5', feature: 'mathematics_interest', prompt: 'Interest in Mathematics & Numbers' },
  { id: 'q6', feature: 'accountancy_interest', prompt: 'Interest in Accounting, Auditing & Ledgers' },
  { id: 'q7', feature: 'business_finance_interest', prompt: 'Interest in Financial Markets & Banking' },
  { id: 'q8', feature: 'business_interest', prompt: 'Interest in Business Strategy & Startups' },
  { id: 'q9', feature: 'law_debate_interest', prompt: 'Interest in Law, Rules & Legal Debates' },
  { id: 'q10', feature: 'history_political_science_interest', prompt: 'Interest in History, Politics & Civics' },
  { id: 'q11', feature: 'government_public_service_interest', prompt: 'Interest in Civil Service & Public Administration' },
  { id: 'q12', feature: 'psychology_interest', prompt: 'Interest in Human Psychology & Mental Health' },
  { id: 'q13', feature: 'teaching_interest', prompt: 'Interest in Teaching, Lecturing & Mentoring' },
  { id: 'q14', feature: 'public_speaking', prompt: 'Confidence in Public Speaking & Presenting' },
  { id: 'q15', feature: 'creativity', prompt: 'Creativity, Hands-on Dexterity & Design' },
];

export default function MargdarshakChatbot({ 
  isOpen, 
  onClose, 
  onNavigateStream,
  initialQuery = '',
  onClearInitialQuery
}) {
  const [messages, setMessages] = useState([]);
  const [questions, setQuestions] = useState(DEFAULT_KEY_FEATURES);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isAssessmentActive, setIsAssessmentActive] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [recommendationResult, setRecommendationResult] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [isMinimized, setIsMinimized] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const chatEndRef = useRef(null);
  const resultsRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (recommendationResult) {
      // Smoothly scroll to the START (top) of recommendations so user sees the #1 career card immediately
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 80);
    } else {
      scrollToBottom();
    }
  }, [messages, currentQuestionIndex, isAnalyzing, recommendationResult]);

  // Load questions from backend
  useEffect(() => {
    fetchChatbotQuestions()
      .then((data) => {
        if (data && data.questions && data.questions.length > 0) {
          setQuestions(data.questions);
        }
      })
      .catch((err) => {
        console.warn('Using default 15 questions fallback:', err);
      });
  }, []);

  // Initial greeting
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 'greeting',
          sender: 'bot',
          text: 'Namaste! I am Margdarshak AI, your Machine Learning Career Discovery Guide.',
          subtext: 'I will ask you 15 core questions rated on a 1-to-10 scale (default is 5). Based on your responses, our Random Forest classifier analyzes 7,200 empirical benchmarks and recommends your top matching career paths, with 1-click redirection to our website portals.'
        }
      ]);
    }
  }, []);

  // Handle initialQuery if passed from hero prompt
  useEffect(() => {
    if (isOpen && initialQuery && initialQuery.trim()) {
      handleStart();
      if (onClearInitialQuery) onClearInitialQuery();
    }
  }, [isOpen, initialQuery]);

  // Start assessment
  const handleStart = () => {
    setIsAssessmentActive(true);
    setCurrentQuestionIndex(0);
    setAnswers({});
    setRecommendationResult(null);
    setErrorMsg(null);

    const firstQ = questions[0];
    setMessages(prev => [
      ...prev,
      {
        id: Date.now().toString(),
        sender: 'user',
        text: 'Start 15-Question Assessment'
      },
      {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        text: `Question 1 of ${questions.length}: ${firstQ.prompt}`,
        subtext: 'Rate yourself from 1 to 10 (Click a score below or press Enter to keep default 5):',
        qIdx: 0
      }
    ]);
  };

  // Submit an answer for the current question
  const handleAnswerQuestion = (val) => {
    const rating = Math.max(1, Math.min(10, parseInt(val, 10) || 5));
    const currentQ = questions[currentQuestionIndex];
    const updatedAnswers = {
      ...answers,
      [currentQ.feature]: rating
    };
    setAnswers(updatedAnswers);

    // Add user message
    const userMsg = {
      id: Date.now().toString(),
      sender: 'user',
      text: `[${currentQuestionIndex + 1}/${questions.length}] ${currentQ.prompt}: ${rating}/10`
    };

    const nextIdx = currentQuestionIndex + 1;
    if (nextIdx < questions.length) {
      const nextQ = questions[nextIdx];
      setCurrentQuestionIndex(nextIdx);
      setMessages(prev => [
        ...prev,
        userMsg,
        {
          id: (Date.now() + 1).toString(),
          sender: 'bot',
          text: `Question ${nextIdx + 1} of ${questions.length}: ${nextQ.prompt}`,
          subtext: 'Rate yourself from 1 to 10 (Click a score below or press Enter to keep default 5):',
          qIdx: nextIdx
        }
      ]);
    } else {
      // Finished all 15 questions -> Run ML model
      setCurrentQuestionIndex(nextIdx);
      setMessages(prev => [...prev, userMsg]);
      runModelPrediction(updatedAnswers);
    }
    setTextInput('');
  };

  // Quick fill remaining with default 5
  const handleFillRemainingWithDefault = () => {
    const filled = { ...answers };
    for (let i = currentQuestionIndex; i < questions.length; i++) {
      const q = questions[i];
      if (filled[q.feature] === undefined) {
        filled[q.feature] = 5;
      }
    }
    setAnswers(filled);
    setCurrentQuestionIndex(questions.length);
    setMessages(prev => [
      ...prev,
      {
        id: Date.now().toString(),
        sender: 'user',
        text: `Set remaining questions to default 5/10 and compute recommendations.`
      }
    ]);
    runModelPrediction(filled);
  };

  // Run backend prediction
  const runModelPrediction = async (assessmentAnswers) => {
    setIsAnalyzing(true);
    setErrorMsg(null);

    try {
      const payload = {
        student_name: 'Student',
        stream: 'General',
        answers: assessmentAnswers
      };

      const result = await recommendCareer(payload);
      setRecommendationResult(result);

      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          sender: 'bot',
          text: 'Career Assessment Complete! Here are your Top Matches:',
          subtext: 'Our Random Forest model computed your profile compatibility and distinctiveness benchmark against 7,200 training cases:',
          results: result.recommendations
        }
      ]);
    } catch (err) {
      console.error('Recommendation failed:', err);
      setErrorMsg(err.message || 'Error running career recommendation model.');
      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          sender: 'bot',
          text: 'Prediction Error',
          subtext: 'Unable to reach the recommendation service. Please verify the backend server is running.'
        }
      ]);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Restart / Reset
  const handleRestart = () => {
    setIsAssessmentActive(false);
    setCurrentQuestionIndex(0);
    setAnswers({});
    setRecommendationResult(null);
    setErrorMsg(null);
    setTextInput('');
    setMessages([
      {
        id: 'greeting_reset',
        sender: 'bot',
        text: 'Assessment reset. Ready when you are!',
        subtext: 'Click below to start the 15-question career assessment again.'
      }
    ]);
  };

  // Redirect to website stream / tab
  const handleRedirect = (rec) => {
    if (onNavigateStream) {
      const targetStream = rec.target_stream || 'PCM';
      const targetTab = rec.target_tab || 'predictor';
      onNavigateStream(targetStream, targetTab);
      if (onClose) onClose();
    }
  };

  // Handle text input submission
  const handleTextSubmit = (e) => {
    e?.preventDefault();
    if (!textInput.trim()) {
      if (isAssessmentActive && currentQuestionIndex < questions.length) {
        handleAnswerQuestion(5); // Default 5 on empty submit
      } else if (!isAssessmentActive) {
        handleStart();
      }
      return;
    }

    const num = parseInt(textInput.trim(), 10);
    if (!isNaN(num) && isAssessmentActive && currentQuestionIndex < questions.length) {
      handleAnswerQuestion(num);
    } else {
      if (!isAssessmentActive) {
        handleStart();
      } else {
        handleAnswerQuestion(5);
      }
    }
  };

  if (!isOpen) return null;

  const currentQ = questions[currentQuestionIndex];
  const progressPct = questions.length > 0 ? Math.round((currentQuestionIndex / questions.length) * 100) : 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-950/60 backdrop-blur-sm animate-fadeIn">
      <div 
        className={`bg-white rounded-3xl shadow-2xl border border-white/80 flex flex-col transition-all duration-300 overflow-hidden ${
          isMinimized 
            ? 'w-full max-w-md h-16' 
            : 'w-full max-w-3xl h-[94vh] max-h-[850px]'
        }`}
      >
        {/* Header — Classy Frosted Iridescent */}
        <div className="bg-slate-950/95 backdrop-blur-xl p-4 text-white flex items-center justify-between border-b border-white/10 shrink-0">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/25">
              <Compass className="w-5 h-5 text-amber-300 animate-spin-slow" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="font-black text-base tracking-tight font-sans">Margdarshak AI</h3>
                <span className="bg-amber-400 text-slate-950 text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full shadow-xs">
                  Random Forest ML
                </span>
              </div>
              <p className="text-[11px] text-slate-300 font-medium">15 High-Impact Features • 1-Click Career Redirection</p>
            </div>
          </div>

          <div className="flex items-center space-x-1.5 text-white/80">
            <button
              onClick={handleRestart}
              title="Restart Assessment"
              className="p-1.5 hover:bg-white/15 hover:text-white rounded-xl transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              title={isMinimized ? "Expand" : "Minimize"}
              className="p-1.5 hover:bg-white/15 hover:text-white rounded-xl transition-colors"
            >
              {isMinimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
            </button>
            <button
              onClick={onClose}
              title="Close Chatbot"
              className="p-1.5 hover:bg-white/15 hover:text-white rounded-xl transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Minimized Bar */}
        {isMinimized ? (
          <div className="p-4 bg-slate-50 flex items-center justify-between cursor-pointer" onClick={() => setIsMinimized(false)}>
            <div className="flex items-center space-x-2 text-xs font-bold text-slate-700">
              <MessageSquare className="w-4 h-4 text-blue-600" />
              <span>Margdarshak AI: Click to resume career discovery</span>
            </div>
            <Maximize2 className="w-3.5 h-3.5 text-slate-400" />
          </div>
        ) : (
          <>
            {/* Assessment Progress Bar */}
            {isAssessmentActive && currentQuestionIndex < questions.length && (
              <div className="bg-slate-100 border-b border-slate-200 px-4 py-2 shrink-0 flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-slate-700">
                    Question {currentQuestionIndex + 1} of {questions.length}
                  </span>
                  <span className="text-[11px] text-slate-500 font-medium">
                    ({progressPct}% completed)
                  </span>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={handleFillRemainingWithDefault}
                    className="text-[11px] text-indigo-600 hover:text-indigo-800 font-bold flex items-center space-x-1 transition-colors"
                    title="Fill remaining questions with neutral 5 and see recommendations immediately"
                  >
                    <FastForward className="w-3.5 h-3.5" />
                    <span>Quick Finish (Default 5)</span>
                  </button>
                </div>
              </div>
            )}

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 bg-slate-50/70 text-slate-800 text-sm">
              {messages.map((m) => (
                <div key={m.id} className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
                  {m.sender === 'bot' ? (
                    <div className="flex items-start space-x-2.5 max-w-[96%]">
                      <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5">
                        <Compass className="w-4 h-4 text-amber-300" />
                      </div>
                      <div className="bg-white p-3.5 sm:p-4 rounded-2xl rounded-tl-sm border border-slate-200 shadow-sm text-slate-800 space-y-2.5">
                        <p className="font-extrabold text-slate-900 text-[15px]">{m.text}</p>
                        {m.subtext && (
                          <p className="text-xs font-medium text-slate-600 leading-relaxed">{m.subtext}</p>
                        )}

                        {/* Top 3 Career Results Card Deck */}
                        {m.results && m.results.length > 0 && (
                          <div ref={resultsRef} className="mt-4 pt-3 border-t border-slate-100 space-y-3.5">
                            <div className="flex items-center justify-between text-xs font-extrabold text-slate-600 uppercase tracking-wider">
                              <span>Top Recommended Career Trajectories:</span>
                              <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                                Random Forest ML
                              </span>
                            </div>

                            {m.results.map((rec, idx) => (
                              <div 
                                key={rec.career || idx} 
                                className="p-4 rounded-2xl bg-white border-2 border-slate-200 hover:border-blue-500 hover:shadow-lg transition-all space-y-3"
                              >
                                <div className="flex items-start justify-between gap-2">
                                  <div>
                                    <div className="flex items-center space-x-2">
                                      <span className={`w-6 h-6 rounded-lg text-white flex items-center justify-center text-xs font-black shrink-0 ${
                                        idx === 0 ? 'bg-amber-500 shadow-xs' : idx === 1 ? 'bg-slate-500' : 'bg-amber-700'
                                      }`}>
                                        #{rec.rank}
                                      </span>
                                      <h4 className="font-black text-slate-900 text-base leading-snug">
                                        {rec.career.toUpperCase()}
                                      </h4>
                                    </div>
                                    <div className="text-xs font-bold text-indigo-700 mt-1 pl-8">
                                      Domain: <span className="font-medium text-slate-700">{rec.career_family}</span>
                                    </div>
                                  </div>

                                  <div className="shrink-0 text-right">
                                    <div className="text-sm font-black text-emerald-700 bg-emerald-100/80 px-2.5 py-1 rounded-xl flex items-center space-x-1 border border-emerald-200">
                                      <BrainCircuit className="w-3.5 h-3.5 mr-1" />
                                      <span>{rec.confidence}%</span>
                                    </div>
                                    <span className="text-[10px] text-slate-400 font-medium">Model Match</span>
                                  </div>
                                </div>

                                {/* Why this was recommended (Explainability Engine) */}
                                <div className="text-xs bg-slate-50 p-3 rounded-xl border border-slate-100 space-y-1.5">
                                  <div className="font-extrabold text-slate-900 flex items-center space-x-1.5">
                                    <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                                    <span>Why this was recommended:</span>
                                  </div>
                                  <ul className="space-y-1 pl-2 text-slate-700">
                                    {rec.reasons && rec.reasons.map((r, rIdx) => (
                                      <li key={rIdx} className="flex items-start space-x-1.5">
                                        <span className="text-blue-600 font-bold">•</span>
                                        <span className="leading-relaxed">{r}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>

                                {/* Representative Roles & Typical Path */}
                                {rec.representative_roles && (
                                  <div className="text-xs text-slate-600">
                                    <strong className="text-slate-800">Roles: </strong>
                                    <span>{rec.representative_roles}</span>
                                  </div>
                                )}

                                {rec.typical_path_after_12 && (
                                  <div className="text-[11px] text-amber-950 bg-amber-50/70 p-2 rounded-lg border border-amber-200/70">
                                    <strong>Typical Path: </strong>
                                    <span>{rec.typical_path_after_12}</span>
                                  </div>
                                )}

                                {/* Associated Premier Colleges */}
                                {rec.associated_colleges && rec.associated_colleges.length > 0 && (
                                  <div className="pt-1">
                                    <div className="text-[11px] font-extrabold text-slate-700 flex items-center mb-1.5">
                                      <GraduationCap className="w-3.5 h-3.5 mr-1 text-blue-600" />
                                      <span>Premier Academies & Entrance Exams:</span>
                                    </div>
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                                      {rec.associated_colleges.map((col, cIdx) => (
                                        <div key={cIdx} className="p-2 bg-slate-50 rounded-xl text-[11px] border border-slate-200">
                                          <div className="font-bold text-slate-900 truncate">{col.name}</div>
                                          <div className="text-blue-700 font-semibold">{col.degree}</div>
                                          <div className="text-emerald-700 font-medium">Exam: {col.exam}</div>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}

                                {/* REDIRECTION BUTTON */}
                                <div className="pt-2">
                                  <button
                                    onClick={() => handleRedirect(rec)}
                                    className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-xs flex items-center justify-center space-x-2 shadow-md hover:shadow-lg transition-all active:scale-[0.98]"
                                  >
                                    <span>🚀 {rec.redirect_label || `Explore ${rec.career} on our website`}</span>
                                    <ArrowRight className="w-4 h-4" />
                                  </button>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ) : (
                    <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-2.5 px-4 rounded-2xl rounded-tr-sm text-sm shadow-sm max-w-[80%]">
                      {m.text}
                    </div>
                  )}
                </div>
              ))}

              {/* In-chat Question Prompt Widget (Active during questions) */}
              {isAssessmentActive && currentQuestionIndex < questions.length && (
                <div className="bg-white p-4 rounded-2xl border-2 border-indigo-200 shadow-md space-y-3.5 animate-fadeIn">
                  <div className="flex items-center justify-between">
                    <span className="px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-800 text-xs font-black uppercase tracking-wider">
                      Question {currentQuestionIndex + 1} of {questions.length}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">
                      Scale: 1 (Lowest) to 10 (Highest)
                    </span>
                  </div>

                  <p className="text-sm font-extrabold text-slate-900">
                    {currentQ.prompt}
                  </p>

                  {/* 10-point Rating Buttons */}
                  <div className="space-y-1.5">
                    <div className="text-[11px] font-bold text-slate-500">
                      Select your score (Default is 5):
                    </div>
                    <div className="grid grid-cols-10 gap-1 sm:gap-1.5">
                      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => {
                        const isDefault = num === 5;
                        return (
                          <button
                            key={num}
                            onClick={() => handleAnswerQuestion(num)}
                            className={`py-2 rounded-xl text-xs font-black transition-all flex flex-col items-center justify-center ${
                              isDefault 
                                ? 'bg-amber-100 hover:bg-amber-200 text-amber-900 border-2 border-amber-300' 
                                : 'bg-slate-50 hover:bg-blue-600 hover:text-white text-slate-800 border border-slate-200'
                            }`}
                          >
                            <span>{num}</span>
                            {isDefault && <span className="text-[8px] font-bold text-amber-700 sm:block hidden">Def</span>}
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Fast Action Buttons */}
                  <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                    {currentQuestionIndex > 0 ? (
                      <button
                        onClick={() => setCurrentQuestionIndex(prev => prev - 1)}
                        className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold flex items-center space-x-1 transition-colors"
                      >
                        <ArrowLeft className="w-3.5 h-3.5" />
                        <span>Previous</span>
                      </button>
                    ) : <div />}

                    <button
                      onClick={() => handleAnswerQuestion(5)}
                      className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold flex items-center space-x-1.5 shadow-sm transition-transform active:scale-95"
                    >
                      <span>Keep Default (5) & Next</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              )}

              {/* Analyzing Loader */}
              {isAnalyzing && (
                <div className="flex items-center space-x-3 text-slate-700 p-4 bg-white rounded-2xl border border-slate-200 shadow-sm max-w-[90%] animate-pulse">
                  <BrainCircuit className="w-5 h-5 text-indigo-600 animate-spin" />
                  <span className="text-xs font-bold">
                    Running Random Forest ML Classifier & Computing Explainability Benchmarks...
                  </span>
                </div>
              )}

              <div ref={chatEndRef} />
            </div>

            {/* Bottom Input Area */}
            <div className="p-3 sm:p-4 bg-white border-t border-slate-200/80 shrink-0">
              {!isAssessmentActive ? (
                <div className="space-y-2">
                  <button
                    onClick={handleStart}
                    className="w-full py-3 px-4 rounded-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-sm shadow-md flex items-center justify-center space-x-2 transition-all hover:shadow-lg active:scale-[0.99]"
                  >
                    <Compass className="w-4 h-4 text-amber-300" />
                    <span>Start 15-Question ML Career Assessment</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              ) : currentQuestionIndex >= questions.length ? (
                <div className="flex space-x-2">
                  <button
                    onClick={handleRestart}
                    className="flex-1 py-2.5 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center space-x-1.5 transition-colors"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Retake 15-Question Assessment</span>
                  </button>
                  <button
                    onClick={onClose}
                    className="flex-1 py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow-sm transition-colors"
                  >
                    <span>Close Chatbot</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              ) : (
                <form onSubmit={handleTextSubmit} className="flex space-x-2">
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    placeholder="Career Recommendation Chatbot"
                    className="flex-1 px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                  />
                  <button
                    type="submit"
                    className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs flex items-center space-x-1.5 shadow-sm transition-transform active:scale-95"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>Submit</span>
                  </button>
                </form>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
