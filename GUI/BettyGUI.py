'''
Created on 1 Feb 2010

@author: Mike Thomas

'''
import os
from PyQt4.QtGui import (QMainWindow, QApplication,
                         QMessageBox, QFileDialog, QRadioButton)
from PyQt4.QtCore import (pyqtSignature, QString, SIGNAL, QDate,
                          QTime, QSettings, QVariant, QSize, QPoint,
                          QStringList, Qt)
import sys
from ui_Betty_MainWindow import Ui_Betty_MainWindow
from Model.RaceModel import (RaceModel,
                             getDefaultAdjustments, setDefaultAdjustments)
from Model import Chance, RaceCourses
from RaceDelegate import RaceDelegate
from editRoundsDlg import editRoundsDlg
from editAdjustDlg import editAdjustDlg
from Data import Horse
import raceSelector

APPNAME = "Betty"
APPVERSION = "0.6"

def setCombo(combo, itemText):
    itemList = [unicode(combo.itemText(i)) for
        i in xrange(0, combo.count())]
    if itemText in itemList:
        combo.setCurrentIndex(itemList.index(itemText))
    else:
        combo.addItem(itemText)
        combo.setCurrentIndex(combo.count() - 1)

class BettyMain(QMainWindow, Ui_Betty_MainWindow):
    '''
    classdocs
    '''

    __formatExtension = "*.bty"

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(BettyMain, self).__init__(parent)
        state, size, pos = self.__readSettings()
        self.setupUi(self)
        self.__setupCourseCombo()
        self.__makeAllOddsButtons()
        self.__makeAllSortButtons()
        self.deleteButton.setEnabled(False)
        self.raceTable.setGridStyle(Qt.NoPen)
        self.raceTable.setModel(self.model)
        self.raceTable.setItemDelegate(RaceDelegate(self))
        self.connect(self.model, SIGNAL("rowsInserted(QModelIndex,int,int)"),
                     self.__check_deleteButton)
        self.connect(self.model, SIGNAL("rowsRemoved(QModelIndex,int,int)"),
                     self.__check_deleteButton)
        self.__loadButtonSettings()
        self.reset()
        self.connect(self.model, SIGNAL("dirtied"), self.dirtied)
        self.move(pos)
        self.resize(size)
        self.restoreState(state)

    def __readSettings(self):
        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles").toStringList()
        filename = unicode(settings.value("LastFile").toString())
        self.currentDir = os.path.dirname(filename)
        if len(filename) == 0:
            filename = None
        size = settings.value("MainWindow/Size", QVariant(QSize(100, 500))).toSize()
        pos = settings.value("MainWindow/Position", QVariant(QPoint(100, 100))).toPoint()
        state = settings.value("MainWindow/State").toByteArray()
        rounds = settings.value("Rounds").toStringList()
        adjusts = settings.value("DefaultAdjusts").toStringList()
        self.__oddsDisplay = unicode(settings.value("OddsSetting").toString())
        self.__sortOrder = unicode(settings.value("SortSetting").toString())
        if len(adjusts) > 0:
            setDefaultAdjustments([unicode(a) for a in adjusts])
        if len(rounds) > 0:
            rounds = [int(unicode(r)) for r in rounds]
        else:
            rounds = None
        self.model = RaceModel(filename, rounds = rounds)
        return state, size, pos


    def __loadButtonSettings(self):
        try:
            button = getattr(self, "%sButton" % self.__oddsDisplay)
            button.click()
        except AttributeError:
            implementedButton = [x for x in Chance.oddsList if Chance.oddsMap[x].implemented][0]
            button = getattr(self, "%sButton" % implementedButton)
            button.click()
        try:
            button = getattr(self, "%sSortButton" % self.__sortOrder)
            button.click()
        except AttributeError:
            implementedButton = [x for x in Horse.horseSortList][0]
            button = getattr(self, "%sSortButton" % implementedButton)
            button.click()

    def __setupCourseCombo(self):
        self.courseCombo.clear()
        self.courseCombo.addItem("Unknown")
        self.courseCombo.addItems(RaceCourses.ukCourses)
        setCombo(self.courseCombo, self.model.course)

    def __makeAllOddsButtons(self):
        def makeOddsButton(name, oddsDisplayer):
            bname = "%sButton" % name
            button = QRadioButton(self.oddsGroupBox)
            setattr(self, bname, button)
            def buttonClicked():
                self.__oddsDisplay = name
                self.model.setOddsDisplay(oddsDisplayer)
            self.connect(button, SIGNAL("clicked()"),
                         buttonClicked)
            button.setEnabled(oddsDisplayer.implemented)
            self.oddsLayout.addWidget(button)
            button.setText(name.capitalize())
        for oddsName in Chance.oddsList:
            makeOddsButton(oddsName, Chance.oddsMap[oddsName])

    def __makeAllSortButtons(self):
        def makeSortButton(name, sortFunction):
            bname = "%sSortButton" % name
            button = QRadioButton(self.sortBox)
            setattr(self, bname, button)
            def buttonClicked():
                self.__sortOrder = name
                self.model.setSortOrder(sortFunction)
            self.connect(button, SIGNAL("clicked()"),
                         buttonClicked)
            self.sortLayout.addWidget(button)
            button.setText("By %s" % name.capitalize())
        for sortName in Horse.horseSortList:
            makeSortButton(sortName, Horse.horseSortMap[sortName])

    def reset(self):
        self.populateInfo()
        self.resizeColumns()
        self.__check_deleteButton()
        if self.model.filename is None:
            self.setWindowTitle("%s v%s - Unnamed[*]" % (APPNAME, APPVERSION))
        else:
            self.setWindowTitle("%s v%s - %s[*]" %
                                (APPNAME, APPVERSION,
                                 os.path.basename(self.model.filename)))
        self.setWindowModified(self.model.dirty)

    def dirtied(self):
        self.setWindowModified(self.model.dirty)

    def resizeColumns(self):
        self.raceTable.resizeColumnsToContents()

    def populateInfo(self):
        self.nameEdit.setText(self.model.racename)
        setCombo(self.courseCombo, self.model.course)
        setCombo(self.classCombo, self.model.raceclass)
        self.prizeSpinner.setValue(self.model.prize)
        if self.model.date is None:
            self.dateEdit.setDate(QDate.currentDate())
        else:
            self.dateEdit.setDate(QDate.fromString(self.model.date, QString("dd/MM/yyyy")))
        if self.model.time is None:
            self.timeEdit.setTime(QTime(12, 0))
        else:
            self.timeEdit.setTime(QTime.fromString(self.model.time, QString("hh:mm")))
        miles = self.model.distance / 8
        furlongs = self.model.distance % 8
        self.milesSpinner.setValue(miles)
        self.furlongCombo.setCurrentIndex(furlongs)
        self.__setNumRunners()

    def __setNumRunners(self):
        self.RunnerLabel.setText("%d" % self.model.rowCount())

    @pyqtSignature("")
    def on_addButton_clicked(self):
        row = self.model.rowCount()
        self.model.insertRows(row)
        index = self.model.index(row, 0)
        self.raceTable.setCurrentIndex(index)
        self.raceTable.edit(index)
        self.__setNumRunners()

    @pyqtSignature("")
    def on_deleteButton_clicked(self):
        index = self.raceTable.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        name = self.model.data(self.model.index(row, 0)).toString()
        answer = QMessageBox.question(self, "Remove Horse",
                                      QString("Remove horse %1").arg(name),
                                      QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.No:
            return
        self.model.removeRows(row)
        self.resizeColumns()
        self.__setNumRunners()

    @pyqtSignature("QString")
    def on_nameEdit_textChanged(self):
        self.model.racename = unicode(self.nameEdit.text())

    @pyqtSignature("QString")
    def on_courseCombo_activated(self):
        self.model.course = unicode(self.courseCombo.currentText())

    @pyqtSignature("QString")
    def on_courseCombo_editTextChanged(self, text):
        self.model.course = unicode(text)

    @pyqtSignature("QString")
    def on_classCombo_activated(self):
        self.model.raceclass = unicode(self.classCombo.currentText())

    @pyqtSignature("int")
    def on_milesSpinner_valueChanged(self):
        self.model.distance = self.__calculateDistance()

    @pyqtSignature("QString")
    def on_furlongCombo_activated(self):
        self.model.distance = self.__calculateDistance()

    def __calculateDistance(self):
        return int(self.milesSpinner.value() * 8
                   + self.furlongCombo.currentIndex())

    @pyqtSignature("QString")
    def on_classCombo_editTextChanged(self, text):
        self.model.raceclass = unicode(text)

    @pyqtSignature("QDate")
    def on_dateEdit_dateChanged(self, date):
        self.model.date = unicode(date.toString("dd/MM/yyyy"))

    @pyqtSignature("QTime")
    def on_timeEdit_timeChanged(self, time):
        self.model.time = unicode(time.toString("hh:mm"))

    @pyqtSignature("int")
    def on_prizeSpinner_valueChanged(self):
        self.model.prize = int(self.prizeSpinner.value())

    @pyqtSignature("")
    def on_actionNew_triggered(self):
        if not self.__okToContinue():
            return
        self.model.newRace()
        self.reset()

    @pyqtSignature("")
    def on_actionSave_triggered(self):
        self.__fileSave()

    @pyqtSignature("")
    def on_actionSave_As_triggered(self):
        self.__fileSaveAs()

    @pyqtSignature("")
    def on_actionOpen_triggered(self):
        self.__fileOpen()

    @pyqtSignature("")
    def on_actionAbout_triggered(self):
        message = "%s v%s" % (APPNAME, APPVERSION)
        message += os.linesep
        message += "Copyright Mike Thomas 2010"
        QMessageBox.about(self, "About...", message)

    @pyqtSignature("")
    def on_actionDownload_triggered(self):
        if not self.__okToContinue():
            return
        dlg = raceSelector.raceSelector(self)
        if not dlg.exec_():
            return
        newRace = dlg.race
        if newRace is None:
            return
        self.model.newDownload(newRace)
        self.reset()

    @pyqtSignature("")
    def on_editRoundsButton_clicked(self):
        dlg = editRoundsDlg(self.model, self)
        if dlg.exec_():
            self.model.setRounds(dlg.getRounds())
            self.reset()

    @pyqtSignature("")
    def on_editAdjustsButton_clicked(self):
        dlg = editAdjustDlg(self.model)
        if dlg.exec_():
            self.model.setAdjustNames(dlg.getAdjusts())
            if dlg.makeDefault():
                setDefaultAdjustments(dlg.getAdjusts())
            self.reset()

    def __okToContinue(self):
        if not self.model.dirty:
            return True
        reply = QMessageBox.question(self, "Betty - Unsaved Changes",
                                     "Save unsaved changes?",
                                     buttons = QMessageBox.Yes |
                                     QMessageBox.No | QMessageBox.Cancel,
                                     defaultButton = QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
            return False
        elif reply == QMessageBox.Yes:
            return self.__fileSave()
        return True

    def __fileSave(self, filename = None):
        if filename is None:
            filename = self.model.filename
        if filename is None:
            return self.__fileSaveAs()
        else:
            if not self.model.save(filename):
                QMessageBox.warning(self, "File Error",
                                    "Could not save %s" % filename)
                return False
            self.currentDir = os.path.dirname(self.model.filename)
            self.reset()
            return True

    def __fileSaveAs(self):
        extensionName = "Betty files (%s)" % self.__formatExtension
        path = os.path.join(self.currentDir, "_".join([str(self.dateEdit.date().toString("yyyyMMdd")),
                                                       self.model.course,
                                                       str(self.timeEdit.time().toString("hhmm"))]))
        filename = QFileDialog.getSaveFileName(self,
                                               "Betty - Save Race As",
                                               path,
                                               extensionName)
        if not filename.isEmpty():
            if not filename.contains("."):
                filename += self.__formatExtension
            return self.__fileSave(filename)
        else:
            return False

    def __fileOpen(self):
        if not self.__okToContinue():
            return
        extensionName = "Betty files (%s)" % self.__formatExtension
        filename = QFileDialog.getOpenFileName(self,
                                               "Betty - Load Race",
                                               self.currentDir,
                                               extensionName)
        if not filename.isEmpty():
            if self.model.load(unicode(filename)):
                self.currentDir = os.path.dirname(self.model.filename)
                self.reset()
            else:
                QMessageBox.warning(self, "File Error",
                                    "Could not load %s" % filename)

    def __check_deleteButton(self):
        enabled = self.model.rowCount() > 2
        self.deleteButton.setEnabled(enabled)

    def closeEvent(self, event):
        if self.__okToContinue():
            settings = QSettings()
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position", QVariant(self.pos()))
            settings.setValue("MainWindow/State", QVariant(self.saveState()))
            filename = QVariant()
            if self.model.filename is not None:
                filename = QVariant(QString(self.model.filename))
            settings.setValue("LastFile", filename)
            settings.setValue("Rounds",
                              QVariant(QStringList(self.model.roundSizes())))
            settings.setValue("DefaultAdjusts",
                              QVariant(QStringList(getDefaultAdjustments())))
            settings.setValue("OddsSetting",
                              QVariant(QString(self.__oddsDisplay)))
            settings.setValue("SortSetting",
                              QVariant(QString(self.__sortOrder)))
        else:
            event.ignore()

if __name__ == "__main__":
    import Download
    Download.RPDownloader.setTestMode()
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName(APPNAME)
    main = BettyMain()
    main.show()
    app.exec_()
