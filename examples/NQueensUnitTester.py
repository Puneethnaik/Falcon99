import unittest
from src.client.FalconClient import NQueensSolver
import numpy as np

class MyTestCase(unittest.TestCase):
    def test_crossover(self):
        nqueens_solver = NQueensSolver(number_of_queens=8, initial_population_size=100)
        chromosome1 = np.random.permutation(nqueens_solver.number_of_queens)
        chromosome2 = np.random.permutation(nqueens_solver.number_of_queens)

        #check that the crossover happens normally, that is the alleles present in the child are all
        #unique
        allele_count = {

        }
        child = nqueens_solver.crossover(chromosome1, chromosome2)
        for allele in child:
            try:
                allele_count[allele] += 1
            except KeyError:
                allele_count[allele] = 1
        for value in allele_count.values():
            self.assertEqual(value, 1)
        for i in range(nqueens_solver.number_of_queens):
            self.assertTrue(i in allele_count.keys())
    def test_fitness(self):
        nqueens_solver = NQueensSolver(number_of_queens=8, initial_population_size=100)
        chromosome = [8, 1, 5, 3, 4, 2, 7, 6]
        self.assertEqual(nqueens_solver.fitness(chromosome), 1/7)
    def test_convergence(self):
        nqueens_solver = NQueensSolver(number_of_queens=8, initial_population_size=100)
        count = 2000
        prev = -1
        while count > 0:
            nqueens_solver.next_generation()
            current_best_fitness = nqueens_solver.fitness(nqueens_solver.population[-1])
            self.assertTrue(current_best_fitness >= prev)
            prev = current_best_fitness
            count -= 1
        print("The best fitness is", nqueens_solver.fitness(nqueens_solver.population[-1]))

if __name__ == '__main__':
    unittest.main()
