# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\Betty\src\GUI\editRoundsDlg.ui'
#
# Created: Thu Feb 11 21:14:47 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_roundsDlg(object):
    def setupUi(self, roundsDlg):
        roundsDlg.setObjectName("roundsDlg")
        roundsDlg.resize(242, 242)
        roundsDlg.setMinimumSize(QtCore.QSize(242, 242))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Horse"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        roundsDlg.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(roundsDlg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.roundListWidget = QtGui.QListWidget(roundsDlg)
        self.roundListWidget.setDragEnabled(True)
        self.roundListWidget.setObjectName("roundListWidget")
        self.horizontalLayout.addWidget(self.roundListWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addButton = QtGui.QPushButton(roundsDlg)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.upButton = QtGui.QPushButton(roundsDlg)
        self.upButton.setObjectName("upButton")
        self.verticalLayout.addWidget(self.upButton)
        self.downButton = QtGui.QPushButton(roundsDlg)
        self.downButton.setObjectName("downButton")
        self.verticalLayout.addWidget(self.downButton)
        self.delButton = QtGui.QPushButton(roundsDlg)
        self.delButton.setObjectName("delButton")
        self.verticalLayout.addWidget(self.delButton)
        self.sortButton = QtGui.QPushButton(roundsDlg)
        self.sortButton.setObjectName("sortButton")
        self.verticalLayout.addWidget(self.sortButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(roundsDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(roundsDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), roundsDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), roundsDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(roundsDlg)

    def retranslateUi(self, roundsDlg):
        roundsDlg.setWindowTitle(QtGui.QApplication.translate("roundsDlg", "Edit Rounds", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("roundsDlg", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.upButton.setText(QtGui.QApplication.translate("roundsDlg", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
        self.downButton.setText(QtGui.QApplication.translate("roundsDlg", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
        self.delButton.setText(QtGui.QApplication.translate("roundsDlg", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.sortButton.setText(QtGui.QApplication.translate("roundsDlg", "Sort", None, QtGui.QApplication.UnicodeUTF8))

import Betty_rc
