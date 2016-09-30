class Ship(object):
    """
    Ship basic classes
    """
    ORIENTATION_HORIZONTAL = '-'
    ORIENTATION_VERTICAL = '|'

    def __init__(self, size, coord_x=0, coord_y=0, direction=ORIENTATION_HORIZONTAL):
        self.size = size
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.direction = direction
        self.health = size
