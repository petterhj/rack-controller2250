import time
import struct
import serial
import random
from config import *
from datetime import datetime

last_refresh = datetime.now()
last_string = datetime.now()

ser = serial.Serial(**{
   # 'port': SERIAL_DEVICE,
   'baudrate': SERIAL_BAUDRATE,
   'parity': serial.PARITY_NONE,
   'stopbits': serial.STOPBITS_ONE,
   'bytesize': serial.EIGHTBITS,
   'timeout': SERIAL_TIMEOUT
})

ser.port = SERIAL_DEVICE
ser.open()

while True:
    if (datetime.now() - last_refresh).seconds > 3:
        # print('='*10, 'WRITING VALUES', '='*10)
        # ser.write(struct.pack('@B', 1))
        # ser.write(struct.pack('@BBBB', *(
        #     4,
        #     6,
        #     8,
        #     10,
        # )))
        t = random.randint(0, 2)
        
        if (t == 1):
            ser.write('VAL=4,6,8,10,\r\n'.encode('ascii'))
        elif (t == 2):
            ser.write('STR=FOOBAR|\r\n'.encode('ascii'))
        else:
            pass
        last_refresh = datetime.now()

    # if (datetime.now() - last_string).seconds > 10:
    #     print('='*10, 'WRITING STRING', '='*10)
    #     # ser.write(struct.pack('@B', 2))
    #     ser.write('STR|BAR|\r\n'.encode('ascii'))
    #     last_string = datetime.now()

    inp = ser.readline().strip()
    if inp:
        print(inp)

    time.sleep(0.1)


ser.close()