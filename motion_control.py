import logging

from marlin_driver import MarlinDriver
from position import Position


logger = logging.getLogger('ender_3_test.motion_control')

MOTION_DEFAULT_TRAVEL_Z = 5 # default height from base while travelling
MOTION_ADDED_TRAVEL_Z = 2 # added height to current/target pos while travelling


class MotionController(object):

    def __init__(self):
        self.marlin = MarlinDriver()
        self.tool_position = Position(x=0, y=0, z=0)
        self.tool_offset = Position(x=0, y=0, z=0)

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

    def home(self, axis=''):
        # TODO: home safely depending on tool position
        self.marlin.home(axis)
        self._update_tool_position()

    def move_to(self, pos, relative=False, direct=False):
        if relative:
            pos = pos + self.tool_position

        travel_poses = []
        if direct:
            travel_poses.append(pos)
        else:
            travel_z = max(pos.z + MOTION_ADDED_TRAVEL_Z, MOTION_DEFAULT_TRAVEL_Z)
            travel_z = max(self.marlin.current_position.z + MOTION_ADDED_TRAVEL_Z, travel_z)
            travel_poses.append(Position(z=travel_z))
            travel_poses.append(Position(x=pos.x, y=pos.y))
            travel_poses.append(Position(z=pos.z))

        self.marlin.set_feedrate(self.speed)
        for p in travel_poses:
            self.marlin.move_to(self._apply_tool_offset(p))
        self._update_tool_position()

    def _apply_tool_offset(self, pos):
        return pos + self.tool_offset

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
    # ctrl.home()
    ctrl.set_speed(500)
    ctrl.set_tool_offset(Position(x=15.5, y=12, z=2))
    ctrl.move_to(Position(x=100, y=100, z=1))
    ctrl.move_to(Position(x=0, y=0, z=1))
    ctrl.move_to(Position(x=100), direct=True)
    ctrl.move_to(Position(y=50), relative=True, direct=True)
    ctrl.move_to(Position(y=100), direct=True)
    ctrl.disconnect()
