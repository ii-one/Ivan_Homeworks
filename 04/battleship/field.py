import sys

STATUS = {0: u' · ',   # Empty
          1: u' • ',   # Blocked to place ship
          2: u' ▩ ',   # Ship
          3: u' ✓ ',   # Miss
          4: u' 🔥 ',  # Hit
          5: u' ╳ ',   # Killed
          6: u' ¤ ' # shot cursor
}

MOVES = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1),
    'p': 'done',
    'f': 'fire'
}

class Field(object):
    """
    Field contains all the data (ships, hits, locked spaces, and is used to make
    visual output to the user.
    """

    # Every generated field filled with '0'
    def __init__(self, size, owner = None, field = [], cursor_field = []):
        self.size = size
        self.field = [[0 for x in range(size)] for y in range(size)]
        self.cursor_field = [[0 for x in range(size)] for y in range(size)]
        self.cursor_field[0][0] = 6
        self.field_to_show = [[0 for x in range(size)] for y in range(size)]
        self.owner = owner
        self.construct()

    def construct(self):
        self.field = [[0 for x in range(self.size)] for y in range(self.size)]
        self.cursor_field = [[0 for x in range(self.size)] for y in range(self.size)]
        self.cursor_field[0][0] = 6
    # Formats and outputs field to user
    def show(self):
        """
        This method prints field to user.
        :return: None
        """
        print('\n'*80)
        print('Field of:', self.owner)

        for x in range(0,self.size):
            print('{:3}'.format(x+1), end =' ') #Line number
            for y in range(0,self.size):
                # Merging layers
                if self.cursor_field[x][y] == 6:
                    self.field_to_show[x][y] = self.cursor_field[x][y]
                else:
                    self.field_to_show[x][y] = self.field[x][y]
                # Printing merged field
                print('{:3}'.format(STATUS[self.field_to_show[x][y]]), end='')

            print('') # Placing end-of-line to place lines one by one

        # Format and print 'y' numbers line
        print ('    ', end='')
        for line_numbers, elements in enumerate(self.field[0]):
            print('{:^3}'.format(line_numbers + 1), end ='')

        #print('\n')

    def check_field(self, ship):
        """Function to check if it is possible to place ship on the field"""

        if ship.direction == '|':
            # Checking field edges
            if ship.coord_y not in range(0, 10) or ship.coord_x+ship.size > 10  or ship.coord_x < 0:
                raise ValueError

            # Checking for empty space under the ship
            delta = 0
            for i in range(ship.size):
                delta += self.field[ship.coord_x+i][ship.coord_y]
            if delta != 0:
                raise ValueError
            else:
                return True

        if ship.direction == '-':
            # Checking field edges
            if ship.coord_x not in range(0, 10) or ship.coord_y+ship.size > 10  or ship.coord_y < 0:
                raise ValueError

            # Checking for empty space under the ship
            delta = 0
            for i in range(ship.size):
                delta += self.field[ship.coord_x][ship.coord_y+i]
            if delta != 0:
                raise ValueError
            else:
                return True


    def lock_cells(self, ship):
        """Function drawing one cell thickness line with locked STATUS around ship """
        lock_x1, lock_y1 = ship.coord_x - 1, ship.coord_y - 1
        if ship.direction == '|':
            lock_x2 = lock_x1 + 2
            lock_y2 = lock_y1 + ship.size + 1
        if ship.direction == '-':
            lock_x2 = lock_x1 + ship.size + 1
            lock_y2 = lock_y1 + 2

        for y in range(lock_x2-lock_x1+1):
            for x in range(lock_y2-lock_y1+1):
                # To prevent IndexError
                if lock_x1+x in range (0, 10) and lock_y1+y in range (0, 10):
                    self.field[lock_x1+x][lock_y1+y] = 1 if ship.health != 0 else 3

    # Method is under develop, to provide correct work in all directions (
    # Now it works correctly only from left to right
    # 100% Correct for auto-mode
    def find_free_space(self, ship):
        """This function is to find free space for a ship
            iterating over the field"""
        placed = False
        if ship.coord_x is None: ship.coord_x = 0
        if ship.coord_y is None: ship.coord_y = 0

        while not placed:
            try:
                self.check_field(ship)
                placed = True
            except ValueError:
                ship.coord_y += 1

            # Reached end of field, rotate ship and start scan again
            if ship.coord_x == 10 and ship.coord_y == 10:
                ship.coord_x = 0
                ship.coord_y = 0
                ship.direction = '-' if ship.direction =='|' else '|'

            # Reached end of line, switching to next one
            if ship.coord_y == 10:
                ship.coord_x += 1
                ship.coord_y = 0

    def place(self, ship):
        """ This function to be used if we decide to move all ship place handling
            inside field Class"""
        if ship.coord_x == None:
            ship.coord_x = 0
            print('x=0')
        if ship.coord_y == None:
            print('y=0')
            ship.coord_y = 0
        print (self.check_field(ship))
        if self.check_field(ship):
             self.lock_cells(ship)
             #self.show()
             return ship
        else:
             self.find_free_space(ship)
             print ('loooking')
             #self.show()
             return ship

#    - checks if field under ship equals 0 (no locked cells, no ships)
#      if ok - lock cells around, draw new field state
#    the only problem is to save previous field state, to redraw on a new user
#    movement

#    My idea is that ship changes it coordinates by user keyboard input, if
#    it is not possible to place ship at coordinates, than place method
#    trying to find nearest ones and placing ship there

#    New ship is trying to place on the field
#    If ok - drawing ship at a place and waiting for new ship movement or accept by
#     'p' key (place command), then calling place method again with new ship, and so on


# may be it is better to handle input somewhere outside?????
    # @staticmethod
    # def handle_user_input(message = ''):
    #     """
    #     Handles user input. List of accepted moves:
    #         'w' - up,
    #         's' - down,
    #         'a' - left,
    #         'd' - right
    #     :return: <str> current move.
    #     """
    #     if sys.version_info[0] == 2:
    #         input_function = raw_input
    #     else:
    #         input_function = input
    #
    #     key_pressed = input_function(message)
    #     if key_pressed in MOVES.keys():
    #         return str(key_pressed)
    #     else:
    #         print('Use right button!')

    def erase_ship(self, ship):
        """ фукция для стирания поля/кораблей"""
        if ship.direction == '|':
            for point in range(ship.size):
                self.field[ship.coord_x+point][ship.coord_y] = 0
        else:
            for point in range(ship.size):
                self.field[ship.coord_x][ship.coord_y+point] = 0
        return True

    def draw_ship(self, ship):
        """ фукция для отрисовки поля/кораблей"""
        if ship.direction == '|':
            for point in range(ship.size):
                self.field[ship.coord_x+point][ship.coord_y] = 2 if ship.health != 0 else 5
        else:
            for point in range(ship.size):
                self.field[ship.coord_x][ship.coord_y+point] = 2 if ship.health != 0 else 5


        #self.show()
        return True

    # def draw_cursor(self, shot):
    #     """ фукция для отрисовки поля/кораблей"""
    #     self.cursor_field[shot.coord_x][shot.coord_y] = 6
    #     self.show()
    #     return True
    # def erase_cursor(self, shot):
    #     """ фукция для отрисовки поля/кораблей"""
    #     self.cursor_field[shot.coord_x][shot.coord_y] = 0
    #     self.show()
    #     return True

#    def place(self, ship):
# may be it is better to handle input somewhere outside?????
