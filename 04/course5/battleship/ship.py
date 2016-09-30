# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from battleship.base import OnFieldBase

__author__ = 'sobolevn'


class Ship(OnFieldBase):
    ORIENTATION_HORIZONTAL = '-'
    ORIENTATION_VERTICAL = '|'

    def __init__(self, x, y, length, orientation):
        super(Ship, self).__init__(x, y)
        self.orientation = orientation
        self.length = length

        self._damage = []

    @property
    def is_alive(self):
        return len(self._damage) < self.length

    @classmethod
    def allowed_orientations(cls):
        return [
            cls.ORIENTATION_HORIZONTAL,
            cls.ORIENTATION_VERTICAL,
        ]

    def __iter__(self):
        if self.orientation == self.__class__.ORIENTATION_VERTICAL:
            vector = ((self.x + d, self.y) for d in range(self.length))
        else:
            vector = ((self.x, self.y + d) for d in range(self.length))

        return vector

    def __contains__(self, item):
        x1, y1 = self.__class__._decouple(item)

        return any((x1 == x and y1 == y) for x, y in self)

    def do_damage(self, x, y):
        if (x, y) in self._damage:
            raise ValueError('Already damaged')
        self._damage.append((x, y))

    def intersects(self, other):
        for x, y in self:
            for x1, y1 in other:
                d_x = abs(x - x1)
                d_y = abs(y - y1)
                if d_x <= 1 and d_y <= 1:
                    return True
        return False
