'''
Created on 12 Feb 2010

@author: Mike Thomas

'''

from ui_editAdjustDlg import Ui_adjustDlg
from upDownList import upDownList
from PyQt4.QtGui import QDialog, QApplication
from PyQt4.QtCore import pyqtSignature, Qt
from Model import RaceModel
from addAdjustDlg import addAdjustDlg

class editAdjustDlg(Ui_adjustDlg, QDialog, upDownList):
    '''
    classdocs
    '''


    def __init__(self, model, parent = None):
        '''
        Constructor
        '''
        super(editAdjustDlg, self).__init__(parent)
        self.setupUi(self)
        content = model.getAdjustNames()
        self.setupUpDownList(listWidget = self.adjustListWidget,
                          getContents = self.getAdjusts,
                          contents = content)

    @pyqtSignature("")
    def on_addButton_clicked(self):
        addDlg = addAdjustDlg(self)
        if addDlg.exec_():
            value = addDlg.lineEdit.text()
            if len(self.adjustListWidget.findItems(value, Qt.MatchExactly)) == 0:
                self.adjustListWidget.addItem(value)
                self.adjustListWidget.setCurrentRow(self.adjustListWidget.count() - 1)

    @pyqtSignature("")
    def on_delButton_clicked(self):
        self.deleteItem("Delete Adjustment", "Delete %s adjustment?")

    def getAdjusts(self):
        return [unicode(self.adjustListWidget.item(row).text())
                for row in range(0, self.adjustListWidget.count())]

    def makeDefault(self):
        return self.checkBox.isChecked()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    racemodel = RaceModel.RaceModel()
    dlg = editAdjustDlg(racemodel)
    dlg.exec_()
    print dlg.getAdjusts()
