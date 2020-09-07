import asyncio
import json
import websockets
import uuid
from json import JSONEncoder

class GameManager:
    def __init__(self, id=None, players={}, streamers={}, game_state_service=None, streamer_count=1, start_time='', connection=None):
        self.id = id
        self.players = players
        self.streamers = streamers
        self.game_state_service = game_state_service
        self.streamer_count = streamer_count
        self.start_time = start_time
        self.connection = connection

    def __str__(self):
        return "<Game Manager id=%s>" % self.id

    async def register_player(self, websocket, path):
        #TODO add logic to check the player credentials against a persisted list of participants
        self.players["first_player"] = {
            "websocket": websocket
        }
        if self.are_all_players_registered():
            await self.run()

    def run(self):
        print("Running the empty implementation")

    def has_achieved_winning_state(self, game_state):
        return False

    async def register_streamer(self, websocket, path):
        print("Registering a streamer")
        print("The streams are", self.streamers)
        self.streamers["streamer_"+str(self.streamer_count)] = {
            "websocket": websocket
        }
        self.streamer_count += 1
        await asyncio.gather(self.stream_game())


    async def stream_game(self):
        while(True):
            print("The number of streamers are", len(self.streamers.keys()))
            try:
                for streamer in self.streamers.keys():
                    await self.streamers[streamer]["websocket"].send(json.dumps(self.game_worker.game_state_service.get_state()))
            except websockets.exceptions.ConnectionClosedOK:
                #Remove the client from the state of streamers
                del self.streamers[streamer]
            await asyncio.sleep(1)

    def are_all_players_registered(self):
        return ("first_player" in self.players.keys()) and ("second_player" in self.players.keys())

    def get_player(self, player_name):
        return self.players.get(player_name, None)

    def set_connection_object(self, connection):
        self.connection = connection
