"""Storage helpers for Scene Lifecycle."""
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
import homeassistant.util.dt as dt_util

from .const import DOMAIN, STORAGE_KEY, STORAGE_VERSION

_LOGGER = logging.getLogger(__name__)

class SceneLifecycleStorage:
    """Class to handle Scene Lifecycle storage."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the storage."""
        self.hass = hass
        self.store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._data: dict[str, Any] = {
            "entries": {},
            "automation_claims": {},
        }

    async def async_load(self) -> None:
        """Load data from storage."""
        stored = await self.store.async_load()
        if stored:
            self._data = stored
        else:
            self._data = {
                "entries": {},
                "automation_claims": {},
            }

    async def async_save(self) -> None:
        """Save data to storage."""
        await self.store.async_save(self._data)

    def is_active(self, entry_id: str) -> bool:
        """Check if a specific config entry's scene is active."""
        entry = self.get_entry(entry_id)
        return entry.get("is_active", False)

    def get_entry(self, entry_id: str) -> dict[str, Any]:
        """Get storage data for a specific config entry."""
        return self._data.get("entries", {}).get(entry_id, {})

    async def async_mark_active(
        self, entry_id: str, snapshot_scene_id: str, suspended_automations: list[str],
        pre_scene_effects: dict[str, Any] = None
    ) -> None:
        """Mark an entry as active and store its snapshot and automations."""
        if "entries" not in self._data:
            self._data["entries"] = {}
            
        self._data["entries"][entry_id] = {
            "is_active": True,
            "snapshot_scene_id": snapshot_scene_id,
            "suspended_automations": suspended_automations,
            "pre_scene_effects": pre_scene_effects or {},
            "activated_at": dt_util.utcnow().isoformat(),
        }
        await self.async_save()

    async def async_mark_inactive(self, entry_id: str) -> None:
        """Mark an entry as inactive."""
        if entry_id in self._data.get("entries", {}):
            self._data["entries"][entry_id]["is_active"] = False
            await self.async_save()

    async def async_remove_entry(self, entry_id: str) -> None:
        """Remove storage data for a specific config entry entirely."""
        changed = False
        if entry_id in self._data.get("entries", {}):
            self._data["entries"].pop(entry_id)
            changed = True
        
        # Clean up any orphaned claims for this entry
        empty_claims = []
        for auto_id, claims in self._data.get("automation_claims", {}).items():
            if entry_id in claims:
                claims.remove(entry_id)
                changed = True
            if not claims:
                empty_claims.append(auto_id)
        
        for auto_id in empty_claims:
            self._data["automation_claims"].pop(auto_id)

        if changed:
            await self.async_save()

    async def async_claim_automation(self, automation_id: str, entry_id: str) -> bool:
        """Claim an automation for suppression. Returns True if this is the first claim."""
        if "automation_claims" not in self._data:
            self._data["automation_claims"] = {}

        if automation_id not in self._data["automation_claims"]:
            self._data["automation_claims"][automation_id] = []
        
        is_first = len(self._data["automation_claims"][automation_id]) == 0
        
        if entry_id not in self._data["automation_claims"][automation_id]:
            self._data["automation_claims"][automation_id].append(entry_id)
            await self.async_save()
            
        return is_first

    async def async_release_automation(self, automation_id: str, entry_id: str) -> bool:
        """Release a claimed automation. Returns True if this was the last release."""
        if automation_id not in self._data.get("automation_claims", {}):
            return False
            
        claims = self._data["automation_claims"][automation_id]
        if entry_id in claims:
            claims.remove(entry_id)
            
        is_last = len(claims) == 0
        if is_last:
            self._data["automation_claims"].pop(automation_id)
            
        await self.async_save()
        return is_last

    def get_all_claimed_automations(self) -> dict[str, list[str]]:
        """Get all currently claimed automations and who claims them."""
        return self._data.get("automation_claims", {})

    def get_all_active_entries(self) -> dict[str, dict[str, Any]]:
        """Get all currently active entries."""
        return {
            entry_id: data 
            for entry_id, data in self._data.get("entries", {}).items() 
            if data.get("is_active")
        }

