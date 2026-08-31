"""Switch platform for Scene Lifecycle."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.event import async_call_later

from .const import DOMAIN
from .manager import SceneLifecycleManager

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Scene Lifecycle switch based on a config entry."""
    manager: SceneLifecycleManager = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SceneLifecycleSwitch(manager)])


class SceneLifecycleSwitch(SwitchEntity):
    """Switch representation of a Scene Lifecycle."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_icon = "mdi:auto-fix"

    def __init__(self, manager: SceneLifecycleManager) -> None:
        """Initialize the switch."""
        self.manager = manager
        self._attr_unique_id = f"{manager.entry_id}_switch"
        self._cancel_timer = None
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, manager.entry_id)},
            name=manager.name,
            manufacturer="Scene Lifecycle",
        )

    @property
    def is_on(self) -> bool:
        """Return True if the scene lifecycle is active."""
        return self.manager.storage.is_active(self.manager.entry_id)

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        self.async_write_ha_state()

    @callback
    def _async_timer_finished(self, _time) -> None:
        """Handle the auto-revert timer finishing."""
        self._cancel_timer = None
        self.hass.async_create_task(self.async_turn_off())

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Activate the scene lifecycle."""
        await self.manager.async_activate()
        
        if self.manager.duration > 0:
            if self._cancel_timer:
                self._cancel_timer()
            self._cancel_timer = async_call_later(
                self.hass, self.manager.duration, self._async_timer_finished
            )
            
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Deactivate the scene lifecycle."""
        if self._cancel_timer:
            self._cancel_timer()
            self._cancel_timer = None
            
        await self.manager.async_deactivate()
        self.async_write_ha_state()
