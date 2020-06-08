#Standard Imports
import asyncio
import websockets
import os
import json

#Falcon Imports
from src.server.GameStateService import GameStateService
from src.server.GameInformation import GameInformation
from src.server.GameManager import  GameManager

import chess

class GameWorker:
    def __init__(self, game_information:GameInformation=None, timer_state_service=None, score_state_service=None, game_manager:GameManager=None):
        self.game_information = game_information
        empty_chess_board = chess.Board()
        self.game_state_service = GameStateService({
            "individual_one": empty_chess_board.fen(),
            "individual_two": empty_chess_board.fen()
        })
        self.timer_state_service = timer_state_service
        self.score_state_service = score_state_service
        self.game_manager = game_manager
        self.game_manager.set_game_worker(self)
        print("Starting Game Worker for ", game_information.name)
    async def open_connection(self):
        print("Opening connection")
        self.game_connection = await websockets.serve(self.game_manager.register_player, self.game_information.server_domain, self.game_information.game_port)
        self.stream_connection = await websockets.serve(self.game_manager.register_streamer, self.game_information.server_domain, self.game_information.stream_port)
        # self.game_manager.set_connection_object()

    async def run(self):
        print("Running the game event loop")
        while(True):
            #Game event loop
            player = self.game_manager.get_player("first_player")
            await player.get("websocket").send(json.dumps(self.game_state_service.get_state()))
            action = await player.get("websocket").recv()
            print("Recieved action", action)
            self.game_state_service.update_state(json.loads(action))
            # self.game_state_service.update_state(self.game_manager.get_second_player().make_turn())
            if self.has_achieved_winning_state(self.game_state_service.state):
                break

    def has_achieved_winning_state(self, game_state):
        return False

    def prepare_uri(self):
        '''
        Return a URI of the service to be accessed from the server whose
        information passed in the constructor
        :return: URI as a string
        '''
        uri = "ws://" + os.path.join(self.server_domain + ":" + str(self.port), self.resource_name)
        return uri

game_information = GameInformation(game_port=4000, stream_port=5000, server_domain="localhost", service_name="NQueensGame", name="NQueensGame", description="This is a N Queens Game")
game_manager = GameManager()
game_worker = GameWorker(game_information=game_information, game_manager=game_manager)

asyncio.get_event_loop().run_until_complete(game_worker.open_connection())
# asyncio.get_event_loop().run_until_complete(game_worker.run())
asyncio.get_event_loop().run_forever()
