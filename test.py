import atexit
import logging
import sys
import time

import serial
from serial.tools.list_ports import comports


logging.basicConfig(
    # filename='logfile.log',
    stream=sys.stdout, 
    filemode='w',
    format='%(levelname)s %(asctime)s - %(message)s', 
    level=logging.DEBUG)

logger = logging.getLogger('opentrons.ender_3.test')


# SERIAL PORT
ENDER_3_USB_HWID = '1A86:7523'
ENDER_3_BAUDRATE = 115200
ENDER_3_READ_TIMEOUT = 5
ENDER_3_ACK = 'ok'
ENDER_3_BUSY_MSG = 'echo:busy: processing'


def _serial_is_ender_3_port(port_info):
  return (port_info.hwid and ENDER_3_USB_HWID in port_info.hwid)


def _serial_log_port_info(port_info):
  logger.debug('- Port: {0}'.format(port_info.device))
  for key, val in port_info.__dict__.items():
    if (key != 'device' and val and val != 'n/a'):
      logger.debug('\t- {0}: {1}'.format(key, val))


def _serial_get_ender_3_port():
  found_ports = []
  for p in comports():
    _serial_log_port_info(p)
    if _serial_is_ender_3_port(p):
      found_ports.append(p)
  logger.debug('Found {0} ports'.format(len(found_ports)))
  return found_ports


def _serial_connect_to_ender_3():
    found_ports = _serial_get_ender_3_port()
    for p in found_ports:
        logger.debug(p)
        port = serial.Serial()
        port.port = p.device
        port.baudrate = ENDER_3_BAUDRATE
        port.timeout = ENDER_3_READ_TIMEOUT # read timeout
        port.write_timeout = 1 # write timeout
        port.open()
        port.reset_input_buffer() # clear input buffer
        atexit.register(port.close)
        return port


def _serial_write_string(port, msg, delimiter='\r\n'):
    if delimiter:
        msg = '{0}{1}'.format(msg, delimiter)
    msg = msg.encode('utf-8')
    logger.debug('->{0}'.format(msg))
    port.write(msg)
    port.flush() # wait until all data is written


def _serial_read_strings(port, ack=ENDER_3_ACK):
    rsp = []
    port.reset_input_buffer() # clear input buffer
    while True:
        msg = port.readline()
        if not msg:
            raise RuntimeError('Did not get response from Ender-3')
        msg = msg.decode('utf-8').strip()
        if ENDER_3_BUSY_MSG in msg:
            break
        if ack in msg:
            return rsp
        logger.debug('<-{0}'.format(msg))
        rsp.append(msg)


if __name__ == '__main__':
    port = _serial_connect_to_ender_3()
    _serial_write_string(port, 'G28Y')
    _serial_read_strings(port)
