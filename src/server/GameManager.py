import asyncio
class GameManager:
    def __init__(self):
        self.players = {}
    async def register_player(self, websocket, path):
        self.players["first_player"] = {
            "websocket": websocket
        }
        if self.are_all_players_registered():
            await asyncio.gather(self.game_worker.run())

    def set_game_worker(self, game_worker):
        self.game_worker = game_worker

    def are_all_players_registered(self):
        return True

    def get_player(self, player_name):
        return self.players.get(player_name, None)

    def set_connection_object(self, connection):
        self.connection = connection