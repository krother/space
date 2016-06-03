
class Location:
    name = ''
    description = ''
    action_name = ''
    active = True

    def contact(self, ship):
        pass

class SpaceStation(Location):
    name = 'Terran Outpost'
    description = 'A small space station marks the border of the Terran Federation.'
    action_name = 'contact %s'%name

    def contact(self, ship):
        print('''Good luck on your mission!''')
        input()

class SmugglerShip(Location):
    name = 'Smuggler Ship'
    description = "A small vessel hidden in an asteroid belt. You had almost overlooked them if they hadn't contacted you."
    action_name = 'board %s'%name

    def contact(self, ship):
        print('''"We are in dire need of repairs and ran out of gas."''')
        if ship.cargo == 'gas':
            print('"In exchange for your supplies we will give you this priceless artifact."')
            ship.artifacts += 1
            ship.cargo = 0
            self.active = False
        input() 


class AncientVault(Location):
    name = 'Ancient Vault'
    description = 'A huge monument made by an unknown civilization. It has five openings that fit small objects.'
    action_name = 'examine Ancient Vault'

    def contact(self, ship):
        if ship.artifacts < 5:
            print('''The artifacts seem to fit into the five holes. You need more of them.''')
        elif ship.artifacts >= 5:
            print('''You insert five artifacts into the hole. The vault opens!!!.''')
            self.active = False
        else:
            print('''The monument does not react to anything you try.''')
        input()


class Caves(Location):
    name = 'Underground caves'
    description = 'The caves are many miles deep and stretch over half of the planets surface.'
    action_name = 'explore caves'

    def contact(self, ship):
        if ship.cargo == 'food':
            print('After two months of search, you discover a strange artifact at the bottom of the caves.')
            ship.cargo = ''
            ship.artifacts += 1
            self.active = False
        else:
            print('You abandon the search after a week. You need more supplies to explore the caves deeper.')
        input()

    
class AncientShipwreck(Location):

    name = 'Strange signal'
    description = 'A regular radar pulse emanates from underneath the desert surface.'
    action_name = 'send landing party'

    def contact(self, ship):
        if ship.cargo == 'nucleons':
            print('you discover an ancient shipwreck. Using a cache of gluons you clear up the radiation and enter. Inside you find an ancient artifact!')
            ship.cargo = ''
            ship.artifacts += 1
            self.active = False
        else:
            print('You discover an abandoned shipwreck emitting the pulse. However, there is lots of nuclear debris that you will need to clean up before you can enter.')
        input()

class AquaCity(Location):
    name = 'Aquatic City'
    description = 'a huge coral reef hosts a submarine sentient species'
    action_name = 'contact aliens'

    def contact(self, ship):
        if ship.cargo == 'trinkets':
            print('After a long negotiation you trade a container of cheap jewellery, waving cats and rubber ducks for a strange artifact. You wonder who made the better deal.')
            ship.cargo = ''
            ship.artifacts += 1
            self.active = False
        else:
            print('The aliens are friendly and seem to enjoy trading. For a couple of tools you get an impressive collection of sea shells.')
        input()


class SiliconValley(Location):
    name = 'Silicon Valley'
    description = 'A valley near a volcanic geyser seems to be where the strange organisms gather.'
    action_name = 'send landing party'

    def contact(self, ship):
        print('In the valley you find an uninhabited cave with an artifact!')
        ship.artifacts += 1
        self.active = False
        input()

