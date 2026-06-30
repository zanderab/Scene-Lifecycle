import React from 'react';
import { CheckCircle2, AlertTriangle, Info } from 'lucide-react';

export function SectionCritique() {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-semibold text-zinc-100 tracking-tight mb-4">Concept Critique</h2>
        <p className="text-zinc-400 text-lg leading-relaxed">
          The concept hits a very real, highly requested pain point in the Home Assistant ecosystem. The "snapshot, restore, and lock" pattern is something almost every power user builds manually with scripts and helpers. Productizing this is an excellent idea.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <CheckCircle2 className="text-emerald-400" size={24} />
            <h3 className="text-xl font-medium text-zinc-200">Strengths</h3>
          </div>
          <ul className="space-y-3 text-zinc-400">
            <li className="flex items-start gap-2">
              <span className="text-emerald-500/50 mt-1">•</span>
              <span><strong>Addresses a true gap:</strong> The HA scene engine has always lacked state tracking and rollback capabilities.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-500/50 mt-1">•</span>
              <span><strong>UX focused:</strong> Moving away from YAML and input_booleans to a config flow drastically lowers the barrier to entry.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-500/50 mt-1">•</span>
              <span><strong>HACS distribution:</strong> This absolutely needs to be a custom component. Blueprints simply do not have the APIs to manipulate or scan other automations cleanly.</span>
            </li>
          </ul>
        </div>

        <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <AlertTriangle className="text-amber-400" size={24} />
            <h3 className="text-xl font-medium text-zinc-200">Technical Challenges</h3>
          </div>
          <ul className="space-y-3 text-zinc-400">
            <li className="flex items-start gap-2">
              <span className="text-amber-500/50 mt-1">•</span>
              <span><strong>Automation Suspension:</strong> Modifying <code className="text-amber-200/80 bg-amber-500/10 px-1 py-0.5 rounded">automation.turn_off</code> is viable, but risky. If HA crashes or the user reloads while a scene is active, you must ensure those automations aren't permanently disabled. You will need a robust restore-on-boot mechanism using HA's <code className="text-amber-200/80 bg-amber-500/10 px-1 py-0.5 rounded">.storage</code>.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-500/50 mt-1">•</span>
              <span><strong>Condition Injection (Option B):</strong> Programmatically injecting conditions into existing automations is an anti-pattern in HA. The config is often owned by YAML or the UI editor, and rewriting their configuration dynamically is brittle and dangerous. Stick to turning them off (Option A).</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-500/50 mt-1">•</span>
              <span><strong>Snapshot Fidelity:</strong> <code className="text-amber-200/80 bg-amber-500/10 px-1 py-0.5 rounded">scene.create</code> works well for lights, but can be finicky with media players or custom climate entities. You may need to sanitize which attributes are saved, or limit managed entities strictly to lights and switches initially.</span>
            </li>
          </ul>
        </div>
      </div>

      <div className="bg-blue-900/20 border border-blue-800/50 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-3">
          <Info className="text-blue-400" size={24} />
          <h3 className="text-lg font-medium text-blue-100">The "Manual Override" Problem</h3>
        </div>
        <p className="text-blue-200/80 text-sm leading-relaxed">
          Consider state invalidation. If a user activates "Movie Mode", but then manually goes to the dashboard and turns the ceiling light off, is the scene still "Active"? You will need to decide if your state machine strictly enforces the scene (auto-reverting manual changes), gracefully degrades (shows as "Mixed" state), or simply ignores it until deactivated. For v1, ignoring manual changes is the safest route.
        </p>
      </div>
    </div>
  );
}
