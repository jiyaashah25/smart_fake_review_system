import React from 'react';
import { Shield } from 'lucide-react';
import { ViewType } from './Navbar';

interface FooterProps {
  onNavigate: (view: ViewType) => void;
}

export const Footer: React.FC<FooterProps> = ({ onNavigate }) => {
  return (
    <footer className="border-t border-[#493643] bg-[#211A22] text-[#C5B8C1] py-10 mt-16 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Info */}
          <div className="md:col-span-2 space-y-2.5">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded bg-[#E8A0B8] flex items-center justify-center text-[#171319]">
                <Shield className="w-3.5 h-3.5 font-bold" />
              </div>
              <span className="text-sm font-semibold text-[#FFF7F2]">
                ReviewGuard AI
              </span>
            </div>
            <p className="text-xs text-[#C5B8C1] max-w-sm leading-relaxed">
              A deceptive review detection and text analysis system built with Natural Language Processing and supervised Machine Learning.
            </p>
            <div className="text-[11px] text-[#C5B8C1]/80">
              Trained on the Ott et al. Deceptive Opinion Spam benchmark dataset.
            </div>
          </div>

          {/* Navigation Links */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#FFF7F2] mb-2.5">
              Navigation
            </h4>
            <ul className="space-y-1.5 text-xs">
              <li>
                <button
                  type="button"
                  onClick={() => onNavigate('overview')}
                  className="hover:text-[#E8A0B8] transition-colors"
                >
                  Overview
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => onNavigate('analyzer')}
                  className="hover:text-[#E8A0B8] transition-colors"
                >
                  Analyze Review
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => onNavigate('performance')}
                  className="hover:text-[#E8A0B8] transition-colors"
                >
                  Model Performance
                </button>
              </li>
            </ul>
          </div>

          {/* Technical Specifications */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[#FFF7F2] mb-2.5">
              Technical Stack
            </h4>
            <ul className="space-y-1 text-xs text-[#C5B8C1]">
              <li>• scikit-learn & TF-IDF Vectorizer</li>
              <li>• Calibrated Logistic Regression</li>
              <li>• FastAPI Python REST Backend</li>
              <li>• React 18, TypeScript & Vite</li>
              <li>• Dark Blush Pink & Cream Palette</li>
            </ul>
          </div>
        </div>

        {/* Mandatory Model Disclaimer */}
        <div className="pt-6 border-t border-[#493643] text-center space-y-1.5">
          <p className="text-[11px] text-[#C5B8C1] max-w-3xl mx-auto leading-relaxed">
            <strong>Disclaimer: </strong>
            ReviewGuard AI provides automated predictions based on statistical text analysis.
            Results are indicative patterns and should not be considered definitive proof of review fraud.
          </p>
          <div className="text-[11px] text-[#8A7984]">
            Academic machine learning demonstration & project viva evaluation.
          </div>
        </div>
      </div>
    </footer>
  );
};
