import websockets
import asyncio
import subprocess

from src.server.GameInformation import GameInformation
class FalconServer:
    def __init__(self):
        self.game_workers = {}

    def register_game(self, game_information:GameInformation):
        #spawn a new process
        print("Spawning a new game worker")
        game_worker = subprocess.Popen(["/usr/bin/python3", "/home/puneeth/Desktop/Projects/Falcon99/src/server/GameWorker.py"])
        print("Spawned a new game worker with pid", game_worker.pid)

        self.game_workers[game_information.name] = {
            "game_information": game_information,
            "game_worker_pid": game_worker.pid
        }

