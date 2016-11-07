import os
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
      self.laptimer = Laptimer("%s/../tracks/%s.json" % (os.path.dirname(os.path.abspath(__file__)), self.mainWin.TRACK))
      self.last_lap_id = 0
      self.last_sector_idlap = 0
      self.last_sector_start = 0

      self.fastest_lap_time = 0
      self.last_lap_time = 0
      self.lap_start_time = 0

   def run(self):
      self.stopped = 0
      self.last_lap_id = 0
      self.last_sector_idlap = 0
      self.last_sector_start = 0
      self.lap_start_time = 0

      self.db = sqlite3.connect('%s/data.db' % os.path.dirname(os.path.abspath(__file__)))
      cur = self.db.cursor()

      cur.execute("INSERT INTO round(start, video) values(%s, %s)" % (
         (self.mainWin.start_datetime - datetime(1970, 1, 1)).total_seconds(),
         int((self.mainWin.start_datetime - datetime(1970, 1, 1)).total_seconds())))

      current_round_id = cur.lastrowid

      while True:
         point_datetime_obj = datetime.utcnow()
         point_datetime = (point_datetime_obj - datetime(1970, 1, 1)).total_seconds()
         elapsed_time = (point_datetime_obj - self.mainWin.start_datetime).total_seconds()

         insert_query = ("INSERT INTO data("
            "id_round, id_lap, datetime, elapsed_time, "
            "altitude, latitude, longitude, speed, "
            "rpm, gear, "
            "accel_angle_x, accel_angle_y, accel_angle_z, accel_gforce_x, accel_gforce_y, accel_gforce_z, "
            "gyros_x, gyros_y, gyros_z) "
            "VALUES("
               "%s, %s, %.3f, %.3f, "
               "%s, %s, %s, %s, "
               "%s, %s, "
               "%s, %s, %s, "
               "%s, %s, %s, "
               "%s, %s, %s)" % (
               current_round_id, self.last_lap_id, point_datetime, elapsed_time,
               self.mainWin.altitude, self.mainWin.latitude, self.mainWin.longitude, self.mainWin.speed,
               int(self.mainWin.rpm), int(self.mainWin.gear),
               self.mainWin.accel_angle_x, self.mainWin.accel_angle_y, self.mainWin.accel_angle_z,
               self.mainWin.accel_gforce_x, self.mainWin.accel_gforce_y, self.mainWin.accel_gforce_z,
               self.mainWin.gyros_x, self.mainWin.gyros_y, self.mainWin.gyros_z,))

         cur.execute(insert_query)

         checkpoint = self.laptimer.check(self.mainWin.latitude, self.mainWin.longitude)
         if checkpoint:

            if (point_datetime - float(self.last_sector_start)) < 10: continue

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

   def loadHistory(self):
      self.db = sqlite3.connect('%s/data.db' % os.path.dirname(os.path.abspath(__file__)))
      cur = self.db.execute("SELECT start, end FROM lap ORDER BY lap.start")

      all_laps = cur.fetchall()
      for lap in all_laps:
         if lap[0] and lap[1]:
            self.last_lap_time = datetime.fromtimestamp(lap[1]) - datetime.fromtimestamp(lap[0])
            if self.fastest_lap_time == 0 or self.last_lap_time < self.fastest_lap_time:
               self.fastest_lap_time = self.last_lap_time

            self.emit(QtCore.SIGNAL('update(PyQt_PyObject)'), {
               "last": self.last_lap_time,
               "best": self.fastest_lap_time})

      self.db.close()


   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0



class MultiWiiThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.stopped = 1
        self.serialMultiWii = False
        self.MultiWiiSerial = "/dev/ttyMultiWii"

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

            try:
                str = self.serialMultiWii.readline()
                parts = str.replace("\n", "").split(", ")
                if len(parts) == 11:
                   data = {
                       "rpm": parts[0],
                       "gear": parts[1],
                       "gforce_x": parts[2],
                       "gforce_y": parts[3],
                       "gforce_z": parts[4],
                       "xAngle": parts[5],
                       "yAngle": parts[6],
                       "zAngle": parts[7],
                       "hx": parts[8],
                       "hy": parts[9],
                       "hz": parts[10]
                   }

                   self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )
            except Exception, e:
                print e
                pass

    def setPort(self, port):
        self.MultiWiiSerial = port

    def stop(self):
        self.stopped = 1

    def isRunning(self):
        return self.stopped == 0


class GPSThread(QtCore.QThread):
   def __init__(self, device):
      QtCore.QThread.__init__(self)
      self.stopped = 1
      self.device = device

      os.popen("sudo systemctl stop gpsd")
      time.sleep(2)
      ser = serial.Serial(self.device, self.get_baudrate())

      # CFG-RATE (60 millis)
      cmd_rate = b'\xB5\x62\x06\x08\x06\x00\x3C\x00\x01\x00\x01\x00\x52\x22'
      ser.write(cmd_rate)

      # CFG-PRT (UART-1 115200)
      cmd_prt = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x00\xC2\x01\x00\x07\x00\x03\x00\x00\x00\x00\x00\xC0\x7E'
      ser.write(cmd_prt)
      ser.close()

      os.popen("sudo systemctl restart gpsd")

      

   def get_baudrate(self):
      baudrate = 9600
      command = "stty < %s | grep speed | awk '{print $2}'" % self.device
      baudrate_str = os.popen(command).read().rstrip()
      if baudrate_str != "":
         baudrate = int(baudrate_str)

      return baudrate


   def run(self):
      self.gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
      self.stopped = 0

      latitude = 0
      longitude = 0
      speed = 0

      while True:
         if self.stopped:
            break

         self.gpsd.next()
         data = {
            "altitude": self.gpsd.fix.altitude,
            "latitude": self.gpsd.fix.latitude,
            "longitude": self.gpsd.fix.longitude,
            "speed": self.gpsd.fix.speed
         }

         self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), data )

   def stop(self):
      self.stopped = 1

   def isRunning(self):
      return self.stopped == 0
