'''
Created on 1 Feb 2010

@author: Mike Thomas

'''
from ui_Betty_MainWindow import Ui_Betty_MainWindow
from PyQt4.QtGui import QMainWindow, QTableWidgetItem, QApplication, QMessageBox
from PyQt4.QtCore import QVariant, Qt, pyqtSignature, QString
import sys
import Race
import editHorseDlg

class BettyMain(QMainWindow, Ui_Betty_MainWindow):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(BettyMain, self).__init__(parent)
        self.setupUi(self)
        self.race = Race.EmptyRace()
        self.__currentHorse = None
        self.updateTable()

    def updateTable(self, current = None):
        self.raceTable.clear()
        self.raceTable.setRowCount(len(self.race))
        self.raceTable.setColumnCount(self.race.numColumns)
        self.raceTable.setHorizontalHeaderLabels(self.race.columnTitles())
        selected = None
        for row, horse in enumerate(self.race):
            for col, item in enumerate(self.horseItems(horse)):
                if col == 0:
                    if current == horse.id:
                        selected = item
                    item.setData(Qt.UserRole, QVariant(long(horse.id)))
                self.raceTable.setItem(row, col, item)
        self.raceTable.resizeColumnsToContents()
        if selected is None:
            self.editButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            selected.setSelected(True)
            self.raceTable.setCurrentItem(selected)
            self.raceTable.scrollToItem(selected)

    def horseItems(self, horse):
        for var in self.race.iterHorse(horse):
            print var
            if isinstance(var, basestring) or isinstance(var, QString):
                yield QTableWidgetItem(var)
            elif isinstance(var, int):
                yield QTableWidgetItem("%d" % var)
            else:
                QMessageBox.warning(self, "Horse item error",
                                    "Unknown type of horse item: %s" % str(type(var)))

    @pyqtSignature("")
    def on_addButton_clicked(self):
        h = self.race.addHorse()
        self.updateTable(h.id)

    @pyqtSignature("")
    def on_editButton_clicked(self):
        dlg = editHorseDlg.editHorseDlg(self.__currentHorse)
        if dlg.exec_():
            self.updateTable(self.__currentHorse.id)

    @pyqtSignature("")
    def on_deleteButton_clicked(self):
        self.race.delHorse(self.__currentHorse)
        self.updateTable()

    def on_raceTable_itemSelectionChanged(self):
        if self.raceTable.currentRow() >= len(self.race):
            self.__currentHorse = None
            enabled = False
        else:
            self.__currentHorse = self.race.horses[self.raceTable.currentRow()]
            enabled = True
        if(len(self.race) > 2):
            self.deleteButton.setEnabled(enabled)
        self.editButton.setEnabled(enabled)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = BettyMain()
    main.show()
    app.exec_()
