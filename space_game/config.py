import os

LANG = "EN"
if os.getenv("LANG").upper().startswith("DE"):
    LANG = "DE"

BASE_PATH = os.path.split(__file__)[0]
