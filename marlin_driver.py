import logging

from ender_3_serial import Ender3Serial
from position import Position


logger = logging.getLogger('ender_3_test.marlin')

MARLIN_GCODE_HOME = 'G28'
MARLIN_GCODE_POSITION_GET = 'M114'
MARLIN_GCODE_MOVE = 'G0'
MARLIN_GCODE_MAX_FEEDRATE = 'M203'
MARLIN_GCODE_MAX_ACCELERATION = 'M201'
MARLIN_GCODE_ACCELERATION = 'M204'
MARLIN_GCODE_FINISH_MOVES = 'M400'

MARLIN_DEFAULT_MAX_SPEED = {
    'x': 500,
    'y': 500,
    'z': 200
}

MARLIN_ACK = b'ok'
MARLIN_BUSY_MSG = b'echo:busy: processing'


class MarlinDriver(object):

    def __init__(self):
        self.ender_3 = Ender3Serial()
        self.current_position = Position(x=0, y=0, z=0)
        self.max_speed = MARLIN_DEFAULT_MAX_SPEED.copy()

    def connect(self):
        self.ender_3.connect_to_ender_3()
        self.update_position()

    def disconnect(self):
        self.ender_3.close()

    def command(self, gcode):
        self.ender_3.write_string(gcode)
        rsp_list = self.ender_3.read_bytes(ack=MARLIN_ACK)
        rsp_list = self._filter_response_list(rsp_list)
        return rsp_list

    def update_position(self):
        self.finish_moves()
        rsp = self.command(MARLIN_GCODE_POSITION_GET)
        parsed_rsp = self._parse_response_coordinates(rsp[0])
        pos = Position(**parsed_rsp)
        self.current_position.update(pos)

    def home(self, axis=''):
        if not axis:
            axis = 'xyz'
        logger.debug('Homing {0}'.format(axis))
        home_msg = '{0} {1}'.format(MARLIN_GCODE_HOME, axis.upper())
        if 'x' in axis:
            self.current_position.update(Position(x=0))
        if 'y' in axis:
            self.current_position.update(Position(y=0))
        if 'z' in axis:
            self.current_position.update(Position(z=0))
        self.set_max_speed(**self.max_speed)
        self.command(home_msg)
        self.finish_moves()
        self.update_position()

    def finish_moves(self):
        self.command(MARLIN_GCODE_FINISH_MOVES)

    def move_to(self, pos, speed=None):
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
        self.current_position.update(pos)

    def set_acceleration(self, acceleration):
        # default is 1000
        accel_msg = '{0} T{1}'.format(MARLIN_GCODE_ACCELERATION, acceleration)
        self.command(accel_msg)

    def set_speed(self, speed):
        speed = speed * 60 # mm/m
        speed_msg = '{0} F{1}'.format(MARLIN_GCODE_MOVE, speed)
        self.command(speed_msg)

    def set_max_acceleration(self, x=None, y=None, z=None):
        # defaults (x=500, y=500, z=100)
        accel_msg = '{0}'.format(MARLIN_GCODE_MAX_ACCELERATION)
        if x is not None:
            accel_msg = '{0} X{1}'.format(accel_msg, x)
        if y is not None:
            accel_msg = '{0} Y{1}'.format(accel_msg, y)
        if z is not None:
            accel_msg = '{0} Z{1}'.format(accel_msg, z)
        self.command(accel_msg)

    def set_max_speed(self, x=None, y=None, z=None):
        rate_msg = '{0}'.format(MARLIN_GCODE_MAX_FEEDRATE)
        if x is not None:
            self.max_speed['x'] = x
            rate_msg = '{0} X{1}'.format(rate_msg, x)
        if y is not None:
            self.max_speed['y'] = y
            rate_msg = '{0} Y{1}'.format(rate_msg, y)
        if z is not None:
            self.max_speed['z'] = z
            rate_msg = '{0} Z{1}'.format(rate_msg, z)
        self.command(rate_msg)

    def _filter_response_list(self, rsp_list):
        filtered_list = []
        for rsp in rsp_list:
            if MARLIN_BUSY_MSG in rsp:
                continue
            if MARLIN_ACK in rsp:
                continue
            filtered_list.append(rsp.decode('utf-8'))
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
    marlin.home()

    # marlin.set_max_speed(z=200)
    # marlin.set_speed(200)
    # marlin.move_to(Position(z=50))

    marlin.set_max_speed(y=500)
    marlin.set_speed(500)
    marlin.set_max_acceleration(y=2000)
    marlin.set_acceleration(2000)
    marlin.move_to(Position(y=150))
    marlin.move_to(Position(y=0))

    marlin.disconnect()
