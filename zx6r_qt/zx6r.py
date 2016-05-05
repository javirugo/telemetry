import sys
from datetime import datetime
import time
import glob

from PyQt4 import QtGui, QtCore
import mainwindow

settings = {
  "start_raspi": "/home/jaruiz/workspace/start_raspi.sh",
  "picam_home": "/home/jaruiz/picam"
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


  def switchRecording(self):
    if not self.recording:

      # TODO: Ensure gnome-mplayer is killed

      self.process.close()
      self.process.start(self.settings["start_raspi"])
      self.process.waitForFinished(3000)

      self.start_datetime = datetime.now()
      self.process.start("echo 'dir=/datos\nfilename=%s.ts' > %s/hooks/start_record" % (self.start_datetime, self.settings["picam_home"]))
      self.ui.pbRecord.setStyleSheet("background-color: #AC1E2C;")
      self.ui.pbRecord.setText("STOP Recording")
      self.recording = True
    else:
      self.process.close()
      self.process.start("touch %s/hooks/stop_record" % self.settings["picam_home"])
      self.process.waitForFinished(3000)
      self.process.close()
      self.process.start("export CAMPID=`ps uax | grep picam | grep -v grep | awk '{print $2}'`; kill -9 $CAMPID >/dev/null 2>&1")

      self.ui.pbRecord.setStyleSheet("background-color: #1EAC4B;")
      self.ui.pbRecord.setText("Record")
      self.recording = False


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
	    '--window', str(self.ui.widgetPlayer.winId()),
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
