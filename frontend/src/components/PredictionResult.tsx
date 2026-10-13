import React from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  FileText,
  Clock,
  Info
} from 'lucide-react';
import { PredictionResultData } from '../types/review';
import { ConfidenceMeter } from './ConfidenceMeter';
import { SuspiciousSignals } from './SuspiciousSignals';

interface PredictionResultProps {
  data: PredictionResultData;
}

export const PredictionResult: React.FC<PredictionResultProps> = ({ data }) => {
  const isFake = data.label === 1;

  return (
    <div
      className={`rounded-lg border p-6 sm:p-7 bg-[#29212B] shadow-sm transition-colors ${
        isFake ? 'border-[#E05A68]/40' : 'border-[#52B788]/40'
      }`}
    >
      {/* Top Banner / Verdict */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-[#493643]">
        <div className="flex items-center space-x-3.5">
          <div
            className={`w-11 h-11 rounded-md flex items-center justify-center shrink-0 border ${
              isFake
                ? 'bg-[#201921] text-[#E05A68] border-[#E05A68]/40'
                : 'bg-[#201921] text-[#52B788] border-[#52B788]/40'
            }`}
          >
            {isFake ? (
              <AlertTriangle className="w-5 h-5" />
            ) : (
              <CheckCircle2 className="w-5 h-5" />
            )}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span
                className={`text-[11px] font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${
                  isFake
                    ? 'bg-[#201921] text-[#E05A68] border-[#E05A68]/40'
                    : 'bg-[#201921] text-[#52B788] border-[#52B788]/40'
                }`}
              >
                {isFake ? 'Potentially Fake' : 'Likely Genuine'}
              </span>
              <span className="text-xs text-[#C5B8C1] flex items-center space-x-1">
                <Clock className="w-3 h-3 inline" />
                <span>Analyzed just now</span>
              </span>
            </div>
            <h3 className="text-xl sm:text-2xl font-semibold text-[#FFF7F2] mt-1 tracking-tight">
              {data.label_name}
            </h3>
          </div>
        </div>

        {/* Model Spec Badge */}
        <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center text-xs text-[#C5B8C1] bg-[#201921] px-3 py-2 rounded-md border border-[#493643]">
          <span className="text-[#FFF7F2] font-medium">
            {data.model_name}
          </span>
          <span className="text-[11px] text-[#C5B8C1]">TF-IDF N-Gram Vectorizer</span>
        </div>
      </div>

      {/* Grid: Confidence & Text Statistics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 my-5">
        <div className="lg:col-span-2">
          <ConfidenceMeter
            confidence={data.confidence}
            level={data.confidence_level}
            label={data.label}
          />
        </div>

        <div className="bg-[#201921] border border-[#493643] rounded-lg p-4 sm:p-5 flex flex-col justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-[#B87591] flex items-center space-x-1.5 mb-3">
              <FileText className="w-3.5 h-3.5 text-[#E8A0B8]" />
              <span>Review Characteristics</span>
            </span>
            <div className="grid grid-cols-2 gap-2.5 text-center">
              <div className="p-2.5 rounded-md bg-[#29212B] border border-[#493643]">
                <div className="text-base font-semibold text-[#FFF7F2]">{data.word_count}</div>
                <div className="text-[11px] text-[#C5B8C1] uppercase font-medium">Words</div>
              </div>
              <div className="p-2.5 rounded-md bg-[#29212B] border border-[#493643]">
                <div className="text-base font-semibold text-[#FFF7F2]">{data.review_length}</div>
                <div className="text-[11px] text-[#C5B8C1] uppercase font-medium">Characters</div>
              </div>
            </div>
          </div>

          <div className="text-xs text-[#C5B8C1] pt-3 border-t border-[#493643] mt-3 leading-relaxed">
            {data.explanation_summary}
          </div>
        </div>
      </div>

      {/* Signals & Explainability */}
      <div className="bg-[#201921] border border-[#493643] rounded-lg p-5 mb-5">
        <SuspiciousSignals
          signals={data.signals}
          influentialTerms={data.influential_terms}
        />
      </div>

      {/* Required Visible Disclaimer */}
      <div className="flex items-start space-x-2.5 p-3.5 rounded-md bg-[#201921] border border-[#493643] text-xs text-[#C5B8C1] leading-relaxed">
        <Info className="w-4 h-4 text-[#E8A0B8] shrink-0 mt-0.5" />
        <p>
          <strong className="text-[#FFF7F2] font-semibold">Model Disclaimer: </strong>
          {data.disclaimer}
        </p>
      </div>
    </div>
  );
};
