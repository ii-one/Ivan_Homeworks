__author__ = 'skorenev'

"""
Players file. Contains players classes
"""

from functools import reduce

def get_input_function():
    """
    This function returns right `input` function for python2 and python3.
    :return: function `input` in python3 or `raw_input` in python2.
    """

    try:
        input_function = raw_input
    except NameError:
        # `raw_input` was not defined, so `NameError` occured:
        input_function = input

    return input_function

class Player(object):
    """
    Basic class for all items, provides basic methods and values.
    This class has to be subclassed in order to create new items.
    """

    def __init__(self, name = '', caption = '', field = None, opponent_field = None, fleet = [], type_of_player = 'human'):
        self.name = name
        self.caption = caption
        self.field = []
        self.opponent_field = []
        self.fleet = []
        self.shots = []

    def construct(self):
        input_function = get_input_function()
        welcome_text = 'Input username for ' + self.caption + ': '
        heading = input_function(welcome_text)
        return Player(heading, self.caption)

    def fleet_list(self):
        print('\\n')
        for ship in range(len(self.fleet)):
            print('Ship #%s: Size:%s Health:%s x:%s y:%s'%(ship, self.fleet[ship].size, self.fleet[ship].health, self.fleet[ship].coord_x, self.fleet[ship].coord_y))
        return len(self.fleet)

    def check_health(self, shot):
        hit = False
        overall_health = 0
        #one_ship_health = 0

        for ship in self.fleet:
            if ship.direction == '|':
                if shot.coord_x in range(ship.coord_x, ship.coord_x+ship.size) \
                 and shot.coord_y == ship.coord_y:
                    ship.health -= 1
                    hit = True
                    saved_ship = ship

            if ship.direction == '-':
                if shot.coord_y in range(ship.coord_y, ship.coord_y+ship.size) \
                 and shot.coord_x == ship.coord_x:
                    ship.health -= 1
                    hit = True
                    saved_ship = ship

        for ship in self.fleet:
            overall_health += ship.health

        if hit == True:
            return overall_health, saved_ship, True
        else:
            return overall_health, None, False
