
import serial
import smbus
import math
import time
import sqlite3
import pigpio

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
         elapsed_time = (point_datetime - self.mainWin.start_datetime).total_seconds()

         insert_query = ("INSERT INTO data("
            "id_round, datetime, elapsed_time, "
            "altitude, latitude, longitude, speed, bt_latitude, bt_longitude, bt_speed,"
            "rpm, gear, "
            "accel_angle_x, accel_angle_y, accel_angle_z, accel_gforce_x, accel_gforce_y, accel_gforce_z, "
            "gyros_x, gyros_y, gyros_z, gyros_temperature, "
            "compass, baro_temperature, baro_pressure) "
            "VALUES(%s, %.3f, %.3f, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
               current_round_id, point_datetime, elapsed_time,
               self.mainWin.altitude, self.mainWin.latitude, self.mainWin.longitude, self.mainWin.speed,
               self.mainWin.bt_latitude, self.mainWin.bt_longitude, self.mainWin.bt_speed,
               int(self.mainWin.rpm), int(self.mainWin.gear),
               self.mainWin.accel_angle_x, self.mainWin.accel_angle_y, self.mainWin.accel_angle_z,
               self.mainWin.accel_gforce_x, self.mainWin.accel_gforce_y, self.mainWin.accel_gforce_z,
               self.mainWin.gyros_x, self.mainWin.gyros_y, self.mainWin.gyros_z, self.mainWin.gyros_temperature,
               self.mainWin.compass, self.mainWin.baro_temperature, self.mainWin.baro_pressure))

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



class MultiWiiThread(QtCore.QThread):
    def __init__(self, MultiWiiSerial = '/dev/ttyMultiWii'):
        QtCore.QThread.__init__(self)
        self.stopped = 1
        self.MultiWiiSerial = MultiWiiSerial

    def run(self):
        self.stopped = 0

        self.serialMultiWii = serial.Serial(
            port = self.MultiWiiSerial,
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = None)

        while True:
            if self.stopped:
                self.serialMultiWii.close()
                break

        if self.serialMultiWii.inWaiting():
            str = self.serialMultiWii.readline()
            parts = str.replace("\n", "").split(", ")
            if len(parts) == 19:
                data = {
                    "altitude": parts[0],
                    "latitude": parts[1],
                    "longitude": parts[2],
                    "heading": parts[3],
                    "speed": parts[4],
                    "gforce_x": parts[5],
                    "gforce_y": parts[6],
                    "gforce_z": parts[7],
                    "xAngle": parts[8],
                    "yAngle": parts[9],
                    "zAngle": parts[10],
                    "hx": parts[11],
                    "hy": parts[12],
                    "hz": parts[13],
                    "temperature": parts[14],
                    "temp_bmp": parts[15],
                    "pressure": parts[16],
                    "rpm": parts[17],
                    "gear": parts[18]
                }
                self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )

    def setPort(self, port):
        self.MultiWiiSerial = port

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
