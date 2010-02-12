'''
Created on 12 Feb 2010

@author: Mike Thomas

'''

from PyQt4.QtCore import pyqtSignature, SIGNAL
from PyQt4.QtGui import QMessageBox

class upDownList(object):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''

    def setupUpDownList(self, listWidget = None, maxItems = 10,
                        getContents = None, stringify = str,
                        contents = None):
        self.listWidget = listWidget
        self.listWidget.setSortingEnabled(False)
        self.maxItems = maxItems
        self.getContents = getContents
        self.stringify = stringify
        if contents is not None:
            for item in contents:
                self.listWidget.addItem(self.stringify(item))
        self.listWidget.setCurrentRow(0)
        self.listWidget.connect(self.listWidget,
                                SIGNAL("currentRowChanged(int)"), self.checkButtons)
        self.checkButtons()

    def deleteItem(self, dlgTitle, question):
        item = self.listWidget.currentItem()
        if QMessageBox.question(self, dlgTitle,
                                question % unicode(item.text()),
                                QMessageBox.Yes | QMessageBox.Default,
                                QMessageBox.No) == QMessageBox.Yes:
            row = self.listWidget.currentRow()
            self.listWidget.takeItem(row)
            self.listWidget.setCurrentRow(min(row, self.listWidget.count() - 1))

    @pyqtSignature("")
    def on_downButton_clicked(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.takeItem(row)
        self.listWidget.insertItem(row + 1, item)
        self.listWidget.setCurrentRow(row + 1)

    @pyqtSignature("")
    def on_upButton_clicked(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.takeItem(row)
        self.listWidget.insertItem(row - 1, item)
        self.listWidget.setCurrentRow(row - 1)

    def checkButtons(self):
        enabled = False
        if self.listWidget.count() > 1:
            enabled = True
        self.delButton.setEnabled(enabled)
        self.sortButton.setEnabled(enabled)
        if self.listWidget.currentRow() > 0:
            self.upButton.setEnabled(enabled)
        else:
            self.upButton.setEnabled(False)
        if self.listWidget.currentRow() < self.listWidget.count() - 1:
            self.downButton.setEnabled(enabled)
        else:
            self.downButton.setEnabled(False)
        enabled = True
        if self.listWidget.count() >= self.maxItems:
            enabled = False
        self.addButton.setEnabled(enabled)

    @pyqtSignature("")
    def on_sortButton_clicked(self):
        values = self.getContents()
        values.sort()
        for row, value in enumerate(values):
            self.listWidget.item(row).setText(self.stringify(value))
