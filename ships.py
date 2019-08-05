
from functools import partial
from collections import namedtuple

Command = namedtuple('Command', ('key', 'description', 'action'))


class Spaceship:

    def __init__(self):
        self.planet = None
        self.artifacts = 0
        self.cargo = ''
        self.active = True

    def move_to(self, planet):
        print('MOVE TO ', planet.name)
        self.planet = planet

    def load_cargo(self, resource):
        self.cargo = resource

    def exit(self):
        self.active = False

    def get_report(self):
        result = '''
Spaceship Bridge
================
cargo              : {}
artifacts found    : {}/5
'''.format(self.cargo, self.artifacts)
        return result

    def __repr__(self):
        return f"<spaceship at: {self.planet.name}>"

    def get_commands(self):
        commands = []
        # move
        for i, planet in enumerate(self.planet.connections):
            warp = Command(str(i + 1), f"warp to {planet.name}", partial(self.move_to, planet))
            commands.append(warp)
        # load goods
        for resource in self.planet.resources:
            load = Command(resource[0].upper(), f"collect {resource}", partial(self.load_cargo, resource))
            commands.append(load)
        # talk to people
        if self.planet.contactable:
            contact = Command('t', self.planet.location.action_name, partial(self.planet.location.contact, self))
            commands.append(contact)

        exit_game = Command('x', 'exit game', self.exit)
        commands.append(exit_game)
        return commands
