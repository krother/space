
from locations import SpaceStation, Caves, AncientVault, AncientShipwreck, SiliconValley, AquaCity, SmugglerShip

class Planet:

    def __init__(self, name, desc, pop, resources, location=None):
        self.name = name
        self.description = desc
        self.connections = []
        self.resources = resources
        self.population = pop
        self.colonized = False
        self.location = location

    def add_connection(self, planet):
        self.connections.append(planet)

    def get_report(self):
        result = '''
%s system
%s
%s

population: %i
resources : %s
'''%(self.name, '='*(len(self.name)+7), self.description, self.population,
     ', '.join(self.resources))
        if self.location and self.location.name:
            result += '''
%s:
%s'''%(self.location.name, self.location.description)
        return result
        

GALAXY = [
    Planet('Terra', 'The cradle of mankind. A blue jewel floating in space.',
           3, ['food', 'trinkets']),
    Planet('Rorke', 'A hot white star surrounded by a vast asteroid belt.',
           0, ['ore'], SmugglerShip()),
    Planet('Magminus', 'A volcanic planet inhabited by a silicon-based species.',
           1, ['minerals'], SiliconValley()),
    Planet('Vega', 'A fertile world with rich aquatic life forms.',
           1, ['biotics'], AquaCity()),
    Planet('X2475', 'Neutron star with really nothing going on.',
           0, ['nucleons']),
    Planet('Sirius', 'A sandy desert with seven beautiful orange moons.',
           0, ['ore'], AncientShipwreck()),
    Planet('Octygon', 'A dead rocky planet with mysterious underground caves.',
           0, ['ore'], Caves()),
    Planet('Kucharsky', 'A huge dark ochre gas planet.',
           0, ['gas']), 
    Planet('Centauri', 'Civilizations outpost in space.',
           1, ['minerals', 'nucleons'], SpaceStation()),
    Planet('New Haven', 'A earth-like yet uninhabited world.',
           0, ['food', 'biotics']),
    Planet('Olympus', 'The home world of the Firstborn.',
           0, [], AncientVault())
    ]

MAP = {    
    'Terra': ['Centauri', 'Sirius'],
    'Centauri': ['Kucharsky', 'Terra', 'Vega', 'Sirius'],
    'Sirius': ['Terra', 'Centauri', 'Vega'],
    'Vega': ['Sirius', 'Centauri', 'Octygon'],
    'Kucharsky': ['New Haven', 'Centauri', 'Magminus'],
    'New Haven': ['Rorke', 'Octygon', 'Kucharsky'],
    'Octygon': ['Rorke', 'Magminus', 'New Haven', 'Vega'],
    'Magminus': ['Octygon', 'Kucharsky'],
    'Rorke': ['X2475', 'New Haven', 'Octygon'],
    'X2475': ['Rorke', 'Olympus'],
    'Olympus': ['X2475'],
    }

def set_connections(galaxy, mapdict):
    '''builds the connection graph'''
    for planet in galaxy:
        for targetname in mapdict[planet.name]:
            target = None
            for p in galaxy:
                if p.name == targetname:
                    target = p
            planet.add_connection(target)
    
set_connections(GALAXY, MAP)
