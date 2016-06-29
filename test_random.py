
from unittest import TestCase, main
from unittest.mock import patch
from space import SpaceGame, GALAXY
from random import choice
import time

class SpaceTests(TestCase):

    def setUp(self):
        self.moves = 0

    def random_move(*args):
        char = choice("1234cptBFGMNO")
        #time.sleep(0.3)
        return char

    @patch('builtins.input', random_move)
    def test_pickup_artifact(self):
        sg = SpaceGame(GALAXY)
        sg.travel()


if __name__ == '__main__':
    main(buffer=True)
