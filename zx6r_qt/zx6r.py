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
   from mocks import KDSThread, GPSThread, I2CThread
else:
   from threads import KDSThread, GPSThread, I2CThread, DataRecordThread

settings = {
  "start_raspi": "/picam/start.sh",
  "picam_home": "/picam",
  "KDSSerialPort": "/dev/ttyKDS"
}


class MainWindow(QtGui.QMainWindow):

   def __init__(self, settings):
      super(MainWindow, self).__init__()
      self.recording = False
      self.settings = settings
      self.process = QtCore.QProcess(self)
      self.ui = mainwindow.Ui_MainWindow()
      self.ui.setupUi(self)

      self.ui.pbRecord.clicked.connect(self.switchRecording)
      self.ui.pbReboot.clicked.connect(self.reboot)
      self.ui.pbShutdown.clicked.connect(self.shutdown)
      self.ui.pbRecord.setStyleSheet("background-color: #1EAC4B;")
      self.ui.pbLiveStatus.clicked.connect(self.pollerControl)

      os.system("sudo killall pigpiod && sudo pigpiod &")

      self.KDSThread = KDSThread()
      self.connect( self.KDSThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateKDS )
      self.GPSThread = GPSThread()
      self.connect( self.GPSThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateGPS )
      self.I2CThread = I2CThread()
      self.connect( self.I2CThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateI2C )
      
      self.DataRecordThread = DataRecordThread(self)
      self.connect( self.DataRecordThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateLaptimes )

      self.ui.labelLastLapTime.setText("00:00.000")
      self.ui.labelBestLapTime.setText("00:00.000")
      self.updateLaptimes({
         "last": self.DataRecordThread.last_lap_time,
         "best": self.DataRecordThread.fastest_lap_time})

      self.start_datetime = False
      self.current_round_id = 0
      self.latitude = 0
      self.longitude = 0
      self.speed = 0
      self.rpm = 0
      self.gear = 0
      self.lean_x = 0
      self.lean_y = 0
      self.lean_z = 0
      self.gforce_x = 0
      self.gforce_y = 0
      self.gforce_z = 0
      self.compass = 0
      

   # If anything goes wrong, click the "reboot" button!
   # https://www.youtube.com/watch?v=PtXtIivRRKQ
   def reboot(self):
      os.system("sudo reboot")


   # For safeness, shutdown with a button
   def shutdown(self):
      os.system("sudo shutdown -h now")


   # Called when needed... This controls that the pollers are started or stopped
   # depending on the status of "recording" and liveStatus-pushbutton
   def pollerControl(self, checkbox_status = False):
      if self.ui.pbLiveStatus.isChecked() or self.recording:
         if not self.KDSThread.isRunning(): self.KDSThread.start()
         if not self.I2CThread.isRunning(): self.I2CThread.start()
         if not self.GPSThread.isRunning(): self.GPSThread.start()
      else:
         self.KDSThread.stop()
         self.GPSThread.stop()
         self.I2CThread.stop()
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


   # Called from the DataRecordThread when a lap is finished
   def updateLaptimes(self, data):
      if isinstance(data["last"], timedelta):
         self.ui.labelLastLapTime.setText(
            "%.2d:%.2d.%s" % (
               (data["last"].seconds//60)%60,
               data["last"].seconds%60,
               str(data["last"].microseconds)[:3]))

         #self.ui.labelLastLapTime.setText(str(data["last"]))

      if isinstance(data["best"], timedelta):
         self.ui.labelBestLapTime.setText(
            "%.2d:%.2d.%s" % (
               (data["best"].seconds//60)%60,
               data["best"].seconds%60,
               str(data["best"].microseconds)[:3]))

         #self.ui.labelBestLapTime.setText(str(data["best"]))


   # Called from the KDSThread when new data is received from KDS
   def updateKDS(self, data):
      self.rpm = data["rpm"]
      self.gear = data["gear"]

      if self.ui.pbLiveStatus.isChecked():
         self.ui.lcdRPM.display(self.rpm)
         self.ui.lcdGear.display(self.gear)
         self.ui.progressBarRPM.setValue(self.rpm)


   # Called from the GPSThread when new data is received from GPS
   def updateGPS(self, data):
      self.latitude = 0 if math.isnan(data["latitude"]) else data["latitude"]
      self.longitude = 0 if math.isnan(data["longitude"]) else data["longitude"]
      self.speed = 0 if math.isnan(data["speed"]) else data["speed"]

      if self.ui.pbLiveStatus.isChecked():
         self.ui.labelStatus_lat.setText(str(self.latitude))
         self.ui.labelStatus_lon.setText(str(self.longitude))
         self.ui.labelStatus_speed.setText("%s kph" % str(self.speed))


   # Called from the I2CThread when new data is available on I2C
   def updateI2C(self, data):
      self.lean_x = data["lean_x"]
      self.lean_y = data["lean_y"]
      self.lean_z = data["lean_z"]
      self.gforce_x = data["gforce_x"]
      self.gforce_y = data["gforce_y"]
      self.gforce_z = data["gforce_z"]
      self.compass = data["compass"]

      if self.ui.pbLiveStatus.isChecked():
         self.ui.dialLean.setValue(round(self.lean_x + 180))
         self.ui.labelStatus_gyros.setText(str(round(self.lean_x, 2)))
         self.ui.labelStatus_accelerometer.setText(str(round(self.gforce_x, 2)))
         self.ui.labelStatus_heading.setText(str(self.compass))


   # This is called with a small delay from the record-switch method to allow picam
   # to start the daemon and get ready
   def startRecording(self):
         #self.start_datetime = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
         self.start_datetime = datetime.utcnow()

         os.system("echo 'dir=/datos\nfilename=%s.ts' > /picam/hooks/start_record" % \
            int((self.start_datetime - datetime(1970, 1, 1)).total_seconds()))

         self.DataRecordThread.start()
         self.ui.pbRecord.setStyleSheet("background-color: #AC1E2C;")
         self.ui.pbRecord.setText("STOP Recording")


   # This is called with a small delay from the record-switch method to allow picam
   # to stop recording before killing the daemon
   def stopRecording(self):
         os.system("killall picam")

         self.ui.pbRecord.setStyleSheet("background-color: #1EAC4B;")
         self.ui.pbRecord.setText("Record")
         self.recording = False
         self.pollerControl()


   # Issued when the record button is pressed
   def switchRecording(self):
      self.timeoutTimer = QtCore.QTimer(self)
      self.timeoutTimer.setSingleShot(True)

      if not self.recording:
         self.ui.pbRecord.setStyleSheet("background-color: #662222;")
         self.recording = True
         self.pollerControl()

         self.process.close()
         self.process.start(self.settings["start_raspi"])
         self.timeoutTimer.timeout.connect(self.startRecording)

      else:
         self.ui.pbRecord.setStyleSheet("background-color: #662222;")
         os.system("touch %s/hooks/stop_record" % self.settings["picam_home"])
         self.DataRecordThread.stop()
         self.timeoutTimer.timeout.connect(self.stopRecording)

      self.timeoutTimer.start(3000)



app = QtGui.QApplication(sys.argv)
my_mainWindow = MainWindow(settings)

if useMock:
   my_mainWindow.show()
else:
   QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
   my_mainWindow.showFullScreen()

sys.exit(app.exec_())

