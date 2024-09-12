"""
Space Traveller - graphical user interface
"""

import os
import sys

from space_game.lang import LANG, TEXT
from space_game.location import create_galaxy
from space_game.game import SpaceGame
from space_game.config import BASE_PATH


galaxy = create_galaxy(os.path.join(BASE_PATH, f"galaxy_{LANG}.json"))
game = SpaceGame(location=galaxy["Pandalor"])

while not game.solved:

    print("-" * 60)
    print("location: ", game.location.name)
    print("          ", game.location.description)
    print()
    print("cargo   : ", game.cargo)
    print("crew    : ", ", ".join(game.crew))
    print()

    if game.message:
        print(game.message)
        print("<press enter>")
        input()

    commands = game.get_commands()
    print(TEXT["Available commands"], "\n")
    for i, cmd in enumerate(commands, 1):
        print( f"[{i}] {cmd.name}")
    print("[x] Exit")

    key = input("\nenter command: ")
    if key == "x":
        sys.exit(0)
    else:
        cmd = commands[int(key) - 1]
        cmd.callback()
