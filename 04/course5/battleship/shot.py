# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from battleship.base import OnFieldBase

__author__ = 'sobolevn'


class Shot(OnFieldBase):
    def __init__(self, x, y, enemy_ships, real=True):
        super(Shot, self).__init__(x, y)
        self.hit = False
        self.real = real

        for ship in enemy_ships:
            for x, y in ship:
                if self.x == x and self.y == y:
                    self.hit = True

    def __eq__(self, other):
        x1, y1 = self.__class__._decouple(other)
        return self.x == x1 and self.y == y1

    def __str__(self):
        status = 'Hit' if self.hit else 'Missed'
        return '%s (%d, %d)' % (status, self.x + 1, self.y + 1)

    def add(self, cords, ships):
        x1, y1 = self.__class__._decouple(cords)
        return Shot(self.x + x1, self.y + y1, ships)
