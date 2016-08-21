import sys, os
from datetime import datetime, timedelta
import time
import math
import glob

from PyQt4 import QtGui, QtCore
import mainwindow

useMock = False

if useMock:
   from threads import DataRecordThread
   from mocks import MultiWiiThread, GPSThread
else:
   from threads import MultiWiiThread, GPSThread, DataRecordThread


class MainWindow(QtGui.QMainWindow):

   def __init__(self):
      super(MainWindow, self).__init__()
      self.recording = False
      self.process = QtCore.QProcess(self)
      self.ui = mainwindow.Ui_MainWindow()
      self.ui.setupUi(self)

      self.ui.tableLaps.setColumnCount(2)
      self.ui.tableLaps.setRowCount(0)
      self.ui.tableLaps.setSortingEnabled(False)
      self.ui.tableLaps.horizontalHeader().setStretchLastSection(True)


      self.ui.pbRecord.clicked.connect(self.switchRecording)
      self.ui.pbReboot.clicked.connect(self.reboot)
      self.ui.pbShutdown.clicked.connect(self.shutdown)
      self.ui.pbRecord.setStyleSheet("background-color: #1EAC4B;")
      self.ui.pbLiveStatus.clicked.connect(self.pollerControl)

      self.ui.labelLastLapTime.setText("00:00.000")
      self.ui.labelBestLapTime.setText("00:00.000")

      self.MultiWiiThread = MultiWiiThread()
      self.connect( self.MultiWiiThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateMultiWii )
      self.GPSThread = GPSThread()
      self.connect( self.GPSThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateGPS )
      self.DataRecordThread = DataRecordThread(self)
      self.connect( self.DataRecordThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateLaptimes )
      self.DataRecordThread.loadHistory()

      self.start_datetime = False
      self.current_round_id = 0

      self.elapsed_time = False
      self.wii_altitude = 0
      self.wii_latitude = 0
      self.wii_longitude = 0
      self.wii_speed = 0
      self.altitude = 0
      self.latitude = 0
      self.longitude = 0
      self.speed = 0
      self.rpm = 0
      self.gear = 0
      self.gyros_x = 0
      self.gyros_y = 0
      self.gyros_z = 0
      self.gyros_temperature = 0
      self.accel_gforce_x = 0
      self.accel_gforce_y = 0
      self.accel_gforce_z = 0
      self.accel_angle_x = 0
      self.accel_angle_y = 0
      self.accel_angle_z = 0
      self.compass = 0
      self.baro_temperature = 0
      self.baro_pressure = 0

      self.gyros_correction = -5.7
      self.accel_correction = 0.20 #-0.21


   # If anything goes wrong, click the "reboot" button! 
   # https://www.youtube.com/watch?v=PtXtIivRRKQ
   def reboot(self):
      if self.recording: self.switchRecording()
      os.system("sudo reboot")


   # For safeness, shutdown with a button
   def shutdown(self):
      if self.recording: self.switchRecording()
      os.system("sudo shutdown -h now")


   # Called when needed... This controls that the pollers are started or stopped
   # depending on the status of "recording" and liveStatus-pushbutton
   def pollerControl(self, checkbox_status = False):
      if self.ui.pbLiveStatus.isChecked() or self.recording:
         if not self.MultiWiiThread.isRunning(): self.MultiWiiThread.start()
         if not self.GPSThread.isRunning(): self.GPSThread.start()
      else:
         self.MultiWiiThread.stop()
         self.GPSThread.stop()

      if not self.ui.pbLiveStatus.isChecked():
         self.ui.progressBarRPM.setValue(0)
         self.ui.dialLean.setValue(180)
         self.ui.lcdRPM.display(0)
         self.ui.lcdGear.display(0)
         self.ui.labelStatus_lat.setText("latitude")
         self.ui.labelStatus_lon.setText("longitude")
         self.ui.labelStatus_speed.setText("speed")
         self.ui.labelStatus_gyros.setText("degrees")
         self.ui.labelStatus_accelerometer.setText("0 to 2 g")
         self.ui.labelStatus_heading.setText("heading")
         self.ui.labelStatus_temperature.setText("degrees C")
         self.ui.labelStatus_pressure.setText("Pa")


   # Called from the DataRecordThread when a lap is finished
   def updateLaptimes(self, data, addLapToTable = True):
      if isinstance(data["last"], timedelta):
         timestr = "%.2d:%.2d.%s" % (
               (data["last"].seconds//60)%60,
               data["last"].seconds%60,
               str(data["last"].microseconds)[:3])

         self.ui.labelLastLapTime.setText(timestr)

         if addLapToTable:
            newrow = self.ui.tableLaps.rowCount() + 1
            self.ui.tableLaps.setRowCount(newrow)
            lapItem = QtGui.QTableWidgetItem("Lap %i  " % newrow)
            timeItem = QtGui.QTableWidgetItem(" %s" % timestr)
            lapItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            timeItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            if data["last"] <= data["best"]:
               rowIdx = 0
               while rowIdx < self.ui.tableLaps.rowCount():
                  prevLap = self.ui.tableLaps.item(rowIdx, 0)
                  prevTime = self.ui.tableLaps.item(rowIdx, 1)
                  if prevLap: prevLap.setBackgroundColor(QtGui.QColor(0, 0, 0))
                  if prevTime: prevTime.setBackgroundColor(QtGui.QColor(0, 0, 0))
                  rowIdx += 1

               lapItem.setBackgroundColor(QtGui.QColor(17, 62, 29))
               timeItem.setBackgroundColor(QtGui.QColor(17, 62, 29))
            else:
               lapItem.setBackgroundColor(QtGui.QColor(0, 0, 0))
               timeItem.setBackgroundColor(QtGui.QColor(0, 0, 0))

            self.ui.tableLaps.setItem(newrow -1, 0, lapItem)
            self.ui.tableLaps.setItem(newrow -1, 1, timeItem)


      if isinstance(data["best"], timedelta):
         self.ui.labelBestLapTime.setText(
            "%.2d:%.2d.%s" % (
               (data["best"].seconds//60)%60,
               data["best"].seconds%60,
               str(data["best"].microseconds)[:3]))


   # Called from the KDSThread when new data is received from KDS
   def updateMultiWii(self, data):
      self.wii_altitude = float(data["altitude"])
      self.wii_latitude = float(data["latitude"])
      self.wii_longitude = float(data["longitude"])
      self.wii_speed = int(data["speed"])
      self.compass = float(data["heading"])
      self.accel_gforce_x = float(data["gforce_x"])
      self.accel_gforce_y = float(data["gforce_y"]) + self.accel_correction
      self.accel_gforce_z = float(data["gforce_z"])
      self.accel_angle_x = float(data["xAngle"]) + self.gyros_correction
      self.accel_angle_y = float(data["yAngle"])
      self.accel_angle_z = float(data["zAngle"])
      self.gyros_x = float(data["hx"])
      self.gyros_y = float(data["hy"])
      self.gyros_z = float(data["hz"])
      self.gyros_temperature = int(data["temperature"])
      self.baro_temperature = int(data["temp_bmp"]) / 10
      self.baro_pressure = int(data["pressure"])
      self.rpm = int(data["rpm"])
      self.gear = int(data["gear"])

      if self.ui.pbLiveStatus.isChecked():
         self.ui.lcdRPM.display(self.rpm)
         self.ui.lcdGear.display(self.gear)
         self.ui.progressBarRPM.setValue(self.rpm)
         self.ui.dialLean.setValue((self.accel_angle_x * -1) + 180)
         self.ui.labelStatus_gyros.setText(str(self.accel_angle_x))
         self.ui.labelStatus_accelerometer.setText(str(round(self.accel_gforce_y, 2)))
         self.ui.labelStatus_heading.setText(str(round(self.compass, 4)))
         self.ui.labelStatus_temperature.setText(str(round(self.gyros_temperature, 0)))
         self.ui.labelStatus_pressure.setText(str(self.baro_pressure))


   # Called from the GPSThread when new data is received from GPS
   def updateGPS(self, data):
      self.altitude = 0 if math.isnan(data["altitude"]) else data["altitude"]
      self.latitude = 0 if math.isnan(data["latitude"]) else data["latitude"]
      self.longitude = 0 if math.isnan(data["longitude"]) else data["longitude"]
      self.speed = 0 if math.isnan(data["speed"]) else data["speed"]

      if self.ui.pbLiveStatus.isChecked():
         self.ui.labelStatus_lat.setText(str(self.latitude))
         self.ui.labelStatus_lon.setText(str(self.longitude))
         self.ui.labelStatus_speed.setText("%s kph" % str(self.speed))


   # Issued when the record button is pressed
   def switchRecording(self):
      if not self.recording:
         self.recording = True
         self.start_datetime = datetime.utcnow()
         self.ui.pbRecord.setStyleSheet("background-color: #662222;")
         self.pollerControl()
         self.DataRecordThread.start()
         self.ui.pbRecord.setStyleSheet("background-color: #AC1E2C;")
         self.ui.pbRecord.setText("STOP Recording")
      else:
         self.recording = False
         self.DataRecordThread.stop()
         self.ui.pbRecord.setStyleSheet("background-color: #1EAC4B;")
         self.ui.pbRecord.setText("Record")
         self.pollerControl()



app = QtGui.QApplication(sys.argv)
my_mainWindow = MainWindow()

QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
my_mainWindow.showFullScreen()

sys.exit(app.exec_())

