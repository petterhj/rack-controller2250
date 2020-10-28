# Imports
import time
import serial

from config import *
from gui import RackApp
from hardware import Hardware
from logger import logger


# logger.add('controller2250.log', retention='3 days')


# Class: RackClient
class RackClient(serial.Serial):
    # Init
    def __init__(self, *args, **kwargs):
        super(RackClient, self).__init__(**{
           'baudrate': SERIAL_BAUDRATE,
           'parity': serial.PARITY_NONE,
           'stopbits': serial.STOPBITS_ONE,
           'bytesize': serial.EIGHTBITS,
           'timeout': SERIAL_TIMEOUT
        })

        # Data
        self.sensor_data = None
        self.string_data = None
        self.string_delay = 5

        # Sensors
        self.hardware = Hardware()
        self.sensor_data = None


    # Open
    def open(self):
        attempts = 0

        while (attempts < SERIAL_ATTEMPTS):
            try:
                logger.info('Opening serial port %s' % (SERIAL_DEVICE))
                self.port = SERIAL_DEVICE
                super(RackClient, self).open()
            except:
                logger.exception('Could not open serial port %s' % (SERIAL_DEVICE))

            if self.is_open:
                break

            attempts += 1
            logger.warning('Awaiting new open attempt')
            time.sleep(3*attempts)


    # Process
    def process(self):
        if self.string_data:
            output = 'STR=%s' % (self.string_data[0:14])

            # Write
            if self.write(output):
                logger.warning('Delaying %d seconds' % (self.string_delay))
                time.sleep(self.string_delay)
                self.string_data = None
                self.string_delay = 5
                return True
            else:
                return False

        else:
            # Refresh sensor data
            try:
                logger.debug('Refreshing sensor data...')
                self.sensor_data = self.hardware.sensor_data()
            except:
                logger.exception('Could not get sensor data')
                return False
            else:
                output = 'VAL=%d,%d,%d,%d,' % (
                    self.sensor_data[0],
                    self.sensor_data[1],
                    self.sensor_data[2],
                    self.sensor_data[3],
                )

                # Write
                return self.write(output)


    # Write
    def write(self, data):
        logger.debug('Writing data: %s' % (data))

        try:
            # Encode and write data
            data = data + '\r\n'
            data = data.encode('ascii')
            
            super(RackClient, self).write(data)
            
            # Acknowledgement
            ack = self.readline().strip().decode('unicode-escape')

            if 'OK' in ack:
                logger.debug('Ack received ("%s")' % (ack))
                return True
            else:
                logger.error('Missing or incorrect response... ("%s")' % (ack))
                return False
            
        except:
            logger.exception('Could not write to serial')
            return False



# Main
if __name__ == "__main__":
    logger.info('Starting rack client')

    logger.info('> DEBUG: %r' % (DEBUG))
    logger.info('> APP_NAME: %r' % (APP_NAME))
    logger.info('> VERSION: %r' % (VERSION))
    logger.info('> SERIAL_DEVICE: %r' % (SERIAL_DEVICE))
    logger.info('> BASE_DIR: %r' % (BASE_DIR))

    serial = RackClient()
    app = RackApp(serial)
    # app.OnInit(serial)
    app.MainLoop()