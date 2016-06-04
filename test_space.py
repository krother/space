
from unittest import TestCase, main
from unittest.mock import patch
from space import SpaceGame, GALAXY
from locations import AncientShipwreck
from ships import Spaceship


PICKUP = iter('Fx')
MOVE = iter('1x')
TRIPLE_JUMP = iter('111x')
FIRST_ARTIFACT = iter('1N4t_x')

class SpaceTests(TestCase):

    @patch('builtins.input', lambda x:next(PICKUP))
    def test_pickup(self):
        sg = SpaceGame(GALAXY)
        sg.travel()
        self.assertEqual(sg.ship.cargo, 'food')

    @patch('builtins.input', lambda x:next(MOVE))
    def test_warp(self):
        sg = SpaceGame(GALAXY)
        sg.travel()
        self.assertEqual(sg.ship.location.name, 'Centauri')

    @patch('builtins.input', lambda x:next(TRIPLE_JUMP))
    def test_triple_warp(self):
        sg = SpaceGame(GALAXY)
        sg.travel()
        self.assertEqual(sg.ship.location.name, 'New Haven')

    @patch('builtins.input', lambda *args:next(FIRST_ARTIFACT))
    def test_pickup_artifact(self):
        sg = SpaceGame(GALAXY)
        sg.travel()
        self.assertEqual(sg.ship.artifacts, 1)

    @patch('builtins.input', lambda :None)
    def test_other_input(self):
        asw = AncientShipwreck()
        ship = Spaceship()
        asw.contact(ship)
        self.assertEqual(ship.artifacts, 0)
        ship.cargo = 'nucleons'
        asw.contact(ship)
        self.assertEqual(ship.artifacts, 1) 



if __name__ == '__main__':
    main(buffer=True)
