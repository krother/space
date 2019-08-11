
from locations import SpaceStation, Caves, AncientVault
from locations import AncientShipwreck, SiliconValley
from locations import AquaCity, SmugglerShip
from views import IMAGES
import arcade
import json


class Planet:

    def __init__(self, json_record):
        self.name = json_record['name']
        self.description = json_record['description']
        self.image = json_record['image']
        self.connection_names = json_record['connections']
        self.connections = []
        self.resources = json_record['goods']
        self.location = None # json_record['location']

    def draw(self):
        IMAGES[self.image].draw(150, 800, 200, 200)
        report = self.get_report()
        arcade.draw_text(report, 300, 900, arcade.color.GREEN, 20, font_name='GARA', anchor_y="top")
        if self.location:
            self.location.draw()

    @property
    def contactable(self):
        return self.location and self.location.name and self.location.active

    def add_connection(self, planet):
        self.connections.append(planet)

    def get_report(self):
        result = '''
%s system
%s
%s
''' % (self.name, '='*(len(self.name)+7), self.description)
        return result


def create_galaxy():
    j = json.load(open('galaxy.json'))
    galaxy = [Planet(loc) for loc in j]

    # builds connection graph
    for planet in galaxy:
        for targetname in planet.connection_names:
            target = None
            for p in galaxy:
                if p.name == targetname:
                    target = p
            planet.add_connection(target)

    return galaxy
