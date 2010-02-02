'''
Created on 1 Feb 2010

@author: Mike Thomas

'''
from ui_Betty_MainWindow import Ui_Betty_MainWindow
from PyQt4.QtGui import QMainWindow, QTableWidgetItem, QApplication, QMessageBox
from PyQt4.QtCore import QVariant, Qt, pyqtSignature, QString, SIGNAL
import sys
from Model.RaceModel import RaceModel

class BettyMain(QMainWindow, Ui_Betty_MainWindow):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(BettyMain, self).__init__(parent)
        self.model = RaceModel()
        self.setupUi(self)
        self.deleteButton.setEnabled(False)
        self.raceTable.setModel(self.model)
        self.connect(self.model, SIGNAL("rowsInserted(QModelIndex,int,int)"),
                     self.check_deleteButton)
        self.connect(self.model, SIGNAL("rowsRemoved(QModelIndex,int,int)"),
                     self.check_deleteButton)
        self.resizeColumns()

    def resizeColumns(self):
        self.raceTable.resizeColumnsToContents()


    @pyqtSignature("")
    def on_addButton_clicked(self):
        row = self.model.rowCount()
        self.model.insertRows(row)
        index = self.model.index(row, 0)
        self.raceTable.setCurrentIndex(index)
        #self.raceTable.edit(index)

    @pyqtSignature("")
    def on_deleteButton_clicked(self):
        index = self.raceTable.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        name = self.model.data(self.model.index(row, 0)).toString()
        if QMessageBox.question(self, "Remove Horse",
                                QString("Remove horse %1").arg(name),
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return
        self.model.removeRows(row)
        self.resizeColumns()

    def check_deleteButton(self):
        if(self.model.rowCount() > 2):
            self.deleteButton.setEnabled(True)
        else:
            self.deleteButton.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = BettyMain()
    main.show()
    app.exec_()
