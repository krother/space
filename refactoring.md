
# Refactoring

## Disclaimer

No real animals (pandas, pythons, unicorns etc.) were launched to space in the preparation of this tutorial.

## Prerequisites

Intermediate tutorial.
You need to be familiar with command line and a text editor (VSCode, PyCharm).
If you have used Python exclusively in Jupyter or online editors until now, it may turn out to be very difficult to work on the exercises in the tutorial. Consider yourself warned.

1. Preparations: Virtual env, Install deps
2. Run tests. Run game
3. Goal: Make the web interface work.
4. Motivation
- Simple workflow: test. Refactor. test
- Name some small refactorings: BALL
- BUT: What if 
- refactoring breaks the test
- there are no tests
- This is what we have here.
5. Better workflow
- Run tests
- define new interface within the old code
- Write tests against the new interface
- Run tests
- refactor
- Run tests
6. Architecture: dependency graph
7. Introduce Facade
- convenience functions
- data exchange objects (pull from app.py)
- class diagram: Facade
- connect GUI to Facade
- run tests
8. Test against Facade
- write test
- run tests
9. Connect API to Facade
- write code
- run tests
10. BONUS
- htmx
- isolate persistence layer
11. Q & A

## INTIME:
- create module `boundary.py`
- create data exchange classes GameData, LocationData

- create boundary function: start_game
def start_game() -> GameData:
- borrow from gui
- create game_id in boundary. Use '1' as game_id for now

- write test:
def test_start_game():
    assert start_game()

- adjust gui
  * use start_game method
  * draw method [small refac not noticed before]
  * add solved

- create boundary function: execute_command
def execute_command(game_id: str, command: str) -> GameData:

- extract function def _get_game_data(game_id, game, message=None) -> GameData:
- add test

- use boundary in gui
- move GUI stuff from game to gui
- remove .active from test (internal state, not public info)

tODO: move message to game
TODO: fix test containing slon

## Extras:

Make it possible to manage 2+ games in parallel:

import uuid
str(uuid.uuid1())

store them in a 

write a test that checks whether 2 games are different.

!! Tempting to add persistence layer (DB or similar) right away. This is a separate feature