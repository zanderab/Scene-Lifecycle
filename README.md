# 🎬 Scene Lifecycle for Home Assistant

A custom integration that brings complete scene lifecycle management to Home Assistant — snapshot, suppress, restore.

## ✨ What It Does

Most Home Assistant scenes are "fire and forget" — they activate, but don't:

- Remember the previous state of lights they touch
- Suppress other automations that interfere (motion sensors, dynamic lighting blueprints)
- Restore the previous state cleanly when deactivated

**Scene Lifecycle fixes all three.**

## 🎯 Features (v0.1)

- 🔄 **Snapshot & Restore** — Captures current entity state before activating, restores on deactivation
- 🛡️ **Automation Suppression** — Temporarily disables conflicting automations while active
- 🔢 **Reference Counting** — Multiple active scenes can share the same automation safely
- 💾 **Restart-Safe** — Persisted state survives Home Assistant restarts
- 🎛️ **UI Config Flow** — Set up entirely through the Home Assistant UI, no YAML required
- 🔘 **Switch Entity per Scene** — Native HA toggle for dashboards, voice, and automations

## 📦 Installation

### Via HACS (Custom Repository)

1. HACS → Integrations → ⋮ (top right) → Custom repositories
2. Add `https://github.com/zanderab/Scene-Lifecycle` as type **Integration**
3. Search for **Scene Lifecycle** and download
4. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/scene_lifecycle` folder
2. Copy it to your `<config>/custom_components/` directory
3. Restart Home Assistant

## 🛠️ Setup

1. **Settings → Devices & Services → + Add Integration**
2. Search for **Scene Lifecycle**
3. Fill in:
   - **Name** — friendly name (e.g. "Movie Mode")
   - **Target Scene** — the scene to activate
   - **Managed Entities** — optional, extra entities to snapshot
   - **Automations to Suppress** — automations that should be paused while active

A new switch entity is created. Add it to your dashboard or use it in automations.

## 🧪 How It Works

When the switch is turned **ON**:

1. Captures current state of all managed entities (using `scene.create`)
2. Disables configured automations (with reference counting)
3. Activates the target scene

When the switch is turned **OFF**:

1. Restores the snapshot
2. Re-enables automations (only when no other lifecycle still claims them)

## ⚠️ Known Limitations (v0.1)

- WLED effect names may not always restore perfectly
- Snapshot is in-memory — HA restart while active preserves suppression but loses snapshot
- Entity/automation mapping is manual (auto-detection planned for v0.2)

## 🗺️ Roadmap

- [ ] v0.2 — Auto-detect automations referencing managed entities
- [ ] v0.3 — Per-area scene grouping
- [ ] v0.4 — Voice assistant integration
- [ ] v1.0 — Submit to default HACS repository

## 📜 License

MIT
