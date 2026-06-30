import React from 'react';
import { Section, sections } from '../types';
import { cn } from '../lib/utils';
import { Layers } from 'lucide-react';

interface SidebarProps {
  activeSection: string;
  onSelect: (id: string) => void;
}

export function Sidebar({ activeSection, onSelect }: SidebarProps) {
  return (
    <div className="w-64 bg-zinc-900 border-r border-zinc-800 h-screen flex flex-col fixed left-0 top-0 overflow-y-auto">
      <div className="p-6">
        <div className="flex items-center gap-3 text-zinc-100 mb-2">
          <div className="p-2 bg-blue-600/20 rounded-lg text-blue-400">
            <Layers size={24} />
          </div>
          <h1 className="font-semibold text-lg tracking-tight">Scene Manager</h1>
        </div>
        <p className="text-zinc-500 text-xs font-medium uppercase tracking-wider mb-8">Design Document</p>
        
        <nav className="space-y-1">
          {sections.map((section) => (
            <button
              key={section.id}
              onClick={() => onSelect(section.id)}
              className={cn(
                "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-left",
                activeSection === section.id
                  ? "bg-zinc-800 text-zinc-100"
                  : "text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200"
              )}
            >
              <section.icon size={18} className={activeSection === section.id ? "text-blue-400" : "text-zinc-500"} />
              {section.title}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
}
