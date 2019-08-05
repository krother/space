
from locations import SpaceStation, Caves, AncientVault
from locations import AncientShipwreck, SiliconValley
from locations import AquaCity, SmugglerShip


class Planet:

    def __init__(self, name, desc, resources, connection_names, location=None):
        self.name = name
        self.description = desc
        self.connection_names = connection_names
        self.connections = []
        self.resources = resources
        self.location = location

    @property
    def contactable(self):
        return self.location and self.location.name and self.location.active

    def add_connection(self, planet):
        self.connections.append(planet)

    def get_report(self):
        result = '''
%s system
%s
%s

resources : %s
''' % (self.name, '='*(len(self.name)+7), self.description,
       ', '.join(self.resources))
        if self.location:
            result += self.location.get_report()
        return result


def create_galaxy():
    galaxy = [
        Planet('Terra', 'The cradle of mankind. A blue jewel floating in space.',
               ['food', 'trinkets'],
               ['Centauri', 'Sirius']
              ),
        Planet('Rorke', 'A hot white star surrounded by a vast asteroid belt.',
               ['ore'],
               ['X2475', 'New Haven', 'Octygon'],
               SmugglerShip),
        Planet('Magminus', 'A volcanic planet inhabited by a silicon-based species.',
               ['minerals'],
               ['Octygon', 'Kucharsky'],
               SiliconValley),
        Planet('Vega', 'A fertile world with rich aquatic life forms.',
               ['biotics'],
               ['Sirius', 'Centauri', 'Octygon'],
               AquaCity),
        Planet('X2475', 'Neutron star with really nothing going on.',
               ['nucleons'],
               ['Rorke', 'Olympus']),
        Planet('Sirius', 'A sandy desert with seven beautiful orange moons.',
               ['ore'],
               ['Terra', 'Centauri', 'Vega'],
               AncientShipwreck),
        Planet('Octygon', 'A dead rocky planet with mysterious underground caves.',
               ['ore'],
               ['Rorke', 'Magminus', 'New Haven', 'Vega'],
               Caves),
        Planet('Kucharsky', 'A huge dark ochre gas planet.',
               ['gas'],
               ['New Haven', 'Centauri', 'Magminus']),
        Planet('Centauri', 'Civilizations outpost in space.',
               ['minerals', 'nucleons'],
               ['Kucharsky', 'Terra', 'Vega', 'Sirius'],
               SpaceStation),
        Planet('New Haven', 'A earth-like yet uninhabited world.',
               ['food', 'biotics'],
               ['Rorke', 'Octygon', 'Kucharsky']),
        Planet('Olympus', 'The home world of the Firstborn.',
               [],
               ['X2475'],
               AncientVault)
    ]

    # builds connection graph
    for planet in galaxy:
        for targetname in planet.connection_names:
            target = None
            for p in galaxy:
                if p.name == targetname:
                    target = p
            planet.add_connection(target)

    return galaxy
