"""
User actions.

Implementation of the Command Design Pattern.
"""
#TODO: watch Raymond Hettingers talk and then use super() 

class Command:

    def __init__(self, key, description):
        self.key = key
        self.description = description

    def execute(self):
        pass


class Warp(Command):

    def __init__(self, key, ship, planet):
        Command.__init__(self, str(key), "warp to %s"%(planet.name))
        self.ship = ship
        self.planet = planet

    def execute(self):
        self.ship.location = self.planet


class Harvest(Command):

    def __init__(self, resource, ship):
        Command.__init__(self, resource[0].upper(), "harvest %s"%(resource))
        self.resource = resource
        self.ship = ship

    def execute(self):
        self.ship.cargo = self.resource


class Colonize(Command):

    def __init__(self, ship, planet):
        Command.__init__(self, 'c', 'colonize planet')
        self.ship = ship
        self.planet = planet

    def execute(self):
        self.ship.colonize(self.planet)


class Pickup(Command):

    def __init__(self, ship, planet):
        Command.__init__(self, 'p', 'pick up colonist')
        self.ship = ship
        self.planet = planet

    def execute(self):
        self.ship.pickup(self.planet)


class Contact(Command):

    def __init__(self, ship, planet):
        Command.__init__(self, 't', planet.location.action_name)
        self.ship = ship
        self.planet = planet

    def execute(self):
        self.planet.location.contact(self.ship)


class Exit(Command):

    def __init__(self, ship):
        Command.__init__(self, 'x', 'exit game')
        self.ship = ship
        
    def execute(self):
        self.ship.active = False


SearchArtifacts = Contact


def get_commands(ship, planet):
    commands = []
    # move
    for i, neighbor in enumerate(planet.connections):
        commands.append(Warp(i+1, ship, neighbor))
    # move
    for resource in planet.resources:
        commands.append(Harvest(resource, ship))
    # colonize / pickup
    commands.append(Colonize(ship, planet))
    commands.append(Pickup(ship, planet))
    # talk to people
    if planet.location and planet.location.name and planet.location.active:
        commands.append(Contact(ship, planet))
    # exit
    commands.append(Exit(ship))
    return commands

