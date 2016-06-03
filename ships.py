
class Spaceship:

    def __init__(self):
        self.colonists = 1
        self.location = None
        self.artifacts = 0
        self.cargo = ''

    def moveto(self, planet):
        self.location = planet

    def colonize(self, planet):
        if self.colonists:
            self.colonists -= 1
            planet.population += 1
            planet.colonized = True

    def pickup(self, planet):
        if planet.population:
            self.colonists += 1
            planet.population -= 1

    def load_cargo(self, cargo):
        self.cargo = cargo
            
    def get_report(self):
        result = '''
Spaceship Controller
====================
colonists on board : %i
cargo              : %s
artifacts found    : %i/5
'''%(self.colonists, self.cargo, self.artifacts)
        return result
