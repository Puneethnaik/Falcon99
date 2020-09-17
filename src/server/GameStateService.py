from src.server.CustomEncoder import CustomEncoder
import json
class GameStateService:
    '''
        This class deals with the creation, updation, retrieval and disposal of game state.
    '''
    def __init__(self, state):
        self.state = state

    def update_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def toJSON(self):
        return json.dumps(self.__dict__, cls=CustomEncoder)