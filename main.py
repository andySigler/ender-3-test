import logging

from ender_3_serial import Ender3Serial

logger = logging.getLogger('ender_3_test.marlin')


MARLIN_GCODE_HOME = 'G28'

MARLIN_ACK = 'ok'
MARLIN_BUSY_MSG = 'echo:busy: processing'


class MarlinDriver(object):

    def __init__(self):
        self.ender_3 = Ender3Serial()
        self.position = {'X': 0, 'Y': 0, 'Z': 0}

    def connect(self):
        self.ender_3.connect_to_ender_3()

    def close(self):
        self.ender_3.close()

    def command(self, gcode):
        self.ender_3.write_string(gcode)
        rsp_list = self.ender_3.read_strings(ack=MARLIN_ACK)
        rsp_list = self._filter_response_list(rsp_list)
        return rsp_list

    def home(self, axis=''):
        logger.debug('Homing {0}'.format(axis))
        home_msg = '{0}{1}'.format(MARLIN_GCODE_HOME, axis.upper())
        rsp_list = self.command(home_msg)
        self.position = self._parse_response_coordinates(rsp_list[0])

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
            axis.split(':')[0]: float(axis.split(':')[1])
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
    marlin.home('Z')
    marlin.close()
