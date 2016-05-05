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
    (track_data["START"]["lat3"], track_data["START"]["lon3"])
])

SECTOR2_POLY = Polygon([
    (track_data["SECTOR2"]["lat1"], track_data["SECTOR2"]["lon1"]),
    (track_data["SECTOR2"]["lat2"], track_data["SECTOR2"]["lon2"]),
    (track_data["SECTOR2"]["lat3"], track_data["SECTOR2"]["lon3"])
])

SECTOR3_POLY = Polygon([
    (track_data["SECTOR3"]["lat1"], track_data["SECTOR3"]["lon1"]),
    (track_data["SECTOR3"]["lat2"], track_data["SECTOR3"]["lon2"]),
    (track_data["SECTOR3"]["lat3"], track_data["SECTOR3"]["lon3"])
])

LAPS = []
metricsSource = Metrics()
metricsSource.setMockData(track_data["MOCK"])

current_sector = 0
current_lap = 0
inside_poly = False

LAPS.append({ "started": False, "ended": False,
	  "sectors": [
	    {"started": False, "ended": False},
	    {"started": False, "ended": False},
	    {"started": False, "ended": False} ]})
while True:
    cur_ts, cur_lat, cur_lon = metricsSource.getMetrics()
    current_point = Point(cur_lat, cur_lon)
    # print "%s, %s, %s" % (cur_ts, cur_lat, cur_lon)

    if current_point.within(START_POLY):
        if inside_poly:
            continue
        else:
            inside_poly = True
	    print "start!"
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
	    print "SECTOR2"
            inside_poly = True

            LAPS[current_lap]["sectors"][0]["ended"] = cur_ts
            LAPS[current_lap]["sectors"][1]["started"] = cur_ts

    elif current_point.within(SECTOR3_POLY):
        if inside_poly:
            continue
        else:
	    print "SECTOR3"
            inside_poly = True

            LAPS[current_lap]["sectors"][1]["ended"] = cur_ts
            LAPS[current_lap]["sectors"][2]["started"] = cur_ts

    else:
        inside_poly = False
    
    if len(LAPS) > 2:
      break

print LAPS
