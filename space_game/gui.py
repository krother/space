"""
Space Traveller - graphical user interface
"""

import os
import time

import arcade
from arcade import key as akeys
from arcade.key import ESCAPE

from space_game.config import BASE_PATH
from space_game.galaxy import GalaxyGraph
from space_game.game import SpaceGame
from space_game.lang import LANG, TEXT
from space_game.views import FONT_SETTINGS, IMAGES, SLOW_MOTION, print_message


SIZEX, SIZEY = (1500, 1000)

MOVES = {
    akeys.NUM_1: 1,
    akeys.NUM_2: 2,
    akeys.NUM_3: 3,
    akeys.NUM_4: 4,
    akeys.NUM_5: 5,
    akeys.NUM_6: 6,
    akeys.NUM_7: 7,
    akeys.NUM_8: 8,
    akeys.NUM_9: 9,
    akeys.KEY_1: 1,
    akeys.KEY_2: 2,
    akeys.KEY_3: 3,
    akeys.KEY_4: 4,
    akeys.KEY_5: 5,
    akeys.KEY_6: 6,
    akeys.KEY_7: 7,
    akeys.KEY_8: 8,
    akeys.KEY_9: 9,
}


def start_new_game():
    galaxy = GalaxyGraph.create_galaxy(
        os.path.join(BASE_PATH, f"galaxy_{LANG}.json")
    )
    game = SpaceGame(location=galaxy["Pandalor"])
    return game


class SpaceGameWindow(arcade.Window):
    def __init__(self, no_window=False):
        if not no_window:
            super().__init__(SIZEX, SIZEY, "Space", update_rate=0.2)
            arcade.set_background_color(arcade.color.BLACK)
        self.game = start_new_game()
        self.commands = list(self.game.get_commands())
        self._keylog = ""

    def on_draw(self):
        arcade.start_render()
        self.draw_game()
        self.draw_location()
        self.draw_commands()
        if self.game.message:
            print_message(self.game.message)
        arcade.finish_render()
        if self.game.message:
            arcade.pause(0.1)

    def update(self, delta_time):
        # pylint: disable=unused-argument
        if self.game.solved:
            arcade.pause(5.0)
            arcade.window_commands.close_window()

    def draw_commands(self):
        commands = TEXT["Available commands"] + ":\n\n"
        for i, cmd in enumerate(self.commands, 1):
            commands += f"[{i}] {cmd.name}\n"
        commands += "\n[Esc] Exit"
        arcade.draw_text(
            text=commands,
            start_x=300,
            start_y=600,
            width=600,
            multiline=True,
            **FONT_SETTINGS,
        )

    def draw_game(self) -> None:
        """Draws the players inventory"""
        arcade.draw_text(
            text=TEXT["cargo bay"],
            start_x=800,
            start_y=600,
            **FONT_SETTINGS,  # type: ignore
        )
        arcade.draw_text(
            text=TEXT["crew"],
            start_x=800,
            start_y=400,
            **FONT_SETTINGS,  # type: ignore
        )

        if self.game.cargo:
            IMAGES[self.game.cargo].draw_sized(870, 500, 128, 128)
        for i, c in enumerate(self.game.crew):
            IMAGES[c].draw_sized(870 + i * 120, 320, 96, 96)

    def draw_location(self) -> None:
        IMAGES[self.game.location.image].draw_sized(150, 850, 200, 200)
        arcade.draw_text(
            text=self.game.location.name,
            start_x=300,
            start_y=950,
            bold=True,
            **FONT_SETTINGS,  # type: ignore
        )
        arcade.draw_text(
            text=self.game.location.description,
            start_x=300,
            start_y=900,
            multiline=True,
            width=600,
            **FONT_SETTINGS,  # type: ignore
        )

    def move(self, key):
        """Processes a key pressed"""
        for i, cmd in enumerate(self.commands, 1):
            if key == i:
                if SLOW_MOTION:
                    time.sleep(3)
                cmd.execute()
                self.commands = list(self.game.get_commands())

    def on_key_press(self, symbol, modifiers):
        """Handle player movement"""
        # pylint: disable=unused-argument
        key = MOVES.get(symbol, " ")
        self._keylog += str(key)
        self.move(key)
        if symbol == ESCAPE:
            arcade.window_commands.close_window()


def main():
    sg = SpaceGameWindow()
    arcade.run()
    # print(sg._keylog)


if __name__ == "__main__":
    main()
