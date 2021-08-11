import logging

import serial
from serial.tools.list_ports import comports


logger = logging.getLogger('ender_3_test.serial')

# SERIAL PORT
ENDER_3_USB_HWID = '1A86:7523'
ENDER_3_BAUDRATE = 115200
ENDER_3_READ_TIMEOUT = 5


def _is_ender_3_port(port_info):
  return (port_info.hwid and ENDER_3_USB_HWID in port_info.hwid)


def _log_port_info(port_info):
  logger.debug('- Port: {0}'.format(port_info.device))
  for key, val in port_info.__dict__.items():
    if (key != 'device' and val and val != 'n/a'):
      logger.debug('\t- {0}: {1}'.format(key, val))


def _get_ender_3_port():
  for p in comports():
    _log_port_info(p)
    if _is_ender_3_port(p):
      return p.device
  raise RuntimeError('No Ender-3 serial port found')


class Ender3Serial(serial.Serial):

    def __init__(self):
        super().__init__()
        self.port = None
        self.baudrate = ENDER_3_BAUDRATE
        self.timeout = ENDER_3_READ_TIMEOUT # read timeout
        self.write_timeout = 1 # write timeout

    def connect_to_ender_3(self):
        self.port = _get_ender_3_port()
        self.open()
        logger.debug('Connected to: {0}'.format(self.port))
        self.reset_input_buffer() # clear input buffer

    def write_string(self, msg, delimiter='\r\n'):
        if delimiter:
            msg = '{0}{1}'.format(msg, delimiter)
        msg = msg.encode('utf-8')
        logger.debug('->{0}'.format(msg))
        self.write(msg)
        self.flush() # wait until all data is written

    def read_bytes(self, ack=None):
        if not ack:
            raise ValueError('\"ack=\"" must be set when reading lines')
        rsp = []
        self.reset_input_buffer() # clear input buffer
        while True:
            msg = self.readline()
            if not msg:
                raise RuntimeError('Did not get response from Ender-3')
            logger.debug('<-{0}'.format(msg))
            rsp.append(msg)
            if ack in msg:
                return rsp


if __name__ == '__main__':
    import sys

    logging.basicConfig(
        stream=sys.stdout, 
        filemode='w',
        format='%(levelname)s %(asctime)s - %(message)s', 
        level=logging.ERROR)
    logger.setLevel(logging.DEBUG)

    port = Ender3Serial()
    port.connect_to_ender_3()
    port.write_string('G28')
    port.read_bytes(ack=b'ok')
    port.close()
