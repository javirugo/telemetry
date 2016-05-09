import sys, os
from datetime import datetime
import time
import glob

from PyQt4 import QtGui, QtCore
import mainwindow
from threads import KDSThread, GPSThread

settings = {
  "start_raspi": "/picam/start.sh",
  "picam_home": "/picam"
}


class MainWindow(QtGui.QMainWindow):

   def __init__(self, settings):
      super(MainWindow, self).__init__()
      self.recording = False
      self.start_datetime = False
      self.settings = settings
      self.process = QtCore.QProcess(self)
      self.ui = mainwindow.Ui_MainWindow()
      self.ui.setupUi(self)

      self.ui.pbRecord.clicked.connect(self.switchRecording)
      self.ui.tabMedia.currentChanged.connect(self.changedSelectedTab)
      self.ui.pbRecord.setStyleSheet("background-color: #1EAC4B;")
      self.ui.lvMediaList.doubleClicked.connect(self.playVideo)
      self.ui.radioLiveStatus.toggled.connect(self.liveStatusSwitch)
      self.ui.radioLiveLaptimer.toggled.connect(self.liveLaptimerSwitch)

      self.KDSThread = KDSThread()
      self.connect( self.KDSThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateKDS )
      self.GPSThread = GPSThread()
      self.connect( self.GPSThread, QtCore.SIGNAL("update(PyQt_PyObject)"), self.updateGPS )
      
      self.latitude = 0
      self.longitude = 0
      self.speed = 0
      self.rpm = 0
      self.kph = 0
      self.lean = 0
      self.gforce = 0


   def pollMetrics(self, running = True):
      if running:
         if not self.KDSThread.isRunning():
            self.KDSThread.start()

         if not self.GPSThread.isRunning():
            self.GPSThread.start()
      else:
         self.KDSThread.stop()
         self.GPSThread.stop()


   def liveLaptimerSwitch(self, checked):
      pass


   def liveStatusSwitch(self, checked):
      if checked:
         self.pollMetrics()
      else:
         if not self.recording:
            self.pollMetrics(False)


   def updateKDS(self, data):
      print data
      self.rpm = data["rpm"]
      self.kph = data["kph"]
      self.lean = data["lean"]
      self.gforce = data["gforce"]

      if self.ui.radioLiveStatus.isChecked():
         self.ui.labelStatus_gyros.setText(str(self.lean))
         self.ui.labelStatus_accelerometer.setText(str(self.gforce))
         self.ui.labelStatus_rpm.setText(str(self.rpm))
         self.ui.labelStatus_kph.setText(str(self.kph))


   def updateGPS(self, data):
      print data
      self.latitude = data["latitude"]
      self.longitude = data["longitude"]
      self.speed = data["speed"]

      if self.ui.radioLiveStatus.isChecked():
         self.ui.labelStatus_lat.setText(str(self.latitude))
         self.ui.labelStatus_lon.setText(str(self.longitude))


   def startRecording(self):
         self.start_datetime = datetime.now()
         
         os.system("echo 'dir=/datos\nfilename=%s.ts' > /picam/hooks/start_record" % self.start_datetime)
         self.ui.pbRecord.setStyleSheet("background-color: #AC1E2C;")
         self.ui.pbRecord.setText("STOP Recording")


   def stopRecording(self):
         os.system("killall picam")

         if not self.ui.radioLiveStatus.isChecked():
            self.pollMetrics(False)

         self.ui.pbRecord.setStyleSheet("background-color: #1EAC4B;")
         self.ui.pbRecord.setText("Record")
         self.recording = False


   def switchRecording(self):
      self.timeoutTimer = QtCore.QTimer(self)
      self.timeoutTimer.setSingleShot(True)

      if not self.recording:
         self.recording = True

         # TODO: Ensure gnome-mplayer is killed

         self.pollMetrics()

         self.process.close()
         self.process.start(self.settings["start_raspi"])
         self.timeoutTimer.timeout.connect(self.startRecording)

      else:
         if not self.ui.radioLiveStatus.isChecked():
            self.pollMetrics(False)

         os.system("touch %s/hooks/stop_record" % self.settings["picam_home"])
         self.timeoutTimer.timeout.connect(self.stopRecording)

      self.timeoutTimer.start(3000)


   def updateVideosList(self):
      model = QtGui.QStandardItemModel(self.ui.lvMediaList)

      list = glob.glob("/datos/*.ts")
      for video in list:
         videoItem = QtGui.QStandardItem(video.replace("/datos/", "").replace(".ts", ""))
         model.appendRow(videoItem)

      self.ui.lvMediaList.setModel(model)


   def changedSelectedTab(self, tabIndex):
      if tabIndex == 3:
         self.updateVideosList()
      else:
         self.process.kill()


   def playVideo(self, clickedVideo):
      if self.recording: return
      self.process.close()
      self.process.start(
         'gnome-mplayer', [
            "--window", str(self.ui.widgetPlayer.winId()),
            "--showcontrols=1",
            "--autostart=1",
            "--disablefullscreen",
            "--replace_and_play",
            "--width=350",
            "--height=260",
            "--quit_on_complete",
            "/datos/%s.ts" % clickedVideo.data().toString()])


   '''
   def stopVideo(self, event):
      self.process.kill()
      self.ui.widgetPlayer.setStyleSheet("background-color: black;")
   '''

app = QtGui.QApplication(sys.argv)
my_mainWindow = MainWindow(settings)
my_mainWindow.show()
#my_mainWindow.showFullScreen()

sys.exit(app.exec_())
