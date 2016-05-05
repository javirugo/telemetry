#!/usr/bin/python

from mock_metrics import Metrics

import json
import time
from datetime import datetime
from shapely.geometry import Polygon, Point

with open('ALMERIA.json') as track_file:
    track_data = json.load(track_file)

START_POLY = Polygon([
    (track_data["START"]["lat1"], track_data["START"]["lon1"]),
    (track_data["START"]["lat2"], track_data["START"]["lon2"]),
    (track_data["START"]["lat3"], track_data["START"]["lon3"]),
    (track_data["START"]["lat4"], track_data["START"]["lon4"])
])

SECTOR2_POLY = Polygon([
    (track_data["SECTOR2"]["lat1"], track_data["SECTOR2"]["lon1"]),
    (track_data["SECTOR2"]["lat2"], track_data["SECTOR2"]["lon2"]),
    (track_data["SECTOR2"]["lat3"], track_data["SECTOR2"]["lon3"]),
    (track_data["SECTOR2"]["lat4"], track_data["SECTOR2"]["lon4"])
])

SECTOR3_POLY = Polygon([
    (track_data["SECTOR3"]["lat1"], track_data["SECTOR3"]["lon1"]),
    (track_data["SECTOR3"]["lat2"], track_data["SECTOR3"]["lon2"]),
    (track_data["SECTOR3"]["lat3"], track_data["SECTOR3"]["lon3"]),
    (track_data["SECTOR3"]["lat4"], track_data["SECTOR3"]["lon4"])
])

metricsSource = Metrics()
metricsSource.setMockData(track_data["MOCK"])

current_sector = 0
current_lap = 0
inside_poly = False

LAPS = [{ "started": False, "ended": False,
	  "sectors": [
	    {"started": False, "ended": False},
	    {"started": False, "ended": False},
	    {"started": False, "ended": False} ]}]
while True:
    cur_ts, cur_lat, cur_lon = metricsSource.getMetrics()
    current_point = Point(cur_lat, cur_lon)

    if current_point.within(START_POLY):
        if inside_poly:
            continue
        else:
            inside_poly = True
            LAPS[current_lap]["ended"] = cur_ts
            LAPS[current_lap]["sectors"][2]["ended"] = cur_ts

            current_lap += 1
	    LAPS.append({ "started": False, "ended": False,
		      "sectors": [
			{"started": False, "ended": False},
			{"started": False, "ended": False},
			{"started": False, "ended": False} ]})

            LAPS[current_lap]["started"] = cur_ts
            LAPS[current_lap]["sectors"][0] = {"started": cur_ts, "ended": False}
            LAPS[current_lap]["sectors"][1] = {"started": False, "ended": False}
            LAPS[current_lap]["sectors"][2] = {"started": False, "ended": False}

    elif current_point.within(SECTOR2_POLY):
        if inside_poly:
            continue
        else:
            inside_poly = True

            LAPS[current_lap]["sectors"][0]["ended"] = cur_ts
            LAPS[current_lap]["sectors"][1]["started"] = cur_ts

    elif current_point.within(SECTOR3_POLY):
        if inside_poly:
            continue
        else:
            inside_poly = True

            LAPS[current_lap]["sectors"][1]["ended"] = cur_ts
            LAPS[current_lap]["sectors"][2]["started"] = cur_ts

    else:
        inside_poly = False

    if len(LAPS) > 5:
      break

lap_no = 1
for lap in LAPS:
  if not lap["started"] or not lap["ended"]: continue

  print "Lap %i: %s" % (lap_no, round((lap["ended"] - lap["started"]).total_seconds(), 3))
  print "\tsec1: %s secs" % round((lap["sectors"][0]["ended"] - lap["sectors"][0]["started"]).total_seconds(), 3)
  print "\tsec2: %s secs" % round((lap["sectors"][1]["ended"] - lap["sectors"][1]["started"]).total_seconds(), 3)
  print "\tsec3: %s secs" % round((lap["sectors"][2]["ended"] - lap["sectors"][2]["started"]).total_seconds(), 3)
  lap_no += 1
