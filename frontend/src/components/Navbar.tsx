import React, { useState } from 'react';
import { Shield, Menu, X } from 'lucide-react';

export type ViewType = 'overview' | 'analyzer' | 'performance';

interface NavbarProps {
  onNavigate: (view: ViewType) => void;
  currentView: ViewType;
  isBackendHealthy: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  onNavigate,
  currentView,
  isBackendHealthy,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems: { id: ViewType; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'analyzer', label: 'Analyze Review' },
    { id: 'performance', label: 'Model Performance' },
  ];

  const handleItemClick = (id: ViewType) => {
    onNavigate(id);
    setMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-40 w-full bg-[#171319]/95 backdrop-blur-md border-b border-[#493643] transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <button
          type="button"
          onClick={() => handleItemClick('overview')}
          className="flex items-center space-x-2.5 text-left focus:outline-none group"
        >
          <div className="w-8 h-8 rounded-md bg-[#E8A0B8] text-[#171319] flex items-center justify-center shrink-0 font-bold shadow-xs">
            <Shield className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="text-base font-semibold tracking-tight text-[#FFF7F2]">
                ReviewGuard
              </span>
              <span className="text-[11px] font-medium px-1.5 py-0.5 rounded bg-[#29212B] text-[#E8A0B8] border border-[#493643]">
                AI
              </span>
            </div>
            <span className="text-[10px] text-[#C5B8C1] block -mt-0.5 font-normal">
              Deceptive Review Detection
            </span>
          </div>
        </button>

        {/* Desktop Nav Links */}
        <nav className="hidden md:flex items-center space-x-1">
          {navItems.map((item) => {
            const isActive = currentView === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => handleItemClick(item.id)}
                className={`px-3.5 py-1.5 rounded-md text-sm transition-colors ${
                  isActive
                    ? 'text-[#171319] bg-[#E8A0B8] font-semibold shadow-xs'
                    : 'text-[#FFF7F2] hover:text-[#E8A0B8] hover:bg-[#211A22] font-normal'
                }`}
              >
                {item.label}
              </button>
            );
          })}
        </nav>

        {/* Right Status & Action */}
        <div className="hidden sm:flex items-center space-x-3">
          <div
            className={`flex items-center space-x-1.5 text-xs px-2.5 py-1 rounded-full border border-[#493643] ${
              isBackendHealthy
                ? 'bg-[#211A22] text-[#52B788]'
                : 'bg-[#211A22] text-[#E05A68]'
            }`}
            title={isBackendHealthy ? 'FastAPI & ML model online' : 'Backend offline'}
          >
            {isBackendHealthy ? (
              <span className="w-1.5 h-1.5 rounded-full bg-[#52B788] animate-pulse" />
            ) : (
              <span className="w-1.5 h-1.5 rounded-full bg-[#E05A68]" />
            )}
            <span className="font-medium">
              {isBackendHealthy ? 'Model Online' : 'Model Offline'}
            </span>
          </div>

          <button
            type="button"
            onClick={() => handleItemClick('analyzer')}
            className="px-3.5 py-1.5 rounded-md text-xs font-semibold text-[#171319] bg-[#E8A0B8] hover:bg-[#F3C4D5] transition-colors shadow-xs"
          >
            Analyze Review
          </button>
        </div>

        {/* Mobile Hamburger Button */}
        <div className="flex md:hidden items-center space-x-2">
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-md text-[#C5B8C1] hover:text-[#FFF7F2] hover:bg-[#211A22] focus:outline-none"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-[#493643] bg-[#211A22] px-4 pt-3 pb-4 space-y-1">
          {navItems.map((item) => {
            const isActive = currentView === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => handleItemClick(item.id)}
                className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                  isActive
                    ? 'text-[#171319] bg-[#E8A0B8] font-semibold'
                    : 'text-[#FFF7F2] hover:text-[#E8A0B8] hover:bg-[#29212B]'
                }`}
              >
                {item.label}
              </button>
            );
          })}

          <div className="pt-3 border-t border-[#493643] flex items-center justify-between">
            <span className="text-xs text-[#C5B8C1]">
              Status: {isBackendHealthy ? 'Model Online' : 'Model Offline'}
            </span>
            <button
              type="button"
              onClick={() => handleItemClick('analyzer')}
              className="px-3 py-1.5 rounded-md text-xs font-semibold text-[#171319] bg-[#E8A0B8]"
            >
              Analyze Review
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
