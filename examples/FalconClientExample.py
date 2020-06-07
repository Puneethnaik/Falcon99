import asyncio
from src.client.FalconClient import FalconClient
client = FalconClient(server_domain="192.168.0.105", port=4000, resource_name="NQueensGame")

asyncio.get_event_loop().run_until_complete(client.connect())
asyncio.get_event_loop().run_forever()