# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from collections import OrderedDict
from contextlib import contextmanager

from battleship.utils import print_with_space
from battleship.players import Player, AIPlayer
from battleship.field import GameField
from battleship.base import Informational
from battleship.ship import Ship

__author__ = 'sobolevn'


class GameController(Informational):
    # {length_of_ship: number_of_ships}
    # Why ordered dict? Because I had issues with random ships:
    # When placing big ships before the small ones, it is easier to
    # generate valid result.
    SHIP_RULES = OrderedDict([(4, 1), (3, 2), (2, 3), (1, 4)])

    @staticmethod
    def _on_exit_callback():
        print('exiting..')

    def __init__(self, size=10, ship_rules=None,
                 first_human=True, second_human=True):
        with self._catch_exit(self.__class__._on_exit_callback):
            # Creating players:
            self.players = []
            first_player_class = Player if first_human else AIPlayer
            first_player = first_player_class(human=True)
            self.players.append(first_player)

            # Second player might be a person or a computer:
            second_player_class = Player if second_human else AIPlayer
            self.players.append(second_player_class(
                human=second_human,
                exclude=(first_player.name, ),
            ))

            # Creating empty field:
            self.field = GameField(10)

            # Placing the ships:
            if ship_rules is None:
                self.ship_rules = self.__class__.SHIP_RULES

            for player in self.players:
                self.__class__.print_for_player(
                    "It's time for %s to place his ships!" % player.name,
                    with_space=True)
                player.place_ships(self.ship_rules, self.field)

    def is_game_finished(self):
        for player in self.players:
            if all(not ship.is_alive for ship in player.ships):
                return True
        return False

    @contextmanager
    def _catch_exit(self, exit_callback):
        try:
            yield
        except KeyboardInterrupt:
            exit_callback()

    def print_fields(self, shooter, waiter):
        self.__class__.print_for_player(
            "It's now %s's turn to shoot. Own field:" % shooter,
            with_space=True
        )
        self.field.render_own(shooter, enemy=waiter)

        self.__class__.print_for_player(
            "Enemy's field:", with_space=True)
        self.field.render_enemy(shooter)

    def start_game(self):
        change_player_on_turn = False

        print_with_space('Starting the game!')

        shooter, waiter = self.players
        while not self.is_game_finished():
            if change_player_on_turn:
                shooter, waiter = waiter, shooter

            self.print_fields(shooter, waiter)
            shot = shooter.shoot(self.field, waiter.ships)
            if shot.hit:
                ship = waiter.take_shot(shot, self.field.size)
                if not ship.is_alive:
                    shooter.create_fake_shots(ship, self.field.size)
            change_player_on_turn = not shot.hit

            self.print_fields(shooter, waiter)
            self.__class__.print_for_player(shot)
        # The have finished:
        print('Game over, %s won!' % shooter)

if __name__ == '__main__':
    # Here you can modify the players type;
    game = GameController(size=10, first_human=True, second_human=False)
    game.start_game()
