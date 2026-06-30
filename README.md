# 🎬 Scene Lifecycle for Home Assistant2 3A custom integration that brings complete scene lifecycle management to Home Assistant — snapshot, suppress, restore.4 5## 

✨ What It Does6 7Most Home Assistant scenes are "fire and forget" — they activate, but don't:8- Remember the previous state of lights they touch9- Suppress other automations that interfere (motion sensors, dynamic lighting blueprints)10- Restore the previous state cleanly when deactivated11 12**Scene Lifecycle fixes all three.**13 14## 🎯 Features (v0.1)15 16- 🔄 **Snapshot & Restore** — Captures current entity state before activating, restores on deactivation17- 

🛡️ **Automation Suppression** — Temporarily disables conflicting automations while active18- 

🔢 **Reference Counting** — Multiple active scenes can share the same automation safely19- 

💾 **Restart-Safe** — Persisted state survives Home Assistant restarts20- 

🎛️ **UI Config Flow** — Set up entirely through the Home Assistant UI, no YAML required21- 

🔘 **Switch Entity per Scene** — Native HA toggle for dashboards, voice, and automations22 23## 

📦 Installation24 25### Via HACS (Custom Repository)26 271. HACS → Integrations → ⋮ (top right) → Custom repositories282. Add `https://github.com/zanderab/Scene-Lifecycle` as type **Integration**293. Search for **Scene Lifecycle** and download304. Restart Home Assistant31 32### Manual Installation33 341. Download the `custom_components/scene_lifecycle` folder352. Copy it to your `<config>/custom_components/` directory363. Restart Home Assistant37 38## 🛠️ Setup39 401. **Settings → Devices & Services → + Add Integration**412. Search for **Scene Lifecycle**423. Fill in:43   - **Name** — friendly name (e.g. "Movie Mode")44   - **Target Scene** — the scene to activate45   - **Managed Entities** — optional, extra entities to snapshot46   - **Automations to Suppress** — automations that should be paused while active47 48A new switch entity is created. Add it to your dashboard or use it in automations.49 50## 

🧪 How It Works51 52When the switch is turned **ON**:531. Captures current state of all managed entities (using `scene.create`)542. Disables configured automations (with reference counting)553. Activates the target scene56 57When the switch is turned **OFF**:581. Restores the snapshot592. Re-enables automations (only when no other lifecycle still claims them)60 61## 

⚠️ Known Limitations (v0.1)62 63- WLED effect names may not always restore perfectly64- Snapshot is in-memory — HA restart while active preserves suppression but loses snapshot65- Entity/automation mapping is manual (auto-detection planned for v0.2)66 67## 🗺️ Roadmap68 69- [ ] v0.2 — Auto-detect automations referencing managed entities70- [ ] v0.3 — Per-area scene grouping71- [ ] v0.4 — Voice assistant integration72- [ ] v1.0 — Submit to default HACS repository73 74## 

📜 License75 76MIT
