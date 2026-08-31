"""Manager class for orchestrating Scene Lifecycle per config entry."""
import logging
import re
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr

from .const import (
    CONF_MANAGED_ENTITIES,
    CONF_SCENE_ID,
    CONF_SUPPRESSED_AUTOMATIONS,
    CONF_DEACTIVATE_OTHER,
    CONF_MANAGED_AREAS,
    CONF_TRANSITION_TIME,
    CONF_DURATION,
    CONF_RESET_SCRIPT,
)
from .storage import SceneLifecycleStorage

_LOGGER = logging.getLogger(__name__)


class SceneLifecycleManager:
    """Orchestrates the full scene lifecycle for one config entry."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, storage: SceneLifecycleStorage
    ) -> None:
        """Initialize the manager."""
        self.hass = hass
        self.entry = entry
        self.storage = storage

        self.entry_id = entry.entry_id
        self.name = entry.title or entry.data.get(CONF_NAME, "Unknown Scene Lifecycle")
        self.scene_id = entry.data.get(CONF_SCENE_ID)

        # Options override data
        self.managed_entities: list[str] = entry.options.get(
            CONF_MANAGED_ENTITIES, entry.data.get(CONF_MANAGED_ENTITIES, [])
        )
        self.suppressed_automations: list[str] = entry.options.get(
            CONF_SUPPRESSED_AUTOMATIONS, entry.data.get(CONF_SUPPRESSED_AUTOMATIONS, [])
        )
        self.deactivate_other: list[str] = entry.options.get(
            CONF_DEACTIVATE_OTHER, entry.data.get(CONF_DEACTIVATE_OTHER, [])
        )
        self.managed_areas: list[str] = entry.options.get(
            CONF_MANAGED_AREAS, entry.data.get(CONF_MANAGED_AREAS, [])
        )
        self.transition_time: int = entry.options.get(
            CONF_TRANSITION_TIME, entry.data.get(CONF_TRANSITION_TIME, 0)
        )
        self.duration: int = entry.options.get(
            CONF_DURATION, entry.data.get(CONF_DURATION, 0)
        )
        self.reset_script: str = entry.options.get(
            CONF_RESET_SCRIPT, entry.data.get(CONF_RESET_SCRIPT, "")
        )

        # Deterministic snapshot ID based on entry_id to avoid collisions
        entry_id_clean = re.sub(r'[^a-z0-9]', '', self.entry_id.lower())[:12]
        self.snapshot_scene_id = f"scene_lifecycle_snapshot_{entry_id_clean}"

    # =========================================================================
    # ACTIVATE
    # =========================================================================
    async def async_activate(self) -> bool:
        """Activate the scene, take snapshot, and suppress automations."""
        if self.storage.is_active(self.entry_id):
            _LOGGER.info(
                "[%s] Scene is already active, ignoring activation request.", self.name
            )
            return False

        _LOGGER.debug("[%s] Activating scene lifecycle...", self.name)
        
        claims_made = []

        try:
            # 0. Deactivate other mutually exclusive scenes
            for switch_id in self.deactivate_other:
                _LOGGER.debug("[%s] Deactivating exclusive switch: %s", self.name, switch_id)
                try:
                    await self.hass.services.async_call(
                        "switch",
                        "turn_off",
                        {"entity_id": switch_id},
                        blocking=True,
                    )
                except Exception as err:
                    _LOGGER.warning("[%s] Failed to turn off exclusive switch %s: %s", self.name, switch_id, err)

            # 1. Compute full list of entities to snapshot
            snapshot_entities = set(self.managed_entities)
            
            # 1a. Add entities from managed areas
            if self.managed_areas:
                entity_reg = er.async_get(self.hass)
                device_reg = dr.async_get(self.hass)
                for area_id in self.managed_areas:
                    # Get entities directly assigned to the area
                    area_entities = er.async_entries_for_area(entity_reg, area_id)
                    for ent in area_entities:
                        snapshot_entities.add(ent.entity_id)
                    
                    # Get entities assigned to devices in the area
                    area_devices = dr.async_entries_for_area(device_reg, area_id)
                    for dev in area_devices:
                        dev_entities = er.async_entries_for_device(entity_reg, dev.id)
                        for ent in dev_entities:
                            snapshot_entities.add(ent.entity_id)
                            
            # 1b. Add entities from the target scene itself
            scene_state = self.hass.states.get(self.scene_id)
            if scene_state and "entity_id" in scene_state.attributes:
                scene_entities = scene_state.attributes["entity_id"]
                if isinstance(scene_entities, list):
                    snapshot_entities.update(scene_entities)
                elif isinstance(scene_entities, str):
                    snapshot_entities.add(scene_entities)

            entity_list = list(snapshot_entities)
            _LOGGER.debug("[%s] Snapshotting %d entities.", self.name, len(entity_list))

            # 1c. Capture pre-scene effect and states for lights
            pre_scene_effects = {}
            for entity_id in entity_list:
                if entity_id.startswith("light."):
                    state = self.hass.states.get(entity_id)
                    if state:
                        pre_scene_effects[entity_id] = {
                            "effect": state.attributes.get("effect"),
                            "state": state.state
                        }

            # 2. Call scene.create to make the snapshot
            if entity_list:
                await self.hass.services.async_call(
                    "scene",
                    "create",
                    {
                        "scene_id": self.snapshot_scene_id,
                        "snapshot_entities": entity_list,
                    },
                    blocking=True,
                )

            # 3. Suppress automations
            for auto_id in self.suppressed_automations:
                is_first = await self.storage.async_claim_automation(auto_id, self.entry_id)
                claims_made.append(auto_id)
                if is_first:
                    _LOGGER.debug("[%s] Disabling automation: %s", self.name, auto_id)
                    await self.hass.services.async_call(
                        "automation",
                        "turn_off",
                        {"entity_id": auto_id},
                        blocking=True,
                    )
                else:
                    _LOGGER.debug(
                        "[%s] Automation %s already claimed, skipping turn_off.",
                        self.name,
                        auto_id,
                    )

            # 4. Activate target scene
            try:
                _LOGGER.debug("[%s] Turning on target scene: %s with transition %s", self.name, self.scene_id, self.transition_time)
                
                service_data = {"entity_id": self.scene_id}
                if self.transition_time > 0:
                    service_data["transition"] = self.transition_time
                    
                await self.hass.services.async_call(
                    "scene",
                    "turn_on",
                    service_data,
                    blocking=True,
                )
            except Exception as err:
                _LOGGER.warning(
                    "[%s] The target scene could not be found or failed to turn on (%s): %s",
                    self.name,
                    self.scene_id,
                    err,
                )

            # 5. Mark as active
            await self.storage.async_mark_active(
                self.entry_id, self.snapshot_scene_id, self.suppressed_automations,
                pre_scene_effects
            )
            _LOGGER.info("[%s] Activation complete.", self.name)
            return True

        except Exception as err:
            _LOGGER.error("[%s] Unexpected error during activation: %s", self.name, err, exc_info=True)
            
            # Rollback any claims made during this failed activation
            for auto_id in claims_made:
                try:
                    is_last = await self.storage.async_release_automation(auto_id, self.entry_id)
                    if is_last:
                        _LOGGER.debug("[%s] Rollback: Re-enabling automation %s", self.name, auto_id)
                        await self.hass.services.async_call(
                            "automation",
                            "turn_on",
                            {"entity_id": auto_id},
                            blocking=True,
                        )
                except Exception as rollback_err:
                    _LOGGER.warning(
                        "[%s] Failed to rollback automation %s: %s", 
                        self.name, auto_id, rollback_err
                    )
            return False

    # =========================================================================
    # DEACTIVATE
    # =========================================================================
    async def async_deactivate(self) -> bool:
        """Deactivate the scene, restore snapshot, and release automations."""
        if not self.storage.is_active(self.entry_id):
            _LOGGER.info("[%s] Scene is not active, ignoring deactivation.", self.name)
            return False

        _LOGGER.debug("[%s] Deactivating scene lifecycle...", self.name)

        # 0. Run reset script if provided
        if self.reset_script:
            _LOGGER.debug("[%s] Running reset script: %s", self.name, self.reset_script)
            try:
                await self.hass.services.async_call(
                    "script",
                    "turn_on",
                    {"entity_id": self.reset_script},
                    blocking=True,
                )
            except Exception as err:
                _LOGGER.warning("[%s] Failed to run reset script %s: %s", self.name, self.reset_script, err)

        # 1. Restore the snapshot
        full_snapshot_id = f"scene.{self.snapshot_scene_id}"
        
        entry_data = self.storage.get_entry(self.entry_id)
        pre_scene_effects = entry_data.get("pre_scene_effects", {})
        
        # 1a. Force-clear light effects before restoring snapshot if needed
        # This helps integrations like Tapo that get stuck in an effect and ignore color commands.
        for entity_id, orig_data in pre_scene_effects.items():
            if isinstance(orig_data, dict):
                orig_effect = orig_data.get("effect")
                orig_state = orig_data.get("state")
            else:
                # Backwards compatibility with existing active scenes
                orig_effect = orig_data
                orig_state = "on"

            # Skip clearing the effect if the light was originally off, preventing it from flashing on
            if orig_state == "off":
                continue

            current_state = self.hass.states.get(entity_id)
            if not current_state:
                continue
                
            current_effect = current_state.attributes.get("effect")
            
            if current_effect and current_effect != orig_effect:
                _LOGGER.debug("[%s] Forcing effect clear for %s before snapshot restore", self.name, entity_id)
                
                clear_effect_val = orig_effect
                if clear_effect_val is None:
                    # Try to find a valid 'none' or 'None' in effect_list, fallback to 'None'
                    effect_list = current_state.attributes.get("effect_list", [])
                    if isinstance(effect_list, list):
                        if "none" in effect_list:
                            clear_effect_val = "none"
                        elif "None" in effect_list:
                            clear_effect_val = "None"
                        elif "Clear" in effect_list:
                            clear_effect_val = "Clear"
                        else:
                            clear_effect_val = "None"
                    else:
                        clear_effect_val = "None"
                        
                try:
                    await self.hass.services.async_call(
                        "light",
                        "turn_on",
                        {"entity_id": entity_id, "effect": clear_effect_val},
                        blocking=True,
                    )
                except Exception as err:
                    _LOGGER.debug("[%s] Soft-failure clearing effect on %s: %s", self.name, entity_id, err)

        try:
            _LOGGER.debug("[%s] Restoring snapshot: %s with transition %s", self.name, full_snapshot_id, self.transition_time)
            service_data = {"entity_id": full_snapshot_id}
            if self.transition_time > 0:
                service_data["transition"] = self.transition_time
                
            await self.hass.services.async_call(
                "scene",
                "turn_on",
                service_data,
                blocking=True,
            )
        except Exception as err:
            _LOGGER.warning(
                "[%s] Failed to restore snapshot scene (%s): %s",
                self.name,
                full_snapshot_id,
                err,
            )

        # 2. Release automations
        suspended_autos = entry_data.get("suspended_automations", [])
        
        for auto_id in suspended_autos:
            is_last = await self.storage.async_release_automation(auto_id, self.entry_id)
            if is_last:
                _LOGGER.debug("[%s] Re-enabling automation: %s", self.name, auto_id)
                await self.hass.services.async_call(
                    "automation",
                    "turn_on",
                    {"entity_id": auto_id},
                    blocking=True,
                )
            else:
                _LOGGER.debug(
                    "[%s] Automation %s still claimed by others, skipping turn_on.",
                    self.name,
                    auto_id,
                )

        # 3. Mark as inactive
        await self.storage.async_mark_inactive(self.entry_id)
        _LOGGER.info("[%s] Deactivation complete.", self.name)
        return True

    # =========================================================================
    # RECOVERY
    # =========================================================================
    async def async_recover_on_boot(self) -> None:
        """Recover state upon Home Assistant boot if the scene was left active."""
        if self.storage.is_active(self.entry_id):
            _LOGGER.warning(
                "[%s] Found active on boot. Re-applying automation suppressions but "
                "leaving scene state as-is to prevent unexpected changes.",
                self.name,
            )
            
            entry_data = self.storage.get_entry(self.entry_id)
            suspended_autos = entry_data.get("suspended_automations", [])

            for auto_id in suspended_autos:
                _LOGGER.debug(
                    "[%s] Re-issuing turn_off for automation: %s", self.name, auto_id
                )
                try:
                    await self.hass.services.async_call(
                        "automation",
                        "turn_off",
                        {"entity_id": auto_id},
                        blocking=True,
                    )
                except Exception as err:
                    _LOGGER.error(
                        "[%s] Failed to disable automation %s during boot recovery: %s",
                        self.name,
                        auto_id,
                        err,
                    )

    # =========================================================================
    # TEARDOWN
    # =========================================================================
    async def async_teardown(self) -> None:
        """Handle cleanup when the config entry is unloaded or removed."""
        _LOGGER.debug("[%s] Tearing down manager.", self.name)
        if self.storage.is_active(self.entry_id):
            _LOGGER.info("[%s] Deactivating before teardown.", self.name)
            await self.async_deactivate()

        await self.storage.async_remove_entry(self.entry_id)
        _LOGGER.debug("[%s] Teardown complete.", self.name)
