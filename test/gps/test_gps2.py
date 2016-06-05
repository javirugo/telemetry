import serial
import pynmea2
from datetime import datetime

def parseGPS(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)

        print "Datetime: %s Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (
		datetime.now(),
		msg.timestamp,
		msg.lat,
		msg.lat_dir,
		msg.lon,
		msg.lon_dir,
		msg.altitude,
		msg.altitude_units)

serialPort = serial.Serial("/dev/ttyS0", 57600, timeout=None)

while True:
    str = serialPort.readline()
    parseGPS(str)
