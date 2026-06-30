import React from 'react';
import { Search, Code2 } from 'lucide-react';

export function SectionAPI() {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-semibold text-zinc-100 tracking-tight mb-4">HA API Discovery</h2>
        <p className="text-zinc-400 text-lg leading-relaxed">
          How to interact with Home Assistant internals to find and suppress automations.
        </p>
      </div>

      <div className="space-y-6">
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Search className="text-blue-400" size={24} />
            <h3 className="text-xl font-medium text-zinc-200">Discovering Automations</h3>
          </div>
          <p className="text-zinc-400 text-sm leading-relaxed mb-4">
            To present a list of automations to the user that they might want to suppress, you can access the state machine directly. Automations expose their entity targets in their attributes.
          </p>
          <div className="bg-zinc-950 rounded-lg p-4 font-mono text-sm text-zinc-300 overflow-x-auto border border-zinc-800">
            <code>
              <span className="text-emerald-400"># Fetch all automations</span><br/>
              automations = hass.states.async_all(<span className="text-amber-300">'automation'</span>)<br/><br/>
              <span className="text-emerald-400"># Filter by related entities</span><br/>
              <span className="text-purple-400">for</span> auto <span className="text-purple-400">in</span> automations:<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;entity_id = auto.attributes.get(<span className="text-amber-300">'entity_id'</span>, [])<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-emerald-400"># Compare with managed scene entities</span>
            </code>
          </div>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Code2 className="text-amber-400" size={24} />
            <h3 className="text-xl font-medium text-zinc-200">Snapshotting</h3>
          </div>
          <p className="text-zinc-400 text-sm leading-relaxed mb-4">
            Do not build your own state saver. Use the built-in <code className="bg-zinc-800 px-1 rounded text-zinc-300">scene.create</code> service. It handles the nuances of storing attributes (like color_temp, brightness) in a temporary scene object in memory.
          </p>
          <div className="bg-zinc-950 rounded-lg p-4 font-mono text-sm text-zinc-300 overflow-x-auto border border-zinc-800">
            <code>
              <span className="text-emerald-400"># Create temporary snapshot</span><br/>
              <span className="text-purple-400">await</span> hass.services.async_call(<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-amber-300">'scene'</span>, <span className="text-amber-300">'create'</span>,<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;{'{'}<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-amber-300">'scene_id'</span>: <span className="text-amber-300">'snapshot_movie_mode'</span>,<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-amber-300">'snapshot_entities'</span>: managed_entity_list<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;{'}'}<br/>
              )<br/><br/>
              <span className="text-emerald-400"># Restore later via scene.turn_on</span>
            </code>
          </div>
        </div>
      </div>
    </div>
  );
}
