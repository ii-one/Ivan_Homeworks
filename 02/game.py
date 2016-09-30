# -*- coding: utf-8 -*-

# `random` module is used to shuffle field, see§:
# https://docs.python.org/3/library/random.html#random.shuffle
import random
import sys

__author__ = 'i-0ne'

if sys.version_info[0] == 2:
    input_function = raw_input
else:
    input_function = input


global field
global move_count
move_count = 1
field = []
# Empty tile, there's only one empty cell on a field:
EMPTY_MARK = 'x'

# Dictionary of possible moves if a form of:
# key -> delta to move the empty tile on a field.
MOVES = {
    'w': -4,
    's': 4,
    'a': -1,
    'd': 1,
}

#пусть квадратик с числом iрасположен до (если считать слева направо и сверху
#вниз) k квадратиков с числами меньшими  i.. Будем считать  ni=k, то есть
#если после костяшки с  i-м числом нет чисел, меньших  i, то  k=0..
#Также введем число  e — номер ряда пустой клетки (считая с 1). Если сумма
#E от 1 до 15 ni + E является нечётной, то решения головоломки не существует
def shuffle_field():
    """
    This method is used to create a field at the very start of the game.
    :return: list with 16 randomly shuffled tiles,
    one of which is a empty space.
    """
    field = [i for i in range(16)]
    counter = 0
    random.shuffle(field)
    for position, element in enumerate(field):
        for looper in range(position, 16):
            if field[looper] < element:
                 counter +=1            #counting K for all n in game field
    a = field.index(0)
    line_number = abs(a//4+1)
    counter += line_number # adding line number according to formula

    if not counter % 2 == 0:
        print('Reshuffling! Board cannot be solved. "Odd check" is', counter)
        field = shuffle_field()
        return field
    else:
        print('Ок. "Odd check" for this board is', counter)
        field = [EMPTY_MARK if i==0 else i for i in field]
        print(len(field))
        return field


def print_field(field):
    """
    This method prints field to user.
    :param field: current field state to be printed.
    :return: None
    """
    print('\n')
    field = [field[i:i + 4] for i in range(0, len(field), 4)]
    for count, rows in enumerate(field):
        formatted_row = "│".join(['{:^3}'.format(element) for element in rows])
        horizontal_line = "┼".join(['{:3}'.format('─' * 3) for element in rows])
        print(formatted_row)
        if count < 3:  # Ignoring bottom horizontal line
            print(horizontal_line)
    return None


def is_game_finished(field):
    """
    This method checks if the game is finished.
    :param field: current field state.
    :return: True if the game is finished, False otherwise.
    """
    check_field = list(field)                      #making copy, to prevent damage to game field
    del check_field[check_field.index(EMPTY_MARK)] #Preparing for compare, only int inside
    return check_field == sorted(check_field)


def perform_move(field, key):
    """
    Moves empty-tile inside the field.
    :param field: current field state.
    :param key: move direction.
    :return: new field state (after the move).
    :raises: IndexError if the move can't me done.
    """
    global move_count
    a, b = field.index(EMPTY_MARK), field.index(EMPTY_MARK) + MOVES[key]
    string_change = abs(a//4 - b//4)
    if (abs(a-b) == 1 or b < 0) and string_change == 1:
        raise IndexError
    else:
        field[b], field[a] = field[a], field[b]
        move_count +=1
        return field


def handle_user_input(message =''):
    """
    Handles user input. List of accepted moves:
        'w' - up,
        's' - down,
        'a' - left,
        'd' - right
    :return: <str> current move.
    """
    key_pressed = input_function(message)
    if key_pressed in MOVES.keys():
        return str(key_pressed)
    else:
        key_pressed = handle_user_input("Please use '{}' keys: ".format("','".join(MOVES.keys())))
        return str(key_pressed)


def main():
    """
    The main method. It stars when the program is called.
    It also calls other methods.
    :return: None
    """
    field = shuffle_field()
    message = 'Moves: 0. Your move >'
    while not is_game_finished(field):
        try:
            print_field(field)
            key = handle_user_input(message)
            message = 'Moves: {}. Your move >'.format(move_count)
            perform_move(field, key)
        except KeyboardInterrupt:
            print('\nShutting down! Bye!')
            print('\nTotal moves: {}\n'.format(move_count-1))
            sys.exit()
        except IndexError:
            message = 'Restricted move. Try another direction >'
    return None


if __name__ == '__main__':
    # See what this means:
    # http://stackoverflow.com/questions/419163/what-does-if-name-main-do
    main()
