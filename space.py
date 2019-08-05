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

    def __init__(self, start_planet):
        self.ship = Spaceship()
        self.ship.planet = start_planet

    @property
    def is_running(self):
        return self.ship.active and not self.solved

    @property
    def solved(self):
        planet = self.ship.planet
        return planet.name == 'Olympus' and not planet.location.active

    def print_report(self):
        planet = self.ship.planet
        shipreport = self.ship.get_report()
        planet_report = planet.get_report()
        print('\n' * 30)
        print_twocolumn(planet_report, shipreport)

    @staticmethod
    def print_commands(commands):
        print("\nAvailable commands:")
        for cmd in commands:
            print(f"[{cmd.key}] {cmd.description}")
        print()

    @staticmethod
    def enter_command(commands):
        key = input("What shall we do? ")
        for cmd in commands:
            if key == cmd.key:
                print(key)
                if views.SLOW_MOTION:
                    time.sleep(3)
                cmd.action()

    def travel(self):
        while self.is_running:
            self.print_report()
            commands = self.ship.get_commands()
            self.print_commands(commands)
            self.enter_command(commands)


if __name__ == '__main__':
    intro()
    galaxy = create_galaxy()
    sg = SpaceGame(galaxy[0])
    sg.travel()
    if sg.solved:
        outro()
