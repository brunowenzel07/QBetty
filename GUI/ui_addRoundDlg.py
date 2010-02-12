# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\Betty\src\GUI\addRoundDlg.ui'
#
# Created: Fri Feb 12 09:14:11 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_addRoundDialog(object):
    def setupUi(self, addRoundDialog):
        addRoundDialog.setObjectName("addRoundDialog")
        addRoundDialog.resize(203, 91)
        self.verticalLayout = QtGui.QVBoxLayout(addRoundDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(addRoundDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtGui.QSpinBox(addRoundDialog)
        self.spinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(200)
        self.spinBox.setSingleStep(5)
        self.spinBox.setProperty("value", 100)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(addRoundDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(addRoundDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), addRoundDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), addRoundDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addRoundDialog)

    def retranslateUi(self, addRoundDialog):
        addRoundDialog.setWindowTitle(QtGui.QApplication.translate("addRoundDialog", "Add Round", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("addRoundDialog", "New Round Value", None, QtGui.QApplication.UnicodeUTF8))

