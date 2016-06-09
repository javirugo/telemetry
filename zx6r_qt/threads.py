
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
      self.laptimer = Laptimer("../tracks/ALMERIA.json")
      self.last_lap_id = 0
      self.last_sector_idlap = 0
      self.last_sector_start = 0

      self.fastest_lap_time = 0
      self.last_lap_time = 0
      self.lap_start_time = 0
      
      self.db = sqlite3.connect('data.db')
      cur = self.db.execute("SELECT start, end FROM lap ORDER BY lap.start")
      all_laps = cur.fetchall()
      self.last_lap_time, self.fastest_lap_time = self.laptimer.loadHistory(all_laps)

      self.emit(QtCore.SIGNAL('update(PyQt_PyObject)'), {
         "last": self.last_lap_time,
         "best": self.fastest_lap_time})

      self.db.close()


   def run(self):
      self.stopped = 0
      self.last_lap_id = 0
      self.last_sector_idlap = 0
      self.last_sector_start = 0
      self.lap_start_time = 0

      self.db = sqlite3.connect('data.db')
      cur = self.db.cursor()

      cur.execute("INSERT INTO round(start, video) values(%s, %s)" % (
         (self.mainWin.start_datetime - datetime(1970, 1, 1)).total_seconds(),
         int((self.mainWin.start_datetime - datetime(1970, 1, 1)).total_seconds())))

      current_round_id = cur.lastrowid

      while True:
         point_datetime_obj = datetime.utcnow()
         point_datetime = (point_datetime_obj - datetime(1970, 1, 1)).total_seconds()

         insert_query = ("INSERT INTO data(id_round, datetime, latitude, longitude, speed, "
            "rpm, kph, gear, lean_x, lean_y, lean_z, gforce_x, gforce_y, gforce_z, compass) "
            "VALUES(%s, %.3f, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
               current_round_id, point_datetime,
               self.mainWin.latitude, self.mainWin.longitude, self.mainWin.speed,
               int(self.mainWin.rpm), int(self.mainWin.kph), int(self.mainWin.gear),
               self.mainWin.lean_x, self.mainWin.lean_y, self.mainWin.lean_z,
               self.mainWin.gforce_x, self.mainWin.gforce_y, self.mainWin.gforce_z,
               self.mainWin.compass))

         cur.execute(insert_query)

         checkpoint = self.laptimer.check(self.mainWin.latitude, self.mainWin.longitude)
         if checkpoint:
         
            # Set ending time of last sector
            if self.last_lap_id:
               cur.execute("UPDATE sector SET end=%.3f WHERE id_lap=%s and start=%s" %(
                  point_datetime,
                  self.last_lap_id,
                  self.last_sector_start))
         
            if checkpoint == self.laptimer.CHECKPOINT_START:
               if self.last_lap_id:
                  cur.execute("UPDATE lap SET end=%.3f WHERE id=%s" %(
                     point_datetime,
                     self.last_lap_id))

               # Calculate "last lap time"
               if self.lap_start_time:
                  self.last_lap_time = point_datetime_obj - self.lap_start_time

                  if self.fastest_lap_time == 0 or self.last_lap_time < self.fastest_lap_time:
                     self.fastest_lap_time = self.last_lap_time

                  self.emit(QtCore.SIGNAL('update(PyQt_PyObject)'), {
                     "last": self.last_lap_time,
                     "best": self.fastest_lap_time})

               self.lap_start_time = point_datetime_obj

               cur.execute("INSERT INTO lap(id_round, start) VALUES(%s, %.3f)" %(
                  current_round_id, point_datetime))

               self.last_lap_id = cur.lastrowid

            if self.last_lap_id:
               cur.execute("INSERT INTO sector(id_lap, start) VALUES(%s, %.3f)" %(
                  self.last_lap_id, point_datetime))

            self.last_sector_start = "%.3f" % point_datetime


         if self.stopped:
            cur.execute("UPDATE round SET end=%s" % point_datetime)
            self.db.commit()
            self.db.close()
            break

         self.db.commit()
         time.sleep(0.04)


   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0




