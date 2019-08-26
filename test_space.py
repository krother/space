
from unittest.mock import patch
from space import SpaceGame, create_galaxy
import pytest
from ships import Spaceship
import views

COMPLETE_SOLUTION = open('solution.txt').read().strip()

views.SKIP_INPUT = True

@pytest.fixture
def space():
    galaxy = create_galaxy()
    return SpaceGame(galaxy[0])

def travel(galaxy, keys):
    """executes some game moves"""
    for k in keys:
        galaxy.move(k)

class TestSpace:

    def test_pickup(self, space):
        space.move(3)
        assert space.ship.cargo == 'food'

    def test_warp(self, space):
        space.move(1)
        assert space.ship.location.name == 'Centauri'

    def test_triple_warp(self, space):
        travel(space, [1, 1, 1])
        assert space.ship.location.name == 'New Haven'

    def test_pickup_artifact(self, space):
        travel(space, [1, 5, 3, 1, 4, 4, 2])
        assert space.ship.artifacts == 1

    def test_aquacity_puzzle(self, space):
        travel(space, [4, 2, 3, 4])
        assert space.ship.artifacts == 0
        assert space.ship.cargo == 'medical'
        assert space.ship.location.active
        travel(space, [3, 9])
        assert space.ship.cargo == ''
        assert space.ship.artifacts == 1
        assert not space.ship.location.active

    def test_finish_game(self, space):
        solution = [int(x) for x in COMPLETE_SOLUTION]
        travel(space, solution)
        print(space.ship.artifacts)
        print(space.ship.location.name)
        assert space.solved
