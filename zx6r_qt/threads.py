
import serial
import smbus
import math
import time
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
         port='/dev/ttyUSB0',
         baudrate=19200,
         parity=serial.PARITY_NONE,
         stopbits=serial.STOPBITS_ONE,
         bytesize=serial.EIGHTBITS,
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


class MPU6050Thread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.bus = smbus.SMBus(1)
      self.MUP6050_address = 0x68


   def read_byte(self, adr):
       return bus.read_byte_data(self.MUP6050_address, adr)

   def read_word(self, adr):
       high = self.bus.read_byte_data(self.MUP6050_address, adr)
       low = self.bus.read_byte_data(self.MUP6050_address, adr+1)
       val = (high << 8) + low
       return val

   def read_word_2c(self, adr):
       val = self.read_word(adr)
       if (val >= 0x8000):
           return -((65535 - val) + 1)
       else:
           return val


   def run(self):
      self.bus.write_byte_data(self.MUP6050_address, 0x6b, 0)
      self.stopped = 0

      lean = 0
      gforce = 0

      while True:
         if self.stopped:
            break

         try:
            gyro_xout = self.read_word_2c(0x43)
            gyro_yout = self.read_word_2c(0x45)
            gyro_zout = self.read_word_2c(0x47)

            accel_xout = self.read_word_2c(0x3b)
            accel_yout = self.read_word_2c(0x3d)
            accel_zout = self.read_word_2c(0x3f)

            data = {
               "lean": accel_yout,
               "gforce": gyro_xout
            }

            self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )
            time.sleep(0.05)
         except Exception, e:
            time.sleep(0.1)
            pass
            
   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0


