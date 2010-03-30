'''
Created on 2 Feb 2010

@author: Mike Thomas

'''

from PyQt4.QtCore import QAbstractTableModel, QModelIndex, QVariant
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QFont
from Data.Race import emptyRace, Race
from Model.Chance import Round
from Model import Chance
from Data import Adjustments, Horse

def makeRaceProperty(attribute):
    def fget(self):
        return self.race.__getattribute__(attribute)
    def fset(self, value):
        if value != self.race.__getattribute__(attribute):
            self.dirty = True
        return self.race.__setattr__(attribute, value)
    return property(fget, fset)

def setDefaultAdjustments(adjustList):
    Adjustments.defaultAdjustmentNames = tuple(adjustList)

def getDefaultAdjustments():
    return tuple(Adjustments.defaultAdjustmentNames)

class RaceModel(QAbstractTableModel):
    '''
    classdocs
    '''
    def __init__(self, filename = None, rounds = None):
        '''
        Constructor
        '''
        super(RaceModel, self).__init__()
        self.filename = None
        self.dirty = False
        self.oddsDisplay = Chance.DecimalOddsDisplay
        self.race = None
        self.rounds = []
        self.horseSorter = Horse.cmpHorseByInsertion
        self.horseList = []
        self.__columnMaps = {}
        self.makeColumns("name")
        self.makeColumns("rating")
        self.makeColumns("adjRating")
        self.makeColumns("adjust")
        self.makeColumns("round")
        self.load(filename)
        self.setColumnMaps()
        self.setRounds(rounds)
        self.updateOdds()

    def __getDirty(self):
        return self.__dirty

    def __setDirty(self, value):
        self.__dirty = value
        self.emit(SIGNAL("dirtied"))

    dirty = property(__getDirty, __setDirty, None,
                     "Boolean indicating that data has changed since saving.")

    racename = makeRaceProperty("name")
    raceclass = makeRaceProperty("raceClass")
    course = makeRaceProperty("course")
    distance = makeRaceProperty("distance")
    date = makeRaceProperty("date")
    time = makeRaceProperty("time")
    prize = makeRaceProperty("prize")

    def makeColumns(self, columnGroup):
        self.__columnMaps[columnGroup] = {}
        getColName = "%sColumn" % columnGroup
        def getCol(slf, index):
            if isinstance(index, QModelIndex):
                return slf.__columnMaps[columnGroup][index.column()]
            else:
                return slf.__columnMaps[columnGroup][index]
        self.__setattr__(getColName, getCol)

    def isColumn(self, columnGroup, index):
        if isinstance(index, QModelIndex):
            return self.isColumn(columnGroup, index.column())
        else:
            return index in self.__columnMaps[columnGroup]

    def getColumn(self, columnGroup, index):
        if isinstance(index, QModelIndex):
            return self.getColumn(columnGroup, index.column())
        else:
            return self.__columnMaps[columnGroup][index]

    def __setColumnMap(self, mapName, startCol, iterator):
        total = 0
        self.__columnMaps[mapName] = {}
        for index in iterator:
            self.__columnMaps[mapName][startCol + total] = index
            total += 1
        return total

    def setColumnMaps(self):
        for colMap in self.__columnMaps:
            self.__columnMaps[colMap] = {}
        column = self.__setColumnMap("name", 0, xrange(0, 1))
        column += self.__setColumnMap("rating", column,
                                      xrange(0, Horse.Horse.numRatings))
        column += self.__setColumnMap("adjust", column,
                                      xrange(0, len(self.race.adjusts)))
        column += self.__setColumnMap("adjRating", column,
                                      xrange(0, Horse.Horse.numRatings))
        column += self.__setColumnMap("round", column,
                                      xrange(0, len(self.rounds)))

    def rowCount(self, index = QModelIndex()): #@UnusedVariable
        return len(self.race)

    def columnCount(self, index = QModelIndex()): #@UnusedVariable
        return int(len(self.race.adjusts) +
                   (Horse.Horse.numRatings * 2) + 1 + len(self.rounds))

    def data(self, index, role = Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.race))):
            return QVariant()
        horse = self.horseList[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            retVal = QVariant()
            if self.isColumn("name", column):
                retVal = QVariant(horse.name)
            elif self.isColumn("rating", column):
                retVal = QVariant(horse[self.getColumn("rating", column)])
            elif self.isColumn("adjust", column):
                index = self.getColumn("adjust", column)
                adjust = self.race.adjusts[index]
                retVal = QVariant(self.race.adjusts.getAdjust(adjust, horse))
            elif self.isColumn("adjRating", column):
                index = self.getColumn("adjRating", column)
                rating = self.race.adjusts.getAdjustedRating(horse, index)
                retVal = QVariant(rating)
            elif self.isColumn("round", column):
                index = self.getColumn("round", column)
                odds = self.rounds[index].convert(horse.prob)
                retVal = QVariant(self.oddsDisplay.display(odds))
            return retVal
        elif role == Qt.TextAlignmentRole:
            if self.isColumn("name", column):
                return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
            else:
                return QVariant(int(Qt.AlignRight | Qt.AlignVCenter))
        elif role == Qt.FontRole:
            if self.isColumn("round", column):
                font = QFont()
                font.setBold(True)
                return QVariant(font)
            elif self.isColumn("adjRating", column):
                font = QFont()
                font.setItalic(True)
                return QVariant(font)
            else:
                return QVariant()
        return QVariant()

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        retVal = QVariant()
        if role != Qt.DisplayRole:
            return retVal
        if orientation == Qt.Horizontal:
            if self.isColumn("name", section):
                retVal = QVariant("Horse name")
            elif self.isColumn("rating", section):
                index = self.getColumn("rating", section)
                retVal = QVariant(Horse.Horse.ratingTitles[index])
            elif self.isColumn("adjust", section):
                index = self.getColumn("adjust", section)
                retVal = QVariant(self.race.adjusts[index])
            elif self.isColumn("adjRating", section):
                index = self.getColumn("adjRating", section)
                retVal = QVariant("Adjusted\n" + Horse.Horse.ratingTitles[index])
            elif self.isColumn("round", section):
                index = self.getColumn("round", section)
                retVal = QVariant("%d%%" % self.rounds[index].roundVal)
        else:
            retVal = QVariant(int(section + 1))
        return retVal

    def updateOdds(self):
        self.race.calculate()
        self.sortHorses()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if self.isColumn("round", index) or self.isColumn("adjRating", index):
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index))
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
                            Qt.ItemIsEditable)

    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.race):
            horse = self.horseList[index.row()]
            column = index.column()
            if self.isColumn("name", column):
                horse.name = value.toString()
            elif self.isColumn("rating", column):
                colIndex = self.getColumn("rating", column)
                value, ok = value.toInt()
                if ok:
                    horse[colIndex] = value
            elif self.isColumn("adjust", column):
                colIndex = self.getColumn("adjust", column)
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
        horses = [self.horseList[i] for i in xrange(position, position + rows)]
        for h in horses:
            self.race.delHorse(h)
        self.endRemoveRows()
        self.updateOdds()
        self.dirty = True
        return True

    def setOddsDisplay(self, displayer):
        self.oddsDisplay = displayer
        self.reset()

    def setSortOrder(self, orderFunc):
        self.horseSorter = orderFunc
        self.sortHorses()

    def sortHorses(self):
        self.horseList = list(self.race.horses)
        self.horseList.sort(cmp = self.horseSorter)
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
                    self.race = emptyRace()
                return False
            self.setColumnMaps()
            self.reset()
            self.updateOdds()
            self.dirty = False
            return True
        else:
            self.race = emptyRace()
            self.reset()
            self.updateOdds()
            self.dirty = False
            return False

    def newRace(self):
        self.race = emptyRace()
        self.setColumnMaps()
        self.reset()
        self.updateOdds()
        self.filename = None
        self.dirty = False

    def newDownload(self, newRace):
        self.race = newRace
        self.setAdjustNames(getDefaultAdjustments())
        self.setColumnMaps()
        self.reset()
        self.updateOdds()
        self.filename = None
        self.dirty = True

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

    def roundSizes(self):
        return ["%d" % int(thisRound.roundVal) for thisRound in self.rounds]

    def setRounds(self, roundList = None):
        if roundList is None:
            self.rounds = [Round(70), Round(), Round(130)]
        else:
            self.rounds = [Round(r) for r in roundList]
        self.setColumnMaps()
        self.reset()

    def getAdjustNames(self):
        return tuple([a for a in self.race.adjusts])

    def setAdjustNames(self, adjustList):
        self.race.adjusts.reset(adjustList)
        self.setColumnMaps()
        self.reset()
        self.dirty = True


