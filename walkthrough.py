
from unittest.mock import patch
from space import SpaceGame, create_galaxy
import views

COMPLETE_SOLUTION = iter(open('solution.txt').read())
views.SKIP_INPUT = True
views.SLOW_MOTION = True


@patch('builtins.input', lambda x: next(COMPLETE_SOLUTION))
def show_walkthrough():
    galaxy = create_galaxy()
    sg = SpaceGame(galaxy)
    sg.travel()


if __name__ == '__main__':
    show_walkthrough()
