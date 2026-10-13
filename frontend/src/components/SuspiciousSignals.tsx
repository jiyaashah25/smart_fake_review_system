import React from 'react';
import {
  AlertTriangle,
  Info,
  CheckCircle2,
  TrendingUp,
  TrendingDown
} from 'lucide-react';
import { TextSignal, InfluentialTerms } from '../types/review';

interface SuspiciousSignalsProps {
  signals: TextSignal[];
  influentialTerms: InfluentialTerms;
}

export const SuspiciousSignals: React.FC<SuspiciousSignalsProps> = ({
  signals,
  influentialTerms
}) => {
  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-[#29212B] text-[#E05A68] border border-[#E05A68]/40';
      case 'medium':
        return 'bg-[#29212B] text-[#E0A96D] border border-[#E0A96D]/40';
      case 'low':
        return 'bg-[#29212B] text-[#C5B8C1] border border-[#493643]';
      default:
        return 'bg-[#29212B] text-[#52B788] border border-[#52B788]/40';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return <AlertTriangle className="w-4 h-4 text-[#E05A68] shrink-0 mt-0.5" />;
      case 'medium':
        return <AlertTriangle className="w-4 h-4 text-[#E0A96D] shrink-0 mt-0.5" />;
      case 'low':
        return <Info className="w-4 h-4 text-[#C5B8C1] shrink-0 mt-0.5" />;
      default:
        return <CheckCircle2 className="w-4 h-4 text-[#52B788] shrink-0 mt-0.5" />;
    }
  };

  const hasInfluential =
    (influentialTerms.fake_influential && influentialTerms.fake_influential.length > 0) ||
    (influentialTerms.genuine_influential && influentialTerms.genuine_influential.length > 0);

  return (
    <div className="space-y-6">
      {/* Qualitative Stylistic Signals */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-[#B87591]">
            Stylistic & Structural Signals
          </h4>
          <span className="text-xs text-[#C5B8C1]">
            {signals.length} {signals.length === 1 ? 'signal' : 'signals'} evaluated
          </span>
        </div>

        <div className="grid grid-cols-1 gap-2.5">
          {signals.map((signal, idx) => (
            <div
              key={idx}
              className="flex items-start space-x-3 p-3 rounded-md bg-[#171319] border border-[#493643]"
            >
              {getSeverityIcon(signal.severity)}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-medium text-[#FFF7F2]">
                    {signal.title}
                  </span>
                  <span
                    className={`text-[10px] uppercase font-semibold tracking-wider px-2 py-0.5 rounded-full ${getSeverityBadge(
                      signal.severity
                    )}`}
                  >
                    {signal.severity}
                  </span>
                </div>
                <p className="text-xs text-[#C5B8C1] mt-1 leading-relaxed">
                  {signal.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Influential Terms (TF-IDF Attribution) */}
      {hasInfluential && (
        <div className="pt-4 border-t border-[#493643]">
          <div className="mb-3">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#B87591]">
              Influential Words & Phrases (TF-IDF Attribution)
            </h4>
            <p className="text-xs text-[#C5B8C1] mt-0.5">
              Specific terms that carried high weight toward the classification score.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* Terms pushing toward fake */}
            {influentialTerms.fake_influential && influentialTerms.fake_influential.length > 0 && (
              <div className="p-3 rounded-md bg-[#171319] border border-[#E05A68]/30">
                <div className="flex items-center space-x-1.5 text-xs font-medium text-[#E05A68] mb-2">
                  <TrendingUp className="w-3.5 h-3.5" />
                  <span>Terms associated with deceptive reviews</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {influentialTerms.fake_influential.map((term, i) => (
                    <span
                      key={i}
                      className="inline-flex items-center text-xs px-2 py-0.5 rounded bg-[#29212B] border border-[#E05A68]/40 text-[#E05A68] font-mono"
                      title={`Linear model weight: +${term.contribution.toFixed(2)}`}
                    >
                      "{term.term}"
                      <span className="text-[10px] text-[#E05A68] ml-1 font-sans">
                        +{term.contribution.toFixed(2)}
                      </span>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Terms pushing toward genuine */}
            {influentialTerms.genuine_influential && influentialTerms.genuine_influential.length > 0 && (
              <div className="p-3 rounded-md bg-[#171319] border border-[#52B788]/30">
                <div className="flex items-center space-x-1.5 text-xs font-medium text-[#52B788] mb-2">
                  <TrendingDown className="w-3.5 h-3.5" />
                  <span>Terms associated with genuine reviews</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {influentialTerms.genuine_influential.map((term, i) => (
                    <span
                      key={i}
                      className="inline-flex items-center text-xs px-2 py-0.5 rounded bg-[#29212B] border border-[#52B788]/40 text-[#52B788] font-mono"
                      title={`Linear model weight: ${term.contribution.toFixed(2)}`}
                    >
                      "{term.term}"
                      <span className="text-[10px] text-[#52B788] ml-1 font-sans">
                        {term.contribution.toFixed(2)}
                      </span>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
