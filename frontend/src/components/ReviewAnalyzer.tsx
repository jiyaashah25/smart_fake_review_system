import React, { useState } from 'react';
import { Send, RotateCcw, AlertCircle, HelpCircle } from 'lucide-react';
import { validateReviewText } from '../utils/validation';
import { LoadingAnimation } from './LoadingAnimation';

interface ReviewAnalyzerProps {
  onAnalyze: (text: string) => Promise<any>;
  loading: boolean;
  error: string | null;
}

const BENCHMARK_EXAMPLES = [
  {
    label: 'Descriptive & Specific',
    hint: 'Likely Genuine pattern',
    text: 'We stayed at this hotel for three nights on our family trip to Chicago. The front desk was friendly and check-in took five minutes. The bathroom was spotless, though water pressure in the shower was a bit low on the 14th floor.'
  },
  {
    label: 'Promotional Language',
    hint: 'Deceptive opinion pattern',
    text: 'BEST HOTEL EXPERIENCE EVER IN MY ENTIRE LIFE!!!! Words cannot describe the unbelievable perfection of this place. You MUST BOOK NOW! 100% recommended, guaranteed satisfaction!'
  },
  {
    label: 'Short Generic Feedback',
    hint: 'Low detail pattern',
    text: 'Great product and good value for money. Highly recommend to everyone.'
  }
];

export const ReviewAnalyzer: React.FC<ReviewAnalyzerProps> = ({
  onAnalyze,
  loading,
  error
}) => {
  const [inputText, setInputText] = useState<string>('');
  const [validationError, setValidationError] = useState<string | null>(null);

  const maxLength = 5000;
  const validation = validateReviewText(inputText, maxLength);

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.target.value);
    if (validationError) setValidationError(null);
  };

  const handleClear = () => {
    setInputText('');
    setValidationError(null);
  };

  const handleSelectExample = (exampleText: string) => {
    setInputText(exampleText);
    setValidationError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validation.isValid) {
      setValidationError(validation.error || 'Please enter review text to analyze.');
      return;
    }

    try {
      await onAnalyze(inputText);
    } catch {
      // Handled via props
    }
  };

  return (
    <div className="bg-[#29212B] border border-[#493643] rounded-lg p-6 sm:p-7 shadow-sm">
      <div className="mb-5">
        <h2 className="text-xl font-semibold text-[#FFF7F2]">
          Analyze Review
        </h2>
        <p className="text-xs sm:text-sm text-[#C5B8C1] mt-1 leading-relaxed">
          Submit review text to test for linguistic markers and deceptive writing patterns using the trained NLP model.
        </p>
      </div>

      {/* Preset Test Examples */}
      <div className="mb-4">
        <div className="flex items-center space-x-1.5 text-xs text-[#C5B8C1] mb-2 font-medium">
          <HelpCircle className="w-3.5 h-3.5 text-[#E8A0B8]" />
          <span>Test with sample benchmark reviews:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {BENCHMARK_EXAMPLES.map((ex, idx) => (
            <button
              key={idx}
              type="button"
              disabled={loading}
              onClick={() => handleSelectExample(ex.text)}
              className="text-xs px-3 py-1.5 rounded-md bg-[#201921] hover:bg-[#2e2330] text-[#FFF7F2] border border-[#493643] hover:border-[#E8A0B8] transition-colors disabled:opacity-50 text-left"
              title={ex.hint}
            >
              <span className="font-medium">{ex.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Submission Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="review-textarea" className="sr-only">
            Review text input
          </label>
          <textarea
            id="review-textarea"
            value={inputText}
            onChange={handleTextChange}
            disabled={loading}
            rows={6}
            placeholder="Paste or write customer review text here (e.g., 'We stayed for a weekend conference. Check-in was fast, the room was quiet, though the elevator was slow during checkout...')"
            className={`w-full rounded-md bg-[#201921] border ${
              validationError
                ? 'border-[#E05A68] focus:border-[#E05A68] focus:ring-1 focus:ring-[#E05A68]'
                : 'border-[#493643] focus:border-[#E8A0B8] focus:ring-1 focus:ring-[#E8A0B8]'
            } p-3.5 text-sm text-[#FFF7F2] placeholder:text-[#8A7984] focus:outline-none transition-colors resize-y min-h-[140px] leading-relaxed`}
          />

          {/* Counts & Validation Status */}
          <div className="flex items-center justify-between text-xs text-[#C5B8C1] mt-2 px-1">
            <div className="flex items-center space-x-3">
              <span>{validation.wordCount} words</span>
              <span>•</span>
              <span>{validation.charCount} / {maxLength.toLocaleString()} characters</span>
            </div>
            {validation.charCount > maxLength * 0.9 && (
              <span className="text-[#E0A96D] font-medium">Approaching character limit</span>
            )}
          </div>
        </div>

        {/* Validation or Backend Errors */}
        {(validationError || error) && (
          <div className="flex items-start space-x-2.5 p-3.5 rounded-md bg-[#201921] border border-[#E05A68]/40 text-xs text-[#E05A68]">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <div className="leading-relaxed">
              <strong className="font-semibold block">Notice:</strong>
              {validationError || error}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
          <button
            type="button"
            onClick={handleClear}
            disabled={loading || !inputText}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-1.5 px-4 py-2 rounded-md text-xs font-medium text-[#C5B8C1] hover:text-[#FFF7F2] bg-[#201921] hover:bg-[#2e2330] border border-[#493643] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Clear text</span>
          </button>

          <button
            type="submit"
            disabled={loading || inputText.trim().length === 0}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-2.5 rounded-md text-sm font-semibold text-[#171319] bg-[#E8A0B8] hover:bg-[#F3C4D5] transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
            <span>{loading ? 'Analyzing review...' : 'Analyze Review'}</span>
          </button>
        </div>
      </form>

      {/* Loading feedback */}
      {loading && (
        <div className="mt-4 pt-4 border-t border-[#493643]">
          <LoadingAnimation message="Extracting TF-IDF n-grams and calculating class probability..." />
        </div>
      )}
    </div>
  );
};
