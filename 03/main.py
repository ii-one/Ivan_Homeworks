# -*- coding: utf-8 -*-

"""
Main file. Contains program execution logic.
"""

from __future__ import print_function

import inspect
import sys

import commands

# import custom_exceptions
from custom_exceptions import UserExitException

from models import (
    Storage,
)

from utils import get_input_function

__author__ = 'sobolevn'


def get_routes():
    """
    This function contains the dictionary of possible commands.
    :return: `dict` of possible commands, with the format: `name -> class`
    """

        # Dynamic load:
    get_module = sys.modules[commands.__name__]
    def class_filter(klass):
     return inspect.isclass(klass) \
            and klass.__module__ == get_module.__name__ \
            and issubclass(klass, get_module.BaseCommand) \
            and klass is not get_module.BaseCommand

    routes = inspect.getmembers(
         sys.modules[get_module.__name__],
         class_filter
    )

    return dict((route.label(), route) for _, route in routes)



def perform_command(command):
    """
    Performs the command by name.
    Stores the result in `Storage()`.
    :param command: command name, selected by user.
    """

    command = command.lower()
    routes = get_routes()

    try:
        command_class = routes[command]
        command_inst = command_class()

        storage = Storage()
        command_inst.perform(storage.items)
    except KeyError:
        print('Bad command, try again.')
    except UserExitException as ex:
        print(ex)
        raise


def parse_user_input():
    """
    Gets the user input.
    :return: `str` with the user input.
    """

    input_function = get_input_function()

    message = 'Input your command: (%s): ' % '|'.join(
            get_routes().keys())
    return input_function(message)


def main():
    """
    Main method, works infinitelly until user runs `exit` command.
    Or hits `Ctrl+C` in the console.
    """

    while True:
        try:
            command = parse_user_input()
            perform_command(command)
        except UserExitException:
            break
        except KeyboardInterrupt:
            print('Shutting down, bye!')
            break


if __name__ == '__main__':
    main()
