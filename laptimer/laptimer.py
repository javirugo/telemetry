#!/usr/bin/python

#from mock_metrics import Metrics
from real_metrics import Metrics

import json
import time
from datetime import datetime
from shapely.geometry import Polygon, Point

with open('../tracks/JEREZ.json') as track_file:
    track_data = json.load(track_file)

START_POLY = Polygon([
    (track_data["START"]["lat3"], track_data["START"]["lon3"]),
    (track_data["START"]["lat2"], track_data["START"]["lon2"]),
    (track_data["START"]["lat4"], track_data["START"]["lon4"]),
    (track_data["START"]["lat1"], track_data["START"]["lon1"])
])

SECTOR2_POLY = Polygon([
    (track_data["SECTOR2"]["lat1"], track_data["SECTOR2"]["lon1"]),
    (track_data["SECTOR2"]["lat2"], track_data["SECTOR2"]["lon2"]),
    (track_data["SECTOR2"]["lat3"], track_data["SECTOR2"]["lon3"]),
    (track_data["SECTOR2"]["lat4"], track_data["SECTOR2"]["lon4"])
])

SECTOR3_POLY = Polygon([
    (track_data["SECTOR3"]["lat3"], track_data["SECTOR3"]["lon3"]),
    (track_data["SECTOR3"]["lat2"], track_data["SECTOR3"]["lon2"]),
    (track_data["SECTOR3"]["lat4"], track_data["SECTOR3"]["lon4"]),
    (track_data["SECTOR3"]["lat1"], track_data["SECTOR3"]["lon1"])
])

metricsSource = Metrics("/home/jaruiz/data.db")
#metricsSource = Metrics()
#metricsSource.setMockData(track_data["MOCK"])

current_sector = 0
current_lap = 0
inside_poly = False

LAPS = [{ "started": False, "ended": False,
	  "sectors": [
	    {"started": False, "ended": False},
	    {"started": False, "ended": False},
	    {"started": False, "ended": False} ]}]

while True:
    metrics_data = metricsSource.getMetrics()
    if not metrics_data: break

    cur_ts, cur_lat, cur_lon = metrics_data
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

lap_no = 1
best_lap = 999
best_sec1 = 999
best_sec2 = 999
best_sec3 = 999
for lap in LAPS:

  if not lap["started"] or not lap["ended"]: continue

  lap_time_seconds = (lap["ended"] - lap["started"]).total_seconds()
  if lap_time_seconds > 150: continue
  if lap_time_seconds < best_lap: best_lap = lap_time_seconds

  m, s = divmod(lap_time_seconds, 60)
  print "Lap %i: %02d:%05.2f" % (lap_no, m, s)
  if lap["sectors"][0]["ended"] and lap["sectors"][0]["started"]:
    sector_seconds = (lap["sectors"][0]["ended"] - lap["sectors"][0]["started"]).total_seconds()
    m, s = divmod(sector_seconds, 60)
    print "\tsec1: %02d:%05.2f" % (m, s)
    if sector_seconds < best_sec1: best_sec1 = sector_seconds

  if lap["sectors"][1]["ended"] and lap["sectors"][1]["started"]:
    sector_seconds = (lap["sectors"][1]["ended"] - lap["sectors"][1]["started"]).total_seconds()
    m, s = divmod(sector_seconds, 60)
    print "\tsec2: %02d:%05.2f" % (m, s)
    if sector_seconds < best_sec2: best_sec2 = sector_seconds

  if lap["sectors"][2]["ended"] and lap["sectors"][2]["started"]:
    sector_seconds = (lap["sectors"][2]["ended"] - lap["sectors"][2]["started"]).total_seconds()
    m, s = divmod(sector_seconds, 60)
    print "\tsec3: %02d:%05.2f" % (m, s)
    if sector_seconds < best_sec3: best_sec3 = sector_seconds

  lap_no += 1


m, s = divmod(best_lap, 60)
print "\n\nBEST LAP (REAL): %02d:%05.2f\n" % (m, s)

potential_lap_seconds = best_sec1 + best_sec2 + best_sec3
m, s = divmod(potential_lap_seconds, 60)
print "Best Sectors (potential lap): %02d:%05.2f" % (m, s)

m, s = divmod(best_sec1, 60)
print "\tsector1: %02d:%05.2f" % (m, s)

m, s = divmod(best_sec2, 60)
print "\tsector2: %02d:%05.2f" % (m, s)

m, s = divmod(best_sec3, 60)
print "\tsector3: %02d:%05.2f\n\n" % (m, s)
