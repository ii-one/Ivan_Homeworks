# -*- coding: utf-8 -*-

"""
This module contains all the commands we work with.
If you want to create a new command it should be placed here.
"""

from __future__ import print_function

import sys
import inspect
import json
import models

# import custom_exceptions
from custom_exceptions import UserExitException



from utils import (
    #get_input_function,
    user_input
)

__author__ = 'sobolevn'


class BaseCommand(object):
    """
    Main class for all the commands.
    Defines basic method and values for all of them.
    Should be subclassed to create new commands.
    """

    @staticmethod
    def label():
        """
        This method is called to get the commands short name:
        like `new` or `list`.
        """
        raise NotImplemented()

    def perform(self, objects, *args, **kwargs):
        """
        This method is called to run the command's logic.
        """
        raise NotImplemented()


class ListCommand(BaseCommand):
    @staticmethod
    def label():
        return 'list'

    def perform(self, objects, *args, **kwargs):
        if len(objects) == 0:
            print('There are no items in storage.')
            return

        for index, obj in enumerate(objects):
            print('{}: {}'.format(index, str(obj)))


class NewCommand(BaseCommand):
    @staticmethod
    def label():
        return 'new'

    @staticmethod
    def _load_item_classes():
        # Dynamic load:
         get_module = sys.modules[models.__name__]
         def class_filter(klass):
             return inspect.isclass(klass) \
                    and klass.__module__ == get_module.__name__ \
                    and issubclass(klass, get_module.BaseItem) \
                    and klass is not get_module.BaseItem

         routes = inspect.getmembers(
                 sys.modules[get_module.__name__],
                 class_filter
         )
        # classes = {
        #     'ToDoItem': ToDoItem,
        #     'ToBuyItem': ToBuyItem,
        #     'ToReadItem': ToReadItem
        # }
         return dict((route.__name__, route) for _, route in routes)

    def perform(self, objects, *args, **kwargs):
        classes = self._load_item_classes()

        print('Select item type:')
        for index, name in enumerate(classes.keys()):
            print('{}: {}'.format(index, name))

        # input_function = get_input_function()
        # selection = None
        #
        # while True:
        #     try:
        #         selection = int(input_function('Input number: '))
        #         break
        #     except ValueError:
        #         print('Bad input, try again.')
        selection = user_input('Input number: ')

        selected_key = list(classes.keys())[selection]
        selected_class = classes[selected_key]
        print('Selected: {}'.format(selected_class.__name__))
        print()

        new_object = selected_class.construct()

        objects.append(new_object)
        print('Added {}'.format(str(new_object)))
        print()
        return new_object

class DoneCommand(BaseCommand):
    @staticmethod
    def label():
        return 'done'

    def perform (self, objects, *args, **kwargs):
        if len(objects) == 0:
            print('There are no items in storage.')
            return

        print('Select item you have done:')
        for index, obj in enumerate(objects):
            print('{}: {}'.format(index, str(obj)))

        selection = user_input('Input number: ')
        objects[selection].done = True

class UndoneCommand(BaseCommand):
    @staticmethod
    def label():
        return 'undone'

    def perform (self, objects, *args, **kwargs):
        if len(objects) == 0:
            print('There are no items in storage.')
            return

        print('Select item to mark undone:')
        for index, obj in enumerate(objects):
            print('{}: {}'.format(index, str(obj)))

        selection = user_input('Input number: ')
        objects[selection].done = False

class SaveCommand(BaseCommand):
    @staticmethod
    def label():
        return 'save'

    def perform(self, objects, *args, **kwargs):
        file_to_write = open('file_to_write', 'wb')
        pickle.dump(objects, file_to_write, protocol=None, fix_imports=True)
        file_to_write.close()

class ExitCommand(BaseCommand):
    @staticmethod
    def label():
        return 'exit'

    def perform(self, objects, *args, **kwargs):
        raise UserExitException('See you next time!')
