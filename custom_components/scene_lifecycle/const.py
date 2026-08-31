"""Constants for the Scene Lifecycle integration."""

from homeassistant.const import Platform

DOMAIN = "scene_lifecycle"

CONF_SCENE_ID = "scene_id"
CONF_MANAGED_ENTITIES = "managed_entities"
CONF_SUPPRESSED_AUTOMATIONS = "suppressed_automations"
CONF_DEACTIVATE_OTHER = "deactivate_other"

# New Enhancements
CONF_MANAGED_AREAS = "managed_areas"
CONF_TRANSITION_TIME = "transition_time"
CONF_DURATION = "duration"
CONF_RESET_SCRIPT = "reset_script"

PLATFORMS: list[Platform] = [Platform.SWITCH]

STORAGE_KEY = f"{DOMAIN}.storage"
STORAGE_VERSION = 1

