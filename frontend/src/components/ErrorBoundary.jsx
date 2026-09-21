import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    // Clear URL search params that might have triggered corrupt state
    try {
      window.history.pushState({}, '', window.location.pathname);
    } catch (e) {
      console.warn(e);
    }
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[400px] flex items-center justify-center p-6">
          <div className="max-w-md w-full bg-white rounded-3xl border border-rose-200 shadow-xl p-6 sm:p-8 text-center space-y-4">
            <div className="w-12 h-12 rounded-full bg-rose-50 text-rose-600 flex items-center justify-center mx-auto">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-black text-slate-900">
              Something went wrong while rendering this section
            </h3>
            <p className="text-xs text-slate-500 font-normal">
              {this.state.error?.message || 'An unexpected rendering issue occurred.'}
            </p>
            <button
              onClick={this.handleReset}
              className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs inline-flex items-center space-x-2 shadow-md shadow-blue-500/25 transition-all"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Reset & Reload Page</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
