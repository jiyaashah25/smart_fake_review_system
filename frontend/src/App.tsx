import React, { useState, useEffect } from 'react';
import { Navbar, ViewType } from './components/Navbar';
import { HeroSection } from './components/HeroSection';
import { ReviewAnalyzer } from './components/ReviewAnalyzer';
import { PredictionResult } from './components/PredictionResult';
import { AnalyticsDashboard } from './components/AnalyticsDashboard';
import { ReviewHistory } from './components/ReviewHistory';
import { HowItWorks } from './components/HowItWorks';
import { Footer } from './components/Footer';
import { useReviewAnalysis } from './hooks/useReviewAnalysis';
import { api } from './services/api';
import { ArrowLeft, ArrowRight, BarChart2, Search } from 'lucide-react';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewType>('overview');
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(true);

  const {
    loading,
    result,
    error,
    history,
    analyzeReview,
    clearHistory,
    selectHistoryItem
  } = useReviewAnalysis();

  // Periodic health check
  useEffect(() => {
    const checkServer = async () => {
      try {
        const res = await api.checkHealth();
        setIsBackendHealthy(res.status === 'healthy' && res.model_loaded);
      } catch {
        setIsBackendHealthy(false);
      }
    };

    checkServer();
    const interval = setInterval(checkServer, 20000);
    return () => clearInterval(interval);
  }, []);

  const handleNavigate = (view: ViewType) => {
    setCurrentView(view);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#171319] text-[#FFF7F2]">
      {/* Sticky Top Navbar */}
      <Navbar
        onNavigate={handleNavigate}
        currentView={currentView}
        isBackendHealthy={isBackendHealthy}
      />

      {/* Main Page Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        {/* VIEW 1: OVERVIEW */}
        {currentView === 'overview' && (
          <div className="space-y-12 animate-fade-in">
            {/* Hero with Process Explanations */}
            <HeroSection
              onAnalyzeClick={() => handleNavigate('analyzer')}
              onAnalyticsClick={() => handleNavigate('performance')}
            />

            {/* How It Works Pipeline Section */}
            <HowItWorks />
          </div>
        )}

        {/* VIEW 2: DEDICATED REVIEW ANALYSIS PAGE */}
        {currentView === 'analyzer' && (
          <div className="space-y-6 animate-fade-in">
            {/* Top Navigation Row */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#493643]">
              <div className="flex items-center space-x-2">
                <button
                  type="button"
                  onClick={() => handleNavigate('overview')}
                  className="inline-flex items-center space-x-1.5 text-xs font-medium px-3 py-1.5 rounded-md bg-[#29212B] border border-[#493643] text-[#C5B8C1] hover:text-[#FFF7F2] hover:bg-[#211A22] transition-colors"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Overview</span>
                </button>
                <div className="h-4 w-[1px] bg-[#493643] hidden sm:block" />
                <span className="text-xs text-[#E8A0B8] font-medium hidden sm:inline">
                  Single Review Analysis
                </span>
              </div>

              <div className="flex items-center space-x-3 text-xs">
                <button
                  type="button"
                  onClick={() => handleNavigate('performance')}
                  className="inline-flex items-center space-x-1 text-[#C5B8C1] hover:text-[#FFF7F2] transition-colors"
                >
                  <BarChart2 className="w-3.5 h-3.5 text-[#E8A0B8]" />
                  <span>Model Performance</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Single Review Analyzer Panel */}
            <ReviewAnalyzer
              onAnalyze={analyzeReview}
              loading={loading}
              error={error}
            />

            {/* Prediction Result Display */}
            {result && (
              <div className="animate-fade-in">
                <PredictionResult data={result} />
              </div>
            )}

            {/* Session Review History */}
            <ReviewHistory
              history={history}
              onSelect={item => {
                selectHistoryItem(item);
                window.scrollTo({ top: 80, behavior: 'smooth' });
              }}
              onClear={clearHistory}
            />

            {/* Bottom Context Banner */}
            <div className="p-5 rounded-lg bg-[#29212B] border border-[#493643] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 className="text-sm font-semibold text-[#FFF7F2]">
                  Need to inspect empirical evaluation metrics?
                </h3>
                <p className="text-xs text-[#C5B8C1] mt-0.5">
                  Examine confusion matrices, ROC curves, and cross-validation statistics on the benchmark test set.
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleNavigate('performance')}
                className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-md text-xs font-semibold text-[#FFF7F2] bg-[#201921] hover:bg-[#29212B] border border-[#493643] transition-colors shrink-0"
              >
                <span>View Model Performance</span>
                <ArrowRight className="w-3.5 h-3.5 text-[#E8A0B8]" />
              </button>
            </div>
          </div>
        )}

        {/* VIEW 3: DEDICATED MODEL PERFORMANCE PAGE */}
        {currentView === 'performance' && (
          <div className="space-y-6 animate-fade-in">
            {/* Top Navigation Row */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#493643]">
              <div className="flex items-center space-x-2">
                <button
                  type="button"
                  onClick={() => handleNavigate('overview')}
                  className="inline-flex items-center space-x-1.5 text-xs font-medium px-3 py-1.5 rounded-md bg-[#29212B] border border-[#493643] text-[#C5B8C1] hover:text-[#FFF7F2] hover:bg-[#211A22] transition-colors"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Overview</span>
                </button>
                <div className="h-4 w-[1px] bg-[#493643] hidden sm:block" />
                <span className="text-xs text-[#E8A0B8] font-medium hidden sm:inline">
                  Empirical Benchmark Telemetry
                </span>
              </div>

              <button
                type="button"
                onClick={() => handleNavigate('analyzer')}
                className="inline-flex items-center space-x-1 text-xs font-medium text-[#C5B8C1] hover:text-[#FFF7F2] transition-colors"
              >
                <Search className="w-3.5 h-3.5 text-[#E8A0B8]" />
                <span>Test in Review Analyzer</span>
                <ArrowRight className="w-3.5 h-3.5 ml-0.5" />
              </button>
            </div>

            {/* Full Model Performance Dashboard */}
            <AnalyticsDashboard />
          </div>
        )}
      </main>

      {/* Professional Footer */}
      <Footer onNavigate={handleNavigate} />
    </div>
  );
};

export default App;
