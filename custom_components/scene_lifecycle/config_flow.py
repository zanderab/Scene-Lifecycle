import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import AbortFlow

from .const import (
    DOMAIN,
    CONF_SCENE_ID,
    CONF_MANAGED_ENTITIES,
    CONF_SUPPRESSED_AUTOMATIONS,
    CONF_DEACTIVATE_OTHER,
    CONF_MANAGED_AREAS,
    CONF_TRANSITION_TIME,
    CONF_DURATION,
    CONF_RESET_SCRIPT,
)

SCENE_COMPATIBLE_DOMAINS = [
    "light",
    "switch",
    "fan",
    "media_player",
    "climate",
    "cover",
    "input_boolean",
]

class SceneLifecycleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Scene Lifecycle."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return SceneLifecycleOptionsFlowHandler()

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:

            try:
                # Ensure reset script defaults to empty string if omitted
                if CONF_RESET_SCRIPT not in user_input or user_input[CONF_RESET_SCRIPT] is None:
                    user_input[CONF_RESET_SCRIPT] = ""
                
                # Enforce unique_id based on the target scene

                await self.async_set_unique_id(user_input[CONF_SCENE_ID])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )
            except AbortFlow:
                raise
            except Exception:
                errors["base"] = "unknown"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME): selector.TextSelector(),
                vol.Required(CONF_SCENE_ID): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="scene", multiple=False)
                ),
                vol.Optional(CONF_MANAGED_ENTITIES, default=[]): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=SCENE_COMPATIBLE_DOMAINS, multiple=True)
                ),
                vol.Optional(CONF_MANAGED_AREAS, default=[]): selector.AreaSelector(
                    selector.AreaSelectorConfig(multiple=True)
                ),
                vol.Optional(CONF_TRANSITION_TIME, default=0): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=3600, mode=selector.NumberSelectorMode.BOX)
                ),
                vol.Optional(CONF_DURATION, default=0): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=86400, mode=selector.NumberSelectorMode.BOX)
                ),
                vol.Optional(CONF_RESET_SCRIPT): selector.EntitySelector(selector.EntitySelectorConfig(domain="script", multiple=False)),
                vol.Optional(CONF_SUPPRESSED_AUTOMATIONS, default=[]): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="automation", multiple=True)
                ),
                vol.Optional(CONF_DEACTIVATE_OTHER, default=[]): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch", multiple=True)
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )


class SceneLifecycleOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Scene Lifecycle."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        # Ensure reset script can be cleared. Voluptuous `Optional` will sometimes exclude keys if they are empty.
        # By providing a default empty string, we make sure it's always included.
        if user_input is not None:
            if CONF_RESET_SCRIPT not in user_input or user_input[CONF_RESET_SCRIPT] is None:
                 user_input[CONF_RESET_SCRIPT] = ""
            return self.async_create_entry(title="", data=user_input)

        # Fallback to config entry data if options are not set yet
        current_managed = self.config_entry.options.get(
            CONF_MANAGED_ENTITIES,
            self.config_entry.data.get(CONF_MANAGED_ENTITIES, []),
        )
        current_areas = self.config_entry.options.get(
            CONF_MANAGED_AREAS,
            self.config_entry.data.get(CONF_MANAGED_AREAS, []),
        )
        current_transition = self.config_entry.options.get(
            CONF_TRANSITION_TIME,
            self.config_entry.data.get(CONF_TRANSITION_TIME, 0),
        )
        current_duration = self.config_entry.options.get(
            CONF_DURATION,
            self.config_entry.data.get(CONF_DURATION, 0),
        )
        current_reset_script = self.config_entry.options.get(
            CONF_RESET_SCRIPT,
            self.config_entry.data.get(CONF_RESET_SCRIPT, ""),
        )
        current_suppressed = self.config_entry.options.get(
            CONF_SUPPRESSED_AUTOMATIONS,
            self.config_entry.data.get(CONF_SUPPRESSED_AUTOMATIONS, []),
        )
        current_deactivate = self.config_entry.options.get(
            CONF_DEACTIVATE_OTHER,
            self.config_entry.data.get(CONF_DEACTIVATE_OTHER, []),
        )

        options_schema = vol.Schema(
            {
                vol.Optional(CONF_MANAGED_ENTITIES, default=current_managed): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=SCENE_COMPATIBLE_DOMAINS, multiple=True)
                ),
                vol.Optional(CONF_MANAGED_AREAS, default=current_areas): selector.AreaSelector(
                    selector.AreaSelectorConfig(multiple=True)
                ),
                vol.Optional(CONF_TRANSITION_TIME, default=current_transition): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=3600, mode=selector.NumberSelectorMode.BOX)
                ),
                vol.Optional(CONF_DURATION, default=current_duration): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=86400, mode=selector.NumberSelectorMode.BOX)
                ),
                vol.Optional(CONF_RESET_SCRIPT, default=current_reset_script): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="script", multiple=False)
                ),
                vol.Optional(CONF_SUPPRESSED_AUTOMATIONS, default=current_suppressed): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="automation", multiple=True)
                ),
                vol.Optional(CONF_DEACTIVATE_OTHER, default=current_deactivate): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="switch", multiple=True)
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )
