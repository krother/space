'''
Space Traveller - main controller
'''

__author__ = "Kristian Rother"


import time
from ships import Spaceship
from planets import create_galaxy
from views import intro, outro, print_twocolumn
import views


class SpaceGame:

    def __init__(self, galaxy_obj):
        self.ship = Spaceship()
        self.ship.planet = galaxy_obj[0]

    @property
    def is_running(self):
        return self.ship.active and not self.solved

    @property
    def solved(self):
        planet = self.ship.planet
        return planet.name == 'Olympus' and not planet.location.active

    def travel(self):
        while self.is_running:
            planet = self.ship.planet
            shipreport = self.ship.get_report()
            planet_report = planet.get_report()
            print('\n' * 30)
            print_twocolumn(planet_report, shipreport)
            print("\nAvailable commands:")
            commands = self.ship.get_commands()
            for cmd in commands:
                print("[%s] %s" % (cmd.key, cmd.description))
            print()

            key = input("What shall we do? ")
            for cmd in commands:
                if key == cmd.key:
                    print(key)
                    if views.SLOW_MOTION:
                        time.sleep(3)
                    cmd.action()


if __name__ == '__main__':
    intro()
    galaxy = create_galaxy()
    sg = SpaceGame(galaxy)
    sg.travel()
    if sg.solved:
        outro()
