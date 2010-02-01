'''
Created on 1 Feb 2010

@author: Mike Thomas

'''
import ui_editHorseDlg
from PyQt4.QtGui import QDialog

class editHorseDlg(QDialog, ui_editHorseDlg.Ui_editHorseDlg):
    '''
    classdocs
    '''


    def __init__(self, horse, parent = None):
        '''
        Constructor
        '''
        super(editHorseDlg, self).__init__(parent)
        self.setupUi(self)
        self.horse = horse
        self.horseEdit.setText(horse.name)
        self.rprSpinBox.setValue(horse.rpr)
        self.tsSpinBox.setValue(horse.ts)

    def on_buttonBox_accepted(self):
        self.horse.name = unicode(self.horseEdit.text())
        self.horse.rpr = self.rprSpinBox.value()
        self.horse.ts = self.tsSpinBox.value()


if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    from Horse import Horse
    app = QApplication(sys.argv)
    h = Horse()
    form = editHorseDlg(h)
    form.show()
    app.exec_()
    print h.name, h.rpr, h.ts
