import websockets
import os
import json
import chess

class FalconClient:
    def __init__(self, server_domain, port, resource_name):
        self.server_domain = server_domain
        self.port = port
        self.resource_name = resource_name
    async def connect(self):
        uri = self.prepare_uri()
        print(uri)
        try:
            self.connection = await websockets.connect(uri)
            await self.run()
        except Exception as e:
            print("Could not connect to the server. Details", e)
    async def run(self):
        while True:
            message = await self.connection.recv()
            print("The message recieved is", message)
            await self.connection.send(json.dumps(chess.Board().fen()))

    def prepare_uri(self):
        '''
        Return a URI of the service to be accessed from the server whose
        information passed in the constructor
        :return: URI as a string
        '''
        uri = "ws://" + os.path.join(self.server_domain + ":" + str(self.port), self.resource_name)
        return uri