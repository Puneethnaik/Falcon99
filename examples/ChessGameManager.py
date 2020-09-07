from src.server.GameManager import GameManager
import chess
import json
from src.server.GameStateService import GameStateService

class ChessGameManager(GameManager):
    def __init__(self):
        super.__init__()
        empty_chess_board = chess.Board()
        self.game_state_service = GameStateService({
            "fen": empty_chess_board.fen()
        })
    async def run(self):
        print("Game manager %d running game event loop" % self.id)
        while (True):
            player = self.get_player("first_player")
            await player.get("websocket").send(json.dumps(self.game_state_service.get_state()))
            action = await player.get("websocket").recv()
            print("Recieved action", action)
            self.game_state_service.update_state(json.loads(action))
            # self.game_state_service.update_state(self.game_manager.get_second_player().make_turn())
            if self.has_achieved_winning_state(self.game_state_service.state):
                break