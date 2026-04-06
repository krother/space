"""
Space Traveller - graphical user interface
"""

import sys

from space_game.lang import TEXT
from space_game.facade import start_game, execute_command, GameData



def select_command(game) -> GameData:
    print(TEXT["Available commands"], "\n")
    for i, cmd in enumerate(game.commands, 1):
        print(f"[{i}] {cmd}")
    print("[x] Exit")
    key = input("\nenter command: ")
    if key == "x":
        finish()
    else:
        cmd = game.commands[int(key) - 1]
        return execute_command(game.game_id, cmd)


def finish():
    sys.exit(0)


def main():
    game = start_game()
    while not game.solved:
        print(game)
        game = select_command(game)


if __name__ == "__main__":
    main()
