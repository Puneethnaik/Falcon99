import unittest

from src.client.FalconClient import StockFishClient

class MyTestCase(unittest.TestCase):
    def test_something(self):
        client = StockFishClient()
        client.engine.set_fen_position("rn1qkbnr/ppp1pppp/8/3p4/3P2b1/4PN2/PPP2PPP/RNBQKB1R b KQkq - 0 3")
        best_move = client.engine.get_best_move()
        print(best_move)
        client.engine.set_position([best_move])
        self.assertEqual(client.engine.)

if __name__ == '__main__':
    unittest.main()
