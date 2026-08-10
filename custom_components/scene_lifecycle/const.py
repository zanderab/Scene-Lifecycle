"""Constants for the Scene Lifecycle integration."""

from homeassistant.const import Platform

DOMAIN = "scene_lifecycle"

CONF_SCENE_ID = "scene_id"
CONF_MANAGED_ENTITIES = "managed_entities"
CONF_SUPPRESSED_AUTOMATIONS = "suppressed_automations"
CONF_DEACTIVATE_OTHER = "deactivate_other"

PLATFORMS: list[Platform] = [Platform.SWITCH]

STORAGE_KEY = f"{DOMAIN}.storage"
STORAGE_VERSION = 1

