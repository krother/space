
from functools import partial
from collections import namedtuple
import arcade
from views import IMAGES


Command = namedtuple('Command', ('description', 'action'))

TRANSITIONS = {
    ('planet', 'planet'): 'warp to',
    ('planet', 'ship'): 'board',
    ('ship', 'planet'): 'back to',
    ('planet', 'surface'): 'beam down to',
    ('surface', 'planet'): 'back to orbit of',
}


class Spaceship:

    def __init__(self):
        self.location = None
        self.artifacts = 0
        self.cargo = ''

    def draw(self):
        report = self.get_report()
        arcade.draw_text(report, 700, 600, arcade.color.GREEN, 20, font_name='GARA', anchor_y="top")
        if self.cargo:
            IMAGES[self.cargo].draw(770, 500, 128, 128)
        for i in range(1, self.artifacts+1):
            IMAGES[f"artifact{i}"].draw(630 + i * 140, 320, 128, 128)

    def move_to(self, location):
        self.location = location
        #return fMOVE TO {location.name}'

    def load_cargo(self, resource):
        self.cargo = resource
        #return f'PICKED UP {resource}'

    def get_report(self):
        result = f'''Cargo Bay:\n\n\n\n\n\n\n\n\nArtifacts:'''
        return result

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
            load = Command(f"collect {resource}", partial(self.load_cargo, resource))
            commands.append(load)
        # talk to people
        if self.location.active and self.location.action_name:
            contact = Command(self.location.action_name, partial(self.location.contact, self))
            commands.append(contact)

        return commands
