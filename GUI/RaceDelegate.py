'''
Created on 7 Feb 2010

@author: Mike Thomas

'''

from PyQt4.QtGui import QItemDelegate, QSpinBox, QLineEdit
from PyQt4.QtCore import Qt, QSize

class RaceDelegate(QItemDelegate):
    '''
    classdocs
    '''

    def sizeHint(self, option, index):
        model = index.model()
        column = index.column()
        fm = option.fontMetrics
        sample = "xxx"
        if model.isColumn("name", column):
            sample = "This is a long horse name"
        elif model.isColumn("rating", column):
            sample = "xTopspeedx"
        elif model.isColumn("adjust", column):
            sample = "Long adjust"
        elif model.isColumn("adjRating", column):
            sample = "Topspeed"
        elif model.isColumn("round", column):
            sample = "x100/30x"
        return QSize(fm.width(sample), fm.height())

    def createEditor(self, parent, option, index):
        model = index.model()
        if model.isColumn("name", index):
            textedit = QLineEdit(parent)
            return textedit
        elif model.isColumn("rating", index):
            spinbox = QSpinBox(parent)
            spinbox.setRange(0, 200)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            return spinbox
        elif model.isColumn("adjust", index):
            spinbox = QSpinBox(parent)
            spinbox.setRange(-10, 10)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            return spinbox
        else:
            return QItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        model = index.model()
        horse = model.race[index.row()]
        if model.isColumn("name", index):
            editor.setText(model.race[index.row()].name)
        elif model.isColumn("rating", index):
            ratingIndex = model.getColumn("rating", index)
            editor.setValue(horse[ratingIndex])
        elif model.isColumn("adjust", index):
            adjustIndex = model.getColumn("adjust", index)
            editor.setValue(model.race.adjusts.getAdjust(model.race.adjusts[adjustIndex], horse))
        else:
            QItemDelegate.setEditorData(self, editor, index)
