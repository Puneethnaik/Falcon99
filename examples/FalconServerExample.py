from src.server.FalconServer import FalconServer
from src.server.GameInformation import GameInformation

server = FalconServer()
game_information = GameInformation(port=4000, server_domain="192.168.0.105", service_name="NQueensGame", name="N Queens Puzzle", description="This is a N Queens Game")
server.register_game(game_information)