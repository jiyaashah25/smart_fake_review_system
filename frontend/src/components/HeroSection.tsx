import React from 'react';
import { Search, BarChart2, ArrowRight } from 'lucide-react';

interface HeroSectionProps {
  onAnalyzeClick: () => void;
  onAnalyticsClick: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  onAnalyzeClick,
  onAnalyticsClick,
}) => {
  return (
    <section className="relative pt-4 pb-10 space-y-12">
      {/* Background Depth Effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[280px] bg-[#E8A0B8]/5 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute top-1/3 left-1/4 w-[280px] h-[180px] bg-[#B87591]/5 blur-[90px] rounded-full pointer-events-none" />

      {/* Editorial Headline & Introduction */}
      <div className="relative max-w-3xl mx-auto text-center space-y-4">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-[#29212B] border border-[#493643] text-[#F3C4D5] text-xs font-medium backdrop-blur-sm">
          <span>Trained on Deceptive Opinion Spam Benchmark</span>
        </div>

        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-semibold text-[#FFF7F2] tracking-tight leading-tight">
          Better insight into the reviews you read.
        </h1>

        <p className="text-base sm:text-lg text-[#C5B8C1] max-w-2xl mx-auto leading-relaxed">
          Analyze review language using a machine learning model trained on a labelled deceptive-opinion benchmark.
        </p>

        {/* Primary Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-3">
          <button
            type="button"
            onClick={onAnalyzeClick}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-2.5 rounded-md text-sm font-semibold text-[#171319] bg-[#E8A0B8] hover:bg-[#F3C4D5] transition-colors shadow-xs"
          >
            <Search className="w-4 h-4" />
            <span>Analyze a review</span>
          </button>

          <button
            type="button"
            onClick={onAnalyticsClick}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-2.5 rounded-md text-sm font-medium text-[#FFF7F2] bg-[#29212B] hover:bg-[#211A22] border border-[#493643] transition-colors"
          >
            <BarChart2 className="w-4 h-4 text-[#E8A0B8]" />
            <span>View model performance</span>
          </button>
        </div>
      </div>

      {/* 3-Stage Process Explanation */}
      <div className="relative bg-[#29212B] border border-[#493643] rounded-lg p-6 sm:p-8 max-w-5xl mx-auto shadow-sm backdrop-blur-sm">
        <div className="mb-6">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-[#B87591]">
            Analysis Pipeline
          </h2>
          <p className="text-lg font-semibold text-[#FFF7F2] mt-0.5">
            How a review is evaluated
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-2 border-t md:border-t-0 md:border-l border-[#493643] pt-4 md:pt-0 md:pl-5 first:border-0 first:pt-0 first:pl-0">
            <span className="text-xs font-mono font-semibold text-[#E8A0B8]">01</span>
            <h3 className="text-sm font-semibold text-[#FFF7F2]">
              1. Review text is submitted
            </h3>
            <p className="text-xs text-[#C5B8C1] leading-relaxed">
              Customer review feedback is submitted directly into the review analyzer.
              The text is parsed, sanitized, and tokenized for inspection.
            </p>
          </div>

          <div className="space-y-2 border-t md:border-t-0 md:border-l border-[#493643] pt-4 md:pt-0 md:pl-5">
            <span className="text-xs font-mono font-semibold text-[#E8A0B8]">02</span>
            <h3 className="text-sm font-semibold text-[#FFF7F2]">
              2. NLP model analyzes textual patterns
            </h3>
            <p className="text-xs text-[#C5B8C1] leading-relaxed">
              TF-IDF n-gram vectorization extracts lexical patterns, while heuristic detectors examine
              stylistic signals such as promotional superlatives and punctuation density.
            </p>
          </div>

          <div className="space-y-2 border-t md:border-t-0 md:border-l border-[#493643] pt-4 md:pt-0 md:pl-5">
            <span className="text-xs font-mono font-semibold text-[#E8A0B8]">03</span>
            <h3 className="text-sm font-semibold text-[#FFF7F2]">
              3. Prediction and supporting signals
            </h3>
            <p className="text-xs text-[#C5B8C1] leading-relaxed">
              The application displays the predicted class (likely genuine or potentially fake), calibrated
              confidence score, and influential terms that guided the outcome.
            </p>
          </div>
        </div>

        {/* Methodology & Limitations Disclaimer */}
        <div className="mt-6 pt-5 border-t border-[#493643] text-xs text-[#C5B8C1] leading-relaxed">
          <strong className="text-[#FFF7F2] font-medium">Model scope and limitations: </strong>
          This model identifies linguistic patterns statistically associated with deceptive reviews in research benchmarks;
          it does not verify fraud with certainty or access commercial seller databases.
        </div>
      </div>

      {/* Feature Gateway Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 max-w-5xl mx-auto">
        <div
          onClick={onAnalyzeClick}
          className="bg-[#29212B] border border-[#493643] hover:border-[#E8A0B8] rounded-lg p-6 cursor-pointer transition-all flex flex-col justify-between group shadow-sm"
        >
          <div>
            <div className="w-9 h-9 rounded-md bg-[#201921] border border-[#493643] text-[#E8A0B8] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
              <Search className="w-4 h-4" />
            </div>
            <h3 className="text-base font-semibold text-[#FFF7F2]">
              Single Review Analysis Engine
            </h3>
            <p className="text-xs text-[#C5B8C1] mt-1.5 leading-relaxed">
              Test individual customer reviews with instant predictions, calibrated confidence metrics, stylistic indicators, and token-level feature attribution.
            </p>
          </div>
          <div className="pt-4 mt-4 border-t border-[#493643] flex items-center justify-between text-xs font-semibold text-[#E8A0B8]">
            <span>Analyze text</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        <div
          onClick={onAnalyticsClick}
          className="bg-[#29212B] border border-[#493643] hover:border-[#E8A0B8] rounded-lg p-6 cursor-pointer transition-all flex flex-col justify-between group shadow-sm"
        >
          <div>
            <div className="w-9 h-9 rounded-md bg-[#201921] border border-[#493643] text-[#E8A0B8] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
              <BarChart2 className="w-4 h-4" />
            </div>
            <h3 className="text-base font-semibold text-[#FFF7F2]">
              Model Performance & Evaluation
            </h3>
            <p className="text-xs text-[#C5B8C1] mt-1.5 leading-relaxed">
              Examine empirical metrics from the hold-out test set (90.3% accuracy), algorithm comparison benchmarks, confusion matrix heatmaps, and ROC curves.
            </p>
          </div>
          <div className="pt-4 mt-4 border-t border-[#493643] flex items-center justify-between text-xs font-semibold text-[#E8A0B8]">
            <span>View metrics</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>
      </div>
    </section>
  );
};
