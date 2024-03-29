import json
import os

import arcade

from space_game.views import BASE_PATH, FONT_SETTINGS, IMAGES


DEFAULT_GALAXY = os.path.join(BASE_PATH, "galaxy_EN.json")


class Location:
    # pylint: disable=too-many-instance-attributes

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.description = kwargs["description"]
        self.image = kwargs["image"]
        self.type = kwargs.get("type", "planet")
        self.connection_names = kwargs["connections"]
        self.connections = []
        self.resources = kwargs.get("goods", [])

        # Action Triggers
        self.action_name = kwargs.get("action_name")
        self.require_good = kwargs.get("require_good")
        self.require_artifacts = kwargs.get("require_artifacts", -1)
        self.activated_message = kwargs.get("activated_message")
        self.not_activated_message = kwargs.get("not_activated_message")
        self.activate_clear_cargo = kwargs.get("activate_clear_cargo", False)
        self.activate_gain_artifact = kwargs.get("activate_gain_artifact", False)
        self.active = True

    def __repr__(self):
        return f"<Location: {self.name}>"

    def draw(self):
        IMAGES[self.image].draw_sized(150, 850, 200, 200)
        arcade.draw_text(text=self.name, start_x=300, start_y=950, bold=True, **FONT_SETTINGS)
        arcade.draw_text(text=self.description, start_x=300, start_y=900, multiline=True, width=600, **FONT_SETTINGS)

    def add_connection(self, location):
        self.connections.append(location)

    def activate(self, ship):
        self.active = False
        if self.activate_clear_cargo:
            ship.cargo = ""
        if self.activate_gain_artifact:
            ship.artifacts += 1

    def contact(self, ship):
        if self.active:
            if (self.require_good and ship.cargo == self.require_good) or (
                self.require_artifacts >= 0 and ship.artifacts >= self.require_artifacts
            ):
                self.activate(ship)
                return self.activated_message
            return self.not_activated_message
        return ""


def create_galaxy(fn=DEFAULT_GALAXY):
    """Loads entire playing environment from a JSON file"""
    j = json.load(open(fn, encoding="utf-8"))
    galaxy = [Location(**loc) for loc in j]

    # builds connection graph
    for location in galaxy:
        for targetname in location.connection_names:
            target = None
            for p in galaxy:
                if p.name == targetname:
                    target = p
            assert target is not None
            location.add_connection(target)

    return galaxy
