#!/usr/bin/python

from datetime import datetime
import time
import random

class Metrics:

  def setMockData(self, data):
    self.data = data
    self.index = 0

  def getMetrics(self):
    time.sleep(round(random.uniform(0.001, 0.090), 3))
    if self.index == (len(self.data) -1):
        return False
        #self.index = 0

    retval = [datetime.now(), self.data[self.index][1], self.data[self.index][0]]
    self.index += 1
    return retval
