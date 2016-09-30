# -*- coding: utf-8 -*-

from __future__ import print_function

from battleship.base import Informational

__author__ = 'sobolevn'


class GameField(Informational):
    INITIAL_STATE = '.'
    SHIP_STATE = '='

    MISS = 'o'
    HIT = 'x'

    def __init__(self, size):
        self.size = size

    @staticmethod
    def _pretty_print_field(field):
        for row in field:
            print(row)

    def _render_initial(self):
        field = []
        for x in range(self.size):
            row = []
            for y in range(self.size):
                row.append(self.__class__.INITIAL_STATE)
            field.append(row)
        return field

    def render_own(self, player, enemy=None):
        field = self._render_initial()

        for ship in player.ships:
            for x, y in ship:
                field[x][y] = self.__class__.SHIP_STATE

        if enemy is not None:
            for shot in enemy.shots:
                if field[shot.x][shot.y] == self.__class__.INITIAL_STATE:
                    field[shot.x][shot.y] = self.__class__.MISS
                else:
                    field[shot.x][shot.y] = self.__class__.HIT
        self._pretty_print_field(field)

    def render_enemy(self, player):
        field = self._render_initial()

        for shot in player.shots:
            field[shot.x][shot.y] = self.__class__.HIT if shot.hit \
                else self.__class__.MISS
        self._pretty_print_field(field)
