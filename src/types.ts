import { Divide, FileCode, Lightbulb, Map, PenTool, ShieldAlert } from 'lucide-react';

export type SectionId = 'critique' | 'mvp' | 'architecture' | 'structure' | 'api' | 'naming';

export interface Section {
  id: SectionId;
  title: string;
  icon: any;
  description: string;
}

export const sections: Section[] = [
  { id: 'critique', title: 'Concept Critique', icon: ShieldAlert, description: 'Analysis of the idea and technical hurdles.' },
  { id: 'mvp', title: 'MVP Scope Cut', icon: Divide, description: 'What to build for v0.1 and what to defer.' },
  { id: 'architecture', title: 'Architecture Diagram', icon: Map, description: 'High-level component interaction.' },
  { id: 'structure', title: 'File Structure', icon: FileCode, description: 'Python project layout for custom_component.' },
  { id: 'api', title: 'HA API Discovery', icon: Lightbulb, description: 'How to interact with Home Assistant internals.' },
  { id: 'naming', title: 'Naming Suggestions', icon: PenTool, description: 'Alternative names for the integration.' },
];
