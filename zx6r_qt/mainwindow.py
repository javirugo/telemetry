# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(478, 319)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet(_fromUtf8("QMainWindow { width: 318px; height: 238px; }\n"
"\n"
"#centralwidget { background-color: black; color: white; }\n"
"\n"
"QWidget { background-color: #262424; color: white; font-size: 12px; }\n"
"\n"
"QPushButton { background-color: black; color: white; border: 1px solid #4A4646; }\n"
"\n"
"QTabBar::tab { min-width: 185px; font-weight: normal; color: #DC3434; padding: 10px 22px; border: 0; background-color: black; font-size: 18px; }\n"
"\n"
"QTabBar::tab:selected { font-weight: bold; background-color: #4A585D; color: #85F187; }\n"
"\n"
"QTabWidget::pane { border: 2px solid red; border-radius: 7px; background-color: #3E3E3E;}\n"
"\n"
"#labelBestLapTime, #labelLastLapTime { font-size: 50px; font-weight: bold; }\n"
"\n"
"#labelLastLap, #labelBestLap { font-size: 16px; font-weight: bold; }\n"
"\n"
"#labelBestLapTime {color: #24A523; }\n"
"#labelLastLapTime {color: #9098A9; }\n"
"\n"
"#tabStatus QLabel { padding: 4px 2px;  qproperty-alignment: AlignCenter; background-color: black; font-size: 14px; }\n"
"\n"
"#tabStatus QLabel#labelStatusGyroscope, #tabStatus QLabel#labelStatusAccelerometer, #tabStatus QLabel#labelStatusCompass { background-color: #262424; }\n"
"\n"
"#pbRecord {  border-style: solid; border-width: 3px; border-color: #585858; border-radius: 8px; font-size: 26px; font-weight: bold;}\n"
"\n"
"#pbLiveStatus { font-size: 20px; font-weight: bold; border-radius: 8px; background-color: #463535; color: #AB0A0A; }\n"
"#pbLiveStatus:checked { background-color: #164321; color: #1B5028; }\n"
"\n"
"#pbShutdown, #pbReboot { border-radius: 4px; color: #D5A6A6; }\n"
"\n"
"#progressBarRPM { background-color: black; }\n"
"#progressBarRPM::chunk { background: #C6D0CE; }"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabApplication = QtGui.QTabWidget(self.centralwidget)
        self.tabApplication.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabApplication.setStyleSheet(_fromUtf8(""))
        self.tabApplication.setTabPosition(QtGui.QTabWidget.North)
        self.tabApplication.setIconSize(QtCore.QSize(16, 16))
        self.tabApplication.setObjectName(_fromUtf8("tabApplication"))
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.pbRecord = QtGui.QPushButton(self.tabMain)
        self.pbRecord.setGeometry(QtCore.QRect(20, 20, 411, 61))
        self.pbRecord.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbRecord.setObjectName(_fromUtf8("pbRecord"))
        self.labelLastLapTime = QtGui.QLabel(self.tabMain)
        self.labelLastLapTime.setGeometry(QtCore.QRect(80, 95, 341, 71))
        self.labelLastLapTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLastLapTime.setObjectName(_fromUtf8("labelLastLapTime"))
        self.labelBestLap = QtGui.QLabel(self.tabMain)
        self.labelBestLap.setGeometry(QtCore.QRect(10, 200, 61, 21))
        self.labelBestLap.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelBestLap.setObjectName(_fromUtf8("labelBestLap"))
        self.labelLastLap = QtGui.QLabel(self.tabMain)
        self.labelLastLap.setGeometry(QtCore.QRect(10, 120, 61, 21))
        self.labelLastLap.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelLastLap.setObjectName(_fromUtf8("labelLastLap"))
        self.labelBestLapTime = QtGui.QLabel(self.tabMain)
        self.labelBestLapTime.setGeometry(QtCore.QRect(80, 175, 341, 71))
        self.labelBestLapTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labelBestLapTime.setObjectName(_fromUtf8("labelBestLapTime"))
        self.tabApplication.addTab(self.tabMain, _fromUtf8(""))
        self.tabStatus = QtGui.QWidget()
        self.tabStatus.setObjectName(_fromUtf8("tabStatus"))
        self.labelStatusGyroscope = QtGui.QLabel(self.tabStatus)
        self.labelStatusGyroscope.setGeometry(QtCore.QRect(260, 60, 70, 31))
        self.labelStatusGyroscope.setObjectName(_fromUtf8("labelStatusGyroscope"))
        self.labelStatusAccelerometer = QtGui.QLabel(self.tabStatus)
        self.labelStatusAccelerometer.setGeometry(QtCore.QRect(30, 130, 71, 41))
        self.labelStatusAccelerometer.setObjectName(_fromUtf8("labelStatusAccelerometer"))
        self.labelStatus_lat = QtGui.QLabel(self.tabStatus)
        self.labelStatus_lat.setGeometry(QtCore.QRect(10, 10, 161, 41))
        self.labelStatus_lat.setObjectName(_fromUtf8("labelStatus_lat"))
        self.labelStatus_lon = QtGui.QLabel(self.tabStatus)
        self.labelStatus_lon.setGeometry(QtCore.QRect(170, 10, 161, 41))
        self.labelStatus_lon.setObjectName(_fromUtf8("labelStatus_lon"))
        self.labelStatus_gyros = QtGui.QLabel(self.tabStatus)
        self.labelStatus_gyros.setGeometry(QtCore.QRect(260, 150, 71, 41))
        self.labelStatus_gyros.setObjectName(_fromUtf8("labelStatus_gyros"))
        self.labelStatus_accelerometer = QtGui.QLabel(self.tabStatus)
        self.labelStatus_accelerometer.setGeometry(QtCore.QRect(100, 130, 121, 41))
        self.labelStatus_accelerometer.setObjectName(_fromUtf8("labelStatus_accelerometer"))
        self.labelStatusCompass = QtGui.QLabel(self.tabStatus)
        self.labelStatusCompass.setGeometry(QtCore.QRect(19, 90, 81, 41))
        self.labelStatusCompass.setObjectName(_fromUtf8("labelStatusCompass"))
        self.labelStatus_heading = QtGui.QLabel(self.tabStatus)
        self.labelStatus_heading.setGeometry(QtCore.QRect(100, 90, 121, 41))
        self.labelStatus_heading.setObjectName(_fromUtf8("labelStatus_heading"))
        self.labelStatus_speed = QtGui.QLabel(self.tabStatus)
        self.labelStatus_speed.setGeometry(QtCore.QRect(330, 10, 111, 41))
        self.labelStatus_speed.setObjectName(_fromUtf8("labelStatus_speed"))
        self.pbReboot = QtGui.QPushButton(self.tabStatus)
        self.pbReboot.setGeometry(QtCore.QRect(362, 230, 91, 31))
        self.pbReboot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbReboot.setObjectName(_fromUtf8("pbReboot"))
        self.pbShutdown = QtGui.QPushButton(self.tabStatus)
        self.pbShutdown.setGeometry(QtCore.QRect(2, 230, 91, 31))
        self.pbShutdown.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbShutdown.setObjectName(_fromUtf8("pbShutdown"))
        self.pbLiveStatus = QtGui.QPushButton(self.tabStatus)
        self.pbLiveStatus.setGeometry(QtCore.QRect(100, 220, 255, 41))
        self.pbLiveStatus.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbLiveStatus.setCheckable(True)
        self.pbLiveStatus.setObjectName(_fromUtf8("pbLiveStatus"))
        self.progressBarRPM = QtGui.QProgressBar(self.tabStatus)
        self.progressBarRPM.setGeometry(QtCore.QRect(390, 60, 41, 101))
        self.progressBarRPM.setMaximum(16000)
        self.progressBarRPM.setProperty("value", 0)
        self.progressBarRPM.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.progressBarRPM.setTextVisible(False)
        self.progressBarRPM.setOrientation(QtCore.Qt.Vertical)
        self.progressBarRPM.setObjectName(_fromUtf8("progressBarRPM"))
        self.dialLean = QtGui.QDial(self.tabStatus)
        self.dialLean.setGeometry(QtCore.QRect(260, 90, 71, 64))
        self.dialLean.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dialLean.setMaximum(360)
        self.dialLean.setProperty("value", 180)
        self.dialLean.setTracking(False)
        self.dialLean.setWrapping(False)
        self.dialLean.setNotchTarget(20.0)
        self.dialLean.setNotchesVisible(True)
        self.dialLean.setObjectName(_fromUtf8("dialLean"))
        self.lcdGear = QtGui.QLCDNumber(self.tabStatus)
        self.lcdGear.setGeometry(QtCore.QRect(396, 190, 31, 31))
        self.lcdGear.setNumDigits(1)
        self.lcdGear.setObjectName(_fromUtf8("lcdGear"))
        self.lcdRPM = QtGui.QLCDNumber(self.tabStatus)
        self.lcdRPM.setGeometry(QtCore.QRect(380, 160, 64, 23))
        self.lcdRPM.setObjectName(_fromUtf8("lcdRPM"))
        self.dialLean.raise_()
        self.labelStatusGyroscope.raise_()
        self.labelStatusAccelerometer.raise_()
        self.labelStatus_lat.raise_()
        self.labelStatus_lon.raise_()
        self.labelStatus_accelerometer.raise_()
        self.labelStatusCompass.raise_()
        self.labelStatus_heading.raise_()
        self.labelStatus_speed.raise_()
        self.pbReboot.raise_()
        self.pbShutdown.raise_()
        self.pbLiveStatus.raise_()
        self.progressBarRPM.raise_()
        self.lcdGear.raise_()
        self.lcdRPM.raise_()
        self.labelStatus_gyros.raise_()
        self.tabApplication.addTab(self.tabStatus, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabApplication)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))

        self.retranslateUi(MainWindow)
        self.tabApplication.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ZX6R", None))
        self.pbRecord.setText(_translate("MainWindow", "Record", None))
        self.labelLastLapTime.setText(_translate("MainWindow", "03:88:456", None))
        self.labelBestLap.setText(_translate("MainWindow", "Best:", None))
        self.labelLastLap.setText(_translate("MainWindow", "Last:", None))
        self.labelBestLapTime.setText(_translate("MainWindow", "03:88:456", None))
        self.tabApplication.setTabText(self.tabApplication.indexOf(self.tabMain), _translate("MainWindow", "Main", None))
        self.labelStatusGyroscope.setText(_translate("MainWindow", "Lean", None))
        self.labelStatusAccelerometer.setText(_translate("MainWindow", "GForce", None))
        self.labelStatus_lat.setText(_translate("MainWindow", "latitude", None))
        self.labelStatus_lon.setText(_translate("MainWindow", "longitude", None))
        self.labelStatus_gyros.setText(_translate("MainWindow", "degrees", None))
        self.labelStatus_accelerometer.setText(_translate("MainWindow", "0 to 2 g", None))
        self.labelStatusCompass.setText(_translate("MainWindow", "Compass", None))
        self.labelStatus_heading.setText(_translate("MainWindow", "heading", None))
        self.labelStatus_speed.setText(_translate("MainWindow", "speed", None))
        self.pbReboot.setText(_translate("MainWindow", "Reboot", None))
        self.pbShutdown.setText(_translate("MainWindow", "Shutdown", None))
        self.pbLiveStatus.setText(_translate("MainWindow", "LIVE", None))
        self.tabApplication.setTabText(self.tabApplication.indexOf(self.tabStatus), _translate("MainWindow", "Status", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))

