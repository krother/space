import pytest

from space_game import views
from space_game.space import SpaceGame, create_galaxy


COMPLETE_SOLUTION = open("solution.txt", encoding="utf-8").read().strip()

views.SKIP_INPUT = True


@pytest.fixture
def space():
    galaxy = create_galaxy()
    return SpaceGame(galaxy[0], no_window=True)


def travel(galaxy, keys):
    """execute some game moves"""
    for k in keys:
        galaxy.move(k)


class TestSpace:
    # pylint: disable=redefined-outer-name

    def test_pickup(self, space):
        space.move(3)
        assert space.ship.cargo == "food"

    def test_warp(self, space):
        space.move(1)
        assert space.ship.location.name == "Centauri"

    def test_triple_warp(self, space):
        travel(space, [1, 1, 1])
        assert space.ship.location.name == "New Haven"

    def test_pickup_elephant(self, space):
        travel(space, [1, 5, 3, 1, 4, 4, 2])
        assert "slon1" in space.ship.crew

    def test_aquacity_puzzle(self, space):
        travel(space, [4, 2, 3, 4])
        assert "pingu" not in space.ship.crew
        assert space.ship.cargo == "medical"
        assert space.ship.location.active
        travel(space, [3, 9])
        assert space.ship.cargo == ""
        assert "pingu" in space.ship.crew
        assert not space.ship.location.active

    def test_finish_game(self, space):
        solution = [int(x) for x in COMPLETE_SOLUTION]
        travel(space, solution)
        assert space.solved
