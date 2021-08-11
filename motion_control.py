import logging

from marlin_driver import MarlinDriver
from position import Position


logger = logging.getLogger('ender_3_test.motion_control')

MOTION_DEFAULT_TRAVEL_Z = 5 # default height from base while travelling
MOTION_DEFAULT_SPEED = 300


class MotionController(object):

    def __init__(self):
        self.marlin = MarlinDriver()
        self.tool_position = Position(x=0, y=0, z=0)
        self.tool_offset = Position(x=0, y=0, z=0)
        self.safe_z = MOTION_DEFAULT_TRAVEL_Z
        self.speed = MOTION_DEFAULT_SPEED

    def connect(self):
        self.marlin.connect()
        self._update_tool_position()

    def disconnect(self):
        self.marlin.disconnect()

    def set_speed(self, speed):
        self.speed = speed

    def set_tool_offset(self, offset):
        self.tool_offset.update(offset)
        self._update_tool_position()

    def set_safe_z(self, safe_z):
        self.safe_z = safe_z

    def home(self, axis=''):
        # TODO: home safely depending on tool position
        self.marlin.home(axis)
        self._update_tool_position()

    def move_to(self, pos, relative=False, direct=False, safe_z=None):
        if self.tool_position.distance_to(pos) == 0:
            # same position, do nothing
            return
        if not relative:
            xy_tool = Position(x=self.tool_position.x, y=self.tool_position.y, z=0)
            xy_pos = Position(x=pos.x, y=pos.y, z=0)
            if xy_tool.distance_to(xy_pos) == 0:
                # same XY position, so just move directly to Z
                direct = True
        if safe_z is None:
            safe_z = self.safe_z
        if relative:
            # Positions are allowed to have None as an axis value
            if pos.x is not None:
                pos.x += self.tool_position.x
            if pos.y is not None:
                pos.y += self.tool_position.y
            if pos.z is not None:
                pos.z += self.tool_position.z

        travel_poses = []
        if direct:
            travel_poses.append(pos)
        else:
            travel_z = max(pos.z, safe_z)
            travel_z = max(self.marlin.current_position.z, travel_z)
            travel_poses.append(Position(z=travel_z))
            travel_poses.append(Position(x=pos.x, y=pos.y))
            travel_poses.append(Position(z=pos.z))

        self.marlin.set_speed(self.speed)
        for p in travel_poses:
            self.marlin.move_to(self._apply_tool_offset(p))
        self._update_tool_position()

    def _apply_tool_offset(self, pos):
        # Positions are allowed to have None as an axis value
        if pos.x is not None:
            pos.x += self.tool_offset.x
        if pos.y is not None:
            pos.y += self.tool_offset.y
        if pos.z is not None:
            pos.z += self.tool_offset.z
        return pos

    def _update_tool_position(self):
        self.tool_position = self.marlin.current_position - self.tool_offset


if __name__ == '__main__':
    import sys

    logging.basicConfig(
        # filename='logfile.log',
        stream=sys.stdout, 
        filemode='w',
        format='%(levelname)s %(asctime)s - %(message)s', 
        level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    ctrl = MotionController()
    ctrl.connect()
    ctrl.home()
    ctrl.set_speed(500)
    ctrl.set_tool_offset(Position(x=15.5, y=12, z=2))
    ctrl.move_to(Position(x=100, y=100, z=1))
    ctrl.move_to(Position(x=0, y=0, z=1))
    ctrl.move_to(Position(x=100), direct=True)
    ctrl.move_to(Position(y=50), relative=True, direct=True)
    ctrl.move_to(Position(y=100), direct=True)
    ctrl.disconnect()
