import os

LANG = "EN"
lang = os.getenv("LANG")
if lang and lang.upper().startswith("DE"):
    LANG = "DE"

BASE_PATH = os.path.split(__file__)[0]
