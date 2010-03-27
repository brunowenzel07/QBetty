'''
Created on 27 Mar 2010

@author: Mike Thomas

'''

from ui_optionSelector import Ui_StringSelector
from PyQt4.QtGui import QDialog, QApplication
from PyQt4.QtCore import QString, SIGNAL

class optionSelector(Ui_StringSelector, QDialog):
    '''
    classdocs
    '''


    def __init__(self, title, optionList, parent = None):
        '''
        Constructor
        '''
        super(optionSelector, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.listWidget.setSortingEnabled(False)
        for item in optionList:
            self.listWidget.addItem(QString(item))
        self.listWidget.connect(self.listWidget,
                                SIGNAL("currentRowChanged(int)"),
                                self.checkButtons)
        self.listWidget.setCurrentRow(0)

    def checkButtons(self):
        enabled = self.listWidget.currentRow() > -1
        self.selectButton.setEnabled(enabled)

    def getOptionIndex(self):
        return self.listWidget.currentRow()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = optionSelector("Select an option", ["a", "b", "c"])
    dlg.exec_()

