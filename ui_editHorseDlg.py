# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\Betty\src\editHorseDlg.ui'
#
# Created: Mon Feb 01 01:42:22 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_editHorseDlg(object):
    def setupUi(self, editHorseDlg):
        editHorseDlg.setObjectName("editHorseDlg")
        editHorseDlg.resize(400, 300)
        self.verticalLayout_3 = QtGui.QVBoxLayout(editHorseDlg)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(editHorseDlg)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.horseEdit = QtGui.QLineEdit(editHorseDlg)
        self.horseEdit.setObjectName("horseEdit")
        self.horizontalLayout_2.addWidget(self.horseEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtGui.QLabel(editHorseDlg)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.rprSpinBox = QtGui.QSpinBox(editHorseDlg)
        self.rprSpinBox.setMaximum(200)
        self.rprSpinBox.setObjectName("rprSpinBox")
        self.horizontalLayout.addWidget(self.rprSpinBox)
        self.label_3 = QtGui.QLabel(editHorseDlg)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.tsSpinBox = QtGui.QSpinBox(editHorseDlg)
        self.tsSpinBox.setMaximum(200)
        self.tsSpinBox.setObjectName("tsSpinBox")
        self.horizontalLayout.addWidget(self.tsSpinBox)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.groupBox = QtGui.QGroupBox(editHorseDlg)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(editHorseDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.label.setBuddy(self.horseEdit)
        self.label_2.setBuddy(self.rprSpinBox)
        self.label_3.setBuddy(self.tsSpinBox)

        self.retranslateUi(editHorseDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), editHorseDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), editHorseDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(editHorseDlg)

    def retranslateUi(self, editHorseDlg):
        editHorseDlg.setWindowTitle(QtGui.QApplication.translate("editHorseDlg", "Edit Horse Details", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("editHorseDlg", "Horse Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("editHorseDlg", "RPR", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("editHorseDlg", "Topspeed", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("editHorseDlg", "Adjustments", None, QtGui.QApplication.UnicodeUTF8))

