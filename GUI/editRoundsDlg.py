'''
Created on 12 Feb 2010

@author: Mike Thomas

'''

from PyQt4.QtGui import QDialog, QApplication, QMessageBox, QListWidgetItem
from PyQt4.QtCore import pyqtSignature, SIGNAL, Qt
from ui_editRoundsDlg import Ui_roundsDlg
from addRoundDlg import addRoundDlg
from Model import RaceModel

def roundString(value):
    return "%d" % value

class editRoundsDlg(Ui_roundsDlg, QDialog):
    '''
    classdocs
    '''


    def __init__(self, model, parent = None):
        '''
        Constructor
        '''
        self.model = model
        super(editRoundsDlg, self).__init__(parent)
        self.setupUi(self)
        content = [int(r) for r in model.roundSizes()]
        self.roundListWidget.setSortingEnabled(False)
        for round in content:
            self.roundListWidget.addItem(roundString(round))
        self.roundListWidget.setCurrentRow(0)
        self.connect(self.roundListWidget, SIGNAL("currentRowChanged(int)"), self.checkButtons)
        self.checkButtons()

    @pyqtSignature("")
    def on_addButton_clicked(self):
        addDlg = addRoundDlg(self)
        if addDlg.exec_():
            value = addDlg.spinBox.value()
            if len(self.roundListWidget.findItems(roundString(value), Qt.MatchExactly)) == 0:
                self.roundListWidget.addItem(roundString(value))
                self.roundListWidget.setCurrentRow(self.roundListWidget.count() - 1)

    @pyqtSignature("")
    def on_delButton_clicked(self):
        item = self.roundListWidget.currentItem()
        if QMessageBox.question(self, "Delete Round",
                                "Delete %s round?" % unicode(item.text()),
                                QMessageBox.Yes | QMessageBox.Default,
                                QMessageBox.No) == QMessageBox.Yes:
            row = self.roundListWidget.currentRow()
            self.roundListWidget.takeItem(row)
            self.roundListWidget.setCurrentRow(min(row, self.roundListWidget.count() - 1))

    @pyqtSignature("")
    def on_downButton_clicked(self):
        row = self.roundListWidget.currentRow()
        item = self.roundListWidget.takeItem(row)
        self.roundListWidget.insertItem(row + 1, item)
        self.roundListWidget.setCurrentRow(row + 1)

    @pyqtSignature("")
    def on_upButton_clicked(self):
        row = self.roundListWidget.currentRow()
        item = self.roundListWidget.takeItem(row)
        self.roundListWidget.insertItem(row - 1, item)
        self.roundListWidget.setCurrentRow(row - 1)

    def checkButtons(self):
        enabled = False
        if self.roundListWidget.count() > 1:
            enabled = True
        self.delButton.setEnabled(enabled)
        self.sortButton.setEnabled(enabled)
        if self.roundListWidget.currentRow() > 0:
            self.upButton.setEnabled(enabled)
        else:
            self.upButton.setEnabled(False)
        if self.roundListWidget.currentRow() < self.roundListWidget.count() - 1:
            self.downButton.setEnabled(enabled)
        else:
            self.downButton.setEnabled(False)
        enabled = True
        if self.roundListWidget.count() >= 10:
            enabled = False
        self.addButton.setEnabled(enabled)

    @pyqtSignature("")
    def on_sortButton_clicked(self):
        values = self.getRounds()
        values.sort()
        for row, value in enumerate(values):
            self.roundListWidget.item(row).setText(roundString(value))

    def getRounds(self):
        return [int(self.roundListWidget.item(row).text()) for row in range(0, self.roundListWidget.count())]


if __name__ == "__main__":
    model = RaceModel.RaceModel()
    import sys
    app = QApplication(sys.argv)
    dlg = editRoundsDlg(model)
    dlg.exec_()
    print dlg.getRounds()

