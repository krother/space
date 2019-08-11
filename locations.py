
from views import IMAGES
import arcade


class Location:

    def __init__(self, name, description, image, action_name, **kwargs):
        self.name = name
        self.description = description
        self.image = image
        self.action_name = action_name
        self.require_good = kwargs.get('require_good')
        self.require_artifacts = kwargs.get('require_artifacts', -1)
        self.activated_message = kwargs.get('activated_message')
        self.not_activated_message = kwargs.get('not_activated_message')
        self.activate_clear_cargo = kwargs.get('activate_clear_cargo', False)
        self.activate_gain_artifact = kwargs.get('activate_gain_artifact', False)
        self.active = True

    def activate(self, ship):
        self.active = False
        print(self.activated_message)
        if self.activate_clear_cargo:
            ship.cargo = ''
        if self.activate_gain_artifact:
            ship.artifacts += 1

    def contact(self, ship):
        if self.active:
            if (self.require_good and ship.cargo == self.require_good) or \
               (self.require_artifacts >= 0 and ship.artifacts >= self.require_artifacts):
                self.activate(ship)
            else:
                return self.not_activated_message

    def draw(self):
        IMAGES[self.image].draw(150, 550, 200, 200)
        report = self.get_report()
        arcade.draw_text(report, 300, 650, arcade.color.GREEN, 20, font_name='GARA', anchor_y="top")

    def get_report(self):
        if self.name:
            return f'\n{self.name}: \n{self.description}'
        return ''


SpaceStation = Location(
    name='Terran Outpost',
    description='A small space station marks the border of the Terran Federation.',
    image='wrath',
    action_name='contact outpost',
    not_activated_message='Good luck on your mission!'
)


SmugglerShip = Location(
    name='Smuggler Ship',
    description="A small vessel hidden in an asteroid belt. You had almost overlooked them if they hadn't contacted you.",
    image='phalanx_comm',
    action_name='board the ship',
    not_activated_message="We are in dire need of repairs and ran out of gas.",
    require_good='gas',
    activated_message="In exchange for your supplies we will give you this priceless artifact.",
    activate_clear_cargo=True,
    activate_gain_artifact=True
)


AncientVault = Location(
    name='Ancient Space Station',
    description='A huge monument made by an unknown civilization. It has five openings that fit small objects.',
    image='000',
    action_name='examine Ancient Vault',
    require_artifacts=5,
    not_activated_message='The openings seem to be made for some kind of alien artifacts.',
    activated_message='You insert five artifacts into the hole. The monolith opens!!!.'
)

Caves = Location(
    name='Underground caves',
    description='The caves are many miles deep and stretch over half of the planets surface.',
    image='uninhabited-rocky-airless-00',
    action_name='explore caves',
    require_good='food',
    activated_message='After two weeks of search, you discover a strange artifact at the bottom of the caves.',
    not_activated_message='You abandon the search after a week. You need more food supplies to explore the caves deeper.',
    activate_clear_cargo=True,
    activate_gain_artifact=True
)

AncientShipwreck = Location(
    name='Strange signal',
    description='A regular radar pulse emanates from underneath the desert surface.',
    image='desertic',
    action_name='send landing party',
    require_good='nucleons',
    activated_message='you discover an ancient shipwreck. Using a cache of gluons you clear up the radiation and enter. Inside you find an ancient artifact!',
    activate_clear_cargo=True,
    activate_gain_artifact=True,
    not_activated_message='You discover an abandoned shipwreck emitting the pulse. However, there is lots of nuclear debris. You will need a stron neutron source to clean it up before you can enter.'
)


AquaCity = Location(
    name='Aquatic City',
    description='a huge coral reef hosts a submarine sentient species',
    image='aquatic3',
    action_name='contact aliens',
    require_good='medical',
    activated_message='After a long bargain you trade a container of medical goods for a strange artifact. You wonder who made the better deal.',
    activate_clear_cargo=True,
    activate_gain_artifact=True,
    not_activated_message='The aliens are friendly and seem to enjoy trading. They seem to have problems with aggressive bacteria though.'
)


SiliconValley = Location(
    name='Silicon Valley',
    description='A valley near a volcanic geyser seems to be where the strange organisms gather.',
    image='lava',
    action_name='send landing party',
    require_artifacts=0,
    activated_message='In the valley you find an uninhabited cave with an artifact!',
    activate_gain_artifact=True
)
