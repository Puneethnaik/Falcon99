import websockets
from contextlib import closing
import asyncio
import json
from multiprocessing import Process
from aiopipe import aiopipe

from src.server.GameInformation import GameInformation
from src.server.CustomEncoder import CustomEncoder
from examples.ChessGameManager import ChessGameManager
from src.server.GameWorker import run_game_worker

class FalconServer:
    def __init__(self):
        self.game_workers = {}
        self.number_of_game_managers = 0
        self.flag = True

    def register_game(self, game_information: GameInformation):
        pass


    async def spawn_game_worker(self, game_information):
        worker_conn, server_conn = aiopipe()
        with worker_conn.send() as tmp:
            game_worker = Process(target=run_game_worker, args=(tmp, game_information))
            game_worker.start()
        server_conn = await server_conn.open(asyncio.get_event_loop())
        print("Spawned a new game worker with pid", game_worker.pid)
        # TODO game name should be unique as it is used for indexing
        self.game_workers[game_information.service_name] = {
            "game_information": game_information,
            "game_worker_pid": game_worker.pid,
            "server_conn": server_conn,
            "worker_conn": worker_conn
        }

    async def create_game_manager(self, name):
        #fetch the game information given the game service  name
        game_information = GameInformation.getByName(name)
        # spawn a new process
        print("Spawning a new game worker")
        # check whether the mentioned game connection port is available or not.
        # first find if a game worker is already serving games similar to this game.
        if self.flag:
            # If all checks passed spawn a new game worker
            self.flag = False
            await self.spawn_game_worker(game_information=game_information)

        else:
            # await asyncio.sleep(10)
            print("Unable to spawn a game worker")

        # TODO pick the right game manager
        # Ask for start time, either ask for game and stream ports
        # or assign the free game ports and stream ports
        # await asyncio.sleep(5)
        game_manager = ChessGameManager(game_manager_id=self.number_of_game_managers, player_mapping={"id1":"first_player", "id2":"second_player"})
        self.number_of_game_managers += 1
        # TODO share this game manager object in shared memory with the game worker that runs the game
        # Or else if there is no game worker for the game, spawn a game worker and then assign this game manager
        # object to that game worker
        print("The id of the game manager created is %d" % game_manager.game_manager_id)
        # self.game_managers.append(game_manager)


        server_conn = self.game_workers[name].get("server_conn", None)
        if server_conn is None:
            print("The pipe between the master process and the worker process seems to be broken.")
        else:
            print("Writing %s to worker process" % (game_manager.toJSON() + '|' + game_information.service_name + '\n'))
            server_conn.write((game_manager.toJSON() + '|' + game_information.service_name + '\n').encode('UTF-8'))

