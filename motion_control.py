import logging

from marlin_driver import MarlinDriver
from position import Position


logger = logging.getLogger('ender_3_test.motion_control')

MOTION_DEFAULT_TRAVEL_Z = 20 # default height from base while travelling
MOTION_ADDED_TRAVEL_Z = 5 # added height to current/target pos while travelling


class MotionController(object):

    def __init__(self):
        self.marlin = MarlinDriver()

    def connect(self):
        self.marlin.connect()

    def disconnect(self):
        self.marlin.disconnect()

    def set_speed(self, speed):
        self.speed = speed

    def home(self):
        # TODO: home safely depending on tool position
        self.marlin.home()

    def move_to(self, pos, direct=False):
        self.marlin.set_feedrate(self.speed)
        if direct:
            self.marlin.move_to(pos)
        else:
            travel_z = max(pos.z + MOTION_ADDED_TRAVEL_Z, MOTION_DEFAULT_TRAVEL_Z)
            travel_z = max(self.marlin.current_position.z + MOTION_ADDED_TRAVEL_Z, travel_z)
            self.marlin.move_to(Position(z=travel_z))
            self.marlin.move_to(Position(x=pos.x, y=pos.y))
            self.marlin.move_to(Position(z=pos.z))


if __name__ == '__main__':
    import sys

    logging.basicConfig(
        # filename='logfile.log',
        stream=sys.stdout, 
        filemode='w',
        format='%(levelname)s %(asctime)s - %(message)s', 
        level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    # ser_logger = logging.getLogger('ender_3_test.serial')
    # ser_logger.setLevel(logging.DEBUG)

    ctrl = MotionController()
    ctrl.connect()
    # ctrl.home()
    ctrl.set_speed(100)
    ctrl.move_to(Position(x=200), direct=True)
    ctrl.disconnect()
