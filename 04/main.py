# -*- coding: utf-8 -*-

"""
Main file. Contains program execution logic.
"""
import sys
import random

from collections import OrderedDict
from battleship.players import Player
from battleship.field import Field
from battleship.ship import Ship
from battleship.shot import Shot


SHIPS_LIST = OrderedDict([(4, 1), (3, 2), (2, 3), (1, 4)])
FIELD_SIZE = 10
MOVES = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1),
    'r': 'rotate',
    'p': 'done',
    'f': 'fire'
}


def handle_user_input(message = ''):
    """
    Handles user input. List of accepted moves:
        'w' - up,
        's' - down,
        'a' - left,
        'd' - right
    :return: <str> current move.
    """
    if sys.version_info[0] == 2:
        input_function = raw_input
    else:
        input_function = input

    key_pressed = input_function(message)
    if key_pressed in MOVES.keys():
        return str(key_pressed)
    else:
        print('Please, use right buttons')


class MyException(Exception):
    def __init__(self, message, errors):
        # Now for your custom code...
        self.errors = errors
        self.message = message


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


def get_correct_name(text):
    """
    This function for fill emptiness of names
    """
    player = Player(caption=text).construct()

    while player.name == '':
        player = Player(caption=text).construct()

    return player


class UserExitException(KeyboardInterrupt):
    pass

def ship_place(field, ship):

    field.find_free_space(ship) #initializing coordinates to place ship
    field.draw_ship(ship)

    while True:
        move = handle_user_input('\nPlace your ship:')
        if move == 'p':
            field.lock_cells(ship)
            field.draw_ship(ship)
            break

        if move == 'r':
            field.erase_ship(ship)
            ship.direction = '-' if ship.direction == '|' else '|'
            field.draw_ship(ship)

        if move != None and move != 'r' and move != 'p':
            try:
                field.erase_ship(ship)
                ship.coord_x += MOVES.get(move)[0]
                ship.coord_y += MOVES.get(move)[1]
                field.check_field(ship)
                field.draw_ship(ship)
            except ValueError:
                field.find_free_space(ship)
                field.draw_ship(ship)


def create_fleet(player, mode = 'auto'):

    if mode == 'auto':
        for ship in SHIPS_LIST.items():
            ship_size, ship_count = ship[0], ship[1]
            for ship_number in range(ship_count):
                new_ship = Ship(ship_size)
                new_ship.coord_x = random.randint(0,9)
                new_ship.coord_y = random.randint(0,9)
                new_ship.direction = '|' if random.randint(0,1) == 1 else '-'
                player.field.find_free_space(new_ship)
                player.field.lock_cells(new_ship)
                player.field.draw_ship(new_ship)
                player.fleet.append(new_ship)

    else:
        for ship in SHIPS_LIST.items():
            ship_size, ship_count = ship[0], ship[1]
            for ship_number in range(ship_count):
                new_ship = Ship(ship_size)
                ship_place(player.field, new_ship)
                player.fleet.append(new_ship)
                print('Ship Added')

    print('Fleet for {1} ({0}) is generated. '.format(player.caption, player.name))


def perform_shot(player, opponent, shot):

    player.field.cursor_field[0][0] = 6

    while True:
        move = handle_user_input('\nMake your shot:')

        if move == 'f' \
         and player.opponent_field.field[shot.coord_x][shot.coord_y] in (0, 1, 2):

            overall_health, fired_ship, hit = opponent.check_health(shot)

            if overall_health == 0:
                print('Player {} wins! Congratulations!'.format(player.name))
                sys.exit()

            if hit:
                player.opponent_field.field[shot.coord_x][shot.coord_y] = 4
                if fired_ship.health ==0:
                    player.opponent_field.lock_cells(fired_ship)
                    player.opponent_field.draw_ship(fired_ship)

                player.opponent_field.show()
                print(' ||| {}, nice shot!'.format(player.name), end = '')
                break

            else:
                player.opponent_field.field[shot.coord_x][shot.coord_y] = 3
                opponent.opponent_field.show()
                print(" ||| {} missed. {}'s Turn.".format(player.name, opponent.name), end = '')
                raise MyException("", player.caption)
                break

        if move != None and move != 'r' and move != 'p' and move != 'f' :

            # cursor save position

            for i in range(0,10):
                for j in range(0,10):
                    if player.opponent_field.cursor_field[i][j] == 6:
                        #print('FOUND',player.opponent_field.cursor_field[i][j])
                        shot.coord_x = i
                        shot.coord_y = j

            player.opponent_field.cursor_field = [[0 for x in range(player.field.size)] for y in range(player.field.size)]
            
            # Bound check before placement
            if shot.coord_x+MOVES.get(move)[0] in range (0,10):
                shot.coord_x += MOVES.get(move)[0]
            if shot.coord_y+MOVES.get(move)[1] in range (0,10):
                shot.coord_y += MOVES.get(move)[1]

            player.opponent_field.cursor_field[shot.coord_x][shot.coord_y] = 6
            player.opponent_field.show()


            #if opponent.field.field[shot.coord_x][shot.coord_y] in (0,1,2) \
            #and player.opponent_field.field[shot.coord_x][shot.coord_y] in (0,1,2):
                #if opponent.field.field[shot.coord_x][shot.coord_y] == 2:

                    #player.opponent_field.field[shot.coord_x][shot.coord_y] = 4
                    #redraw(player)

                    #print(overall_health, ship_health, hit)

                    # TO DO: function to find ship decrease healt, if health = 0 put fake shots
            #     else:
            #
            #         player.opponent_field.field[shot.coord_x][shot.coord_y] = 3
            #         redraw(opponent)
            #         print('miss')
            #         # TO DO: next player turn
            #         raise MyException("Change players", player.caption)
            #
            #     break
            # else:
            #     print('wrong place to fire')

def main():
    """
    Main method, works infinitelly until user runs `exit` command.
    Or hits `Ctrl+C` in the console.
    """

    # Make Players
    player_1 = get_correct_name('Player 1')
    player_2 = get_correct_name('Player 2')

    #print('Hello %s: %s' % (player_1.caption, player_1.name))
    #print('Hello %s: %s' % (player_2.caption, player_2.name))

    # Make field
    player_1.field = Field(FIELD_SIZE, player_1.caption)
    player_1.opponent_field = Field(FIELD_SIZE, player_2.caption)

    player_2.field = Field(FIELD_SIZE, player_2.caption)
    player_2.opponent_field = Field(FIELD_SIZE, player_1.caption)

    # Place ships on field
    create_fleet(player_1)
    create_fleet(player_2)

    #player_1.game_field = Field(FIELD_SIZE, player_1.caption)
    game_player = player_1
    game_opponent = player_2

    input('\nPlease press enter to start your Battle!')
    game_player.opponent_field.show()

    while True:
        try:
            new_shot = Shot(0, 0)
            perform_shot(game_player, game_opponent, new_shot)
            # command = get_input_function()

            pass
        except UserExitException as ex:
            break
        except KeyboardInterrupt:
            print('Exit, bye!')
            break
        except MyException as ex:
            details = ex.args[0]
            print(details, end = '')
            game_player , game_opponent = game_opponent, game_player
            pass



if __name__ == '__main__':
    main()
