import os


LANG = "EN"
if os.getenv("LANG", "EN").upper().startswith("DE"):
    LANG = "DE"

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
