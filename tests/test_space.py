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
        assert space_gui.game.cargo == "bamboo"

    def test_warp(self, space_gui):
        space_gui.move(1)
        assert space_gui.game.location.name == "B-Soup"

    def test_triple_warp(self, space_gui):
        travel(space_gui, [1, 1, 1])
        assert space_gui.game.location.name == "Colabo"

    def test_pickup_python(self, space_gui):
        travel(space_gui, [1, 1, 1, 4, 3, 2, 3, 4, 2])
        assert "python" in space_gui.game.crew

    def test_aquacity_puzzle(self, space_gui):
        travel(space_gui, [3, 2, 3, 4])
        assert "pingu" not in space_gui.game.crew
        assert space_gui.game.cargo == "bamboo"
        assert space_gui.game.location.active
        travel(space_gui, [3])
        assert "dna" in space_gui.game.cargo

    def test_finish_game(self, space_gui):
        solution = [int(x) for x in COMPLETE_SOLUTION]
        travel(space_gui, solution)
        assert space_gui.game.solved
