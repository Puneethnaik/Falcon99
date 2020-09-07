class GameInformation:
    def __init__(self, name, description, game_port, stream_port, service_name, server_domain):
        self.name = name
        self.description = description
        self.game_port = game_port
        self.stream_port = stream_port
        self.service_name = service_name
        self.server_domain = server_domain

    def getByName(name):
        #TODO implement a database layer that fetches this information from the database
        game_information = GameInformation(service_name="NQueensGame",
                                           game_port=4000,
                                           stream_port=5000,
                                           server_domain="localhost",
                                           name="N Queens Puzzle",
                                           description="This is a N Queens Game")
        return game_information