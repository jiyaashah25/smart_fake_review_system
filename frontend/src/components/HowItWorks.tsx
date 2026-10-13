import React from 'react';
import {
  FileText,
  Binary,
  Cpu,
  ShieldCheck,
  AlertCircle
} from 'lucide-react';

export const HowItWorks: React.FC = () => {
  const steps = [
    {
      num: '01',
      title: 'Text Preprocessing',
      icon: FileText,
      description:
        'Raw review text is normalized, stripping extraneous markup and tokenizing sentences while retaining critical negation words and punctuation markers.'
    },
    {
      num: '02',
      title: 'TF-IDF Feature Extraction',
      icon: Binary,
      description:
        'Converts cleaned tokens into word and bigram vectors with sublinear term-frequency weighting across a calibrated vocabulary.'
    },
    {
      num: '03',
      title: 'Supervised Classification',
      icon: Cpu,
      description:
        'A pre-trained Logistic Regression model evaluates the high-dimensional feature vector against learned deceptive-opinion decision boundaries.'
    },
    {
      num: '04',
      title: 'Prediction & Explainability',
      icon: ShieldCheck,
      description:
        'Generates the classification verdict alongside confidence scores, stylistic flags (e.g. promotional superlatives), and token attribution weights.'
    }
  ];

  return (
    <div className="bg-[#29212B] border border-[#493643] rounded-lg p-6 sm:p-8 shadow-sm">
      <div className="max-w-2xl mb-8">
        <span className="text-xs font-semibold uppercase tracking-wider text-[#E8A0B8] mb-1 block">
          Machine Learning Pipeline
        </span>
        <h2 className="text-xl sm:text-2xl font-bold text-[#FFF7F2]">
          How ReviewGuard AI Evaluates Reviews
        </h2>
        <p className="text-xs sm:text-sm text-[#C5B8C1] mt-1.5 leading-relaxed">
          An end-to-end natural language processing pipeline translating raw text into calibrated credibility indicators.
        </p>
      </div>

      {/* 4 Steps Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <div
              key={idx}
              className="p-4 rounded-md bg-[#201921] border border-[#493643] flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="w-8 h-8 rounded bg-[#171319] border border-[#493643] text-[#E8A0B8] flex items-center justify-center">
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-mono font-bold text-[#E8A0B8]">
                    {step.num}
                  </span>
                </div>

                <h3 className="text-sm font-semibold text-[#FFF7F2] mb-1.5">
                  {step.title}
                </h3>
                <p className="text-xs text-[#C5B8C1] leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Methodology Note */}
      <div className="mt-6 pt-5 border-t border-[#493643] flex items-start space-x-2.5 text-xs text-[#C5B8C1] leading-relaxed">
        <AlertCircle className="w-4 h-4 text-[#E0A96D] shrink-0 mt-0.5" />
        <p>
          <strong className="text-[#FFF7F2] font-medium">Methodology Note: </strong>
          The model assesses statistical and lexical patterns from the benchmark corpus.
          It does not access external merchant transaction histories or physical proof of purchase.
          All predictions reflect statistical likelihood, not legal proof of deception.
        </p>
      </div>
    </div>
  );
};
