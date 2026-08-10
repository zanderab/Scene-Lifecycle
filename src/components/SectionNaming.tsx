import React from 'react';
import { PenTool, Check } from 'lucide-react';

export function SectionNaming() {
  const names = [
    { name: "Scene Lifecycle", desc: "Accurate, implies a start, duration, and end.", vote: "best" },
    { name: "Transient Scenes", desc: "Describes exactly what they are—temporary states.", vote: "good" },
    { name: "Scene Locks", desc: "Focuses on the automation suppression aspect.", vote: "good" },
    { name: "Scene Manager", desc: "A bit generic, might imply a UI editor for scenes.", vote: "neutral" },
    { name: "Smart Scenes", desc: "Too generic, sounds like a marketing term.", vote: "bad" }
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-semibold text-zinc-100 tracking-tight mb-4">Naming Suggestions</h2>
        <p className="text-zinc-400 text-lg leading-relaxed">
          "Scene Manager" is functional, but slightly generic. It implies a tool used to create or edit the YAML of scenes. Here are some alternatives focused on the <em>behavior</em> of the integration.
        </p>
      </div>

      <div className="grid gap-3">
        {names.map((n) => (
          <div key={n.name} className="bg-zinc-900 border border-zinc-800 rounded-lg p-5 flex items-center justify-between group hover:border-zinc-700 transition-colors">
            <div>
              <h3 className="text-lg font-medium text-zinc-200 mb-1 flex items-center gap-2">
                {n.name}
                {n.vote === 'best' && <span className="bg-emerald-500/10 text-emerald-400 text-[10px] uppercase font-bold px-2 py-0.5 rounded-full">Top Pick</span>}
              </h3>
              <p className="text-zinc-500 text-sm">{n.desc}</p>
            </div>
            {n.vote === 'best' && <Check className="text-emerald-500" />}
          </div>
        ))}
      </div>
      
      <div className="bg-blue-900/10 border border-blue-900/30 rounded-xl p-6 mt-8">
        <p className="text-zinc-300 leading-relaxed">
          <strong>Recommendation:</strong> Use <strong className="text-blue-400">"Scene Lifecycle"</strong>. It perfectly describes the problem you are solving (managing what happens before, during, and after a scene is active).
        </p>
      </div>
    </div>
  );
}
