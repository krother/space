'''

Space Traveller - main controller

'''

__author__ = "Kristian Rother"


from planets import GALAXY
from ships import Spaceship
from views import intro, outro, print_twocolumn
from commands import get_commands       

class SpaceGame:

    def __init__(self, galaxy):
        self.ship = Spaceship()
        self.ship.location = galaxy[0]

    @property
    def is_running(self):
        return self.ship.active and not self.solved
    
    @property
    def solved(self):
        planet = self.ship.location
        return planet.name == 'Olympus' and \
            not planet.location.active

    def travel(self):
        while self.is_running:
            planet = self.ship.location
            shipreport = self.ship.get_report()
            planreport = planet.get_report()
            print('\n' * 30)
            print_twocolumn(planreport, shipreport)
            print("\nAvailable commands:")
            commands = get_commands(self.ship, planet)
            for cmd in commands:
                print("[%s] %s"%(cmd.key, cmd.description))
            print()
            
            key = input("What shall we do? ")
            for cmd in commands:
                if key == cmd.key:
                    cmd.execute()


if __name__ == '__main__':
    intro()
    sg = SpaceGame(GALAXY)
    sg.travel()
    if sg.solved:
        outro()
