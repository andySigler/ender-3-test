import math


class Position(object):

    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '(x={0},y={1},z={2})'.format(self.x, self.y, self.z)

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
