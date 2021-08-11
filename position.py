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
        diff_y = self.y - pos.x
        diff_z = self.z - pos.z
        xy_dist = math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))
        return abs(math.sqrt(math.pow(xy_dist, 2) + math.pow(diff_z, 2)))
