import logging

from ender_3_serial import Ender3Serial
from position import Position


logger = logging.getLogger('ender_3_test.marlin')

MARLIN_GCODE_HOME = 'G28'
MARLIN_GCODE_POSITION_GET = 'M114'
MARLIN_GCODE_MOVE = 'G0'
MARLIN_GCODE_MAX_FEEDRATE = 'M203'
MARLIN_GCODE_FINISH_MOVES = 'M400'

MARLIN_DEFAULT_MAX_FEEDRATE = {
    'x': 500,
    'y': 500,
    'z': 10
}

MARLIN_ACK = 'ok'
MARLIN_BUSY_MSG = 'echo:busy: processing'


class MarlinDriver(object):

    def __init__(self):
        self.ender_3 = Ender3Serial()
        self.current_position = Position()
        self.target_position = Position()

    def connect(self):
        self.ender_3.connect_to_ender_3()
        self.update_position(initialize=True)

    def disconnect(self):
        self.ender_3.close()

    def command(self, gcode):
        gcode_with_finish = '{0} {1}'.format(gcode, MARLIN_GCODE_FINISH_MOVES)
        self.ender_3.write_string(gcode)
        rsp_list = self.ender_3.read_strings(ack=MARLIN_ACK)
        rsp_list = self._filter_response_list(rsp_list)
        return rsp_list

    def update_position(self, initialize=False):
        rsp = self.command(MARLIN_GCODE_POSITION_GET)
        parsed_rsp = self._parse_response_coordinates(rsp[0])
        pos = Position(**parsed_rsp)
        self.current_position.update(pos)
        if initialize:
            self.target_position.update(pos)
        else:
            target_dist = self.current_position.distance_to(self.target_position)
            if target_dist > 1:
                raise RuntimeError(
                    'Current position {0} is {1} from target position {2}'.format(
                        self.current_position, target_dist, self.target_position))

    def home(self, axis=''):
        if not axis:
            axis = 'xyz'
        logger.debug('Homing {0}'.format(axis))
        home_msg = '{0} {1}'.format(MARLIN_GCODE_HOME, axis.upper())
        if 'x' in axis:
            self.target_position.update(Position(x=0))
        if 'y' in axis:
            self.target_position.update(Position(y=0))
        if 'z' in axis:
            self.target_position.update(Position(z=0))
        self.set_max_feedrate(**MARLIN_DEFAULT_MAX_FEEDRATE)
        self.command(home_msg)
        self.update_position()

    def move_to(self, pos, speed=None):
        self.target_position.update(pos)
        move_msg = '{0}'.format(MARLIN_GCODE_MOVE)
        if pos.x is not None:
            move_msg = '{0} X{1}'.format(move_msg, round(pos.x, 3))
        if pos.y is not None:
            move_msg = '{0} Y{1}'.format(move_msg, round(pos.y, 3))
        if pos.z is not None:
            move_msg = '{0} Z{1}'.format(move_msg, round(pos.z, 3))
        if speed is not None:
            move_msg = '{0} F{1}'.format(move_msg, speed)
        self.command(move_msg)
        self.update_position()

    def set_feedrate(self, feedrate):
        feedrate = feedrate * 60 # mm/m
        move_msg = '{0} F{1}'.format(MARLIN_GCODE_MOVE, feedrate)
        self.command(move_msg)

    def set_max_feedrate(self, x=None, y=None, z=None):
        rate_msg = '{0}'.format(MARLIN_GCODE_FEEDRATE)
        if x is not None:
            rate_msg = '{0} X{1}'.format(rate_msg, x)
        if y is not None:
            rate_msg = '{0} Y{1}'.format(rate_msg, y)
        if z is not None:
            rate_msg = '{0} Z{1}'.format(rate_msg, z)
        self.command(rate_msg)

    def _filter_response_list(self, rsp_list):
        filtered_list = []
        for rsp in rsp_list:
            if MARLIN_BUSY_MSG in rsp:
                continue
            if MARLIN_ACK in rsp:
                continue
            filtered_list.append(rsp)
        return filtered_list

    def _parse_response_coordinates(self, rsp):
        # X:0.00 Y:0.00 Z:0.00 E:0.00 Count X:0 Y:0 Z:0
        return {
            axis.split(':')[0].lower(): float(axis.split(':')[1])
            for axis in rsp.split(' ')[:3]
        }



if __name__ == '__main__':
    import sys

    logging.basicConfig(
        # filename='logfile.log',
        stream=sys.stdout, 
        filemode='w',
        format='%(levelname)s %(asctime)s - %(message)s', 
        level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    marlin = MarlinDriver()
    marlin.connect()
    marlin.set_feedrate(z=5)
    marlin.move_to(Position(z=10))
    marlin.set_feedrate(z=1)
    marlin.move_to(Position(z=20))
    marlin.set_feedrate(z=5)
    marlin.home('z')
    marlin.disconnect()
