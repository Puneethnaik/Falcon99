import websockets
import os
import json
import chess
import random
import numpy
import asyncio


#Stockfish dependency
import stockfish

class NQueensSolver:
    def __init__(self, number_of_queens, initial_population_size):
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
                if i == j:
                    continue
                gene2 = chromosome[j]
                if (gene2 + j == gene1 + i) or (abs(gene2 - j) == abs(gene1 - i)) or (gene1 == gene2):
                    number_of_clashing_queens += 1
        number_of_clashing_queens = number_of_clashing_queens / 2
        return 1 / (1 + number_of_clashing_queens)
    def next_generation(self):
        #choose the two best individuals
        adam = self.population[-1]
        eve = self.population[-2]
        radam = random.choice(self.population)
        reve = random.choice(self.population)
        rchild = self.crossover(radam, reve)
        # print("Rchild fitness", self.fitness(rchild))
        #adam and eve create a new generation
        #create children with crossover function
        new_population = []
        for i in range(self.initial_population_size):
            child = self.crossover(adam, eve)
            if random.random() <= 0.8:
                self.mutate(1, child)
            elif random.random() <= 0.4:
                self.mutate(2, child)
            new_population.append(child)
        # if self.fitness(rchild) > self.fitness(new_population[0]):
        #     new_population[0] = rchild
        new_population.sort(key=lambda chromosome: self.fitness(chromosome))
        self.population = new_population
    def crossover(self, adam, eve):
        #We use order 1 crossover
        adami = random.randint(0, len(adam))
        adamj = random.randint(adami, len(adam))
        adam_alleles = adam[adami:adamj + 1]
        eve_alleles = []
        for allele in eve:
            if allele not in adam_alleles:
                eve_alleles.append(allele)
        child = [0]*len(adam)
        eve_counter = 0
        for i in range(len(adam)):
            if i >= adami and i <= adamj:
                child[i] = adam_alleles[i - adami]
            else:
                child[i] = eve_alleles[eve_counter]
                eve_counter += 1
        return child

    def create_random_chromosome(self):
        return numpy.random.permutation(self.number_of_queens)
    def mutate(self, number, chromosome):
        if number >= 1:
            randomi = random.randint(0, len(chromosome) - 1)
            randomj = random.randint(0, len(chromosome) - 1)
            chromosome[randomi], chromosome[randomj] = chromosome[randomj], chromosome[randomi]
        if number >= 2:
            randomi = random.randint(0, len(chromosome) - 1)
            randomj = random.randint(0, len(chromosome) - 1)
            chromosome[randomi], chromosome[randomj] = chromosome[randomj], chromosome[randomi]
        return chromosome

    def convert_chromosome_to_FEN(self, chromosome):
        chessboard = chess.Board("8/8/8/8/8/8/8/8 w - - 0 1")
        positions = [
            [chess.H1, chess.H2, chess.H3, chess.H4, chess.H5, chess.H6, chess.H7, chess.H8],
            [chess.G1, chess.G2, chess.G3, chess.G4, chess.G5, chess.G6, chess.G7, chess.G8],
            [chess.F1, chess.F2, chess.F3, chess.F4, chess.F5, chess.F6, chess.F7, chess.F8],
            [chess.E1, chess.E2, chess.E3, chess.E4, chess.E5, chess.E6, chess.E7, chess.E8],
            [chess.D1, chess.D2, chess.D3, chess.D4, chess.D5, chess.D6, chess.D7, chess.D8],
            [chess.C1, chess.C2, chess.C3, chess.C4, chess.C5, chess.C6, chess.C7, chess.C8],
            [chess.B1, chess.B2, chess.B3, chess.B4, chess.B5, chess.B6, chess.B7, chess.B8],
            [chess.A1, chess.A2, chess.A3, chess.A4, chess.A5, chess.A6, chess.A7, chess.A8],
        ]
        for i in range(len(chromosome)):
            chessboard.set_piece_at(positions[chromosome[i] - 1][i], chess.Piece(piece_type=chess.QUEEN, color=chess.WHITE))
        return chessboard.fen()


class StockFishClient:
    def __init__(self):
        self.engine = stockfish.Stockfish()
    def set_position(self, moves):
        print("Setting as the fen of the board", moves)
        self.engine.set_position(moves)
        print(self.engine.get_board_visual())
    def make_move(self):
        best_move = self.engine.get_best_move()
        print("The best move is", best_move)
        # self.engine.set_position([best_move])
        # print(self.engine.get_board_visual())
        return best_move

class FalconClient:
    def __init__(self, server_domain, port, resource_name, game_manager_id, player_id):
        self.server_domain = server_domain
        self.port = port
        self.resource_name = resource_name
        self.game_manager_id = game_manager_id
        self.stockfish_solver = StockFishClient()
        self.player_id = player_id
        self.moves = []
        # self.nqueens_solver = NQueensSolver(number_of_queens=8, initial_population_size=1000)
    async def connect(self):
        uri = self.prepare_uri()
        print(uri)
        try:
            self.connection = await websockets.connect(uri)
            await self.run()
        except websockets.ConnectionClosed as e:
            print("Could not connect to the server. Details", e)
    async def run(self):
        while True:
            message = await self.connection.recv()
            print("[%s %s]The message recieved is %s" % (self.game_manager_id, self.player_id, message))
            # self.nqueens_solver.next_generation()
            # game_state = {}
            # for i in range(len(self.nqueens_solver.population)):
            #     game_state["individual"+str(i)] = {
            #         "chromosome": self.nqueens_solver.convert_chromosome_to_FEN(self.nqueens_solver.population[i]),
            #         "fitness": self.nqueens_solver.fitness(self.nqueens_solver.population[i])
            #     }
            game_state = json.loads(message)
            self.stockfish_solver.set_position(game_state["moves"])
            self.moves = game_state["moves"]
            game_state = {}
            self.moves.append(self.stockfish_solver.make_move())
            game_state["moves"] = self.moves

            # chess_board = chess.Board(game_state.get("individual_one"))
            # print(random.choice(list(chess_board.legal_moves)))
            # chess_board.push(random.choice(list(chess_board.legal_moves)))
            # game_state["individual_one"] = chess_board.fen()

            # await asyncio.sleep(1)
            print("Sending this state to server", game_state)
            await self.connection.send(json.dumps(game_state))

    def prepare_uri(self):
        '''
        Return a URI of the service to be accessed from the server whose
        information passed in the constructor
        :return: URI as a string
        '''
        uri = "ws://" + os.path.join(self.server_domain + ":" + str(self.port), self.game_manager_id, self.resource_name, self.player_id)
        return uri