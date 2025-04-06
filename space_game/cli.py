"""
Space Traveller - graphical user interface
"""

import os
import sys

from space_game.config import BASE_PATH
from space_game.galaxy import GalaxyGraph
from space_game.game import SpaceGame
from space_game.lang import LANG, TEXT


def start_game():
    galaxy = GalaxyGraph.create_galaxy(
        os.path.join(BASE_PATH, f"galaxy_{LANG}.json")
    )
    return SpaceGame(location=galaxy["Pandalor"])


def print_game_state(game):
    print("-" * 60)
    print("location: ", game.location.name)
    print("          ", game.location.description)
    print()
    print("cargo   : ", game.cargo)
    print("crew    : ", ", ".join(game.crew))
    print()


def wait_for_message(game):
    if game.message:
        print(game.message)
        print("<press enter>")
        input()


def select_command(game):
    commands = list(game.get_commands())
    print(TEXT["Available commands"], "\n")
    for i, cmd in enumerate(commands, 1):
        print(f"[{i}] {cmd.name}")
    print("[x] Exit")
    key = input("\nenter command: ")
    if key == "x":
        finish()
    else:
        cmd = commands[int(key) - 1]
        cmd.execute()


def finish():
    sys.exit(0)


def main():
    game = start_game()
    while not game.solved:
        print_game_state(game)
        wait_for_message(game)
        select_command(game)


if __name__ == "__main__":
    main()