class KDSThread(QtCore.QThread):
   def __init__(self, KDSSerial = 18):
      import pigpio
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.KDSSerial = KDSSerial

   def run(self):
      self.stopped = 0
      self.serialKDS = pigpio.pi()
      self.serialKDS.set_mode(self.KDSSerial, pigpio.INPUT)
      self.serialKDS.bb_serial_read_open(self.KDSSerial, 19200, 8)

      while True:
         if self.stopped:
            self.serialKDS.bb_serial_read_close(self.KDSSerial)
            self.serialKDS.stop()
            break

         (count, str) = self.serialKDS.bb_serial_read(self.KDSSerial)
         if count:
            parts = str.replace("\n", "").split(", ")
            if len(parts) == 3:
               data = {"rpm": parts[0], "kph": parts[1], "gear": parts[2]}
               self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )

         time.sleep(0.05)

   def setPort(self, port):
      self.KDSSerial = port

   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0


'''
      class KDSThread(QtCore.QThread):
         def __init__(self, KDSSerial = '/dev/ttyKDS'):
            QtCore.QThread.__init__(self)
            self.stopped = 1
            self.KDSSerial = KDSSerial

         def run(self):
            self.stopped = 0

            self.serialKDS = serial.Serial(
               port=self.KDSSerial,
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
                  if len(parts) == 3:
                     data = {"rpm": parts[0], "kph": parts[1], "gear": parts[2]}
                     self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )

         def setPort(self, port):
            self.KDSSerial = port

         def stop(self):
            self.stopped = 1

         def isRunning(self):
            return self.stopped == 0
'''


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
      self.gyro_scale = 131.0
      self.accel_scale = 16384.0

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

   def read_all(self):
      raw_gyro_data = self.bus.read_i2c_block_data(self.MUP6050_address, 0x43, 6)
      raw_accel_data = self.bus.read_i2c_block_data(self.MUP6050_address, 0x3b, 6)

      gyro_scaled_x = self.twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale
      gyro_scaled_y = self.twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale
      gyro_scaled_z = self.twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale

      accel_scaled_x = self.twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / self.accel_scale
      accel_scaled_y = self.twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / self.accel_scale
      accel_scaled_z = self.twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / self.accel_scale

      return(gyro_scaled_x,gyro_scaled_y,gyro_scaled_z,accel_scaled_x,accel_scaled_y,accel_scaled_z)

   def twos_compliment(self, val):
      if (val >= 0x8000):
         return -((65535 - val) + 1)
      else:
         return val

   def get_y_rotation(self, x,y,z):
      radians = math.atan2(x, self.dist(y,z))
      return -math.degrees(radians)

   def get_x_rotation(self, x,y,z):
      radians = math.atan2(y, self.dist(x,z))
      return math.degrees(radians)

   def dist(self, a, b):
      return math.sqrt((a * a) + (b * b))


   def run(self):
      self.bus.write_byte_data(self.MUP6050_address, 0x6b, 0) # wake up mpu6050
      self.bus.write_byte_data(self.MUP6050_address, 0x1A, 0x06) # set DLPF to 6 (5Hz)

      self.time_diff = 0.01
      (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.read_all()

      last_x = self.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
      last_y = self.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

      self.gyro_offset_x = gyro_scaled_x
      self.gyro_offset_y = gyro_scaled_y

      self.gyro_total_x = (last_x) - self.gyro_offset_x
      self.gyro_total_y = (last_y) - self.gyro_offset_y

      self.bus.write_byte_data(self.HMC5883L_address, 0, 0b01110000)
      self.bus.write_byte_data(self.HMC5883L_address, 1, 0b00100000)
      self.bus.write_byte_data(self.HMC5883L_address, 2, 0b00000000)
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

            time.sleep(self.time_diff - 0.005)
            (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.read_all()

            gyro_scaled_x -= self.gyro_offset_x
            gyro_scaled_y -= self.gyro_offset_y

            gyro_x_delta = (gyro_scaled_x * self.time_diff)
            gyro_y_delta = (gyro_scaled_y * self.time_diff)

            self.gyro_total_x += gyro_x_delta
            self.gyro_total_y += gyro_y_delta

            rotation_x = self.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
            rotation_y = self.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

            data = {
               "lean_x": round(rotation_x, 2),
               "lean_y": round(rotation_y, 2),
               "lean_z": 0,
               "gforce_x": round(accel_scaled_x, 2),
               "gforce_y": round(accel_scaled_y, 2),
               "gforce_z": 0,
               "compass": math.degrees(bearing)
            }

            self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )
            #time.sleep(0.05)
         except IOError:
            time.sleep(0.01)
            pass

   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0

