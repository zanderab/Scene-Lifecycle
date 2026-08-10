import React from 'react';
import { Folder, File, FileCode } from 'lucide-react';

export function SectionStructure() {
  const TreeItem = ({ name, type, desc, depth = 0 }: { name: string, type: 'folder' | 'py' | 'json', desc?: string, depth?: number }) => (
    <div className="flex items-center gap-3 py-2 border-b border-zinc-800/50 last:border-0 hover:bg-zinc-800/30 px-4 transition-colors" style={{ paddingLeft: `${depth * 1.5 + 1}rem` }}>
      {type === 'folder' ? <Folder size={18} className="text-blue-400" /> : type === 'json' ? <File size={18} className="text-amber-400" /> : <FileCode size={18} className="text-emerald-400" />}
      <span className="font-mono text-sm text-zinc-300 w-48 shrink-0">{name}</span>
      {desc && <span className="text-zinc-500 text-sm">{desc}</span>}
    </div>
  );

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-semibold text-zinc-100 tracking-tight mb-4">File Structure</h2>
        <p className="text-zinc-400 text-lg leading-relaxed">
          The minimum required Python project layout for a Home Assistant custom component implementing a Config Flow.
        </p>
      </div>

      <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden shadow-2xl">
        <div className="bg-zinc-950 px-4 py-3 border-b border-zinc-800 flex items-center gap-2">
          <Folder size={18} className="text-blue-500" />
          <span className="font-mono text-sm text-zinc-200 font-medium">custom_components/scene_manager/</span>
        </div>
        
        <div className="py-2">
          <TreeItem depth={1} type="py" name="__init__.py" desc="Setup logic, async_setup_entry, service registration" />
          <TreeItem depth={1} type="json" name="manifest.json" desc="Domain, version, IoT class, requirements" />
          <TreeItem depth={1} type="py" name="const.py" desc="DOMAIN, CONF_*, constants" />
          <TreeItem depth={1} type="py" name="config_flow.py" desc="UI setup flow (step_user), options flow" />
          <TreeItem depth={1} type="py" name="switch.py" desc="Switch entity logic (turn_on, turn_off)" />
          <TreeItem depth={1} type="py" name="manager.py" desc="Core state machine, snapshot logic, HA API wrapper" />
          <TreeItem depth={1} type="py" name="storage.py" desc="Helpers for HA .storage persistence" />
          <TreeItem depth={1} type="folder" name="translations/" />
          <TreeItem depth={2} type="json" name="en.json" desc="Config flow UI translation strings" />
        </div>
      </div>
      
      <div className="bg-emerald-900/10 border border-emerald-900/30 rounded-xl p-6">
        <h3 className="text-emerald-400 font-medium mb-2">Key Dependency</h3>
        <p className="text-zinc-400 text-sm leading-relaxed">
          Ensure your <code className="text-zinc-300 font-mono bg-zinc-800 px-1 rounded">manifest.json</code> defines <code className="text-zinc-300 font-mono bg-zinc-800 px-1 rounded">"dependencies": ["scene", "automation", "switch"]</code> so HA loads those components before yours, guaranteeing their service calls are available.
        </p>
      </div>
    </div>
  );
}
