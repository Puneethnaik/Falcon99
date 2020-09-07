import asyncio
from src.client.FalconClient import FalconClient
client = FalconClient(server_domain="localhost", port=4000, resource_name="NQueensGame", game_manager_id="338965971240490992060603431953846598276")

asyncio.get_event_loop().run_until_complete(client.connect())
asyncio.get_event_loop().run_forever()