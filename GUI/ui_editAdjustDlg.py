# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\Betty\src\GUI\editAdjustDlg.ui'
#
# Created: Thu Feb 11 21:12:08 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_adjustDlg(object):
    def setupUi(self, adjustDlg):
        adjustDlg.setObjectName("adjustDlg")
        adjustDlg.resize(242, 242)
        adjustDlg.setMinimumSize(QtCore.QSize(242, 242))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Horse"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        adjustDlg.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(adjustDlg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtGui.QListWidget(adjustDlg)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addButton = QtGui.QPushButton(adjustDlg)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.upButton = QtGui.QPushButton(adjustDlg)
        self.upButton.setObjectName("upButton")
        self.verticalLayout.addWidget(self.upButton)
        self.downButton = QtGui.QPushButton(adjustDlg)
        self.downButton.setObjectName("downButton")
        self.verticalLayout.addWidget(self.downButton)
        self.delButton = QtGui.QPushButton(adjustDlg)
        self.delButton.setObjectName("delButton")
        self.verticalLayout.addWidget(self.delButton)
        self.sortButton = QtGui.QPushButton(adjustDlg)
        self.sortButton.setObjectName("sortButton")
        self.verticalLayout.addWidget(self.sortButton)
        self.setDefaultsButton = QtGui.QPushButton(adjustDlg)
        self.setDefaultsButton.setObjectName("setDefaultsButton")
        self.verticalLayout.addWidget(self.setDefaultsButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(adjustDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(adjustDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), adjustDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), adjustDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(adjustDlg)

    def retranslateUi(self, adjustDlg):
        adjustDlg.setWindowTitle(QtGui.QApplication.translate("adjustDlg", "Edit Adjustments", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("adjustDlg", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.upButton.setText(QtGui.QApplication.translate("adjustDlg", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
        self.downButton.setText(QtGui.QApplication.translate("adjustDlg", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
        self.delButton.setText(QtGui.QApplication.translate("adjustDlg", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.sortButton.setText(QtGui.QApplication.translate("adjustDlg", "Sort", None, QtGui.QApplication.UnicodeUTF8))
        self.setDefaultsButton.setText(QtGui.QApplication.translate("adjustDlg", "Set Defaults", None, QtGui.QApplication.UnicodeUTF8))

import Betty_rc
