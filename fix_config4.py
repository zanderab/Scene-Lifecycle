import re

with open('custom_components/scene_lifecycle/config_flow.py', 'r') as f:
    lines = f.readlines()

out_lines = []
skip = False
for line in lines:
    if "options_schema = vol.Schema" in line:
        skip = True
        out_lines.append("""        schema_dict = {
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
        }
        
        if current_reset_script:
            schema_dict[vol.Optional(CONF_RESET_SCRIPT, description={"suggested_value": current_reset_script})] = selector.EntitySelector(
                selector.EntitySelectorConfig(domain="script", multiple=False)
            )
        else:
            schema_dict[vol.Optional(CONF_RESET_SCRIPT)] = selector.EntitySelector(
                selector.EntitySelectorConfig(domain="script", multiple=False)
            )
            
        schema_dict.update({
            vol.Optional(CONF_SUPPRESSED_AUTOMATIONS, default=current_suppressed): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="automation", multiple=True)
            ),
            vol.Optional(CONF_DEACTIVATE_OTHER, default=current_deactivate): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="switch", multiple=True)
            ),
        })
        options_schema = vol.Schema(schema_dict)
""")
    elif skip and "return self.async_show_form(" in line:
        skip = False
        out_lines.append(line)
    elif not skip:
        out_lines.append(line)

with open('custom_components/scene_lifecycle/config_flow.py', 'w') as f:
    f.writelines(out_lines)
