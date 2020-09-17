import asyncio
from src.client.FalconClient import FalconClient
players = []
for i in range(1):
    player1 = FalconClient(server_domain="localhost", port=4000, resource_name="NQueensGame", game_manager_id=str(i), player_id="id1")
    player2 = FalconClient(server_domain="localhost", port=4000, resource_name="NQueensGame", game_manager_id=str(i), player_id="id2")
    players.append(player1.connect())
    players.append(player2.connect())
asyncio.get_event_loop().run_until_complete(asyncio.gather(*players))

asyncio.get_event_loop().run_forever()