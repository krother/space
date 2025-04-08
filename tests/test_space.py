"""
Unit Tests for the GUI.

These tests hijack the keyboard and enter keys.
"""

import os

import pytest

from space_game import views
from space_game.gui import SpaceGameWindow

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(BASE_PATH, "test_data")
SOLUTION_FILE = os.path.join(TEST_DATA_PATH, "solution.txt")
COMPLETE_SOLUTION = open(SOLUTION_FILE, encoding="utf-8").read().strip()

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
        """Press one key to pick up an item"""
        space_gui.move(3)
        assert space_gui.game.cargo == "bamboo"

    def test_warp(self, space_gui):
        """After one step, you arrive in the B-Soup system"""
        space_gui.move(1)
        assert space_gui.game.location.name == "B-Soup"

    def test_triple_warp(self, space_gui):
        """Going to Colabo requires three jumps"""
        travel(space_gui, [1, 1, 1])
        assert space_gui.game.location.name == "Colabo"

    def test_pickup_python(self, space_gui):
        """recruit the Python character to your crew"""
        travel(space_gui, [1, 1, 1, 4, 3, 2, 3, 4, 2])
        assert "python" in space_gui.game.crew

    def test_aquacity_puzzle(self, space_gui):
        """trade bamboo for DNA on Kubernety"""
        travel(space_gui, [3, 2, 3, 4])
        assert "pingu" not in space_gui.game.crew
        assert space_gui.game.cargo == "bamboo"
        assert space_gui.game.location.active
        travel(space_gui, [3])
        assert "dna" in space_gui.game.cargo

    def test_finish_game(self, space_gui):
        """when entering the complete solution, the game is finished"""
        solution = [int(x) for x in COMPLETE_SOLUTION]
        travel(space_gui, solution)
        assert space_gui.game.solved
