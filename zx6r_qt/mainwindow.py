# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu May  5 20:41:51 2016
#      by: PyQt4 UI code generator 4.11.1
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
        MainWindow.resize(481, 322)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet(_fromUtf8("QMainWindow { width: 468px; height: 218px; }\n"
"\n"
"#centralwidget { background-color: black; color: white; }\n"
"\n"
"QWidget { background-color: #262424; color: white; font-size: 14px; }\n"
"\n"
"QPushButton { background-color: black; color: white; border: 1px solid #4A4646; }\n"
"\n"
"QTabBar::tab { min-width: 75px; font-weight: normal; color: #DC3434; padding: 10px 20px; border: 0; background-color: black; }\n"
"\n"
"QTabBar::tab:selected { font-weight: bold; background-color: #4A585D; color: #85F187; }\n"
"\n"
"QTabWidget::pane { border: 2px solid red; border-radius: 7px; background-color: #3E3E3E;}\n"
"\n"
"#labelCurrentLapTime, #labelBestLapTime, #labelLastLapTime { font-size: 50px; }\n"
"\n"
"#labelCurrentLapTime {color: #95FAFF; }\n"
"#labelBestLapTime {color: #24A523; }\n"
"#labelLastLapTime {color: #9098A9; }\n"
"\n"
"#tabStatus QLabel { padding: 8px 2px;  qproperty-alignment: AlignCenter; background-color: black; }"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabMedia = QtGui.QTabWidget(self.centralwidget)
        self.tabMedia.setStyleSheet(_fromUtf8(""))
        self.tabMedia.setTabPosition(QtGui.QTabWidget.North)
        self.tabMedia.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabMedia.setIconSize(QtCore.QSize(16, 16))
        self.tabMedia.setObjectName(_fromUtf8("tabMedia"))
        self.tabActions = QtGui.QWidget()
        self.tabActions.setObjectName(_fromUtf8("tabActions"))
        self.pbRecord = QtGui.QPushButton(self.tabActions)
        self.pbRecord.setGeometry(QtCore.QRect(10, 10, 191, 51))
        self.pbRecord.setObjectName(_fromUtf8("pbRecord"))
        self.pbQuit = QtGui.QPushButton(self.tabActions)
        self.pbQuit.setGeometry(QtCore.QRect(310, 210, 141, 41))
        self.pbQuit.setObjectName(_fromUtf8("pbQuit"))
        self.tabMedia.addTab(self.tabActions, _fromUtf8(""))
        self.tabStatus = QtGui.QWidget()
        self.tabStatus.setObjectName(_fromUtf8("tabStatus"))
        self.labelStatusCamera = QtGui.QLabel(self.tabStatus)
        self.labelStatusCamera.setGeometry(QtCore.QRect(10, 30, 141, 36))
        self.labelStatusCamera.setObjectName(_fromUtf8("labelStatusCamera"))
        self.labelStatusGPS = QtGui.QLabel(self.tabStatus)
        self.labelStatusGPS.setGeometry(QtCore.QRect(10, 70, 141, 36))
        self.labelStatusGPS.setObjectName(_fromUtf8("labelStatusGPS"))
        self.labelStatusGyroscope = QtGui.QLabel(self.tabStatus)
        self.labelStatusGyroscope.setGeometry(QtCore.QRect(10, 110, 141, 36))
        self.labelStatusGyroscope.setObjectName(_fromUtf8("labelStatusGyroscope"))
        self.labelStatusAccelerometer = QtGui.QLabel(self.tabStatus)
        self.labelStatusAccelerometer.setGeometry(QtCore.QRect(10, 150, 141, 36))
        self.labelStatusAccelerometer.setObjectName(_fromUtf8("labelStatusAccelerometer"))
        self.labelStatusKDS = QtGui.QLabel(self.tabStatus)
        self.labelStatusKDS.setGeometry(QtCore.QRect(10, 190, 141, 36))
        self.labelStatusKDS.setObjectName(_fromUtf8("labelStatusKDS"))
        self.tabMedia.addTab(self.tabStatus, _fromUtf8(""))
        self.tabTiming = QtGui.QWidget()
        self.tabTiming.setObjectName(_fromUtf8("tabTiming"))
        self.labelCurrentLap = QtGui.QLabel(self.tabTiming)
        self.labelCurrentLap.setGeometry(QtCore.QRect(20, 40, 91, 16))
        self.labelCurrentLap.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCurrentLap.setObjectName(_fromUtf8("labelCurrentLap"))
        self.labelCurrentLapTime = QtGui.QLabel(self.tabTiming)
        self.labelCurrentLapTime.setGeometry(QtCore.QRect(120, 30, 301, 41))
        self.labelCurrentLapTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCurrentLapTime.setObjectName(_fromUtf8("labelCurrentLapTime"))
        self.labelLastLap = QtGui.QLabel(self.tabTiming)
        self.labelLastLap.setGeometry(QtCore.QRect(20, 120, 91, 16))
        self.labelLastLap.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelLastLap.setObjectName(_fromUtf8("labelLastLap"))
        self.labelLastLapTime = QtGui.QLabel(self.tabTiming)
        self.labelLastLapTime.setGeometry(QtCore.QRect(120, 110, 301, 41))
        self.labelLastLapTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLastLapTime.setObjectName(_fromUtf8("labelLastLapTime"))
        self.labelBestLapTime = QtGui.QLabel(self.tabTiming)
        self.labelBestLapTime.setGeometry(QtCore.QRect(120, 190, 301, 41))
        self.labelBestLapTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labelBestLapTime.setObjectName(_fromUtf8("labelBestLapTime"))
        self.labelBestLap = QtGui.QLabel(self.tabTiming)
        self.labelBestLap.setGeometry(QtCore.QRect(20, 200, 91, 16))
        self.labelBestLap.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelBestLap.setObjectName(_fromUtf8("labelBestLap"))
        self.tabMedia.addTab(self.tabTiming, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.widgetPlayer = QtGui.QWidget(self.tab)
        self.widgetPlayer.setGeometry(QtCore.QRect(110, 0, 351, 261))
        self.widgetPlayer.setObjectName(_fromUtf8("widgetPlayer"))
        self.lvMediaList = QtGui.QListView(self.tab)
        self.lvMediaList.setGeometry(QtCore.QRect(0, 0, 111, 261))
        self.lvMediaList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.lvMediaList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.lvMediaList.setMovement(QtGui.QListView.Free)
        self.lvMediaList.setObjectName(_fromUtf8("lvMediaList"))
        self.tabMedia.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabMedia)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))

        self.retranslateUi(MainWindow)
        self.tabMedia.setCurrentIndex(3)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QObject.connect(self.pbQuit, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ZX6R", None))
        self.pbRecord.setText(_translate("MainWindow", "Record", None))
        self.pbQuit.setText(_translate("MainWindow", "Quit", None))
        self.tabMedia.setTabText(self.tabMedia.indexOf(self.tabActions), _translate("MainWindow", "Actions", None))
        self.labelStatusCamera.setText(_translate("MainWindow", "MEDIA", None))
        self.labelStatusGPS.setText(_translate("MainWindow", "GPS", None))
        self.labelStatusGyroscope.setText(_translate("MainWindow", "GYROSCOPE", None))
        self.labelStatusAccelerometer.setText(_translate("MainWindow", "ACCELEROMETER", None))
        self.labelStatusKDS.setText(_translate("MainWindow", "KDS", None))
        self.tabMedia.setTabText(self.tabMedia.indexOf(self.tabStatus), _translate("MainWindow", "Status", None))
        self.labelCurrentLap.setText(_translate("MainWindow", "Current Lap:", None))
        self.labelCurrentLapTime.setText(_translate("MainWindow", "03:88:456", None))
        self.labelLastLap.setText(_translate("MainWindow", "Last:", None))
        self.labelLastLapTime.setText(_translate("MainWindow", "03:88:456", None))
        self.labelBestLapTime.setText(_translate("MainWindow", "03:88:456", None))
        self.labelBestLap.setText(_translate("MainWindow", "Best:", None))
        self.tabMedia.setTabText(self.tabMedia.indexOf(self.tabTiming), _translate("MainWindow", "Lap Timer", None))
        self.tabMedia.setTabText(self.tabMedia.indexOf(self.tab), _translate("MainWindow", "Media", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))

