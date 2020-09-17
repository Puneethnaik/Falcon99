# Standard Imports
import asyncio
import websockets
import os
import json

# Falcon Imports
from src.server.GameInformation import GameInformation
from src.server.GameManager import GameManager
from examples.ChessGameManager import ChessGameManager


class GameWorker:
    def __init__(self, game_information: GameInformation = None):
        self.game_information = game_information
        # self.game_state_service = GameStateService({
        #     "individual_one": empty_chess_board.fen(),
        #     "individual_two": empty_chess_board.fen()
        # })
        self.game_managers = []
        self.game_connection = None
        self.stream_connection = None
        self.worker_conn = None
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)
        print("Starting Game Worker for ", game_information.name)

    async def open_connection(self):
        print("Opening connection")
        # Only one game connection and stream connection per game worker

        self.game_connection = await websockets.serve(self.game_connection_callback,
                                                      self.game_information.server_domain,
                                                      self.game_information.game_port)
        self.stream_connection = await websockets.serve(self.stream_connection_callback,
                                                        self.game_information.server_domain,
                                                        self.game_information.stream_port)

    def find_game_manager_given_path(self, path):
        _, game_manager_id, resource_name, player_id = path.split('/')
        print("The path recieved is", path)
        for game_manager in self.game_managers:
            print(game_manager)
            if game_manager.game_manager_id == int(game_manager_id):
                return True, game_manager
        return False, None

    async def game_connection_callback(self, websocket, path):
        _find_game_manager_given_path = self.find_game_manager_given_path(path)
        *_, player_id = path.split('/')
        if _find_game_manager_given_path[0]:
            print("Access check with game manager and passing control to the game manager")
            print("The type of the game manager is", type(_find_game_manager_given_path[1]))
            await _find_game_manager_given_path[1].register_player(websocket, player_id, path)
        else:
            print("Game manager requested by the client is not found. Please contact the game admin.")

    async def stream_connection_callback(self, websocket, path):
        print("the path is ", path)

    def prepare_uri(self):
        '''
        Return a URI of the service to be accessed from the server whose
        information passed in the constructor
        :return: URI as a string
        '''
        uri = "ws://" + os.path.join(self.server_domain + ":" + str(self.port), self.resource_name)
        return uri

    def return_correct_game_manager_instance(self, service_name, game_manager_json):
        if service_name.strip() == 'NQueensGame':
            print("Initiating chess game manager instance")
            return ChessGameManager(**json.loads(game_manager_json))
        else:
            print("Returning none")
            return None

    async def check_for_game_manager(self):
        self.worker_conn_stream = await self.worker_conn.open(asyncio.get_event_loop())
        while True:
            print("Checking for game manager from server process")
            server_message_json = await self.worker_conn_stream.readline()
            server_message_json = server_message_json.decode('UTF-8')
            # print("Recieved %s from server process" % (server_message_json))
            game_manager_json, service_name = server_message_json.split('|')
            game_manager = self.return_correct_game_manager_instance(service_name=service_name, game_manager_json=game_manager_json)
            # print("The type of game manager is", type(game_manager))
            self.game_managers.append(game_manager)
            # asyncio.gather(game_manager.run())
            await asyncio.gather(game_manager.run())


def run_game_worker(worker_conn, game_information):
    # TODO access the game information from shared memory owned by FalconServer master process
    # game_information = GameInformation(game_port=4000,
    #                                    stream_port=5000,
    #                                    server_domain="localhost",
    #                                    service_name="NQueensGame",
    #                                    name="NQueensGame",
    #                                    description="This is a N Queens Game")
    # game_manager = GameManager()
    game_worker = GameWorker(game_information=game_information)
    game_worker.worker_conn = worker_conn
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(game_worker.check_for_game_manager(), game_worker.open_connection()))
    # asyncio.get_event_loop().call_soon(game_worker.check_for_game_manager())
    # asyncio.get_event_loop().run_until_complete(game_worker.open_connection())
