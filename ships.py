
from functools import partial
from collections import namedtuple
import arcade
from views import IMAGES
from lang import TEXT

Command = namedtuple('Command', ('description', 'action'))

TRANSITIONS = {
    ('planet', 'planet'): TEXT['warp to'],
    ('planet', 'ship'): TEXT['board'],
    ('ship', 'planet'): TEXT['back to'],
    ('planet', 'surface'): TEXT['beam down to'],
    ('surface', 'planet'): TEXT['back to orbit of'],
}


class Spaceship:

    def __init__(self):
        self.location = None
        self.artifacts = 0
        self.cargo = ''

    def draw(self):
        report = f"{TEXT['cargo bay']}:\n\n\n\n\n\n\n\n\n{TEXT['artifacts']}:"
        arcade.draw_text(report, 800, 600, arcade.color.GREEN, 20, font_name='GARA', anchor_y="top")
        if self.cargo:
            IMAGES[self.cargo].draw_sized(870, 500, 128, 128)
        for i in range(1, self.artifacts+1):
            IMAGES[f"artifact{i}"].draw_sized(730 + i * 140, 320, 96, 96)

    def move_to(self, location):
        self.location = location

    def load_cargo(self, resource):
        self.cargo = resource
        #return f'PICKED UP {resource}'

    def __repr__(self):
        return f"<spaceship at: {self.location.name}>"

    def get_commands(self):
        commands = []
        # move
        for location in self.location.connections:
            transition = (self.location.type, location.type)
            prefix = TRANSITIONS.get(transition, 'move to')
            move = Command(f"{prefix} {location.name}", partial(self.move_to, location))
            commands.append(move)
        # load goods
        for resource in self.location.resources:
            load = Command(f"{TEXT['collect']} {TEXT[resource]}", partial(self.load_cargo, resource))
            commands.append(load)
        # talk to people
        if self.location.active and self.location.action_name:
            contact = Command(self.location.action_name, partial(self.location.contact, self))
            commands.append(contact)

        return commands
