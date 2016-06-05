import serial
import time
import sys
from datetime import datetime

ser = serial.Serial(
    port='/dev/ttyAMA0',\
    baudrate=57600,\
#    baudrate=19200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=None)

while True:
    c = ser.read()
    sys.stdout.write(c)
    if c == "\n": sys.stdout.write("%s, " % datetime.now())

