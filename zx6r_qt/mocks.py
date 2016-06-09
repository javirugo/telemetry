
import time
import json
import random
from datetime import datetime
from PyQt4 import QtCore


class KDSThread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.currentRPM = 0
      self.currentGear = 0
      self.decreaseRPM = False
      self.decreaseGear = False

   def run(self):
      self.stopped = 0
      self.currentRPM = 0
      self.currentGear = 0

      while True:
         if self.stopped:
            break

         if self.decreaseRPM:
            self.currentRPM -= 100
            if self.currentRPM < 200: self.decreaseRPM = False
         else:
            self.currentRPM += 100
            if self.currentRPM > 15800: self.decreaseRPM = True

         if self.decreaseGear:
            self.currentGear -= 0.1
            if self.currentGear < 1: self.decreaseGear = False

         else:
            self.currentGear += 0.1
            if self.currentGear > 6: self.decreaseGear = True
         
         data = {"rpm": self.currentRPM, "gear": int(self.currentGear)}
         self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )

         time.sleep(0.1)

   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0



class GPSThread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.currentIndex = 0
      trackfile = "../tracks/ALMERIA.json"
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

         time.sleep(random.uniform(0.001, 0.060))

   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0


class I2CThread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.lean_x = 0
      self.gforce_y = 0
      self.decreaseLean = False
      self.decreaseGForce = False

   def run(self):
      self.stopped = 0

      lean = 0
      gforce = 0

      while True:
         if self.stopped:
            break

         if self.decreaseLean:
            self.lean_x -= 1
            if self.lean_x == -90: self.decreaseLean = False
         else:
            self.lean_x += 1
            if self.lean_x == 90: self.decreaseLean = True

         if self.decreaseGForce:
            self.gforce_y -= 2
            if self.gforce_y > 100: self.decreaseGForce = False
         else:
            self.gforce_y += 2
            if self.gforce_y < 10: self.decreaseGForce = True

         data = {
            "lean_x": self.lean_x,
            "lean_y": 5,
            "lean_z": 6,
            "gforce_x": 8,
            "gforce_y": self.gforce_y,
            "gforce_z": 9,
            "compass": 12
         }

         self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )
         time.sleep(0.1)

   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0

