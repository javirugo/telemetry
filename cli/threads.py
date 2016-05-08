
import threading
import serial
import RPi.GPIO as GPIO
from gps import *

class LedBlink(threading.Thread):
   def __init__(self, threadID, name, pin):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.pin = pin
      self.interval = 0.2
      self.running = True


   def run(self):
      self.pin_high = False
      while self.running:
         if self.pin_high:
            GPIO.output(self.pin, GPIO.LOW)
            self.pin_high = False
         else:
            GPIO.output(self.pin, GPIO.HIGH)
            self.pin_high = True

         time.sleep(self.interval)


class GpsThread(threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.gpsd = gps(mode=WATCH_ENABLE)
      self.current_value = None
      self.running = True
      self.latitude = 0
      self.longitude = 0
      self.speed = 0
      self.compass = 0
      self.datetime = 0

   def run(self):
      while self.running:
         self.gpsd.next()
         self.latitude = self.gpsd.fix.latitude
         self.longitude = self.gpsd.fix.longitude
         self.speed = self.gpsd.fix.speed


class KDSThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
      self.rpm = 0
      self.kph = 0
      self.lean = 0
      self.gforce = 0
      self.running = True

      self.serialKDS = serial.Serial(
         port='/dev/ttyUSB0',\
         baudrate=19200,\
         parity=serial.PARITY_NONE,\
         stopbits=serial.STOPBITS_ONE,\
         bytesize=serial.EIGHTBITS,\
         timeout=None)

      self.getData()

   def getData(self):
      while self.running:
         str = self.serialKDS.readline()
         parts = str.replace("\n", "").split(", ")
         if len(parts) == 4:
            [self.rpm, self.kph, self.lean, self.gforce] = parts

