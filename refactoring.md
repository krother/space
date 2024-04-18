
# Refactoring

## Goal



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


    review the code
    write a minimal test
    add type annotations
    extract core data structures
    separate easily cleanable parts from very bad parts
    remove excess dependencies
    be very transparent about which features of the code you trust


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

## Extra Challenge 1: Parallel games

One thing the new interface should make possible is running two or more games in parallel.
This was not possible in the original GUI (and did not make much sense either).

First, write a test that checks whether two games are different.

    game1 = start_game()
    game2 = start_game()
    game1 = execute_command(game1.game_id, game1.commands[0])
    game2 = execute_command(game2.game_id, game2.commands[0])
    assert game1.location.name1 == game2.location.name

The test should fail, if you assigned the same default id to all games.
To make the test pass, you need somthing like:

    import uuid
 
    game_id = str(uuid.uuid1())

## Extra Challenge 2: Persistence Layer

store them in a 

https://www.cosmicpython.com/book/chapter_02_repository.html


!! Tempting to add persistence layer (DB or similar) right away. This is a separate feature


## Disclaimer

No real animals (pandas, pythons, unicorns etc.) were launched to space in the preparation of this tutorial.

## License

Distributed under the conditions of the MIT License. See LICENSE file.

With contributions by Kristian Rother, Tim Weber, Veit Schiele and Frank Hofmann.

Some artwork has been adopted from the Naev game. See `images/ARTWORK_LICENSE` for details.
The rest of the artwork was generated with [beta.dreamstudio.ai](https://beta.dreamstudio.ai/).
