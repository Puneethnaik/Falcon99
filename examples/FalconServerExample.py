from src.server.FalconServer import FalconServer
from src.server.GameInformation import GameInformation

import asyncio
server = FalconServer()
game_information = GameInformation(service_name="NQueensGame",
                                   game_port=4000,
                                   stream_port=5000,
                                   server_domain="localhost",
                                   name="N Queens Puzzle",
                                   description="This is a N Queens Game")
server.register_game(game_information)
game_managers = []
for i in range(1):
    game_managers.append(server.create_game_manager("NQueensGame"))
asyncio.get_event_loop().run_until_complete(asyncio.gather(*game_managers))

