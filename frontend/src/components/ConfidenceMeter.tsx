import React from 'react';
import { CheckCircle2, AlertTriangle, HelpCircle } from 'lucide-react';

interface ConfidenceMeterProps {
  confidence: number;
  level: 'high' | 'medium' | 'low';
  label: 0 | 1;
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({ confidence, level, label }) => {
  const isFake = label === 1;

  const getBarColor = () => {
    if (level === 'low') return 'bg-[#E0A96D]';
    if (isFake) return 'bg-[#E05A68]';
    return 'bg-[#52B788]';
  };

  const getBadgeStyle = () => {
    if (level === 'low') {
      return 'bg-[#171319] text-[#E0A96D] border-[#E0A96D]/40';
    }
    if (isFake) {
      return 'bg-[#171319] text-[#E05A68] border-[#E05A68]/40';
    }
    return 'bg-[#171319] text-[#52B788] border-[#52B788]/40';
  };

  const getLevelLabel = () => {
    switch (level) {
      case 'high':
        return 'High confidence';
      case 'medium':
        return 'Moderate confidence';
      case 'low':
      default:
        return 'Borderline score';
    }
  };

  return (
    <div className="bg-[#201921] border border-[#493643] rounded-lg p-5">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          {level === 'low' ? (
            <HelpCircle className="w-4 h-4 text-[#E0A96D]" />
          ) : isFake ? (
            <AlertTriangle className="w-4 h-4 text-[#E05A68]" />
          ) : (
            <CheckCircle2 className="w-4 h-4 text-[#52B788]" />
          )}
          <span className="text-xs font-semibold uppercase tracking-wider text-[#B87591]">
            Model Confidence
          </span>
        </div>
        <span className={`text-xs px-2.5 py-0.5 rounded-full border font-medium ${getBadgeStyle()}`}>
          {getLevelLabel()}
        </span>
      </div>

      <div className="space-y-2.5">
        <div className="flex justify-between items-baseline text-sm">
          <span className="text-[#C5B8C1] font-normal">Calibrated probability</span>
          <span className="text-lg font-semibold tracking-tight text-[#FFF7F2]">
            {confidence.toFixed(1)}%
          </span>
        </div>

        {/* Clean, Restrained Horizontal Progress Bar */}
        <div className="w-full bg-[#171319] rounded-full h-2.5 overflow-hidden border border-[#493643]">
          <div
            className={`h-full rounded-full ${getBarColor()} transition-all duration-500 ease-out shadow-xs`}
            style={{ width: `${Math.min(Math.max(confidence, 5), 100)}%` }}
          />
        </div>

        <p className="text-xs text-[#C5B8C1] leading-relaxed pt-1">
          {level === 'low'
            ? 'The review sits near the model decision boundary. Stylistic signals present mixed characteristics.'
            : isFake
            ? `The model identified vocabulary and phrasing resembling deceptive training samples at ${confidence.toFixed(1)}% confidence.`
            : `The text exhibits balanced lexical and experiential patterns typical of genuine reviews at ${confidence.toFixed(1)}% confidence.`}
        </p>
      </div>
    </div>
  );
};
