
import json
from datetime import datetime
from shapely.geometry import Polygon, Point


class Laptimer():
   CHECKPOINT_START = 1
   CHECKPOINT_SECTOR2 = 2
   CHECKPOINT_SECTOR3 = 3

   def __init__(self, trackfile):
      self.inside_area = False

      with open(trackfile) as track_file:
         track_data = json.load(track_file)

         self.START_POLY = Polygon([
             (track_data["START"]["lat1"], track_data["START"]["lon1"]),
             (track_data["START"]["lat2"], track_data["START"]["lon2"]),
             (track_data["START"]["lat3"], track_data["START"]["lon3"]),
             (track_data["START"]["lat4"], track_data["START"]["lon4"])
         ])

         self.SECTOR2_POLY = Polygon([
             (track_data["SECTOR2"]["lat1"], track_data["SECTOR2"]["lon1"]),
             (track_data["SECTOR2"]["lat2"], track_data["SECTOR2"]["lon2"]),
             (track_data["SECTOR2"]["lat3"], track_data["SECTOR2"]["lon3"]),
             (track_data["SECTOR2"]["lat4"], track_data["SECTOR2"]["lon4"])
         ])

         self.SECTOR3_POLY = Polygon([
             (track_data["SECTOR3"]["lat1"], track_data["SECTOR3"]["lon1"]),
             (track_data["SECTOR3"]["lat2"], track_data["SECTOR3"]["lon2"]),
             (track_data["SECTOR3"]["lat3"], track_data["SECTOR3"]["lon3"]),
             (track_data["SECTOR3"]["lat4"], track_data["SECTOR3"]["lon4"])
         ])
      
         track_file.close()


   def check(self, latitude, longitude, current_dt = False):
      current_point = Point(latitude, longitude)
      cur_ts = datetime.utcnow() if not current_dt else current_dt

      if current_point.within(self.START_POLY):
         if self.inside_area:
            return False
         else:
            self.inside_area = True
            return self.CHECKPOINT_START

      elif current_point.within(self.SECTOR2_POLY):
         if self.inside_area:
            return False
         else:
            self.inside_area = True
            return self.CHECKPOINT_SECTOR2

      elif current_point.within(self.SECTOR3_POLY):
         if self.inside_area:
            return False
         else:
            self.inside_area = True
            return self.CHECKPOINT_SECTOR3

      else:
         self.inside_area = False

      return False


   def loadHistory(self, all_laps, last_lap, best_lap):
      for lap in all_laps:
         last_lap = datetime.fromtimestamp(lap["end"]) - datetime.fromtimestamp(lap["start"])
         if last_lap < best_lap or best_lap == 0:
            best_lap = last_lap


