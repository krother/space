import os

import space_game.config
from space_game.errors import NoEntryFound, DuplicateEntry

match os.getenv("REPO_TYPE"):

    case "mongodb":
        from .repository_mongodb import (
            create_game,
            get_game,
            update_game,
            add_location,
            get_location,
            update_location,
            add_location_batch,
            delete_location,
        )
    case "dict":
        from .repository_dict import (
            create_game,
            get_game,
            update_game,
            add_location,
            get_location,
            update_location,
            add_location_batch,
            delete_location,
        )
    case "duckdb":
        from .repository_duckdb import (
            create_game,
            get_game,
            update_game,
            add_location,
            get_location,
            update_location,
            add_location_batch,
            delete_location,
        )
    case "postgres":
        from .repository_postgres import (
            create_game,
            get_game,
            update_game,
            add_location,
            get_location,
            update_location,
            add_location_batch,
            delete_location,
        )
