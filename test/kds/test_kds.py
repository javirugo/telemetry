#!/usr/bin/python

import pigpio
import time

serialKDS = pigpio.pi()
serialKDS.set_mode(18, pigpio.INPUT)
try: serialKDS.bb_serial_read_open(18, 19200, 8)
except: pass

while True:
	(count, str) = serialKDS.bb_serial_read(18)
	if str != "": print str
	time.sleep(0.1)
