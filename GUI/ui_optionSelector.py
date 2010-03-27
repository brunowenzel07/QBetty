# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\Betty\src\GUI\optionSelector.ui'
#
# Created: Sat Mar 27 18:35:45 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_StringSelector(object):
    def setupUi(self, StringSelector):
        StringSelector.setObjectName("StringSelector")
        StringSelector.resize(256, 366)
        self.verticalLayout = QtGui.QVBoxLayout(StringSelector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtGui.QListWidget(StringSelector)
        self.listWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.selectButton = QtGui.QPushButton(StringSelector)
        self.selectButton.setObjectName("selectButton")
        self.horizontalLayout.addWidget(self.selectButton)
        self.cancelButton = QtGui.QPushButton(StringSelector)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(StringSelector)
        QtCore.QObject.connect(self.selectButton, QtCore.SIGNAL("clicked()"), StringSelector.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), StringSelector.reject)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.selectButton.click)
        QtCore.QMetaObject.connectSlotsByName(StringSelector)

    def retranslateUi(self, StringSelector):
        StringSelector.setWindowTitle(QtGui.QApplication.translate("StringSelector", "Select Option", None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate("StringSelector", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("StringSelector", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

