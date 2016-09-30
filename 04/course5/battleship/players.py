# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import random

from battleship.base import Informational
from battleship.shot import Shot
from battleship.ship import Ship
from battleship.utils import get_input

__author__ = 'sobolevn'


class Player(Informational):
    # Magic methods:
    def __init__(self, human=True, exclude=None):
        self._human = human
        self._ships = []
        self._shots = []

        self.name = self._wait_for_name(exclude=exclude)
        self._greet_player()

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    # Properties:

    @property
    def ships(self):
        return self._ships

    @property
    def shots(self):
        return self._shots

    # Private and protected methods:

    def _greet_player(self):
        self.__class__.print_for_player('Hello, %s' % self.name)

    @staticmethod
    def __get_cords(size):
        cords = get_input(
            "Input cords form %s to %s in 'x, y' format: " %
            (1, size)
        )
        x, y = [(int(value) - 1) for value in cords.strip().split(',')]

        if (x < 0 or y < 0) or (x >= size or y >= size):
            raise ValueError()
        return x, y

    # Placing ships:

    def place_ships(self, ship_rules, field):
        def valid_ship_position():
            if ship is None:
                return False

            for cords in ship:
                if any(cord >= field.size for cord in cords):
                    self.__class__.print_for_player(
                        'Ship is out of game field.')
                    return False

            for other_ship in self._ships:
                if other_ship.intersects(ship):
                    self.__class__.print_for_player(
                        'Ship is collapsing with other ship')
                    return False
            return True

        for length, count in ship_rules.items():
            self.__class__.print_for_player(
                'Create %d ship(s) with length of %d' % (count, length),
                with_space=True)
            for _ in range(count):
                ship = None
                while True:
                    ship = self._wait_for_ship(length, field.size)
                    if valid_ship_position():
                        break
                self._ships.append(ship)
                self.__class__.print_for_player('Ship created',
                                                with_space=True)

    # Shooting:

    def shoot(self, field, enemy_ships):
        def valid_shoot_position():
            return (shot is not None) and (shot not in self._shots)

        shot = None
        while not valid_shoot_position():
            shot = self._wait_for_shot(field.size, enemy_ships)
        self._shots.append(shot)
        return shot

    def create_fake_shots(self, ship, size):
        for ship_x, ship_y in ship:
            range_x = range(ship_x - 1, ship_x + 2)
            range_y = range(ship_y - 1, ship_y + 2)

            for x in range_x:
                for y in range_y:
                    if (x, y) in ship:
                        continue

                    if 0 <= y < size and 0 <= x < size:
                        fake = Shot(x, y, [], real=False)
                        if fake not in self._shots:
                            self._shots.append(fake)

    def take_shot(self, shot, size):
        for ship in self._ships:
            if shot in ship:
                try:
                    ship.do_damage(shot.x, shot.y)
                    return ship
                except ValueError:
                    pass

    # Interface methods:

    def _wait_for_name(self, exclude=None):
        return get_input("What's your name? ")

    def _wait_for_ship(self, length, size):
        while True:
            try:
                x, y = Player.__get_cords(size)

                if length != 1:
                    orientation_string = ', '.join(Ship.allowed_orientations())
                    orientation = get_input(
                        "How to orientate your ship (%s): " %
                        orientation_string
                    ).strip()
                    if orientation not in Ship.allowed_orientations():
                        raise ValueError()
                else:
                    orientation = Ship.ORIENTATION_VERTICAL

                return Ship(x, y, length, orientation)
            except (IndexError, ValueError, ):
                print('Bad input')

    def _wait_for_shot(self, size, enemy_ships):
        while True:
            try:
                # TODO: think about it.
                x, y = Player.__get_cords(size)
                return Shot(x, y, enemy_ships)
            except (IndexError, ValueError):
                print('Bad input')


class AIPlayer(Player):
    _verbose = False
    __ai_names = ('Joe', 'Chandler', 'Ross', )

    def __init__(self, human=False, exclude=None):
        super(AIPlayer, self).__init__(human=human, exclude=exclude)

    def _greet_player(self):
        print('Created a player for you: %s' % self.name)

    def _wait_for_name(cls, exclude=None):
        if exclude is None:
            exclude = []

        while True:
            name = random.choice(cls.__ai_names)
            if name not in exclude:
                return name

    def _wait_for_ship(self, length, size):
        orientation = random.choice(Ship.allowed_orientations())
        if orientation == Ship.ORIENTATION_VERTICAL:
            min_x_cord, min_y_cord = size - 1, size - length
        else:
            min_x_cord, min_y_cord = size - length, size - 1

        x = random.randint(0, min_x_cord)
        y = random.randint(0, min_y_cord)
        return Ship(x, y, length, orientation)

    def _wait_for_shot(self, size, enemy_ships):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        return Shot(x, y, enemy_ships)
