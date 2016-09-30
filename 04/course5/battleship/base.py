# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from battleship.utils import print_with_space

__author__ = 'sobolevn'


class Informational(object):
    _verbose = True

    @classmethod
    def print_for_player(cls, message, with_space=False):
        if cls._verbose:
            print_f = print if not with_space else print_with_space
            print_f(message)


class OnFieldBase(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def _decouple(other):
        if isinstance(other, (tuple, list)):
            x1, y1 = other
        else:
            x1, y1 = other.x, other.y
        return x1, y1
