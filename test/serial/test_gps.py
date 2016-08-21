import serial
import time
import sys
from datetime import datetime

ser = serial.Serial(
    port='/dev/ttyGPS',\
#    baudrate=9600,\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=None)

while True:
    c = ser.read()
    sys.stdout.write(c)
    if c == "\n": sys.stdout.write("%s, " % datetime.now())

