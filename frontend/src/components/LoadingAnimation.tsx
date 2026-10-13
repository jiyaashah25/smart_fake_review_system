import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const LoadingAnimation: React.FC<LoadingProps> = ({
  message = 'Processing review with NLP model...',
  size = 'md'
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 space-y-3">
      <Loader2 className={`${sizeClasses[size]} text-[#E8A0B8] animate-spin`} />
      {message && (
        <p className="text-xs font-medium text-[#C5B8C1] text-center">
          {message}
        </p>
      )}
    </div>
  );
};
