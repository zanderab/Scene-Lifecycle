import React from 'react';

export default function App() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-300 flex items-center justify-center font-mono p-6">
      <div className="max-w-lg text-center space-y-6">
        <div className="inline-flex items-center justify-center p-3 bg-blue-500/10 rounded-full mb-4">
          <svg className="w-8 h-8 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h1 className="text-2xl font-semibold text-zinc-100">Python Generation Mode</h1>
        <p className="text-sm leading-relaxed">
          The React dashboard has been deactivated. The workspace is now strictly generating Home Assistant custom component code in Python.
        </p>
        <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-left">
          <p className="text-xs text-zinc-500 uppercase tracking-wider font-semibold mb-2">Workspace Target</p>
          <code className="text-sm text-emerald-400">/custom_components/scene_lifecycle/</code>
        </div>
        <p className="text-xs text-zinc-500 mt-8">
          You can download these files at any time via the Export button (GitHub/ZIP).
        </p>
      </div>
    </div>
  );
}
