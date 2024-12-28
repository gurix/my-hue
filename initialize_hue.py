from appkey import get_appkey
from discover import find_hue_bridge
import asyncio
import yaml

ip_address = asyncio.run(find_hue_bridge())
appkey = get_appkey(ip_address)

if appkey:
    # Data to serialize
    config_data = {
        "ip_address": ip_address,
        "appkey": appkey,
    }

    # Serialize to YAML file
    with open("hue_config.yaml", "w") as yaml_file:
        yaml.dump(config_data, yaml_file)

    print("Configuration saved to hue_config.yaml")
else:
    print("Failed to obtain app key.")
