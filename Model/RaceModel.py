'''
Created on 2 Feb 2010

@author: Mike Thomas

'''

from PyQt4.Qt import QAbstractTableModel, QModelIndex, QVariant
from PyQt4.QtCore import Qt, SIGNAL
from Data.Race import EmptyRace, Race
from Data.Horse import Horse
from Model.Chance import Round
from Model import Chance

def makeRaceProperty(attribute):
    def fget(self):
        return self.race.__getattribute__(attribute)
    def fset(self, value):
        if value != self.race.__getattribute__(attribute):
            self.dirty = True
        return self.race.__setattr__(attribute, value)
    return property(fget, fset)



class RaceModel(QAbstractTableModel):
    '''
    classdocs
    '''


    def __init__(self, filename = None):
        '''
        Constructor
        '''
        super(RaceModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.oddsDisplay = Chance.DecimalOddsDisplay
        self.race = None
        self.load()
        self.rounds = [Round(70), Round(), Round(130)]
        self.ratingColumns = {}
        self.adjRatingColumns = {}
        self.adjustColumns = {}
        self.roundColumns = {}
        self.setColumnMap()
        self.updateOdds()


    racename = makeRaceProperty("name")
    raceclass = makeRaceProperty("raceClass")
    course = makeRaceProperty("course")
    distance = makeRaceProperty("distance")
    date = makeRaceProperty("date")
    time = makeRaceProperty("time")
    prize = makeRaceProperty("prize")

    def setColumnMap(self):
        self.ratingColumns = {}
        self.adjRatingColumns = {}
        self.adjustColumns = {}
        self.roundColumns = {}
        column = 1
        for index in xrange(0, Horse.numRatings):
            self.ratingColumns[column] = index
            column += 1
        for index in xrange(0, len(self.race.adjusts)):
            self.adjustColumns[column] = index
            column += 1
        for index in xrange(0, Horse.numRatings):
            self.adjRatingColumns[column] = index
            column += 1
        for index, round in enumerate(self.rounds):
            self.roundColumns[column] = index
            column += 1

    def rowCount(self, index = QModelIndex()):
        return len(self.race)

    def columnCount(self, index = QModelIndex()):
        return len(self.race.adjusts) + (Horse.numRatings * 2) + 1 + len(self.rounds)

    def data(self, index, role = Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.race))):
            return QVariant()
        horse = self.race[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(horse.name)
            elif column in self.ratingColumns:
                return QVariant(horse[self.ratingColumns[column]])
            elif column in self.adjustColumns:
                index = self.adjustColumns[column]
                return QVariant(self.race.adjusts.getAdjust(self.race.adjusts[index],
                                                             horse))
            elif column in self.adjRatingColumns:
                index = self.adjRatingColumns[column]
                return QVariant(self.race.adjusts.getAdjustedRating(horse, index))
            elif column in self.roundColumns:
                index = self.roundColumns[column]
                return QVariant(self.oddsDisplay.display(self.rounds[index].convert(horse.prob)))
        return QVariant()

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == 0:
                return QVariant("Horse name")
            elif section in self.ratingColumns:
                index = self.ratingColumns[section]
                return QVariant(Horse.ratingTitles[index])
            elif section in self.adjustColumns:
                index = self.adjustColumns[section]
                return QVariant(self.race.adjusts[index])
            elif section in self.adjRatingColumns:
                index = self.adjRatingColumns[section]
                return QVariant("Adjusted " + Horse.ratingTitles[index])
            elif section in self.roundColumns:
                index = self.roundColumns[section]
                return QVariant("%d%%" % self.rounds[index].roundVal)
            else:
                return QVariant(int(section + 1))
        return QVariant()

    def updateOdds(self):
        self.race.calculate()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() in self.roundColumns or index.column() in self.adjRatingColumns:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index))
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
                            Qt.ItemIsEditable)

    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.race):
            horse = self.race[index.row()]
            column = index.column()
            if column == 0:
                horse.name = value.toString()
            elif column in self.ratingColumns:
                colIndex = self.ratingColumns[column]
                value, ok = value.toInt()
                if ok:
                    horse[colIndex] = value
            elif column in self.adjustColumns:
                colIndex = self.adjustColumns[column]
                value, ok = value.toInt()
                if ok:
                    self.race.adjusts.setAdjust(colIndex, horse, value)
            else:
                return False
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            self.updateOdds()
            return True
        return False

    def insertRows(self, position, rows = 1, index = QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in xrange(rows):
            self.race.insert(position + row)
        self.endInsertRows()
        self.updateOdds()
        self.dirty = True
        return True

    def removeRows(self, position, rows = 1, index = QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        horses = [self.race[i] for i in xrange(position, position + rows)]
        for h in horses:
            self.race.delHorse(h)
        self.endRemoveRows()
        self.updateOdds()
        self.dirty = True
        return True

    def setOddsDisplay(self, displayer):
        self.oddsDisplay = displayer
        self.reset()

    def load(self, filename = None):
        oldfile = self.filename
        oldrace = self.race
        if filename is not None:
            self.filename = filename
        if self.filename is not None:
            self.race = Race()
            if not self.race.load(self.filename):
                self.race = oldrace
                self.filename = oldfile
                if oldrace is None:
                    self.race = EmptyRace()
                return False
            self.setColumnMap()
            self.reset()
            self.updateOdds()
            self.dirty = False
            return True
        else:
            self.race = EmptyRace()
            self.reset()
            self.updateOdds()
            self.dirty = False
            return False

    def newRace(self):
        self.race = EmptyRace()
        self.reset()
        self.updateOdds()
        self.dirty = False


    def save(self, filename = None):
        if filename is not None:
            self.filename = unicode(filename)
        if self.filename is not None:
            if not self.race.save(self.filename):
                self.filename = None
                return False
            self.dirty = False
            return True
        return False
