'''
Created on 12 Feb 2010

@author: Mike Thomas

'''

from PyQt4.QtGui import QDialog, QApplication
from PyQt4.QtCore import pyqtSignature, Qt
from ui_editRoundsDlg import Ui_roundsDlg
from upDownList import upDownList
from addRoundDlg import addRoundDlg
from Model import RaceModel

def roundString(value):
    return "%d" % value

class editRoundsDlg(Ui_roundsDlg, QDialog, upDownList):
    '''
    classdocs
    '''


    def __init__(self, model, parent = None):
        '''
        Constructor
        '''
        super(editRoundsDlg, self).__init__(parent)
        self.setupUi(self)
        content = [int(r) for r in model.roundSizes()]
        self.setupUpDownList(listWidget = self.roundListWidget,
                          getContents = self.getRounds,
                          stringify = roundString,
                          contents = content)

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
        self.deleteItem("Delete Round", "Delete %s%% round?")

    def getRounds(self):
        return [int(self.roundListWidget.item(row).text()) for row in range(0, self.roundListWidget.count())]


def main():
    racemodel = RaceModel.RaceModel()
    import sys
    app_ = QApplication(sys.argv)
    dlg = editRoundsDlg(racemodel)
    dlg.exec_()
    print dlg.getRounds()

if __name__ == "__main__":
    main()
