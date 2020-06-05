class GameStateService:
    '''
        This class deals with the creation, updation, retrieval and disposal of game state.
    '''
    def __init__(self, state):
        self.state = state

    def update_state(self, state):
        self.state = state

    def get_state(self, state):
        return self.state