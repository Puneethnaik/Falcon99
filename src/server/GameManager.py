import asyncio
import json
import websockets
class GameManager:
    def __init__(self):
        self.players = {}
        self.streamers = {}
        self.streamer_count = 1
    async def register_player(self, websocket, path):
        self.players["first_player"] = {
            "websocket": websocket
        }
        if self.are_all_players_registered():
            await asyncio.gather(self.game_worker.run())
    async def register_streamer(self, websocket, path):
        print("Registering a streamer")
        print("The streams are", self.streamers)
        self.streamers["streamer_"+str(self.streamer_count)] = {
            "websocket": websocket
        }
        self.streamer_count += 1
        await asyncio.gather(self.stream_game())
    def set_game_worker(self, game_worker):
        self.game_worker = game_worker

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
        return True

    def get_player(self, player_name):
        return self.players.get(player_name, None)

    def set_connection_object(self, connection):
        self.connection = connection