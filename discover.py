from aiohue.discovery import discover_nupnp

async def find_hue_bridge():
    bridges = await discover_nupnp()
    for bridge in bridges:
        print(f"Bridge found: {bridge.host}")
        return bridge.host

