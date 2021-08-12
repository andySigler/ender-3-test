import math


POSITION_ROUNDING_PRECISION = 2


class Position(object):

    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '(x={0},y={1},z={2})'.format(self.x, self.y, self.z)

    def __add__(self, pos):
        ret = Position()
        # X
        if self.x is not None and pos.x is not None:
            ret.x = self.x + pos.x
        elif self.x is not None or pos.x is not None:
            raise ValueError('Cannot do {0} + {1}'.format(self, pos))
        # Y
        if self.y is not None and pos.y is not None:
            ret.y = self.y + pos.y
        elif self.y is not None or pos.y is not None:
            raise ValueError('Cannot do {0} + {1}'.format(self, pos))
        # Z
        if self.z is not None and pos.z is not None:
            ret.z = self.z + pos.z
        elif self.z is not None or pos.z is not None:
            raise ValueError('Cannot do {0} + {1}'.format(self, pos))
        return ret

    def __sub__(self, pos):
        ret = Position()
        # X
        if self.x is not None and pos.x is not None:
            ret.x = self.x - pos.x
        elif self.x is not None or pos.x is not None:
            raise ValueError('Cannot do {0} - {1}'.format(self, pos))
        # Y
        if self.y is not None and pos.y is not None:
            ret.y = self.y - pos.y
        elif self.y is not None or pos.y is not None:
            raise ValueError('Cannot do {0} - {1}'.format(self, pos))
        # Z
        if self.z is not None and pos.z is not None:
            ret.z = self.z - pos.z
        elif self.z is not None or pos.z is not None:
            raise ValueError('Cannot do {0} - {1}'.format(self, pos))
        return ret

    def __mul__(self, value):
        ret = self.duplicate()
        if ret.x is not None:
            ret.x = round(ret.x * value, POSITION_ROUNDING_PRECISION)
        if ret.y is not None:
            ret.y = round(ret.y * value, POSITION_ROUNDING_PRECISION)
        if ret.z is not None:
            ret.z = round(ret.z * value, POSITION_ROUNDING_PRECISION)
        return ret

    def __truediv__(self, value):
        ret = self.duplicate()
        if ret.x is not None:
            ret.x = round(ret.x / value, POSITION_ROUNDING_PRECISION)
        if ret.y is not None:
            ret.y = round(ret.y / value, POSITION_ROUNDING_PRECISION)
        if ret.z is not None:
            ret.z = round(ret.z / value, POSITION_ROUNDING_PRECISION)
        return ret

    def duplicate(self):
        return Position(x=self.x, y=self.y, z=self.z)

    def update(self, pos):
        if pos.x is not None:
            self.x = pos.x
        if pos.y is not None:
            self.y = pos.y
        if pos.z is not None:
            self.z = pos.z

    def distance_to(self, pos):
        assert self.x is not None
        assert self.y is not None
        assert self.z is not None
        assert pos.x is not None
        assert pos.y is not None
        assert pos.z is not None
        diff_x = self.x - pos.x
        diff_y = self.y - pos.y
        diff_z = self.z - pos.z
        return math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2) + math.pow(diff_z, 2))


if __name__ == '__main__':
    pos_a = Position(x=0, y=0, z=0)
    pos_b = Position(x=100, y=0, z=0)
    print(pos_a.distance_to(pos_b))
    pos_a = Position(x=1, y=0, z=3)
    pos_b = Position(x=100, y=2, z=-1)
    print(pos_a + pos_b)
    print(pos_a - pos_b)
    print(pos_a * 2)
    print(pos_a / 2)
    pos_b.update(pos_a)
    print(pos_b)
