
import serial
from gps import *
from PyQt4 import QtCore

class KDSThread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1

   def run(self):
      self.stopped = 0

      rpm = 0
      kph = 0
      lean = 0
      gforce = 0

      self.serialKDS = serial.Serial(
         port='/dev/ttyUSB0',\
         baudrate=19200,\
         parity=serial.PARITY_NONE,\
         stopbits=serial.STOPBITS_ONE,\
         bytesize=serial.EIGHTBITS,\
         timeout=None)

      while True:
         if self.stopped:
            self.serialKDS.close()
            break

         if self.serialKDS.inWaiting():
            str = self.serialKDS.readline()
            parts = str.replace("\n", "").split(", ")
            if len(parts) == 4:
               data = {"rpm": parts[0], "kph": parts[1], "lean": parts[2], "gforce": parts[3]}
               self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )

   def stop(self):
      self.stopped = 1


   def isRunning(self):
      return self.stopped == 0


class GPSThread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1

   def run(self):
      self.gpsd = gps(mode=WATCH_ENABLE)
      self.stopped = 0

      latitude = 0
      longitude = 0
      speed = 0

      while True:
         if self.stopped:
            break

         self.gpsd.next()
         data = {
            "latitude": self.gpsd.fix.latitude,
            "longitude": self.gpsd.fix.longitude,
            "speed": self.gpsd.fix.speed
         }

         self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )


   def stop(self):
      self.stopped = 1


   def isRunning(self):
      return self.stopped == 0


