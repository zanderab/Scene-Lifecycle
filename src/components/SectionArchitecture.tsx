import React from 'react';

export function SectionArchitecture() {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-semibold text-zinc-100 tracking-tight mb-4">Architecture</h2>
        <p className="text-zinc-400 text-lg leading-relaxed mb-8">
          The integration requires a central manager class attached to the Home Assistant <code className="text-zinc-300">hass.data</code> object, coordinating the snapshot process, the generated entities, and the persistent storage.
        </p>
      </div>

      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-8 overflow-x-auto">
        <pre className="text-sm font-mono text-zinc-300 leading-relaxed">
{`+-------------------------------------------------------------+
|  Home Assistant Core                                        |
|                                                             |
|  +--------------------+    +-----------------------------+  |
|  |   Config Flow      |    |      Scene Manager (Core)   |  |
|  | (UI Configuration) |--->| - State Machine (Active?)   |  |
|  +--------------------+    | - Snapshot/Restore Logic    |  |
|                            | - Automation Supression     |  |
|  +--------------------+    |                             |  |
|  | .storage/ JSON     |<---| - Persist Active Scenes     |  |
|  | (Persistence)      |    | - Persist Disabled Automs   |  |
|  +--------------------+    +-----------------------------+  |
|                                 |          |          |     |
|  +--------------------+         v          v          v     |
|  |   Switch Entity    |  +--------+ +----------+ +--------+ |
|  | (scene_mngr.movie) |  | scenes | | entities | | automs | |
|  +--------------------+  +--------+ +----------+ +--------+ |
+-------------------------------------------------------------+`}
        </pre>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-zinc-900/50 p-5 rounded-lg border border-zinc-800">
          <h4 className="text-blue-400 font-medium mb-2">1. Core Manager</h4>
          <p className="text-zinc-500 text-sm">A singleton attached to <code className="bg-zinc-800 px-1 rounded">hass.data[DOMAIN]</code>. Handles the <code className="bg-zinc-800 px-1 rounded">scene.create</code> snapshotting and automation tracking logic.</p>
        </div>
        <div className="bg-zinc-900/50 p-5 rounded-lg border border-zinc-800">
          <h4 className="text-blue-400 font-medium mb-2">2. The Switch</h4>
          <p className="text-zinc-500 text-sm">Every managed scene creates a switch. <code className="bg-zinc-800 px-1 rounded">async_turn_on</code> triggers the snapshot, disables automations, and turns on the HA scene.</p>
        </div>
        <div className="bg-zinc-900/50 p-5 rounded-lg border border-zinc-800">
          <h4 className="text-blue-400 font-medium mb-2">3. Storage</h4>
          <p className="text-zinc-500 text-sm">Uses <code className="bg-zinc-800 px-1 rounded">homeassistant.helpers.storage</code> to ensure if HA crashes, it remembers which automations were temporarily turned off.</p>
        </div>
      </div>
    </div>
  );
}
