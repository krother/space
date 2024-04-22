"""
Space Traveller - graphical user interface
"""

import time

import arcade
from arcade import key as akeys
from arcade.key import ESCAPE

from space_game.facade import start_game, execute_command, GameData
from space_game.lang import LANG, TEXT
from space_game.views import IMAGES, FONT_SETTINGS, SLOW_MOTION, print_message


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


class SpaceGameWindow(arcade.Window):
    def __init__(self, no_window=False):
        if not no_window:
            super().__init__(SIZEX, SIZEY, "Space", update_rate=0.2)
            arcade.set_background_color(arcade.color.BLACK)
        self.game = start_game()  # old: start_new_game()
        # self.commands = self.game.get_commands() # removed
        self._keylog = ""

    def on_draw(self):
        arcade.start_render()
        self.draw_game()  #self.game.draw()
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

    # moved here from game.py
    def draw_game(self) -> None:
        """Draws the players inventory"""
        arcade.draw_text(text=TEXT['cargo bay'], start_x=800, start_y=600, **FONT_SETTINGS)
        arcade.draw_text(text=TEXT['crew'], start_x=800, start_y=400, **FONT_SETTINGS)

        if self.game.cargo:
            IMAGES[self.game.cargo].draw_sized(870, 500, 128, 128)
        for i, c in enumerate(self.game.crew):
            IMAGES[c].draw_sized(870 + i * 120, 320, 96, 96)

    def draw_commands(self):
        commands = TEXT["Available commands"] + ":\n\n"
        for i, cmd in enumerate(self.game.commands, 1):  # added game.
            commands += f"[{i}] {cmd}\n"   # old: cmd.name
        commands += "\n[Esc] Exit"
        arcade.draw_text(
            text=commands,
            start_x=300,
            start_y=600,
            width=600,
            multiline=True,
            **FONT_SETTINGS,
        )

    def draw_location(self) -> None:
        IMAGES[self.game.location.image].draw_sized(150, 850, 200, 200)
        arcade.draw_text(text=self.game.location.name, start_x=300, start_y=950, bold=True, **FONT_SETTINGS)
        arcade.draw_text(
            text=self.game.location.description, start_x=300, start_y=900, multiline=True, width=600, **FONT_SETTINGS
        )

    def move(self, key):
        """Processes a key pressed"""
        for i, cmd in enumerate(self.game.commands, 1):  # old: self.commands
            if key == i:
                if SLOW_MOTION:
                    time.sleep(3)
                # old: cmd.callback()
                # old: self.commands = self.game.get_commands()
                self.game = execute_command(self.game.game_id, cmd)

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
