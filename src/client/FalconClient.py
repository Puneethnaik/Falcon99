import websockets
import os
import json
import chess
import random
import asyncio

class NQueensSolver:
    def __init__(self, size_of_chess_board, number_of_queens, initial_population_size):
        self.size_of_chess_board = size_of_chess_board
        self.number_of_queens = number_of_queens
        self.initial_population_size = initial_population_size
        self.population = []
        for i in range(self.initial_population_size):
            self.population.append(self.create_random_chromosome())
        #sort and rank the population according to the fitness values of each chromosome
        self.population.sort(key=lambda chromosome: self.fitness(chromosome))

    def fitness(self, chromosome):
        number_of_clashing_queens = 0
        for i in range(len(chromosome)):
            gene1 = chromosome[i]
            for j in range(len(chromosome)):
                gene2 = chromosome[j]
                if (gene2 + j == gene1 + i) or (abs(gene2 - j) == abs(gene1 - i)) or (gene1 == gene2):
                    number_of_clashing_queens += 1
        number_of_clashing_queens = number_of_clashing_queens / 2
        return 1 / (1 + number_of_clashing_queens)
    def create_random_chromosome(self):
        return [random.randint(1, self.size_of_chess_board) for _ in range(self.number_of_queens)]

    def convert_chromosome_to_FEN(self, chromosome):
        chessboard = chess.Board("8/8/8/8/8/8/8/8 w - - 0 1")
        positions = [
            [chess.A1, chess.A2, chess.A3, chess.A4, chess.A5, chess.A6, chess.A7, chess.A8],
            [chess.B1, chess.B2, chess.B3, chess.B4, chess.B5, chess.B6, chess.B7, chess.B8],
            [chess.C1, chess.C2, chess.C3, chess.C4, chess.C5, chess.C6, chess.C7, chess.C8],
            [chess.D1, chess.D2, chess.D3, chess.D4, chess.D5, chess.D6, chess.D7, chess.D8],
            [chess.E1, chess.E2, chess.E3, chess.E4, chess.E5, chess.E6, chess.E7, chess.E8],
            [chess.F1, chess.F2, chess.F3, chess.F4, chess.F5, chess.F6, chess.F7, chess.F8],
            [chess.G1, chess.G2, chess.G3, chess.G4, chess.G5, chess.G6, chess.G7, chess.G8],
            [chess.H1, chess.H2, chess.H3, chess.H4, chess.H5, chess.H6, chess.H7, chess.H8],
        ]
        for i in range(len(chromosome)):
            chessboard.set_piece_at(positions[chromosome[i] - 1][i], chess.Piece(piece_type=chess.QUEEN, color=chess.WHITE))
        return chessboard.fen()


class FalconClient:
    def __init__(self, server_domain, port, resource_name):
        self.server_domain = server_domain
        self.port = port
        self.resource_name = resource_name
        self.nqueens_solver = NQueensSolver(nq=3, maxFitness=3, generation=1)
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
            population = self.nqueens_solver.generate_population()
            game_state = {}
            for i in range(len(population)):
                game_state["individual"+str(i)] = {
                    "chromosome": self.nqueens_solver.convert_chromosome_to_FEN(population[i]),
                    "fitness": self.nqueens_solver.fitness(population[i])
                }

            # chess_board = chess.Board(game_state.get("individual_one"))
            # print(random.choice(list(chess_board.legal_moves)))
            # chess_board.push(random.choice(list(chess_board.legal_moves)))
            # game_state["individual_one"] = chess_board.fen()

            await asyncio.sleep(1)
            await self.connection.send(json.dumps(game_state))

    def prepare_uri(self):
        '''
        Return a URI of the service to be accessed from the server whose
        information passed in the constructor
        :return: URI as a string
        '''
        uri = "ws://" + os.path.join(self.server_domain + ":" + str(self.port), self.resource_name)
        return uri