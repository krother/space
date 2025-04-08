"""
Unit Tests for the CLI.

These tests hijack the keyboard and enter keys.
"""

import os

from unittest.mock import patch, MagicMock

from space_game.cli import start_game, select_command


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(BASE_PATH, "test_data")
SOLUTION_FILE = os.path.join(TEST_DATA_PATH, "solution.txt")
COMPLETE_SOLUTION = open(SOLUTION_FILE, encoding="utf-8").read().strip()


class TestSpace:

    def test_pickup(self):
        """Press one key to pick up an item"""
        game = start_game()
        with patch("builtins.input", side_effect=["3"]):
            select_command(game) 
            assert game.cargo == "bamboo"

    def test_triple_warp(self):
        """Going to Colabo requires three jumps"""
        game = start_game()
        with patch("builtins.input", side_effect=["1", "1", "1"]):
            for _ in range(3):
                select_command(game) 
            assert game.location.name == "Colabo"

    def test_exit(self):
        """Exit key works"""
        game = start_game()
        m = MagicMock()
        with patch("builtins.input", side_effect=["x"]):
            with patch("space_game.cli.finish", m):
                select_command(game)
        assert m.assert_called
        assert m.call_count == 1
