# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = 'sobolevn'


def print_with_space(message):
    print()
    print(message)


def get_input(message):
    try:
        input_function = raw_input
    except NameError:
        input_function = input

    return input_function(message)
