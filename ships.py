
from functools import partial
from collections import namedtuple
import arcade
from views import IMAGES


Command = namedtuple('Command', ('description', 'action'))


class Spaceship:

    def __init__(self):
        self.planet = None
        self.artifacts = 5
        self.cargo = ''

    def draw(self):
        report = self.get_report()
        arcade.draw_text(report, 700, 400, arcade.color.GREEN, 20, font_name='GARA', anchor_y="top")
        if self.cargo:
            IMAGES[self.cargo].draw(770, 300, 128, 128)
        for i in range(1, self.artifacts+1):
            IMAGES[f"artifact{i}"].draw(630 + i * 140, 120, 128, 128)


    def move_to(self, planet):
        self.planet = planet
        #return fMOVE TO {planet.name}'

    def load_cargo(self, resource):
        self.cargo = resource
        #return f'PICKED UP {resource}'

    def get_report(self):
        result = f'''Cargo Bay:\n\n\n\n\n\n\n\n\nArtifacts:'''
        return result

    def __repr__(self):
        return f"<spaceship at: {self.planet.name}>"

    def get_commands(self):
        commands = []
        # move
        for planet in self.planet.connections:
            warp = Command(f"warp to {planet.name}", partial(self.move_to, planet))
            commands.append(warp)
        # load goods
        for resource in self.planet.resources:
            load = Command(f"collect {resource}", partial(self.load_cargo, resource))
            commands.append(load)
        # talk to people
        if self.planet.contactable:
            contact = Command(self.planet.location.action_name, partial(self.planet.location.contact, self))
            commands.append(contact)

        return commands
