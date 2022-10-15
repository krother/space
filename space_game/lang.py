import os


LANG = "EN"
if os.getenv("LANG").upper().startswith("DE"):
    LANG = "DE"

DE = {
    "cargo bay": "Frachtraum",
    "artifacts": "Artefakte",
    "collect": "kaufe",
    "warp to": "Sprung nach",
    "board": "fliege zu",
    "back to": "zurück zu",
    "beam down to": "herunterbeamen zu",
    "back to orbit of": "hochbeamen zu",
    "ore": "Erze",
    "gas": "Gas",
    "food": "Nahrung",
    "medical": "Medikamente",
    "nucleons": "Neutronen",
    "minerals": "Mineralien",
    "spices": "Gewürze",
    "Alien Space Station": "Ausserirdisches Monument",
    "Available commands": "Befehle",
}

EN = {k: k for k in DE}

TEXT = EN if LANG == "EN" else DE
