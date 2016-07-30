
import time
import os
import json
import random
from datetime import datetime
from PyQt4 import QtCore


class GPSThread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.currentIndex = 0
      trackfile = "%s/../tracks/JEREZ.json" % os.path.dirname(os.path.abspath(__file__))
      with open(trackfile) as track_file:
         track_data = json.load(track_file)
         self.gpsdata = track_data["MOCK"]
         track_file.close()

   def run(self):
      self.stopped = 0

      while True:
         if self.stopped:
            break

         longitude = self.gpsdata[self.currentIndex][0]
         latitude = self.gpsdata[self.currentIndex][1]
         data = {"latitude": latitude, "longitude": longitude, "speed": 100}
         self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )
         self.currentIndex += 1
         if self.currentIndex >= len(self.gpsdata):
            self.currentIndex = 0

         time.sleep(random.uniform(0.05, 0.10))

   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0



class MultiWiiThread(QtCore.QThread):
   def __init__(self, MultiWiiSerial = '/dev/ttyMultiWii'):
      QtCore.QThread.__init__(self)
      self.stopped = 1

   def run(self):
      self.stopped = 0

      while True:
         if self.stopped:
            break

         data = {
            "altitude": 0,
            "latitude": 0,
            "longitude": 0,
            "heading": 0,
            "speed": 0,
            "gforce_x": 0,
            "gforce_y": 0,
            "gforce_z": 0,
            "xAngle": 0,
            "yAngle": 0,
            "zAngle": 0,
            "hx": 0,
            "hy": 0,
            "hz": 0,
            "temperature": 0,
            "temp_bmp": 100,
            "pressure": 1000,
            "rpm": 0,
            "gear": 0
         }

         self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )
         time.sleep(random.uniform(0.001, 0.060))

   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0



