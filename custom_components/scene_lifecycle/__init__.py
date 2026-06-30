"""The Scene Lifecycle integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .manager import SceneLifecycleManager
from .storage import SceneLifecycleStorage

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Scene Lifecycle from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Initialize shared storage if it doesn't exist yet
    if "storage" not in hass.data[DOMAIN]:
        storage = SceneLifecycleStorage(hass)
        await storage.async_load()
        hass.data[DOMAIN]["storage"] = storage
    else:
        storage = hass.data[DOMAIN]["storage"]

    # Initialize the manager for this entry
    manager = SceneLifecycleManager(hass, entry, storage)
    hass.data[DOMAIN][entry.entry_id] = manager

    # Recover state on boot (re-apply automation suppression if it was active)
    await manager.async_recover_on_boot()

    # Forward setup to the switch platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Listen for options updates
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Remove the manager instance from memory, but do not teardown storage yet.
        # Teardown happens only if the entry is actually removed by the user.
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry from the UI."""
    # Since the manager was removed from memory in async_unload_entry,
    # we need to temporarily recreate it to execute the teardown routine cleanly.
    storage: SceneLifecycleStorage = hass.data[DOMAIN].get("storage")
    if storage:
        manager = SceneLifecycleManager(hass, entry, storage)
        await manager.async_teardown()


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
