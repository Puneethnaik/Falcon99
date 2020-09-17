from src.server.GameManager import GameManager
import chess
import json
from src.server.GameStateService import GameStateService
from src.server.CustomEncoder import CustomEncoder
import asyncio

class ChessGameManager(GameManager):
    def __init__(self, game_manager_id=None, player_mapping={}, players={}, streamers={}, game_state_service=None, streamer_count=1, start_time='', connection=None):
        super().__init__(game_manager_id=game_manager_id,
                         player_mapping=player_mapping,
                         players=players,
                         streamers=streamers,
                         game_state_service=game_state_service,
                         streamer_count=streamer_count,
                         start_time=start_time,
                         connection=connection
                         )
        empty_chess_board = chess.Board()
        self.game_state_service = GameStateService({
            "moves": []
        })

    async def run(self):
        print("Running the chess run function")
        print("Game manager %d running game event loop" % self.game_manager_id)
        while (True):
            player1 = self.get_player("first_player")
            player2 = self.get_player("second_player")
            if player1 is None or player2 is None:
                await asyncio.sleep(1)
                continue
            print("The player1 recieved is ", player1)
            print("The game state before sending it is", self.game_state_service.get_state())
            await player1["websocket"].send(json.dumps(self.game_state_service.get_state()))
            action = await player1.get("websocket").recv()

            print("Recieved action from player 1", action)
            self.game_state_service.update_state(json.loads(action))
            await player2["websocket"].send(json.dumps(self.game_state_service.get_state()))
            action = await player2.get("websocket").recv()
            print("Recieved action from player 2", action)

            self.game_state_service.update_state(json.loads(action))

            # self.game_state_service.update_state(self.game_manager.get_second_player().make_turn())
            if self.has_achieved_winning_state(self.game_state_service.state):
                break

    def are_all_players_registered(self):
        return ("first_player" in self.players.keys()) and ("second_player" in self.players.keys())
    def toJSON(self):
        return json.dumps(self.__dict__, cls=CustomEncoder)