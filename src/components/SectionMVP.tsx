import React from 'react';
import { Target, ArrowRight } from 'lucide-react';

export function SectionMVP() {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-semibold text-zinc-100 tracking-tight mb-4">MVP Scope Cut</h2>
        <p className="text-zinc-400 text-lg leading-relaxed">
          To launch a successful v0.1 that proves the concept without getting bogged down in edge cases, here is the recommended feature division.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-4">
          <div className="flex items-center gap-3 border-b border-emerald-900 pb-2">
            <Target className="text-emerald-400" size={24} />
            <h3 className="text-xl font-medium text-emerald-100">Must Have (v0.1)</h3>
          </div>
          <ul className="space-y-4">
            <li className="bg-zinc-900 border border-zinc-800 rounded-lg p-4">
              <h4 className="text-zinc-200 font-medium mb-1">UI Config Flow</h4>
              <p className="text-zinc-500 text-sm">Select an existing HA Scene from a dropdown to "Manage" it.</p>
            </li>
            <li className="bg-zinc-900 border border-zinc-800 rounded-lg p-4">
              <h4 className="text-zinc-200 font-medium mb-1">Entity Selection</h4>
              <p className="text-zinc-500 text-sm">Manually select entities to snapshot. (Deferring auto-detection of entities from scenes, as parsing scene states can be complex).</p>
            </li>
            <li className="bg-zinc-900 border border-zinc-800 rounded-lg p-4">
              <h4 className="text-zinc-200 font-medium mb-1">Automation Suspension (Option A)</h4>
              <p className="text-zinc-500 text-sm">Disable selected automations via <code className="text-zinc-400 bg-zinc-800 px-1 py-0.5 rounded">automation.turn_off</code>.</p>
            </li>
            <li className="bg-zinc-900 border border-zinc-800 rounded-lg p-4">
              <h4 className="text-zinc-200 font-medium mb-1">Switch Entity Generation</h4>
              <p className="text-zinc-500 text-sm">Generate a <code className="text-zinc-400 bg-zinc-800 px-1 py-0.5 rounded">switch.scene_mngr_movie</code> for easy UI integration and state tracking.</p>
            </li>
            <li className="bg-zinc-900 border border-zinc-800 rounded-lg p-4">
              <h4 className="text-zinc-200 font-medium mb-1">Persistent State (.storage)</h4>
              <p className="text-zinc-500 text-sm">Save active scenes and disabled automations to disk to survive restarts.</p>
            </li>
          </ul>
        </div>

        <div className="space-y-4">
          <div className="flex items-center gap-3 border-b border-zinc-800 pb-2">
            <ArrowRight className="text-zinc-500" size={24} />
            <h3 className="text-xl font-medium text-zinc-400">Defer to v1.0+</h3>
          </div>
          <ul className="space-y-4">
            <li className="bg-zinc-900/40 border border-zinc-800/50 rounded-lg p-4 opacity-80">
              <h4 className="text-zinc-300 font-medium mb-1">Condition Injection (Option B)</h4>
              <p className="text-zinc-500 text-sm">Modifying automation YAML/JSON programmatically is dangerous. Drop it for now.</p>
            </li>
            <li className="bg-zinc-900/40 border border-zinc-800/50 rounded-lg p-4 opacity-80">
              <h4 className="text-zinc-300 font-medium mb-1">Auto-detecting Scene Entities</h4>
              <p className="text-zinc-500 text-sm">HA scenes are essentially just dictionaries of target states. Reverse-engineering them reliably across all integrations is a rabbit hole.</p>
            </li>
            <li className="bg-zinc-900/40 border border-zinc-800/50 rounded-lg p-4 opacity-80">
              <h4 className="text-zinc-300 font-medium mb-1">Custom Lovelace Cards</h4>
              <p className="text-zinc-500 text-sm">Rely on standard Mushroom or Tile cards pointed at your generated Switch entity for the MVP.</p>
            </li>
            <li className="bg-zinc-900/40 border border-zinc-800/50 rounded-lg p-4 opacity-80">
              <h4 className="text-zinc-300 font-medium mb-1">Scene Priorities / Queuing</h4>
              <p className="text-zinc-500 text-sm">Complex logic that requires a robust state machine. Stick to simple toggle behaviors first.</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
