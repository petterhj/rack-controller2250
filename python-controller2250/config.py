import os, sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.abspath(os.path.dirname(__file__))

DEBUG                           = False
APP_NAME                        = 'RackController'
VERSION                         = '1.0-beta1'
SERIAL_DEVICE                   = 'COM4'
SERIAL_BAUDRATE                 = 115200
SERIAL_ATTEMPTS                 = 3
SERIAL_TIMEOUT                  = 5
REFRESH_RATE                    = 1500	# milliseconds
BASE_DIR                        = application_path
DIST_FILE_NAME                  = 'controller2250-%s' % (VERSION)