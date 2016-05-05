#!/usr/bin/python

from mock_metrics import Metrics
import json
import time

with open('ALMERIA.json') as track_file:
    track_data = json.load(track_file)

metrics = Metrics()
metrics.setMockData(track_data["MOCK"])
