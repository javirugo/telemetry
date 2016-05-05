#!/usr/bin/python

from datetime import datetime

class Metrics:

  def setMockData(self, data):
    self.data = data
    self.index = 0

  def getMetrics(self):
    if self.index == (len(self.data) -1):
      self.index = 0

    retval = [datetime.now(), self.data[self.index][1], self.data[self.index][0]]
    self.index += 1
    return retval
