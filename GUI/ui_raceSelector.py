# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\Betty\src\GUI\raceSelector.ui'
#
# Created: Sun Apr 04 19:41:17 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_raceSelector(object):
    def setupUi(self, raceSelector):
        raceSelector.setObjectName("raceSelector")
        raceSelector.resize(679, 378)
        self.verticalLayout = QtGui.QVBoxLayout(raceSelector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(raceSelector)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox = QtGui.QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dateList = QtGui.QListWidget(self.groupBox)
        self.dateList.setObjectName("dateList")
        self.horizontalLayout.addWidget(self.dateList)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.frame)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.courseList = QtGui.QListWidget(self.groupBox_2)
        self.courseList.setObjectName("courseList")
        self.horizontalLayout_2.addWidget(self.courseList)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(self.frame)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.timeList = QtGui.QListWidget(self.groupBox_3)
        self.timeList.setObjectName("timeList")
        self.horizontalLayout_3.addWidget(self.timeList)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(raceSelector)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtGui.QSpacerItem(476, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.frame_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.frame_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_5.addWidget(self.pushButton_2)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(raceSelector)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), raceSelector.accept)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), raceSelector.reject)
        QtCore.QObject.connect(self.timeList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), raceSelector.accept)
        QtCore.QMetaObject.connectSlotsByName(raceSelector)

    def retranslateUi(self, raceSelector):
        raceSelector.setWindowTitle(QtGui.QApplication.translate("raceSelector", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("raceSelector", "Race Date", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("raceSelector", "Race Course", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("raceSelector", "Race Time", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("raceSelector", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("raceSelector", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

