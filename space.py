'''
Space Traveller - main app
'''

__author__ = "Kristian Rother"


import time
from ships import Spaceship
from planets import create_galaxy
from views import outro, print_message
import views
import re
import random
import arcade
from arcade.key import ESCAPE, SPACE
from arcade import key as akeys
from lang import EN as TEXT


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


class SpaceGame(arcade.Window):

    def __init__(self, start_location):
        super().__init__(SIZEX, SIZEY, "Space", update_rate=0.2)
        arcade.set_background_color(arcade.color.BLACK)
        self.ship = Spaceship()
        self.ship.location = start_location
        self.commands = self.ship.get_commands()
        self.message = ''
        self._keylog = ''

    def on_draw(self):
        arcade.start_render()
        self.ship.location.draw()
        self.ship.draw()
        self.draw_commands()
        if self.message:
            print_message(self.message)
            arcade.finish_render()
            arcade.pause(0.5)

    def update(self, time_delta):
        if self.solved:
            outro()
            arcade.window_commands.close_window()

    @property
    def solved(self):
        location = self.ship.location
        return location.name == TEXT['Alien Space Station'] and not location.active

    def draw_commands(self):
        commands = TEXT["Available commands"] + ":\n\n"
        for i, cmd in enumerate(self.commands, 1):
            commands += f"[{i}] {cmd.description}\n"
        commands += "\n[Esc] Exit"
        arcade.draw_text(commands, 300, 600, arcade.color.GREEN, 20, font_name='GARA', anchor_y="top")

    def move(self, key):
        """Processes a key pressed"""
        if self.message:
            self.message = ''  # delete displayed message
            return

        for i, cmd in enumerate(self.commands, 1):
            if key == i:
                if views.SLOW_MOTION:
                    time.sleep(3)
                self.message = cmd.action()
                self.commands = self.ship.get_commands()

    def on_key_press(self, symbol, mod):
        """Handle player movement"""
        key = MOVES.get(symbol, ' ')
        self._keylog += str(key)
        self.move(key)
        if symbol == ESCAPE:
            arcade.window_commands.close_window()


if __name__ == '__main__':
    galaxy = create_galaxy('galaxy.json')
    sg = SpaceGame(galaxy[0])
    arcade.run()
    print(sg._keylog)
