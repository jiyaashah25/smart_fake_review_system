import React from 'react';
import { History, Trash2, ArrowRight, Clock } from 'lucide-react';
import { HistoryItem } from '../types/review';

interface ReviewHistoryProps {
  history: HistoryItem[];
  onSelect: (item: HistoryItem) => void;
  onClear: () => void;
}

export const ReviewHistory: React.FC<ReviewHistoryProps> = ({
  history,
  onSelect,
  onClear
}) => {
  return (
    <div className="bg-[#29212B] border border-[#493643] rounded-lg p-5 sm:p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#493643]">
        <div className="flex items-center space-x-2">
          <History className="w-4 h-4 text-[#E8A0B8]" />
          <h3 className="text-sm font-semibold text-[#FFF7F2]">
            Session Analysis History
          </h3>
          <span className="text-xs text-[#C5B8C1]">
            ({history.length} {history.length === 1 ? 'review' : 'reviews'})
          </span>
        </div>

        {history.length > 0 && (
          <button
            onClick={onClear}
            type="button"
            className="text-xs text-[#C5B8C1] hover:text-[#E05A68] transition-colors flex items-center space-x-1"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear history</span>
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="py-8 text-center text-xs text-[#C5B8C1]">
          <p>No reviews analyzed in this session yet.</p>
          <p className="mt-1 text-[#8A7984]">Analyzed reviews from the current browser session will appear here.</p>
        </div>
      ) : (
        <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
          {history.map(item => {
            const isFake = item.result.label === 1;
            return (
              <div
                key={item.id}
                onClick={() => onSelect(item)}
                className="p-3 rounded-md bg-[#201921] border border-[#493643] hover:border-[#E8A0B8] cursor-pointer transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3 group"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-1">
                    <span
                      className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full border ${
                        isFake
                          ? 'bg-[#171319] text-[#E05A68] border-[#E05A68]/40'
                          : 'bg-[#171319] text-[#52B788] border-[#52B788]/40'
                      }`}
                    >
                      {isFake ? 'Potentially Fake' : 'Likely Genuine'}
                    </span>
                    <span className="text-xs text-[#FFF7F2] font-medium">
                      {item.result.confidence.toFixed(1)}% score
                    </span>
                    <span className="text-[11px] text-[#C5B8C1] flex items-center space-x-1">
                      <Clock className="w-3 h-3 inline" />
                      <span>{item.timestamp}</span>
                    </span>
                  </div>
                  <p className="text-xs text-[#C5B8C1] truncate max-w-xl">
                    {item.text}
                  </p>
                </div>

                <div className="flex items-center text-xs text-[#E8A0B8] font-medium shrink-0 group-hover:underline">
                  <span>Reopen result</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-1 group-hover:translate-x-0.5 transition-transform" />
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
