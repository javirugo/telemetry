#!/usr/bin/python

from datetime import datetime
import sqlite3 as lite

class Metrics:
  cur_idx = 0
  data = {}

  def __init__(self, data_filename):
    con = lite.connect(data_filename)
    with con:
      cur = con.cursor()
      cur.execute("SELECT datetime, latitude, longitude FROM data")
      rows = cur.fetchall()
      cur_lat = 0
      cur_lon = 0
      for row in rows:
        if row[0] == cur_lat and row[1] == cur_lon: continue
        self.data[self.cur_idx] = [datetime.fromtimestamp(row[0]), row[1], row[2]]
        self.cur_idx += 1
        cur_lat = row[0]
        cur_lon = row[1]

      self.cur_idx = 0


  def getMetrics(self):
    if self.cur_idx >= (len(self.data) -1):
      return False

    retval = self.data[self.cur_idx]
    self.cur_idx += 1
    return retval
