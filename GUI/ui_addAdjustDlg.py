# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\Betty\src\GUI\addAdjustDlg.ui'
#
# Created: Fri Feb 12 09:53:29 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_addAdjustDialog(object):
    def setupUi(self, addAdjustDialog):
        addAdjustDialog.setObjectName("addAdjustDialog")
        addAdjustDialog.resize(314, 78)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(addAdjustDialog.sizePolicy().hasHeightForWidth())
        addAdjustDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(addAdjustDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(addAdjustDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(addAdjustDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(addAdjustDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(addAdjustDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), addAdjustDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), addAdjustDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addAdjustDialog)

    def retranslateUi(self, addAdjustDialog):
        addAdjustDialog.setWindowTitle(QtGui.QApplication.translate("addAdjustDialog", "New Adjustment", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("addAdjustDialog", "Adjustment Name", None, QtGui.QApplication.UnicodeUTF8))

