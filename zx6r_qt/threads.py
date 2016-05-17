
import serial
import smbus
import math
import time
import sqlite3
from datetime import datetime
from gps import *
from PyQt4 import QtCore

from laptimer import Laptimer


class DataRecordThread(QtCore.QThread):
   def __init__(self, mainwin):
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.mainWin = mainwin
      self.laptimer = Laptimer("/home/jaruiz/telemetry/tracks/ALMERIA.json")
      self.last_lap_id = 0
      self.last_sector_id = 0

      self.fastest_lap_time = 0
      self.last_lap_time = 0
      self.lap_start_time = 0

   def run(self):
      self.stopped = 0

      self.db = sqlite3.connect('data.db')
      cur = self.db.cursor()

      cur.execute("INSERT INTO round(start, video) values(%s, %s)" % (
         round((self.mainWin.start_datetime - datetime(1970, 1, 1)).total_seconds()),
         round(self.mainWin.start_datetime)))

      current_round_id = cur.lastrowid

      while True:
         print "pass"
         point_datetime_obj = datetime.utcnow()
         point_datetime = (point_datetime_obj - datetime(1970, 1, 1)).total_seconds()
         insert_query = ("INSERT INTO data(id_round, datetime, latitude, longitude, speed, "
            "rpm, gear, lean_x, lean_y, lean_z, gforce_x, gforce_y, gforce_z, compass) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
               current_round_id, point_datetime,
               self.mainWin.latitude, self.mainWin.longitude, self.mainWin.speed,
               int(self.mainWin.rpm), int(self.mainWin.gear),
               self.mainWin.lean_x, self.mainWin.lean_y, self.mainWin.lean_z,
               self.mainWin.gforce_x, self.mainWin.gforce_y, self.mainWin.gforce_z,
               self.mainWin.compass))

         cur.execute(insert_query)

         checkpoint = self.laptimer.check(self.mainWin.latitude, self.mainWin.longitude)
         if checkpoint:
         
            # Set ending time of last sector
            if self.last_sector_id:
               cur.execute("UPDATE sector SET end=%s WHERE id=%s" %(
                  point_datetime,
                  self.last_sector_id))
         
            if checkpoint == self.laptimer.CHECKPOINT_START:
               if self.last_lap_id:
                  cur.execute("UPDATE lap SET end=%s WHERE id=%s" %(
                     point_datetime,
                     self.last_lap_id))

                  # Calculate "last lap time"
                  if self.lap_start_time:
                     self.last_lap_time = point_datetime - point_datetime_obj
                     if self.last_lap_time < self.fastest_lap_time:
                        self.fastest_lap_time = self.last_lap_time

                     self.emit(QtCore.SIGNAL('update(PyQt_PyObject)'), {
                        "last": self.last_lap_time,
                        "best": self.fastest_lap_time})

                  self.lap_start_time = point_datetime
               
               cur.execute("INSERT INTO lap(id_round, start) VALUES(%s, %s)" %(
                  current_round_id, point_datetime))

               self.last_lap_id = cur.lastrowid

            cur.execute("INSERT INTO sector(id_lap, start) VALUES(%s, %s)" %(
               self.last_lap_id, point_datetime))

            self.last_sector_id = cur.lastrowid


         if self.stopped:
            cur.execute("UPDATE round SET end=%s" % point_datetime)
            self.db.commit()
            self.db.close()
            break

         self.db.commit()
         time.sleep(0.05)


   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0



class KDSThread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1

   def run(self):
      self.stopped = 0

      rpm = 0

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
            if len(parts) == 2:
               data = {"rpm": parts[0], "gear": parts[1]}
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


class I2CThread(QtCore.QThread):
   def __init__(self):
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.bus = smbus.SMBus(1)
      self.MUP6050_address = 0x68
      self.HMC5883L_address = 0x1e
      self.HMC5883L_scale = 0.92

   def read_word(self, i2c_dev, adr):
      high = self.bus.read_byte_data(i2c_dev, adr)
      low = self.bus.read_byte_data(i2c_dev, adr+1)
      val = (high << 8) + low
      return val

   def read_word_2c(self, i2c_dev, adr):
      val = self.read_word(i2c_dev, adr)
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
            compass_x_out = self.read_word_2c(self.HMC5883L_address, 3) * self.HMC5883L_scale
            compass_y_out = self.read_word_2c(self.HMC5883L_address, 7) * self.HMC5883L_scale
            compass_z_out = self.read_word_2c(self.HMC5883L_address, 5) * self.HMC5883L_scale

            bearing  = math.atan2(compass_y_out, compass_x_out)
            if (bearing < 0):
                bearing += 2 * math.pi


            gyro_yout = self.read_word_2c(self.MUP6050_address, 0x45)
            gyro_zout = self.read_word_2c(self.MUP6050_address, 0x47)
            accel_xout = self.read_word_2c(self.MUP6050_address, 0x3b)
            accel_zout = self.read_word_2c(self.MUP6050_address, 0x3f)

            gyro_xout = self.read_word_2c(self.MUP6050_address, 0x43)
            accel_yout = self.read_word_2c(self.MUP6050_address, 0x3d)

            data = {
               "lean_x": accel_yout,
               "lean_y": accel_xout,
               "lean_z": accel_zout,
               "gforce_x": gyro_yout,
               "gforce_y": gyro_xout,
               "gforce_z": gyro_zout,
               "compass": math.degrees(bearing)
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

