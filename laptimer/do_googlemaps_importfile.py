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
      cur.execute("SELECT latitude, longitude, speed FROM data")
      rows = cur.fetchall()
      cur_lat = 0
      cur_lon = 0
      number = 0
      for row in rows:
        if row[0] == cur_lat and row[1] == cur_lon: continue
        if number == 3:
          print "%s, %s, %s" % (row[0], row[1], row[2])
          cur_lat = row[0]
          cur_lon = row[1]
          number = 0
        else:
          number += 1

metrics = Metrics("data_almeria_16jun.db")
