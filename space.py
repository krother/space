'''

Space Traveller - main controller

'''

__author__ = "Kristian Rother"


from planets import GALAXY
from ships import Spaceship
from views import intro, outro, print_twocolumn
from commands import get_commands       
        
def travel(galaxy):
    ship = Spaceship()
    planet = galaxy[0]
    ship.moveto(planet)
    while planet.name != 'Olympus' or planet.location.active:
        planet = ship.location
        shipreport = ship.get_report()
        planreport = planet.get_report()
        print('\n' * 30)
        print_twocolumn(planreport, shipreport)
        print("\nAvailable commands:")
        commands = get_commands(ship, planet)
        for cmd in commands:
            print("[%s] %s"%(cmd.key, cmd.description))
        print()
        
        key = input("What shall we do? ")
        for cmd in commands:
            if key == cmd.key:
                cmd.execute()


if __name__ == '__main__':
    intro()
    travel(GALAXY)
    outro()
