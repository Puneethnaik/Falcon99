# Standard Imports
import asyncio
import websockets
import os
import json

# Falcon Imports
from src.server.GameInformation import GameInformation
from src.server.GameManager import GameManager


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
        _, game_manager_id, resource_name = path.split('/')
        for game_manager in self.game_managers:
            if game_manager.id == game_manager_id:
                return True, game_manager
        return False, None

    async def game_connection_callback(self, websocket, path):
        _find_game_manager_given_path = self.find_game_manager_given_path(path)
        if _find_game_manager_given_path[0]:
            print("Access check with game manager and passing control to the game manager")
            _find_game_manager_given_path[1].register_player(websocket, path)
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

    async def check_for_game_manager(self):
        self.worker_conn_stream = await self.worker_conn.open(asyncio.get_event_loop())
        while True:
            print("Checking for game manager from server process")
            game_manager_json = await self.worker_conn_stream.readline()
            print("Recieved %s from server process" % (game_manager_json))
            game_manager = GameManager(**json.loads(game_manager_json))
            self.game_managers.append(game_manager)
            asyncio.get_event_loop().call_soon(game_manager.run)


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
