import pytest

from space_game import views
from space_game.gui import SpaceGameWindow


COMPLETE_SOLUTION = open("solution.txt", encoding="utf-8").read().strip()

views.SKIP_INPUT = True


@pytest.fixture
def space_gui():
    return SpaceGameWindow(no_window=True)


def travel(galaxy, keys):
    """execute some game moves"""
    for k in keys:
        galaxy.move(k)


class TestSpace:
    # pylint: disable=redefined-outer-name

    def test_pickup(self, space_gui):
        space_gui.move(3)
        assert space_gui.game.cargo == "food"

    def test_warp(self, space_gui):
        space_gui.move(1)
        assert space_gui.game.location.name == "Centauri"

    def test_triple_warp(self, space_gui):
        travel(space_gui, [1, 1, 1])
        assert space_gui.game.location.name == "New Haven"

    def test_pickup_elephant(self, space_gui):
        travel(space_gui, [1, 5, 3, 1, 4, 4, 2])
        assert "slon1" in space_gui.game.crew

    def test_aquacity_puzzle(self, space_gui):
        travel(space_gui, [4, 2, 3, 4])
        assert "pingu" not in space_gui.game.crew
        assert space_gui.game.cargo == "medical"
        assert space_gui.game.location.active
        travel(space_gui, [3, 9])
        assert space_gui.game.cargo == ""
        assert "pingu" in space_gui.game.crew
        assert not space_gui.game.location.active

    def test_finish_game(self, space_gui):
        solution = [int(x) for x in COMPLETE_SOLUTION]
        travel(space_gui, solution)
        assert space_gui.game.solved
