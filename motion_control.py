import logging

from marlin_driver import MarlinDriver
from position import Position


logger = logging.getLogger('ender_3_test.motion_control')


class MotionController(object):

    def __init__(self):
        self.marlin = MarlinDriver()

    def connect(self):
        self.marlin.connect()

    def disconnect(self):
        self.marlin.disconnect()

    def home(self):
        # TODO: home safely...
        self.marlin.home()


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
    ctrl.disconnect()
