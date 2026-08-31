import re

with open('custom_components/scene_lifecycle/config_flow.py', 'r') as f:
    content = f.read()

# For CONF_RESET_SCRIPT in options flow, replace default with suggested_value
content = re.sub(
    r'vol\.Optional\(CONF_RESET_SCRIPT, default=current_reset_script\)',
    r'vol.Optional(CONF_RESET_SCRIPT, description={"suggested_value": current_reset_script})',
    content
)

with open('custom_components/scene_lifecycle/config_flow.py', 'w') as f:
    f.write(content)
