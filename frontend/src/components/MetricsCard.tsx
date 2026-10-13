import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  description: string;
  icon: LucideIcon;
}

export const MetricsCard: React.FC<MetricsCardProps> = ({
  title,
  value,
  subtitle,
  description,
  icon: Icon
}) => {
  return (
    <div className="rounded-lg bg-[#29212B] border border-[#493643] p-4 flex flex-col justify-between shadow-xs">
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-[#C5B8C1]">
            {title}
          </span>
          <div className="w-7 h-7 rounded-md flex items-center justify-center bg-[#201921] text-[#E8A0B8] border border-[#493643]">
            <Icon className="w-3.5 h-3.5" />
          </div>
        </div>

        <div className="flex items-baseline space-x-1.5">
          <div className="text-2xl font-bold tracking-tight text-[#FFF7F2]">
            {value}
          </div>
          {subtitle && (
            <span className="text-xs text-[#C5B8C1] font-normal">
              {subtitle}
            </span>
          )}
        </div>
      </div>

      <div className="mt-3 pt-2.5 border-t border-[#493643]">
        <p className="text-xs text-[#C5B8C1] leading-relaxed">
          {description}
        </p>
      </div>
    </div>
  );
};
