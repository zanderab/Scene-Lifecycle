import re

with open('custom_components/scene_lifecycle/config_flow.py', 'r') as f:
    content = f.read()

# Fix user step schema
content = re.sub(
    r'vol\.Optional\(CONF_RESET_SCRIPT, default=""\): selector\.EntitySelector\([\s]*selector\.EntitySelectorConfig\(domain="script", multiple=False\)[\s]*\),',
    r'vol.Optional(CONF_RESET_SCRIPT): selector.EntitySelector(selector.EntitySelectorConfig(domain="script", multiple=False)),',
    content
)

# Fix user step user_input modification
replacement_user = """
            try:
                # Ensure reset script defaults to empty string if omitted
                if CONF_RESET_SCRIPT not in user_input or user_input[CONF_RESET_SCRIPT] is None:
                    user_input[CONF_RESET_SCRIPT] = ""
                
                # Enforce unique_id based on the target scene
"""
content = content.replace("            try:\n                # Enforce unique_id based on the target scene", replacement_user)

# Fix init step schema
# We'll build the schema dynamically so we can conditionally add default
replacement_init_schema = """
        schema_dict = {
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
            schema_dict[vol.Optional(CONF_RESET_SCRIPT, default=current_reset_script)] = selector.EntitySelector(
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
"""

# Replace the whole options_schema = vol.Schema({ ... })
import re
content = re.sub(
    r'[\s]*options_schema = vol\.Schema\([\s]*\{[\s\S]*?vol\.Optional\(CONF_DEACTIVATE_OTHER.*?\)[\s]*\}[\s]*\)',
    replacement_init_schema,
    content
)

with open('custom_components/scene_lifecycle/config_flow.py', 'w') as f:
    f.write(content)
