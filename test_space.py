
from unittest.mock import patch
from space import SpaceGame, create_galaxy
from locations import AncientShipwreck
from ships import Spaceship
import views
import pytest

PICKUP = iter('Fx')
MOVE = iter('1x')
TRIPLE_JUMP = iter('111x')
FIRST_ARTIFACT = iter('1N4t_x')
COMPLETE_SOLUTION = iter(open('solution.txt').read())

views.SKIP_INPUT = True

@pytest.fixture
def galaxy():
    return create_galaxy()


class TestSpace:

    @patch('builtins.input', lambda x: next(PICKUP))
    def test_pickup(self, galaxy):
        sg = SpaceGame(galaxy)
        sg.travel()
        assert sg.ship.cargo == 'food'

    @patch('builtins.input', lambda x: next(MOVE))
    def test_warp(self, galaxy):
        sg = SpaceGame(galaxy)
        sg.travel()
        assert sg.ship.planet.name == 'Centauri'

    @patch('builtins.input', lambda x: next(TRIPLE_JUMP))
    def test_triple_warp(self, galaxy):
        sg = SpaceGame(galaxy)
        sg.travel()
        assert sg.ship.planet.name == 'New Haven'

    @patch('builtins.input', lambda *args: next(FIRST_ARTIFACT))
    def test_pickup_artifact(self, galaxy):
        sg = SpaceGame(galaxy)
        sg.travel()
        assert sg.ship.artifacts == 1

    @staticmethod
    @patch('builtins.input', lambda: None)
    def test_other_input():
        asw = AncientShipwreck()
        ship = Spaceship()
        asw.contact(ship)
        assert ship.artifacts == 0
        ship.cargo = 'nucleons'
        asw.contact(ship)
        assert ship.artifacts == 1

    @patch('builtins.input', lambda x: next(COMPLETE_SOLUTION))
    def test_finish_game(self, galaxy):
        sg = SpaceGame(galaxy)
        sg.travel()
        assert sg.solved
